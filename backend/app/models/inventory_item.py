from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.types import fk_bigint, pk_bigint


class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("businesses.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("products.id"), nullable=False, unique=True)
    current_stock: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    business: Mapped["Business"] = relationship(back_populates="inventory_items")
    product: Mapped["Product"] = relationship(back_populates="inventory_item")
