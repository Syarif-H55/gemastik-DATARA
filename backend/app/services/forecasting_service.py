"""Service Sales Forecasting (API Contract bab 12, AI_ML spec bab forecasting).

Metode: kombinasi Simple Average / Moving Average / Simple Estimate.
Dipilih berdasarkan kecukupan data. Tidak mengarang data historis.
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.business import Business
from app.repositories import product_repository, transaction_repository

_LOOKBACK_DAYS = 14
_TREND_WINDOW = 4


def _forecast_for_product(db: Session, product, daily_qty: dict[datetime.date, float], today: datetime) -> dict:
    days = [(today - timedelta(days=i)).date() for i in range(_LOOKBACK_DAYS - 1, -1, -1)]
    actual_series = [float(daily_qty.get(day, 0.0)) for day in days]

    active_days = sum(1 for q in actual_series if q > 0)
    data_sufficient = active_days >= 7
    avg = sum(actual_series) / len(actual_series) if actual_series else 0.0
    recent_avg = sum(actual_series[-7:]) / 7 if len(actual_series) >= 7 else avg

    if data_sufficient:
        predicted = recent_avg
        method = "Moving Average (7 hari)"
        model = "moving-average"
        confidence = 88 if active_days >= 10 else 76
    elif active_days > 0:
        predicted = avg
        method = "Simple Average"
        model = "simple-average"
        confidence = 62
    else:
        predicted = 0.0
        method = "Simple Estimate (data terbatas)"
        model = "simple-estimate"
        confidence = 40

    half = _TREND_WINDOW
    recent = sum(actual_series[-half:])
    prior = sum(actual_series[-2 * half : -half])
    if data_sufficient and prior > 0:
        ratio = recent / prior
        if ratio > 1.2:
            trend = "up"
        elif ratio < 0.8:
            trend = "down"
        else:
            trend = "flat"
    else:
        trend = "flat"

    next_period = (today + timedelta(days=1)).date()
    predicted_units = round(predicted, 1)

    # Points: 7 hari aktual terakhir + titik prediksi periode berikutnya.
    points: list[dict] = []
    for i in range(7, 0, -1):
        day = today - timedelta(days=i)
        day_qty = float(daily_qty.get(day.date(), 0.0))
        points.append(
            {
                "period": day.date().isoformat(),
                "actual": day_qty,
                "forecast": round(sum(actual_series[: _LOOKBACK_DAYS - i]) / max(1, _LOOKBACK_DAYS - i), 1),
                "lower": 0,
                "upper": 0,
            }
        )
    points.append(
        {
            "period": next_period.isoformat(),
            "actual": 0,
            "forecast": predicted_units,
            "lower": round(max(0.0, predicted_units - 3), 1),
            "upper": round(predicted_units + 3, 1),
        }
    )

    trend_label = {"up": "naik", "down": "menurun", "flat": "stabil"}[trend]
    if data_sufficient:
        reasoning = (
            f"Riwayat penjualan {product.name} {_LOOKBACK_DAYS} hari terakhir menunjukkan "
            f"tren {trend_label} (rata-rata {recent_avg:.1f} unit/hari). "
            f"Prediksi {predicted_units:.0f} unit untuk periode berikutnya dengan kepercayaan {confidence}%."
        )
    elif active_days > 0:
        reasoning = (
            f"Data penjualan {product.name} masih terbatas ({active_days} hari). "
            f"Estimasi kasar {predicted_units:.0f} unit/hari dengan kepercayaan {confidence}%. "
            "Catat transaksi lebih rutin agar prediksi makin akurat."
        )
    else:
        reasoning = (
            f"Belum ada riwayat penjualan untuk {product.name}. "
            "Forecast tidak dibuat hingga data transaksi tersedia."
        )

    return {
        "product_id": product.id,
        "name": product.name,
        "sku": product.sku or "",
        "model": model,
        "method": method,
        "next_period": next_period.isoformat(),
        "predicted_units": predicted_units,
        "confidence": confidence,
        "trend": trend,
        "points": points,
        "reasoning": reasoning,
    }


def forecast_all(db: Session, business: Business) -> list[dict]:
    today = datetime.now()
    start = today - timedelta(days=_LOOKBACK_DAYS)
    daily_qty = transaction_repository.daily_qty_per_product(db, business.id, start, today)
    products = product_repository.list_by_business(db, business.id)
    return [_forecast_for_product(db, p, daily_qty.get(p.id, {}), today) for p in products]


def forecast_product(db: Session, business: Business, product_id: int) -> dict:
    from app.core.errors import NotFoundError

    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    today = datetime.now()
    start = today - timedelta(days=_LOOKBACK_DAYS)
    daily_qty = transaction_repository.daily_qty_per_product(db, business.id, start, today)
    return _forecast_for_product(db, product, daily_qty.get(product_id, {}), today)
