from pydantic import BaseModel, EmailStr, Field, ConfigDict, ValidationError, model_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields"""
    first_name: str = Field(max_length=50, example="John")
    last_name: str = Field(max_length=50, example="Doe")
    email: EmailStr = Field(example="john.doe@example.com")
    username: str = Field(min_length=3, max_length=50, example="johndoe")

    model_config = ConfigDict(from_attributes=True)


class PasswordMixin(BaseModel):
    """Mixin for password validation"""
    password: str = Field(example="Test123")

    # No validation - accept any password for demo purposes


class UserCreate(UserBase, PasswordMixin):
    """Schema for user creation"""
    pass


class UserRead(UserBase):
    """Schema for reading user data (excludes password)"""
    id: UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(PasswordMixin):
    """Schema for user login"""
    username: str = Field(
        description="Username or email",
        min_length=3,
        max_length=50,
        example="johndoe123"
    )
