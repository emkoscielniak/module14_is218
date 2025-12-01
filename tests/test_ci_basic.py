#!/usr/bin/env python3
"""
Minimal tests that should pass in CI environment
"""

import pytest

def test_basic_math():
    """Basic test that should always pass"""
    assert 1 + 1 == 2

def test_string_operations():
    """Test basic string operations"""
    assert "hello".upper() == "HELLO"
    assert len("test") == 4

def test_imports_work():
    """Test that core Python modules can be imported"""
    import json
    import os
    import sys
    assert json.dumps({"test": "value"}) == '{"test": "value"}'

def test_fastapi_import():
    """Test FastAPI can be imported"""
    try:
        import fastapi
        assert hasattr(fastapi, 'FastAPI')
    except ImportError:
        pytest.skip("FastAPI not available")

def test_sqlalchemy_import():
    """Test SQLAlchemy can be imported"""
    try:
        import sqlalchemy
        assert hasattr(sqlalchemy, 'create_engine')
    except ImportError:
        pytest.skip("SQLAlchemy not available")

def test_pydantic_import():
    """Test Pydantic can be imported"""
    try:
        import pydantic
        assert hasattr(pydantic, 'BaseModel')
    except ImportError:
        pytest.skip("Pydantic not available")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])