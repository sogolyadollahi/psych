from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.auth import router as auth_router
from app.api.v1.meals import router as meal_router
from app.api.v1.workout import router as workout_router
from app.api.v1.supplement import router as supplement_router
from app.api.v1.food_scanner import router as food_scanner_router
from app.api.v1.progress import router as progress_router
from app.api.v1.dashboard import router as dashboard_router
from app.services.scheduler import AppScheduler
from app.api.v1.statistics import router as statistics_router


scheduler = AppScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(
    title="Psych API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {"status": "OK"}


app.include_router(auth_router, prefix="/api/v1")
app.include_router(workout_router, prefix="/api/v1")
app.include_router(meal_router, prefix="/api/v1")
app.include_router(supplement_router, prefix="/api/v1")
app.include_router(food_scanner_router, prefix="/api/v1")
app.include_router(progress_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(statistics_router, prefix="/api/v1")
