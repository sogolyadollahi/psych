from datetime import time
from unittest.mock import Mock

from app.models.supplement import Supplement
from app.services.reminder_service import ReminderService


def test_get_due_supplements():
    repository = Mock()
    service = ReminderService(repository)

    supplements = [
        Supplement(
            id=1,
            user_id=10,
            name="Creatine",
            dosage="5g",
            reminder_time=time(14, 0),
            is_active=True,
        ),
        Supplement(
            id=2,
            user_id=20,
            name="Vitamin D",
            dosage="1000 IU",
            reminder_time=time(14, 0),
            is_active=True,
        ),
    ]

    repository.get_active_by_reminder_time.return_value = supplements

    result = service.get_due_supplements(
        reminder_time=time(14, 0),
    )

    assert result == supplements
    assert len(result) == 2

    repository.get_active_by_reminder_time.assert_called_once_with(
        reminder_time=time(14, 0),
    )


def test_no_due_supplements():
    repository = Mock()
    service = ReminderService(repository)

    repository.get_active_by_reminder_time.return_value = []

    result = service.get_due_supplements(
        reminder_time=time(15, 0),
    )

    assert result == []

    repository.get_active_by_reminder_time.assert_called_once_with(
        reminder_time=time(15, 0),
    )


def test_only_active_supplements_are_returned_by_repository():
    repository = Mock()
    service = ReminderService(repository)

    active_supplement = Supplement(
        id=1,
        user_id=10,
        name="Creatine",
        dosage="5g",
        reminder_time=time(14, 0),
        is_active=True,
    )

    repository.get_active_by_reminder_time.return_value = [
        active_supplement,
    ]

    result = service.get_due_supplements(
        reminder_time=time(14, 0),
    )

    assert len(result) == 1
    assert result[0].is_active is True