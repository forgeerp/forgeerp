"""GitHub Workflows generator"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from jinja2 import Template
from forgeerp.core.engine.github_generator.templates import (
    SETUP_CLIENT_WORKFLOW_TEMPLATE,
    DEPLOY_CLIENT_WORKFLOW_TEMPLATE,
    DISASTER_RECOVERY_WORKFLOW_TEMPLATE,
    DIAGNOSE_SERVICES_WORKFLOW_TEMPLATE,
    FIX_COMMON_ISSUES_WORKFLOW_TEMPLATE,
)


class GitHubWorkflowGenerator:
    """Generator for GitHub Actions workflows"""
    
    def __init__(self, repo_dir: Path):
        self.repo_dir = Path(repo_dir)
        self.workflows_dir = self.repo_dir / ".github" / "workflows"
        self.workflows_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_workflow(self, workflow_name: str, workflow_data: Dict[str, Any]):
        """Generate a workflow from data dictionary"""
        workflow_path = self.workflows_dir / workflow_name
        
        with open(workflow_path, "w") as f:
            yaml.dump(workflow_data, f, default_flow_style=False, sort_keys=False)
    
    def generate_workflow_from_template(self, workflow_name: str, template: str, context: Dict[str, Any]):
        """Generate a workflow from Jinja2 template"""
        workflow_path = self.workflows_dir / workflow_name
        
        jinja_template = Template(template)
        workflow_content = jinja_template.render(**context)
        
        with open(workflow_path, "w") as f:
            f.write(workflow_content)
    
    def generate_setup_client_workflow(self, client_data: Dict[str, Any]):
        """Generate setup-client.yml workflow"""
        workflow_name = "setup-client.yml"
        
        workflow_data = {
            "name": "Setup Client",
            "on": {
                "workflow_dispatch": {
                    "inputs": {
                        "client_name": {
                            "description": "Client name",
                            "required": True,
                            "type": "string"
                        },
                        "environment": {
                            "description": "Environment",
                            "required": True,
                            "type": "choice",
                            "options": client_data.get("environments", ["dev", "hml", "prod", "all"])
                        }
                    }
                }
            },
            "jobs": {
                "setup": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"name": "Setup Client", "run": "echo 'Setting up client'"}
                    ]
                }
            }
        }
        
        self.generate_workflow(workflow_name, workflow_data)
    
    def generate_deploy_client_workflow(self, client_data: Dict[str, Any]):
        """Generate deploy-client.yml workflow"""
        workflow_name = "deploy-client.yml"
        
        workflow_data = {
            "name": "Deploy Client",
            "on": {
                "push": {
                    "paths": ["clients/**/values-*.yaml"]
                },
                "workflow_dispatch": {}
            },
            "jobs": {
                "deploy": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v4"},
                        {"name": "Deploy", "run": "echo 'Deploying client'"}
                    ]
                }
            }
        }
        
        self.generate_workflow(workflow_name, workflow_data)
    
    def generate_workflows_for_client(
        self,
        client_data: Dict[str, Any],
        installed_modules: Optional[List[str]] = None
    ):
        """Generate all workflows for a client based on installed modules"""
        installed_modules = installed_modules or []
        
        # Always generate setup and deploy workflows
        self.generate_setup_client_workflow(client_data)
        self.generate_deploy_client_workflow(client_data)
        
        # Generate workflows based on installed modules
        if "hetzner" in installed_modules:
            self.generate_disaster_recovery_workflow()
        
        # Always generate diagnosis and fix workflows
        self.generate_diagnose_services_workflow()
        self.generate_fix_common_issues_workflow()
    
    def generate_disaster_recovery_workflow(self):
        """Generate disaster-recovery.yml workflow"""
        workflow_name = "disaster-recovery.yml"
        template = Template(DISASTER_RECOVERY_WORKFLOW_TEMPLATE)
        workflow_content = template.render()
        
        workflow_path = self.workflows_dir / workflow_name
        with open(workflow_path, "w") as f:
            f.write(workflow_content)
    
    def generate_diagnose_services_workflow(self):
        """Generate diagnose-services.yml workflow"""
        workflow_name = "diagnose-services.yml"
        template = Template(DIAGNOSE_SERVICES_WORKFLOW_TEMPLATE)
        workflow_content = template.render()
        
        workflow_path = self.workflows_dir / workflow_name
        with open(workflow_path, "w") as f:
            f.write(workflow_content)
    
    def generate_fix_common_issues_workflow(self):
        """Generate fix-common-issues.yml workflow"""
        workflow_name = "fix-common-issues.yml"
        template = Template(FIX_COMMON_ISSUES_WORKFLOW_TEMPLATE)
        workflow_content = template.render()
        
        workflow_path = self.workflows_dir / workflow_name
        with open(workflow_path, "w") as f:
            f.write(workflow_content)


class GitHubActionGenerator:
    """Generator for GitHub Actions reusable actions"""
    
    def __init__(self, repo_dir: Path):
        self.repo_dir = Path(repo_dir)
        self.actions_dir = self.repo_dir / ".github" / "actions"
        self.actions_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_action(self, action_name: str, action_data: Dict[str, Any]):
        """Generate a reusable action"""
        action_dir = self.actions_dir / action_name
        action_dir.mkdir(parents=True, exist_ok=True)
        
        action_path = action_dir / "action.yml"
        
        with open(action_path, "w") as f:
            yaml.dump(action_data, f, default_flow_style=False, sort_keys=False)

