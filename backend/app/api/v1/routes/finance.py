"""Finance API (API Contract bab 10)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.services import analytics_service

router = APIRouter()


@router.get("/summary", response_model=dict)
def summary(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": analytics_service.finance_summary(db, business)}
