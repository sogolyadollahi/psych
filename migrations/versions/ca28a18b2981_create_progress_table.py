"""create progress table

Revision ID: ca28a18b2981
Revises: e0bb66e5fb25
Create Date: 2026-09-13 10:29:49.952316

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ca28a18b2981"
down_revision: Union[str, Sequence[str], None] = "e0bb66e5fb25"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "progress",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "weight",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "body_fat",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "chest",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "waist",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "arm",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "thigh",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "progress_date",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_progress_user_id"),
        "progress",
        ["user_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_progress_progress_date"),
        "progress",
        ["progress_date"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("progress")
