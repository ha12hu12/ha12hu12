"""users_create revision

Revision ID: 35e2e65f9cb9
Revises: 8fa2991425a8
Create Date: 2026-07-26 08:31:43.759347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '35e2e65f9cb9'
down_revision: Union[str, Sequence[str], None] = '8fa2991425a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
            'users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                server_default=sa.text('now()'),
                                nullable=False),
                                
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
