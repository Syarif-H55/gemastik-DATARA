"""Authentication API (API Contract bab 4).

- ``POST /api/v1/auth/login``   — validasi kredensial, kembalikan access token.
- ``GET  /api/v1/auth/me``      — user yang sedang terautentikasi.
- ``POST /api/v1/auth/logout``  — konfirmasi logout (token stateless dibuang client).
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse
from app.services import auth_service

router = APIRouter()


@router.post("/login", response_model=dict)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = auth_service.authenticate(db, payload.email, payload.password)
    token = create_access_token(user.id)
    data = LoginResponse(
        user=UserResponse(id=user.id, name=user.name, email=user.email),
        access_token=token,
    )
    return {"success": True, "data": data.model_dump()}


@router.get("/me", response_model=dict)
def me(current_user: User = Depends(get_current_user)) -> dict:
    data = UserResponse(id=current_user.id, name=current_user.name, email=current_user.email)
    return {"success": True, "data": data.model_dump()}


@router.post("/logout", response_model=dict)
def logout(current_user: User = Depends(get_current_user)) -> dict:
    return {"success": True, "message": "Logged out successfully"}
