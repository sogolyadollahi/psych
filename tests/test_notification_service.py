from datetime import time
from unittest.mock import Mock

from app.models.supplement import Supplement
from app.services.notification_service import NotificationService


def test_send_supplement_reminder():
    provider = Mock()

    service = NotificationService(
        provider=provider,
    )

    supplement = Supplement(
        id=1,
        user_id=10,
        name="Creatine",
        dosage="5g",
        reminder_time=time(9, 0),
        is_active=True,
    )

    service.send_supplement_reminder(
        supplement=supplement,
    )

    provider.send_supplement_reminder.assert_called_once_with(
        supplement=supplement,
        message="Reminder: Time to take Creatine (5g)",
    )