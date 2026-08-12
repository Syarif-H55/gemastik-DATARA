"""Finance API (API Contract bab 10)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.schemas.finance import OperatingExpenseCreateRequest, OperatingExpenseUpdateRequest
from app.services import analytics_service, expense_service

router = APIRouter()


@router.get("/summary", response_model=dict)
def summary(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": analytics_service.finance_summary(db, business)}


@router.get("/expenses", response_model=dict)
def list_expenses(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": expense_service.list_expenses(db, business)}


@router.post("/expenses", response_model=dict, status_code=201)
def create_expense(
    payload: OperatingExpenseCreateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": expense_service.create_expense(db, business, payload)}


@router.put("/expenses/{expense_id}", response_model=dict)
def update_expense(
    expense_id: int,
    payload: OperatingExpenseUpdateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": expense_service.update_expense(db, business, expense_id, payload)}


@router.delete("/expenses/{expense_id}", response_model=dict)
def delete_expense(
    expense_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": expense_service.delete_expense(db, business, expense_id)}