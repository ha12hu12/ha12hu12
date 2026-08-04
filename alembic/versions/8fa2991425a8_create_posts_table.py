"""create_posts_table

Revision ID: 8fa2991425a8
Revises: 
Create Date: 2026-07-26 08:10:50.751787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8fa2991425a8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("posts",  sa.Column('id', sa.Integer(), 
                                            nullable = False, primary_key = True), 
                        sa.Column("title",sa.VARCHAR(100), nullable = False))


def downgrade() -> None:
    """Downgrade schema."""
   
