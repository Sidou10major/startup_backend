from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.services.recommendations import generate_recommendation_report 

from app.db.deps import get_db, get_current_user
from app.models.simulation_run import SimulationRun
from app.models.simulation_step import SimulationStep
from app.models.startup_profile import StartupProfile
from app.models.user import User
from app.schemas.simulation import (
    SimulationInput,
    SimulationResponse,
    MultiStepSimulationInput,
    MultiStepSimulationResponse,
    AllowedDecisionsResponse,
)
from app.services.simulation_engine import apply_decision, get_allowed_decisions
from app.services.rule_engine import evaluate_rule_based
from app.services.ml_model import predict_ai
from app.services.explainability import (
    explain_decision_tree,
    summarize_hybrid_result,
    get_final_decision,
)

router = APIRouter(prefix="/simulate", tags=["Simulation"])


def evaluate_state(state):
    rule_result = evaluate_rule_based(state)

    ai_raw = predict_ai(state)
    ai_explanation = explain_decision_tree(state)

    ai_result = {
        "prediction": ai_raw["prediction"],
        "label": ai_raw["label"],
        "probability": ai_raw["probability"],
        "runway": ai_raw["runway"],
        "explanation": ai_explanation,
    }

    
    rule_failure = rule_result["risk_score"] >= 0.60
    ai_failure = ai_result["label"] == "FAILURE"
    agreement = rule_failure == ai_failure

    final_decision = get_final_decision(rule_result, ai_result)
    summary = summarize_hybrid_result(rule_result, ai_result, agreement)

    risk_scores = {
        "global_risk": round(
            0.6 * ai_raw["probability"] + 0.4 * rule_result["risk_score"], 4
        )
    }
    recommendations = generate_recommendation_report(
        state,
        rule_result["derived"],
        risk_scores,
    )

    return {
        "runway": rule_result["runway"],
        "rule_based": rule_result,
        "ai_based": ai_result,
        "agreement": agreement,
        "final_decision": final_decision,
        "summary": summary,
        "recommendations": recommendations,  
    }


@router.get("/decisions", response_model=AllowedDecisionsResponse)
def list_allowed_decisions():
    return {"decisions": get_allowed_decisions()}


@router.post("/step")
def simulate_step(payload: SimulationInput):
    try:
        updated_state = apply_decision(payload.state, payload.decision)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    evaluation = evaluate_state(updated_state)

    return {
        "updated_state": updated_state,
        "runway": evaluation["runway"],
        "rule_based": evaluation["rule_based"],
        "ai_based": evaluation["ai_based"],
        "agreement": evaluation["agreement"],
        "final_decision": evaluation["final_decision"],
        "summary": evaluation["summary"],
        "recommendations": evaluation["recommendations"],  
    }


@router.post("/run")
def simulate_multiple_steps(
    payload: MultiStepSimulationInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_state = payload.initial_state
    steps = []

    startup_profile_id = payload.startup_profile_id

    if startup_profile_id is None:
        auto_profile = StartupProfile(
            user_id=current_user.id,
            name=payload.run_name or "Auto-generated startup profile",
            sector="Unknown",
            cash=payload.initial_state.cash,
            burn_rate=payload.initial_state.burn_rate,
            pmf_score=payload.initial_state.pmf_score,
            retention_rate=payload.initial_state.retention_rate,
            traction=payload.initial_state.traction,
            adaptability=payload.initial_state.adaptability,
            decision_delay=payload.initial_state.decision_delay,
            team_strength=payload.initial_state.team_strength,
            tech_debt=payload.initial_state.tech_debt,
            scalability=payload.initial_state.scalability,
            regulatory_risk=payload.initial_state.regulatory_risk,
            external_shock=payload.initial_state.external_shock,
        )
        db.add(auto_profile)
        db.commit()
        db.refresh(auto_profile)
        startup_profile_id = auto_profile.id

    simulation_run = SimulationRun(
        user_id=current_user.id,
        startup_profile_id=startup_profile_id,
        run_name=payload.run_name or "Simulation Run",
        initial_cash=payload.initial_state.cash,
        initial_burn_rate=payload.initial_state.burn_rate,
    )

    db.add(simulation_run)
    db.commit()
    db.refresh(simulation_run)

    for index, decision in enumerate(payload.decisions, start=1):
        try:
            updated_state = apply_decision(current_state, decision)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Step {index}: {str(e)}")

        evaluation = evaluate_state(updated_state)

        step_record = SimulationStep(
            simulation_run_id=simulation_run.id,
            step_number=index,
            decision=decision,
            cash=updated_state.cash,
            burn_rate=updated_state.burn_rate,
            pmf_score=updated_state.pmf_score,
            retention_rate=updated_state.retention_rate,
            traction=updated_state.traction,
            adaptability=updated_state.adaptability,
            decision_delay=updated_state.decision_delay,
            team_strength=updated_state.team_strength,
            tech_debt=updated_state.tech_debt,
            scalability=updated_state.scalability,
            regulatory_risk=updated_state.regulatory_risk,
            external_shock=updated_state.external_shock,
            runway=evaluation["runway"],
            rule_risk_score=evaluation["rule_based"]["risk_score"],
            rule_risk_level=evaluation["rule_based"]["risk_level"],
            ai_prediction=evaluation["ai_based"]["prediction"],
            ai_label=evaluation["ai_based"]["label"],
            ai_probability=evaluation["ai_based"]["probability"],
            agreement=evaluation["agreement"],
            final_decision=evaluation["final_decision"],
        )

        db.add(step_record)

        steps.append({
            "step_number": index,
            "decision": decision,
            "updated_state": updated_state,
            "runway": evaluation["runway"],
            "rule_based": evaluation["rule_based"],
            "ai_based": evaluation["ai_based"],
            "agreement": evaluation["agreement"],
            "final_decision": evaluation["final_decision"],
            "summary": evaluation["summary"],
            "recommendations": evaluation["recommendations"], 
        })

        current_state = updated_state

    final_eval = evaluate_state(current_state)

    simulation_run.final_cash = current_state.cash
    simulation_run.final_burn_rate = current_state.burn_rate
    simulation_run.final_risk_level = final_eval["rule_based"]["risk_level"]
    simulation_run.final_ai_label = final_eval["ai_based"]["label"]
    simulation_run.agreement = final_eval["agreement"]
    simulation_run.final_decision = final_eval["final_decision"]

    db.commit()

    return {
        "simulation_run_id": simulation_run.id,
        "initial_state": payload.initial_state,
        "steps": steps,
        "final_state": current_state,
        "final_recommendations": final_eval["recommendations"],  
    }