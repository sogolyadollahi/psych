from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Progress(Base):
    __tablename__ = "progress"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    weight: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    body_fat: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    chest: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    waist: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    arm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    thigh: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    progress_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="progress_records",
    )
