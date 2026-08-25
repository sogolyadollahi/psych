from decimal import Decimal
from typing import Any

from app.services.nutrition.usda_provider import USDAProvider


class NutritionService:
    CALORIES_NUTRIENT_ID = 1008
    PROTEIN_NUTRIENT_ID = 1003
    CARBS_NUTRIENT_ID = 1005
    FAT_NUTRIENT_ID = 1004

    def __init__(self, provider: USDAProvider):
        self.provider = provider

    @classmethod
    def extract_nutrition(
        cls,
        food: dict[str, Any],
    ) -> dict[str, Decimal]:
        nutrients = {
            "calories": Decimal("0"),
            "protein": Decimal("0"),
            "carbs": Decimal("0"),
            "fat": Decimal("0"),
        }

        nutrient_mapping = {
            cls.CALORIES_NUTRIENT_ID: "calories",
            cls.PROTEIN_NUTRIENT_ID: "protein",
            cls.CARBS_NUTRIENT_ID: "carbs",
            cls.FAT_NUTRIENT_ID: "fat",
        }

        for nutrient in food.get("foodNutrients", []):
            nutrient_id = nutrient.get("nutrient", {}).get("id")
            amount = nutrient.get("amount")

            if nutrient_id in nutrient_mapping and amount is not None:
                nutrients[nutrient_mapping[nutrient_id]] = Decimal(
                    str(amount)
                )

        return nutrients

    @staticmethod
    def calculate_for_quantity(
        nutrition_per_100g: dict[str, Decimal],
        quantity_grams: Decimal,
    ) -> dict[str, Decimal]:
        factor = quantity_grams / Decimal("100")

        return {
            nutrient: amount * factor
            for nutrient, amount in nutrition_per_100g.items()
        }

    def search_food(
        self,
        query: str,
        page_size: int = 10,
    ) -> list[dict[str, Any]]:
        return self.provider.search_food(
            query=query,
            page_size=page_size,
        )

    def get_nutrition_for_food(
        self,
        fdc_id: int,
        quantity_grams: Decimal,
    ) -> dict[str, Decimal]:
        food = self.provider.get_food(fdc_id)

        nutrition_per_100g = self.extract_nutrition(food)

        return self.calculate_for_quantity(
            nutrition_per_100g=nutrition_per_100g,
            quantity_grams=quantity_grams,
        )