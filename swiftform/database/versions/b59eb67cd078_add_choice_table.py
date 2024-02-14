"""Add choice table

Revision ID: b59eb67cd078
Revises: e580689eb685
Create Date: 2024-02-12 08:39:27.535644

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b59eb67cd078"
down_revision: Union[str, None] = "e580689eb685"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "choice",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["question.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("question", sa.Column("form_id", sa.Integer(), nullable=False))
    op.add_column("question", sa.Column("min", sa.Integer(), nullable=True))
    op.add_column("question", sa.Column("max", sa.Integer(), nullable=True))
    op.add_column("question", sa.Column("steps", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "question", "form", ["form_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "question", type_="foreignkey")
    op.drop_column("question", "steps")
    op.drop_column("question", "max")
    op.drop_column("question", "min")
    op.drop_column("question", "form_id")
    op.drop_table("choice")
    # ### end Alembic commands ###
