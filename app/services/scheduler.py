import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.database import SessionLocal
from app.notifications.log_provider import LogNotificationProvider
from app.repositories.supplement_repository import SupplementRepository
from app.services.notification_service import NotificationService
from app.services.reminder_runner import ReminderRunner
from app.services.reminder_service import ReminderService


logger = logging.getLogger(__name__)


class AppScheduler:

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def run_reminders(self) -> None:
        print(">>> Reminder job started")

        db = SessionLocal()
        print(">>> Database session created")

        try:
            repository = SupplementRepository(db)
            print(">>> Repository created")

            reminder_service = ReminderService(
                repository=repository,
            )
            print(">>> Reminder service created")

            notification_service = NotificationService(
                provider=LogNotificationProvider(),
            )
            print(">>> Notification service created")

            runner = ReminderRunner(
                reminder_service=reminder_service,
                notification_service=notification_service,
            )
            print(">>> Reminder runner created")

            print(">>> Running reminder runner")

            result = runner.run()

            print(
                f">>> Reminder job completed | notifications={result}"
            )

        except Exception as exc:
            print(f">>> Reminder job failed: {exc}")
            raise

        finally:
            db.close()
            print(">>> Database session closed")

    def start(self) -> None:
        self.scheduler.add_job(
            self.run_reminders,
            trigger="interval",
            minutes=1,
            id="supplement_reminders",
            replace_existing=True,
        )

        self.scheduler.start()

        logger.info("Reminder scheduler started")

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Reminder scheduler stopped")