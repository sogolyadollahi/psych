from datetime import datetime

from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService


class ReminderRunner:

    def __init__(
        self,
        reminder_service: ReminderService,
        notification_service: NotificationService,
    ):
        self.reminder_service = reminder_service
        self.notification_service = notification_service

    def run(
        self,
        current_time: datetime | None = None,
    ) -> int:
        if current_time is None:
            current_time = datetime.now()

        reminder_time = current_time.replace(
            second=0,
            microsecond=0,
        ).time()

        due_supplements = self.reminder_service.get_due_supplements(
            reminder_time=reminder_time,
        )

        for supplement in due_supplements:
            self.notification_service.send_supplement_reminder(
                supplement=supplement,
            )

        return len(due_supplements)