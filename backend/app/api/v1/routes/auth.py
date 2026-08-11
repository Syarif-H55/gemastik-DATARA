"""Authentication API (API Contract bab 4).

- ``POST /api/v1/auth/register`` — buat akun baru (user + business).
- ``POST /api/v1/auth/login``   — validasi kredensial, kembalikan access token.
- ``POST /api/v1/auth/google``  — login/registrasi via Sign in with Google
  (ID token diverifikasi backend; akun baru dibuat otomatis bila email belum ada).
- ``GET  /api/v1/auth/me``      — user yang sedang terautentikasi.
- ``POST /api/v1/auth/logout``  — konfirmasi logout (token stateless dibuang client).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_settings, get_current_user, get_db
from app.core.config import Settings
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import GoogleLoginRequest, LoginRequest, LoginResponse, RegisterRequest, UserResponse
from app.services import auth_service

router = APIRouter()


def _session_data(user: User) -> dict:
    token = create_access_token(user.id)
    return LoginResponse(
        user=UserResponse(id=user.id, name=user.name, email=user.email),
        access_token=token,
    ).model_dump()


@router.post("/register", response_model=dict, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    user = auth_service.register(
        db,
        name=payload.name,
        email=payload.email,
        password=payload.password,
        business_name=payload.business_name,
        business_type=payload.business_type,
    )
    return {"success": True, "data": _session_data(user)}


@router.post("/login", response_model=dict)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = auth_service.authenticate(db, payload.email, payload.password)
    return {"success": True, "data": _session_data(user)}


@router.post("/google", response_model=dict)
def login_google(
    payload: GoogleLoginRequest,
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_current_settings),
) -> dict:
    user = auth_service.login_with_google(
        db, id_token=payload.id_token, client_id=settings.google_client_id
    )
    return {"success": True, "data": _session_data(user)}


@router.get("/me", response_model=dict)
def me(current_user: User = Depends(get_current_user)) -> dict:
    data = UserResponse(id=current_user.id, name=current_user.name, email=current_user.email)
    return {"success": True, "data": data.model_dump()}


@router.post("/logout", response_model=dict)
def logout(current_user: User = Depends(get_current_user)) -> dict:
    return {"success": True, "message": "Logged out successfully"}
