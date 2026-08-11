from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.types import fk_bigint, pk_bigint


class Business(Base):
    __tablename__ = "businesses"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    business_type: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="business")
    configuration: Mapped["BusinessConfiguration"] = relationship(back_populates="business", uselist=False)
    targets: Mapped[list["BusinessTarget"]] = relationship(back_populates="business")
    products: Mapped[list["Product"]] = relationship(back_populates="business")
    sales_transactions: Mapped[list["SalesTransaction"]] = relationship(back_populates="business")
    inventory_items: Mapped[list["InventoryItem"]] = relationship(back_populates="business")
    inventory_movements: Mapped[list["InventoryMovement"]] = relationship(back_populates="business")
    operating_expenses: Mapped[list["OperatingExpense"]] = relationship(back_populates="business")
    forecast_results: Mapped[list["ForecastResult"]] = relationship(back_populates="business")
    restock_recommendations: Mapped[list["RestockRecommendation"]] = relationship(back_populates="business")
    pricing_recommendations: Mapped[list["PricingRecommendation"]] = relationship(back_populates="business")
    health_assessments: Mapped[list["BusinessHealthAssessment"]] = relationship(back_populates="business")
    growth_recommendations: Mapped[list["GrowthRecommendation"]] = relationship(back_populates="business")
    decisions_applied: Mapped[list["DecisionApplied"]] = relationship(back_populates="business")
    ai_conversations: Mapped[list["AIConversation"]] = relationship(back_populates="business")
