from datetime import date

from pydantic import BaseModel, ConfigDict


class DashboardTodayResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date

    calories: float
    protein: float
    workout_duration_minutes: int

    active_supplements: int
    total_supplements: int

    latest_progress_date: date | None = None


class DashboardSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_date: date
    end_date: date

    total_calories: float
    total_protein: float
    total_workout_duration_minutes: int

    active_supplements: int
    total_supplements: int

    latest_progress_date: date | None = None