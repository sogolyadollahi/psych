from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.core.rate_limiter import limiter
from app.models.user import User
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# =========================================================
# Register
# =========================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new Psych user account.",
    responses={
        409: {
            "description": "Email is already registered.",
        },
        422: {
            "description": "Validation error.",
        },
    },
)
@limiter.limit("5/minute")
def register(
    request: Request,
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)

    try:
        return auth_service.register(user_data)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        ) from error


# =========================================================
# Login
# =========================================================

@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate a user and return an access token.",
    responses={
        401: {
            "description": "Invalid email or password.",
        },
        422: {
            "description": "Validation error.",
        },
        429: {
            "description": "Too many login attempts.",
        },
    },
)
@limiter.limit("5/minute")
def login(
    request: Request,
    user_data: UserLogin,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)

    try:
        return auth_service.login(
            email=str(user_data.email),
            password=user_data.password,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error),
        ) from error


# =========================================================
# Current User
# =========================================================

@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Return the profile of the currently authenticated user.",
    responses={
        401: {
            "description": "Authentication credentials are invalid or missing.",
        },
    },
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user