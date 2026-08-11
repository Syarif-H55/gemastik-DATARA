from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import RecommendationStatus
from app.models.types import fk_bigint, pk_bigint


class RestockRecommendation(Base):
    __tablename__ = "restock_recommendations"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("businesses.id"), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("products.id"), nullable=False, index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    current_stock: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    forecasted_demand: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    safety_days: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    recommended_quantity: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    reason_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(RecommendationStatus, native_enum=True), nullable=False, default=RecommendationStatus.PENDING
    )

    business: Mapped["Business"] = relationship(back_populates="restock_recommendations")
    product: Mapped["Product"] = relationship(back_populates="restock_recommendations")
