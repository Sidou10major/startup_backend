from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.models.simulation_run import SimulationRun
from app.models.simulation_step import SimulationStep
from app.models.startup_profile import StartupProfile
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview")
def get_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_startup_profiles = (
        db.query(func.count(StartupProfile.id))
        .filter(StartupProfile.user_id == current_user.id)
        .scalar()
        or 0
    )

    total_runs = (
        db.query(func.count(SimulationRun.id))
        .filter(SimulationRun.user_id == current_user.id)
        .scalar()
        or 0
    )

    user_run_ids = (
        db.query(SimulationRun.id)
        .filter(SimulationRun.user_id == current_user.id)
        .subquery()
    )

    total_steps = (
        db.query(func.count(SimulationStep.id))
        .filter(SimulationStep.simulation_run_id.in_(user_run_ids))
        .scalar()
        or 0
    )

    high_risk_runs = (
        db.query(func.count(SimulationRun.id))
        .filter(
            SimulationRun.user_id == current_user.id,
            SimulationRun.final_risk_level == "HIGH",
        )
        .scalar()
        or 0
    )

    medium_risk_runs = (
        db.query(func.count(SimulationRun.id))
        .filter(
            SimulationRun.user_id == current_user.id,
            SimulationRun.final_risk_level == "MEDIUM",
        )
        .scalar()
        or 0
    )

    low_risk_runs = (
        db.query(func.count(SimulationRun.id))
        .filter(
            SimulationRun.user_id == current_user.id,
            SimulationRun.final_risk_level == "LOW",
        )
        .scalar()
        or 0
    )

    safe_runs = (
        db.query(func.count(SimulationRun.id))
        .filter(
            SimulationRun.user_id == current_user.id,
            SimulationRun.final_decision == "SAFE",
        )
        .scalar()
        or 0
    )

    moderate_risk_runs = (
        db.query(func.count(SimulationRun.id))
        .filter(
            SimulationRun.user_id == current_user.id,
            SimulationRun.final_decision == "MODERATE RISK",
        )
        .scalar()
        or 0
    )

    at_risk_runs = (
        db.query(func.count(SimulationRun.id))
        .filter(
            SimulationRun.user_id == current_user.id,
            SimulationRun.final_decision == "AT RISK",
        )
        .scalar()
        or 0
    )

    avg_final_cash = (
        db.query(func.avg(SimulationRun.final_cash))
        .filter(SimulationRun.user_id == current_user.id)
        .scalar()
    )

    avg_final_burn_rate = (
        db.query(func.avg(SimulationRun.final_burn_rate))
        .filter(SimulationRun.user_id == current_user.id)
        .scalar()
    )

    return {
        "summary_cards": {
            "total_startup_profiles": total_startup_profiles,
            "total_runs": total_runs,
            "total_steps": total_steps,
            "average_final_cash": round(avg_final_cash or 0, 2),
            "average_final_burn_rate": round(avg_final_burn_rate or 0, 2),
        },
        "risk_distribution": {
            "HIGH": high_risk_runs,
            "MEDIUM": medium_risk_runs,
            "LOW": low_risk_runs,
        },
        "final_decision_distribution": {
            "SAFE": safe_runs,
            "MODERATE RISK": moderate_risk_runs,
            "AT RISK": at_risk_runs,
        },
    }


@router.get("/most-used-decisions")
def get_most_used_decisions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    decisions = (
        db.query(SimulationStep.decision)
        .join(SimulationRun, SimulationStep.simulation_run_id == SimulationRun.id)
        .filter(SimulationRun.user_id == current_user.id)
        .all()
    )

    decision_list = [d[0] for d in decisions]
    counts = Counter(decision_list)

    return {
        "total_unique_decisions": len(counts),
        "most_used_decisions": [
            {"decision": decision, "count": count}
            for decision, count in counts.most_common()
        ],
    }


@router.get("/runs-per-startup-profile")
def get_runs_per_startup_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    results = (
        db.query(
            StartupProfile.id,
            StartupProfile.name,
            func.count(SimulationRun.id).label("runs_count"),
        )
        .outerjoin(SimulationRun, StartupProfile.id == SimulationRun.startup_profile_id)
        .filter(StartupProfile.user_id == current_user.id)
        .group_by(StartupProfile.id, StartupProfile.name)
        .all()
    )

    return [
        {
            "startup_profile_id": row.id,
            "startup_name": row.name,
            "runs_count": row.runs_count,
        }
        for row in results
    ]


@router.get("/startup-profile/{startup_profile_id}")
def get_dashboard_for_startup_profile(
    startup_profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = (
        db.query(StartupProfile)
        .filter(
            StartupProfile.id == startup_profile_id,
            StartupProfile.user_id == current_user.id,
        )
        .first()
    )

    if not startup:
        return {
            "message": "Startup profile not found",
            "startup_profile_id": startup_profile_id,
        }

    runs = (
        db.query(SimulationRun)
        .filter(
            SimulationRun.startup_profile_id == startup_profile_id,
            SimulationRun.user_id == current_user.id,
        )
        .all()
    )

    run_count = len(runs)

    high_risk_runs = sum(1 for r in runs if r.final_risk_level == "HIGH")
    medium_risk_runs = sum(1 for r in runs if r.final_risk_level == "MEDIUM")
    low_risk_runs = sum(1 for r in runs if r.final_risk_level == "LOW")

    safe_runs = sum(1 for r in runs if r.final_decision == "SAFE")
    moderate_risk_runs = sum(1 for r in runs if r.final_decision == "MODERATE RISK")
    at_risk_runs = sum(1 for r in runs if r.final_decision == "AT RISK")

    avg_final_cash = (
        sum((r.final_cash or 0) for r in runs) / run_count if run_count > 0 else 0
    )
    avg_final_burn_rate = (
        sum((r.final_burn_rate or 0) for r in runs) / run_count if run_count > 0 else 0
    )

    steps = (
        db.query(SimulationStep)
        .join(SimulationRun, SimulationStep.simulation_run_id == SimulationRun.id)
        .filter(
            SimulationRun.startup_profile_id == startup_profile_id,
            SimulationRun.user_id == current_user.id,
        )
        .all()
    )

    decision_counts = Counter(step.decision for step in steps)

    return {
        "startup_profile": {
            "id": startup.id,
            "name": startup.name,
            "sector": startup.sector,
        },
        "summary_cards": {
            "total_runs": run_count,
            "average_final_cash": round(avg_final_cash, 2),
            "average_final_burn_rate": round(avg_final_burn_rate, 2),
        },
        "risk_distribution": {
            "HIGH": high_risk_runs,
            "MEDIUM": medium_risk_runs,
            "LOW": low_risk_runs,
        },
        "final_decision_distribution": {
            "SAFE": safe_runs,
            "MODERATE RISK": moderate_risk_runs,
            "AT RISK": at_risk_runs,
        },
        "most_used_decisions": [
            {"decision": decision, "count": count}
            for decision, count in decision_counts.most_common()
        ],
    }


@router.get("/recent-runs")
def get_recent_runs(
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    runs = (
        db.query(SimulationRun)
        .filter(SimulationRun.user_id == current_user.id)
        .order_by(SimulationRun.created_at.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "id": run.id,
            "run_name": run.run_name,
            "startup_profile_id": run.startup_profile_id,
            "final_cash": run.final_cash,
            "final_burn_rate": run.final_burn_rate,
            "final_risk_level": run.final_risk_level,
            "final_ai_label": run.final_ai_label,
            "agreement": run.agreement,
            "final_decision": run.final_decision,
            "created_at": run.created_at,
        }
        for run in runs
    ]