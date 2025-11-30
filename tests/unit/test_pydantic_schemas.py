# tests/unit/test_pydantic_schemas.py

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError
from app.schemas.base import UserBase, PasswordMixin, UserCreate, UserRead, UserLogin
from app.schemas.user import UserResponse, Token, TokenData


class TestUserBase:
    """Test UserBase schema validation."""

    def test_valid_user_base(self):
        """Test UserBase with valid data."""
        data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com",
            "username": "johndoe123"
        }
        user = UserBase(**data)
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.username == "johndoe123"

    def test_invalid_email(self):
        """Test UserBase with invalid email format."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email-format",
            "username": "johndoe123"
        }
        with pytest.raises(ValidationError):
            UserBase(**data)

    def test_username_too_short(self):
        """Test UserBase with username too short."""
        data = {
            "first_name": "John", 
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "username": "jo"  # Only 2 characters
        }
        with pytest.raises(ValidationError):
            UserBase(**data)

    def test_username_too_long(self):
        """Test UserBase with username too long."""
        data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john.doe@example.com",
            "username": "a" * 51  # 51 characters
        }
        with pytest.raises(ValidationError):
            UserBase(**data)

    def test_missing_required_fields(self):
        """Test UserBase with missing required fields."""
        data = {
            "first_name": "John"
            # Missing other required fields
        }
        with pytest.raises(ValidationError):
            UserBase(**data)


class TestPasswordMixin:
    """Test PasswordMixin schema validation."""

    def test_valid_password(self):
        """Test PasswordMixin with valid password."""
        data = {"password": "ValidPass123"}
        password_mixin = PasswordMixin(**data)
        assert password_mixin.password == "ValidPass123"

    def test_password_too_short(self):
        """Test PasswordMixin with password too short."""
        data = {"password": "short"}  # Only 5 characters
        with pytest.raises(ValidationError, match="Password must be at least 6 characters long"):
            PasswordMixin(**data)

    def test_password_no_uppercase(self):
        """Test PasswordMixin with no uppercase letter."""
        data = {"password": "lowercase123"}
        with pytest.raises(ValidationError, match="Password must contain at least one uppercase letter"):
            PasswordMixin(**data)

    def test_password_no_lowercase(self):
        """Test PasswordMixin with no lowercase letter."""  
        data = {"password": "UPPERCASE123"}
        with pytest.raises(ValidationError, match="Password must contain at least one lowercase letter"):
            PasswordMixin(**data)

    def test_password_no_digit(self):
        """Test PasswordMixin with no digit."""
        data = {"password": "NoDigitsHere"}
        with pytest.raises(ValidationError, match="Password must contain at least one digit"):
            PasswordMixin(**data)

    def test_password_too_long(self):
        """Test PasswordMixin with password too long."""
        data = {"password": "A" + "a" * 127 + "1"}  # 129 characters (A + 127 a's + 1 = 129)
        with pytest.raises(ValidationError):
            PasswordMixin(**data)


class TestUserCreate:
    """Test UserCreate schema validation."""

    def test_valid_user_create(self):
        """Test UserCreate with all valid data."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com", 
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        user_create = UserCreate(**data)
        assert user_create.first_name == "John"
        assert user_create.password == "SecurePass123"

    def test_invalid_user_create_bad_password(self):
        """Test UserCreate with invalid password."""
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "username": "johndoe123", 
            "password": "weak"  # Too short and no uppercase/digit
        }
        with pytest.raises(ValidationError):
            UserCreate(**data)


class TestUserRead:
    """Test UserRead schema validation."""

    def test_valid_user_read(self):
        """Test UserRead with all valid data."""
        user_id = uuid4()
        now = datetime.utcnow()
        
        data = {
            "id": user_id,
            "first_name": "John", 
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "username": "johndoe123",
            "is_active": True,
            "is_verified": False,
            "created_at": now,
            "updated_at": now
        }
        user_read = UserRead(**data)
        assert user_read.id == user_id
        assert user_read.is_active is True
        assert user_read.is_verified is False


class TestUserResponse:
    """Test UserResponse schema validation."""

    def test_valid_user_response(self):
        """Test UserResponse with valid data."""
        user_id = uuid4()
        now = datetime.utcnow()
        
        data = {
            "id": user_id,
            "username": "johndoe123",
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe", 
            "is_active": True,
            "is_verified": False,
            "created_at": now,
            "updated_at": now
        }
        user_response = UserResponse(**data)
        assert user_response.id == user_id
        assert user_response.username == "johndoe123"


class TestToken:
    """Test Token schema validation."""

    def test_valid_token(self):
        """Test Token with valid data."""
        user_id = uuid4()
        now = datetime.utcnow()
        
        user_data = {
            "id": user_id,
            "username": "johndoe123", 
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "is_active": True,
            "is_verified": False,
            "created_at": now,
            "updated_at": now
        }
        user_response = UserResponse(**user_data)
        
        token_data = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "token_type": "bearer",
            "user": user_response
        }
        token = Token(**token_data)
        assert token.access_token.startswith("eyJ")
        assert token.token_type == "bearer"
        assert token.user.username == "johndoe123"


class TestTokenData:
    """Test TokenData schema validation."""

    def test_valid_token_data(self):
        """Test TokenData with valid user_id."""
        user_id = uuid4()
        token_data = TokenData(user_id=user_id)
        assert token_data.user_id == user_id

    def test_token_data_none(self):
        """Test TokenData with None user_id."""
        token_data = TokenData(user_id=None)
        assert token_data.user_id is None

    def test_token_data_empty(self):
        """Test TokenData with no parameters."""
        token_data = TokenData()
        assert token_data.user_id is None


class TestUserLogin:
    """Test UserLogin schema validation."""

    def test_valid_user_login(self):
        """Test UserLogin with valid credentials."""
        data = {
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        user_login = UserLogin(**data)
        assert user_login.username == "johndoe123"
        assert user_login.password == "SecurePass123"

    def test_user_login_short_username(self):
        """Test UserLogin with username too short."""
        data = {
            "username": "jo",  # Too short
            "password": "SecurePass123"
        }
        with pytest.raises(ValidationError):
            UserLogin(**data)

    def test_user_login_invalid_password(self):
        """Test UserLogin with invalid password."""
        data = {
            "username": "johndoe123", 
            "password": "weak"  # Invalid password
        }
        with pytest.raises(ValidationError):
            UserLogin(**data)