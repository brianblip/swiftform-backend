"""empty message

Revision ID: a8f4623245de
Revises: 0d3611d2ed9a, c89c0a4c7214
Create Date: 2024-02-08 11:18:09.194854

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "a8f4623245de"
down_revision: Union[str, None] = ("0d3611d2ed9a", "c89c0a4c7214")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
