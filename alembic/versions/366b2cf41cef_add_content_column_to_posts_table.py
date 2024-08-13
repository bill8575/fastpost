"""add content column to posts table

Revision ID: 366b2cf41cef
Revises: 1ab55a300cde
Create Date: 2024-08-09 23:19:13.010507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '366b2cf41cef'
down_revision: Union[str, None] = '1ab55a300cde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
