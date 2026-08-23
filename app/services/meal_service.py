from decimal import Decimal

from app.models.meal import Meal
from app.models.meal_item import MealItem
from app.repositories.meal_repository import MealRepository


class MealService:

    def __init__(
        self,
        meal_repository: MealRepository,
    ):
        self.meal_repository = meal_repository

    def create_meal(
        self,
        user_id: int,
        name: str,
        meal_date,
    ) -> Meal:
        meal = Meal(
            user_id=user_id,
            name=name,
            meal_date=meal_date,
        )

        return self.meal_repository.create(meal)

    def get_meal(
        self,
        meal_id: int,
        user_id: int,
    ) -> Meal | None:
        meal = self.meal_repository.get_by_id(meal_id)

        if meal is None:
            return None

        if meal.user_id != user_id:
            return None

        return meal

    def get_user_meals(
        self,
        user_id: int,
    ) -> list[Meal]:
        return self.meal_repository.get_by_user_id(user_id)

    def update_meal(
        self,
        meal: Meal,
        name: str | None = None,
        meal_date=None,
    ) -> Meal:

        if name is not None:
            meal.name = name

        if meal_date is not None:
            meal.meal_date = meal_date

        return self.meal_repository.update(meal)

    def delete_meal(
        self,
        meal: Meal,
    ) -> None:
        self.meal_repository.delete(meal)

    @staticmethod
    def calculate_nutrition_totals(
        items: list[MealItem],
    ) -> dict[str, Decimal]:

        total_calories = sum(
            (item.calories for item in items),
            Decimal("0"),
        )

        total_protein = sum(
            (item.protein for item in items),
            Decimal("0"),
        )

        total_carbs = sum(
            (item.carbs for item in items),
            Decimal("0"),
        )

        total_fat = sum(
            (item.fat for item in items),
            Decimal("0"),
        )

        return {
            "calories": total_calories,
            "protein": total_protein,
            "carbs": total_carbs,
            "fat": total_fat,
        }