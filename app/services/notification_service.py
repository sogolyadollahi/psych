from app.models.supplement import Supplement
from app.notifications.base import NotificationProvider


class NotificationService:

    def __init__(
        self,
        provider: NotificationProvider,
    ):
        self.provider = provider

    def send_supplement_reminder(
        self,
        supplement: Supplement,
    ) -> None:
        message = (
            f"Reminder: Time to take "
            f"{supplement.name} ({supplement.dosage})"
        )

        self.provider.send_supplement_reminder(
            supplement=supplement,
            message=message,
        )