"""Repository akses data untuk entitas User."""
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create(db: Session, *, name: str, email: str, password_hash: str) -> User:
    """Buat user baru. Password WAJIB sudah berupa hash (jangan kirim plaintext)."""
    user = User(name=name, email=email, password=password_hash)
    db.add(user)
    db.flush()
    return user
