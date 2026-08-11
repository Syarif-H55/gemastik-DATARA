from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import ExpenseType
from app.models.types import fk_bigint, pk_bigint


class OperatingExpense(Base):
    __tablename__ = "operating_expenses"

    id: Mapped[int] = mapped_column(pk_bigint(), primary_key=True, autoincrement=True)
    business_id: Mapped[int] = mapped_column(fk_bigint(), ForeignKey("businesses.id"), nullable=False, index=True)
    expense_type: Mapped[ExpenseType] = mapped_column(Enum(ExpenseType, native_enum=True), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(15, 2), nullable=False)
    expense_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    business: Mapped["Business"] = relationship(back_populates="operating_expenses")
