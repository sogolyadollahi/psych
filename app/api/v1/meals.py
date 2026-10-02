from fastapi import APIRouter, Depends, HTTPException, Request, status
from decimal import Decimal


from app.api.v1.deps import get_current_user
from app.api.v1.meal_deps import (
    get_meal_item_service,
    get_meal_service,
    get_nutrition_service,
)
from app.core.rate_limiter import limiter
from app.models.user import User
from app.schemas.meal import (
    FoodNutritionRequest,
    FoodNutritionResponse,
    FoodSearchResult,
    MealCreate,
    MealDetailResponse,
    MealItemCreate,
    MealItemResponse,
    MealItemUpdate,
    MealResponse,
    MealUpdate,
    NutritionTotals,
)
from app.services.meal_item_service import MealItemService
from app.services.meal_service import MealService
from app.services.nutrition.nutrition_service import NutritionService


router = APIRouter(
    prefix="/meals",
    tags=["Meals"],
)


# =========================================================
# Meal
# =========================================================

@router.post(
    "",
    response_model=MealResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create meal",
    description="Create a new meal for the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
    },
)
def create_meal(
    data: MealCreate,
    current_user: User = Depends(get_current_user),
    service: MealService = Depends(get_meal_service),
):
    return service.create_meal(
        user_id=current_user.id,
        name=data.name,
        meal_date=data.meal_date,
    )


@router.get(
    "",
    response_model=list[MealResponse],
    summary="List meals",
    description="Return all meals belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
    },
)
def get_meals(
    current_user: User = Depends(get_current_user),
    service: MealService = Depends(get_meal_service),
):
    return service.get_user_meals(
        user_id=current_user.id,
    )


# =========================================================
# Nutrition / Food
# =========================================================

@router.get(
    "/foods/search",
    response_model=list[FoodSearchResult],
    summary="Search foods",
    description="Search for foods using the nutrition service.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
        429: {"description": "Too many food search requests."},
        502: {"description": "Food database service is unavailable."},
    },
)
@limiter.limit("20/minute")
def search_food(
    request: Request,
    query: str,
    _current_user: User = Depends(get_current_user),
    nutrition_service: NutritionService = Depends(
        get_nutrition_service
    ),
):
    try:
        foods = nutrition_service.search_food(
            query=query,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Food database service is currently unavailable.",
        ) from exc

    return [
        FoodSearchResult(
            fdc_id=food["fdcId"],
            description=food["description"],
            data_type=food.get("dataType"),
        )
        for food in foods
    ]


@router.post(
    "/foods/nutrition",
    response_model=FoodNutritionResponse,
    summary="Get food nutrition",
    description="Retrieve nutritional information for a food.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
        429: {"description": "Too many nutrition lookup requests."},
        502: {"description": "Food database service is unavailable."},
    },
)
@limiter.limit("20/minute")
def get_food_nutrition(
    request: Request,
    data: FoodNutritionRequest,
    _current_user: User = Depends(get_current_user),
    nutrition_service: NutritionService = Depends(
        get_nutrition_service
    ),
):
    try:
        nutrition = nutrition_service.get_nutrition_for_food(
            fdc_id=data.fdc_id,
            quantity_grams=data.quantity_grams,
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Food database service is currently unavailable.",
        ) from exc

    return FoodNutritionResponse(
        fdc_id=data.fdc_id,
        quantity_grams=data.quantity_grams,
        calories=nutrition["calories"],
        protein=nutrition["protein"],
        carbs=nutrition["carbs"],
        fat=nutrition["fat"],
        source="usda",
    )


# =========================================================
# Single Meal
# =========================================================

@router.get(
    "/{meal_id}",
    response_model=MealDetailResponse,
    summary="Get meal",
    description="Return a specific meal belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Meal not found."},
    },
)
def get_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    meal_service: MealService = Depends(get_meal_service),
    item_service: MealItemService = Depends(get_meal_item_service),
):
    meal = meal_service.get_meal(
        meal_id=meal_id,
        user_id=current_user.id,
    )

    if meal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found",
        )

    items = item_service.get_meal_items(
        meal_id=meal.id,
        user_id=current_user.id,
    )

    if items is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found",
        )

    totals = MealService.calculate_nutrition_totals(
        items
    )

    return MealDetailResponse(
        id=meal.id,
        user_id=meal.user_id,
        name=meal.name,
        meal_date=meal.meal_date,
        items=items,
        nutrition_totals=NutritionTotals(**totals),
    )


@router.patch(
    "/{meal_id}",
    response_model=MealResponse,
    summary="Update meal",
    description="Update a meal belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Meal not found."},
        422: {"description": "Validation error."},
    },
)
def update_meal(
    meal_id: int,
    data: MealUpdate,
    current_user: User = Depends(get_current_user),
    service: MealService = Depends(get_meal_service),
):
    meal = service.get_meal(
        meal_id=meal_id,
        user_id=current_user.id,
    )

    if meal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found",
        )

    return service.update_meal(
        meal=meal,
        name=data.name,
        meal_date=data.meal_date,
    )


@router.delete(
    "/{meal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete meal",
    description="Delete a meal belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Meal not found."},
    },
)
def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    service: MealService = Depends(get_meal_service),
):
    meal = service.get_meal(
        meal_id=meal_id,
        user_id=current_user.id,
    )

    if meal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found",
        )

    service.delete_meal(meal)


# =========================================================
# Meal Items
# =========================================================

@router.post(
    "/{meal_id}/items",
    response_model=MealItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add meal item",
    description="Add a food item to a meal belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Meal not found."},
        422: {"description": "Validation error."},
    },
)
def create_meal_item(
    meal_id: int,
    data: MealItemCreate,
    current_user: User = Depends(get_current_user),
    service: MealItemService = Depends(get_meal_item_service),
):
    item = service.create_item(
        meal_id=meal_id,
        user_id=current_user.id,
        name=data.name,
        quantity=data.quantity,
        unit=data.unit,
        calories=data.calories,
        protein=data.protein,
        carbs=data.carbs,
        fat=data.fat,
        source=data.source,
        source_food_id=data.source_food_id,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal not found",
        )

    return item


@router.patch(
    "/{meal_id}/items/{item_id}",
    response_model=MealItemResponse,
    summary="Update meal item",
    description="Update an item belonging to a meal of the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Meal or meal item not found."},
        422: {"description": "Validation error."},
    },
)
def update_meal_item(
    meal_id: int,
    item_id: int,
    data: MealItemUpdate,
    current_user: User = Depends(get_current_user),
    service: MealItemService = Depends(get_meal_item_service),
):
    item = service.get_item(
        meal_item_id=item_id,
        user_id=current_user.id,
    )

    if item is None or item.meal_id != meal_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal item not found",
        )

    return service.update_item(
        item=item,
        name=data.name,
        quantity=data.quantity,
        unit=data.unit,
        calories=data.calories,
        protein=data.protein,
        carbs=data.carbs,
        fat=data.fat,
        source=data.source,
        source_food_id=data.source_food_id,
    )


@router.delete(
    "/{meal_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete meal item",
    description="Delete an item belonging to a meal of the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Meal or meal item not found."},
    },
)
def delete_meal_item(
    meal_id: int,
    item_id: int,
    current_user: User = Depends(get_current_user),
    service: MealItemService = Depends(get_meal_item_service),
):
    item = service.get_item(
        meal_item_id=item_id,
        user_id=current_user.id,
    )

    if item is None or item.meal_id != meal_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal item not found",
        )

    service.delete_item(item)