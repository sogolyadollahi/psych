from fastapi import Depends

from app.api.v1.supplement_deps import get_supplement_repository
from app.notifications.log_provider import LogNotificationProvider
from app.repositories.supplement_repository import SupplementRepository
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService


def get_reminder_service(
    repository: SupplementRepository = Depends(
        get_supplement_repository
    ),
) -> ReminderService:
    return ReminderService(
        repository=repository,
    )


def get_notification_service() -> NotificationService:
    provider = LogNotificationProvider()

    return NotificationService(
        provider=provider,
    )