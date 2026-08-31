from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.supplement import Supplement


class SupplementRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        supplement: Supplement,
    ) -> Supplement:
        self.db.add(supplement)
        self.db.commit()
        self.db.refresh(supplement)

        return supplement

    def get_by_id(
        self,
        supplement_id: int,
    ) -> Supplement | None:
        statement = select(Supplement).where(
            Supplement.id == supplement_id
        )

        return self.db.scalar(statement)

    def get_by_user_id(
        self,
        user_id: int,
    ) -> list[Supplement]:
        statement = (
            select(Supplement)
            .where(
                Supplement.user_id == user_id
            )
            .order_by(
                Supplement.reminder_time.asc(),
                Supplement.created_at.desc(),
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        supplement: Supplement,
    ) -> Supplement:
        self.db.commit()
        self.db.refresh(supplement)

        return supplement

    def delete(
        self,
        supplement: Supplement,
    ) -> None:
        self.db.delete(supplement)
        self.db.commit()