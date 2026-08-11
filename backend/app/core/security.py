"""Primitive keamanan DATARA: hashing password (bcrypt) dan access token (JWT).

Password tidak pernah disimpan/dikembalikan plaintext. Hash disimpan di kolom
``users.password`` (VARCHAR(255), prefix bcrypt ``$2b$``).

Token adalah JWT stateless (HS256) dengan claim ``sub`` = user id.
Secret dibaca dari konfigurasi saat pemanggilan (bukan import) agar mudah
di-override di test.
"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import get_settings


def hash_password(password: str) -> str:
    """Return bcrypt hash (str) — tidak pernah menyimpan plaintext."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verifikasi password terhadap hash bcrypt; aman untuk hash rusak."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_access_token(
    user_id: int,
    *,
    secret: str | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    settings = get_settings()
    secret = secret or settings.resolved_jwt_secret
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + (expires_delta or timedelta(minutes=settings.jwt_expire_minutes)),
        "type": "access",
    }
    return jwt.encode(payload, secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str, *, secret: str | None = None) -> int | None:
    """Decode token -> user id, atau None bila invalid/kedaluwarsa."""
    settings = get_settings()
    secret = secret or settings.resolved_jwt_secret
    try:
        payload = jwt.decode(token, secret, algorithms=[settings.jwt_algorithm])
    except jwt.InvalidTokenError:
        return None
    sub = payload.get("sub")
    try:
        return int(sub)
    except (TypeError, ValueError):
        return None
