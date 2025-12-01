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

    def test_add_calculation_divide(self, setup_database, clean_db):
        """Test division calculation"""
        calculation_data = {
            "a": 20.0,
            "b": 4.0,
            "type": "Divide"
        }
        
        response = client.post("/calculations", json=calculation_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["result"] == 5.0

    def test_add_calculation_divide_by_zero(self, setup_database, clean_db):
        """Test division by zero validation"""
        calculation_data = {
            "a": 10.0,
            "b": 0.0,
            "type": "Divide"
        }
        
        response = client.post("/calculations", json=calculation_data)
        assert response.status_code == 422  # Validation error
        assert "zero" in response.json()["detail"][0]["msg"].lower()

    def test_add_calculation_invalid_type(self, setup_database, clean_db):
        """Test invalid calculation type"""
        calculation_data = {
            "a": 10.0,
            "b": 5.0,
            "type": "Invalid"
        }
        
        response = client.post("/calculations", json=calculation_data)
        assert response.status_code == 422  # Validation error

    def test_add_calculation_missing_fields(self, setup_database, clean_db):
        """Test calculation creation with missing fields"""
        calculation_data = {
            "a": 10.0
            # Missing b and type
        }
        
        response = client.post("/calculations", json=calculation_data)
        assert response.status_code == 422  # Validation error


class TestCalculationRead:
    """Test calculation read endpoints"""

    def test_read_calculation_by_id(self, setup_database, clean_db):
        """Test reading a specific calculation by ID"""
        # First create a calculation
        calculation_data = {
            "a": 8.0,
            "b": 2.0,
            "type": "Multiply"
        }
        
        create_response = client.post("/calculations", json=calculation_data)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Now read it back
        response = client.get(f"/calculations/{calculation_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == calculation_id
        assert data["a"] == 8.0
        assert data["b"] == 2.0
        assert data["type"] == "Multiply"
        assert data["result"] == 16.0

    def test_read_nonexistent_calculation(self, setup_database, clean_db):
        """Test reading a calculation that doesn't exist"""
        response = client.get("/calculations/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["error"].lower()


class TestCalculationBrowse:
    """Test calculation browse endpoint"""

    def test_browse_calculations_empty(self, setup_database, clean_db):
        """Test browsing calculations when none exist"""
        response = client.get("/calculations")
        
        assert response.status_code == 200
        assert response.json() == []

    def test_browse_calculations_with_data(self, setup_database, clean_db):
        """Test browsing calculations with existing data"""
        # Create several calculations
        calculations_data = [
            {"a": 1.0, "b": 2.0, "type": "Add"},
            {"a": 5.0, "b": 3.0, "type": "Sub"},
            {"a": 4.0, "b": 6.0, "type": "Multiply"}
        ]
        
        created_ids = []
        for calc_data in calculations_data:
            response = client.post("/calculations", json=calc_data)
            assert response.status_code == 201
            created_ids.append(response.json()["id"])
        
        # Browse all calculations
        response = client.get("/calculations")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Check that all created calculations are returned
        returned_ids = [calc["id"] for calc in data]
        for created_id in created_ids:
            assert created_id in returned_ids

    def test_browse_calculations_pagination(self, setup_database, clean_db):
        """Test pagination in browse endpoint"""
        # Create 5 calculations
        for i in range(5):
            calc_data = {"a": i, "b": 1.0, "type": "Add"}
            response = client.post("/calculations", json=calc_data)
            assert response.status_code == 201
        
        # Test limit
        response = client.get("/calculations?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        
        # Test skip
        response = client.get("/calculations?skip=2&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2


class TestCalculationEdit:
    """Test calculation edit/update endpoint"""

    def test_edit_calculation_full_update(self, setup_database, clean_db):
        """Test updating all fields of a calculation"""
        # Create a calculation
        calculation_data = {
            "a": 10.0,
            "b": 5.0,
            "type": "Add"
        }
        
        create_response = client.post("/calculations", json=calculation_data)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Update the calculation
        update_data = {
            "a": 20.0,
            "b": 4.0,
            "type": "Multiply"
        }
        
        response = client.put(f"/calculations/{calculation_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == calculation_id
        assert data["a"] == 20.0
        assert data["b"] == 4.0
        assert data["type"] == "Multiply"
        assert data["result"] == 80.0  # Should be recalculated

    def test_edit_calculation_partial_update(self, setup_database, clean_db):
        """Test updating only some fields of a calculation"""
        # Create a calculation
        calculation_data = {
            "a": 12.0,
            "b": 3.0,
            "type": "Divide"
        }
        
        create_response = client.post("/calculations", json=calculation_data)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Update only the 'a' field
        update_data = {
            "a": 15.0
        }
        
        response = client.put(f"/calculations/{calculation_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == calculation_id
        assert data["a"] == 15.0
        assert data["b"] == 3.0  # Should remain unchanged
        assert data["type"] == "Divide"  # Should remain unchanged
        assert data["result"] == 5.0  # Should be recalculated

    def test_edit_nonexistent_calculation(self, setup_database, clean_db):
        """Test updating a calculation that doesn't exist"""
        update_data = {
            "a": 10.0,
            "b": 2.0,
            "type": "Add"
        }
        
        response = client.put("/calculations/99999", json=update_data)
        
        assert response.status_code == 404
        assert "not found" in response.json()["error"].lower()

    def test_edit_calculation_invalid_data(self, setup_database, clean_db):
        """Test updating calculation with invalid data"""
        # Create a calculation first
        calculation_data = {
            "a": 10.0,
            "b": 5.0,
            "type": "Add"
        }
        
        create_response = client.post("/calculations", json=calculation_data)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Try to update with invalid type
        update_data = {
            "type": "InvalidType"
        }
        
        response = client.put(f"/calculations/{calculation_id}", json=update_data)
        assert response.status_code == 422  # Validation error


class TestCalculationDelete:
    """Test calculation deletion endpoint"""

    def test_delete_calculation(self, setup_database, clean_db):
        """Test successful calculation deletion"""
        # Create a calculation
        calculation_data = {
            "a": 7.0,
            "b": 3.0,
            "type": "Sub"
        }
        
        create_response = client.post("/calculations", json=calculation_data)
        assert create_response.status_code == 201
        calculation_id = create_response.json()["id"]
        
        # Delete the calculation
        response = client.delete(f"/calculations/{calculation_id}")
        
        assert response.status_code == 204
        
        # Verify it's deleted by trying to read it
        get_response = client.get(f"/calculations/{calculation_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_calculation(self, setup_database, clean_db):
        """Test deleting a calculation that doesn't exist"""
        response = client.delete("/calculations/99999")
        
        assert response.status_code == 404
        assert "not found" in response.json()["error"].lower()


class TestCalculationDatabase:
    """Test calculation data storage and retrieval from database"""

    def test_calculation_stored_in_database(self, setup_database, clean_db):
        """Test that calculation is properly stored in database"""
        calculation_data = {
            "a": 9.0,
            "b": 4.0,
            "type": "Add"
        }
        
        response = client.post("/calculations", json=calculation_data)
        assert response.status_code == 201
        calculation_id = response.json()["id"]
        
        # Verify in database
        db = TestingSessionLocal()
        try:
            calc = db.query(Calculation).filter(Calculation.id == calculation_id).first()
            assert calc is not None
            assert calc.a == 9.0
            assert calc.b == 4.0
            assert calc.type == "Add"
            assert calc.result == 13.0
        finally:
            db.close()

    def test_calculation_result_computation(self, setup_database, clean_db):
        """Test that calculation results are properly computed and stored"""
        test_cases = [
            {"a": 10.0, "b": 3.0, "type": "Add", "expected": 13.0},
            {"a": 10.0, "b": 3.0, "type": "Sub", "expected": 7.0},
            {"a": 6.0, "b": 4.0, "type": "Multiply", "expected": 24.0},
            {"a": 15.0, "b": 3.0, "type": "Divide", "expected": 5.0},
        ]
        
        for test_case in test_cases:
            calc_data = {
                "a": test_case["a"],
                "b": test_case["b"], 
                "type": test_case["type"]
            }
            
            response = client.post("/calculations", json=calc_data)
            assert response.status_code == 201
            
            data = response.json()
            assert data["result"] == test_case["expected"], f"Failed for {test_case['type']}"