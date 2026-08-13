"""Service autentikasi user (login & registrasi)."""
import secrets

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token
from sqlalchemy.orm import Session

from app.core.errors import ConflictError, UnauthorizedError
from app.core.security import hash_password, verify_password
from app.models.business import Business
from app.models.business_configuration import BusinessConfiguration
from app.models.user import User
from app.repositories import business_repository, user_repository

_GOOGLE_ISSUERS = ("accounts.google.com", "https://accounts.google.com")


def authenticate(db: Session, email: str, password: str) -> User:
    """Validasi kredensial. Pesan error seragam agar tidak bocor info akun."""
    user = user_repository.get_by_email(db, email)
    if user is None or not verify_password(password, user.password):
        raise UnauthorizedError("Email atau kata sandi salah.")
    return user


def _verify_google_id_token(id_token: str, client_id: str) -> dict:
    """Verifikasi ID token Google: signature, aud, exp, iss.

    Melempar UnauthorizedError bila token tidak valid.
    """
    try:
        info = google_id_token.verify_oauth2_token(
            id_token,
            google_requests.Request(),
            client_id,
            clock_skew_in_seconds=300,
        )
    except Exception as exc:
        raise UnauthorizedError(
            f"Token Google tidak valid atau sudah kedaluwarsa. ({type(exc).__name__}: {exc})"
        ) from exc
    if info.get("iss") not in _GOOGLE_ISSUERS:
        raise UnauthorizedError("Token Google tidak valid.")
    return info


def login_with_google(db: Session, *, id_token: str, client_id: str) -> User:
    """Login/registrasi via akun Google (Sign in with Google).

    ID token diverifikasi di backend (jangan percaya klaim dari client).
    User baru otomatis dibuat beserta business default; user lama yang
    emailnya sama langsung masuk.
    """
    if not client_id:
        raise UnauthorizedError(
            "Login Google belum dikonfigurasi — GOOGLE_CLIENT_ID belum diisi di backend/.env."
        )

    info = _verify_google_id_token(id_token, client_id)
    email = (info.get("email") or "").lower()
    if not email:
        raise UnauthorizedError("Akun Google tidak memiliki email.")

    user = user_repository.get_by_email(db, email)
    if user is not None:
        return user

    name = (info.get("name") or email.split("@")[0])[:100]
    user = user_repository.create(
        db,
        name=name,
        email=email,
        # Password acak: akun ini hanya bisa masuk lewat Google.
        password_hash=hash_password(secrets.token_urlsafe(32)),
    )
    business = business_repository.create(
        db,
        user_id=user.id,
        name="Bisnis Saya",
        business_type="food_beverage",
    )
    db.add(BusinessConfiguration(business_id=business.id, safety_days=3, lead_time=3, target_margin=30))
    db.commit()
    db.refresh(user)
    return user


def register(
    db: Session,
    *,
    name: str,
    email: str,
    password: str,
    business_name: str,
    business_type: str,
) -> User:
    """Buat user baru beserta business dan konfigurasi default."""
    if user_repository.get_by_email(db, email) is not None:
        raise ConflictError("Email sudah terdaftar. Gunakan email lain atau masuk.")

    user = user_repository.create(
        db,
        name=name,
        email=email,
        password_hash=hash_password(password),
    )
    business = business_repository.create(
        db,
        user_id=user.id,
        name=business_name,
        business_type=business_type,
    )
    db.add(BusinessConfiguration(business_id=business.id, safety_days=3, lead_time=3, target_margin=30))
    db.commit()
    db.refresh(user)
    return user
