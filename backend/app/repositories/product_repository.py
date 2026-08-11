"""Repository akses data untuk Product, ProductCost, dan Inventory.

Domain yang dipegang: produk, komponen HPP, stok, dan riwayat pergerakan stok.
"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.enums import MovementType
from app.models.inventory_item import InventoryItem
from app.models.inventory_movement import InventoryMovement
from app.models.product import Product
from app.models.product_cost import ProductCost


def list_by_business(db: Session, business_id: int) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.business_id == business_id)
        .order_by(Product.id.asc())
        .all()
    )


def get_by_business(db: Session, product_id: int, business_id: int) -> Product | None:
    return (
        db.query(Product)
        .filter(Product.id == product_id, Product.business_id == business_id)
        .first()
    )


def create(
    db: Session,
    *,
    business_id: int,
    name: str,
    sku: str | None,
    selling_price: float,
    unit: str,
    low_stock_threshold: float | None,
) -> Product:
    product = Product(
        business_id=business_id,
        name=name,
        sku=sku,
        selling_price=selling_price,
        unit=unit,
        low_stock_threshold=low_stock_threshold,
    )
    db.add(product)
    db.flush()
    db.refresh(product)  # muat server_default (created_at/updated_at)
    return product


# ---------------------------------------------------------------------------
# ProductCost / HPP
# ---------------------------------------------------------------------------


def list_costs(db: Session, product_id: int) -> list[ProductCost]:
    return (
        db.query(ProductCost)
        .filter(ProductCost.product_id == product_id)
        .order_by(ProductCost.id.asc())
        .all()
    )


def get_cost_by_type(db: Session, product_id: int, cost_type) -> ProductCost | None:
    return (
        db.query(ProductCost)
        .filter(ProductCost.product_id == product_id, ProductCost.cost_type == cost_type)
        .first()
    )


def upsert_cost(
    db: Session,
    *,
    product_id: int,
    cost_type,
    name: str,
    cost_per_unit: float,
) -> ProductCost:
    cost = get_cost_by_type(db, product_id, cost_type)
    if cost is None:
        cost = ProductCost(product_id=product_id, cost_type=cost_type, name=name, cost_per_unit=cost_per_unit)
        db.add(cost)
    else:
        cost.name = name
        cost.cost_per_unit = cost_per_unit
    db.flush()
    return cost


# ---------------------------------------------------------------------------
# InventoryItem / stock
# ---------------------------------------------------------------------------


def get_inventory_by_product(db: Session, product_id: int) -> InventoryItem | None:
    return (
        db.query(InventoryItem)
        .filter(InventoryItem.product_id == product_id)
        .first()
    )


def get_inventories_by_business(db: Session, business_id: int) -> list[InventoryItem]:
    return (
        db.query(InventoryItem)
        .filter(InventoryItem.business_id == business_id)
        .order_by(InventoryItem.product_id.asc())
        .all()
    )


def create_inventory(db: Session, *, business_id: int, product_id: int, current_stock: float = 0) -> InventoryItem:
    item = InventoryItem(business_id=business_id, product_id=product_id, current_stock=current_stock)
    db.add(item)
    db.flush()
    return item


def set_stock(db: Session, inventory_item: InventoryItem, current_stock: float) -> None:
    inventory_item.current_stock = current_stock
    db.flush()


# ---------------------------------------------------------------------------
# InventoryMovement / riwayat stok
# ---------------------------------------------------------------------------


def create_movement(
    db: Session,
    *,
    business_id: int,
    product_id: int,
    movement_type: MovementType,
    quantity: float,
    movement_date: datetime,
    reference_id: int | None = None,
    note: str | None = None,
) -> InventoryMovement:
    movement = InventoryMovement(
        business_id=business_id,
        product_id=product_id,
        movement_type=movement_type,
        quantity=quantity,
        movement_date=movement_date,
        reference_id=reference_id,
        note=note,
    )
    db.add(movement)
    db.flush()
    db.refresh(movement)  # muat server_default (created_at)
    return movement


def list_movements(db: Session, business_id: int, *, limit: int = 100, product_id: int | None = None) -> list[InventoryMovement]:
    query = db.query(InventoryMovement).filter(InventoryMovement.business_id == business_id)
    if product_id is not None:
        query = query.filter(InventoryMovement.product_id == product_id)
    return (
        query.order_by(InventoryMovement.movement_date.desc(), InventoryMovement.id.desc())
        .limit(limit)
        .all()
    )
