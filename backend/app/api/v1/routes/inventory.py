"""Inventory API (API Contract bab 9)."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_business, get_db
from app.models.business import Business
from app.schemas.inventory import InventoryMovementCreateRequest
from app.services import inventory_service

router = APIRouter()


@router.get("", response_model=dict)
def list_inventory(
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": inventory_service.list_inventory(db, business)}


@router.get("/movements", response_model=dict)
def list_movements(
    product_id: int | None = Query(default=None),
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": inventory_service.list_movements(db, business, product_id=product_id)}


@router.post("/movements", response_model=dict, status_code=201)
def create_movement(
    payload: InventoryMovementCreateRequest,
    business: Business = Depends(get_current_business),
    db: Session = Depends(get_db),
) -> dict:
    return {"success": True, "data": inventory_service.create_movement(db, business, payload)}
