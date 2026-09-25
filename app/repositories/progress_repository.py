from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.progress import Progress


class ProgressRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        progress: Progress,
    ) -> Progress:
        self.db.add(progress)
        self.db.flush()
        self.db.refresh(progress)

        return progress

    def get_by_id(
        self,
        progress_id: int,
    ) -> Progress | None:
        statement = select(Progress).where(
            Progress.id == progress_id
        )

        return self.db.scalar(statement)

    def get_by_user_id(
        self,
        user_id: int,
    ) -> list[Progress]:
        statement = (
            select(Progress)
            .where(
                Progress.user_id == user_id
            )
            .order_by(
                Progress.progress_date.desc()
            )
        )

        return list(
            self.db.scalars(statement).all()
        )

    def get_by_user_id_and_date_range(
        self,
        user_id: int,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Progress]:
        statement = select(Progress).where(
            Progress.user_id == user_id
        )

        if start_date is not None:
            statement = statement.where(
                Progress.progress_date >= start_date
            )

        if end_date is not None:
            statement = statement.where(
                Progress.progress_date <= end_date
            )

        statement = statement.order_by(
            Progress.progress_date.asc()
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(
        self,
        progress: Progress,
    ) -> Progress:
        self.db.flush()
        self.db.refresh(progress)

        return progress

    def delete(
        self,
        progress: Progress,
    ) -> None:
        self.db.delete(progress)