"""Client schemas - Pydantic schemas for Client"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class ClientBase(BaseModel):
    """Base client schema"""
    name: str
    code: str
    email: Optional[str] = None
    namespace_prefix: str = ""
    domain: Optional[str] = None


class ClientCreate(ClientBase):
    """Schema for creating a client"""
    pass


class ClientUpdate(BaseModel):
    """Schema for updating a client"""
    name: Optional[str] = None
    email: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None
    onboarding_completed: Optional[bool] = None


class ClientResponse(ClientBase):
    """Schema for client response"""
    id: int
    is_active: bool
    onboarding_completed: bool
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ClientListResponse(BaseModel):
    """Schema for client list response"""
    clients: List[ClientResponse]
    total: int

