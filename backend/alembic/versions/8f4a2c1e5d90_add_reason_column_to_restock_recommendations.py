"""add reason column to restock_recommendations

Revision ID: 8f4a2c1e5d90
Revises: b0c48013c53e
Create Date: 2026-08-11

Menambahkan kolom `reason` (TEXT, nullable) pada `restock_recommendations`
agar penjelasan rekomendasi tersimpan (simetris dengan
`pricing_recommendations.reason`) dan dipakai oleh Decision Monitoring
(`decision_service.apply_restock`).

Non-destruktif: hanya menambah kolom nullable.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8f4a2c1e5d90"
down_revision: Union[str, Sequence[str], None] = "b0c48013c53e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("restock_recommendations", sa.Column("reason", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("restock_recommendations", "reason")
