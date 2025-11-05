"""Tests for GitHub Actions workflow generation"""

import pytest
from pathlib import Path
import yaml
from forgeerp.core.engine.github_generator.workflows import GitHubWorkflowGenerator


def test_workflow_generation_basic(github_workflows_dir, github_repo_dir):
    """Test basic workflow generation"""
    generator = GitHubWorkflowGenerator(github_repo_dir)
    
    workflow_data = {
        "name": "Test Workflow",
        "on": {
            "workflow_dispatch": {}
        },
        "jobs": {
            "test": {
                "runs-on": "ubuntu-latest",
                "steps": [
                    {"uses": "actions/checkout@v4"},
                    {"run": "echo 'Hello World'"}
                ]
            }
        }
    }
    
    workflow_name = "test-workflow.yml"
    generator.generate_workflow(workflow_name, workflow_data)
    
    # Verify workflow file exists
    workflow_path = github_workflows_dir / workflow_name
    assert workflow_path.exists()
    
    # Verify workflow is valid YAML
    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)
    
    assert workflow_content["name"] == "Test Workflow"
    assert "jobs" in workflow_content
    assert "test" in workflow_content["jobs"]


def test_workflow_generation_with_template(github_workflows_dir, github_repo_dir):
    """Test workflow generation using Jinja2 template"""
    generator = GitHubWorkflowGenerator(github_repo_dir)
    
    template = """
name: {{ workflow_name }}
on:
  workflow_dispatch:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "{{ message }}"
"""
    
    workflow_name = "template-workflow.yml"
    context = {
        "workflow_name": "Template Workflow",
        "message": "Hello from template"
    }
    
    generator.generate_workflow_from_template(
        workflow_name,
        template,
        context
    )
    
    # Verify workflow file exists
    workflow_path = github_workflows_dir / workflow_name
    assert workflow_path.exists()
    
    # Verify workflow content
    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)
    
    assert workflow_content["name"] == "Template Workflow"
    assert "test" in workflow_content["jobs"]


def test_workflow_syntax_validation(github_workflows_dir, github_repo_dir, act_runner):
    """Test workflow syntax validation using act"""
    if not act_runner:
        pytest.skip("act is not available")
    
    # Generate a simple workflow
    workflow_content = """
name: Test Workflow
on:
  workflow_dispatch:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Test"
"""
    
    workflow_path = github_workflows_dir / "test-workflow.yml"
    with open(workflow_path, "w") as f:
        f.write(workflow_content)
    
    # Validate workflow syntax
    assert act_runner.validate_workflow("test-workflow.yml")


def test_setup_client_workflow_generation(github_workflows_dir, github_repo_dir):
    """Test setup-client.yml workflow generation"""
    generator = GitHubWorkflowGenerator(github_repo_dir)
    
    client_data = {
        "client_name": "test-client",
        "environments": ["dev", "hml", "prod"]
    }
    
    workflow_name = "setup-client.yml"
    generator.generate_setup_client_workflow(client_data)
    
    # Verify workflow file exists
    workflow_path = github_workflows_dir / workflow_name
    assert workflow_path.exists()
    
    # Verify workflow content
    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)
    
    assert "workflow_dispatch" in workflow_content.get("on", {})
    assert "jobs" in workflow_content


def test_deploy_client_workflow_generation(github_workflows_dir, github_repo_dir):
    """Test deploy-client.yml workflow generation"""
    generator = GitHubWorkflowGenerator(github_repo_dir)
    
    client_data = {
        "client_name": "test-client",
        "environments": ["dev", "hml", "prod"]
    }
    
    workflow_name = "deploy-client.yml"
    generator.generate_deploy_client_workflow(client_data)
    
    # Verify workflow file exists
    workflow_path = github_workflows_dir / workflow_name
    assert workflow_path.exists()
    
    # Verify workflow content
    with open(workflow_path, "r") as f:
        workflow_content = yaml.safe_load(f)
    
    assert "push" in workflow_content.get("on", {})
    assert "jobs" in workflow_content

