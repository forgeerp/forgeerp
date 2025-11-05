"""Templates for GitHub Actions workflows"""

# Template base para setup-client.yml
SETUP_CLIENT_WORKFLOW_TEMPLATE = """
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
          # TODO: Add actual setup steps based on installed modules
"""

# Template base para deploy-client.yml
DEPLOY_CLIENT_WORKFLOW_TEMPLATE = """
name: Deploy Client

on:
  push:
    paths:
      - 'clients/**/values-*.yaml'
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
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Deploy
        run: |
          echo "Deploying client ${{ inputs.client_name }}"
          echo "Environment: ${{ inputs.environment }}"
          # TODO: Add actual deploy steps based on installed modules
"""

# Template base para disaster-recovery.yml
DISASTER_RECOVERY_WORKFLOW_TEMPLATE = """
name: Disaster Recovery

on:
  workflow_dispatch:
    inputs:
      action:
        description: 'Recovery action'
        required: true
        type: choice
        options:
          - provision
          - restore
          - rebuild

jobs:
  disaster-recovery:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Disaster Recovery
        run: |
          echo "Executing disaster recovery: ${{ inputs.action }}"
          # TODO: Add actual disaster recovery steps
"""

# Template base para diagnose-services.yml
DIAGNOSE_SERVICES_WORKFLOW_TEMPLATE = """
name: Diagnose Services

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  diagnose:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Diagnose Services
        run: |
          echo "Diagnosing services..."
          # TODO: Add actual diagnosis steps
"""

# Template base para fix-common-issues.yml
FIX_COMMON_ISSUES_WORKFLOW_TEMPLATE = """
name: Fix Common Issues

on:
  workflow_dispatch:
    inputs:
      auto_approve:
        description: 'Auto approve for production'
        required: false
        type: boolean
        default: false

jobs:
  fix:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Fix Common Issues
        run: |
          echo "Fixing common issues..."
          # TODO: Add actual fix steps
"""

