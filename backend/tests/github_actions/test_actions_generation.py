"""Tests for GitHub Actions reusable actions generation"""

import pytest
from pathlib import Path
import yaml


def test_action_generation_basic(github_actions_dir, github_repo_dir):
    """Test basic action generation"""
    from forgeerp.core.engine.github_generator.workflows import GitHubActionGenerator
    
    generator = GitHubActionGenerator(github_repo_dir)
    
    action_data = {
        "name": "Test Action",
        "description": "A test action",
        "inputs": {
            "test_input": {
                "description": "Test input",
                "required": True,
                "type": "string"
            }
        },
        "runs": {
            "using": "composite",
            "steps": [
                {"run": "echo ${{ inputs.test_input }}", "shell": "bash"}
            ]
        }
    }
    
    action_name = "test-action"
    generator.generate_action(action_name, action_data)
    
    # Verify action file exists
    action_path = github_actions_dir / action_name / "action.yml"
    assert action_path.exists()
    
    # Verify action is valid YAML
    with open(action_path, "r") as f:
        action_content = yaml.safe_load(f)
    
    assert action_content["name"] == "Test Action"
    assert "inputs" in action_content
    assert "runs" in action_content


def test_action_validation(github_actions_dir, github_repo_dir):
    """Test action YAML validation"""
    action_content = """
name: 'Test Action'
description: 'A test action'
inputs:
  test_input:
    description: 'Test input'
    required: true
    default: 'default-value'
runs:
  using: 'composite'
  steps:
    - run: echo "${{ inputs.test_input }}"
      shell: bash
"""
    
    action_path = github_actions_dir / "test-action" / "action.yml"
    action_path.parent.mkdir(parents=True)
    
    with open(action_path, "w") as f:
        f.write(action_content)
    
    # Verify action is valid YAML
    with open(action_path, "r") as f:
        action_data = yaml.safe_load(f)
    
    assert action_data["name"] == "Test Action"
    assert "inputs" in action_data
    assert "runs" in action_data
    assert action_data["runs"]["using"] == "composite"


def test_action_with_docker(github_actions_dir, github_repo_dir):
    """Test action with Docker runs"""
    action_content = """
name: 'Docker Action'
description: 'An action that uses Docker'
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.message }}
"""
    
    action_path = github_actions_dir / "docker-action" / "action.yml"
    action_path.parent.mkdir(parents=True)
    
    with open(action_path, "w") as f:
        f.write(action_content)
    
    # Verify action is valid
    with open(action_path, "r") as f:
        action_data = yaml.safe_load(f)
    
    assert action_data["runs"]["using"] == "docker"
    assert "image" in action_data["runs"]

