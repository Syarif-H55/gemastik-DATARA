"""Repository akses data untuk entitas BusinessConfiguration."""
from sqlalchemy.orm import Session

from app.models.business_configuration import BusinessConfiguration


def get_by_business_id(db: Session, business_id: int) -> BusinessConfiguration | None:
    return db.query(BusinessConfiguration).filter(BusinessConfiguration.business_id == business_id).first()
