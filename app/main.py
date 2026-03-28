from fastapi import FastAPI
from app.api.routes_prediction import router as prediction_router
from app.api.routes_simulation import router as simulation_router
from app.api.routes_startup_profiles import router as startup_profiles_router
from app.api.routes_history import router as history_router
from app.api.routes_dashboard import router as dashboard_router
from app.api.routes_auth import router as auth_router
from app.db.session import Base, engine

from app.models.user import User  # noqa: F401
from app.models.startup_profile import StartupProfile  # noqa: F401
from app.models.simulation_run import SimulationRun  # noqa: F401
from app.models.simulation_step import SimulationStep  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Startup Failure Simulation API")

app.include_router(auth_router)
app.include_router(prediction_router)
app.include_router(simulation_router)
app.include_router(startup_profiles_router)
app.include_router(history_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {"message": "Startup Failure Simulation Backend is running"}