"""Tests for authentication"""

from fastapi import status


def test_login_success(client, admin_user):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, admin_user):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "wrong"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_login_nonexistent_user(client):
    """Test login with nonexistent user"""
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "nonexistent", "password": "password"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user(client, auth_headers_admin, admin_user):
    """Test getting current user information"""
    response = client.get(
        "/api/v1/auth/me",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "admin"
    assert data["email"] == "admin@test.com"
    assert data["role"] == "superuser"


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client, auth_headers_admin):
    """Test logout"""
    response = client.post(
        "/api/v1/auth/logout",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Successfully logged out"

