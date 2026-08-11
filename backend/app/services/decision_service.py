"""Service keputusan & monitoring: apply pricing/restock, list decisions (API Contract bab 16).

`metrics_before` disimpan saat keputusan diterapkan; `metrics_after` dihitung dari
data aktual saat dibaca — tidak pernah menggunakan hasil prediksi.
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.errors import BusinessError, ConflictError, NotFoundError
from app.models.business import Business
from app.models.enums import (
    DecisionAppliedStatus,
    DecisionAppliedType,
    MovementType,
    RecommendationStatus,
)
from app.repositories import product_repository, recommendation_repository, transaction_repository
from app.services.catalog_service import compute_unit_hpp

_PERIOD_DAYS = 30


def _revenue_total(db: Session, business_id: int) -> float:
    start = datetime.now() - timedelta(days=_PERIOD_DAYS)
    totals = transaction_repository.totals_in_range(db, business_id, start, datetime.now())
    return totals["revenue"]


def _margin_avg(db: Session, business_id: int) -> float:
    start = datetime.now() - timedelta(days=_PERIOD_DAYS)
    cogs = transaction_repository.cogs_total_in_range(db, business_id, start, datetime.now())
    revenue = _revenue_total(db, business_id)
    return (revenue - cogs) / revenue * 100 if revenue > 0 else 0.0


def _product_stock(db: Session, business_id: int, product_id: int) -> float:
    inventory = product_repository.get_inventory_by_product(db, product_id)
    return float(inventory.current_stock) if inventory else 0.0


def _metrics(db: Session, business: Business, product_id: int | None) -> dict:
    return {
        "revenue": round(_revenue_total(db, business.id), 2),
        "margin": round(_margin_avg(db, business.id), 2),
        "stock": _product_stock(db, business.id, product_id) if product_id else 0.0,
    }


def apply_pricing(db: Session, business: Business, recommendation_id: int) -> dict:
    rec = recommendation_repository.get_pricing_recommendation(db, recommendation_id, business.id)
    if rec is None:
        raise NotFoundError("Rekomendasi tidak ditemukan.")
    if rec.status != RecommendationStatus.PENDING:
        raise ConflictError("Recommendation has already been applied.")

    product = product_repository.get_by_business(db, rec.product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    old_price = float(product.selling_price)
    new_price = float(rec.recommended_price)

    metrics_before = _metrics(db, business, product.id)
    product.selling_price = new_price
    rec.status = RecommendationStatus.ACCEPTED

    decision = recommendation_repository.create_decision(
        db,
        business_id=business.id,
        recommendation_id=rec.id,
        decision_type=DecisionAppliedType.PRICING,
        title=f"Naikkan harga {product.name}",
        summary=f"Harga disesuaikan dari Rp {old_price:,.0f} → Rp {new_price:,.0f} untuk menutup HPP dan target margin.",
        reasoning=rec.reason,
        metrics_before=metrics_before,
        status=DecisionAppliedStatus.FLAT,
        outcome_notes="Keputusan baru diterapkan; hasil akan terpantau dari data aktual berikutnya.",
    )
    db.commit()
    return {
        "product_id": product.id,
        "old_price": old_price,
        "new_price": new_price,
        "decision_id": decision.id,
        "status": "applied",
    }


def apply_restock(db: Session, business: Business, recommendation_id: int) -> dict:
    rec = recommendation_repository.get_restock_recommendation(db, recommendation_id, business.id)
    if rec is None:
        raise NotFoundError("Rekomendasi tidak ditemukan.")
    if rec.status != RecommendationStatus.PENDING:
        raise ConflictError("Recommendation has already been applied.")

    product = product_repository.get_by_business(db, rec.product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    quantity = float(rec.recommended_quantity)
    if quantity <= 0:
        raise BusinessError("Tidak ada jumlah restock yang direkomendasikan untuk produk ini.")

    inventory = product_repository.get_inventory_by_product(db, product.id)
    if inventory is None:
        inventory = product_repository.create_inventory(
            db, business_id=business.id, product_id=product.id, current_stock=0
        )
    new_stock = float(inventory.current_stock) + quantity

    metrics_before = _metrics(db, business, product.id)
    product_repository.create_movement(
        db,
        business_id=business.id,
        product_id=product.id,
        movement_type=MovementType.RESTOCK,
        quantity=quantity,
        movement_date=datetime.now(),
        reference_id=rec.id,
        note=f"Restock {product.name} sesuai rekomendasi",
    )
    product_repository.set_stock(db, inventory, new_stock)
    rec.status = RecommendationStatus.ACCEPTED

    decision = recommendation_repository.create_decision(
        db,
        business_id=business.id,
        recommendation_id=rec.id,
        decision_type=DecisionAppliedType.RESTOCK,
        title=f"Restock {product.name}",
        summary=f"Penambahan stok {quantity:,.0f} unit mengikuti forecast permintaan.",
        reasoning=rec.reason or "",
        metrics_before=metrics_before,
        status=DecisionAppliedStatus.FLAT,
        outcome_notes="Stok bertambah sesuai rekomendasi; pantau penjualan ke depan.",
    )
    db.commit()
    return {
        "product_id": product.id,
        "quantity_received": quantity,
        "new_stock": new_stock,
        "decision_id": decision.id,
        "status": "applied",
    }


def _derive_status(metrics_before: dict, metrics_after: dict) -> tuple[DecisionAppliedStatus, str]:
    revenue_growth = metrics_after["revenue"] - metrics_before["revenue"]
    margin_growth = metrics_after["margin"] - metrics_before["margin"]
    stock_growth = metrics_after["stock"] - metrics_before["stock"]
    if revenue_growth > 0 or margin_growth > 0 or stock_growth > 0:
        status = DecisionAppliedStatus.IMPROVED
        notes = "Indikator menunjukkan perbaikan setelah keputusan diterapkan."
    elif revenue_growth < 0 or margin_growth < 0 or stock_growth < 0:
        status = DecisionAppliedStatus.REGRESSED
        notes = "Indikator menurun setelah keputusan; tinjau kembali strategi dan data terkini."
    else:
        status = DecisionAppliedStatus.FLAT
        notes = "Indikator relatif stabil setelah keputusan diterapkan."
    return status, notes


def list_decisions(db: Session, business: Business) -> list[dict]:
    decisions = recommendation_repository.list_applied_decisions(db, business.id)
    result: list[dict] = []
    for decision in decisions:
        product_id = None
        if decision.type == DecisionAppliedType.RESTOCK:
            rec = recommendation_repository.get_restock_recommendation(db, decision.recommendation_id, business.id)
            product_id = rec.product_id if rec else None
        elif decision.type == DecisionAppliedType.PRICING:
            rec = recommendation_repository.get_pricing_recommendation(db, decision.recommendation_id, business.id)
            product_id = rec.product_id if rec else None

        product_name = None
        if product_id is not None:
            product = product_repository.get_by_business(db, product_id, business.id)
            product_name = product.name if product else None

        metrics_before = decision.metrics_before or {"revenue": 0, "margin": 0, "stock": 0}
        metrics_after = _metrics(db, business, product_id)
        status, notes = _derive_status(metrics_before, metrics_after)

        result.append(
            {
                "id": decision.id,
                "type": decision.type.value.lower(),
                "product_id": product_id,
                "product_name": product_name,
                "title": decision.title,
                "summary": decision.summary or "",
                "reasoning": decision.reasoning or "",
                "applied_at": decision.applied_at.isoformat(),
                "metrics_before": metrics_before,
                "metrics_after": metrics_after,
                "status": status.value.lower(),
                "outcome_notes": decision.outcome_notes or notes,
            }
        )
    return result


def get_decision(db: Session, business: Business, decision_id: int) -> dict:
    decision = recommendation_repository.get_decision(db, decision_id, business.id)
    if decision is None:
        raise NotFoundError("Keputusan tidak ditemukan.")
    for item in list_decisions(db, business):
        if item["id"] == decision.id:
            return item
    raise NotFoundError("Keputusan tidak ditemukan.")


def dismiss(db: Session, business: Business, decision_id: int) -> dict:
    decision = recommendation_repository.get_decision(db, decision_id, business.id)
    if decision is None:
        raise NotFoundError("Keputusan tidak ditemukan.")
    return {"id": decision.id, "status": "dismissed", "success": True}


def dismiss_pricing(db: Session, business: Business, recommendation_id: int) -> dict:
    rec = recommendation_repository.get_pricing_recommendation(db, recommendation_id, business.id)
    if rec is None:
        raise NotFoundError("Rekomendasi tidak ditemukan.")
    rec.status = RecommendationStatus.DISMISSED
    db.commit()
    return {"id": rec.id, "status": "dismissed"}


def dismiss_restock(db: Session, business: Business, recommendation_id: int) -> dict:
    rec = recommendation_repository.get_restock_recommendation(db, recommendation_id, business.id)
    if rec is None:
        raise NotFoundError("Rekomendasi tidak ditemukan.")
    rec.status = RecommendationStatus.DISMISSED
    db.commit()
    return {"id": rec.id, "status": "dismissed"}
