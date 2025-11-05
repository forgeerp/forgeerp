"""Configuration routes"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from forgeerp.core.database.database import get_session
from forgeerp.core.database.models.configuration import Configuration
from forgeerp.core.database.models.user import User
from forgeerp.core.api.routes.auth import get_current_user_dependency as get_current_user
from forgeerp.core.services.authentication import check_permission
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/configurations", tags=["configurations"])


class ConfigurationResponse(BaseModel):
    """Schema for configuration response"""
    id: int
    client_id: int | None
    module_id: int | None
    key: str
    value: str
    value_type: str
    description: str | None
    is_active: bool
    
    class Config:
        from_attributes = True


class ConfigurationCreate(BaseModel):
    """Schema for creating a configuration"""
    client_id: int | None = None
    module_id: int | None = None
    key: str
    value: str
    value_type: str = "string"
    description: str | None = None


class ConfigurationUpdate(BaseModel):
    """Schema for updating a configuration"""
    value: str | None = None
    value_type: str | None = None
    description: str | None = None
    is_active: bool | None = None


class ConfigurationListResponse(BaseModel):
    """Schema for configuration list response"""
    configurations: List[ConfigurationResponse]
    total: int


@router.get("", response_model=ConfigurationListResponse)
async def list_configurations(
    client_id: Optional[int] = None,
    module_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List configurations"""
    statement = select(Configuration).where(Configuration.is_active == True)
    
    if client_id:
        statement = statement.where(Configuration.client_id == client_id)
    if module_id:
        statement = statement.where(Configuration.module_id == module_id)
    
    configurations = session.exec(statement.offset(skip).limit(limit)).all()
    
    count_statement = select(Configuration).where(Configuration.is_active == True)
    if client_id:
        count_statement = count_statement.where(Configuration.client_id == client_id)
    if module_id:
        count_statement = count_statement.where(Configuration.module_id == module_id)
    
    total = len(session.exec(count_statement).all())
    
    return ConfigurationListResponse(
        configurations=[ConfigurationResponse.model_validate(c) for c in configurations],
        total=total
    )


@router.get("/{config_id}", response_model=ConfigurationResponse)
async def get_configuration(
    config_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get a configuration by ID"""
    config = session.get(Configuration, config_id)
    
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    return ConfigurationResponse.model_validate(config)


@router.post("", response_model=ConfigurationResponse, status_code=status.HTTP_201_CREATED)
async def create_configuration(
    config_data: ConfigurationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new configuration"""
    # Check permission
    if not check_permission(current_user, "config_create"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Create configuration
    config = Configuration(**config_data.model_dump())
    session.add(config)
    session.commit()
    session.refresh(config)
    
    return ConfigurationResponse.model_validate(config)


@router.patch("/{config_id}", response_model=ConfigurationResponse)
async def update_configuration(
    config_id: int,
    config_data: ConfigurationUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Update a configuration"""
    # Check permission
    if not check_permission(current_user, "config_modify"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    config = session.get(Configuration, config_id)
    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Configuration not found"
        )
    
    # Update fields
    update_data = config_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    config.updated_at = datetime.utcnow()
    session.add(config)
    session.commit()
    session.refresh(config)
    
    return ConfigurationResponse.model_validate(config)

