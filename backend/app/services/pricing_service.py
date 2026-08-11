"""Service Smart Pricing (API Contract bab 13).

Rekomendasi = HPP ÷ (1 − target margin), dibulatkan ke kelipatan Rp 500.
Rekomendasi tidak mengubah harga; perubahan hanya lewat POST /pricing/apply.
"""
import math

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.business import Business
from app.models.enums import RecommendationStatus
from app.repositories import product_repository, recommendation_repository
from app.services.catalog_service import compute_unit_hpp

_ROUNDING = 500


def _round_price(value: float) -> float:
    return math.ceil(value / _ROUNDING) * _ROUNDING


def build_recommendation(db: Session, product, target_margin: float) -> dict:
    hpp = compute_unit_hpp(db, product.id)
    current_price = float(product.selling_price)
    actual_margin = (current_price - hpp) / current_price * 100 if current_price > 0 else 0.0

    if hpp <= 0:
        recommended = current_price
        reason = f"HPP untuk {product.name} belum lengkap (isi komponen biaya di Product Cost). Harga tidak dapat direkomendasikan."
        estimated_margin = actual_margin
        reason_code = "incomplete_hpp"
    else:
        cost_based = hpp / (1 - target_margin / 100)
        recommended = _round_price(cost_based)
        estimated_margin = (recommended - hpp) / recommended * 100 if recommended > 0 else 0.0
        need_increase = recommended > current_price
        if need_increase:
            reason = (
                f"HPP Rp {hpp:,.0f} membuat margin aktual {actual_margin:.0f}% di bawah target {target_margin:.0f}%. "
                f"Naikkan harga ke Rp {recommended:,.0f} untuk mencapai margin ~{target_margin:.0f}%."
            )
            reason_code = "margin_below_target"
        else:
            reason = (
                f"Harga saat ini sudah menghasilkan margin {actual_margin:.0f}% (target {target_margin:.0f}%). "
                "Tidak perlu perubahan harga."
            )
            reason_code = "already_healthy"

    return {
        "id": 0,
        "product_id": product.id,
        "name": product.name,
        "sku": product.sku or "",
        "current_price": current_price,
        "recommended_price": recommended,
        "hpp": hpp,
        "target_margin_percent": target_margin,
        "actual_margin_percent": round(actual_margin, 2),
        "estimated_margin": round(estimated_margin, 2),
        "reasoning": reason,
        "reason_code": reason_code,
    }


def _persist(db: Session, business: Business, built: dict) -> int:
    from app.models.pricing_recommendation import PricingRecommendation

    existing = (
        db.query(PricingRecommendation)
        .filter(
            PricingRecommendation.business_id == business.id,
            PricingRecommendation.product_id == built["product_id"],
            PricingRecommendation.status == RecommendationStatus.PENDING,
        )
        .first()
    )
    if existing is None:
        rec = recommendation_repository.create_pricing_recommendation(
            db,
            business_id=business.id,
            product_id=built["product_id"],
            current_price=built["current_price"],
            current_hpp=built["hpp"],
            recommended_price=built["recommended_price"],
            estimated_margin=built["estimated_margin"],
            reason_code=built["reason_code"],
            reason=built["reasoning"],
        )
        return rec.id
    existing.current_price = built["current_price"]
    existing.current_hpp = built["hpp"]
    existing.recommended_price = built["recommended_price"]
    existing.estimated_margin = built["estimated_margin"]
    existing.reason_code = built["reason_code"]
    existing.reason = built["reasoning"]
    db.flush()
    return existing.id


def recommendations(db: Session, business: Business, target_margin: float = 30) -> list[dict]:
    products = [p for p in product_repository.list_by_business(db, business.id) if p.is_active]
    result: list[dict] = []
    for product in products:
        built = build_recommendation(db, product, target_margin)
        built["id"] = _persist(db, business, built)
        result.append(built)
    db.commit()
    return result


def generate(db: Session, business: Business, product_id: int, target_margin: float) -> dict:
    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    built = build_recommendation(db, product, target_margin)
    built["id"] = _persist(db, business, built)
    db.commit()
    return built
