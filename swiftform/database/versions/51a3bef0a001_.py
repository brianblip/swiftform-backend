"""empty message

Revision ID: 51a3bef0a001
Revises: 50d8b3b9c2ce, 8bfe3c053bdf
Create Date: 2024-02-13 21:49:19.151814

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "51a3bef0a001"
down_revision: Union[str, None] = ("50d8b3b9c2ce", "8bfe3c053bdf")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
