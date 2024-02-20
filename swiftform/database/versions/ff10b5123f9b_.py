"""empty message

Revision ID: ff10b5123f9b
Revises: 25dbdab07366, 8bfe3c053bdf
Create Date: 2024-02-15 10:05:09.658280

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "ff10b5123f9b"
down_revision: Union[str, None] = ("25dbdab07366", "8bfe3c053bdf")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
