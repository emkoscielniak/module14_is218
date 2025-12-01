#!/usr/bin/env python3
"""
CI/CD validation script to test core functionality
"""

def test_imports():
    """Test that all core imports work"""
    try:
        import fastapi
        import sqlalchemy
        import pydantic
        import jose
        import passlib
        import pytest
        print("✅ All core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_app_creation():
    """Test that the FastAPI app can be created"""
    try:
        from main import app
        print("✅ FastAPI app creation successful")
        return True
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        return False

def test_models():
    """Test that models can be imported"""
    try:
        from app.models.user import User
        from app.schemas.base import UserCreate
        print("✅ Model imports successful")
        return True
    except Exception as e:
        print(f"❌ Model imports failed: {e}")
        return False

def main():
    """Run all validation tests"""
    print("🚀 Running CI/CD validation tests...")
    
    tests = [
        test_imports,
        test_app_creation, 
        test_models
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    if all(results):
        print("\n🎉 All validation tests passed!")
        return 0
    else:
        print(f"\n❌ {len([r for r in results if not r])} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())