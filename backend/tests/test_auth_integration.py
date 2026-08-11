"""Test autentikasi end-to-end terhadap MySQL lokal.

Dilewati (skip) otomatis bila database tidak dapat diakses.
Mencakup requirement TASK 03:
1. Login valid.
2. Login invalid.
3. Protected endpoint tanpa authentication (juga di test_auth_unit).
4. User A tidak dapat mengakses Business B.
5. Password tidak disimpan plaintext.
6. Token invalid (juga di test_auth_unit).
"""
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.api.deps import assert_business_access
from app.core.errors import ForbiddenError
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.repositories import business_repository, user_repository

try:
    _probe = SessionLocal()
    _probe.execute(text("SELECT 1"))
    _probe.close()
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False

pytestmark = pytest.mark.skipif(not DB_AVAILABLE, reason="MySQL tidak tersedia")

PASSWORD = "rahasia123"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def created_emails() -> list[str]:
    emails: list[str] = []
    yield emails
    db = SessionLocal()
    try:
        for email in emails:
            user = user_repository.get_by_email(db, email)
            if user is None:
                continue
            business = business_repository.get_by_user_id(db, user.id)
            if business is not None:
                db.delete(business)
                db.flush()
            db.delete(user)
        db.commit()
    finally:
        db.close()


def _make_user(created_emails: list[str], tag: str) -> tuple:
    db = SessionLocal()
    try:
        email = f"authit_{tag}_{uuid.uuid4().hex[:8]}@umkm.id"
        user = user_repository.create(db, name=f"Pemilik {tag}", email=email, password_hash=hash_password(PASSWORD))
        business = business_repository.create(db, user_id=user.id, name=f"Bisnis {tag}", business_type="food_beverage")
        db.commit()
        created_emails.append(email)
        return user, business
    finally:
        db.close()


def _login(client: TestClient, email: str, password: str = PASSWORD):
    return client.post("/api/v1/auth/login", json={"email": email, "password": password})


def test_login_valid(client: TestClient, created_emails: list[str]) -> None:
    user, _ = _make_user(created_emails, "valid")
    res = _login(client, user.email)
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["user"]["id"] == user.id
    assert data["user"]["email"] == user.email
    assert data["user"]["name"] == user.name
    assert data["access_token"]
    assert "password" not in data["user"]
    assert "role" not in data["user"]


def test_login_invalid_password(client: TestClient, created_emails: list[str]) -> None:
    user, _ = _make_user(created_emails, "invalidpw")
    res = _login(client, user.email, password="password-salah")
    assert res.status_code == 401
    body = res.json()
    assert body["success"] is False
    assert "kata sandi" in body["message"].lower()


def test_login_nonexistent_email(client: TestClient) -> None:
    res = _login(client, "tidak-ada@umkm.id")
    assert res.status_code == 401
    assert res.json()["success"] is False


def test_me_returns_authenticated_user(client: TestClient, created_emails: list[str]) -> None:
    user, _ = _make_user(created_emails, "me")
    token = _login(client, user.email).json()["data"]["access_token"]
    res = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    data = res.json()["data"]
    assert data["id"] == user.id
    assert data["email"] == user.email


def test_logout_returns_success(client: TestClient, created_emails: list[str]) -> None:
    user, _ = _make_user(created_emails, "logout")
    token = _login(client, user.email).json()["data"]["access_token"]
    res = client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
    assert body["message"] == "Logged out successfully"


def test_password_stored_as_hash_not_plaintext(created_emails: list[str]) -> None:
    user, _ = _make_user(created_emails, "hashcheck")
    db = SessionLocal()
    try:
        stored = user_repository.get_by_email(db, user.email)
        assert stored is not None
        assert stored.password.startswith("$2")
        assert PASSWORD not in stored.password
        assert stored.password != PASSWORD
    finally:
        db.close()


def test_user_a_cannot_access_business_b(client: TestClient, created_emails: list[str]) -> None:
    user_a, business_a = _make_user(created_emails, "userA")
    _user_b, business_b = _make_user(created_emails, "userB")

    # Guard ownership: business milik A != business B -> 403.
    with pytest.raises(ForbiddenError):
        assert_business_access(business_a, business_b.id)
    # Access ke business milik sendiri -> lolos.
    assert assert_business_access(business_a, business_a.id) is None

    # HTTP isolation: token A hanya bisa melihat business A sendiri.
    token_a = _login(client, user_a.email).json()["data"]["access_token"]
    res = client.get("/api/v1/business", headers={"Authorization": f"Bearer {token_a}"})
    assert res.status_code == 200
    assert res.json()["data"]["id"] == business_a.id
    assert res.json()["data"]["id"] != business_b.id
