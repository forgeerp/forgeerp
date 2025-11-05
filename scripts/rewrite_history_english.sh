#!/bin/bash
# Script to rewrite git history to a single English commit

set -e

echo "🔄 Rewriting git history to single MVP commit in English..."

# Get the first commit hash
FIRST_COMMIT=$(git rev-list --max-parents=0 HEAD)

# Create orphan branch
git checkout --orphan temp_branch

# Add all files
git add -A

# Create single commit in English
git commit -m "🚀 Initial MVP - ForgeERP Infrastructure Management System

A lightweight infrastructure management platform for Odoo partners.

Features:
- Client management (CRUD)
- Module installation system
- GitHub Actions workflow generation
- Unified Docker image deployment
- React frontend with i18n support
- FastAPI backend with SQLite
- E2E testing with Playwright
- Automated documentation generation

Tech Stack:
- Frontend: React 19 + TypeScript + Vite + Tailwind CSS
- Backend: FastAPI + SQLModel + SQLite
- CLI: Typer + Rich
- Testing: Pytest + Playwright
- Containerization: Docker (unified image)"

# Delete old main branch
git branch -D main

# Rename temp branch to main
git branch -m main

echo "✅ History rewritten successfully!"
echo "⚠️  Next step: Force push with 'git push --force origin main'"

