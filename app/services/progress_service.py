from datetime import date

from sqlalchemy.orm import Session

from app.models.progress import Progress
from app.models.user import User
from app.repositories.progress_repository import ProgressRepository
from app.schemas.progress import (
    ProgressAnalyticsResponse,
    ProgressCreate,
    ProgressUpdate,
)


class ProgressService:

    def __init__(self, db: Session):
        self.progress_repository = ProgressRepository(db)

    def create(
        self,
        current_user: User,
        progress_data: ProgressCreate,
    ) -> Progress:

        progress = Progress(
            user_id=current_user.id,
            weight=progress_data.weight_kg,
            body_fat=progress_data.body_fat_percentage,
            chest=progress_data.chest_cm,
            waist=progress_data.waist_cm,
            arm=progress_data.arm_cm,
            thigh=progress_data.thigh_cm,
            progress_date=progress_data.progress_date,
        )

        return self.progress_repository.create(progress)

    def get_all(
        self,
        current_user: User,
    ) -> list[Progress]:

        return self.progress_repository.get_by_user_id(
            current_user.id
        )

    def get_by_id(
        self,
        current_user: User,
        progress_id: int,
    ) -> Progress:

        progress = self.progress_repository.get_by_id(
            progress_id
        )

        if progress is None:
            raise ValueError("Progress record not found")

        if progress.user_id != current_user.id:
            raise ValueError("Progress record not found")

        return progress

    def update(
        self,
        current_user: User,
        progress_id: int,
        progress_data: ProgressUpdate,
    ) -> Progress:

        progress = self.get_by_id(
            current_user=current_user,
            progress_id=progress_id,
        )

        if progress_data.weight_kg is not None:
            progress.weight = progress_data.weight_kg

        if progress_data.body_fat_percentage is not None:
            progress.body_fat = (
                progress_data.body_fat_percentage
            )

        if progress_data.chest_cm is not None:
            progress.chest = progress_data.chest_cm

        if progress_data.waist_cm is not None:
            progress.waist = progress_data.waist_cm

        if progress_data.arm_cm is not None:
            progress.arm = progress_data.arm_cm

        if progress_data.thigh_cm is not None:
            progress.thigh = progress_data.thigh_cm

        if progress_data.progress_date is not None:
            progress.progress_date = (
                progress_data.progress_date
            )

        return self.progress_repository.update(progress)

    def delete(
        self,
        current_user: User,
        progress_id: int,
    ) -> None:

        progress = self.get_by_id(
            current_user=current_user,
            progress_id=progress_id,
        )

        self.progress_repository.delete(progress)

    def get_analytics(
        self,
        current_user: User,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> ProgressAnalyticsResponse:

        if (
            start_date is not None
            and end_date is not None
            and start_date > end_date
        ):
            raise ValueError(
                "start_date cannot be after end_date"
            )

        progress_records = (
            self.progress_repository
            .get_by_user_id_and_date_range(
                user_id=current_user.id,
                start_date=start_date,
                end_date=end_date,
            )
        )

        if not progress_records:
            raise ValueError(
                "No progress records found for the selected date range"
            )

        first_record = progress_records[0]
        last_record = progress_records[-1]

        return ProgressAnalyticsResponse(
            start_date=first_record.progress_date,
            end_date=last_record.progress_date,

            weight_change_kg=self._calculate_change(
                first_record.weight,
                last_record.weight,
            ),

            body_fat_change_percentage=self._calculate_change(
                first_record.body_fat,
                last_record.body_fat,
            ),

            chest_change_cm=self._calculate_change(
                first_record.chest,
                last_record.chest,
            ),

            waist_change_cm=self._calculate_change(
                first_record.waist,
                last_record.waist,
            ),

            arm_change_cm=self._calculate_change(
                first_record.arm,
                last_record.arm,
            ),

            thigh_change_cm=self._calculate_change(
                first_record.thigh,
                last_record.thigh,
            ),
        )

    @staticmethod
    def _calculate_change(
        first_value: float | None,
        last_value: float | None,
    ) -> float | None:

        if first_value is None or last_value is None:
            return None

        return round(
            last_value - first_value,
            2,
        )
        