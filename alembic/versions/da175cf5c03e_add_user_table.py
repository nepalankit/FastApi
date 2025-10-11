"""add user table

Revision ID: da175cf5c03e
Revises: f140585e33ff
Create Date: 2025-10-10 22:58:01.712169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da175cf5c03e'
down_revision: Union[str, Sequence[str], None] = 'f140585e33ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('email',sa.String(),nullable=False,unique=True),
                    sa.Column('password',sa.String(),nullable=False),sa.Column('created_at',sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
