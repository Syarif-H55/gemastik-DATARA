"""Endpoint health check (infrastruktur).

- ``GET /api/health``      liveness — proses berjalan.
- ``GET /api/health/db``   readiness — memverifikasi koneksi database.
"""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_settings
from app.schemas.health import HealthDbData, HealthData

router = APIRouter()


@router.get("/health", response_model=dict)
def health() -> dict:
    settings = get_settings()
    return {
        "success": True,
        "data": HealthData(status="ok", app=settings.app_name, version=settings.app_version).model_dump(),
    }


@router.get("/health/db", response_model=dict)
def health_db(db: Session = Depends(get_db)) -> JSONResponse:
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "data": HealthDbData(status="error", database="unreachable").model_dump(),
            },
        )
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "data": HealthDbData(status="ok", database="connected").model_dump(),
        },
    )