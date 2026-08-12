"""Service Operating Expense (API Contract bab 10.2)."""
from datetime import date

from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.models.business import Business
from app.models.enums import ExpenseType
from app.repositories import expense_repository
from app.schemas.finance import (
    OperatingExpenseCreateRequest,
    OperatingExpenseUpdateRequest,
    expense_category_to_enum,
    expense_enum_to_category,
)


def _serialize(expense) -> dict:
    return {
        "id": expense.id,
        "expense_date": expense.expense_date.isoformat(),
        "category": expense_enum_to_category(expense.expense_type.value),
        "amount": float(expense.amount),
        "description": expense.name,
        "created_at": expense.created_at.isoformat(),
        "updated_at": expense.updated_at.isoformat(),
    }


def list_expenses(db: Session, business: Business) -> list[dict]:
    expenses = expense_repository.list_by_business(db, business.id)
    return [_serialize(e) for e in expenses]


def get_expense(db: Session, business: Business, expense_id: int) -> dict:
    expense = expense_repository.get_by_business(db, expense_id, business.id)
    if expense is None:
        raise NotFoundError("Biaya operasional tidak ditemukan.")
    return _serialize(expense)


def create_expense(db: Session, business: Business, payload: OperatingExpenseCreateRequest) -> dict:
    expense = expense_repository.create(
        db,
        business_id=business.id,
        expense_type=ExpenseType(expense_category_to_enum(payload.category)),
        name=payload.description or payload.category,
        amount=payload.amount,
        expense_date=payload.expense_date,
    )
    db.commit()
    return _serialize(expense)


def update_expense(db: Session, business: Business, expense_id: int, payload: OperatingExpenseUpdateRequest) -> dict:
    expense = expense_repository.get_by_business(db, expense_id, business.id)
    if expense is None:
        raise NotFoundError("Biaya operasional tidak ditemukan.")
    if payload.expense_date is not None:
        expense.expense_date = payload.expense_date
    if payload.amount is not None:
        expense.amount = payload.amount
    if payload.description is not None:
        expense.name = payload.description
    if payload.category is not None:
        expense.expense_type = ExpenseType(expense_category_to_enum(payload.category))
    db.commit()
    return _serialize(expense)


def delete_expense(db: Session, business: Business, expense_id: int) -> dict:
    expense = expense_repository.get_by_business(db, expense_id, business.id)
    if expense is None:
        raise NotFoundError("Biaya operasional tidak ditemukan.")
    expense_repository.delete(db, expense)
    db.commit()
    return {"id": expense_id, "deleted": True}