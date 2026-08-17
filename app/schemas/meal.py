from datetime import date, datetime

from pydantic import BaseModel, Field

class MealItemCreate(BaseModel):
    food_name: str = Field(min_length=1, max_length=200)
    quantity_grams: float = Field(gt=0)

    calories: float = Field(ge=0)
    protein_grams: float = Field(default=0, ge=0)
    carbs_grams: float = Field(default=0, ge=0)
    fat_grams: float = Field(default=0, ge=0)


class Mealcreate(BaseModel):
    meal_type: str = Field(min_length=1, max_length=50)
    meal_date: date
    items: list[MealItemCreate] = Field(min_length=1)


class MealResponse(BaseModel):
    id: int
    meal_type: str
    meal_date: date
    items: list[MealItemCreate]
    total_calories: float
    total_protein_grams: float    
    total_carbs_grams: float
    total_fat_grams: float
    created_at: datetime