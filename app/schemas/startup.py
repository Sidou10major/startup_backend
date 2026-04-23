from pydantic import BaseModel, Field
from typing import List


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


class WeaknessItem(BaseModel):
    icon: str
    label: str
    variable: str


class RecommendationCard(BaseModel):
    title: str
    priority: str
    color: str
    actions: List[str]


class RecommendationReport(BaseModel):
    risk_level: str
    risk_score: float
    key_weaknesses: List[WeaknessItem]
    recommendation_cards: List[RecommendationCard]
    strategic_summary: str


class DerivedMetrics(BaseModel):
    runway: float
    financial_stress: float
    market_fit: float
    growth_rate: float
    decision_quality: float
    timing_score: float
    execution_capability: float
    governance_score: float
    reliability: float
    maintenance_cost: float
    shock_probability: float
    compliance_cost: float


class RuleBasedResponse(BaseModel):
    runway: float
    risk_score: float
    risk_level: str
    verdict: str
    reasons: List[str]
    derived: DerivedMetrics
    recommendation: RecommendationReport


class AIResponse(BaseModel):
    prediction: int
    label: str
    probability: float
    runway: float
    explanation: List[str]
    recommendation: RecommendationReport


class HybridResponse(BaseModel):
    runway: float
    rule_based: RuleBasedResponse
    ai_based: AIResponse
    agreement: bool
    final_decision: str
    summary: str
    recommendation: RecommendationReport