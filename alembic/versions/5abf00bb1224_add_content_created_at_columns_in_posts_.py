"""add (content, created at) columns in posts-- revision

Revision ID: 5abf00bb1224
Revises: 35e2e65f9cb9
Create Date: 2026-07-26 13:22:23.857154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from  sqlalchemy.sql.expression import text

# revision identifiers, used by Alembic.
revision: str = '5abf00bb1224'
down_revision: Union[str, Sequence[str], None] = '35e2e65f9cb9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default = text('now()')))
    op.add_column("posts", sa.Column("content", sa.VARCHAR(500), nullable =  False))
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable = False))
    op.create_foreign_key("posts-users_fk", source_table="posts", referent_table="users", local_cols=["owner_id"], remote_cols=["id"], ondelete="CASCADE")
    
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(constraint_name="posts-users_fk", table_name="posts")
    op.drop_column(table_name="posts", column_name="created_at")
    op.drop_column(table_name="posts", column_name="content")
    op.drop_column(table_name="posts", column_name="owner_id")
    pass
