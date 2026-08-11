from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import TransactionStatus
from app.models.types import fk_bigint, pk_bigint


class SalesTransaction(Base):
    __tablename__ = "sales_transactions"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("businesses.id"), nullable=False, index=True)
    reference_number: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    customer_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    subtotal: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True)
    discount: Mapped[float | None] = mapped_column(Numeric(15, 2), nullable=True, default=0)
    total_amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, native_enum=True), nullable=False, default=TransactionStatus.COMPLETED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    business: Mapped["Business"] = relationship(back_populates="sales_transactions")
    items: Mapped[list["SalesTransactionItem"]] = relationship(
        back_populates="transaction", cascade="all, delete-orphan"
    )


class SalesTransactionItem(Base):
    __tablename__ = "sales_transaction_items"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    transaction_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("sales_transactions.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("products.id"), nullable=False, index=True)
    quantity: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    unit_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    subtotal: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unit_hpp: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    transaction: Mapped["SalesTransaction"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="transaction_items")
