from datetime import datetime, time

from pydantic import BaseModel, Field


class SupplementCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    dosage: str = Field(
        min_length=1,
        max_length=100,
    )

    reminder_time: time

    notes: str | None = Field(
        default=None,
        max_length=500,
    )


class SupplementUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    dosage: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    reminder_time: time | None = None

    notes: str | None = Field(
        default=None,
        max_length=500,
    )

    is_active: bool | None = None


class SupplementResponse(BaseModel):
    id: int
    name: str
    dosage: str
    reminder_time: time
    notes: str | None
    is_active: bool
    created_at: datetime