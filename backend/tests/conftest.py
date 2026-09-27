import uuid
import jwt
import pytest
from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.app.core.database import SessionLocal
from backend.app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_token(user_id: str, role: str = "participant", email: str = "test@dogfood.dev") -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "role": "authenticated",
        "user_metadata": {"role": role, "name": f"User {role}"},
        "aud": "authenticated",
    }
    return jwt.encode(payload, settings.SUPABASE_JWT_SECRET, algorithm="HS256")


@pytest.fixture
def auth_headers():
    def _headers(role: str = "participant", user_id: str = None, email: str = None):
        uid = user_id or str(uuid.uuid4())
        mail = email or f"{uid[:8]}@dogfood.dev"
        token = create_token(uid, role=role, email=mail)
        return {"Authorization": f"Bearer {token}", "X-User-Id": uid}

    return _headers
