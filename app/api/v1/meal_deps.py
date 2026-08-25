from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db
from app.repositories.meal_repository import MealRepository
from app.repositories.meal_item_repository import MealItemRepository
from app.services.meal_service import MealService
from app.services.meal_item_service import MealItemService
from app.services.nutrition.nutrition_service import NutritionService
from app.services.nutrition.usda_provider import USDAProvider


def get_meal_repository(
    db: Session = Depends(get_db),
) -> MealRepository:
    return MealRepository(db)


def get_meal_item_repository(
    db: Session = Depends(get_db),
) -> MealItemRepository:
    return MealItemRepository(db)


def get_meal_service(
    meal_repository: MealRepository = Depends(get_meal_repository),
) -> MealService:
    return MealService(meal_repository)


def get_meal_item_service(
    meal_item_repository: MealItemRepository = Depends(
        get_meal_item_repository
    ),
    meal_repository: MealRepository = Depends(
        get_meal_repository
    ),
) -> MealItemService:
    return MealItemService(
        meal_item_repository=meal_item_repository,
        meal_repository=meal_repository,
    )

def get_usda_provider() -> USDAProvider:
    return USDAProvider()


def get_nutrition_service(
    provider: USDAProvider = Depends(get_usda_provider),
) -> NutritionService:
    return NutritionService(provider)