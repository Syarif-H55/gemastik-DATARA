"""Decisions & Monitoring API (API Contract bab 16)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.services import decision_service

router = APIRouter()


@router.get("", response_model=dict)
def list_decisions(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": decision_service.list_decisions(db, business)}


@router.get("/{decision_id}", response_model=dict)
def get_decision(
    decision_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": decision_service.get_decision(db, business, decision_id)}


@router.post("/{decision_id}/dismiss", response_model=dict)
def dismiss_decision(
    decision_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": decision_service.dismiss(db, business, decision_id)}
