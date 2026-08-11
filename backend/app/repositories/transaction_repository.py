"""Repository akses data untuk SalesTransaction & SalesTransactionItem."""
from datetime import date, datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.enums import TransactionStatus
from app.models.product import Product
from app.models.sales_transaction import SalesTransaction, SalesTransactionItem


def create(
    db: Session,
    *,
    business_id: int,
    reference_number: str | None,
    customer_name: str | None,
    transaction_date: datetime,
    subtotal: float,
    discount: float,
    total_amount: float,
) -> SalesTransaction:
    transaction = SalesTransaction(
        business_id=business_id,
        reference_number=reference_number,
        customer_name=customer_name,
        transaction_date=transaction_date,
        subtotal=subtotal,
        discount=discount,
        total_amount=total_amount,
        status=TransactionStatus.COMPLETED,
    )
    db.add(transaction)
    db.flush()
    db.refresh(transaction)  # muat server_default (created_at/updated_at)
    return transaction


def create_item(
    db: Session,
    *,
    transaction_id: int,
    product_id: int,
    quantity: float,
    unit_price: float,
    subtotal: float,
    unit_hpp: float,
) -> SalesTransactionItem:
    item = SalesTransactionItem(
        transaction_id=transaction_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        subtotal=subtotal,
        unit_hpp=unit_hpp,
    )
    db.add(item)
    db.flush()
    return item


def get_by_business(db: Session, transaction_id: int, business_id: int) -> SalesTransaction | None:
    return (
        db.query(SalesTransaction)
        .filter(SalesTransaction.id == transaction_id, SalesTransaction.business_id == business_id)
        .first()
    )


def list_by_business(db: Session, business_id: int, *, limit: int = 50) -> list[SalesTransaction]:
    return (
        db.query(SalesTransaction)
        .filter(SalesTransaction.business_id == business_id)
        .order_by(SalesTransaction.transaction_date.desc(), SalesTransaction.id.desc())
        .limit(limit)
        .all()
    )


def list_in_range(
    db: Session,
    business_id: int,
    start: datetime,
    end: datetime,
) -> list[SalesTransaction]:
    return (
        db.query(SalesTransaction)
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .all()
    )


def revenue_by_day(
    db: Session,
    business_id: int,
    start: datetime,
    end: datetime,
) -> dict[date, dict]:
    rows = (
        db.query(
            func.date(SalesTransaction.transaction_date).label("day"),
            func.coalesce(func.sum(SalesTransaction.total_amount), 0).label("revenue"),
            func.coalesce(func.sum(SalesTransaction.subtotal), 0).label("subtotal"),
        )
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .group_by(func.date(SalesTransaction.transaction_date))
        .all()
    )
    return {row.day: {"revenue": float(row.revenue), "subtotal": float(row.subtotal)} for row in rows}


def cogs_by_day(
    db: Session,
    business_id: int,
    start: datetime,
    end: datetime,
) -> dict[date, float]:
    rows = (
        db.query(
            func.date(SalesTransaction.transaction_date).label("day"),
            func.coalesce(func.sum(SalesTransactionItem.quantity * SalesTransactionItem.unit_hpp), 0).label("cogs"),
        )
        .join(SalesTransaction, SalesTransaction.id == SalesTransactionItem.transaction_id)
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .group_by(func.date(SalesTransaction.transaction_date))
        .all()
    )
    return {row.day: float(row.cogs) for row in rows}


def totals_in_range(db: Session, business_id: int, start: datetime, end: datetime) -> dict:
    row = (
        db.query(
            func.count(SalesTransaction.id).label("tx_count"),
            func.coalesce(func.sum(SalesTransaction.total_amount), 0).label("revenue"),
            func.coalesce(func.sum(SalesTransaction.subtotal), 0).label("subtotal"),
        )
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .first()
    )
    return {
        "tx_count": int(row.tx_count),
        "revenue": float(row.revenue),
        "subtotal": float(row.subtotal),
    }


def cogs_total_in_range(db: Session, business_id: int, start: datetime, end: datetime) -> float:
    value = (
        db.query(func.coalesce(func.sum(SalesTransactionItem.quantity * SalesTransactionItem.unit_hpp), 0))
        .join(SalesTransaction, SalesTransaction.id == SalesTransactionItem.transaction_id)
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .scalar()
    )
    return float(value)


def revenue_by_category(
    db: Session,
    business_id: int,
    start: datetime,
    end: datetime,
) -> dict[str, float]:
    """Omzet per kategori produk (3 huruf awal SKU)."""
    rows = (
        db.query(
            func.left(Product.sku, 3).label("category"),
            func.coalesce(func.sum(SalesTransactionItem.quantity * SalesTransactionItem.unit_price), 0).label("revenue"),
        )
        .join(Product, Product.id == SalesTransactionItem.product_id)
        .join(SalesTransaction, SalesTransaction.id == SalesTransactionItem.transaction_id)
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .group_by(func.left(Product.sku, 3))
        .all()
    )
    return {row.category: float(row.revenue) for row in rows}


def sales_qty_per_product(
    db: Session,
    business_id: int,
    start: datetime,
    end: datetime,
) -> dict[int, float]:
    rows = (
        db.query(
            SalesTransactionItem.product_id,
            func.coalesce(func.sum(SalesTransactionItem.quantity), 0).label("qty"),
        )
        .join(SalesTransaction, SalesTransaction.id == SalesTransactionItem.transaction_id)
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .group_by(SalesTransactionItem.product_id)
        .all()
    )
    return {row.product_id: float(row.qty) for row in rows}


def daily_qty_per_product(
    db: Session,
    business_id: int,
    start: datetime,
    end: datetime,
) -> dict[int, dict[date, float]]:
    """Qty terjual per produk per hari — input utama forecasting."""
    rows = (
        db.query(
            SalesTransactionItem.product_id,
            func.date(SalesTransaction.transaction_date).label("day"),
            func.coalesce(func.sum(SalesTransactionItem.quantity), 0).label("qty"),
        )
        .join(SalesTransaction, SalesTransaction.id == SalesTransactionItem.transaction_id)
        .filter(
            SalesTransaction.business_id == business_id,
            SalesTransaction.transaction_date >= start,
            SalesTransaction.transaction_date < end,
            SalesTransaction.status == TransactionStatus.COMPLETED,
        )
        .group_by(SalesTransactionItem.product_id, func.date(SalesTransaction.transaction_date))
        .all()
    )
    result: dict[int, dict[date, float]] = {}
    for row in rows:
        result.setdefault(row.product_id, {})[row.day] = float(row.qty)
    return result
