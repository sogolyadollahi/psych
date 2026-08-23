from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class MealItem(Base):
    __tablename__ = "meal_items"

    id: Mapped[int] = mapped_column(primary_key=True)

    meal_id: Mapped[int] = mapped_column(
        ForeignKey("meals.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    unit: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    calories: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    protein: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    carbs: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    fat: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    source: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    source_food_id: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    meal: Mapped["Meal"] = relationship(
        back_populates="items",
    )