"""Dependency injection bersama untuk endpoint FastAPI DATARA.

Termasuk dependency autentikasi & authorization:
- ``get_current_user``    — muat user dari Bearer JWT.
- ``get_current_business``— muat business milik user yang terautentikasi.
- ``assert_business_access`` — pastikan business_id (dari client, jika ada)
  sama dengan business milik user; jika tidak -> 403.
"""
from collections.abc import Generator

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.errors import ForbiddenError, NotFoundError, UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.business import Business
from app.models.user import User
from app.repositories import business_repository, user_repository

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_settings() -> Settings:
    return get_settings()


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_current_settings),
) -> User:
    if credentials is None:
        raise UnauthorizedError()
    user_id = decode_access_token(credentials.credentials, secret=settings.resolved_jwt_secret)
    if user_id is None:
        raise UnauthorizedError("Token tidak valid atau sudah kedaluwarsa.")
    user = user_repository.get_by_id(db, user_id)
    if user is None:
        raise UnauthorizedError()
    return user


def get_current_business(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Business:
    business = business_repository.get_by_user_id(db, user.id)
    if business is None:
        raise NotFoundError("Business belum dibuat untuk user ini.")
    return business


def assert_business_access(business: Business, business_id: int) -> None:
    """Jangan percaya business_id dari client tanpa authorization check."""
    if business.id != business_id:
        raise ForbiddenError("Anda tidak memiliki akses ke business ini.")


__all__ = [
    "Session",
    "Generator",
    "get_db",
    "get_settings",
    "get_current_settings",
    "bearer_scheme",
    "get_current_user",
    "get_current_business",
    "assert_business_access",
]
