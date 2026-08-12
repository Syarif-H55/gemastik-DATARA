"""Sales Transaction API (API Contract bab 8)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.schemas.transaction import TransactionCreateRequest
from app.services import transaction_service

router = APIRouter()


@router.get("/{transaction_id}", response_model=dict)
def get_transaction(
    transaction_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": transaction_service.get_transaction(db, business, transaction_id)}


@router.post("", response_model=dict, status_code=201)
def create_transaction(
    payload: TransactionCreateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": transaction_service.create_sale(db, business, payload)}


@router.get("", response_model=dict)
def list_transactions(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": transaction_service.list_transactions(db, business)}
