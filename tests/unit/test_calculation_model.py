# tests/unit/test_calculation_model.py

import pytest
from app.models.calculation import Calculation

class TestCalculationModel:
    """Test the Calculation SQLAlchemy model."""
    
    def test_calculation_model_creation(self):
        """Test creating a Calculation model instance."""
        calc = Calculation(
            a=5.0,
            b=3.0,
            type="Add"
        )
        assert calc.a == 5.0
        assert calc.b == 3.0
        assert calc.type == "Add"
        assert calc.result is None  # result is optional
        assert calc.id is None  # id is auto-generated
    
    def test_calculation_model_with_result(self):
        """Test creating a Calculation model with pre-computed result."""
        calc = Calculation(
            a=10.0,
            b=4.0,
            type="Sub",
            result=6.0
        )
        assert calc.a == 10.0
        assert calc.b == 4.0
        assert calc.type == "Sub"
        assert calc.result == 6.0
    
    def test_calculate_add(self):
        """Test compute method for addition."""
        calc = Calculation(a=5.0, b=3.0, type="Add")
        result = calc.compute()
        assert result == 8.0
    
    def test_calculate_subtract(self):
        """Test compute method for subtraction."""
        calc = Calculation(a=10.0, b=4.0, type="Sub")
        result = calc.compute()
        assert result == 6.0
    
    def test_calculate_multiply(self):
        """Test compute method for multiplication."""
        calc = Calculation(a=6.0, b=7.0, type="Multiply")
        result = calc.compute()
        assert result == 42.0
    
    def test_calculate_divide(self):
        """Test compute method for division."""
        calc = Calculation(a=15.0, b=3.0, type="Divide")
        result = calc.compute()
        assert result == 5.0
    
    def test_calculate_division_by_zero(self):
        """Test compute method handles division by zero."""
        calc = Calculation(a=5.0, b=0.0, type="Divide")
        with pytest.raises(ValueError, match="Cannot divide by zero!"):
            calc.compute()
    
    def test_calculate_case_insensitive_operations(self):
        """Test compute method with different case variations."""
        # Test lowercase
        calc = Calculation(a=5.0, b=3.0, type="add")
        result = calc.compute()
        assert result == 8.0
        
        # Test full word
        calc = Calculation(a=10.0, b=4.0, type="subtraction")
        result = calc.compute()
        assert result == 6.0
        
        # Test abbreviation
        calc = Calculation(a=6.0, b=7.0, type="mul")
        result = calc.compute()
        assert result == 42.0
        
        # Test division
        calc = Calculation(a=15.0, b=3.0, type="division")
        result = calc.compute()
        assert result == 5.0
    
    def test_calculate_invalid_operation(self):
        """Test compute method with invalid operation type."""
        calc = Calculation(a=5.0, b=3.0, type="Invalid")
        with pytest.raises(ValueError, match="Unsupported calculation type: Invalid"):
            calc.compute()
    
    def test_negative_numbers(self):
        """Test calculations with negative numbers."""
        # Negative + positive
        calc = Calculation(a=-5.0, b=3.0, type="Add")
        result = calc.compute()
        assert result == -2.0
        
        # Negative - negative
        calc = Calculation(a=-10.0, b=-4.0, type="Sub")
        result = calc.compute()
        assert result == -6.0
        
        # Negative * positive
        calc = Calculation(a=-6.0, b=7.0, type="Multiply")
        result = calc.compute()
        assert result == -42.0
        
        # Negative / negative
        calc = Calculation(a=-15.0, b=-3.0, type="Divide")
        result = calc.compute()
        assert result == 5.0
    
    def test_float_calculations(self):
        """Test calculations with float numbers."""
        # Float addition
        calc = Calculation(a=2.5, b=3.7, type="Add")
        result = calc.compute()
        assert result == pytest.approx(6.2)
        
        # Float subtraction
        calc = Calculation(a=10.5, b=4.2, type="Sub")
        result = calc.compute()
        assert result == pytest.approx(6.3)
        
        # Float multiplication
        calc = Calculation(a=2.5, b=4.0, type="Multiply")
        result = calc.compute()
        assert result == pytest.approx(10.0)
        
        # Float division
        calc = Calculation(a=7.5, b=2.5, type="Divide")
        result = calc.compute()
        assert result == pytest.approx(3.0)