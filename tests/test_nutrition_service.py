from decimal import Decimal

from app.services.nutrition.nutrition_service import NutritionService


def test_calculate_nutrition_for_quantity():
    nutrition = {
        "calories": Decimal("165"),
        "protein": Decimal("31"),
        "carbs": Decimal("0"),
        "fat": Decimal("3.6"),
    }

    result = NutritionService.calculate_for_quantity(
        nutrition_per_100g=nutrition,
        quantity_grams=Decimal("250"),
    )

    assert result["calories"] == Decimal("412.5")
    assert result["protein"] == Decimal("77.5")
    assert result["carbs"] == Decimal("0")
    assert result["fat"] == Decimal("9.0")