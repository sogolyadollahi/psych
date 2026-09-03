from pydantic import BaseModel, Field

from decimal import Decimal

from pydantic import BaseModel, Field


class FoodScanItemCreate(BaseModel):
    meal_id: int = Field(gt=0)
    fdc_id: int = Field(gt=0)
    quantity_grams: Decimal = Field(gt=0)


class FoodDetection(BaseModel):
    name: str = Field(min_length=1)


class FoodScanResponse(BaseModel):
    detections: list[FoodDetection]


class FoodCandidate(BaseModel):
    fdc_id: int
    description: str
    data_type: str | None = None
    brand_owner: str | None = None


class FoodCandidateResponse(BaseModel):
    detected_food: str
    candidates: list[FoodCandidate]