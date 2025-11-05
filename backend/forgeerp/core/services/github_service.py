"""GitHub service for PRs and permissions"""

import os
from typing import Optional, Dict, Any, List
from github import Github
from github.Repository import Repository
from github.PullRequest import PullRequest
from forgeerp.core.database.models.permission import PullRequest as PRModel
from forgeerp.core.database.models.permission import PullRequestApproval
from sqlmodel import Session, select


class GitHubService:
    """Service for GitHub API operations"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is required")
        self.github = Github(self.token)
    
    def get_repository(self, owner: str, repo: str) -> Repository:
        """Get a GitHub repository"""
        return self.github.get_repo(f"{owner}/{repo}")
    
    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str = "main"
    ) -> PullRequest:
        """Create a pull request"""
        repository = self.get_repository(owner, repo)
        pr = repository.create_pull(
            title=title,
            body=body,
            head=head,
            base=base
        )
        return pr
    
    def get_pull_request(
        self,
        owner: str,
        repo: str,
        pr_number: int
    ) -> PullRequest:
        """Get a pull request by number"""
        repository = self.get_repository(owner, repo)
        return repository.get_pull(pr_number)
    
    def is_pull_request_approved(
        self,
        owner: str,
        repo: str,
        pr_number: int,
        required_approvals: int = 1
    ) -> bool:
        """Check if a pull request has required approvals"""
        pr = self.get_pull_request(owner, repo, pr_number)
        reviews = pr.get_reviews()
        
        approvals = 0
        for review in reviews:
            if review.state == "APPROVED":
                approvals += 1
        
        return approvals >= required_approvals
    
    def get_pull_request_reviews(
        self,
        owner: str,
        repo: str,
        pr_number: int
    ) -> List[Dict[str, Any]]:
        """Get pull request reviews"""
        pr = self.get_pull_request(owner, repo, pr_number)
        reviews = pr.get_reviews()
        
        return [
            {
                "id": review.id,
                "user": review.user.login,
                "state": review.state,
                "body": review.body,
                "submitted_at": review.submitted_at.isoformat() if review.submitted_at else None
            }
            for review in reviews
        ]
    
    def sync_pull_request_to_database(
        self,
        session: Session,
        owner: str,
        repo: str,
        pr_number: int
    ) -> PRModel:
        """Sync pull request from GitHub to database"""
        pr = self.get_pull_request(owner, repo, pr_number)
        
        # Check if PR already exists in database
        statement = select(PRModel).where(PRModel.github_pr_number == pr_number)
        existing_pr = session.exec(statement).first()
        
        if existing_pr:
            # Update existing PR
            existing_pr.status = "open" if pr.state == "open" else "closed"
            existing_pr.is_approved = self.is_pull_request_approved(owner, repo, pr_number)
            existing_pr.is_merged = pr.merged
            if pr.merged_at:
                existing_pr.merged_at = pr.merged_at
            if pr.closed_at:
                existing_pr.closed_at = pr.closed_at
            
            session.add(existing_pr)
            session.commit()
            session.refresh(existing_pr)
            
            return existing_pr
        
        # Create new PR in database
        pr_model = PRModel(
            github_pr_number=pr.number,
            github_pr_url=pr.html_url,
            title=pr.title,
            description=pr.body,
            status="open" if pr.state == "open" else "closed",
            is_approved=self.is_pull_request_approved(owner, repo, pr_number),
            is_merged=pr.merged,
            merged_at=pr.merged_at,
            closed_at=pr.closed_at
        )
        
        session.add(pr_model)
        session.commit()
        session.refresh(pr_model)
        
        return pr_model
    
    def check_user_permission(
        self,
        owner: str,
        repo: str,
        username: str,
        permission: str = "write"
    ) -> bool:
        """Check if user has permission in repository"""
        repository = self.get_repository(owner, repo)
        
        try:
            collaborator = repository.get_collaborator_permission(username)
            return collaborator in ["write", "admin", "maintain"]
        except Exception:
            return False

