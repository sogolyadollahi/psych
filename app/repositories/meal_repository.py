from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.meal import Meal


class MealRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, meal: Meal) -> Meal:
        self.db.add(meal)
        self.db.commit()
        self.db.refresh(meal)

        return meal

    def get_by_id(self, meal_id: int) -> Meal | None:
        statement = select(Meal).where(
            Meal.id == meal_id
        )

        return self.db.scalar(statement)

    def get_by_user_id(self, user_id: int) -> list[Meal]:
        statement = (
            select(Meal)
            .where(Meal.user_id == user_id)
            .order_by(Meal.meal_date.desc())
        )

        return list(self.db.scalars(statement).all())

    def update(self, meal: Meal) -> Meal:
        self.db.commit()
        self.db.refresh(meal)

        return meal

    def delete(self, meal: Meal) -> None:
        self.db.delete(meal)
        self.db.commit()