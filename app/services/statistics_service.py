from datetime import date

from app.repositories.meal_repository import MealRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.workout_repository import WorkoutRepository
from app.schemas.statistics import (
    DailyNutritionStatistics,
    DailyWorkoutStatistics,
    ProgressStatistics,
    StatisticsResponse,
)


class StatisticsService:

    def __init__(
        self,
        meal_repository: MealRepository,
        workout_repository: WorkoutRepository,
        progress_repository: ProgressRepository,
    ):
        self.meal_repository = meal_repository
        self.workout_repository = workout_repository
        self.progress_repository = progress_repository

    def get_statistics(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> StatisticsResponse:

        if start_date > end_date:
            raise ValueError(
                "start_date must be before or equal to end_date"
            )

        # -------------------------
        # Nutrition statistics
        # -------------------------

        meals = self.meal_repository.get_by_user_id(user_id)

        filtered_meals = [
            meal
            for meal in meals
            if start_date <= meal.meal_date <= end_date
        ]

        nutrition_by_date: dict[date, dict[str, float]] = {}

        for meal in filtered_meals:
            meal_date = meal.meal_date

            if meal_date not in nutrition_by_date:
                nutrition_by_date[meal_date] = {
                    "calories": 0.0,
                    "protein": 0.0,
                }

            for item in meal.items:
                nutrition_by_date[meal_date]["calories"] += float(
                    item.calories
                )
                nutrition_by_date[meal_date]["protein"] += float(
                    item.protein
                )

        nutrition = [
            DailyNutritionStatistics(
                date=day,
                calories=round(values["calories"], 2),
                protein=round(values["protein"], 2),
            )
            for day, values in sorted(nutrition_by_date.items())
        ]

        # -------------------------
        # Workout statistics
        # -------------------------

        workouts = self.workout_repository.get_by_user_id(user_id)

        filtered_workouts = [
            workout
            for workout in workouts
            if start_date <= workout.workout_date.date() <= end_date
        ]

        workout_by_date: dict[date, dict[str, int]] = {}

        for workout in filtered_workouts:
            workout_date = workout.workout_date.date()

            if workout_date not in workout_by_date:
                workout_by_date[workout_date] = {
                    "duration_minutes": 0,
                    "calories_burned": 0,
                }

            workout_by_date[workout_date]["duration_minutes"] += (
                workout.duration_minutes
            )

            workout_by_date[workout_date]["calories_burned"] += (
                workout.calories_burned
            )

        workouts_statistics = [
            DailyWorkoutStatistics(
                date=day,
                duration_minutes=values["duration_minutes"],
                calories_burned=values["calories_burned"],
            )
            for day, values in sorted(workout_by_date.items())
        ]

        # -------------------------
        # Progress statistics
        # -------------------------

        progress_records = (
            self.progress_repository.get_by_user_id_and_date_range(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            )
        )

        progress = [
            ProgressStatistics(
                date=record.progress_date,
                weight=(
                    float(record.weight)
                    if record.weight is not None
                    else None
                ),
                body_fat=(
                    float(record.body_fat)
                    if record.body_fat is not None
                    else None
                ),
                chest=(
                    float(record.chest)
                    if record.chest is not None
                    else None
                ),
                waist=(
                    float(record.waist)
                    if record.waist is not None
                    else None
                ),
                arm=(
                    float(record.arm)
                    if record.arm is not None
                    else None
                ),
                thigh=(
                    float(record.thigh)
                    if record.thigh is not None
                    else None
                ),
            )
            for record in progress_records
        ]

        return StatisticsResponse(
            start_date=start_date,
            end_date=end_date,
            nutrition=nutrition,
            workouts=workouts_statistics,
            progress=progress,
        )