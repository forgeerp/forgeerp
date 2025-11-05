"""GitHub routes - PRs and workflow generation"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from forgeerp.core.database.database import get_session
from forgeerp.core.database.models.user import User
from forgeerp.core.database.models.client import Client
from forgeerp.core.database.models.module import Module, ClientModule
from forgeerp.core.database.models.permission import PullRequest
from forgeerp.core.api.routes.auth import get_current_user_dependency as get_current_user
from forgeerp.core.services.authentication import check_permission
from forgeerp.core.services.github_service import GitHubService
from forgeerp.core.engine.github_generator.workflows import GitHubWorkflowGenerator
from pydantic import BaseModel
import os

router = APIRouter(prefix="/github", tags=["github"])


class GenerateWorkflowsRequest(BaseModel):
    """Schema for generating workflows"""
    client_id: int
    repo_dir: Optional[str] = None


class CreatePRRequest(BaseModel):
    """Schema for creating a PR"""
    title: str
    body: str
    head: str
    base: str = "main"
    change_type: str
    change_target: Optional[str] = None
    change_data: Optional[dict] = None


@router.post("/workflows/generate")
async def generate_workflows(
    request: GenerateWorkflowsRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Generate GitHub Actions workflows for a client"""
    # Check permission
    if not check_permission(current_user, "workflow_generate", client_id=request.client_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get client
    client = session.get(Client, request.client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    
    # Get installed modules for client
    statement = select(ClientModule).where(ClientModule.client_id == request.client_id)
    client_modules = session.exec(statement).all()
    
    installed_modules = []
    for cm in client_modules:
        module = session.get(Module, cm.module_id)
        if module:
            installed_modules.append(module.name)
    
    # Generate workflows
    repo_dir = request.repo_dir or os.getenv("GITHUB_REPO_DIR", "/tmp/test-repo")
    generator = GitHubWorkflowGenerator(repo_dir)
    
    client_data = {
        "client_name": client.code,
        "environments": ["dev", "hml", "prod"]
    }
    
    generator.generate_workflows_for_client(client_data, installed_modules)
    
    return {
        "message": "Workflows generated successfully",
        "client_id": request.client_id,
        "installed_modules": installed_modules,
        "workflows": [
            "setup-client.yml",
            "deploy-client.yml",
            "diagnose-services.yml",
            "fix-common-issues.yml"
        ]
    }


@router.post("/prs/create")
async def create_pull_request(
    request: CreatePRRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Create a pull request for a grave change"""
    # Check permission
    if not check_permission(current_user, "pr_create"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get GitHub service
    github_service = GitHubService()
    
    owner = os.getenv("GITHUB_OWNER", "forgeerp")
    repo = os.getenv("GITHUB_REPO", "forgeerp")
    
    try:
        # Create PR
        pr = github_service.create_pull_request(
            owner=owner,
            repo=repo,
            title=request.title,
            body=request.body,
            head=request.head,
            base=request.base
        )
        
        # Save PR to database
        pr_model = PullRequest(
            github_pr_number=pr.number,
            github_pr_url=pr.html_url,
            title=request.title,
            description=request.body,
            status="open",
            change_type=request.change_type,
            change_target=request.change_target,
            change_data=str(request.change_data) if request.change_data else None
        )
        
        session.add(pr_model)
        session.commit()
        session.refresh(pr_model)
        
        return {
            "message": "Pull request created successfully",
            "pr_number": pr.number,
            "pr_url": pr.html_url,
            "id": pr_model.id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create pull request: {str(e)}"
        )


@router.get("/prs/{pr_number}/status")
async def get_pr_status(
    pr_number: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """Get pull request status and approvals"""
    # Get PR from database
    statement = select(PullRequest).where(PullRequest.github_pr_number == pr_number)
    pr_model = session.exec(statement).first()
    
    if not pr_model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pull request not found"
        )
    
    # Sync with GitHub
    github_service = GitHubService()
    owner = os.getenv("GITHUB_OWNER", "forgeerp")
    repo = os.getenv("GITHUB_REPO", "forgeerp")
    
    try:
        # Sync PR from GitHub
        pr_model = github_service.sync_pull_request_to_database(
            session,
            owner,
            repo,
            pr_number
        )
        
        # Get reviews
        reviews = github_service.get_pull_request_reviews(owner, repo, pr_number)
        
        return {
            "pr_number": pr_model.github_pr_number,
            "status": pr_model.status,
            "is_approved": pr_model.is_approved,
            "is_merged": pr_model.is_merged,
            "reviews": reviews,
            "change_type": pr_model.change_type,
            "change_target": pr_model.change_target
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get PR status: {str(e)}"
        )


@router.get("/prs")
async def list_pull_requests(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """List pull requests"""
    statement = select(PullRequest)
    
    if status:
        statement = statement.where(PullRequest.status == status)
    
    prs = session.exec(statement.offset(skip).limit(limit)).all()
    
    return {
        "prs": [
            {
                "id": pr.id,
                "pr_number": pr.github_pr_number,
                "pr_url": pr.github_pr_url,
                "title": pr.title,
                "status": pr.status,
                "is_approved": pr.is_approved,
                "is_merged": pr.is_merged,
                "change_type": pr.change_type
            }
            for pr in prs
        ],
        "total": len(prs)
    }

