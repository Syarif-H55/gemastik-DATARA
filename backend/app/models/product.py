from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.types import fk_bigint, pk_bigint


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("businesses.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    sku: Mapped[str | None] = mapped_column(String(50), nullable=True)
    selling_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    low_stock_threshold: Mapped[float | None] = mapped_column(Numeric(12, 2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    business: Mapped["Business"] = relationship(back_populates="products")
    costs: Mapped[list["ProductCost"]] = relationship(back_populates="product")
    inventory_item: Mapped["InventoryItem"] = relationship(back_populates="product", uselist=False)
    transaction_items: Mapped[list["SalesTransactionItem"]] = relationship(back_populates="product")
    inventory_movements: Mapped[list["InventoryMovement"]] = relationship(back_populates="product")
    forecast_results: Mapped[list["ForecastResult"]] = relationship(back_populates="product")
    restock_recommendations: Mapped[list["RestockRecommendation"]] = relationship(back_populates="product")
    pricing_recommendations: Mapped[list["PricingRecommendation"]] = relationship(back_populates="product")
