"""Smart Restock API (API Contract bab 14)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.repositories import recommendation_repository
from app.schemas.recommendation import RestockApplyRequest, RestockRecommendationCreateRequest
from app.services import decision_service, restock_service

router = APIRouter()


def _config(db: Session, business: Business) -> tuple[float, float]:
    config = recommendation_repository.get_configuration(db, business.id)
    return (
        float(config.safety_days) if config else 3.0,
        float(config.lead_time) if config else 3.0,
    )


@router.get("/recommendations", response_model=dict)
def get_recommendations(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    safety_days, lead_time = _config(db, business)
    return {"success": True, "data": restock_service.recommendations(db, business, safety_days, lead_time)}


@router.post("/recommendations", response_model=dict, status_code=201)
def generate_recommendation(
    payload: RestockRecommendationCreateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    safety_days, lead_time = _config(db, business)
    return {"success": True, "data": restock_service.generate(db, business, payload.product_id, safety_days, lead_time)}


@router.post("/apply", response_model=dict)
def apply_recommendation(
    payload: RestockApplyRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": decision_service.apply_restock(db, business, payload.recommendation_id)}
