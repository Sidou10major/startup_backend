from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base


class SimulationStep(Base):
    __tablename__ = "simulation_steps"

    id = Column(Integer, primary_key=True, index=True)
    simulation_run_id = Column(Integer, ForeignKey("simulation_runs.id"), nullable=False)

    step_number = Column(Integer, nullable=False)
    decision = Column(String(100), nullable=False)

    cash = Column(Float, nullable=False)
    burn_rate = Column(Float, nullable=False)
    pmf_score = Column(Float, nullable=False)
    retention_rate = Column(Float, nullable=False)
    traction = Column(Float, nullable=False)
    adaptability = Column(Float, nullable=False)
    decision_delay = Column(Float, nullable=False)
    team_strength = Column(Float, nullable=False)
    tech_debt = Column(Float, nullable=False)
    scalability = Column(Float, nullable=False)
    regulatory_risk = Column(Float, nullable=False)
    external_shock = Column(Float, nullable=False)

    runway = Column(Float, nullable=False)

    rule_risk_score = Column(Float, nullable=False)
    rule_risk_level = Column(String(20), nullable=False)

    ai_prediction = Column(Integer, nullable=False)
    ai_label = Column(String(20), nullable=False)
    ai_probability = Column(Float, nullable=False)

    agreement = Column(Boolean, nullable=False)
    final_decision = Column(String(30), nullable=False)

    simulation_run = relationship("SimulationRun", back_populates="steps")