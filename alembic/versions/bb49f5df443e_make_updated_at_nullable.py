"""make updated_at nullable

Revision ID: bb49f5df443e
Revises: 54fddcb2ca18
Create Date: 2026-08-17 23:30:12.091814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bb49f5df443e'
down_revision: Union[str, Sequence[str], None] = '54fddcb2ca18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               server_default=None,
               existing_server_default=sa.text('now()'))


def downgrade() -> None:
    """Downgrade schema."""
    # Rows created after the upgrade may hold NULL, which would break NOT NULL.
    op.execute("UPDATE users SET updated_at = created_at WHERE updated_at IS NULL")
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               server_default=sa.text('now()'))
