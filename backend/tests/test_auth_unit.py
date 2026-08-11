"""Test autentikasi tanpa memerlukan MySQL.

Mencakup: hashing password (tidak plaintext), JWT create/decode, dan
status 401 untuk endpoint protected tanpa token / token invalid.
"""
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_current_settings
from app.core.config import Settings
from app.core.security import create_access_token, decode_access_token, hash_password, verify_password
from app.main import app

TEST_SECRET = "unit-test-secret-key-unit-test-secret-key"


@pytest.fixture
def client() -> TestClient:
    app.dependency_overrides[get_current_settings] = lambda: Settings(
        _env_file=None, jwt_secret=TEST_SECRET
    )
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


# --- Password hashing ---

def test_password_is_not_stored_plaintext() -> None:
    hashed = hash_password("rahasia123")
    assert hashed != "rahasia123"
    assert "rahasia123" not in hashed
    assert hashed.startswith("$2")


def test_password_hash_roundtrip() -> None:
    hashed = hash_password("rahasia123")
    assert verify_password("rahasia123", hashed)
    assert not verify_password("salah-password", hashed)


def test_verify_password_rejects_invalid_hash() -> None:
    assert not verify_password("x", "bukan-hash")


# --- Token JWT ---

def test_create_and_decode_access_token() -> None:
    token = create_access_token(42, secret=TEST_SECRET)
    assert decode_access_token(token, secret=TEST_SECRET) == 42


def test_decode_invalid_token_returns_none() -> None:
    assert decode_access_token("bukan-jwt", secret=TEST_SECRET) is None


def test_decode_token_wrong_secret_returns_none() -> None:
    token = create_access_token(1, secret="secret-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert decode_access_token(token, secret="secret-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb") is None


def test_decode_expired_token_returns_none() -> None:
    token = create_access_token(1, secret=TEST_SECRET, expires_delta=timedelta(seconds=-10))
    assert decode_access_token(token, secret=TEST_SECRET) is None


# --- HTTP: endpoint protected ---

def test_me_requires_authentication(client: TestClient) -> None:
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
    body = res.json()
    assert body["success"] is False
    assert "Autentikasi" in body["message"]


def test_me_rejects_invalid_token(client: TestClient) -> None:
    res = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
    assert res.status_code == 401
    assert res.json()["success"] is False


def test_business_requires_authentication(client: TestClient) -> None:
    res = client.get("/api/v1/business")
    assert res.status_code == 401
    assert res.json()["success"] is False


# --- Google OAuth (Sign in with Google) ---

def _fake_user() -> object:
    return type("User", (), {"id": 7, "name": "Budi Google", "email": "budi@example.com"})


def _fake_db() -> object:
    """Session palsu — service di-monkeypatch sehingga DB tidak disentuh."""
    return type("FakeSession", (), {})()


def test_google_login_rejects_when_not_configured(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.api.deps import get_db

    app.dependency_overrides[get_db] = lambda: _fake_db()

    res = client.post("/api/v1/auth/google", json={"id_token": "eyJhbGciOiJSUzI1NiJ9.abc.def"})
    assert res.status_code == 401
    body = res.json()
    assert body["success"] is False
    assert "GOOGLE_CLIENT_ID" in body["message"]


def test_google_login_rejects_invalid_token(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.api.deps import get_db, get_current_settings
    from app.core.config import Settings
    from app.services import auth_service

    def fake_verify(*args: object, **kwargs: object) -> dict:
        from app.core.errors import UnauthorizedError

        raise UnauthorizedError("Token Google tidak valid atau sudah kedaluwarsa.")

    app.dependency_overrides[get_current_settings] = lambda: Settings(
        _env_file=None, jwt_secret=TEST_SECRET, google_client_id="client-id-tes.apps.googleusercontent.com"
    )
    app.dependency_overrides[get_db] = lambda: _fake_db()
    monkeypatch.setattr(auth_service, "_verify_google_id_token", fake_verify)

    res = client.post("/api/v1/auth/google", json={"id_token": "token-palsu-yang-cukup-panjang-untuk-lolos-validasi"})
    assert res.status_code == 401
    assert res.json()["success"] is False


def test_google_login_with_verified_token(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    from app.api.deps import get_db, get_current_settings
    from app.core.config import Settings
    from app.services import auth_service

    app.dependency_overrides[get_current_settings] = lambda: Settings(
        _env_file=None, jwt_secret=TEST_SECRET, google_client_id="client-id-tes.apps.googleusercontent.com"
    )
    app.dependency_overrides[get_db] = lambda: _fake_db()
    monkeypatch.setattr(auth_service, "login_with_google", lambda db, *, id_token, client_id: _fake_user())

    res = client.post("/api/v1/auth/google", json={"id_token": "eyJhbGciOiJSUzI1NiJ9.abc.def"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["user"]["email"] == "budi@example.com"
    assert data["access_token"]
