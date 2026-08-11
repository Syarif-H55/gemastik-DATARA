from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import MovementType
from app.models.types import fk_bigint, pk_bigint


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("businesses.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("products.id"), nullable=False, index=True)
    movement_type: Mapped[MovementType] = mapped_column(Enum(MovementType, native_enum=True), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    movement_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reference_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    business: Mapped["Business"] = relationship(back_populates="inventory_movements")
    product: Mapped["Product"] = relationship(back_populates="inventory_movements")
