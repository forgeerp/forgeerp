"""Module model - Módulos instalados"""

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .base import BaseModel


class Module(BaseModel, table=True):
    """Módulo disponível no sistema"""
    
    __tablename__ = "modules"
    
    # Informações do Módulo
    name: str = Field(unique=True, index=True)  # Nome do módulo (ex: "hetzner", "postgresql")
    display_name: str  # Nome para exibição
    description: Optional[str] = Field(default=None)
    category: str = Field(default="addon", index=True)  # core, addon
    
    # Dependências
    depends_on: Optional[str] = Field(default=None)  # Módulos dependentes (JSON array)
    
    # Status
    is_active: bool = Field(default=True)
    is_installed: bool = Field(default=False, index=True)
    
    # Relacionamento (usando sa_relationship_kwargs para evitar import circular)


class ClientModule(BaseModel, table=True):
    """Módulo instalado para um cliente"""
    
    __tablename__ = "client_modules"
    
    client_id: int = Field(foreign_key="clients.id", index=True)
    module_id: int = Field(foreign_key="modules.id", index=True)
    
    # Configurações específicas do módulo para este cliente
    config: Optional[str] = Field(default=None)  # JSON com configurações
    
    # Status
    is_active: bool = Field(default=True)
    
    # Relacionamentos (usando ForeignKey apenas)

