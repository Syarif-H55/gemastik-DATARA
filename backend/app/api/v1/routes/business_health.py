"""Business Health API (API Contract bab 15). Dipasang di /api/v1/health."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.services import analytics_service

router = APIRouter()


@router.get("", response_model=dict)
def get_health(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": analytics_service.business_health(db, business)}
