from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class StartupProfile(Base):
    __tablename__ = "startup_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String(100), nullable=False)
    sector = Column(String(100), nullable=True)

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

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    simulation_runs = relationship("SimulationRun", back_populates="startup_profile")