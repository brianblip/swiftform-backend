"""empty message

Revision ID: 50d8b3b9c2ce
Revises: 25dbdab07366, b59eb67cd078
Create Date: 2024-02-13 21:27:02.581163

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "50d8b3b9c2ce"
down_revision: Union[str, None] = ("25dbdab07366", "b59eb67cd078")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
