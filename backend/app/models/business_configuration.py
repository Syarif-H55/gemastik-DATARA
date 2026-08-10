from datetime import datetime

from sqlalchemy import DateTime, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.types import fk_bigint, pk_bigint


class BusinessConfiguration(Base):
    __tablename__ = "business_configurations"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), nullable=False, unique=True, index=True)
    safety_days: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=3)
    lead_time: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=3)
    target_margin: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False, default=30)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    business: Mapped["Business"] = relationship(back_populates="configuration")
