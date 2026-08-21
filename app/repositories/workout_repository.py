from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.workout import Workout


class WorkoutRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, workout: Workout) -> Workout:
        self.db.add(workout)
        self.db.commit()
        self.db.refresh(workout)

        return workout

    def get_by_id(self, workout_id: int) -> Workout | None:
        statement = select(Workout).where(
            Workout.id == workout_id
        )

        return self.db.scalar(statement)

    def get_by_user_id(self, user_id: int) -> list[Workout]:
        statement = (
            select(Workout)
            .where(Workout.user_id == user_id)
            .order_by(Workout.workout_date.desc())
        )

        return list(self.db.scalars(statement).all())

    def update(self, workout: Workout) -> Workout:
        self.db.commit()
        self.db.refresh(workout)

        return workout

    def delete(self, workout: Workout) -> None:
        self.db.delete(workout)
        self.db.commit()