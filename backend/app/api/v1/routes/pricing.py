"""Smart Pricing API (API Contract bab 13)."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.repositories import recommendation_repository
from app.schemas.recommendation import (
    PricingApplyRequest,
    PricingDismissRequest,
    PricingRecommendationCreateRequest,
)
from app.services import decision_service, pricing_service

router = APIRouter()


def _config(db: Session, business: Business) -> tuple[float, float, float]:
    config = recommendation_repository.get_configuration(db, business.id)
    return (
        float(config.safety_days) if config else 3.0,
        float(config.lead_time) if config else 3.0,
        float(config.target_margin) if config else 30.0,
    )


@router.get("/recommendations", response_model=dict)
def get_recommendations(
    target_margin: float | None = Query(default=None, ge=0, le=100),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    _, _, default_margin = _config(db, business)
    margin = target_margin if target_margin is not None else default_margin
    return {"success": True, "data": pricing_service.recommendations(db, business, margin)}


@router.post("/recommendations", response_model=dict, status_code=201)
def generate_recommendation(
    payload: PricingRecommendationCreateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": pricing_service.generate(db, business, payload.product_id, payload.target_margin)}


@router.post("/apply", response_model=dict)
def apply_recommendation(
    payload: PricingApplyRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": decision_service.apply_pricing(db, business, payload.recommendation_id)}


@router.post("/dismiss", response_model=dict)
def dismiss_recommendation(
    payload: PricingDismissRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": decision_service.dismiss_pricing(db, business, payload.recommendation_id)}
