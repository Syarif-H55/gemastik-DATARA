"""Forecasting API (API Contract bab 12)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.services import forecasting_service

router = APIRouter()


@router.get("/products", response_model=dict)
def forecast_all(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": forecasting_service.forecast_all(db, business)}


@router.get("/products/{product_id}", response_model=dict)
def forecast_product(
    product_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": forecasting_service.forecast_product(db, business, product_id)}
