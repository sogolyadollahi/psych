from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class ProgressCreate(BaseModel):
    weight_kg: float | None = Field(default=None, gt=0, le=500)
    body_fat_percentage: float | None = Field(default=None, ge=0, le=100)
    chest_cm: float | None = Field(default=None, gt=0, le=300)
    waist_cm: float | None = Field(default=None, gt=0, le=300)
    arm_cm: float | None = Field(default=None, gt=0, le=200)
    thigh_cm: float | None = Field(default=None, gt=0, le=200)
    progress_date: date


class ProgressUpdate(BaseModel):
    weight_kg: float | None = Field(default=None, gt=0, le=500)
    body_fat_percentage: float | None = Field(default=None, ge=0, le=100)
    chest_cm: float | None = Field(default=None, gt=0, le=300)
    waist_cm: float | None = Field(default=None, gt=0, le=300)
    arm_cm: float | None = Field(default=None, gt=0, le=200)
    thigh_cm: float | None = Field(default=None, gt=0, le=200)
    progress_date: date | None = None


class ProgressResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    weight_kg: float | None = Field(validation_alias="weight")
    body_fat_percentage: float | None = Field(validation_alias="body_fat")
    chest_cm: float | None = Field(validation_alias="chest")
    waist_cm: float | None = Field(validation_alias="waist")
    arm_cm: float | None = Field(validation_alias="arm")
    thigh_cm: float | None = Field(validation_alias="thigh")

    progress_date: date
    created_at: datetime
    updated_at: datetime


class ProgressAnalyticsResponse(BaseModel):
    start_date: date
    end_date: date
    weight_change_kg: float | None
    body_fat_change_percentage: float | None
    chest_change_cm: float | None
    waist_change_cm: float | None
    arm_change_cm: float | None
    thigh_change_cm: float | None
