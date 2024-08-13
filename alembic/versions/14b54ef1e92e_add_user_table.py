"""add user table

Revision ID: 14b54ef1e92e
Revises: 366b2cf41cef
Create Date: 2024-08-09 23:38:05.240191

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14b54ef1e92e'
down_revision: Union[str, None] = '366b2cf41cef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('create_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')                                                            
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
