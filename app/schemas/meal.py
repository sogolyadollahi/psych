from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class MealItemCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=150,
    )

    quantity: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    unit: str = Field(
        min_length=1,
        max_length=30,
    )

    calories: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    protein: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    carbs: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    fat: Decimal = Field(
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    source: str | None = Field(
        default=None,
        max_length=50,
    )

    source_food_id: str | None = Field(
        default=None,
        max_length=100,
    )


class MealItemUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )

    quantity: Decimal | None = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    unit: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    calories: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    protein: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    carbs: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    fat: Decimal | None = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    source: str | None = Field(
        default=None,
        max_length=50,
    )

    source_food_id: str | None = Field(
        default=None,
        max_length=100,
    )


class MealItemResponse(BaseModel):

    id: int
    meal_id: int
    name: str
    quantity: Decimal
    unit: str
    calories: Decimal
    protein: Decimal
    carbs: Decimal
    fat: Decimal
    source: str | None
    source_food_id: str | None


class MealCreate(BaseModel):

    name: str = Field(
        min_length=1,
        max_length=100,
    )

    meal_date: date


class MealUpdate(BaseModel):

    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    meal_date: date | None = None


class NutritionTotals(BaseModel):

    calories: Decimal
    protein: Decimal
    carbs: Decimal
    fat: Decimal


class MealResponse(BaseModel):

    id: int
    user_id: int
    name: str
    meal_date: date


class MealDetailResponse(BaseModel):

    id: int
    user_id: int
    name: str
    meal_date: date
    items: list[MealItemResponse]
    nutrition_totals: NutritionTotals