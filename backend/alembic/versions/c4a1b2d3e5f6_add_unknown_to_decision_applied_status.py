"""add UNKNOWN to decision applied status

Revision ID: c4a1b2d3e5f6
Revises: 70b0ef316b99
Create Date: 2026-08-12 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'c4a1b2d3e5f6'
down_revision: Union[str, Sequence[str], None] = '70b0ef316b99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "ALTER TABLE decisions_applied "
        "MODIFY COLUMN status ENUM('IMPROVED','FLAT','REGRESSED','UNKNOWN') NOT NULL"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "ALTER TABLE decisions_applied "
        "MODIFY COLUMN status ENUM('IMPROVED','FLAT','REGRESSED') NOT NULL"
    )