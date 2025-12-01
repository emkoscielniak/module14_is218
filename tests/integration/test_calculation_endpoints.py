"""
Integration tests for calculation BREAD endpoints with authentication.
Tests the /calculations endpoints with database integration and user authentication.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.models.calculation import Calculation
from app.models.user import User
from main import app
from tests.conftest import create_test_user, authenticate_test_user, create_fake_user

# Test database URL - using in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_calculations.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Setup test database"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def clean_db():
    """Clean database before each test"""
    # Clean all tables
    db = TestingSessionLocal()
    try:
        db.query(Calculation).delete()
        db.query(User).delete()
        db.commit()
    finally:
        db.close()


@pytest.fixture
def test_user_with_auth():
    """Create a test user and return auth headers"""
    db = TestingSessionLocal()
    try:
        # Create test user
        user_data = create_fake_user()
        user_data['password'] = 'TestPassword123'
        user = create_test_user(db, user_data)
        
        # Get auth headers
        auth_headers = authenticate_test_user(client, user.username, 'TestPassword123')
        
        return user, auth_headers
    finally:
        db.close()


class TestCalculationCreate:
    """Test calculation creation (Add) endpoint with authentication"""

    def test_add_calculation_success(self, setup_database, clean_db, test_user_with_auth):
        """Test successful calculation creation with authentication"""
        user, auth_headers = test_user_with_auth
        
        calculation_data = {
            "a": 10.0,
            "b": 5.0,
            "type": "Add"
        }
        
        response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["a"] == 10.0
        assert data["b"] == 5.0
        assert data["type"] == "Add"
        assert data["result"] == 15.0
        assert "id" in data

    def test_add_calculation_subtract(self, setup_database, clean_db, test_user_with_auth):
        """Test subtraction calculation with authentication"""
        user, auth_headers = test_user_with_auth
        
        calculation_data = {
            "a": 10.0,
            "b": 3.0,
            "type": "Sub"
        }
        
        response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 7.0

    def test_add_calculation_multiply(self, setup_database, clean_db, test_user_with_auth):
        """Test multiplication calculation with authentication"""
        user, auth_headers = test_user_with_auth
        
        calculation_data = {
            "a": 6.0,
            "b": 7.0,
            "type": "Multiply"
        }
        
        response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 42.0

    def test_add_calculation_divide(self, setup_database, clean_db, test_user_with_auth):
        """Test division calculation with authentication"""
        user, auth_headers = test_user_with_auth
        
        calculation_data = {
            "a": 20.0,
            "b": 4.0,
            "type": "Divide"
        }
        
        response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 5.0

    def test_add_calculation_divide_by_zero(self, setup_database, clean_db, test_user_with_auth):
        """Test division by zero validation with authentication"""
        user, auth_headers = test_user_with_auth
        
        calculation_data = {
            "a": 10.0,
            "b": 0.0,
            "type": "Divide"
        }
        
        response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error
        assert "zero" in response.json()["detail"][0]["msg"].lower()

    def test_add_calculation_invalid_type(self, setup_database, clean_db, test_user_with_auth):
        """Test invalid calculation type with authentication"""
        user, auth_headers = test_user_with_auth
        
        calculation_data = {
            "a": 10.0,
            "b": 5.0,
            "type": "Invalid"
        }
        
        response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error

    def test_add_calculation_missing_fields(self, setup_database, clean_db, test_user_with_auth):
        """Test calculation creation with missing fields"""
        user, auth_headers = test_user_with_auth
        
        calculation_data = {
            "a": 10.0
            # Missing b and type
        }
        
        response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error

    def test_add_calculation_unauthorized(self, setup_database, clean_db):
        """Test calculation creation without authentication"""
        calculation_data = {
            "a": 10.0,
            "b": 5.0,
            "type": "Add"
        }
        
        response = client.post("/calculations", json=calculation_data)
        assert response.status_code == 401  # Unauthorized


class TestCalculationRead:
    """Test calculation read endpoints with authentication"""

    def test_read_calculation_by_id(self, setup_database, clean_db, test_user_with_auth):
        """Test reading a specific calculation by ID with authentication"""
        user, auth_headers = test_user_with_auth
        
        # First create a calculation
        calculation_data = {
            "a": 8.0,
            "b": 2.0,
            "type": "Multiply"
        }
        
        create_response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Now read it back
        response = client.get(f"/calculations/{calculation_id}", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == calculation_id
        assert data["a"] == 8.0
        assert data["b"] == 2.0
        assert data["type"] == "Multiply"
        assert data["result"] == 16.0

    def test_read_nonexistent_calculation(self, setup_database, clean_db, test_user_with_auth):
        """Test reading a calculation that doesn't exist"""
        user, auth_headers = test_user_with_auth
        
        response = client.get("/calculations/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_read_calculation_unauthorized(self, setup_database, clean_db):
        """Test reading calculation without authentication"""
        response = client.get("/calculations/1")
        assert response.status_code == 401

    def test_read_other_users_calculation(self, setup_database, clean_db):
        """Test that users can't read other users' calculations"""
        # Create first user and calculation
        db = TestingSessionLocal()
        try:
            user1_data = create_fake_user()
            user1_data['password'] = 'Password123'
            user1 = create_test_user(db, user1_data)
            auth1_headers = authenticate_test_user(client, user1.username, 'Password123')
            
            # Create second user
            user2_data = create_fake_user()
            user2_data['password'] = 'Password123'
            user2 = create_test_user(db, user2_data)
            auth2_headers = authenticate_test_user(client, user2.username, 'Password123')
        finally:
            db.close()
        
        # User1 creates a calculation
        calculation_data = {"a": 5.0, "b": 3.0, "type": "Add"}
        create_response = client.post("/calculations", json=calculation_data, headers=auth1_headers)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # User2 tries to read User1's calculation
        response = client.get(f"/calculations/{calculation_id}", headers=auth2_headers)
        assert response.status_code == 404  # Should not find it


class TestCalculationBrowse:
    """Test calculation browse (list) endpoint with authentication"""

    def test_browse_calculations_empty(self, setup_database, clean_db, test_user_with_auth):
        """Test browsing calculations when none exist"""
        user, auth_headers = test_user_with_auth
        
        response = client.get("/calculations", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_browse_calculations_with_data(self, setup_database, clean_db, test_user_with_auth):
        """Test browsing calculations with existing data"""
        user, auth_headers = test_user_with_auth
        
        # Create some calculations
        calculations = [
            {"a": 1.0, "b": 1.0, "type": "Add"},
            {"a": 2.0, "b": 2.0, "type": "Multiply"},
            {"a": 10.0, "b": 5.0, "type": "Sub"}
        ]
        
        for calc_data in calculations:
            response = client.post("/calculations", json=calc_data, headers=auth_headers)
            assert response.status_code == 201
        
        # Browse calculations
        response = client.get("/calculations", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_browse_calculations_pagination(self, setup_database, clean_db, test_user_with_auth):
        """Test calculation browsing with pagination"""
        user, auth_headers = test_user_with_auth
        
        # Create multiple calculations
        for i in range(5):
            calc_data = {"a": float(i), "b": 1.0, "type": "Add"}
            response = client.post("/calculations", json=calc_data, headers=auth_headers)
            assert response.status_code == 201
        
        # Test pagination
        response = client.get("/calculations?skip=2&limit=2", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2

    def test_browse_calculations_unauthorized(self, setup_database, clean_db):
        """Test browsing calculations without authentication"""
        response = client.get("/calculations")
        assert response.status_code == 401


class TestCalculationUpdate:
    """Test calculation update (Edit) endpoints with authentication"""

    def test_update_calculation_put(self, setup_database, clean_db, test_user_with_auth):
        """Test updating calculation with PUT method"""
        user, auth_headers = test_user_with_auth
        
        # Create a calculation
        calculation_data = {"a": 5.0, "b": 3.0, "type": "Add"}
        create_response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Update the calculation
        update_data = {"a": 10.0, "b": 2.0, "type": "Multiply"}
        response = client.put(f"/calculations/{calculation_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["a"] == 10.0
        assert data["b"] == 2.0
        assert data["type"] == "Multiply"
        assert data["result"] == 20.0

    def test_update_calculation_patch(self, setup_database, clean_db, test_user_with_auth):
        """Test updating calculation with PATCH method"""
        user, auth_headers = test_user_with_auth
        
        # Create a calculation
        calculation_data = {"a": 5.0, "b": 3.0, "type": "Add"}
        create_response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Partial update the calculation
        update_data = {"a": 15.0}  # Only update 'a'
        response = client.patch(f"/calculations/{calculation_id}", json=update_data, headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["a"] == 15.0
        assert data["b"] == 3.0  # Should remain unchanged
        assert data["type"] == "Add"  # Should remain unchanged
        assert data["result"] == 18.0  # Should recalculate

    def test_update_nonexistent_calculation(self, setup_database, clean_db, test_user_with_auth):
        """Test updating a calculation that doesn't exist"""
        user, auth_headers = test_user_with_auth
        
        update_data = {"a": 10.0}
        response = client.put("/calculations/99999", json=update_data, headers=auth_headers)
        assert response.status_code == 404

    def test_update_calculation_unauthorized(self, setup_database, clean_db):
        """Test updating calculation without authentication"""
        update_data = {"a": 10.0}
        response = client.put("/calculations/1", json=update_data)
        assert response.status_code == 401


class TestCalculationDelete:
    """Test calculation delete endpoint with authentication"""

    def test_delete_calculation_success(self, setup_database, clean_db, test_user_with_auth):
        """Test successful calculation deletion"""
        user, auth_headers = test_user_with_auth
        
        # Create a calculation
        calculation_data = {"a": 5.0, "b": 3.0, "type": "Add"}
        create_response = client.post("/calculations", json=calculation_data, headers=auth_headers)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Delete the calculation
        response = client.delete(f"/calculations/{calculation_id}", headers=auth_headers)
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/calculations/{calculation_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_nonexistent_calculation(self, setup_database, clean_db, test_user_with_auth):
        """Test deleting a calculation that doesn't exist"""
        user, auth_headers = test_user_with_auth
        
        response = client.delete("/calculations/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_calculation_unauthorized(self, setup_database, clean_db):
        """Test deleting calculation without authentication"""
        response = client.delete("/calculations/1")
        assert response.status_code == 401

    def test_delete_other_users_calculation(self, setup_database, clean_db):
        """Test that users can't delete other users' calculations"""
        # Create two users
        db = TestingSessionLocal()
        try:
            user1_data = create_fake_user()
            user1_data['password'] = 'Password123'
            user1 = create_test_user(db, user1_data)
            auth1_headers = authenticate_test_user(client, user1.username, 'Password123')
            
            user2_data = create_fake_user()
            user2_data['password'] = 'Password123'
            user2 = create_test_user(db, user2_data)
            auth2_headers = authenticate_test_user(client, user2.username, 'Password123')
        finally:
            db.close()
        
        # User1 creates a calculation
        calculation_data = {"a": 5.0, "b": 3.0, "type": "Add"}
        create_response = client.post("/calculations", json=calculation_data, headers=auth1_headers)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # User2 tries to delete User1's calculation
        response = client.delete(f"/calculations/{calculation_id}", headers=auth2_headers)
        assert response.status_code == 404  # Should not find it