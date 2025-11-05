"""Client model - Clientes finais do parceiro Odoo"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .base import BaseModel


class Client(BaseModel, table=True):
    """
    Cliente final do parceiro Odoo
    
    IMPORTANTE: 
    - O parceiro Odoo faz 1 fork do ForgeERP e gerencia múltiplos clientes finais
    - Cada cliente final NÃO tem fork - apenas tem infraestrutura provisionada
    - Este modelo representa os clientes finais, não os forks do repositório
    """
    
    __tablename__ = "clients"
    
    # Informações do Cliente
    name: str = Field(index=True)  # Nome da empresa/cliente
    code: str = Field(unique=True, index=True)  # Código único do cliente (ex: "multimodas", "racco")
    email: Optional[str] = Field(default=None, index=True)
    
    # Informações de Infraestrutura
    namespace_prefix: str = Field(default="")  # Prefixo para namespaces (ex: "{code}-dev")
    domain: Optional[str] = Field(default=None)  # Domínio principal (ex: "multimodas.softhill.com.br")
    
    # Status
    is_active: bool = Field(default=True, index=True)
    onboarding_completed: bool = Field(default=False)
    
    # Relacionamentos (usando sa_relationship_kwargs para evitar import circular)
    # environments, modules e configurations serão definidos nos modelos respectivos
    
    # Timestamps
    last_sync_at: Optional[datetime] = Field(default=None)  # Última sincronização com GitHub


class Environment(BaseModel, table=True):
    """Ambientes de deploy (dev, hml, prod)"""
    
    __tablename__ = "environments"
    
    client_id: int = Field(foreign_key="clients.id", index=True)
    name: str = Field(index=True)  # dev, hml, prod
    namespace: str = Field(unique=True, index=True)  # Namespace completo (ex: "multimodas-dev")
    
    # Configurações do ambiente
    domain: Optional[str] = Field(default=None)  # Domínio do ambiente
    is_production: bool = Field(default=False, index=True)
    
    # Status
    is_active: bool = Field(default=True)
    
    # Relacionamento com Client
    # client será definido via ForeignKey

