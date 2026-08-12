"""Service Finance, Dashboard, dan Business Health (API Contract bab 10-11, 15).

Semua angka dihitung dari data aktual transaksi & biaya. Tidak ada nilai palsu.
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.operating_expense import OperatingExpense
from app.repositories import transaction_repository

_CATEGORY_LABELS = {"MIN": "Minuman", "FOOD": "Makanan", "SNK": "Camilan"}

_PERIOD_DAYS_SUMMARY = 30
_PERIOD_DAYS_TREND = 7


def _operating_expense_total(db: Session, business_id: int, start: datetime, end: datetime) -> float:
    from sqlalchemy import func

    value = (
        db.query(func.coalesce(func.sum(OperatingExpense.amount), 0))
        .filter(
            OperatingExpense.business_id == business_id,
            OperatingExpense.expense_date >= start.date(),
            OperatingExpense.expense_date <= end.date(),
        )
        .scalar()
    )
    return float(value)


def finance_summary(db: Session, business: Business) -> dict:
    today = datetime.now()
    start = today - timedelta(days=_PERIOD_DAYS_SUMMARY)

    totals = transaction_repository.totals_in_range(db, business.id, start, today)
    cogs = transaction_repository.cogs_total_in_range(db, business.id, start, today)
    operating_expense = _operating_expense_total(db, business.id, start, today)

    revenue = totals["revenue"]
    gross_profit = round(revenue - cogs, 2)
    gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0.0
    net_profit = round(gross_profit - operating_expense, 2)

    return {
        "revenue": round(revenue, 2),
        "cogs": round(cogs, 2),
        "gross_profit": gross_profit,
        "gross_margin": round(gross_margin, 2),
        "operating_expense": round(operating_expense, 2),
        "net_profit": net_profit,
    }


def _health_score(db: Session, business: Business, today: datetime) -> tuple[float, int]:
    start_30 = today - timedelta(days=_PERIOD_DAYS_SUMMARY)
    totals = transaction_repository.totals_in_range(db, business.id, start_30, today)
    cogs = transaction_repository.cogs_total_in_range(db, business.id, start_30, today)
    revenue = totals["revenue"]
    margin = (revenue - cogs) / revenue * 100 if revenue > 0 else 0.0
    tx_count = totals["tx_count"]

    products_sold = len(transaction_repository.sales_qty_per_product(db, business.id, start_30, today))

    # Skor komposit 0-100: margin + aktivitas transaksi + keterjualan produk.
    margin_component = max(0.0, min(100.0, margin))
    activity_component = min(100.0, tx_count * 10)
    sell_through_component = min(100.0, products_sold * 12)
    score = round(0.5 * margin_component + 0.3 * activity_component + 0.2 * sell_through_component, 2)
    return score, tx_count


def _health_label(score: float) -> str:
    if score >= 75:
        return "Sehat"
    if score >= 50:
        return "Perlu Perhatian"
    return "Berisiko"


def _health_status(score: float) -> str:
    if score >= 75:
        return "SEHAT"
    if score >= 50:
        return "PERLU_PERHATIAN"
    return "BERISIKO"


def business_health(db: Session, business: Business) -> dict:
    today = datetime.now()
    start_30 = today - timedelta(days=_PERIOD_DAYS_SUMMARY)
    totals = transaction_repository.totals_in_range(db, business.id, start_30, today)

    # Business Rules 13.12: jangan paksa klasifikasi jika data belum cukup.
    if totals["tx_count"] == 0:
        return {
            "status": "INSUFFICIENT_DATA",
            "score": 0.0,
            "label": "Data belum cukup",
            "metrics": {
                "gross_margin": 0.0,
                "net_margin": 0.0,
                "operating_expense": 0.0,
            },
        }

    score, _ = _health_score(db, business, today)
    summary = finance_summary(db, business)
    return {
        "status": _health_status(score),
        "score": score,
        "label": _health_label(score),
        "metrics": {
            "gross_margin": summary["gross_margin"],
            "net_margin": round(summary["net_profit"] / summary["revenue"] * 100, 2) if summary["revenue"] > 0 else 0.0,
            "operating_expense": summary["operating_expense"],
        },
    }


def dashboard(db: Session, business: Business) -> dict:
    today = datetime.now()
    start_30 = today - timedelta(days=_PERIOD_DAYS_SUMMARY)
    start_7 = today - timedelta(days=_PERIOD_DAYS_TREND)

    totals = transaction_repository.totals_in_range(db, business.id, start_30, today)
    cogs = transaction_repository.cogs_total_in_range(db, business.id, start_30, today)
    sold_qty = transaction_repository.sales_qty_per_product(db, business.id, start_30, today)

    revenue = totals["revenue"]
    total_profit = round(revenue - cogs, 2)
    avg_margin = (total_profit / revenue * 100) if revenue > 0 else 0.0

    score, _ = _health_score(db, business, today)

    if totals["tx_count"] == 0:
        business_health_block = {
            "score": 0.0,
            "label": "Data belum cukup",
            "status": "INSUFFICIENT_DATA",
        }
    else:
        business_health_block = {
            "score": score,
            "label": _health_label(score),
            "status": _health_status(score),
        }

    # Tren 7 hari terakhir (per hari).
    revenue_by_day = transaction_repository.revenue_by_day(db, business.id, start_7, today)
    cogs_by_day = transaction_repository.cogs_by_day(db, business.id, start_7, today)
    revenue_trend: list[dict] = []
    for i in range(_PERIOD_DAYS_TREND, -1, -1):
        day = (today - timedelta(days=i)).date()
        day_revenue = revenue_by_day.get(day, {}).get("revenue", 0.0)
        day_cogs = cogs_by_day.get(day, 0.0)
        revenue_trend.append(
            {
                "date": day.isoformat(),
                "revenue": day_revenue,
                "profit": round(day_revenue - day_cogs, 2),
            }
        )

    # Kontribusi kategori berdasarkan SKU.
    cat_revenue = transaction_repository.revenue_by_category(db, business.id, start_30, today)
    category_breakdown = [
        {"name": _CATEGORY_LABELS.get(cat, "Lainnya"), "value": amount}
        for cat, amount in sorted(cat_revenue.items(), key=lambda kv: kv[1], reverse=True)
    ]
    if not category_breakdown:
        category_breakdown = [{"name": "Belum ada data", "value": 0}]

    return {
        "total_revenue": round(revenue, 2),
        "total_profit": total_profit,
        "total_cogs": round(cogs, 2),
        "avg_margin_percent": round(avg_margin, 2),
        "transactions_count": totals["tx_count"],
        "products_sold": len(sold_qty),
        "business_health": business_health_block,
        "revenue_trend": revenue_trend,
        "category_breakdown": category_breakdown,
    }
