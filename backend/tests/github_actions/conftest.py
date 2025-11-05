"""Fixtures for GitHub Actions tests"""

import pytest
import os
import tempfile
import shutil
from pathlib import Path
import subprocess


@pytest.fixture(name="github_repo_dir")
def github_repo_dir_fixture():
    """Create a temporary GitHub repository directory"""
    temp_dir = tempfile.mkdtemp()
    repo_path = Path(temp_dir) / "test-repo"
    repo_path.mkdir(parents=True)
    
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=repo_path,
        check=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=repo_path,
        check=True
    )
    
    yield repo_path
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture(name="github_workflows_dir")
def github_workflows_dir_fixture(github_repo_dir):
    """Create .github/workflows directory"""
    workflows_dir = github_repo_dir / ".github" / "workflows"
    workflows_dir.mkdir(parents=True)
    return workflows_dir


@pytest.fixture(name="github_actions_dir")
def github_actions_dir_fixture(github_repo_dir):
    """Create .github/actions directory"""
    actions_dir = github_repo_dir / ".github" / "actions"
    actions_dir.mkdir(parents=True)
    return actions_dir


@pytest.fixture(name="act_available")
def act_available_fixture():
    """Check if act is available"""
    try:
        result = subprocess.run(
            ["act", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


@pytest.fixture(name="act_runner")
def act_runner_fixture(github_repo_dir, act_available):
    """Create act runner helper"""
    if not act_available:
        pytest.skip("act is not available - install with: brew install act")
    
    class ActRunner:
        def __init__(self, repo_dir):
            self.repo_dir = repo_dir
        
        def run_workflow(self, workflow_name, event="workflow_dispatch", **kwargs):
            """Run a workflow using act"""
            workflow_path = self.repo_dir / ".github" / "workflows" / workflow_name
            cmd = ["act", "-W", str(workflow_path)]
            
            if event != "workflow_dispatch":
                cmd.extend(["-e", event])
            
            # Add secrets if provided
            if "secrets" in kwargs:
                for key, value in kwargs["secrets"].items():
                    cmd.extend(["-s", f"{key}={value}"])
            
            # Add environment variables if provided
            if "env" in kwargs:
                for key, value in kwargs["env"].items():
                    cmd.extend(["-e", f"{key}={value}"])
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
        
        def validate_workflow(self, workflow_name):
            """Validate workflow syntax"""
            workflow_path = self.repo_dir / ".github" / "workflows" / workflow_name
            if not workflow_path.exists():
                return False
            
            # Try to parse YAML
            try:
                import yaml
                with open(workflow_path, "r") as f:
                    yaml.safe_load(f)
                return True
            except Exception:
                return False
    
    return ActRunner(github_repo_dir)

