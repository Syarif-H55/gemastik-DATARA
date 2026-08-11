"""Repository akses data untuk entitas Business.

Model MVP: satu user memiliki satu business (users 1:1 businesses).
"""
from sqlalchemy.orm import Session

from app.models.business import Business


def get_by_user_id(db: Session, user_id: int) -> Business | None:
    return db.query(Business).filter(Business.user_id == user_id).first()


def get_by_id(db: Session, business_id: int) -> Business | None:
    return db.query(Business).filter(Business.id == business_id).first()


def create(db: Session, *, user_id: int, name: str, business_type: str) -> Business:
    business = Business(user_id=user_id, name=name, business_type=business_type)
    db.add(business)
    db.flush()
    return business
