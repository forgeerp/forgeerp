"""Module loader service"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from forgeerp.core.database.models.module import Module, ClientModule


class ModuleLoader:
    """Service for loading and managing modules"""
    
    def __init__(self, addons_dir: Optional[Path] = None):
        self.addons_dir = Path(addons_dir) if addons_dir else Path(__file__).parent.parent.parent.parent.parent / "backend" / "addons"
    
    def load_module_manifest(self, module_name: str) -> Dict[str, Any]:
        """Load module manifest (manifest.yaml)"""
        module_path = self.addons_dir / module_name
        manifest_path = module_path / "manifest.yaml"
        
        if not manifest_path.exists():
            raise FileNotFoundError(f"Module {module_name} not found or manifest.yaml missing")
        
        with open(manifest_path, "r") as f:
            manifest = yaml.safe_load(f)
        
        return manifest
    
    def get_available_modules(self) -> List[str]:
        """Get list of available modules"""
        if not self.addons_dir.exists():
            return []
        
        modules = []
        for item in self.addons_dir.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                manifest_path = item / "manifest.yaml"
                if manifest_path.exists():
                    modules.append(item.name)
        
        return modules
    
    def get_module_dependencies(self, module_name: str) -> List[str]:
        """Get module dependencies"""
        try:
            manifest = self.load_module_manifest(module_name)
            return manifest.get("depends", [])
        except Exception:
            return []
    
    def install_module_in_database(
        self,
        session: Session,
        module_name: str,
        client_id: Optional[int] = None
    ) -> Module:
        """Install module in database"""
        # Check if module already exists
        statement = select(Module).where(Module.name == module_name)
        existing_module = session.exec(statement).first()
        
        if existing_module:
            return existing_module
        
        # Load manifest
        manifest = self.load_module_manifest(module_name)
        
        # Create module
        module = Module(
            name=module_name,
            display_name=manifest.get("name", module_name),
            description=manifest.get("description"),
            category=manifest.get("category", "addon"),
            depends_on=str(manifest.get("depends", [])) if manifest.get("depends") else None,
            is_active=True,
            is_installed=True
        )
        
        session.add(module)
        session.commit()
        session.refresh(module)
        
        # If client_id provided, install for client
        if client_id:
            client_module = ClientModule(
                client_id=client_id,
                module_id=module.id,
                is_active=True
            )
            session.add(client_module)
            session.commit()
        
        return module
    
    def get_installed_modules_for_client(
        self,
        session: Session,
        client_id: int
    ) -> List[Module]:
        """Get installed modules for a client"""
        statement = select(ClientModule).where(
            ClientModule.client_id == client_id,
            ClientModule.is_active == True
        )
        client_modules = session.exec(statement).all()
        
        modules = []
        for cm in client_modules:
            module = session.get(Module, cm.module_id)
            if module:
                modules.append(module)
        
        return modules

