from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1 import users
from app.api.v1.auth import router as auth_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.food_scanner import router as food_scanner_router
from app.api.v1.meals import router as meal_router
from app.api.v1.progress import router as progress_router
from app.api.v1.statistics import router as statistics_router
from app.api.v1.supplement import router as supplement_router
from app.api.v1.workout import router as workout_router
from app.core.config import settings
from app.core.exception_handlers import (
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.core.logging_config import setup_logging
from app.core.rate_limiter import limiter
from app.services.scheduler import AppScheduler


setup_logging()

scheduler = AppScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()

    yield

    scheduler.shutdown()


tags_metadata = [
    {
        "name": "Authentication",
        "description": "Registration, login, and authentication operations.",
    },
    {
        "name": "Workouts",
        "description": "Create and manage user workouts.",
    },
    {
        "name": "Meals",
        "description": "Manage meals and meal items.",
    },
    {
        "name": "Supplements",
        "description": "Manage supplements and reminders.",
    },
    {
        "name": "Food Scanner",
        "description": "Validate and scan food images.",
    },
    {
        "name": "Progress",
        "description": "Track and analyze user progress.",
    },
    {
        "name": "Dashboard",
        "description": "Retrieve dashboard summaries and daily data.",
    },
    {
        "name": "Statistics",
        "description": "Retrieve fitness and nutrition statistics.",
    },
    {
        "name": "Users",
        "description": "Manage user profiles and accounts.",
    },
    {
        "name": "Health",
        "description": "API health monitoring.",
    },
]


app = FastAPI(
    title="Psych API",
    description=(
        "Psych is a fitness and nutrition tracking API "
        "for workouts, meals, supplements, progress, "
        "food scanning, and user profiles."
    ),
    version=settings.APP_VERSION,
    openapi_tags=tags_metadata,
    docs_url="/docs" if settings.DOCS_ENABLED else None,
    redoc_url="/redoc" if settings.DOCS_ENABLED else None,
    openapi_url="/openapi.json" if settings.DOCS_ENABLED else None,
    lifespan=lifespan,
)


# -------------------------
# Rate Limiting
# -------------------------
app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)


# -------------------------
# Exception Handlers
# -------------------------
app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    unhandled_exception_handler,
)


# -------------------------
# CORS
# -------------------------
cors_origins = [
    origin.strip()
    for origin in settings.CORS_ORIGINS.split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Health
# -------------------------
@app.get(
    "/health",
    summary="Health check",
    description="Check whether the Psych API is running.",
    tags=["Health"],
)
def health_check():
    return {"status": "OK"}


# -------------------------
# API Routers
# -------------------------
app.include_router(auth_router, prefix="/api/v1")
app.include_router(workout_router, prefix="/api/v1")
app.include_router(meal_router, prefix="/api/v1")
app.include_router(supplement_router, prefix="/api/v1")
app.include_router(food_scanner_router, prefix="/api/v1")
app.include_router(progress_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(statistics_router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")