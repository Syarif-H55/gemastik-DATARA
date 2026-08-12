"""Repository akses data untuk Operating Expense (API Contract bab 10.2)."""
from datetime import date

from sqlalchemy.orm import Session

from app.models.enums import ExpenseType
from app.models.operating_expense import OperatingExpense


def list_by_business(db: Session, business_id: int, *, limit: int = 100) -> list[OperatingExpense]:
    return (
        db.query(OperatingExpense)
        .filter(OperatingExpense.business_id == business_id)
        .order_by(OperatingExpense.expense_date.desc(), OperatingExpense.id.desc())
        .limit(limit)
        .all()
    )


def get_by_business(db: Session, expense_id: int, business_id: int) -> OperatingExpense | None:
    return (
        db.query(OperatingExpense)
        .filter(OperatingExpense.id == expense_id, OperatingExpense.business_id == business_id)
        .first()
    )


def create(
    db: Session,
    *,
    business_id: int,
    expense_type: ExpenseType,
    name: str,
    amount: float,
    expense_date: date,
) -> OperatingExpense:
    expense = OperatingExpense(
        business_id=business_id,
        expense_type=expense_type,
        name=name,
        amount=amount,
        expense_date=expense_date,
    )
    db.add(expense)
    db.flush()
    return expense


def delete(db: Session, expense: OperatingExpense) -> None:
    db.delete(expense)
    db.flush()