"""Unit tests for authentication service"""

from forgeerp.core.services.authentication import (
    verify_password,
    get_password_hash,
    create_access_token,
    decode_access_token,
)


def test_password_hashing():
    """Test password hashing and verification"""
    password = "test_password"
    hashed = get_password_hash(password)
    
    # Hash should be different from password
    assert hashed != password
    
    # Verification should work
    assert verify_password(password, hashed) is True
    
    # Wrong password should fail
    assert verify_password("wrong_password", hashed) is False


def test_jwt_token_creation():
    """Test JWT token creation and decoding"""
    data = {"sub": "test_user", "user_id": 1}
    token = create_access_token(data)
    
    # Token should be a string
    assert isinstance(token, str)
    assert len(token) > 0
    
    # Decode should work
    decoded = decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == "test_user"
    assert decoded["user_id"] == 1


def test_jwt_token_invalid():
    """Test JWT token with invalid token"""
    invalid_token = "invalid_token_string"
    decoded = decode_access_token(invalid_token)
    
    # Should return None for invalid token
    assert decoded is None

