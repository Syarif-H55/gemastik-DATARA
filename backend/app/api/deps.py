"""Dependency injection bersama untuk endpoint FastAPI DATARA."""
from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.db.session import get_db


def get_current_settings() -> Settings:
    return get_settings()


__all__ = ["Session", "Generator", "get_db", "get_settings", "get_current_settings"]