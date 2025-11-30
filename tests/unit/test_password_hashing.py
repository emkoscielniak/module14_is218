# tests/unit/test_password_hashing.py

import pytest
from app.models.user import User


class TestPasswordHashing:
    """Test password hashing and verification functionality."""

    def test_hash_password_returns_different_value(self):
        """Test that hashed password is different from plain password."""
        plain_password = "TestPassword123"
        hashed_password = User.hash_password(plain_password)
        
        assert hashed_password != plain_password
        assert hashed_password is not None
        assert len(hashed_password) > 0

    def test_hash_password_same_input_different_output(self):
        """Test that same password produces different hashes (salt)."""
        plain_password = "TestPassword123"
        hash1 = User.hash_password(plain_password)
        hash2 = User.hash_password(plain_password)
        
        # Due to salt, same password should produce different hashes
        assert hash1 != hash2

    def test_verify_password_correct(self):
        """Test password verification with correct password."""
        plain_password = "TestPassword123"
        hashed_password = User.hash_password(plain_password)
        
        # Create a user instance to test verify_password method
        user = User(
            first_name="Test",
            last_name="User", 
            email="test@example.com",
            username="testuser",
            password_hash=hashed_password,
            is_active=True,
            is_verified=False
        )
        
        assert user.verify_password(plain_password) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password."""
        plain_password = "TestPassword123"
        wrong_password = "WrongPassword456"
        hashed_password = User.hash_password(plain_password)
        
        # Create a user instance to test verify_password method
        user = User(
            first_name="Test",
            last_name="User", 
            email="test@example.com",
            username="testuser",
            password_hash=hashed_password,
            is_active=True,
            is_verified=False
        )
        
        assert user.verify_password(wrong_password) is False

    def test_hash_empty_password(self):
        """Test hashing an empty password."""
        empty_password = ""
        hashed_password = User.hash_password(empty_password)
        
        assert hashed_password != empty_password
        assert hashed_password is not None

    def test_hash_long_password(self):
        """Test hashing a very long password."""
        long_password = "a" * 1000  # 1000 character password
        hashed_password = User.hash_password(long_password)
        
        assert hashed_password != long_password
        assert hashed_password is not None

    def test_hash_special_characters(self):
        """Test hashing password with special characters."""
        special_password = "Test@#$%^&*()_+{}[]|\\:;\"'<>,.?/~`123"
        hashed_password = User.hash_password(special_password)
        
        user = User(
            first_name="Test",
            last_name="User", 
            email="test@example.com",
            username="testuser",
            password_hash=hashed_password,
            is_active=True,
            is_verified=False
        )
        
        assert user.verify_password(special_password) is True
        assert user.verify_password("wrong") is False

    def test_hash_unicode_password(self):
        """Test hashing password with unicode characters."""
        unicode_password = "Test密码123🔒"
        hashed_password = User.hash_password(unicode_password)
        
        user = User(
            first_name="Test",
            last_name="User", 
            email="test@example.com",
            username="testuser",
            password_hash=hashed_password,
            is_active=True,
            is_verified=False
        )
        
        assert user.verify_password(unicode_password) is True