from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.deps import get_current_user
from app.models.user import User
from app.repositories.meal_repository import MealRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.supplement_repository import SupplementRepository
from app.repositories.workout_repository import WorkoutRepository
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTodayResponse,
)
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


def get_dashboard_service(
    db: Session = Depends(get_db),
) -> DashboardService:
    return DashboardService(
        meal_repository=MealRepository(db),
        workout_repository=WorkoutRepository(db),
        supplement_repository=SupplementRepository(db),
        progress_repository=ProgressRepository(db),
    )


@router.get(
    "/today",
    response_model=DashboardTodayResponse,
    summary="Get today's dashboard",
    description="Return today's fitness and nutrition dashboard for the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
    },
)
def get_today_dashboard(
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    return service.get_today(
        user_id=current_user.id,
    )


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Get dashboard summary",
    description="Return a dashboard summary for the authenticated user, optionally filtered by date range.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
    },
)
def get_dashboard_summary(
    start_date: date | None = Query(
        default=None,
    ),
    end_date: date | None = Query(
        default=None,
    ),
    current_user: User = Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    today = date.today()

    if end_date is None:
        end_date = today

    if start_date is None:
        start_date = end_date - timedelta(days=6)

    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date",
        )    

    return service.get_summary(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )