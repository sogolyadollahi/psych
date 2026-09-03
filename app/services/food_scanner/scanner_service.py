from decimal import Decimal
from typing import Any

from app.models.meal_item import MealItem
from app.services.food_scanner.detector import FoodDetector
from app.services.meal_item_service import MealItemService
from app.services.nutrition.nutrition_service import NutritionService


class ScannerService:

    def __init__(
        self,
        detector: FoodDetector,
        nutrition_service: NutritionService,
        meal_item_service: MealItemService,
    ):
        self.detector = detector
        self.nutrition_service = nutrition_service
        self.meal_item_service = meal_item_service

    def scan(self, image: bytes) -> list[str]:
        return self.detector.detect(image)

    def find_candidates(
        self,
        detected_food: str,
        page_size: int = 10,
    ) -> list[dict[str, Any]]:
        foods = self.nutrition_service.search_food(
            query=detected_food,
            page_size=page_size,
        )

        return [
            self.map_candidate(food)
            for food in foods
            if food.get("fdcId") is not None
        ]

    @staticmethod
    def map_candidate(
        food: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "fdc_id": food["fdcId"],
            "description": food.get(
                "description",
                "Unknown food",
            ),
            "data_type": food.get("dataType"),
            "brand_owner": food.get("brandOwner"),
        }

    def create_meal_item_from_food(
        self,
        meal_id: int,
        user_id: int,
        fdc_id: int,
        quantity_grams: Decimal,
    ) -> MealItem | None:

        food = self.nutrition_service.get_food(fdc_id)

        nutrition = self.nutrition_service.get_nutrition_for_food(
            fdc_id=fdc_id,
            quantity_grams=quantity_grams,
        )

        return self.meal_item_service.create_item(
            meal_id=meal_id,
            user_id=user_id,
            name=food.get(
                "description",
                "Unknown food",
            ),
            quantity=quantity_grams,
            unit="g",
            calories=nutrition["calories"],
            protein=nutrition["protein"],
            carbs=nutrition["carbs"],
            fat=nutrition["fat"],
            source="USDA",
            source_food_id=str(fdc_id),
        )