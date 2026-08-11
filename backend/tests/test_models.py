"""Test struktur/relasi database models (tanpa memerlukan MySQL).

Memvalidasi requirements TASK 02:
- Foreign key integrity (setiap FK mengarah ke tabel/kolom yang benar).
- Business isolation structure (semua tabel domain bisnis terkunci ke `businesses`).
- Unique constraints.
- Uang tidak memakai floating point (DECIMAL/Numeric).
- Relationship integrity (mapper dapat dikonfigurasi tanpa error).
"""
from sqlalchemy import Numeric
from sqlalchemy.orm import configure_mappers

from app.db.base import Base
from app.db import base_models  # noqa: F401  (registrasi seluruh model)

# Tabel yang menjadi child langsung dari `businesses` dan wajib punya
# `business_id` FK -> businesses.id (isolasi business ownership langsung).
# `product_costs` dan `sales_transaction_items` child-of-child (isolasi via
# products / sales_transactions), sehingga tidak memiliki business_id.
DIRECT_BUSINESS_CHILD_TABLES = {
    name
    for name in Base.metadata.tables
    if name
    not in {
        "users",
        "businesses",
        "product_costs",
        "sales_transaction_items",
        "ai_messages",
        "alembic_version",
    }
}


def test_mappers_configure() -> None:
    """Relasi antara model valid (back_populates pasangan konsisten)."""
    configure_mappers()


def test_all_business_tables_isolated_to_businesses() -> None:
    for table_name in DIRECT_BUSINESS_CHILD_TABLES:
        table = Base.metadata.tables[table_name]
        column = table.columns.get("business_id")
        assert column is not None, f"{table_name} tidak punya business_id"
        fk_refs = {fk.target_fullname for fk in column.foreign_keys}
        assert fk_refs == {"businesses.id"}, f"{table_name}.business_id FK -> {fk_refs}"


def test_child_of_child_tables_isolated_via_parent() -> None:
    """product_costs & sales_transaction_items terisolasi melalui parent-nya."""
    product_costs = Base.metadata.tables["product_costs"]
    assert "business_id" not in product_costs.columns
    assert {fk.target_fullname for fk in product_costs.columns["product_id"].foreign_keys} == {
        "products.id"
    }

    items = Base.metadata.tables["sales_transaction_items"]
    assert "business_id" not in items.columns
    item_fks = {
        fk.target_fullname
        for fk in items.columns["transaction_id"].foreign_keys | items.columns["product_id"].foreign_keys
    }
    assert item_fks == {"sales_transactions.id", "products.id"}


def test_key_foreign_keys() -> None:
    def fk_targets(table: str, column: str) -> set[str]:
        col = Base.metadata.tables[table].columns[column]
        return {fk.target_fullname for fk in col.foreign_keys}

    assert fk_targets("businesses", "user_id") == {"users.id"}
    assert fk_targets("products", "business_id") == {"businesses.id"}
    assert fk_targets("product_costs", "product_id") == {"products.id"}
    assert fk_targets("sales_transaction_items", "transaction_id") == {"sales_transactions.id"}
    assert fk_targets("sales_transaction_items", "product_id") == {"products.id"}
    assert fk_targets("inventory_items", "product_id") == {"products.id"}
    assert fk_targets("ai_messages", "conversation_id") == {"ai_conversations.id"}


def test_polymorphic_recommendation_id_has_no_fk() -> None:
    col = Base.metadata.tables["decisions_applied"].columns["recommendation_id"]
    assert len(col.foreign_keys) == 0


def test_unique_constraints() -> None:
    uniques = {
        table: {col.name for col in Base.metadata.tables[table].columns if col.unique}
        for table in Base.metadata.tables
    }
    assert "email" in uniques["users"]
    assert "user_id" in uniques["businesses"]
    assert "business_id" in uniques["business_configurations"]
    assert "product_id" in uniques["inventory_items"]
    assert "reference_number" in uniques["sales_transactions"]


def test_money_columns_use_numeric_not_float() -> None:
    money_columns = {
        "products": ["selling_price"],
        "product_costs": ["cost_per_unit"],
        "sales_transactions": ["total_amount"],
        "sales_transaction_items": ["unit_price", "subtotal", "unit_hpp"],
        "operating_expenses": ["amount"],
        "business_targets": ["target_value"],
        "pricing_recommendations": ["current_price", "current_hpp", "recommended_price", "estimated_margin"],
        "restock_recommendations": ["recommended_quantity"],
        "inventory_items": ["current_stock"],
        "inventory_movements": ["quantity"],
    }
    for table, columns in money_columns.items():
        for col_name in columns:
            col_type = Base.metadata.tables[table].columns[col_name].type
            assert isinstance(col_type, Numeric), (
                f"{table}.{col_name} harus DECIMAL/Numeric, bukan {type(col_type).__name__}"
            )


def test_business_id_columns_are_indexed() -> None:
    """business_id pada tabel child langsung memiliki index (kunci filtered query)."""
    for table_name in DIRECT_BUSINESS_CHILD_TABLES:
        table = Base.metadata.tables[table_name]
        column = table.columns.get("business_id")
        if column is None:
            continue
        indexed = set()
        for index in table.indexes:
            indexed.update(index.columns.keys())
        assert "business_id" in indexed, f"{table_name}.business_id tidak ber-index"


def test_schema_tables_match_data_dictionary_mvp() -> None:
    mvp = {
        "users",
        "businesses",
        "business_configurations",
        "business_targets",
        "products",
        "product_costs",
        "sales_transactions",
        "sales_transaction_items",
        "inventory_items",
        "inventory_movements",
        "operating_expenses",
        "forecast_results",
        "restock_recommendations",
        "pricing_recommendations",
        "business_health_assessments",
        "growth_recommendations",
        "ai_conversations",
        "ai_messages",
    }
    actual = set(Base.metadata.tables)
    assert mvp <= actual, f"Tabel MVP hilang: {sorted(mvp - actual)}"
    extras = actual - mvp
    assert extras == {"decisions_applied"}, (
        f"Tabel tambahan di luar keputusan: {sorted(extras)}. "
        "'decisions_applied' sudah dibenarkan (API Contract /decisions + frontend DecisionRecord)."
    )