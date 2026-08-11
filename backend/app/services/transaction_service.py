"""Service pembuatan transaksi penjualan (atomic: transaksi + item + stok).

Mengikuti API Contract bab 20.1 — seluruh langkah berhasil atau seluruhnya
di-rollback: validasi produk, validasi stok, buat transaksi, snapshot HPP,
buat movement sale, kurangi current stock, lalu commit.
"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.errors import BusinessError, NotFoundError
from app.models.business import Business
from app.models.enums import MovementType
from app.repositories import product_repository, transaction_repository
from app.schemas.transaction import TransactionCreateRequest
from app.services.catalog_service import compute_unit_hpp


def create_sale(db: Session, business: Business, payload: TransactionCreateRequest) -> dict:
    transaction_date = payload.transaction_date or datetime.now()
    if len(payload.items) == 0:
        raise BusinessError("Transaksi minimal harus memiliki satu item.")

    # 1. Validasi produk & stok sebelum membuat apa pun.
    validated: list[tuple[object, float, float, float]] = []  # (product, qty, unit_price, unit_hpp)
    for item in payload.items:
        product = product_repository.get_by_business(db, item.product_id, business.id)
        if product is None:
            raise NotFoundError(f"Produk id={item.product_id} tidak ditemukan.")
        inventory = product_repository.get_inventory_by_product(db, product.id)
        current_stock = float(inventory.current_stock) if inventory else 0.0
        if current_stock < item.quantity:
            raise BusinessError(f"Stok \"{product.name}\" tidak mencukupi (tersisa {current_stock}).")
        unit_price = float(item.selling_price) if item.selling_price is not None else float(product.selling_price)
        validated.append((product, item.quantity, unit_price, compute_unit_hpp(db, product.id)))

    subtotal = round(sum(qty * unit_price for _, qty, unit_price, _ in validated), 2)
    total_amount = round(max(0.0, subtotal - payload.discount), 2)

    # 2. Buat transaksi + item.
    transaction = transaction_repository.create(
        db,
        business_id=business.id,
        reference_number="",
        customer_name=payload.customer_name,
        transaction_date=transaction_date,
        subtotal=subtotal,
        discount=payload.discount,
        total_amount=total_amount,
    )
    transaction.reference_number = f"TRX-{transaction_date.strftime('%Y%m%d')}-{transaction.id:04d}"

    items_out: list[dict] = []
    for product, qty, unit_price, unit_hpp in validated:
        transaction_repository.create_item(
            db,
            transaction_id=transaction.id,
            product_id=product.id,
            quantity=qty,
            unit_price=unit_price,
            subtotal=round(qty * unit_price, 2),
            unit_hpp=unit_hpp,
        )
        # 3. Movement sale + kurangi stok (atomic).
        inventory = product_repository.get_inventory_by_product(db, product.id)
        new_stock = max(0.0, float(inventory.current_stock) - qty)
        product_repository.create_movement(
            db,
            business_id=business.id,
            product_id=product.id,
            movement_type=MovementType.SALE,
            quantity=-qty,
            movement_date=transaction_date,
            reference_id=transaction.id,
            note=f"Penjualan {transaction.reference_number}",
        )
        product_repository.set_stock(db, inventory, new_stock)
        items_out.append(
            {
                "product_id": product.id,
                "quantity": qty,
                "unit_price": unit_price,
                "unit_hpp": unit_hpp,
            }
        )

    db.commit()
    return {
        "id": transaction.id,
        "reference_number": transaction.reference_number,
        "customer_name": transaction.customer_name,
        "transaction_date": transaction_date.isoformat(),
        "subtotal": subtotal,
        "discount": payload.discount,
        "total": total_amount,
        "items": items_out,
        "created_at": transaction.created_at.isoformat(),
    }


def list_transactions(db: Session, business: Business, *, limit: int = 50) -> list[dict]:
    transactions = transaction_repository.list_by_business(db, business.id, limit=limit)
    result: list[dict] = []
    for tx in transactions:
        items = [
            {
                "product_id": item.product_id,
                "quantity": float(item.quantity),
                "unit_price": float(item.unit_price),
                "unit_hpp": float(item.unit_hpp),
            }
            for item in tx.items
        ]
        result.append(
            {
                "id": tx.id,
                "reference_number": tx.reference_number or "",
                "customer_name": tx.customer_name,
                "transaction_date": tx.transaction_date.isoformat(),
                "subtotal": float(tx.subtotal or 0),
                "discount": float(tx.discount or 0),
                "total": float(tx.total_amount),
                "items": items,
                "created_at": tx.created_at.isoformat(),
            }
        )
    return result
