# tests/integration/test_calculation_integration.py

import pytest
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models.calculation import Calculation
from app.models.user import User
from app.schemas.calculation import CalculationCreate, CalculationRead
import uuid

# Create test tables
@pytest.fixture(autouse=True)
def setup_test_database():
    """Set up test database with tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Create a test database session."""
    db = next(get_db())
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    user = User(
        first_name="Test",
        last_name="User", 
        email="test@example.com",
        username="testuser",
        password_hash="hashedpassword"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

class TestCalculationDatabaseIntegration:
    """Integration tests for Calculation model with database."""
    
    def test_create_calculation_in_database(self, db_session):
        """Test creating and storing a calculation in the database."""
        # Create calculation
        calc = Calculation(
            a=5.0,
            b=3.0,
            type="Add"
        )
        
        # Store in database
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        # Verify it was stored correctly
        assert calc.id is not None
        assert calc.a == 5.0
        assert calc.b == 3.0
        assert calc.type == "Add"
        assert calc.result is None
    
    def test_calculation_with_user_relationship(self, db_session, sample_user):
        """Test calculation with user relationship."""
        # Create calculation linked to user
        calc = Calculation(
            a=10.0,
            b=4.0,
            type="Sub",
            user_id=sample_user.id
        )
        
        # Store in database
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        # Verify relationships
        assert calc.user_id == sample_user.id
        assert calc.user == sample_user
        
        # Check back reference
        db_session.refresh(sample_user)
        assert len(sample_user.calculations) == 1
        assert sample_user.calculations[0] == calc
    
    def test_calculation_compute_and_store_result(self, db_session):
        """Test computing result and storing in database."""
        # Create calculation
        calc = Calculation(
            a=6.0,
            b=7.0,
            type="Multiply"
        )
        
        # Compute result
        result = calc.compute()
        calc.result = result
        
        # Store in database
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        # Verify stored result
        assert calc.result == 42.0
        assert calc.compute() == 42.0  # Should match stored result
    
    def test_query_calculations_by_type(self, db_session):
        """Test querying calculations by operation type."""
        # Create multiple calculations
        calculations = [
            Calculation(a=1.0, b=2.0, type="Add"),
            Calculation(a=5.0, b=3.0, type="Sub"),
            Calculation(a=4.0, b=6.0, type="Add"),
            Calculation(a=8.0, b=2.0, type="Divide")
        ]
        
        for calc in calculations:
            db_session.add(calc)
        db_session.commit()
        
        # Query for Add operations
        add_calculations = db_session.query(Calculation).filter(
            Calculation.type == "Add"
        ).all()
        
        assert len(add_calculations) == 2
        assert all(calc.type == "Add" for calc in add_calculations)
        
        # Query for Sub operations
        sub_calculations = db_session.query(Calculation).filter(
            Calculation.type == "Sub"
        ).all()
        
        assert len(sub_calculations) == 1
        assert sub_calculations[0].type == "Sub"
    
    def test_calculation_cascade_delete_with_user(self, db_session, sample_user):
        """Test that calculations are deleted when user is deleted."""
        # Create calculations linked to user
        calc1 = Calculation(a=1.0, b=2.0, type="Add", user_id=sample_user.id)
        calc2 = Calculation(a=5.0, b=3.0, type="Sub", user_id=sample_user.id)
        
        db_session.add_all([calc1, calc2])
        db_session.commit()
        
        # Verify calculations exist
        user_calculations = db_session.query(Calculation).filter(
            Calculation.user_id == sample_user.id
        ).all()
        assert len(user_calculations) == 2
        
        # Delete user
        db_session.delete(sample_user)
        db_session.commit()
        
        # Verify calculations are deleted due to cascade
        remaining_calculations = db_session.query(Calculation).filter(
            Calculation.user_id == sample_user.id
        ).all()
        assert len(remaining_calculations) == 0
    
    def test_calculation_error_handling_invalid_type(self, db_session):
        """Test that invalid calculation types still store but fail on compute."""
        # Create calculation with invalid type (database allows it)
        calc = Calculation(
            a=5.0,
            b=3.0,
            type="InvalidOperation"
        )
        
        # Store in database (should succeed)
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        assert calc.id is not None
        assert calc.type == "InvalidOperation"
        
        # Computing should fail
        with pytest.raises(ValueError, match="Unsupported calculation type"):
            calc.compute()
    
    def test_calculation_division_by_zero_handling(self, db_session):
        """Test division by zero error handling in database context."""
        # Create division by zero calculation
        calc = Calculation(
            a=5.0,
            b=0.0,
            type="Divide"
        )
        
        # Store in database (should succeed)
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        assert calc.id is not None
        assert calc.b == 0.0
        
        # Computing should fail
        with pytest.raises(ValueError, match="Cannot divide by zero!"):
            calc.compute()

class TestCalculationSchemaIntegration:
    """Integration tests for Calculation schemas with database."""
    
    def test_calculation_create_to_model(self, db_session):
        """Test converting CalculationCreate schema to model and storing."""
        # Create schema instance
        calc_create = CalculationCreate(
            a=15.0,
            b=5.0,
            type="Divide"
        )
        
        # Convert to model
        calc_model = Calculation(**calc_create.dict())
        
        # Store in database
        db_session.add(calc_model)
        db_session.commit()
        db_session.refresh(calc_model)
        
        # Verify conversion and storage
        assert calc_model.a == 15.0
        assert calc_model.b == 5.0
        assert calc_model.type == "Divide"
        assert calc_model.id is not None
    
    def test_calculation_model_to_read_schema(self, db_session):
        """Test converting database model to CalculationRead schema."""
        # Create and store calculation
        calc = Calculation(
            a=8.0,
            b=2.0,
            type="Divide"
        )
        calc.result = calc.compute()
        
        db_session.add(calc)
        db_session.commit()
        db_session.refresh(calc)
        
        # Convert to read schema
        calc_read = CalculationRead.from_orm(calc)
        
        # Verify conversion
        assert calc_read.id == calc.id
        assert calc_read.a == 8.0
        assert calc_read.b == 2.0
        assert calc_read.type == "Divide"
        assert calc_read.result == 4.0
    
    def test_multiple_calculations_workflow(self, db_session, sample_user):
        """Test complete workflow with multiple calculations."""
        # Test data
        calculations_data = [
            {"a": 10.0, "b": 5.0, "type": "Add"},
            {"a": 20.0, "b": 4.0, "type": "Sub"},
            {"a": 6.0, "b": 7.0, "type": "Multiply"},
            {"a": 15.0, "b": 3.0, "type": "Divide"}
        ]
        
        stored_calculations = []
        
        # Create, compute, and store calculations
        for calc_data in calculations_data:
            # Create from schema
            calc_create = CalculationCreate(**calc_data)
            
            # Convert to model
            calc_model = Calculation(**calc_create.dict())
            calc_model.user_id = sample_user.id
            
            # Compute and store result
            calc_model.result = calc_model.compute()
            
            # Store in database
            db_session.add(calc_model)
            stored_calculations.append(calc_model)
        
        db_session.commit()
        
        # Verify all calculations were stored
        all_calculations = db_session.query(Calculation).all()
        assert len(all_calculations) == 4
        
        # Verify results
        expected_results = [15.0, 16.0, 42.0, 5.0]
        actual_results = [calc.result for calc in all_calculations]
        assert actual_results == expected_results
        
        # Verify user relationship
        db_session.refresh(sample_user)
        assert len(sample_user.calculations) == 4