"""initial tables

Revision ID: 1708874613
Revises: 
Create Date: 2024-02-25 23:23:33.669922

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1708874613'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ('default',)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('token_blocklist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('jti', sa.String(length=36), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_blocklist_jti'), 'token_blocklist', ['jti'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('email', sa.Text(), nullable=False),
    sa.Column('password', sa.Text(), nullable=False),
    sa.Column('avatar_url', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('form',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipient_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['recipient_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['form.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('section',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('form_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['form_id'], ['form.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('TEXTFIELD', 'TEXTAREA', 'MULTIPLE_CHOICE', 'CHECKBOX', 'DROPDOWN', 'ATTACHMENT', 'DATE', name='questiontype'), nullable=False),
    sa.Column('prompt', sa.Text(), nullable=False),
    sa.Column('section_id', sa.Integer(), nullable=False),
    sa.Column('is_required', sa.Boolean(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['section_id'], ['section.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('response_id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['response_id'], ['response.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('choice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('choice')
    op.drop_table('answer')
    op.drop_table('question')
    op.drop_table('section')
    op.drop_table('response')
    op.drop_table('notification')
    op.drop_table('form')
    op.drop_table('user')
    op.drop_index(op.f('ix_token_blocklist_jti'), table_name='token_blocklist')
    op.drop_table('token_blocklist')
    # ### end Alembic commands ###
