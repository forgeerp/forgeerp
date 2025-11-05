"""Tests for permissions"""

from fastapi import status
from forgeerp.core.services.authentication import check_permission


def test_check_permission_superuser(session, admin_user):
    """Test permission check for superuser"""
    assert check_permission(admin_user, "any_permission") is True
    assert check_permission(admin_user, "client_create") is True
    assert check_permission(admin_user, "client_modify", client_id=1) is True


def test_check_permission_admin(session, regular_user):
    """Test permission check for admin"""
    regular_user.role = "admin"
    session.add(regular_user)
    session.commit()
    
    assert check_permission(regular_user, "any_permission") is True
    assert check_permission(regular_user, "client_create") is True


def test_check_permission_viewer(session, regular_user):
    """Test permission check for viewer"""
    regular_user.role = "viewer"
    session.add(regular_user)
    session.commit()
    
    assert check_permission(regular_user, "client_create") is False
    assert check_permission(regular_user, "client_modify", client_id=1) is False


def test_check_permission_user(session, regular_user):
    """Test permission check for regular user"""
    regular_user.role = "user"
    session.add(regular_user)
    session.commit()
    
    # User role should have basic permissions
    assert check_permission(regular_user, "client_create") is True
    # But restricted for certain operations
    # TODO: Implement specific permission checks

