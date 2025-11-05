"""Client routes"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from forgeerp.core.database.database import get_session
from forgeerp.core.database.models.client import Client
from forgeerp.core.database.models.user import User
from forgeerp.core.database.schemas.client import (
    ClientCreate,
    ClientUpdate,
    ClientResponse,
    ClientListResponse,
)
from forgeerp.core.api.routes.auth import get_current_user_dependency as get_current_user
from forgeerp.core.services.authentication import check_permission
from datetime import datetime

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("", response_model=ClientListResponse)
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List all clients"""
    statement = select(Client).where(Client.is_active == True).offset(skip).limit(limit)
    clients = session.exec(statement).all()
    
    count_statement = select(Client).where(Client.is_active == True)
    total = len(session.exec(count_statement).all())
    
    return ClientListResponse(clients=clients, total=total)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get a client by ID"""
    client = session.get(Client, client_id)
    
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    return client


@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new client"""
    # Check permission
    if not check_permission(current_user, "client_create"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if code already exists
    statement = select(Client).where(Client.code == client_data.code)
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Client code already exists"
        )
    
    # Create client
    client = Client(**client_data.model_dump())
    client.created_by = current_user.id
    client.updated_by = current_user.id
    
    session.add(client)
    session.commit()
    session.refresh(client)
    
    return client


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update a client"""
    # Check permission
    if not check_permission(current_user, "client_modify", client_id=client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Update fields
    update_data = client_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    
    client.updated_at = datetime.utcnow()
    client.updated_by = current_user.id
    
    session.add(client)
    session.commit()
    session.refresh(client)
    
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Delete a client (soft delete)"""
    # Check permission
    if not check_permission(current_user, "client_delete", client_id=client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Soft delete
    client.is_active = False
    client.updated_at = datetime.utcnow()
    client.updated_by = current_user.id
    
    session.add(client)
    session.commit()
    
    return None

