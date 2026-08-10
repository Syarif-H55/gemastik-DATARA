from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import HealthStatus
from app.models.types import fk_bigint, pk_bigint


class BusinessHealthAssessment(Base):
    __tablename__ = "business_health_assessments"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    health_status: Mapped[HealthStatus] = mapped_column(Enum(HealthStatus, native_enum=True), nullable=False)
    score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    business: Mapped["Business"] = relationship(back_populates="health_assessments")
