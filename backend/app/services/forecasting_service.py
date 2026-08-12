"""Service Sales Forecasting (API Contract bab 12, AI_ML spec bab forecasting).

Metode: kombinasi Simple Average / Moving Average / Exponential Smoothing.
Dipilih berdasarkan kecukupan data (AI_ML spec bab 8, business rule 13.11):

- 0 hari terjual                       -> INSUFFICIENT (prediksi 0, confidence rendah)
- 1-6  hari terisi di jendela 14 hari  -> Simple Average (LOW confidence)
- 7-13 hari terisi                     -> Moving Average (MEDIUM confidence)
- >=14 hari terisi                     -> Exponential Smoothing (HIGH confidence)

Confidence dihitung dinamis dari volume & stabilitas data (tidak hardcode).
"""
import math
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.business import Business
from app.repositories import product_repository, transaction_repository

_LOOKBACK_DAYS = 14
_TREND_WINDOW = 4
_MOVING_WINDOW = 7
_EXP_ALPHA = 0.3


def _exponential_smoothing_forecast(series: list[float], alpha: float = _EXP_ALPHA) -> float:
    """Peramalan satu langkah ke depan dengan Exponential Smoothing."""
    if not series:
        return 0.0
    smoothed = series[0]
    for value in series[1:]:
        smoothed = alpha * value + (1 - alpha) * smoothed
    return smoothed


def _coefficient_of_variation(series: list[float]) -> float:
    """CV mengukur stabilitas/pola permintaan; dipakai untuk confidence."""
    if not series:
        return 99.0
    mean = sum(series) / len(series)
    if mean <= 0:
        return 99.0
    variance = sum((v - mean) ** 2 for v in series) / len(series)
    return math.sqrt(variance) / mean


def _normalize_model(model: str) -> str:
    return {
        "simple": "simple",
        "simple-average": "simple",
        "moving": "moving",
        "moving-average": "moving",
        "exponential": "exponential",
        "exponential-smoothing": "exponential",
        "insufficient": "insufficient",
    }.get(model, "insufficient")


def _dynamic_confidence(model: str, active_days: int, series: list[float]) -> int:
    """Confidence dinamis dari volume data + stabilitas, tanpa hardcode 76/88."""
    normalized = _normalize_model(model)
    base = {"insufficient": 20, "simple": 45, "moving": 60, "exponential": 72}[normalized]
    cv = _coefficient_of_variation(series)

    if normalized == "simple":
        bonus = max(0, min(15, active_days * 2))
    elif normalized == "moving":
        bonus = max(0, min(15, active_days * 2))
    elif normalized == "exponential":
        bonus = max(0, min(18, active_days))
    else:
        bonus = 0

    if cv < 0.4:
        stability = 6
    elif cv < 0.8:
        stability = 2
    elif cv > 1.5:
        stability = -8
    else:
        stability = 0

    return int(max(5, min(92, base + bonus + stability)))


def _forecast_for_product(db: Session, product, daily_qty: dict[datetime.date, float], today: datetime) -> dict:
    days = [(today - timedelta(days=i)).date() for i in range(_LOOKBACK_DAYS - 1, -1, -1)]
    actual_series = [float(daily_qty.get(day, 0.0)) for day in days]

    active_days = sum(1 for q in actual_series if q > 0)
    avg = sum(actual_series) / len(actual_series) if actual_series else 0.0
    recent = actual_series[-_MOVING_WINDOW:]

    if active_days == 0:
        predicted = 0.0
        model = "insufficient"
        method = "Data belum cukup (INSUFFICIENT)"
    elif active_days < 7:
        predicted = avg
        model = "simple-average"
        method = "Simple Average"
    elif active_days < _LOOKBACK_DAYS:
        predicted = sum(recent) / len(recent)
        model = "moving-average"
        method = f"Moving Average ({_MOVING_WINDOW} hari)"
    else:
        predicted = _exponential_smoothing_forecast(actual_series)
        model = "exponential-smoothing"
        method = "Exponential Smoothing"

    confidence = _dynamic_confidence(model, active_days, actual_series)
    status = "INSUFFICIENT" if active_days == 0 else "OK"

    # Tren: bandingkan separuh pertama vs kedua jendela data.
    half = _TREND_WINDOW
    recent_sum = sum(actual_series[-half:])
    prior_sum = sum(actual_series[-2 * half : -half])
    if active_days > 0 and prior_sum > 0:
        ratio = recent_sum / prior_sum
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
                "forecast": round(day_qty, 1),
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

    if active_days == 0:
        reasoning = (
            f"Belum ada riwayat penjualan untuk {product.name}. "
            "Forecast tidak dapat dihasilkan (INSUFFICIENT) hingga data transaksi tersedia. "
            "Catat transaksi lebih rutin agar estimasi dapat dibuat."
        )
    elif active_days < 7:
        reasoning = (
            f"Data penjualan {product.name} masih terbatas ({active_days} hari terisi). "
            f"Estimasi kasar {predicted_units:.0f} unit/hari dengan kepercayaan {confidence}%. "
            "Semakin rutin transaksi dicatat, semakin akurat estimasinya."
        )
    elif active_days < _LOOKBACK_DAYS:
        reasoning = (
            f"Penjualan {product.name} dalam {_LOOKBACK_DAYS} hari terakhir cukup untuk "
            f"moving average {_MOVING_WINDOW} hari (rata-rata {predicted:.1f} unit/hari), "
            f"dengan kepercayaan {confidence}%."
        )
    else:
        trend_label = {"up": "naik", "down": "menurun", "flat": "stabil"}[trend]
        reasoning = (
            f"Data penjualan {product.name} {_LOOKBACK_DAYS} hari terakhir mencukupi untuk "
            f"exponential smoothing (bobot lebih besar pada data terbaru), tren {trend_label}. "
            f"Prediksi {predicted_units:.0f} unit untuk periode berikutnya dengan kepercayaan {confidence}%."
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
        "status": status,
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


def refresh(db: Session, business: Business) -> dict:
    """Menghitung ulang forecast seluruh produk dan mempersist hasilnya ke `forecast_results`."""
    from app.repositories import recommendation_repository

    today = datetime.now()
    start = today - timedelta(days=_LOOKBACK_DAYS)
    daily_qty = transaction_repository.daily_qty_per_product(db, business.id, start, today)
    products = product_repository.list_by_business(db, business.id)

    stored = 0
    for product in products:
        result = _forecast_for_product(db, product, daily_qty.get(product.id, {}), today)
        if result["status"] == "INSUFFICIENT":
            continue
        recommendation_repository.create_forecast(
            db,
            business_id=business.id,
            product_id=product.id,
            forecast_date=result["next_period"],
            predicted_quantity=result["predicted_units"],
            model_version=result["model"],
        )
        stored += 1
    db.commit()
    return {"refresh_at": today.isoformat(), "products_updated": stored}


def forecast_product(db: Session, business: Business, product_id: int) -> dict:
    from app.core.errors import NotFoundError

    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    today = datetime.now()
    start = today - timedelta(days=_LOOKBACK_DAYS)
    daily_qty = transaction_repository.daily_qty_per_product(db, business.id, start, today)
    return _forecast_for_product(db, product, daily_qty.get(product_id, {}), today)
