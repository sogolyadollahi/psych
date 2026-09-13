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

    def start(self) -> None:
        if self.scheduler.running:
            return

        self.scheduler.add_job(
            self.run_reminders,
            trigger="interval",
            minutes=1,
            id="supplement_reminders",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )

        self.scheduler.start()

        logger.info("Reminder scheduler started")

    def run_reminders(self) -> None:
        db = SessionLocal()

        try:
            repository = SupplementRepository(db)

            reminder_service = ReminderService(
                repository=repository
            )

            notification_service = NotificationService(
                provider=LogNotificationProvider()
            )

            runner = ReminderRunner(
                reminder_service=reminder_service,
                notification_service=notification_service,
            )

            result = runner.run()

            logger.info(
                "Reminder job completed | notifications=%s",
                result,
            )

        except Exception:
            logger.exception("Reminder job failed")

        finally:
            db.close()

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Reminder scheduler stopped")