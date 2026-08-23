from datetime import date
from decimal import Decimal
from unittest.mock import Mock

from app.models.meal import Meal
from app.models.meal_item import MealItem
from app.services.meal_service import MealService
from app.services.meal_item_service import MealItemService


def test_create_meal():
    repository = Mock()
    service = MealService(repository)

    repository.create.side_effect = lambda meal: meal

    meal = service.create_meal(
        user_id=1,
        name="Lunch",
        meal_date=date(2026, 8, 22),
    )

    assert meal.user_id == 1
    assert meal.name == "Lunch"
    assert meal.meal_date == date(2026, 8, 22)

    repository.create.assert_called_once()


def test_get_meal_owner_can_access():
    repository = Mock()
    service = MealService(repository)

    meal = Meal(
        id=1,
        user_id=10,
        name="Lunch",
        meal_date=date(2026, 8, 22),
    )

    repository.get_by_id.return_value = meal

    result = service.get_meal(
        meal_id=1,
        user_id=10,
    )

    assert result == meal


def test_get_meal_other_user_cannot_access():
    repository = Mock()
    service = MealService(repository)

    meal = Meal(
        id=1,
        user_id=10,
        name="Lunch",
        meal_date=date(2026, 8, 22),
    )

    repository.get_by_id.return_value = meal

    result = service.get_meal(
        meal_id=1,
        user_id=99,
    )

    assert result is None


def test_calculate_nutrition_totals():
    items = [
        MealItem(
            id=1,
            meal_id=1,
            name="Chicken",
            quantity=Decimal("200"),
            unit="g",
            calories=Decimal("330"),
            protein=Decimal("62"),
            carbs=Decimal("0"),
            fat=Decimal("7.2"),
        ),
        MealItem(
            id=2,
            meal_id=1,
            name="Rice",
            quantity=Decimal("150"),
            unit="g",
            calories=Decimal("195"),
            protein=Decimal("4"),
            carbs=Decimal("42"),
            fat=Decimal("0.5"),
        ),
    ]

    totals = MealService.calculate_nutrition_totals(items)

    assert totals["calories"] == Decimal("525")
    assert totals["protein"] == Decimal("66")
    assert totals["carbs"] == Decimal("42")
    assert totals["fat"] == Decimal("7.7")


def test_create_item_owner_can_access_meal():
    meal_repository = Mock()
    item_repository = Mock()

    service = MealItemService(
        meal_item_repository=item_repository,
        meal_repository=meal_repository,
    )

    meal = Meal(
        id=1,
        user_id=10,
        name="Lunch",
        meal_date=date(2026, 8, 22),
    )

    meal_repository.get_by_id.return_value = meal
    item_repository.create.side_effect = lambda item: item

    item = service.create_item(
        meal_id=1,
        user_id=10,
        name="Chicken",
        quantity=Decimal("200"),
        unit="g",
        calories=Decimal("330"),
        protein=Decimal("62"),
        carbs=Decimal("0"),
        fat=Decimal("7.2"),
    )

    assert item is not None
    assert item.meal_id == 1
    assert item.name == "Chicken"

    item_repository.create.assert_called_once()


def test_create_item_other_user_cannot_access_meal():
    meal_repository = Mock()
    item_repository = Mock()

    service = MealItemService(
        meal_item_repository=item_repository,
        meal_repository=meal_repository,
    )

    meal = Meal(
        id=1,
        user_id=10,
        name="Lunch",
        meal_date=date(2026, 8, 22),
    )

    meal_repository.get_by_id.return_value = meal

    result = service.create_item(
        meal_id=1,
        user_id=99,
        name="Chicken",
        quantity=Decimal("200"),
        unit="g",
        calories=Decimal("330"),
        protein=Decimal("62"),
        carbs=Decimal("0"),
        fat=Decimal("7.2"),
    )

    assert result is None
    item_repository.create.assert_not_called()