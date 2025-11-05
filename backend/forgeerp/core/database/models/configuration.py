"""Configuration model - Configurações do sistema"""

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from .base import BaseModel


class Configuration(BaseModel, table=True):
    """Configuração do sistema ou de módulo"""
    
    __tablename__ = "configurations"
    
    # Escopo da configuração
    client_id: Optional[int] = Field(default=None, foreign_key="clients.id", index=True)
    module_id: Optional[int] = Field(default=None, foreign_key="modules.id", index=True)
    
    # Chave e valor
    key: str = Field(index=True)  # Chave da configuração
    value: str  # Valor da configuração (pode ser JSON)
    
    # Tipo
    value_type: str = Field(default="string")  # string, json, integer, boolean
    
    # Descrição
    description: Optional[str] = Field(default=None)
    
    # Status
    is_active: bool = Field(default=True)
    
    # Relacionamento (usando ForeignKey apenas)

