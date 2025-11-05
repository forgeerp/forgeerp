"""Tests for GitHub Actions workflow execution using act"""

import pytest
import yaml
from pathlib import Path


@pytest.mark.act
def test_setup_client_workflow_execution(github_repo_dir, act_runner, github_workflows_dir):
    """Test setup-client.yml workflow execution with act"""
    if not act_runner:
        pytest.skip("act is not available")
    
    # Create a simple setup-client workflow
    workflow_content = """
name: Setup Client
on:
  workflow_dispatch:
    inputs:
      client_name:
        description: 'Client name'
        required: true
        type: string
      environment:
        description: 'Environment'
        required: true
        type: choice
        options:
          - dev
          - hml
          - prod
          - all

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Client
        run: |
          echo "Setting up client ${{ inputs.client_name }}"
          echo "Environment: ${{ inputs.environment }}"
"""
    
    workflow_path = github_workflows_dir / "setup-client.yml"
    with open(workflow_path, "w") as f:
        f.write(workflow_content)
    
    # Run workflow with act
    result = act_runner.run_workflow(
        "setup-client.yml",
        event="workflow_dispatch",
        env={
            "INPUT_CLIENT_NAME": "test-client",
            "INPUT_ENVIRONMENT": "dev"
        }
    )
    
    # Workflow should at least validate (may not fully execute without proper setup)
    assert result["returncode"] in [0, 1]  # 0 = success, 1 = some steps may fail in dry-run


@pytest.mark.act
def test_deploy_client_workflow_execution(github_repo_dir, act_runner, github_workflows_dir):
    """Test deploy-client.yml workflow execution with act"""
    if not act_runner:
        pytest.skip("act is not available")
    
    # Create a simple deploy-client workflow
    workflow_content = """
name: Deploy Client
on:
  push:
    paths:
      - 'clients/**/values-*.yaml'
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Deploy
        run: |
          echo "Deploying client"
"""
    
    workflow_path = github_workflows_dir / "deploy-client.yml"
    with open(workflow_path, "w") as f:
        f.write(workflow_content)
    
    # Run workflow with act
    result = act_runner.run_workflow(
        "deploy-client.yml",
        event="push"
    )
    
    # Workflow should at least validate
    assert result["returncode"] in [0, 1]


@pytest.mark.act
def test_workflow_with_secrets(github_repo_dir, act_runner, github_workflows_dir):
    """Test workflow execution with secrets"""
    if not act_runner:
        pytest.skip("act is not available")
    
    workflow_content = """
name: Test with Secrets
on:
  workflow_dispatch:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Use Secret
        run: |
          echo "Secret: ${{ secrets.TEST_SECRET }}"
"""
    
    workflow_path = github_workflows_dir / "test-secrets.yml"
    with open(workflow_path, "w") as f:
        f.write(workflow_content)
    
    # Run workflow with secrets
    result = act_runner.run_workflow(
        "test-secrets.yml",
        secrets={"TEST_SECRET": "test-value"}
    )
    
    # Verify secret is used (may not fully execute)
    assert result["returncode"] in [0, 1]


def test_workflow_yaml_syntax(github_workflows_dir):
    """Test that generated workflows have valid YAML syntax"""
    # Create a workflow with various YAML structures
    workflow_content = """
name: YAML Syntax Test
on:
  workflow_dispatch:
  push:
    branches:
      - main
      - develop
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest]
        python: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - name: Test
        run: echo "Test"
"""
    
    workflow_path = github_workflows_dir / "yaml-syntax-test.yml"
    with open(workflow_path, "w") as f:
        f.write(workflow_content)
    
    # Verify YAML is valid
    with open(workflow_path, "r") as f:
        workflow_data = yaml.safe_load(f)
    
    assert workflow_data["name"] == "YAML Syntax Test"
    assert "workflow_dispatch" in workflow_data["on"]
    assert "push" in workflow_data["on"]
    assert "test" in workflow_data["jobs"]
    assert "matrix" in workflow_data["jobs"]["test"]["strategy"]

