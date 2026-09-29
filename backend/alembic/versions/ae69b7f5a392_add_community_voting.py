"""add community voting

Revision ID: ae69b7f5a392
Revises: 1b7c2d9e4a10
Create Date: 2026-09-29 21:39:41.705699
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "ae69b7f5a392"
down_revision: Union[str, Sequence[str], None] = "1b7c2d9e4a10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "votes",
        sa.Column("ip_address", sa.String(length=45), nullable=True),
    )

    op.add_column(
        "votes",
        sa.Column("user_agent", sa.String(length=512), nullable=True),
    )

    op.create_index(
        op.f("ix_votes_submission_id"),
        "votes",
        ["submission_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_votes_user_id"),
        "votes",
        ["user_id"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_vote_submission_user",
        "votes",
        ["submission_id", "user_id"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_vote_submission_user",
        "votes",
        type_="unique",
    )

    op.drop_index(
        op.f("ix_votes_user_id"),
        table_name="votes",
    )

    op.drop_index(
        op.f("ix_votes_submission_id"),
        table_name="votes",
    )

    op.drop_column("votes", "user_agent")
    op.drop_column("votes", "ip_address")