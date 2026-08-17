from datetime import date, datetime

from pydantic import BaseModel, Field


class ProgressCreate(BaseModel):
    weight_kg: float | None = Field(
        default=None,
        gt=0,
        le=500,
    )

    body_fat_percentage: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    chest_cm: float | None = Field(default=None, gt=0)
    waist_cm: float | None = Field(default=None, gt=0)
    arm_cm: float | None = Field(default=None, gt=0)
    thigh_cm: float | None = Field(default=None, gt=0)

    progress_date: date


class ProgressResponse(BaseModel):
    id: int 

    weight_kg: float | None
    body_fat_percentage: float | None

    chest_cm: float | None 
    waist_cm: float | None
    arm_cm: float | None
    thigh_cm: float | None

    progress_date: date
    created_at: date