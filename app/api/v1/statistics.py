from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.repositories.meal_repository import MealRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.workout_repository import WorkoutRepository
from app.schemas.statistics import StatisticsResponse
from app.services.statistics_service import StatisticsService


router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


def get_statistics_service(
    db: Session = Depends(get_db),
) -> StatisticsService:
    return StatisticsService(
        meal_repository=MealRepository(db),
        workout_repository=WorkoutRepository(db),
        progress_repository=ProgressRepository(db),
    )


@router.get(
    "",
    response_model=StatisticsResponse,
)
def get_statistics(
    start_date: date | None = Query(default=None),
    end_date: date | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    service: StatisticsService = Depends(get_statistics_service),
):
    today = date.today()

    if end_date is None:
        end_date = today

    if start_date is None:
        start_date = end_date - timedelta(days=6)

    return service.get_statistics(
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
    )