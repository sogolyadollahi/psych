from datetime import date, datetime

from pydantic import BaseModel, Field

class WorkoutCreate(BaseModel):
    muscle_group: str = Field(min_length=1, max_length=100)
    duration_minutes: int = Field(gt=0, lt=1440)
    calories_burned: int | None = Field(default=None, ge=0)
    workout_date: date

class WorkoutUpdate(BaseModel):
    muscle_group: str | None= Field(
        default=None,
        min_length=1'
        max_length=100,
    )
    duration_minutes: int | None = Field(
        default=None,
        gt=0,
        le=1440,
    )
    calories_burned: int | None = Field(
        default=None,
        ge=0,
    )
    workout_date: date | None = None


class WorkoutResponse(BaseModel):
    id : int
    muscle_group: str
    duration_minutes: int
    calories_burned: int | None
    workout_date: date
    created_at: datetime