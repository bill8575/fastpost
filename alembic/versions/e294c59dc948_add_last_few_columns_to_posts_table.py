"""add last few columns to posts table

Revision ID: e294c59dc948
Revises: 6fa773426e84
Create Date: 2024-08-10 23:18:48.842876

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e294c59dc948'
down_revision: Union[str, None] = '6fa773426e84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
