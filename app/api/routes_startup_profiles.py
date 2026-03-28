from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.models.startup_profile import StartupProfile
from app.models.user import User
from app.schemas.startup_profile import StartupProfileCreate

router = APIRouter(prefix="/startup-profiles", tags=["Startup Profiles"])


@router.post("/")
def create_startup_profile(
    payload: StartupProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startup = StartupProfile(
        user_id=current_user.id,
        name=payload.name,
        sector=payload.sector,
        cash=payload.cash,
        burn_rate=payload.burn_rate,
        pmf_score=payload.pmf_score,
        retention_rate=payload.retention_rate,
        traction=payload.traction,
        adaptability=payload.adaptability,
        decision_delay=payload.decision_delay,
        team_strength=payload.team_strength,
        tech_debt=payload.tech_debt,
        scalability=payload.scalability,
        regulatory_risk=payload.regulatory_risk,
        external_shock=payload.external_shock,
    )

    db.add(startup)
    db.commit()
    db.refresh(startup)

    return {
        "message": "Startup profile created successfully",
        "startup_profile_id": startup.id
    }


@router.get("/")
def list_startup_profiles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    startups = (
        db.query(StartupProfile)
        .filter(StartupProfile.user_id == current_user.id)
        .order_by(StartupProfile.id.desc())
        .all()
    )

    return startups