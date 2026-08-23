from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.v1.deps import get_db
from app.repositories.meal_repository import MealRepository
from app.repositories.meal_item_repository import MealItemRepository
from app.services.meal_service import MealService
from app.services.meal_item_service import MealItemService


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