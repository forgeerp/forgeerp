.PHONY: test test-unit test-integration test-coverage install-dev clean

# Run all tests
test:
	pytest

# Run unit tests only
test-unit:
	pytest tests/unit -v

# Run integration tests only
test-integration:
	pytest tests/integration -v

# Run tests with coverage
test-coverage:
	pytest --cov=forgeerp --cov-report=html --cov-report=term

# Run GitHub Actions tests (requires act)
test-github-actions:
	pytest tests/github_actions/ -m "not act"

# Run GitHub Actions tests with act (requires act installed)
test-github-actions-act:
	pytest tests/github_actions/ -m act

# Check if act is installed
check-act:
	@which act > /dev/null && echo "act is installed" || echo "act is not installed - install with: brew install act"

# Run E2E tests (requires frontend running)
test-e2e:
	pytest tests/e2e/ -v

# Run E2E tests with headed browser (see browser)
test-e2e-headed:
	pytest tests/e2e/ --headed -v

# Install Playwright browsers
install-playwright:
	playwright install chromium

# Check if Playwright is installed
check-playwright:
	@python -c "import playwright" 2>/dev/null && echo "Playwright is installed" || echo "Playwright is not installed - install with: pip install playwright && playwright install"

# Generate visual documentation from E2E tests
docs-e2e:
	pytest tests/e2e/test_guia_completo.py --generate-docs -v

# Generate all documentation (internal use)
docs-all: docs-e2e

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-asyncio pytest-cov

# Clean test artifacts
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete

