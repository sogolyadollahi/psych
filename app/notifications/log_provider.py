import logging

from app.models.supplement import Supplement
from app.notifications.base import NotificationProvider


logger = logging.getLogger(__name__)


class LogNotificationProvider(NotificationProvider):

    def send_supplement_reminder(
        self,
        supplement: Supplement,
        message: str,
    ) -> None:
        logger.info(
            "Supplement reminder | user_id=%s supplement_id=%s message=%s",
            supplement.user_id,
            supplement.id,
            message,
        )