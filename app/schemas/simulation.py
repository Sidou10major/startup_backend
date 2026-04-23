from pydantic import BaseModel, Field
from typing import List, Optional
from app.schemas.startup import RuleBasedResponse, AIResponse, RecommendationReport


class StartupState(BaseModel):
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


class SimulationInput(BaseModel):
    state: StartupState
    decision: str
    mode: str = "hybrid"


class MultiStepSimulationInput(BaseModel):
    initial_state: StartupState
    decisions: List[str]
    startup_profile_id: Optional[int] = None
    user_id: Optional[int] = None
    run_name: Optional[str] = None
    mode: str = "hybrid"  


class SimulationResponse(BaseModel):
    updated_state: StartupState
    runway: float
    rule_based: RuleBasedResponse
    ai_based: AIResponse
    agreement: bool
    final_decision: str
    summary: str
    recommendations: RecommendationReport  


class SimulationStepResult(BaseModel):
    step_number: int
    decision: str
    updated_state: StartupState
    runway: float
    rule_based: RuleBasedResponse
    ai_based: AIResponse
    agreement: bool
    final_decision: str
    summary: str
    recommendations: RecommendationReport  


class MultiStepSimulationResponse(BaseModel):
    simulation_run_id: Optional[int] = None
    initial_state: StartupState
    steps: List[SimulationStepResult]
    final_state: StartupState
    final_recommendations: RecommendationReport  


class DecisionItem(BaseModel):
    key: str
    label: str
    description: str


class AllowedDecisionsResponse(BaseModel):
    decisions: List[DecisionItem]