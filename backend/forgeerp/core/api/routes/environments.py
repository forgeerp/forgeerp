"""Environment routes"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from forgeerp.core.database.database import get_session
from forgeerp.core.database.models.client import Client, Environment
from forgeerp.core.database.models.user import User
from forgeerp.core.api.routes.auth import get_current_user_dependency as get_current_user
from forgeerp.core.services.authentication import check_permission
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/environments", tags=["environments"])


class EnvironmentResponse(BaseModel):
    """Schema for environment response"""
    id: int
    client_id: int
    name: str
    namespace: str
    domain: str | None
    is_production: bool
    is_active: bool
    
    class Config:
        from_attributes = True


class EnvironmentCreate(BaseModel):
    """Schema for creating an environment"""
    client_id: int
    name: str
    namespace: str
    domain: str | None = None
    is_production: bool = False


class EnvironmentUpdate(BaseModel):
    """Schema for updating an environment"""
    domain: str | None = None
    is_production: bool | None = None
    is_active: bool | None = None


class EnvironmentListResponse(BaseModel):
    """Schema for environment list response"""
    environments: List[EnvironmentResponse]
    total: int


@router.get("", response_model=EnvironmentListResponse)
async def list_environments(
    client_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List environments"""
    statement = select(Environment).where(Environment.is_active == True)
    
    if client_id:
        statement = statement.where(Environment.client_id == client_id)
    
    environments = session.exec(statement.offset(skip).limit(limit)).all()
    
    count_statement = select(Environment).where(Environment.is_active == True)
    if client_id:
        count_statement = count_statement.where(Environment.client_id == client_id)
    
    total = len(session.exec(count_statement).all())
    
    return EnvironmentListResponse(
        environments=[EnvironmentResponse.model_validate(e) for e in environments],
        total=total
    )


@router.get("/{env_id}", response_model=EnvironmentResponse)
async def get_environment(
    env_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get an environment by ID"""
    env = session.get(Environment, env_id)
    
    if not env:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Environment not found"
        )
    
    return EnvironmentResponse.model_validate(env)


@router.post("", response_model=EnvironmentResponse, status_code=status.HTTP_201_CREATED)
async def create_environment(
    env_data: EnvironmentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new environment"""
    # Check permission
    if not check_permission(current_user, "environment_create", client_id=env_data.client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Verify client exists
    client = session.get(Client, env_data.client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Check if namespace already exists
    statement = select(Environment).where(Environment.namespace == env_data.namespace)
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Environment with this namespace already exists"
        )
    
    # Create environment
    env = Environment(**env_data.model_dump())
    session.add(env)
    session.commit()
    session.refresh(env)
    
    return EnvironmentResponse.model_validate(env)


@router.patch("/{env_id}", response_model=EnvironmentResponse)
async def update_environment(
    env_id: int,
    env_data: EnvironmentUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update an environment"""
    env = session.get(Environment, env_id)
    
    if not env:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Environment not found"
        )
    
    # Check permission
    if not check_permission(current_user, "environment_modify", client_id=env.client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update fields
    update_data = env_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(env, field, value)
    
    env.updated_at = datetime.utcnow()
    session.add(env)
    session.commit()
    session.refresh(env)
    
    return EnvironmentResponse.model_validate(env)


@router.delete("/{env_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_environment(
    env_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Delete an environment (soft delete)"""
    env = session.get(Environment, env_id)
    
    if not env:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Environment not found"
        )
    
    # Check permission
    if not check_permission(current_user, "environment_delete", client_id=env.client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Soft delete
    env.is_active = False
    env.updated_at = datetime.utcnow()
    session.add(env)
    session.commit()
    
    return None

