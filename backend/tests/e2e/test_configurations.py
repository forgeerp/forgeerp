"""E2E tests for configurations page"""

import pytest
from playwright.sync_api import Page, expect
import time


def test_configurations_page_loads(authenticated_page: Page):
    """Test that configurations page loads"""
    # Navigate to configurations tab
    authenticated_page.click("text=Configurações")
    authenticated_page.wait_for_load_state("networkidle")
    
    # Check if page loaded
    expect(authenticated_page.locator("text=Configurações")).to_be_visible()
    expect(authenticated_page.locator("text=Nova Configuração")).to_be_visible()


def test_create_configuration(authenticated_page: Page):
    """Test creating a new configuration"""
    # Navigate to configurations
    authenticated_page.click("text=Configurações")
    authenticated_page.wait_for_load_state("networkidle")
    
    # Click new configuration button
    authenticated_page.click("text=Nova Configuração")
    
    # Wait for form to appear
    expect(authenticated_page.locator('input[placeholder*="ex: github_token"]')).to_be_visible(
        timeout=3000
    )
    
    # Fill form
    authenticated_page.fill('input[placeholder*="ex: github_token"]', "test_config_e2e")
    authenticated_page.fill('textarea[placeholder*="Valor"]', "test_value_e2e")
    authenticated_page.select_option('select', 'string')
    authenticated_page.fill('input[placeholder*="Descrição"]', "Test E2E")
    
    # Submit form
    authenticated_page.click('button:has-text("Criar")')
    
    # Wait for form to close and configuration to appear
    authenticated_page.wait_for_load_state("networkidle")
    time.sleep(1)
    
    # Check if configuration appears in table
    expect(authenticated_page.locator("text=test_config_e2e")).to_be_visible(timeout=5000)


def test_edit_configuration(authenticated_page: Page):
    """Test editing a configuration"""
    # Navigate to configurations
    authenticated_page.click("text=Configurações")
    authenticated_page.wait_for_load_state("networkidle")
    
    # Create a configuration first (if needed)
    # Or use existing one
    
    # Find first edit button
    edit_buttons = authenticated_page.locator('button:has-text("Editar")')
    if edit_buttons.count() > 0:
        edit_buttons.first.click()
        
        # Wait for form to appear
        expect(authenticated_page.locator('button:has-text("Atualizar")')).to_be_visible(
            timeout=3000
        )
        
        # Modify value
        authenticated_page.fill('textarea[placeholder*="Valor"]', "updated_value_e2e")
        
        # Submit
        authenticated_page.click('button:has-text("Atualizar")')
        
        # Wait for update
        authenticated_page.wait_for_load_state("networkidle")
        time.sleep(1)
        
        # Check if updated value appears
        expect(authenticated_page.locator("text=updated_value_e2e")).to_be_visible(
            timeout=5000
        )


def test_delete_configuration(authenticated_page: Page):
    """Test deleting a configuration"""
    # Navigate to configurations
    authenticated_page.click("text=Configurações")
    authenticated_page.wait_for_load_state("networkidle")
    
    # Find delete buttons
    delete_buttons = authenticated_page.locator('button:has-text("Deletar")')
    
    if delete_buttons.count() > 0:
        # Get count before deletion
        count_before = delete_buttons.count()
        
        # Click first delete button
        delete_buttons.first.click()
        
        # Confirm deletion (if dialog appears)
        # Playwright auto-handles alert dialogs
        authenticated_page.wait_for_load_state("networkidle")
        time.sleep(1)
        
        # Check if count decreased (configuration was removed)
        delete_buttons_after = authenticated_page.locator('button:has-text("Deletar")')
        # Note: This is a simple check, actual implementation may vary
        assert delete_buttons_after.count() < count_before or delete_buttons_after.count() == 0


def test_configurations_table_displays(authenticated_page: Page):
    """Test that configurations table displays correctly"""
    # Navigate to configurations
    authenticated_page.click("text=Configurações")
    authenticated_page.wait_for_load_state("networkidle")
    
    # Check table headers
    expect(authenticated_page.locator("text=Chave")).to_be_visible()
    expect(authenticated_page.locator("text=Valor")).to_be_visible()
    expect(authenticated_page.locator("text=Tipo")).to_be_visible()
    expect(authenticated_page.locator("text=Descrição")).to_be_visible()
    expect(authenticated_page.locator("text=Ações")).to_be_visible()


def test_configuration_form_validation(authenticated_page: Page):
    """Test configuration form validation"""
    # Navigate to configurations
    authenticated_page.click("text=Configurações")
    authenticated_page.wait_for_load_state("networkidle")
    
    # Click new configuration
    authenticated_page.click("text=Nova Configuração")
    
    # Try to submit without filling required fields
    authenticated_page.click('button:has-text("Criar")')
    
    # Check if validation errors appear (HTML5 or custom)
    # HTML5 validation should prevent submission
    expect(authenticated_page.locator('input:invalid')).to_have_count(
        at_least=1, timeout=1000
    ).or_(
        expect(authenticated_page.locator("text=/required|obrigatório/i")).to_be_visible()
    )

