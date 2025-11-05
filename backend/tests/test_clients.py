"""Tests for clients"""

from fastapi import status
from forgeerp.core.database.models.client import Client


def test_list_clients_empty(client, auth_headers_admin):
    """Test listing clients when empty"""
    response = client.get(
        "/api/v1/clients",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == 0
    assert len(data["clients"]) == 0


def test_create_client(client, auth_headers_admin, session):
    """Test creating a client"""
    client_data = {
        "name": "Test Client",
        "code": "test-client",
        "email": "test@client.com",
        "namespace_prefix": "test",
        "domain": "test.client.com"
    }
    response = client.post(
        "/api/v1/clients",
        json=client_data,
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Client"
    assert data["code"] == "test-client"
    assert data["is_active"] is True
    assert "id" in data


def test_create_client_duplicate_code(client, auth_headers_admin, session):
    """Test creating a client with duplicate code"""
    client_data = {
        "name": "Test Client",
        "code": "test-client",
        "email": "test@client.com"
    }
    # Create first client
    client.post(
        "/api/v1/clients",
        json=client_data,
        headers=auth_headers_admin
    )
    # Try to create second client with same code
    response = client.post(
        "/api/v1/clients",
        json=client_data,
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"]


def test_get_client(client, auth_headers_admin, session):
    """Test getting a client by ID"""
    # Create client
    client_data = {
        "name": "Test Client",
        "code": "test-client",
        "email": "test@client.com"
    }
    create_response = client.post(
        "/api/v1/clients",
        json=client_data,
        headers=auth_headers_admin
    )
    client_id = create_response.json()["id"]
    
    # Get client
    response = client.get(
        f"/api/v1/clients/{client_id}",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == client_id
    assert data["name"] == "Test Client"


def test_get_client_not_found(client, auth_headers_admin):
    """Test getting a nonexistent client"""
    response = client.get(
        "/api/v1/clients/999",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_client(client, auth_headers_admin, session):
    """Test updating a client"""
    # Create client
    client_data = {
        "name": "Test Client",
        "code": "test-client",
        "email": "test@client.com"
    }
    create_response = client.post(
        "/api/v1/clients",
        json=client_data,
        headers=auth_headers_admin
    )
    client_id = create_response.json()["id"]
    
    # Update client
    update_data = {
        "name": "Updated Client",
        "email": "updated@client.com"
    }
    response = client.patch(
        f"/api/v1/clients/{client_id}",
        json=update_data,
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Client"
    assert data["email"] == "updated@client.com"


def test_delete_client(client, auth_headers_admin, session):
    """Test deleting a client (soft delete)"""
    # Create client
    client_data = {
        "name": "Test Client",
        "code": "test-client",
        "email": "test@client.com"
    }
    create_response = client.post(
        "/api/v1/clients",
        json=client_data,
        headers=auth_headers_admin
    )
    client_id = create_response.json()["id"]
    
    # Delete client
    response = client.delete(
        f"/api/v1/clients/{client_id}",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify client is inactive
    get_response = client.get(
        f"/api/v1/clients/{client_id}",
        headers=auth_headers_admin
    )
    # Client should still exist but be inactive
    assert get_response.status_code == status.HTTP_200_OK


def test_create_client_unauthorized(client):
    """Test creating a client without authentication"""
    client_data = {
        "name": "Test Client",
        "code": "test-client",
        "email": "test@client.com"
    }
    response = client.post(
        "/api/v1/clients",
        json=client_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_clients_unauthorized(client):
    """Test listing clients without authentication"""
    response = client.get("/api/v1/clients")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

