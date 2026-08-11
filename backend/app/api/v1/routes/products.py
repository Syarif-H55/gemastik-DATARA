"""Product & Cost API (API Contract bab 6-7)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.schemas.product import ProductCostsUpdateRequest, ProductCreateRequest, ProductUpdateRequest
from app.services import catalog_service

router = APIRouter()


@router.get("/profitability", response_model=dict)
def profitability(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.get_profitability(db, business)}


@router.get("", response_model=dict)
def list_products(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.list_products(db, business)}


@router.post("", response_model=dict, status_code=201)
def create_product(
    payload: ProductCreateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.create_product(db, business, payload)}


@router.get("/{product_id}", response_model=dict)
def get_product(
    product_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.get_product(db, business, product_id)}


@router.put("/{product_id}", response_model=dict)
def update_product(
    product_id: int,
    payload: ProductUpdateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.update_product(db, business, product_id, payload)}


@router.delete("/{product_id}", response_model=dict)
def deactivate_product(
    product_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.deactivate_product(db, business, product_id)}


@router.get("/{product_id}/costs", response_model=dict)
def get_costs(
    product_id: int,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.get_costs(db, business, product_id)}


@router.put("/{product_id}/costs", response_model=dict)
def update_costs(
    product_id: int,
    payload: ProductCostsUpdateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": catalog_service.update_costs(db, business, product_id, payload)}
