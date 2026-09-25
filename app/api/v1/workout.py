from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.workout import (
    WorkoutCreate,
    WorkoutResponse,
    WorkoutUpdate,
)
from app.services.workout_service import WorkoutService


router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"],
)


@router.post(
    "",
    response_model=WorkoutResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create workout",
    description="Create a new workout for the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        422: {"description": "Validation error."},
    },
)
def create_workout(
    workout_data: WorkoutCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workout_service = WorkoutService(db)

    return workout_service.create(
        current_user=current_user,
        workout_data=workout_data,
    )


@router.get(
    "",
    response_model=list[WorkoutResponse],
    summary="List workouts",
    description="Return all workouts belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
    },
)
def get_workouts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workout_service = WorkoutService(db)

    return workout_service.get_all(
        current_user=current_user,
    )


@router.get(
    "/{workout_id}",
    response_model=WorkoutResponse,
    summary="Get workout",
    description="Return a specific workout belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Workout not found."},
    },
)
def get_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workout_service = WorkoutService(db)

    try:
        return workout_service.get_by_id(
            current_user=current_user,
            workout_id=workout_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.patch(
    "/{workout_id}",
    response_model=WorkoutResponse,
    summary="Update workout",
    description="Update a workout belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Workout not found."},
        422: {"description": "Validation error."},
    },
)
def update_workout(
    workout_id: int,
    workout_data: WorkoutUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workout_service = WorkoutService(db)

    try:
        return workout_service.update(
            current_user=current_user,
            workout_id=workout_id,
            workout_data=workout_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )


@router.delete(
    "/{workout_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete workout",
    description="Delete a workout belonging to the authenticated user.",
    responses={
        401: {"description": "Authentication credentials are invalid or missing."},
        404: {"description": "Workout not found."},
    },
)
def delete_workout(
    workout_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    workout_service = WorkoutService(db)

    try:
        workout_service.delete(
            current_user=current_user,
            workout_id=workout_id,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )