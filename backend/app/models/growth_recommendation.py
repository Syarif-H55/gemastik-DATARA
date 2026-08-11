from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import GrowthCategory, GrowthPriority, GrowthStatus
from app.models.types import fk_bigint, pk_bigint


class GrowthRecommendation(Base):
    __tablename__ = "growth_recommendations"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("businesses.id"), nullable=False, index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    category: Mapped[GrowthCategory] = mapped_column(Enum(GrowthCategory, native_enum=True), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[GrowthPriority] = mapped_column(Enum(GrowthPriority, native_enum=True), nullable=False)
    status: Mapped[GrowthStatus] = mapped_column(
        Enum(GrowthStatus, native_enum=True), nullable=False, default=GrowthStatus.ACTIVE
    )

    business: Mapped["Business"] = relationship(back_populates="growth_recommendations")
