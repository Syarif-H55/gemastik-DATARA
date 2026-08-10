from datetime import datetime

from sqlalchemy import DateTime, Enum, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import RecommendationStatus
from app.models.types import fk_bigint, pk_bigint


class PricingRecommendation(Base):
    __tablename__ = "pricing_recommendations"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    current_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    current_hpp: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    recommended_price: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    estimated_margin: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    reason_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[RecommendationStatus] = mapped_column(
        Enum(RecommendationStatus, native_enum=True), nullable=False, default=RecommendationStatus.PENDING
    )

    business: Mapped["Business"] = relationship(back_populates="pricing_recommendations")
    product: Mapped["Product"] = relationship(back_populates="pricing_recommendations")
