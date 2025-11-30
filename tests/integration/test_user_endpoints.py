# tests/integration/test_user_endpoints.py

import pytest
from fastapi.testclient import TestClient
from main import app
from app.database import get_db
from app.models.user import User
from tests.conftest import TestingSessionLocal

# Override the get_db dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


class TestUserRegistration:
    """Test user registration endpoint."""

    def test_register_user_success(self, client, db_session):
        """Test successful user registration."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        
        response = client.post("/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert "password" not in data  # Password should not be in response
        assert "password_hash" not in data  # Password hash should not be in response
        assert data["is_active"] is True
        assert data["is_verified"] is False
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_register_user_duplicate_email(self, client, db_session):
        """Test registration with duplicate email."""
        user_data = {
            "first_name": "John", 
            "last_name": "Doe",
            "email": "duplicate@example.com",
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        
        # Register first user
        response1 = client.post("/register", json=user_data)
        assert response1.status_code == 201
        
        # Try to register with same email, different username
        user_data2 = user_data.copy()
        user_data2["username"] = "differentuser"
        response2 = client.post("/register", json=user_data2)
        
        assert response2.status_code == 400
        assert "Username or email already exists" in response2.json()["error"]

    def test_register_user_duplicate_username(self, client, db_session):
        """Test registration with duplicate username."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john@example.com",
            "username": "duplicateuser",
            "password": "SecurePass123"
        }
        
        # Register first user
        response1 = client.post("/register", json=user_data)
        assert response1.status_code == 201
        
        # Try to register with same username, different email
        user_data2 = user_data.copy()
        user_data2["email"] = "different@example.com"
        response2 = client.post("/register", json=user_data2)
        
        assert response2.status_code == 400
        assert "Username or email already exists" in response2.json()["error"]

    def test_register_user_invalid_email(self, client, db_session):
        """Test registration with invalid email format."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "invalid-email-format",
            "username": "johndoe123", 
            "password": "SecurePass123"
        }
        
        response = client.post("/register", json=user_data)
        assert response.status_code == 400

    def test_register_user_weak_password(self, client, db_session):
        """Test registration with weak password."""
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "username": "johndoe123",
            "password": "weak"  # Too short and no uppercase/digit
        }
        
        response = client.post("/register", json=user_data)
        assert response.status_code == 400

    def test_register_user_missing_fields(self, client, db_session):
        """Test registration with missing required fields."""
        user_data = {
            "first_name": "John",
            # Missing other required fields
        }
        
        response = client.post("/register", json=user_data)
        assert response.status_code == 400


class TestUserAuthentication:
    """Test user authentication endpoints."""

    def test_login_success_form_data(self, client, db_session):
        """Test successful login using form data."""
        # First register a user
        user_data = {
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john@example.com",
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        client.post("/register", json=user_data)
        
        # Login with form data
        login_data = {
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        
        response = client.post("/login", data=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["username"] == "johndoe123"

    def test_login_success_json(self, client, db_session):
        """Test successful login using JSON data."""
        # First register a user
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com", 
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        client.post("/register", json=user_data)
        
        # Login with JSON data
        login_data = {
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        
        response = client.post("/login/json", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    def test_login_with_email(self, client, db_session):
        """Test login using email instead of username."""
        # First register a user
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "username": "johndoe123", 
            "password": "SecurePass123"
        }
        client.post("/register", json=user_data)
        
        # Login with email
        login_data = {
            "username": "john@example.com",  # Using email as username
            "password": "SecurePass123"
        }
        
        response = client.post("/login", data=login_data)
        assert response.status_code == 200

    def test_login_wrong_password(self, client, db_session):
        """Test login with incorrect password."""
        # First register a user
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        client.post("/register", json=user_data)
        
        # Login with wrong password
        login_data = {
            "username": "johndoe123", 
            "password": "WrongPassword123"
        }
        
        response = client.post("/login", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["error"]

    def test_login_nonexistent_user(self, client, db_session):
        """Test login with non-existent user."""
        login_data = {
            "username": "nonexistent",
            "password": "SecurePass123"
        }
        
        response = client.post("/login", data=login_data)
        
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["error"]


class TestProtectedEndpoints:
    """Test protected endpoints that require authentication."""

    def test_get_current_user_success(self, client, db_session):
        """Test accessing current user endpoint with valid token."""
        # Register and login to get token
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "username": "johndoe123",
            "password": "SecurePass123"
        }
        client.post("/register", json=user_data)
        
        login_response = client.post("/login", data={
            "username": "johndoe123",
            "password": "SecurePass123"
        })
        token = login_response.json()["access_token"]
        
        # Access protected endpoint
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/users/me", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "johndoe123"
        assert data["email"] == "john@example.com"

    def test_get_current_user_no_token(self, client, db_session):
        """Test accessing current user endpoint without token."""
        response = client.get("/users/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client, db_session):
        """Test accessing current user endpoint with invalid token."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)
        assert response.status_code == 401


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data