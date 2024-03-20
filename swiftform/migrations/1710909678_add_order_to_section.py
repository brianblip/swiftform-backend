"""add order to section

Revision ID: 1710909678
Revises: 1708874613
Create Date: 2024-03-20 12:41:18.364350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1710909678"
down_revision: Union[str, None] = "1708874613"
branch_labels: Union[str, Sequence[str], None] = ()
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("section", sa.Column("order", sa.Integer(), nullable=True))

    # Assuming you want to initialize all current rows with a default 'order' value, for example, 0
    op.execute('UPDATE section SET "order" = 0 WHERE "order" IS NULL')

    # Now alter the 'order' column to be non-nullable
    op.alter_column("section", "order", nullable=False)


def downgrade() -> None:
    op.drop_column("section", "order")
