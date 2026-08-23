from decimal import Decimal

from app.models.meal_item import MealItem
from app.repositories.meal_item_repository import MealItemRepository
from app.repositories.meal_repository import MealRepository


class MealItemService:

    def __init__(
        self,
        meal_item_repository: MealItemRepository,
        meal_repository: MealRepository,
    ):
        self.meal_item_repository = meal_item_repository
        self.meal_repository = meal_repository

    def create_item(
        self,
        meal_id: int,
        user_id: int,
        name: str,
        quantity: Decimal,
        unit: str,
        calories: Decimal,
        protein: Decimal,
        carbs: Decimal,
        fat: Decimal,
        source: str | None = None,
        source_food_id: str | None = None,
    ) -> MealItem | None:

        meal = self.meal_repository.get_by_id(meal_id)

        if meal is None:
            return None

        if meal.user_id != user_id:
            return None

        meal_item = MealItem(
            meal_id=meal_id,
            name=name,
            quantity=quantity,
            unit=unit,
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            source=source,
            source_food_id=source_food_id,
        )

        return self.meal_item_repository.create(meal_item)

    def get_item(
        self,
        meal_item_id: int,
        user_id: int,
    ) -> MealItem | None:

        item = self.meal_item_repository.get_by_id(
            meal_item_id
        )

        if item is None:
            return None

        meal = self.meal_repository.get_by_id(item.meal_id)

        if meal is None:
            return None

        if meal.user_id != user_id:
            return None

        return item

    def get_meal_items(
        self,
        meal_id: int,
        user_id: int,
    ) -> list[MealItem] | None:

        meal = self.meal_repository.get_by_id(meal_id)

        if meal is None:
            return None

        if meal.user_id != user_id:
            return None

        return self.meal_item_repository.get_by_meal_id(
            meal_id
        )

    def update_item(
        self,
        item: MealItem,
        name: str | None = None,
        quantity: Decimal | None = None,
        unit: str | None = None,
        calories: Decimal | None = None,
        protein: Decimal | None = None,
        carbs: Decimal | None = None,
        fat: Decimal | None = None,
        source: str | None = None,
        source_food_id: str | None = None,
    ) -> MealItem:

        if name is not None:
            item.name = name

        if quantity is not None:
            item.quantity = quantity

        if unit is not None:
            item.unit = unit

        if calories is not None:
            item.calories = calories

        if protein is not None:
            item.protein = protein

        if carbs is not None:
            item.carbs = carbs

        if fat is not None:
            item.fat = fat

        if source is not None:
            item.source = source

        if source_food_id is not None:
            item.source_food_id = source_food_id

        return self.meal_item_repository.update(item)

    def delete_item(
        self,
        item: MealItem,
    ) -> None:
        self.meal_item_repository.delete(item)