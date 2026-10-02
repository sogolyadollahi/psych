from decimal import Decimal

from pydantic import BaseModel, Field


class FoodScanItemCreate(BaseModel):
    meal_id: int = Field(gt=0)
    fdc_id: int = Field(gt=0)
    quantity_grams: Decimal = Field(
        gt=0,
        le=100_000,
    )


class FoodDetection(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )


class FoodScanResponse(BaseModel):
    detections: list[FoodDetection]


class FoodCandidate(BaseModel):
    fdc_id: int
    description: str = Field(max_length=300)
    data_type: str | None = Field(default=None, max_length=50)
    brand_owner: str | None = Field(default=None, max_length=200)


class FoodCandidateResponse(BaseModel):
    detected_food: str = Field(
        min_length=1,
        max_length=100,
    )
    candidates: list[FoodCandidate]
