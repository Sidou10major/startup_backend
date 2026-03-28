from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.models.simulation_run import SimulationRun
from app.models.simulation_step import SimulationStep
from app.models.user import User

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/runs")
def list_simulation_runs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    runs = (
        db.query(SimulationRun)
        .filter(SimulationRun.user_id == current_user.id)
        .order_by(SimulationRun.id.desc())
        .all()
    )

    return [
        {
            "id": run.id,
            "run_name": run.run_name,
            "startup_profile_id": run.startup_profile_id,
            "final_risk_level": run.final_risk_level,
            "final_ai_label": run.final_ai_label,
            "agreement": run.agreement,
            "final_decision": run.final_decision,
            "created_at": run.created_at,
        }
        for run in runs
    ]


@router.get("/startup-profile/{startup_profile_id}/runs")
def list_runs_by_startup_profile(
    startup_profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    runs = (
        db.query(SimulationRun)
        .filter(
            SimulationRun.startup_profile_id == startup_profile_id,
            SimulationRun.user_id == current_user.id,
        )
        .order_by(SimulationRun.id.desc())
        .all()
    )

    return [
        {
            "id": run.id,
            "run_name": run.run_name,
            "startup_profile_id": run.startup_profile_id,
            "final_risk_level": run.final_risk_level,
            "final_ai_label": run.final_ai_label,
            "agreement": run.agreement,
            "final_decision": run.final_decision,
            "created_at": run.created_at,
        }
        for run in runs
    ]


@router.get("/runs/{run_id}")
def get_simulation_run_details(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run = (
        db.query(SimulationRun)
        .filter(
            SimulationRun.id == run_id,
            SimulationRun.user_id == current_user.id,
        )
        .first()
    )

    if not run:
        raise HTTPException(status_code=404, detail="Simulation run not found")

    steps = (
        db.query(SimulationStep)
        .filter(SimulationStep.simulation_run_id == run_id)
        .order_by(SimulationStep.step_number.asc())
        .all()
    )

    return {
        "run": {
            "id": run.id,
            "run_name": run.run_name,
            "startup_profile_id": run.startup_profile_id,
            "initial_cash": run.initial_cash,
            "initial_burn_rate": run.initial_burn_rate,
            "final_cash": run.final_cash,
            "final_burn_rate": run.final_burn_rate,
            "final_risk_level": run.final_risk_level,
            "final_ai_label": run.final_ai_label,
            "agreement": run.agreement,
            "final_decision": run.final_decision,
            "created_at": run.created_at,
        },
        "steps": [
            {
                "id": step.id,
                "step_number": step.step_number,
                "decision": step.decision,
                "cash": step.cash,
                "burn_rate": step.burn_rate,
                "pmf_score": step.pmf_score,
                "retention_rate": step.retention_rate,
                "traction": step.traction,
                "adaptability": step.adaptability,
                "decision_delay": step.decision_delay,
                "team_strength": step.team_strength,
                "tech_debt": step.tech_debt,
                "scalability": step.scalability,
                "regulatory_risk": step.regulatory_risk,
                "external_shock": step.external_shock,
                "runway": step.runway,
                "rule_risk_score": step.rule_risk_score,
                "rule_risk_level": step.rule_risk_level,
                "ai_prediction": step.ai_prediction,
                "ai_label": step.ai_label,
                "ai_probability": step.ai_probability,
                "agreement": step.agreement,
                "final_decision": step.final_decision,
            }
            for step in steps
        ],
    }


@router.delete("/runs/{run_id}")
def delete_simulation_run(
    run_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run = (
        db.query(SimulationRun)
        .filter(
            SimulationRun.id == run_id,
            SimulationRun.user_id == current_user.id,
        )
        .first()
    )

    if not run:
        raise HTTPException(status_code=404, detail="Simulation run not found")

    db.delete(run)
    db.commit()

    return {
        "message": "Simulation run deleted successfully",
        "deleted_run_id": run_id,
    }


@router.get("/compare")
def compare_two_runs(
    run_id_1: int,
    run_id_2: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    run1 = (
        db.query(SimulationRun)
        .filter(
            SimulationRun.id == run_id_1,
            SimulationRun.user_id == current_user.id,
        )
        .first()
    )
    run2 = (
        db.query(SimulationRun)
        .filter(
            SimulationRun.id == run_id_2,
            SimulationRun.user_id == current_user.id,
        )
        .first()
    )

    if not run1:
        raise HTTPException(status_code=404, detail=f"Simulation run {run_id_1} not found")
    if not run2:
        raise HTTPException(status_code=404, detail=f"Simulation run {run_id_2} not found")

    steps1 = (
        db.query(SimulationStep)
        .filter(SimulationStep.simulation_run_id == run_id_1)
        .order_by(SimulationStep.step_number.asc())
        .all()
    )
    steps2 = (
        db.query(SimulationStep)
        .filter(SimulationStep.simulation_run_id == run_id_2)
        .order_by(SimulationStep.step_number.asc())
        .all()
    )

    comparison = {
        "run_1": {
            "id": run1.id,
            "run_name": run1.run_name,
            "startup_profile_id": run1.startup_profile_id,
            "final_cash": run1.final_cash,
            "final_burn_rate": run1.final_burn_rate,
            "final_risk_level": run1.final_risk_level,
            "final_ai_label": run1.final_ai_label,
            "agreement": run1.agreement,
            "final_decision": run1.final_decision,
            "steps_count": len(steps1),
        },
        "run_2": {
            "id": run2.id,
            "run_name": run2.run_name,
            "startup_profile_id": run2.startup_profile_id,
            "final_cash": run2.final_cash,
            "final_burn_rate": run2.final_burn_rate,
            "final_risk_level": run2.final_risk_level,
            "final_ai_label": run2.final_ai_label,
            "agreement": run2.agreement,
            "final_decision": run2.final_decision,
            "steps_count": len(steps2),
        },
        "differences": {
            "cash_difference": round((run1.final_cash or 0) - (run2.final_cash or 0), 2),
            "burn_rate_difference": round((run1.final_burn_rate or 0) - (run2.final_burn_rate or 0), 2),
            "same_final_risk_level": run1.final_risk_level == run2.final_risk_level,
            "same_final_ai_label": run1.final_ai_label == run2.final_ai_label,
            "same_final_decision": run1.final_decision == run2.final_decision,
        },
        "better_run": determine_better_run(run1, run2),
    }

    return comparison


def determine_better_run(run1, run2):
    score1 = 0
    score2 = 0

    if (run1.final_cash or 0) > (run2.final_cash or 0):
        score1 += 1
    elif (run2.final_cash or 0) > (run1.final_cash or 0):
        score2 += 1

    if (run1.final_burn_rate or 0) < (run2.final_burn_rate or 0):
        score1 += 1
    elif (run2.final_burn_rate or 0) < (run1.final_burn_rate or 0):
        score2 += 1

    risk_rank = {"LOW": 3, "MEDIUM": 2, "HIGH": 1}
    risk1 = risk_rank.get(run1.final_risk_level or "", 0)
    risk2 = risk_rank.get(run2.final_risk_level or "", 0)

    if risk1 > risk2:
        score1 += 1
    elif risk2 > risk1:
        score2 += 1

    decision_rank = {"SAFE": 3, "MODERATE RISK": 2, "AT RISK": 1}
    dec1 = decision_rank.get(run1.final_decision or "", 0)
    dec2 = decision_rank.get(run2.final_decision or "", 0)

    if dec1 > dec2:
        score1 += 1
    elif dec2 > dec1:
        score2 += 1

    if score1 > score2:
        return {
            "winner_run_id": run1.id,
            "winner_run_name": run1.run_name,
            "reason": "Run 1 has a stronger final overall state."
        }
    elif score2 > score1:
        return {
            "winner_run_id": run2.id,
            "winner_run_name": run2.run_name,
            "reason": "Run 2 has a stronger final overall state."
        }

    return {
        "winner_run_id": None,
        "winner_run_name": None,
        "reason": "Both runs are approximately equivalent."
    }