from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import PeriodType, TargetStatus, TargetType
from app.models.types import fk_bigint, pk_bigint


class BusinessTarget(Base):
    __tablename__ = "business_targets"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    target_type: Mapped[TargetType] = mapped_column(Enum(TargetType, native_enum=True), nullable=False)
    target_value: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    period_type: Mapped[PeriodType] = mapped_column(Enum(PeriodType, native_enum=True), nullable=False)
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[TargetStatus] = mapped_column(Enum(TargetStatus, native_enum=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    business: Mapped["Business"] = relationship(back_populates="targets")
