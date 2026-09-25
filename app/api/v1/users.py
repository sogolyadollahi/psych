from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserProfileResponse,
    UserProfileUpdate,
    ChangePasswordRequest,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_service(
    db: Session = Depends(get_db),
) -> UserService:
    return UserService(db)


@router.get(
    "/me",
    response_model=UserProfileResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.get_profile(
        current_user=current_user,
    )


@router.patch(
    "/me",
    response_model=UserProfileResponse,
)
def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    return service.update_profile(
        current_user=current_user,
        profile_data=profile_data,
    )


@router.patch(
    "/me/password",
    status_code=status.HTTP_204_NO_CONTENT,
)
def change_my_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    try:
        service.change_password(
            current_user=current_user,
            password_data=password_data,
        )

    except ValueError as exc:
        error_message = str(exc)

        if error_message == "Current password is incorrect":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            )

        if error_message == (
            "New password must be different from "
            "current password"
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to change password",
        )

    return None

@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_account(
    current_user: User = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    service.delete_account(
        current_user=current_user,
    )

    return None