"""empty message

Revision ID: f9c9fe66cba3
Revises: a8f4623245de, e9d45f69bf84
Create Date: 2024-02-12 10:52:05.514990

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "f9c9fe66cba3"
down_revision: Union[str, None] = ("a8f4623245de", "e9d45f69bf84")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
