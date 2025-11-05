"""E2E tests for login"""

from tests.e2e.utils import wait_for_react, wait_for_navigation_complete

import pytest
from playwright.sync_api import Page, expect


def test_login_page_loads(clean_page: Page):
    """Test that login page loads correctly"""
    expect(clean_page.locator("h1")).to_contain_text("ForgeERP")
    expect(clean_page.locator('input[type="text"]')).to_be_visible()
    expect(clean_page.locator('input[type="password"]')).to_be_visible()
    expect(clean_page.locator('button[type="submit"]')).to_be_visible()


def test_login_success(clean_page: Page):
    """Test successful login"""
    # Fill login form
    clean_page.fill('input[type="text"]', "admin")
    clean_page.fill('input[type="password"]', "admin")
    
    # Submit form
    clean_page.click('button[type="submit"]')
    
    # Wait for redirect to dashboard
    clean_page.wait_for_url("**/", timeout=5000)
    
    # Check if we're on dashboard (not login page)
    expect(clean_page.locator("text=Dashboard")).to_be_visible(timeout=5000)


def test_login_invalid_credentials(clean_page: Page):
    """Test login with invalid credentials"""
    # Fill login form with wrong credentials
    clean_page.fill('input[type="text"]', "wrong")
    clean_page.fill('input[type="password"]', "wrong")
    
    # Submit form
    clean_page.click('button[type="submit"]')
    
    # Wait for error message
    expect(clean_page.locator("text=/Incorrect|error|failed/i")).to_be_visible(timeout=3000)
    
    # Should still be on login page
    expect(clean_page.locator("h1")).to_contain_text("ForgeERP")


def test_login_empty_fields(clean_page: Page):
    """Test login with empty fields"""
    # Try to submit without filling
    clean_page.click('button[type="submit"]')
    
    # HTML5 validation should prevent submission
    # Or form should show validation errors
    expect(clean_page.locator('input[type="text"]:invalid')).to_have_count(
        1, timeout=1000
    ).or_(expect(clean_page.locator('input[type="password"]:invalid')).to_have_count(1))

