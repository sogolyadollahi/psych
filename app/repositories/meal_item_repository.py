from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.meal_item import MealItem


class MealItemRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, meal_item: MealItem) -> MealItem:
        self.db.add(meal_item)
        self.db.flush()
        self.db.refresh(meal_item)

        return meal_item

    def get_by_id(self, meal_item_id: int) -> MealItem | None:
        statement = select(MealItem).where(
            MealItem.id == meal_item_id
        )

        return self.db.scalar(statement)

    def get_by_meal_id(self, meal_id: int) -> list[MealItem]:
        statement = (
            select(MealItem)
            .where(MealItem.meal_id == meal_id)
            .order_by(MealItem.id)
        )

        return list(self.db.scalars(statement).all())

    def update(self, meal_item: MealItem) -> MealItem:
        self.db.flush()
        self.db.refresh(meal_item)

        return meal_item

    def delete(self, meal_item: MealItem) -> None:
        self.db.delete(meal_item)