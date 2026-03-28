from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.startup_profile import StartupProfile
from app.schemas.startup import (
    StartupInput,
    RuleBasedResponse,
    AIResponse,
    HybridResponse,
)
from app.services.rule_engine import evaluate_rule_based
from app.services.ml_model import predict_ai
from app.services.explainability import (
    explain_decision_tree,
    summarize_hybrid_result,
    get_final_decision,
)

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post("/rule-based", response_model=RuleBasedResponse)
def predict_rule_based(startup: StartupInput, db: Session = Depends(get_db)):
    result = evaluate_rule_based(startup)

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

    return result


@router.post("/ai", response_model=AIResponse)
def predict_ai_route(startup: StartupInput):
    result = predict_ai(startup)
    explanation = explain_decision_tree(startup)

    return {
        "prediction": result["prediction"],
        "label": result["label"],
        "probability": result["probability"],
        "runway": result["runway"],
        "explanation": explanation,
    }


@router.post("/hybrid", response_model=HybridResponse)
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
    }

    rule_failure = rule_result["risk_level"] == "HIGH"
    ai_failure = ai_result["label"] == "FAILURE"
    agreement = rule_failure == ai_failure

    final_decision = get_final_decision(rule_result, ai_result)
    summary = summarize_hybrid_result(rule_result, ai_result, agreement)

    return {
        "runway": rule_result["runway"],
        "rule_based": rule_result,
        "ai_based": ai_result,
        "agreement": agreement,
        "final_decision": final_decision,
        "summary": summary,
    }