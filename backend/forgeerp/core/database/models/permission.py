"""Permission model - Sistema de permissões integrado com GitHub PRs"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .base import BaseModel


class Permission(BaseModel, table=True):
    """Permissão de usuário para ações específicas"""
    
    __tablename__ = "permissions"
    
    user_id: int = Field(foreign_key="users.id", index=True)
    
    # Tipo de permissão
    permission_type: str = Field(index=True)  # client_create, client_modify, deploy, disaster_recovery, etc.
    
    # Escopo (opcional)
    client_id: Optional[int] = Field(default=None, foreign_key="clients.id", index=True)
    environment: Optional[str] = Field(default=None)  # dev, hml, prod, ou None para todos
    
    # Status
    is_active: bool = Field(default=True)
    
    # Relacionamento (usando ForeignKey apenas)


class PullRequest(BaseModel, table=True):
    """Pull Request do GitHub para mudanças graves"""
    
    __tablename__ = "pull_requests"
    
    # Informações do PR
    github_pr_number: int = Field(unique=True, index=True)  # Número do PR no GitHub
    github_pr_url: str  # URL do PR
    title: str
    description: Optional[str] = Field(default=None)
    
    # Status
    status: str = Field(default="open", index=True)  # open, approved, merged, closed, rejected
    is_approved: bool = Field(default=False, index=True)
    is_merged: bool = Field(default=False, index=True)
    
    # Mudança proposta
    change_type: str = Field(index=True)  # deploy, disaster_recovery, config_change, etc.
    change_target: Optional[str] = Field(default=None)  # Cliente/ambiente afetado
    change_data: Optional[str] = Field(default=None)  # JSON com detalhes da mudança
    
    # Aprovações (usando ForeignKey apenas)
    
    # Timestamps
    merged_at: Optional[datetime] = Field(default=None)
    closed_at: Optional[datetime] = Field(default=None)


class PullRequestApproval(BaseModel, table=True):
    """Aprovação de PR por um usuário"""
    
    __tablename__ = "pull_request_approvals"
    
    pull_request_id: int = Field(foreign_key="pull_requests.id", index=True)
    approver_id: int = Field(foreign_key="users.id", index=True)
    
    # Status da aprovação
    approved: bool = Field(default=True)
    comment: Optional[str] = Field(default=None)
    
    # Relacionamentos (usando ForeignKey apenas)

