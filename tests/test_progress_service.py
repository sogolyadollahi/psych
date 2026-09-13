from datetime import date
from unittest.mock import Mock

import pytest

from app.models.progress import Progress
from app.models.user import User
from app.schemas.progress import (
    ProgressCreate,
    ProgressUpdate,
)
from app.services.progress_service import ProgressService


# =========================================================
# Helpers
# =========================================================

def create_user(
    user_id: int = 1,
) -> User:
    return User(
        id=user_id,
        email=f"user{user_id}@test.com",
        hashed_password="fake-hash",
    )


def create_progress(
    progress_id: int = 1,
    user_id: int = 1,
    progress_date: date = date(2026, 8, 22),
    weight: float | None = 80.0,
    body_fat: float | None = 20.0,
    chest: float | None = 100.0,
    waist: float | None = 85.0,
    arm: float | None = 35.0,
    thigh: float | None = 55.0,
) -> Progress:
    return Progress(
        id=progress_id,
        user_id=user_id,
        progress_date=progress_date,
        weight=weight,
        body_fat=body_fat,
        chest=chest,
        waist=waist,
        arm=arm,
        thigh=thigh,
    )


# =========================================================
# CREATE
# =========================================================

def test_create_progress():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    repository.create.side_effect = lambda progress: progress

    user = create_user(1)

    progress_data = ProgressCreate(
        weight_kg=80.0,
        body_fat_percentage=20.0,
        chest_cm=100.0,
        waist_cm=85.0,
        arm_cm=35.0,
        thigh_cm=55.0,
        progress_date=date(2026, 8, 22),
    )

    result = service.create(
        current_user=user,
        progress_data=progress_data,
    )

    assert result.user_id == 1
    assert result.weight == 80.0
    assert result.body_fat == 20.0
    assert result.chest == 100.0
    assert result.waist == 85.0
    assert result.arm == 35.0
    assert result.thigh == 55.0
    assert result.progress_date == date(2026, 8, 22)

    repository.create.assert_called_once()


# =========================================================
# GET ALL
# =========================================================

def test_get_all_returns_only_current_user_records():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    records = [
        create_progress(
            progress_id=1,
            user_id=1,
        ),
        create_progress(
            progress_id=2,
            user_id=1,
            progress_date=date(2026, 8, 23),
        ),
    ]

    repository.get_by_user_id.return_value = records

    user = create_user(1)

    result = service.get_all(
        current_user=user,
    )

    assert result == records

    repository.get_by_user_id.assert_called_once_with(1)


# =========================================================
# GET BY ID - OWNER
# =========================================================

def test_get_by_id_owner_can_access():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    progress = create_progress(
        progress_id=1,
        user_id=1,
    )

    repository.get_by_id.return_value = progress

    user = create_user(1)

    result = service.get_by_id(
        current_user=user,
        progress_id=1,
    )

    assert result == progress

    repository.get_by_id.assert_called_once_with(1)


# =========================================================
# GET BY ID - NOT FOUND
# =========================================================

def test_get_by_id_not_found():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    repository.get_by_id.return_value = None

    user = create_user(1)

    with pytest.raises(
        ValueError,
        match="Progress record not found",
    ):
        service.get_by_id(
            current_user=user,
            progress_id=999,
        )


# =========================================================
# GET BY ID - OTHER USER
# =========================================================

def test_get_by_id_other_user_cannot_access():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    progress = create_progress(
        progress_id=1,
        user_id=1,
    )

    repository.get_by_id.return_value = progress

    user = create_user(2)

    with pytest.raises(
        ValueError,
        match="Progress record not found",
    ):
        service.get_by_id(
            current_user=user,
            progress_id=1,
        )


# =========================================================
# UPDATE - OWNER
# =========================================================

def test_update_progress():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    progress = create_progress(
        progress_id=1,
        user_id=1,
    )

    repository.get_by_id.return_value = progress
    repository.update.side_effect = lambda item: item

    user = create_user(1)

    update_data = ProgressUpdate(
        weight_kg=78.5,
        body_fat_percentage=18.5,
        chest_cm=101.0,
        waist_cm=82.0,
        arm_cm=36.0,
        thigh_cm=56.0,
        progress_date=date(2026, 8, 25),
    )

    result = service.update(
        current_user=user,
        progress_id=1,
        progress_data=update_data,
    )

    assert result.weight == 78.5
    assert result.body_fat == 18.5
    assert result.chest == 101.0
    assert result.waist == 82.0
    assert result.arm == 36.0
    assert result.thigh == 56.0
    assert result.progress_date == date(2026, 8, 25)

    repository.update.assert_called_once_with(progress)


# =========================================================
# UPDATE - PARTIAL
# =========================================================

def test_update_progress_partial_fields():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    progress = create_progress(
        progress_id=1,
        user_id=1,
        weight=80.0,
        body_fat=20.0,
        waist=85.0,
    )

    repository.get_by_id.return_value = progress
    repository.update.side_effect = lambda item: item

    user = create_user(1)

    update_data = ProgressUpdate(
        weight_kg=78.0,
    )

    result = service.update(
        current_user=user,
        progress_id=1,
        progress_data=update_data,
    )

    assert result.weight == 78.0
    assert result.body_fat == 20.0
    assert result.waist == 85.0

    repository.update.assert_called_once_with(progress)


