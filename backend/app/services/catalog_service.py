"""Service untuk Product, Cost/HPP, dan Profitability (API Contract bab 6-7).

Backend adalah source of truth: HPP dihitung dari komponen biaya, stok
diambil dari InventoryItem, dan profitabilitas dihitung dari transaksi aktual.
"""
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.business import Business
from app.models.enums import CostType
from app.repositories import product_repository
from app.schemas.product import ProductCostsUpdateRequest, ProductCreateRequest, ProductUpdateRequest

_COST_TYPES = {
    "raw_material": CostType.RAW_MATERIAL,
    "packaging": CostType.PACKAGING,
    "direct_labor": CostType.DIRECT_LABOR,
    "allocated_overhead": CostType.PRODUCTION_OVERHEAD,
}

_COST_NAMES = {
    CostType.RAW_MATERIAL: "Bahan Baku",
    CostType.PACKAGING: "Kemasan",
    CostType.DIRECT_LABOR: "Tenaga Kerja Langsung",
    CostType.PRODUCTION_OVERHEAD: "Overhead Produksi Alokasi",
}


def compute_unit_hpp(db: Session, product_id: int) -> float:
    """HPP/unit = Bahan Baku + Kemasan + TKL + Overhead alokasi."""
    costs = product_repository.list_costs(db, product_id)
    return round(sum(float(c.cost_per_unit) for c in costs), 2)


def get_current_stock(db: Session, product_id: int) -> float:
    inventory = product_repository.get_inventory_by_product(db, product_id)
    return float(inventory.current_stock) if inventory else 0.0


def product_payload(db: Session, product) -> dict:
    return {
        "id": product.id,
        "name": product.name,
        "sku": product.sku or "",
        "selling_price": float(product.selling_price),
        "hpp": compute_unit_hpp(db, product.id),
        "stock": get_current_stock(db, product.id),
        "low_stock_threshold": float(product.low_stock_threshold) if product.low_stock_threshold is not None else 0,
        "unit": product.unit,
        "is_active": product.is_active,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    }


def list_products(db: Session, business: Business) -> list[dict]:
    products = product_repository.list_by_business(db, business.id)
    return [product_payload(db, p) for p in products]


def get_product(db: Session, business: Business, product_id: int) -> dict:
    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    return product_payload(db, product)


def create_product(db: Session, business: Business, payload: ProductCreateRequest) -> dict:
    product = product_repository.create(
        db,
        business_id=business.id,
        name=payload.name,
        sku=payload.sku,
        selling_price=payload.selling_price,
        unit=payload.unit,
        low_stock_threshold=payload.low_stock_threshold,
    )
    product_repository.create_inventory(
        db,
        business_id=business.id,
        product_id=product.id,
        current_stock=payload.current_stock,
    )
    if payload.hpp is not None and payload.hpp > 0:
        # Quick-add dari halaman transaksi: HPP tunggal dipetakan ke komponen
        # Bahan Baku agar unit_hpp langsung tersedia untuk Smart Pricing.
        product_repository.upsert_cost(
            db,
            product_id=product.id,
            cost_type=CostType.RAW_MATERIAL,
            name=_COST_NAMES[CostType.RAW_MATERIAL],
            cost_per_unit=payload.hpp,
        )
    db.commit()
    return product_payload(db, product)


def update_product(db: Session, business: Business, product_id: int, payload: ProductUpdateRequest) -> dict:
    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    if payload.name is not None:
        product.name = payload.name
    if payload.sku is not None:
        product.sku = payload.sku
    if payload.selling_price is not None:
        product.selling_price = payload.selling_price
    if payload.unit is not None:
        product.unit = payload.unit
    if payload.low_stock_threshold is not None:
        product.low_stock_threshold = payload.low_stock_threshold
    if payload.is_active is not None:
        product.is_active = payload.is_active
    db.commit()
    return product_payload(db, product)


def deactivate_product(db: Session, business: Business, product_id: int) -> dict:
    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    product.is_active = False
    db.commit()
    return product_payload(db, product)


def costs_payload(db: Session, product_id: int) -> dict:
    costs = product_repository.list_costs(db, product_id)
    by_type = {c.cost_type: float(c.cost_per_unit) for c in costs}
    return {
        "raw_material": by_type.get(CostType.RAW_MATERIAL, 0.0),
        "packaging": by_type.get(CostType.PACKAGING, 0.0),
        "direct_labor": by_type.get(CostType.DIRECT_LABOR, 0.0),
        "allocated_overhead": by_type.get(CostType.PRODUCTION_OVERHEAD, 0.0),
        "unit_hpp": compute_unit_hpp(db, product_id),
    }


def get_costs(db: Session, business: Business, product_id: int) -> dict:
    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    return costs_payload(db, product_id)


def update_costs(db: Session, business: Business, product_id: int, payload: ProductCostsUpdateRequest) -> dict:
    product = product_repository.get_by_business(db, product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    values = {
        "raw_material": payload.raw_material,
        "packaging": payload.packaging,
        "direct_labor": payload.direct_labor,
        "allocated_overhead": payload.allocated_overhead,
    }
    for key, amount in values.items():
        product_repository.upsert_cost(
            db,
            product_id=product_id,
            cost_type=_COST_TYPES[key],
            name=_COST_NAMES[_COST_TYPES[key]],
            cost_per_unit=amount,
        )
    db.commit()
    return costs_payload(db, product_id)


def get_profitability(db: Session, business: Business) -> list[dict]:
    """Profitabilitas per produk berdasarkan transaksi aktual (tanpa data palsu)."""
    from datetime import datetime, timedelta

    from app.repositories import transaction_repository

    today = datetime.now()
    start = today - timedelta(days=30)
    products = product_repository.list_by_business(db, business.id)
    sold_qty = transaction_repository.sales_qty_per_product(db, business.id, start, today)
    result: list[dict] = []
    for product in products:
        qty_sold = sold_qty.get(product.id, 0.0)
        hpp = compute_unit_hpp(db, product.id)
        selling_price = float(product.selling_price)
        unit_profit = selling_price - hpp
        margin = (unit_profit / selling_price * 100) if selling_price > 0 else 0.0
        total_revenue = qty_sold * selling_price
        total_cost = qty_sold * hpp
        total_profit = total_revenue - total_cost
        result.append(
            {
                "product_id": product.id,
                "name": product.name,
                "sku": product.sku or "",
                "selling_price": selling_price,
                "hpp": hpp,
                "unit_profit": round(unit_profit, 2),
                "margin_percent": round(margin, 2),
                "qty_sold": qty_sold,
                "total_revenue": round(total_revenue, 2),
                "total_cost": round(total_cost, 2),
                "total_profit": round(total_profit, 2),
            }
        )
    return result
