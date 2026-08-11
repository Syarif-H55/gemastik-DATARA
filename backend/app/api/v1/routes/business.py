"""Business API (API Contract bab 5).

Endpoint business selalu memakai business milik user terautentikasi
(via ``get_current_business``) — client TIDAK mengirim ``business_id``.
Ini mencegah akses lintas business.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.repositories import business_configuration_repository
from app.schemas.auth import BusinessResponse

router = APIRouter()


@router.get("", response_model=dict)
def get_business(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    config = business_configuration_repository.get_by_business_id(db, business.id)
    safety_days = float(config.safety_days) if config else 3.0
    data = BusinessResponse(
        id=business.id,
        name=business.name,
        business_type=business.business_type,
        safety_days=safety_days,
    )
    return {"success": True, "data": data.model_dump()}
