"""add content column to post table

Revision ID: f140585e33ff
Revises: 7b67b73679f7
Create Date: 2025-10-10 22:49:29.772675

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f140585e33ff'
down_revision: Union[str, Sequence[str], None] = '7b67b73679f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
