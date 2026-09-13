from datetime import datetime, time
from types import SimpleNamespace
from unittest.mock import Mock, call

from app.services.reminder_runner import ReminderRunner


def create_runner(due_supplements):
    reminder_service = Mock()
    notification_service = Mock()

    reminder_service.get_due_supplements.return_value = due_supplements

    runner = ReminderRunner(
        reminder_service=reminder_service,
        notification_service=notification_service,
    )

    return runner, reminder_service, notification_service


def test_runner_sends_notification_for_due_supplement():
    supplement = SimpleNamespace(
        id=1,
        name="Creatine",
    )

    runner, reminder_service, notification_service = create_runner(
        [supplement]
    )

    result = runner.run(
        current_time=datetime(2026, 9, 13, 14, 0, 0)
    )

    assert result == 1

    reminder_service.get_due_supplements.assert_called_once_with(
        reminder_time=time(14, 0)
    )

    notification_service.send_supplement_reminder.assert_called_once_with(
        supplement=supplement
    )


def test_runner_returns_zero_when_no_supplements_are_due():
    runner, reminder_service, notification_service = create_runner([])

    result = runner.run(
        current_time=datetime(2026, 9, 13, 14, 0, 0)
    )

    assert result == 0

    reminder_service.get_due_supplements.assert_called_once_with(
        reminder_time=time(14, 0)
    )

    notification_service.send_supplement_reminder.assert_not_called()


def test_runner_sends_notifications_for_multiple_supplements():
    supplements = [
        SimpleNamespace(
            id=1,
            name="Creatine",
        ),
        SimpleNamespace(
            id=2,
            name="Vitamin D",
        ),
        SimpleNamespace(
            id=3,
            name="Omega 3",
        ),
    ]

    runner, reminder_service, notification_service = create_runner(
        supplements
    )

    result = runner.run(
        current_time=datetime(2026, 9, 13, 14, 0, 0)
    )

    assert result == 3

    assert notification_service.send_supplement_reminder.call_count == 3

    expected_calls = [
        call(supplement=supplements[0]),
        call(supplement=supplements[1]),
        call(supplement=supplements[2]),
    ]

    notification_service.send_supplement_reminder.assert_has_calls(
        expected_calls
    )


def test_runner_normalizes_seconds_and_microseconds():
    runner, reminder_service, notification_service = create_runner([])

    result = runner.run(
        current_time=datetime(
            2026,
            9,
            13,
            14,
            0,
            37,
            123456,
        )
    )

    assert result == 0

    reminder_service.get_due_supplements.assert_called_once_with(
        reminder_time=time(14, 0)
    )

    notification_service.send_supplement_reminder.assert_not_called()