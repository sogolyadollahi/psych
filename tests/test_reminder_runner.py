from datetime import datetime

from app.core.database import SessionLocal
from app.repositories.supplement_repository import SupplementRepository
from app.services.notification_service import NotificationService
from app.services.reminder_runner import ReminderRunner
from app.services.reminder_service import ReminderService
from app.notifications.log_provider import LogNotificationProvider


def main():
    db = SessionLocal()

    try:
        repository = SupplementRepository(db)
        reminder_service = ReminderService(repository=repository)

        notification_service = NotificationService(
            provider=LogNotificationProvider()
        )

        runner = ReminderRunner(
            reminder_service=reminder_service,
            notification_service=notification_service,
        )

        result = runner.run(
            current_time=datetime(2026, 9, 13, 14, 0, 0)
        )

        print(f">>> Notifications sent: {result}")

    finally:
        db.close()


if __name__ == "__main__":
    main()