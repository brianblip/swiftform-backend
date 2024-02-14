"""empty message

Revision ID: c0b95cd57cc3
Revises: 27261d7d5673, c89c0a4c7214
Create Date: 2024-02-08 09:58:58.724019

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "c0b95cd57cc3"
down_revision: Union[str, None] = ("27261d7d5673", "c89c0a4c7214")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
