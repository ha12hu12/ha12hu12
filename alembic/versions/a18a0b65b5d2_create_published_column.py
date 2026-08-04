"""create published column

Revision ID: a18a0b65b5d2
Revises: 5abf00bb1224
Create Date: 2026-07-26 14:20:40.795022

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a18a0b65b5d2'
down_revision: Union[str, Sequence[str], None] = '5abf00bb1224'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',
                  sa.Column('published',
                  sa.Boolean(), nullable=False, server_default='TRUE'))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'published')
    pass
