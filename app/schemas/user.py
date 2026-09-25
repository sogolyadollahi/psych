from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# =========================================================
# Authentication Schemas
# =========================================================


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=1,
        max_length=128,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime


# =========================================================
# User Profile Schemas
# =========================================================


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    email: EmailStr

    first_name: str | None = None
    last_name: str | None = None

    age: int | None = Field(
        default=None,
        ge=13,
        le=120,
    )

    gender: str | None = None

    height_cm: float | None = Field(
        default=None,
        gt=0,
        le=300,
    )

    activity_level: str | None = None
    goal: str | None = None

    created_at: datetime
    updated_at: datetime


class UserProfileUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        max_length=100,
    )

    last_name: str | None = Field(
        default=None,
        max_length=100,
    )

    age: int | None = Field(
        default=None,
        ge=13,
        le=120,
    )

    gender: str | None = Field(
        default=None,
        max_length=20,
    )

    height_cm: float | None = Field(
        default=None,
        gt=0,
        le=300,
    )

    activity_level: str | None = Field(
        default=None,
        max_length=30,
    )

    goal: str | None = Field(
        default=None,
        max_length=30,
    )

    # =========================================================
# Account Management Schemas
# =========================================================


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(
        min_length=1,
        max_length=128,
    )

    new_password: str = Field(
        min_length=8,
        max_length=128,
    )