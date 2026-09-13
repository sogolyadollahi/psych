from abc import ABC, abstractmethod

from app.models.supplement import Supplement


class NotificationProvider(ABC):

    @abstractmethod
    def send_supplement_reminder(
        self,
        supplement: Supplement,
        message: str,
    ) -> None:
        raise NotImplementedError