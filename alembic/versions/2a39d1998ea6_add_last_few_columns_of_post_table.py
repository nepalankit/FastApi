"""add last few columns of post table

Revision ID: 2a39d1998ea6
Revises: 139076e9e48d
Create Date: 2025-10-11 11:19:37.563715

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a39d1998ea6'
down_revision: Union[str, Sequence[str], None] = '139076e9e48d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'),)
    op.add_column("posts",sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
