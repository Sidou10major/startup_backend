from pydantic import BaseModel, Field


class StartupProfileCreate(BaseModel):
    name: str
    sector: str | None = None
    user_id: int | None = None

    cash: float = Field(..., gt=0)
    burn_rate: float = Field(..., gt=0)
    pmf_score: float = Field(..., ge=0, le=1)
    retention_rate: float = Field(..., ge=0, le=1)
    traction: float = Field(..., ge=0, le=1)
    adaptability: float = Field(..., ge=0, le=1)
    decision_delay: float = Field(..., ge=0)
    team_strength: float = Field(..., ge=0, le=1)
    tech_debt: float = Field(..., ge=0, le=1)
    scalability: float = Field(..., ge=0, le=1)
    regulatory_risk: float = Field(..., ge=0, le=1)
    external_shock: float = Field(..., ge=0, le=1)