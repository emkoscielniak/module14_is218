# tests/unit/test_calculation_schemas.py

import pytest
from pydantic import ValidationError
from app.schemas.calculation import CalculationCreate, CalculationRead, CalculationUpdate

class TestCalculationCreate:
    """Test CalculationCreate schema validation."""
    
    def test_valid_calculation_create(self):
        """Test creating valid CalculationCreate instances."""
        # Test Add operation
        calc = CalculationCreate(a=5.0, b=3.0, type="Add")
        assert calc.a == 5.0
        assert calc.b == 3.0
        assert calc.type == "Add"
        
        # Test Sub operation
        calc = CalculationCreate(a=10.0, b=4.0, type="Sub")
        assert calc.a == 10.0
        assert calc.b == 4.0
        assert calc.type == "Sub"
        
        # Test Multiply operation
        calc = CalculationCreate(a=6.0, b=7.0, type="Multiply")
        assert calc.a == 6.0
        assert calc.b == 7.0
        assert calc.type == "Multiply"
        
        # Test Divide operation
        calc = CalculationCreate(a=15.0, b=3.0, type="Divide")
        assert calc.a == 15.0
        assert calc.b == 3.0
        assert calc.type == "Divide"
    
    def test_invalid_calculation_type(self):
        """Test validation fails for invalid calculation type."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationCreate(a=5.0, b=3.0, type="Invalid")
        
        error = exc_info.value.errors()[0]
        assert "type must be one of" in error['msg']
    
    def test_division_by_zero_validation(self):
        """Test validation prevents division by zero."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationCreate(a=5.0, b=0.0, type="Divide")
        
        error = exc_info.value.errors()[0]
        assert "b cannot be zero for Divide operations" in error['msg']
    
    def test_non_division_zero_b_allowed(self):
        """Test that b=0 is allowed for non-division operations."""
        # Should work fine for other operations
        calc = CalculationCreate(a=5.0, b=0.0, type="Add")
        assert calc.b == 0.0
        
        calc = CalculationCreate(a=5.0, b=0.0, type="Sub")
        assert calc.b == 0.0
        
        calc = CalculationCreate(a=5.0, b=0.0, type="Multiply")
        assert calc.b == 0.0
    
    def test_integer_conversion(self):
        """Test that integers are converted to floats."""
        calc = CalculationCreate(a=5, b=3, type="Add")
        assert calc.a == 5.0
        assert calc.b == 3.0
        assert isinstance(calc.a, float)
        assert isinstance(calc.b, float)
    
    def test_negative_numbers(self):
        """Test calculations with negative numbers."""
        calc = CalculationCreate(a=-5.0, b=3.0, type="Add")
        assert calc.a == -5.0
        assert calc.b == 3.0
        
        calc = CalculationCreate(a=5.0, b=-3.0, type="Sub")
        assert calc.a == 5.0
        assert calc.b == -3.0

class TestCalculationRead:
    """Test CalculationRead schema."""
    
    def test_valid_calculation_read(self):
        """Test creating valid CalculationRead instances."""
        calc = CalculationRead(
            id=1,
            a=5.0,
            b=3.0,
            type="Add",
            result=8.0
        )
        assert calc.id == 1
        assert calc.a == 5.0
        assert calc.b == 3.0
        assert calc.type == "Add"
        assert calc.result == 8.0
    
    def test_calculation_read_without_result(self):
        """Test CalculationRead without result field."""
        calc = CalculationRead(
            id=1,
            a=5.0,
            b=3.0,
            type="Add"
        )
        assert calc.id == 1
        assert calc.a == 5.0
        assert calc.b == 3.0
        assert calc.type == "Add"
        assert calc.result is None
    
    def test_calculation_read_orm_mode(self):
        """Test that orm_mode is enabled."""
        # This is configured in the Config class
        assert CalculationRead.Config.orm_mode is True

class TestCalculationUpdate:
    """Test CalculationUpdate schema validation."""
    
    def test_valid_calculation_update_partial(self):
        """Test creating valid partial CalculationUpdate instances."""
        # Update only 'a'
        calc = CalculationUpdate(a=10.0)
        assert calc.a == 10.0
        assert calc.b is None
        assert calc.type is None
        assert calc.result is None
        
        # Update only 'type'
        calc = CalculationUpdate(type="Multiply")
        assert calc.a is None
        assert calc.b is None
        assert calc.type == "Multiply"
        assert calc.result is None
    
    def test_valid_calculation_update_full(self):
        """Test creating valid full CalculationUpdate instances."""
        calc = CalculationUpdate(
            a=15.0,
            b=5.0,
            type="Divide",
            result=3.0
        )
        assert calc.a == 15.0
        assert calc.b == 5.0
        assert calc.type == "Divide"
        assert calc.result == 3.0
    
    def test_invalid_calculation_update_type(self):
        """Test validation fails for invalid calculation type in update."""
        with pytest.raises(ValidationError) as exc_info:
            CalculationUpdate(type="InvalidType")
        
        error = exc_info.value.errors()[0]
        assert "type must be one of" in error['msg']
    
    def test_calculation_update_empty(self):
        """Test creating empty CalculationUpdate."""
        calc = CalculationUpdate()
        assert calc.a is None
        assert calc.b is None
        assert calc.type is None
        assert calc.result is None