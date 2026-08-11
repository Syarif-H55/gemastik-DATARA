"""Growth Map API (API Contract bab 17)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.services import growth_service

router = APIRouter()


@router.get("", response_model=dict)
def get_growth(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": growth_service.growth_stages(db, business)}
