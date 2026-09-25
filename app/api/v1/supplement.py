from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.deps import get_current_user
from app.api.v1.supplement_deps import get_supplement_service
from app.models.user import User
from app.schemas.supplement import (
    SupplementCreate,
    SupplementResponse,
    SupplementUpdate,
)
from app.services.supplement_service import SupplementService


router = APIRouter(
    prefix="/supplements",
    tags=["Supplements"],
)


# =========================================================
# Create Supplement
# =========================================================

@router.post(
    "",
    response_model=SupplementResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create supplement",
    description="Create a new supplement for the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
    },
)
def create_supplement(
    data: SupplementCreate,
    current_user: User = Depends(get_current_user),
    service: SupplementService = Depends(
        get_supplement_service
    ),
):
    return service.create_supplement(
        user_id=current_user.id,
        name=data.name,
        dosage=data.dosage,
        reminder_time=data.reminder_time,
        notes=data.notes,
    )


# =========================================================
# Get User Supplements
# =========================================================

@router.get(
    "",
    response_model=list[SupplementResponse],
    summary="List supplements",
    description="Return all supplements belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
    },
)
def get_supplements(
    current_user: User = Depends(get_current_user),
    service: SupplementService = Depends(
        get_supplement_service
    ),
):
    return service.get_user_supplements(
        user_id=current_user.id,
    )


# =========================================================
# Get Single Supplement
# =========================================================

@router.get(
    "/{supplement_id}",
    response_model=SupplementResponse,
    summary="Get supplement",
    description="Return a specific supplement belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Supplement not found."},
    },
)
def get_supplement(
    supplement_id: int,
    current_user: User = Depends(get_current_user),
    service: SupplementService = Depends(
        get_supplement_service
    ),
):
    supplement = service.get_supplement(
        supplement_id=supplement_id,
        user_id=current_user.id,
    )

    if supplement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplement not found",
        )

    return supplement


# =========================================================
# Update Supplement
# =========================================================

@router.patch(
    "/{supplement_id}",
    response_model=SupplementResponse,
    summary="Update supplement",
    description="Update a supplement belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Supplement not found."},
        422: {"description": "Validation error."},
    },
)
def update_supplement(
    supplement_id: int,
    data: SupplementUpdate,
    current_user: User = Depends(get_current_user),
    service: SupplementService = Depends(
        get_supplement_service
    ),
):
    supplement = service.get_supplement(
        supplement_id=supplement_id,
        user_id=current_user.id,
    )

    if supplement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplement not found",
        )

    return service.update_supplement(
        supplement=supplement,
        name=data.name,
        dosage=data.dosage,
        reminder_time=data.reminder_time,
        notes=data.notes,
        is_active=data.is_active,
    )


# =========================================================
# Delete Supplement
# =========================================================

@router.delete(
    "/{supplement_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete supplement",
    description="Delete a supplement belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Supplement not found."},
    },
)
def delete_supplement(
    supplement_id: int,
    current_user: User = Depends(get_current_user),
    service: SupplementService = Depends(
        get_supplement_service
    ),
):
    supplement = service.get_supplement(
        supplement_id=supplement_id,
        user_id=current_user.id,
    )

    if supplement is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Supplement not found",
        )

    service.delete_supplement(supplement)

    return None