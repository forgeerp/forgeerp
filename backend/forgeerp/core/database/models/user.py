"""User model - Usuários do sistema"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .base import BaseModel


class User(BaseModel, table=True):
    """Usuário do sistema (parceiro Odoo que gerencia clientes)"""
    
    __tablename__ = "users"
    
    # Informações do Usuário
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password_hash: str  # Hash da senha (bcrypt)
    
    # Perfil
    full_name: Optional[str] = Field(default=None)
    role: str = Field(default="user", index=True)  # viewer, user, admin, superuser
    is_active: bool = Field(default=True, index=True)
    is_superuser: bool = Field(default=False, index=True)
    
    # Autenticação
    last_login_at: Optional[datetime] = Field(default=None)
    failed_login_attempts: int = Field(default=0)
    locked_until: Optional[datetime] = Field(default=None)  # Lock temporário após muitas tentativas
    
    # Relacionamentos (usando ForeignKey apenas)


class Session(BaseModel, table=True):
    """Sessões e tokens JWT"""
    
    __tablename__ = "sessions"
    
    user_id: int = Field(foreign_key="users.id", index=True)
    token: str = Field(unique=True, index=True)  # JWT token
    
    # Informações da sessão
    ip_address: Optional[str] = Field(default=None)
    user_agent: Optional[str] = Field(default=None)
    
    # Expiração
    expires_at: datetime = Field(index=True)
    
    # Status
    is_active: bool = Field(default=True, index=True)
    
    # Relacionamento (usando ForeignKey apenas)

