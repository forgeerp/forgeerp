"""Integration tests for client workflow"""

from fastapi import status


def test_complete_client_workflow(client, auth_headers_admin):
    """Test complete workflow: create, list, update, delete client"""
    # 1. List clients (should be empty)
    response = client.get(
        "/api/v1/clients",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 0
    
    # 2. Create client
    client_data = {
        "name": "Test Client",
        "code": "test-client",
        "email": "test@client.com",
        "namespace_prefix": "test",
        "domain": "test.client.com"
    }
    create_response = client.post(
        "/api/v1/clients",
        json=client_data,
        headers=auth_headers_admin
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    client_id = create_response.json()["id"]
    
    # 3. List clients (should have one)
    response = client.get(
        "/api/v1/clients",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["total"] == 1
    
    # 4. Get client
    response = client.get(
        f"/api/v1/clients/{client_id}",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Test Client"
    
    # 5. Update client
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
    assert response.json()["name"] == "Updated Client"
    
    # 6. Delete client (soft delete)
    response = client.delete(
        f"/api/v1/clients/{client_id}",
        headers=auth_headers_admin
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # 7. List clients (should still show one, but inactive)
    response = client.get(
        "/api/v1/clients",
        headers=auth_headers_admin
    )
    # Client should still exist but be filtered out by is_active=True
    assert response.status_code == status.HTTP_200_OK

