"""Service Inventory: list stok, buat movement non-sale, riwayat pergerakan."""
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.errors import BusinessError, NotFoundError
from app.models.business import Business
from app.models.enums import MovementType
from app.repositories import product_repository
from app.schemas.inventory import InventoryMovementCreateRequest

_MOVEMENT_MAP = {
    "received": MovementType.RESTOCK,
    "waste": MovementType.WASTE,
    "adjustment": MovementType.ADJUSTMENT,
}


def list_inventory(db: Session, business: Business) -> list[dict]:
    items = product_repository.get_inventories_by_business(db, business.id)
    result: list[dict] = []
    for item in items:
        product = item.product
        result.append(
            {
                "product_id": item.product_id,
                "product_name": product.name,
                "current_stock": float(item.current_stock),
                "stock_unit": product.unit,
                "low_stock_threshold": float(product.low_stock_threshold) if product.low_stock_threshold is not None else 0,
            }
        )
    return result


def _compute_delta(movement_type: str, quantity: float) -> float:
    if movement_type == "received":
        if quantity <= 0:
            raise BusinessError("Quantity untuk received harus lebih dari 0.")
        return quantity
    if movement_type == "waste":
        if quantity <= 0:
            raise BusinessError("Quantity untuk waste harus lebih dari 0.")
        return -quantity
    # adjustment: nilai bertanda dari client.
    return quantity


def create_movement(db: Session, business: Business, payload: InventoryMovementCreateRequest) -> dict:
    product = product_repository.get_by_business(db, payload.product_id, business.id)
    if product is None:
        raise NotFoundError("Produk tidak ditemukan.")
    movement_type = _MOVEMENT_MAP.get(payload.movement_type)
    if movement_type is None:
        raise BusinessError("Jenis movement tidak didukung.")
    if movement_type == MovementType.RESTOCK and payload.quantity <= 0:
        raise BusinessError("Quantity untuk received harus lebih dari 0.")
    if movement_type == MovementType.WASTE and payload.quantity <= 0:
        raise BusinessError("Quantity untuk waste harus lebih dari 0.")

    inventory = product_repository.get_inventory_by_product(db, product.id)
    if inventory is None:
        inventory = product_repository.create_inventory(
            db, business_id=business.id, product_id=product.id, current_stock=0
        )

    movement_date = payload.movement_date or datetime.now()
    delta = _compute_delta(payload.movement_type, payload.quantity)
    current = float(inventory.current_stock)
    new_stock = max(0.0, current + delta)

    movement = product_repository.create_movement(
        db,
        business_id=business.id,
        product_id=product.id,
        movement_type=movement_type,
        quantity=delta,
        movement_date=movement_date,
        note=payload.note,
        stock_after=new_stock,
    )
    product_repository.set_stock(db, inventory, new_stock)
    db.commit()

    return {
        "id": movement.id,
        "product_id": product.id,
        "product_name": product.name,
        "movement_type": movement.movement_type.value,
        "quantity": delta,
        "current_stock": new_stock,
        "note": payload.note,
        "created_at": movement.created_at.isoformat(),
    }


def list_movements(db: Session, business: Business, *, limit: int = 100, product_id: int | None = None) -> list[dict]:
    movements = product_repository.list_movements(db, business.id, limit=limit, product_id=product_id)
    result: list[dict] = []
    for m in movements:
        result.append(
            {
                "id": m.id,
                "product_id": m.product_id,
                "product_name": m.product.name if m.product else None,
                "movement_type": m.movement_type.value,
                "quantity": float(m.quantity),
                "stock_after": float(m.stock_after) if m.stock_after is not None else None,
                "note": m.note,
                "created_at": m.created_at.isoformat(),
            }
        )
    return result
