"""Service autentikasi user (login)."""
from sqlalchemy.orm import Session

from app.core.errors import UnauthorizedError
from app.core.security import verify_password
from app.models.user import User
from app.repositories import user_repository


def authenticate(db: Session, email: str, password: str) -> User:
    """Validasi kredensial. Pesan error seragam agar tidak bocor info akun."""
    user = user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.password):
        raise UnauthorizedError("Email atau kata sandi salah.")
    return user
