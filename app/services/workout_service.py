from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workout import Workout
from app.repositories.workout_repository import WorkoutRepository
from app.schemas.workout import WorkoutCreate, WorkoutUpdate


class WorkoutService:

    def __init__(self, db: Session):
        self.workout_repository = WorkoutRepository(db)

    def create(
        self,
        current_user: User,
        workout_data: WorkoutCreate,
    ) -> Workout:

        workout = Workout(
            user_id=current_user.id,
            muscle_group=workout_data.muscle_group,
            duration_minutes=workout_data.duration_minutes,
            calories_burned=workout_data.calories_burned,
            workout_date=workout_data.workout_date,
        )

        return self.workout_repository.create(workout)

    def get_all(
        self,
        current_user: User,
    ) -> list[Workout]:

        return self.workout_repository.get_by_user_id(
            current_user.id
        )

    def get_by_id(
        self,
        current_user: User,
        workout_id: int,
    ) -> Workout:

        workout = self.workout_repository.get_by_id(workout_id)

        if workout is None:
            raise ValueError("Workout not found")

        if workout.user_id != current_user.id:
            raise ValueError("Workout not found")

        return workout

    def update(
        self,
        current_user: User,
        workout_id: int,
        workout_data: WorkoutUpdate,
    ) -> Workout:

        workout = self.get_by_id(
            current_user=current_user,
            workout_id=workout_id,
        )

        if workout_data.muscle_group is not None:
            workout.muscle_group = workout_data.muscle_group

        if workout_data.duration_minutes is not None:
            workout.duration_minutes = (
                workout_data.duration_minutes
            )

        if workout_data.calories_burned is not None:
            workout.calories_burned = (
                workout_data.calories_burned
            )

        if workout_data.workout_date is not None:
            workout.workout_date = workout_data.workout_date

        return self.workout_repository.update(workout)

    def delete(
        self,
        current_user: User,
        workout_id: int,
    ) -> None:

        workout = self.get_by_id(
            current_user=current_user,
            workout_id=workout_id,
        )

        self.workout_repository.delete(workout)