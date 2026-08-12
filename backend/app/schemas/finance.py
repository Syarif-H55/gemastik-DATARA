"""Skema request/response untuk Operating Expense (API Contract bab 10.2)."""
from datetime import date

from pydantic import BaseModel, Field

_EXPENSE_CATEGORY_MAP = {
    "rent": "RENT",
    "fixed_salary": "FIXED_SALARY",
    "administrative": "ADMINISTRATIVE",
    "other": "OTHER",
}


class OperatingExpenseCreateRequest(BaseModel):
    expense_date: date
    category: str = Field(pattern="^(rent|fixed_salary|administrative|other)$")
    amount: float = Field(gt=0)
    description: str | None = Field(default=None, max_length=150)


class OperatingExpenseUpdateRequest(BaseModel):
    expense_date: date | None = None
    category: str | None = Field(default=None, pattern="^(rent|fixed_salary|administrative|other)$")
    amount: float | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, max_length=150)


def expense_category_to_enum(category: str) -> str:
    return _EXPENSE_CATEGORY_MAP[category]


def expense_enum_to_category(value: str) -> str:
    inverse = {v: k for k, v in _EXPENSE_CATEGORY_MAP.items()}
    return inverse[value]