# =========================================================
# UPDATE - OTHER USER
# =========================================================

def test_update_progress_other_user_cannot_access():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    progress = create_progress(
        progress_id=1,
        user_id=1,
    )

    repository.get_by_id.return_value = progress

    user = create_user(2)

    update_data = ProgressUpdate(
        weight_kg=70.0,
    )

    with pytest.raises(
        ValueError,
        match="Progress record not found",
    ):
        service.update(
            current_user=user,
            progress_id=1,
            progress_data=update_data,
        )

    repository.update.assert_not_called()


# =========================================================
# DELETE - OWNER
# =========================================================

def test_delete_progress():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    progress = create_progress(
        progress_id=1,
        user_id=1,
    )

    repository.get_by_id.return_value = progress

    user = create_user(1)

    result = service.delete(
        current_user=user,
        progress_id=1,
    )

    assert result is None

    repository.delete.assert_called_once_with(progress)


# =========================================================
# DELETE - OTHER USER
# =========================================================

def test_delete_progress_other_user_cannot_access():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    progress = create_progress(
        progress_id=1,
        user_id=1,
    )

    repository.get_by_id.return_value = progress

    user = create_user(2)

    with pytest.raises(
        ValueError,
        match="Progress record not found",
    ):
        service.delete(
            current_user=user,
            progress_id=1,
        )

    repository.delete.assert_not_called()


# =========================================================
# ANALYTICS
# =========================================================

def test_get_analytics_calculates_changes():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    first = create_progress(
        progress_id=1,
        user_id=1,
        progress_date=date(2026, 8, 20),
        weight=80.0,
        body_fat=20.0,
        chest=100.0,
        waist=85.0,
        arm=35.0,
        thigh=55.0,
    )

    last = create_progress(
        progress_id=2,
        user_id=1,
        progress_date=date(2026, 8, 30),
        weight=77.5,
        body_fat=18.5,
        chest=102.0,
        waist=81.5,
        arm=36.0,
        thigh=56.5,
    )

    repository.get_by_user_id_and_date_range.return_value = [
        first,
        last,
    ]

    user = create_user(1)

    result = service.get_analytics(
        current_user=user,
    )

    assert result.start_date == date(2026, 8, 20)
    assert result.end_date == date(2026, 8, 30)

    assert result.weight_change_kg == -2.5
    assert result.body_fat_change_percentage == -1.5
    assert result.chest_change_cm == 2.0
    assert result.waist_change_cm == -3.5
    assert result.arm_change_cm == 1.0
    assert result.thigh_change_cm == 1.5


# =========================================================
# ANALYTICS - DATE RANGE
# =========================================================

def test_get_analytics_passes_date_range_to_repository():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    first = create_progress(
        progress_id=1,
        user_id=1,
        progress_date=date(2026, 8, 20),
    )

    repository.get_by_user_id_and_date_range.return_value = [
        first,
    ]

    user = create_user(1)

    start_date = date(2026, 8, 1)
    end_date = date(2026, 8, 31)

    service.get_analytics(
        current_user=user,
        start_date=start_date,
        end_date=end_date,
    )

    repository.get_by_user_id_and_date_range.assert_called_once_with(
        user_id=1,
        start_date=start_date,
        end_date=end_date,
    )


# =========================================================
# ANALYTICS - INVALID DATE RANGE
# =========================================================

def test_get_analytics_invalid_date_range():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    user = create_user(1)

    with pytest.raises(
        ValueError,
        match="start_date cannot be after end_date",
    ):
        service.get_analytics(
            current_user=user,
            start_date=date(2026, 8, 31),
            end_date=date(2026, 8, 1),
        )

    repository.get_by_user_id_and_date_range.assert_not_called()


# =========================================================
# ANALYTICS - NO RECORDS
# =========================================================

def test_get_analytics_no_records():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    repository.get_by_user_id_and_date_range.return_value = []

    user = create_user(1)

    with pytest.raises(
        ValueError,
        match="No progress records found for the selected date range",
    ):
        service.get_analytics(
            current_user=user,
        )


# =========================================================
# ANALYTICS - NONE VALUES
# =========================================================

def test_get_analytics_returns_none_for_missing_measurements():
    repository = Mock()
    service = ProgressService.__new__(ProgressService)

    service.progress_repository = repository

    first = create_progress(
        progress_id=1,
        user_id=1,
        progress_date=date(2026, 8, 20),
        weight=80.0,
        body_fat=None,
        chest=None,
        waist=85.0,
        arm=None,
        thigh=55.0,
    )

    last = create_progress(
        progress_id=2,
        user_id=1,
        progress_date=date(2026, 8, 30),
        weight=78.0,
        body_fat=None,
        chest=102.0,
        waist=82.0,
        arm=36.0,
        thigh=None,
    )

    repository.get_by_user_id_and_date_range.return_value = [
        first,
        last,
    ]

    user = create_user(1)

    result = service.get_analytics(
        current_user=user,
    )

    assert result.weight_change_kg == -2.0
    assert result.body_fat_change_percentage is None
    assert result.chest_change_cm is None
    assert result.waist_change_cm == -3.0
    assert result.arm_change_cm is None
    assert result.thigh_change_cm is None