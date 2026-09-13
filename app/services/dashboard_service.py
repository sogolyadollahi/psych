from datetime import date, datetime, time, timedelta

from app.models.meal import Meal
from app.repositories.meal_repository import MealRepository
from app.repositories.progress_repository import ProgressRepository
from app.repositories.supplement_repository import SupplementRepository
from app.repositories.workout_repository import WorkoutRepository
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTodayResponse,
)


class DashboardService:

    def __init__(
        self,
        meal_repository: MealRepository,
        workout_repository: WorkoutRepository,
        supplement_repository: SupplementRepository,
        progress_repository: ProgressRepository,
    ):
        self.meal_repository = meal_repository
        self.workout_repository = workout_repository
        self.supplement_repository = supplement_repository
        self.progress_repository = progress_repository

    # =====================================================
    # Today
    # =====================================================

    def get_today(
        self,
        user_id: int,
    ) -> DashboardTodayResponse:

        today = date.today()

        meals = self.meal_repository.get_by_user_id(user_id)

        today_meals = [
            meal
            for meal in meals
            if meal.meal_date == today
        ]

        calories = sum(
            sum(item.calories for item in meal.items)
            for meal in today_meals
        )

        protein = sum(
            sum(item.protein for item in meal.items)
            for meal in today_meals
        )

        workouts = self.workout_repository.get_by_user_id(
            user_id
        )

        today_workouts = [
            workout
            for workout in workouts
            if workout.workout_date.date() == today
        ]

        workout_duration = sum(
            workout.duration_minutes
            for workout in today_workouts
        )

        supplements = (
            self.supplement_repository.get_by_user_id(
                user_id
            )
        )

        active_supplements = sum(
            1
            for supplement in supplements
            if supplement.is_active
        )

        progress_records = (
            self.progress_repository.get_by_user_id(
                user_id
            )
        )

        latest_progress_date = (
            progress_records[0].progress_date
            if progress_records
            else None
        )

        return DashboardTodayResponse(
            date=today,
            calories=float(calories),
            protein=float(protein),
            workout_duration_minutes=workout_duration,
            active_supplements=active_supplements,
            total_supplements=len(supplements),
            latest_progress_date=latest_progress_date,
        )

    # =====================================================
    # Summary
    # =====================================================

    def get_summary(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> DashboardSummaryResponse:

        if start_date > end_date:
            raise ValueError(
                "start_date must be before or equal to end_date"
            )

        meals = self.meal_repository.get_by_user_id(user_id)

        filtered_meals = [
            meal
            for meal in meals
            if start_date <= meal.meal_date <= end_date
        ]

        total_calories = sum(
            sum(item.calories for item in meal.items)
            for meal in filtered_meals
        )

        total_protein = sum(
            sum(item.protein for item in meal.items)
            for meal in filtered_meals
        )

        workouts = self.workout_repository.get_by_user_id(
            user_id
        )

        filtered_workouts = [
            workout
            for workout in workouts
            if start_date
            <= workout.workout_date.date()
            <= end_date
        ]

        total_workout_duration = sum(
            workout.duration_minutes
            for workout in filtered_workouts
        )

        supplements = (
            self.supplement_repository.get_by_user_id(
                user_id
            )
        )

        active_supplements = sum(
            1
            for supplement in supplements
            if supplement.is_active
        )

        progress_records = (
            self.progress_repository
            .get_by_user_id_and_date_range(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
            )
        )

        latest_progress_date = (
            progress_records[-1].progress_date
            if progress_records
            else None
        )

        return DashboardSummaryResponse(
            start_date=start_date,
            end_date=end_date,
            total_calories=float(total_calories),
            total_protein=float(total_protein),
            total_workout_duration_minutes=total_workout_duration,
            active_supplements=active_supplements,
            total_supplements=len(supplements),
            latest_progress_date=latest_progress_date,
        )