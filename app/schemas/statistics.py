from datetime import date

from pydantic import BaseModel, ConfigDict


class DailyNutritionStatistics(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    calories: float
    protein: float


class DailyWorkoutStatistics(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    duration_minutes: int
    calories_burned: int


class ProgressStatistics(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: date
    weight: float | None = None
    body_fat: float | None = None
    chest: float | None = None
    waist: float | None = None
    arm: float | None = None
    thigh: float | None = None


class StatisticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_date: date
    end_date: date
    nutrition: list[DailyNutritionStatistics]
    workouts: list[DailyWorkoutStatistics]
    progress: list[ProgressStatistics]