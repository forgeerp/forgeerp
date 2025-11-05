"""Module routes"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from forgeerp.core.database.database import get_session
from forgeerp.core.database.models.module import Module, ClientModule
from forgeerp.core.database.models.user import User
from forgeerp.core.database.models.client import Client
from forgeerp.core.api.routes.auth import get_current_user_dependency as get_current_user
from forgeerp.core.services.authentication import check_permission
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/modules", tags=["modules"])


class ModuleResponse(BaseModel):
    """Schema for module response"""
    id: int
    name: str
    display_name: str
    description: str | None
    category: str
    is_active: bool
    is_installed: bool
    
    class Config:
        from_attributes = True


class ModuleCreate(BaseModel):
    """Schema for creating a module"""
    name: str
    display_name: str
    description: str | None = None
    category: str = "addon"
    depends_on: str | None = None


class ModuleListResponse(BaseModel):
    """Schema for module list response"""
    modules: List[ModuleResponse]
    total: int


class ClientModuleCreate(BaseModel):
    """Schema for installing a module for a client"""
    client_id: int
    module_id: int
    config: str | None = None


@router.get("/{module_id}", response_model=ModuleResponse)
async def get_module(
    module_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get a module by ID"""
    module = session.get(Module, module_id)
    
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    return ModuleResponse.model_validate(module)


@router.post("", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
async def create_module(
    module_data: ModuleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a new module"""
    # Check permission
    if not check_permission(current_user, "module_create"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if module already exists
    statement = select(Module).where(Module.name == module_data.name)
    existing = session.exec(statement).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Module already exists"
        )
    
    # Create module
    module = Module(**module_data.model_dump())
    session.add(module)
    session.commit()
    session.refresh(module)
    
    return ModuleResponse.model_validate(module)


@router.get("/clients/{client_id}", response_model=ModuleListResponse)
async def list_client_modules(
    client_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List modules installed for a client"""
    # Verify client exists
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Get installed modules for client
    statement = select(ClientModule).where(
        ClientModule.client_id == client_id,
        ClientModule.is_active == True
    )
    client_modules = session.exec(statement).all()
    
    # Get module details
    modules = []
    for cm in client_modules:
        module = session.get(Module, cm.module_id)
        if module:
            module_response = ModuleResponse.model_validate(module)
            module_response.is_installed = True
            modules.append(module_response)
    
    return ModuleListResponse(modules=modules, total=len(modules))


@router.post("/clients/{client_id}/install", status_code=status.HTTP_201_CREATED)
async def install_module_for_client(
    client_id: int,
    module_data: ClientModuleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Install a module for a client"""
    # Check permission
    if not check_permission(current_user, "module_install", client_id=client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Verify client exists
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Verify module exists
    module = session.get(Module, module_data.module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Check if already installed
    statement = select(ClientModule).where(
        ClientModule.client_id == client_id,
        ClientModule.module_id == module_data.module_id
    )
    existing = session.exec(statement).first()
    if existing:
        if existing.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Module already installed for this client"
            )
        else:
            # Reactivate if previously installed
            existing.is_active = True
            existing.config = module_data.config
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return {"message": "Module reactivated successfully", "id": existing.id}
    
    # Install module
    client_module = ClientModule(
        client_id=client_id,
        module_id=module_data.module_id,
        config=module_data.config
    )
    session.add(client_module)
    session.commit()
    session.refresh(client_module)
    
    return {"message": "Module installed successfully", "id": client_module.id}


@router.delete("/clients/{client_id}/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def uninstall_module_from_client(
    client_id: int,
    module_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Uninstall a module from a client (soft delete)"""
    # Check permission
    if not check_permission(current_user, "module_uninstall", client_id=client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Verify client exists
    client = session.get(Client, client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Verify module exists
    module = session.get(Module, module_id)
    if not module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    # Find client module
    statement = select(ClientModule).where(
        ClientModule.client_id == client_id,
        ClientModule.module_id == module_id
    )
    client_module = session.exec(statement).first()
    
    if not client_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not installed for this client"
        )
    
    # Soft delete
    client_module.is_active = False
    session.add(client_module)
    session.commit()
    
    return None


@router.get("", response_model=ModuleListResponse)
async def list_modules(
    client_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List all modules (optionally filter by client_id to show installation status)"""
    statement = select(Module).where(Module.is_active == True).offset(skip).limit(limit)
    modules = session.exec(statement).all()
    
    # If client_id provided, mark which modules are installed
    if client_id:
        client = session.get(Client, client_id)
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        # Get installed modules for client
        client_modules_stmt = select(ClientModule).where(
            ClientModule.client_id == client_id,
            ClientModule.is_active == True
        )
        client_modules = session.exec(client_modules_stmt).all()
        installed_module_ids = {cm.module_id for cm in client_modules}
        
        # Mark modules as installed
        module_responses = []
        for m in modules:
            mr = ModuleResponse.model_validate(m)
            mr.is_installed = m.id in installed_module_ids
            module_responses.append(mr)
    else:
        module_responses = [ModuleResponse.model_validate(m) for m in modules]
    
    count_statement = select(Module).where(Module.is_active == True)
    total = len(session.exec(count_statement).all())
    
    return ModuleListResponse(
        modules=module_responses,
        total=total
    )

