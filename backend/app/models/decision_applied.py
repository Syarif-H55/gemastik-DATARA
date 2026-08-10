from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import DecisionAppliedStatus, DecisionAppliedType
from app.models.types import fk_bigint, pk_bigint


class DecisionApplied(Base):
    __tablename__ = "decisions_applied"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    recommendation_id: Mapped[int | None] = mapped_column(fk_bigint(), nullable=True)
    type: Mapped[DecisionAppliedType] = mapped_column(Enum(DecisionAppliedType, native_enum=True), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    reasoning: Mapped[str | None] = mapped_column(Text, nullable=True)
    applied_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    metrics_before: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    metrics_after: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    status: Mapped[DecisionAppliedStatus] = mapped_column(Enum(DecisionAppliedStatus, native_enum=True), nullable=False)
    outcome_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    business: Mapped["Business"] = relationship(back_populates="decisions_applied")
