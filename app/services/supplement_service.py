from datetime import datetime, timezone, time

from app.models.supplement import Supplement
from app.repositories.supplement_repository import SupplementRepository


class SupplementService:

    def __init__(
        self,
        repository: SupplementRepository,
    ):
        self.repository = repository

    # =====================================================
    # Create
    # =====================================================

    def create_supplement(
        self,
        user_id: int,
        name: str,
        dosage: str,
        reminder_time: time,
        notes: str | None = None,
    ) -> Supplement:

        now = datetime.now(timezone.utc)

        supplement = Supplement(
            user_id=user_id,
            name=name,
            dosage=dosage,
            reminder_time=reminder_time,
            notes=notes,
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        return self.repository.create(supplement)

    # =====================================================
    # Get All User Supplements
    # =====================================================

    def get_user_supplements(
        self,
        user_id: int,
    ) -> list[Supplement]:

        supplements = self.repository.get_by_user_id(
            user_id
        )

        return supplements

    # =====================================================
    # Get Single Supplement
    # =====================================================

    def get_supplement(
        self,
        supplement_id: int,
        user_id: int,
    ) -> Supplement | None:

        supplement = self.repository.get_by_id(
            supplement_id=supplement_id
        )

        if supplement is None:
            return None

        if supplement.user_id != user_id:
            return None

        return supplement

    # =====================================================
    # Update
    # =====================================================

    def update_supplement(
        self,
        supplement: Supplement,
        name: str | None = None,
        dosage: str | None = None,
        reminder_time: time | None = None,
        notes: str | None = None,
        is_active: bool | None = None,
    ) -> Supplement:

        if name is not None:
            supplement.name = name

        if dosage is not None:
            supplement.dosage = dosage

        if reminder_time is not None:
            supplement.reminder_time = reminder_time

        if notes is not None:
            supplement.notes = notes

        if is_active is not None:
            supplement.is_active = is_active

        supplement.updated_at = datetime.now(timezone.utc)

        return self.repository.update(supplement)

    # =====================================================
    # Delete
    # =====================================================

    def delete_supplement(
        self,
        supplement: Supplement,
    ) -> None:

        self.repository.delete(supplement)