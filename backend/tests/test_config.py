"""Test konfigurasi backend (tanpa memerlukan MySQL berjalan)."""
import pytest

from app.core.config import Settings


def test_defaults_do_not_hardcode_credentials() -> None:
    settings = Settings(_env_file=None)
    assert settings.database_url == ""
    assert settings.db_password == ""
    assert settings.db_name == ""
    assert settings.api_prefix == "/api"


def test_cors_origin_list_default() -> None:
    settings = Settings(_env_file=None)
    assert settings.cors_origin_list == ["http://localhost:3000"]


def test_cors_origin_list_splits(monkeypatch) -> None:
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000, http://localhost:3001")
    settings = Settings(_env_file=None)
    assert settings.cors_origin_list == ["http://localhost:3000", "http://localhost:3001"]


def test_resolved_database_url_from_database_url(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "mysql+pymysql://user:secret@db:3306/datara")
    settings = Settings(_env_file=None)
    assert settings.resolved_database_url == "mysql+pymysql://user:secret@db:3306/datara"


def test_resolved_database_url_raises_when_missing(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("DB_USER", raising=False)
    monkeypatch.delenv("DB_NAME", raising=False)
    settings = Settings(_env_file=None)
    with pytest.raises(RuntimeError, match="belum dikonfigurasi"):
        settings.resolved_database_url