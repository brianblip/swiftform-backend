"""Add question table

Revision ID: 65e14b288048
Revises: 27261d7d5673
Create Date: 2024-02-06 17:59:31.583797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "65e14b288048"
down_revision: Union[str, None] = "27261d7d5673"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "question",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            sa.Enum(
                "TEXTFIELD",
                "TEXTAREA",
                "MULTIPLE_CHOICE",
                "CHECKBOX",
                "DROPDOWN",
                "ATTACHMENT",
                "SLIDER",
                "DATE",
                name="questiontype",
            ),
            nullable=False,
        ),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("section_id", sa.Integer(), nullable=False),
        sa.Column("is_required", sa.Boolean(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["form_id"],
            ["form.id"],
        ),
        sa.ForeignKeyConstraint(
            ["section_id"],
            ["section.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("question")
    # ### end Alembic commands ###
