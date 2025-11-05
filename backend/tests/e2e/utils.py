"""Utilities for E2E tests"""

import time
from playwright.sync_api import Page
from typing import Optional


def wait_for_react(page: Page, timeout: int = 30000) -> None:
    """
    Wait for React app to be fully loaded and interactive.
    
    This function should be used after page.goto() to ensure React has
    finished hydrating and rendering before interacting with elements.
    
    Args:
        page: Playwright page object
        timeout: Maximum time to wait in milliseconds
    """
    try:
        # Wait for React root element
        page.wait_for_selector('#root', state='visible', timeout=timeout)
        
        # Wait for document ready state
        page.wait_for_function(
            "document.readyState === 'complete'",
            timeout=timeout
        )
        
        # Wait a bit more for React to render
        time.sleep(1)
        
        # Try to find any React-rendered content
        try:
            page.wait_for_selector('input, button, form', timeout=5000)
        except:
            pass  # Not critical if no form elements found
            
    except Exception as e:
        # Log warning but don't fail - page might be loading
        print(f"⚠️  Warning waiting for React: {e}")


def wait_for_navigation_complete(page: Page, timeout: int = 30000) -> None:
    """
    Wait for navigation to complete and React to hydrate.
    
    Use this after clicking links or buttons that trigger navigation.
    
    Args:
        page: Playwright page object
        timeout: Maximum time to wait in milliseconds
    """
    page.wait_for_load_state("networkidle", timeout=timeout)
    wait_for_react(page, timeout=timeout)

