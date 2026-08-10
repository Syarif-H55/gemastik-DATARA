from datetime import datetime

from sqlalchemy import DateTime, Enum, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import CostType
from app.models.types import fk_bigint, pk_bigint


class ProductCost(Base):
    __tablename__ = "product_costs"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    cost_type: Mapped[CostType] = mapped_column(Enum(CostType, native_enum=True), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    cost_per_unit: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    product: Mapped["Product"] = relationship(back_populates="costs")
