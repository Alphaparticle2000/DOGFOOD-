from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1b7c2d9e4a10"

down_revision: Union[str, Sequence[str], None] = "0ec25862acc1"

branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
        "rubrics",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "event_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "track_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "name",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "criteria_weights",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),

        sa.ForeignKeyConstraint(
            ["event_id"],
            ["events.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["track_id"],
            ["tracks.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint(
            "event_id",
            "track_id",
            "name",
            name="uq_rubric_event_track_name",
        ),
    )

    op.create_index(
        "ix_rubrics_id",
        "rubrics",
        ["id"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_scores_submission_judge",
        "scores",
        ["submission_id", "judge_id"],
    )


def downgrade() -> None:

    op.drop_constraint(
        "uq_scores_submission_judge",
        "scores",
        type_="unique",
    )

    op.drop_index(
        "ix_rubrics_id",
        table_name="rubrics",
    )

    op.drop_table("rubrics")