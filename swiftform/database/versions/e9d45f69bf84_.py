"""empty message

Revision ID: e9d45f69bf84
Revises: 65e14b288048, c0b95cd57cc3
Create Date: 2024-02-08 15:26:53.708778

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "e9d45f69bf84"
down_revision: Union[str, None] = ("65e14b288048", "c0b95cd57cc3")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
