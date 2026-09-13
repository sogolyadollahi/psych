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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.get(
    "/{progress_id}",
    response_model=ProgressResponse,
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