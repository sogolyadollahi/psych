from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.progress import (
    ProgressAnalyticsResponse,
    ProgressCreate,
    ProgressResponse,
    ProgressUpdate,
)
from app.services.progress_service import ProgressService


router = APIRouter(
    prefix="/progress",
    tags=["Progress"],
)


@router.post(
    "",
    response_model=ProgressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create progress record",
    description="Create a new progress record for the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
    },
)
def create_progress(
    progress_data: ProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress_service = ProgressService(db)

    return progress_service.create(
        current_user=current_user,
        progress_data=progress_data,
    )


@router.get(
    "",
    response_model=list[ProgressResponse],
    summary="List progress records",
    description="Return all progress records belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
    },
)
def get_progress_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress_service = ProgressService(db)

    return progress_service.get_all(
        current_user=current_user,
    )


@router.get(
    "/analytics",
    response_model=ProgressAnalyticsResponse,
    summary="Get progress analytics",
    description="Return progress analytics for the authenticated user, optionally filtered by date range.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
    },
)
def get_progress_analytics(
    start_date: date | None = None,
    end_date: date | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress_service = ProgressService(db)

    try:
        return progress_service.get_analytics(
            current_user=current_user,
            start_date=start_date,
            end_date=end_date,
        )
    except ValueError as error:
        error_message = str(error)

        if error_message == "start_date cannot be after end_date":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_message,
            ) from error

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_message,
        ) from error


@router.get(
    "/{progress_id}",
    response_model=ProgressResponse,
    summary="Get progress record",
    description="Return a specific progress record belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Progress record not found."},
    },
)
def get_progress(
    progress_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress_service = ProgressService(db)

    try:
        return progress_service.get_by_id(
            current_user=current_user,
            progress_id=progress_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.patch(
    "/{progress_id}",
    response_model=ProgressResponse,
    summary="Update progress record",
    description="Update a progress record belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Progress record not found."},
        422: {"description": "Validation error."},
    },
)
def update_progress(
    progress_id: int,
    progress_data: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress_service = ProgressService(db)

    try:
        return progress_service.update(
            current_user=current_user,
            progress_id=progress_id,
            progress_data=progress_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.delete(
    "/{progress_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete progress record",
    description="Delete a progress record belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Progress record not found."},
    },
)
def delete_progress(
    progress_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    progress_service = ProgressService(db)

    try:
        progress_service.delete(
            current_user=current_user,
            progress_id=progress_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )