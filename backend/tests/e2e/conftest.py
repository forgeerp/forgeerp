"""E2E test fixtures"""

import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from playwright.async_api import async_playwright
import os
import time

# Import React wait utilities
from tests.e2e.utils import wait_for_react, wait_for_navigation_complete


# Pytest hook para adicionar opção --generate-docs
def pytest_addoption(parser):
    """Add custom pytest options"""
    parser.addoption(
        "--generate-docs",
        action="store_true",
        default=False,
        help="Generate visual documentation from tests"
    )


@pytest.fixture
def docs_output_dir(request):
    """Output directory for generated documentation"""
    from pathlib import Path
    output_dir = Path("docs/operacional/screenshots")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


@pytest.fixture
def should_generate_docs(request):
    """Check if documentation should be generated"""
    return request.config.getoption("--generate-docs")


@pytest.fixture(scope="session")
def frontend_url():
    """Frontend URL - defaults to unified image port 8000"""
    return os.getenv("FRONTEND_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def api_url():
    """API URL"""
    return os.getenv("API_URL", "http://localhost:8000")


@pytest.fixture(scope="session")
def page(browser: Browser, frontend_url: str) -> Page:
    """Create a new page for testing"""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    page = context.new_page()
    page.goto(frontend_url)
    wait_for_react(page)  # Wait for React after initial load
    yield page
    context.close()


@pytest.fixture(scope="function")
def authenticated_page(page: Page, frontend_url: str, api_url: str):
    """Page with authenticated user"""
    # Login via API first
    import requests
    
    login_response = requests.post(
        f"{api_url}/api/v1/auth/login",
        json={"username": "admin", "password": "admin"}
    )
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        # Set token in localStorage
        page.goto(frontend_url)
        page.evaluate(f"localStorage.setItem('token', '{token}')")
        page.reload()
        wait_for_react(page)  # Wait for React after reload
    else:
        # Fallback: login via UI
        page.goto(frontend_url)
        wait_for_react(page)  # Wait for React before interacting
        page.fill('input[type="text"]', "admin")
        page.fill('input[type="password"]', "admin")
        page.click('button[type="submit"]')
        wait_for_navigation_complete(page)  # Wait for navigation and React
    
    yield page


@pytest.fixture(scope="function")
def clean_page(page: Page, frontend_url: str):
    """Clean page (not authenticated)"""
    page.goto(frontend_url)
    wait_for_react(page)  # Wait for React after navigation
    page.evaluate("localStorage.clear()")
    page.reload()
    wait_for_react(page)  # Wait for React after reload
    yield page

