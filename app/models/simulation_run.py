from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    startup_profile_id = Column(Integer, ForeignKey("startup_profiles.id"), nullable=False)

    run_name = Column(String(100), nullable=True)

    initial_cash = Column(Float, nullable=False)
    initial_burn_rate = Column(Float, nullable=False)

    final_cash = Column(Float, nullable=True)
    final_burn_rate = Column(Float, nullable=True)

    final_risk_level = Column(String(20), nullable=True)
    final_ai_label = Column(String(20), nullable=True)
    agreement = Column(Boolean, nullable=True)
    final_decision = Column(String(30), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    startup_profile = relationship("StartupProfile", back_populates="simulation_runs")
    steps = relationship("SimulationStep", back_populates="simulation_run", cascade="all, delete-orphan")