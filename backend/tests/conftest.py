"""Pytest configuration and fixtures"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from forgeerp.main import app
from forgeerp.core.database.database import get_session
from forgeerp.core.database.models.user import User
from forgeerp.core.services.authentication import get_password_hash


@pytest.fixture(name="session")
def session_fixture():
    """Create a test database session"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create a test client"""
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="admin_user")
def admin_user_fixture(session: Session):
    """Create an admin user for testing"""
    user = User(
        username="admin",
        email="admin@test.com",
        password_hash=get_password_hash("admin"),
        full_name="Admin User",
        role="superuser",
        is_active=True,
        is_superuser=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="regular_user")
def regular_user_fixture(session: Session):
    """Create a regular user for testing"""
    user = User(
        username="user",
        email="user@test.com",
        password_hash=get_password_hash("user"),
        full_name="Regular User",
        role="user",
        is_active=True,
        is_superuser=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_headers_admin")
def auth_headers_admin_fixture(client: TestClient, admin_user: User):
    """Get auth headers for admin user"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="auth_headers_user")
def auth_headers_user_fixture(client: TestClient, regular_user: User):
    """Get auth headers for regular user"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "user", "password": "user"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

