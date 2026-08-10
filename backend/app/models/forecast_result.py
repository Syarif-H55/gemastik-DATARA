from datetime import date, datetime

from sqlalchemy import Date, DateTime, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.types import fk_bigint, pk_bigint


class ForecastResult(Base):
    __tablename__ = "forecast_results"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, index=True)
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    predicted_quantity: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    business: Mapped["Business"] = relationship(back_populates="forecast_results")
    product: Mapped["Product"] = relationship(back_populates="forecast_results")
