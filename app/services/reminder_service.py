from datetime import time

from app.models.supplement import Supplement
from app.repositories.supplement_repository import SupplementRepository


class ReminderService:

    def __init__(
        self,
        repository: SupplementRepository,
    ):
        self.repository = repository

    def get_due_supplements(
        self,
        reminder_time: time,
    ) -> list[Supplement]:

        return self.repository.get_active_by_reminder_time(
            reminder_time=reminder_time,
        )