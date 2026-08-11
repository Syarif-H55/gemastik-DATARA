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
