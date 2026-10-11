import os

# Configure the app for an isolated in-memory database before it is imported.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SEED_DEMO_DATA"] = "false"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.user import User, UserRole
from app.services.auth import hash_password

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _make_user(username: str, role: str, password: str = "password123") -> None:
    with TestingSessionLocal() as db:
        db.add(
            User(
                username=username,
                email=f"{username}@example.com",
                hashed_password=hash_password(password),
                role=role,
            )
        )
        db.commit()


def _auth_headers(client: TestClient, username: str, password: str = "password123") -> dict[str, str]:
    res = client.post("/api/v1/auth/login", data={"username": username, "password": password})
    assert res.status_code == 200, res.text
    return {"Authorization": f"Bearer {res.json()['access_token']}"}


@pytest.fixture
def admin_headers(client):
    _make_user("admin", UserRole.ADMIN)
    return _auth_headers(client, "admin")


@pytest.fixture
def employee_headers(client):
    _make_user("viewer", UserRole.EMPLOYEE)
    return _auth_headers(client, "viewer")
