"""Service Growth Map / Roadmap Pertumbuhan (API Contract bab 17).

Tahapan dihitung dari indikator bisnis aktual (transaksi, produk terpantau,
keputusan diterapkan, omzet) — rule-based, tanpa data palsu.
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.business import Business
from app.repositories import product_repository, recommendation_repository, transaction_repository
from app.services.catalog_service import compute_unit_hpp

_TARGET_TRANSACTIONS_WEEK = 20
_TARGET_DECISIONS = 5
_TARGET_MONTHLY_REVENUE = 12_000_000


def growth_stages(db: Session, business: Business) -> dict:
    today = datetime.now()
    start_7 = today - timedelta(days=7)
    start_30 = today - timedelta(days=30)

    totals_7 = transaction_repository.totals_in_range(db, business.id, start_7, today)
    totals_30 = transaction_repository.totals_in_range(db, business.id, start_30, today)

    products = product_repository.list_by_business(db, business.id)
    total_products = len(products)
    products_tracked = sum(1 for p in products if compute_unit_hpp(db, p.id) > 0)
    decisions_applied = recommendation_repository.count_applied_decisions(db, business.id)

    stages = [
        {
            "id": 1,
            "label": "Catat & Konsisten",
            "description": "Pencatatan transaksi dan biaya berjalan rutin setiap hari.",
            "metric_1": "Transaksi/minggu",
            "metric_1_value": totals_7["tx_count"],
            "metric_1_target": _TARGET_TRANSACTIONS_WEEK,
            "next_step": "Lanjutkan rutinitas pencatatan harian.",
        },
        {
            "id": 2,
            "label": "Pahami Profitabilitas",
            "description": "Semua produk memiliki HPP dan margin yang terhitung.",
            "metric_1": "Produk terpantau",
            "metric_1_value": products_tracked,
            "metric_1_target": total_products or 1,
            "next_step": "Lengkapi komponen biaya untuk produk yang belum ber-HPP.",
        },
        {
            "id": 3,
            "label": "Keputusan Berbasis Data",
            "description": "Menerapkan rekomendasi pricing & restock secara rutin.",
            "metric_1": "Keputusan diterapkan",
            "metric_1_value": decisions_applied,
            "metric_1_target": _TARGET_DECISIONS,
            "next_step": "Terapkan rekomendasi lain dari Smart Pricing/Restock.",
        },
        {
            "id": 4,
            "label": "Perluas Menuju Pertumbuhan",
            "description": "Evaluasi perkembangan indikator dan siap ekspansi liniteman/menu.",
            "metric_1": "Omzet bulanan",
            "metric_1_value": round(totals_30["revenue"], 2),
            "metric_1_target": _TARGET_MONTHLY_REVENUE,
            "next_step": "Capai target omzet bulanan sebelum menambah outlet.",
        },
    ]

    current_assigned = False
    for stage in stages:
        if stage["metric_1_value"] >= stage["metric_1_target"]:
            stage["status"] = "done"
        elif not current_assigned:
            stage["status"] = "current"
            current_assigned = True
        else:
            stage["status"] = "upcoming"

    return {
        "current_stage": next((s["label"] for s in stages if s["status"] == "current"), None),
        "stages": stages,
    }
