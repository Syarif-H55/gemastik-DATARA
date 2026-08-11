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
from app.schemas.business import BusinessUpdateRequest

router = APIRouter()


def _payload(db: Session, business: Business) -> dict:
    config = business_configuration_repository.get_by_business_id(db, business.id)
    safety_days = float(config.safety_days) if config else 3.0
    return BusinessResponse(
        id=business.id,
        name=business.name,
        business_type=business.business_type,
        safety_days=safety_days,
    ).model_dump()


@router.get("", response_model=dict)
def get_business(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": _payload(db, business)}


@router.put("", response_model=dict)
def update_business(
    payload: BusinessUpdateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    if payload.name is not None:
        business.name = payload.name
    if payload.business_type is not None:
        business.business_type = payload.business_type

    config = business_configuration_repository.get_by_business_id(db, business.id)
    if config is None and payload.safety_days is not None:
        from app.models.business_configuration import BusinessConfiguration

        config = BusinessConfiguration(business_id=business.id, safety_days=payload.safety_days)
        db.add(config)
    elif config is not None and payload.safety_days is not None:
        config.safety_days = payload.safety_days

    db.commit()
    return {"success": True, "data": _payload(db, business)}
