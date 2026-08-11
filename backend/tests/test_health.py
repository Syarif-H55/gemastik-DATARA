"""Test endpoint health check (tanpa memerlukan MySQL berjalan)."""
import pytest
from fastapi.testclient import TestClient

from app.db.session import get_db
from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health_returns_ok(client: TestClient) -> None:
    res = client.get("/api/health")
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"
    assert body["data"]["version"]


def test_health_db_reports_unreachable_when_db_down(client: TestClient) -> None:
    class _BrokenDB:
        def execute(self, *args, **kwargs):
            raise RuntimeError("database unreachable")

    def _override_get_db():
        yield _BrokenDB()

    app.dependency_overrides[get_db] = _override_get_db
    try:
        res = client.get("/api/health/db")
    finally:
        app.dependency_overrides.clear()

    assert res.status_code == 503
    body = res.json()
    assert body["success"] is False
    assert body["data"]["database"] == "unreachable"


def test_unknown_route_returns_structured_error(client: TestClient) -> None:
    res = client.get("/api/does-not-exist")
    assert res.status_code == 404
    body = res.json()
    assert body["success"] is False
    assert "message" in body


def test_canonical_api_structure(client: TestClient) -> None:
    """Health di /api/* (bukan /api/v1); business router dipasang di /api/v1."""
    paths = set(app.openapi()["paths"])
    assert "/api/health" in paths
    assert "/api/health/db" in paths
    assert "/api/v1/health" not in paths