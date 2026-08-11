"""add foreign key constraints

Revision ID: b0c48013c53e
Revises: edb68b91a3a6
Create Date: 2026-08-11

Menambahkan database-level FOREIGN KEY constraints pada kolom-kolom FK yang
sebelumnya hanya berupa BIGINT ber-index. Aturan relasi & cardinality mengikuti
DATA_DICTIONARY_AND_DATA_MODEL_DATARA.md (Section 20).

Catatan:
- `decisions_applied.recommendation_id` bersifat polimorfik (bisa menunjuk
  pricing atau restock recommendation), sehingga sengaja tanpa FK constraint.
- Tidak ada perubahan kolom/tipe; migration ini additive dan non-destruktif.
"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b0c48013c53e"
down_revision: Union[str, Sequence[str], None] = "edb68b91a3a6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# (constraint_name, table, referent_table, local_column)
FOREIGN_KEYS = [
    ("fk_businesses_user_id_users", "businesses", "users", "user_id"),
    ("fk_business_configurations_business_id_businesses", "business_configurations", "businesses", "business_id"),
    ("fk_business_targets_business_id_businesses", "business_targets", "businesses", "business_id"),
    ("fk_products_business_id_businesses", "products", "businesses", "business_id"),
    ("fk_product_costs_product_id_products", "product_costs", "products", "product_id"),
    ("fk_sales_transactions_business_id_businesses", "sales_transactions", "businesses", "business_id"),
    ("fk_sales_transaction_items_transaction_id_sales_transactions", "sales_transaction_items", "sales_transactions", "transaction_id"),
    ("fk_sales_transaction_items_product_id_products", "sales_transaction_items", "products", "product_id"),
    ("fk_inventory_items_business_id_businesses", "inventory_items", "businesses", "business_id"),
    ("fk_inventory_items_product_id_products", "inventory_items", "products", "product_id"),
    ("fk_inventory_movements_business_id_businesses", "inventory_movements", "businesses", "business_id"),
    ("fk_inventory_movements_product_id_products", "inventory_movements", "products", "product_id"),
    ("fk_operating_expenses_business_id_businesses", "operating_expenses", "businesses", "business_id"),
    ("fk_forecast_results_business_id_businesses", "forecast_results", "businesses", "business_id"),
    ("fk_forecast_results_product_id_products", "forecast_results", "products", "product_id"),
    ("fk_restock_recommendations_business_id_businesses", "restock_recommendations", "businesses", "business_id"),
    ("fk_restock_recommendations_product_id_products", "restock_recommendations", "products", "product_id"),
    ("fk_pricing_recommendations_business_id_businesses", "pricing_recommendations", "businesses", "business_id"),
    ("fk_pricing_recommendations_product_id_products", "pricing_recommendations", "products", "product_id"),
    ("fk_business_health_assessments_business_id_businesses", "business_health_assessments", "businesses", "business_id"),
    ("fk_growth_recommendations_business_id_businesses", "growth_recommendations", "businesses", "business_id"),
    ("fk_decisions_applied_business_id_businesses", "decisions_applied", "businesses", "business_id"),
    ("fk_ai_conversations_business_id_businesses", "ai_conversations", "businesses", "business_id"),
    ("fk_ai_messages_conversation_id_ai_conversations", "ai_messages", "ai_conversations", "conversation_id"),
]


def upgrade() -> None:
    """Add foreign key constraints."""
    for name, table, referent, column in FOREIGN_KEYS:
        op.create_foreign_key(name, table, referent, [column], ["id"])


def downgrade() -> None:
    """Drop foreign key constraints (reverse order)."""
    for name, table, referent, column in reversed(FOREIGN_KEYS):
        op.drop_constraint(name, table, type_="foreignkey")