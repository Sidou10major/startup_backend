from pydantic import BaseModel, Field


class StartupInput(BaseModel):
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


class RuleBasedResponse(BaseModel):
    runway: float
    risk_score: float
    risk_level: str
    reasons: list[str]


class AIResponse(BaseModel):
    prediction: int
    label: str
    probability: float
    runway: float
    explanation: list[str]


class HybridResponse(BaseModel):
    runway: float
    rule_based: RuleBasedResponse
    ai_based: AIResponse
    agreement: bool
    final_decision: str
    summary: str