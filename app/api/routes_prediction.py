from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.startup_profile import StartupProfile
from app.schemas.startup import StartupInput
from app.services.rule_engine import evaluate_rule_based
from app.services.ml_model import predict_ai
from app.services.explainability import (
    explain_decision_tree,
    summarize_hybrid_result,
    get_final_decision,
)
from app.services.recommendations import generate_recommendation_report

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/rule-based")
def predict_rule_based(startup: StartupInput, db: Session = Depends(get_db)):
    result = evaluate_rule_based(startup)

    risk_scores = {"global_risk": result["risk_score"]}
    recommendation = generate_recommendation_report(startup, result["derived"], risk_scores)

    startup_record = StartupProfile(
        cash=startup.cash,
        burn_rate=startup.burn_rate,
        pmf_score=startup.pmf_score,
        retention_rate=startup.retention_rate,
        traction=startup.traction,
        adaptability=startup.adaptability,
        decision_delay=startup.decision_delay,
        team_strength=startup.team_strength,
        tech_debt=startup.tech_debt,
        scalability=startup.scalability,
        regulatory_risk=startup.regulatory_risk,
        external_shock=startup.external_shock,
        runway=result["runway"],
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
    )
    db.add(startup_record)
    db.commit()
    db.refresh(startup_record)

    return {
        **result,
        "recommendation": recommendation,
    }


@router.post("/ai")
def predict_ai_route(startup: StartupInput):
    result = predict_ai(startup)
    explanation = explain_decision_tree(startup)

    rule_result = evaluate_rule_based(startup)
    derived = rule_result["derived"]

    ai_global_risk = result["probability"] if result["label"] == "FAILURE" else 1 - result["probability"]
    risk_scores = {"global_risk": round(ai_global_risk, 4)}
    recommendation = generate_recommendation_report(startup, derived, risk_scores)

    return {
        "prediction": result["prediction"],
        "label": result["label"],
        "probability": result["probability"],
        "runway": result["runway"],
        "explanation": explanation,
        "recommendation": recommendation,
    }


@router.post("/hybrid")
def predict_hybrid(startup: StartupInput):
    rule_result = evaluate_rule_based(startup)

    ai_result_raw = predict_ai(startup)
    ai_explanation = explain_decision_tree(startup)

    ai_result = {
        "prediction": ai_result_raw["prediction"],
        "label": ai_result_raw["label"],
        "probability": ai_result_raw["probability"],
        "runway": ai_result_raw["runway"],
        "explanation": ai_explanation,
        "recommendation": None,
    }

    # fix logic
    rule_failure = rule_result["risk_score"] >= 0.60
    ai_failure = ai_result["label"] == "FAILURE"
    agreement = rule_failure == ai_failure

    final_decision = get_final_decision(rule_result, ai_result)
    summary = summarize_hybrid_result(rule_result, ai_result, agreement)

    ai_global_risk = ai_result_raw["probability"] if ai_failure else 1 - ai_result_raw["probability"]
    global_risk = round((rule_result["risk_score"] + ai_global_risk) / 2, 4)
    risk_scores = {"global_risk": global_risk}
    recommendation = generate_recommendation_report(startup, rule_result["derived"], risk_scores)

  
    ai_result["recommendation"] = generate_recommendation_report(startup, rule_result["derived"], risk_scores)

    return {
        "runway": rule_result["runway"],
        "rule_based": {**rule_result, "recommendation": recommendation},
        "ai_based": ai_result,
        "agreement": agreement,
        "final_decision": final_decision,
        "summary": summary,
        "recommendation": recommendation,
    }