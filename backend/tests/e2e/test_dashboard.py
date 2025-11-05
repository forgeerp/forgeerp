"""E2E tests for dashboard"""

import pytest
from playwright.sync_api import Page, expect


def test_dashboard_loads(authenticated_page: Page):
    """Test that dashboard loads correctly"""
    # Wait for dashboard to load
    authenticated_page.wait_for_load_state("networkidle")
    
    # Check if dashboard elements are visible
    expect(authenticated_page.locator("text=Dashboard")).to_be_visible()
    expect(authenticated_page.locator("text=Clientes")).to_be_visible()
    expect(authenticated_page.locator("text=Usuário")).to_be_visible()
    expect(authenticated_page.locator("text=Status")).to_be_visible()


def test_dashboard_navigation(authenticated_page: Page):
    """Test navigation between tabs"""
    # Check if we're on dashboard
    expect(authenticated_page.locator("text=Dashboard").locator("..")).to_have_class(
        /border-blue-500/, timeout=5000
    )
    
    # Click on Configurations tab
    authenticated_page.click("text=Configurações")
    
    # Check if configurations tab is active
    expect(authenticated_page.locator("text=Configurações").locator("..")).to_have_class(
        /border-blue-500/, timeout=3000
    )
    
    # Check if configurations page loaded
    expect(authenticated_page.locator("text=Configurações")).to_be_visible()
    
    # Go back to dashboard
    authenticated_page.click("text=Dashboard")
    
    # Check if dashboard is active again
    expect(authenticated_page.locator("text=Dashboard").locator("..")).to_have_class(
        /border-blue-500/, timeout=3000
    )


def test_dashboard_stats_display(authenticated_page: Page):
    """Test that dashboard stats are displayed"""
    authenticated_page.wait_for_load_state("networkidle")
    
    # Check if stats cards are visible
    expect(authenticated_page.locator("text=Clientes")).to_be_visible()
    expect(authenticated_page.locator("text=Usuário")).to_be_visible()
    expect(authenticated_page.locator("text=Status")).to_be_visible()


def test_logout(authenticated_page: Page):
    """Test logout functionality"""
    # Click logout button
    authenticated_page.click("text=Sair")
    
    # Should redirect to login page
    authenticated_page.wait_for_load_state("networkidle")
    
    # Check if we're back on login page
    expect(authenticated_page.locator("h1")).to_contain_text("ForgeERP", timeout=5000)
    expect(authenticated_page.locator('input[type="text"]')).to_be_visible()

