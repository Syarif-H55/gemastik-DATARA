"""Service Smart Restock (API Contract bab 14).

Menggunakan: Forecast Demand + Current Stock + Safety Days (dikonfigurasi user,
default 3). Rekomendasi tidak menambah stok; perubahan hanya lewat POST /restock/apply.
"""
import math

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.business import Business
from app.models.enums import RecommendationStatus
from app.models.restock_recommendation import RestockRecommendation
from app.repositories import product_repository, recommendation_repository
from app.services import forecasting_service
from app.services.catalog_service import get_current_stock


def build_recommendation(
    db: Session,
    business: Business,
    product,
    safety_days: float,
    lead_time: float,
) -> dict:
    current_stock = get_current_stock(db, product.id)
    low_stock_threshold = float(product.low_stock_threshold) if product.low_stock_threshold is not None else 0.0

    forecasts = {f["product_id"]: f for f in forecasting_service.forecast_all(db, business)}
    forecast = forecasts.get(product.id)
    predicted_daily = forecast["predicted_units"] if forecast else 0.0

    if predicted_daily > 0:
        days_of_supply = current_stock / predicted_daily
        suggested = max(0.0, predicted_daily * (lead_time + safety_days) - current_stock)
        if current_stock <= low_stock_threshold:
            urgency = "critical"
        elif days_of_supply <= lead_time + safety_days:
            urgency = "low"
        else:
            urgency = "healthy"
        basis = f"Forecast {predicted_daily:.1f} unit/hari"
    else:
        days_of_supply = 999.0
        suggested = 0.0
        urgency = "healthy" if current_stock > low_stock_threshold else "critical"
        basis = "Belum ada data forecast"

    if urgency == "critical":
        reason = (
            f"Stok tersisa {current_stock:,.0f} (di bawah ambang {low_stock_threshold:,.0f}). "
            f"{basis}, diperkirakan habis dalam ~{days_of_supply:.0f} hari. Segera restock {suggested:,.0f} unit."
        )
        reason_code = "stock_below_threshold"
    elif urgency == "low":
        reason = (
            f"Stok {current_stock:,.0f} masih cukup tapi mendekati ambang. "
            f"{basis}, restock {suggested:,.0f} unit agar tidak kehabisan."
        )
        reason_code = "supply_near_threshold"
    else:
        reason = (
            f"Stok {current_stock:,.0f} sehat dengan {basis}, cukup untuk ~{days_of_supply:.0f} hari. "
            "Belum perlu restock."
        )
        reason_code = "healthy"

    return {
        "id": 0,
        "product_id": product.id,
        "name": product.name,
        "sku": product.sku or "",
        "current_stock": current_stock,
        "low_stock_threshold": low_stock_threshold,
        "days_of_supply": round(days_of_supply, 1),
        "suggested_quantity": math.ceil(suggested),
        "urgency": urgency,
        "reasoning": reason,
        "reason_code": reason_code,
        "predicted_daily": predicted_daily,
    }


def _persist(db: Session, business: Business, built: dict, safety_days: float) -> int:
    existing = (
        db.query(RestockRecommendation)
        .filter(
            RestockRecommendation.business_id == business.id,
            RestockRecommendation.product_id == built["product_id"],
            RestockRecommendation.status == RecommendationStatus.PENDING,
        )
        .first()
    )
    if existing is None:
        rec = recommendation_repository.create_restock_recommendation(
            db,
            business_id=business.id,
            product_id=built["product_id"],
            current_stock=built["current_stock"],
            forecasted_demand=built["predicted_daily"],
            safety_days=safety_days,
            recommended_quantity=built["suggested_quantity"],
            reason_code=built["reason_code"],
            reason=built["reasoning"],
        )
        return rec.id
    existing.current_stock = built["current_stock"]
    existing.forecasted_demand = built["predicted_daily"]
    existing.recommended_quantity = built["suggested_quantity"]
    existing.reason_code = built["reason_code"]
    existing.reason = built["reasoning"]
    db.flush()
    return existing.id


def recommendations(db: Session, business: Business, safety_days: float, lead_time: float) -> list[dict]:
    products = [p for p in product_repository.list_by_business(db, business.id) if p.is_active]
    result: list[dict] = []
    for product in products:
        built = build_recommendation(db, business, product, safety_days, lead_time)
        built["id"] = _persist(db, business, built, safety_days)
        result.append(built)
    db.commit()
    return result


def generate(db: Session, business: Business, product_id: int, safety_days: float, lead_time: float) -> dict:
    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    built = build_recommendation(db, business, product, safety_days, lead_time)
    built["id"] = _persist(db, business, built, safety_days)
    db.commit()
    return built
