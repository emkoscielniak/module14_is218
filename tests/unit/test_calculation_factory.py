# tests/unit/test_calculation_factory.py

import pytest
from app.operations.calculation_factory import (
    CalculationFactory,
    CalculationStrategy,
    AddStrategy,
    SubtractStrategy,
    MultiplyStrategy,
    DivideStrategy
)

class TestCalculationStrategies:
    """Test individual calculation strategies."""
    
    def test_add_strategy(self):
        """Test AddStrategy execution."""
        strategy = AddStrategy()
        assert strategy.execute(5, 3) == 8
        assert strategy.execute(-2, 7) == 5
        assert strategy.execute(2.5, 3.5) == 6.0
    
    def test_subtract_strategy(self):
        """Test SubtractStrategy execution."""
        strategy = SubtractStrategy()
        assert strategy.execute(10, 3) == 7
        assert strategy.execute(-2, -7) == 5
        assert strategy.execute(5.5, 2.5) == 3.0
    
    def test_multiply_strategy(self):
        """Test MultiplyStrategy execution."""
        strategy = MultiplyStrategy()
        assert strategy.execute(4, 5) == 20
        assert strategy.execute(-3, 4) == -12
        assert strategy.execute(2.5, 4) == 10.0
    
    def test_divide_strategy(self):
        """Test DivideStrategy execution."""
        strategy = DivideStrategy()
        assert strategy.execute(10, 2) == 5.0
        assert strategy.execute(7, 2) == 3.5
        assert strategy.execute(-8, 4) == -2.0
    
    def test_divide_strategy_zero_division(self):
        """Test DivideStrategy with zero division."""
        strategy = DivideStrategy()
        with pytest.raises(ValueError, match="Cannot divide by zero!"):
            strategy.execute(5, 0)

class TestCalculationFactory:
    """Test the CalculationFactory class."""
    
    def test_create_calculation_add(self):
        """Test creating Add calculation strategy."""
        strategy = CalculationFactory.create_calculation("Add")
        assert isinstance(strategy, AddStrategy)
        
        # Test case variations
        strategy = CalculationFactory.create_calculation("add")
        assert isinstance(strategy, AddStrategy)
        
        strategy = CalculationFactory.create_calculation("addition")
        assert isinstance(strategy, AddStrategy)
    
    def test_create_calculation_subtract(self):
        """Test creating Subtract calculation strategy."""
        strategy = CalculationFactory.create_calculation("Sub")
        assert isinstance(strategy, SubtractStrategy)
        
        # Test case variations
        strategy = CalculationFactory.create_calculation("sub")
        assert isinstance(strategy, SubtractStrategy)
        
        strategy = CalculationFactory.create_calculation("subtract")
        assert isinstance(strategy, SubtractStrategy)
        
        strategy = CalculationFactory.create_calculation("subtraction")
        assert isinstance(strategy, SubtractStrategy)
    
    def test_create_calculation_multiply(self):
        """Test creating Multiply calculation strategy."""
        strategy = CalculationFactory.create_calculation("Multiply")
        assert isinstance(strategy, MultiplyStrategy)
        
        # Test case variations
        strategy = CalculationFactory.create_calculation("multiply")
        assert isinstance(strategy, MultiplyStrategy)
        
        strategy = CalculationFactory.create_calculation("mul")
        assert isinstance(strategy, MultiplyStrategy)
        
        strategy = CalculationFactory.create_calculation("multiplication")
        assert isinstance(strategy, MultiplyStrategy)
    
    def test_create_calculation_divide(self):
        """Test creating Divide calculation strategy."""
        strategy = CalculationFactory.create_calculation("Divide")
        assert isinstance(strategy, DivideStrategy)
        
        # Test case variations
        strategy = CalculationFactory.create_calculation("divide")
        assert isinstance(strategy, DivideStrategy)
        
        strategy = CalculationFactory.create_calculation("div")
        assert isinstance(strategy, DivideStrategy)
        
        strategy = CalculationFactory.create_calculation("division")
        assert isinstance(strategy, DivideStrategy)
    
    def test_create_calculation_invalid(self):
        """Test creating calculation with invalid operation type."""
        with pytest.raises(ValueError, match="Unsupported operation type: invalid"):
            CalculationFactory.create_calculation("invalid")
    
    @pytest.mark.parametrize("operation,a,b,expected", [
        ("Add", 5, 3, 8),
        ("Sub", 10, 4, 6),
        ("Multiply", 6, 7, 42),
        ("Divide", 15, 3, 5.0),
        ("add", 2.5, 1.5, 4.0),
        ("subtract", 8, 3, 5),
        ("multiply", 4, 2.5, 10.0),
        ("divide", 9, 3, 3.0),
    ])
    def test_execute_calculation(self, operation, a, b, expected):
        """Test direct execution of calculations through factory."""
        result = CalculationFactory.execute_calculation(operation, a, b)
        assert result == expected
    
    def test_execute_calculation_division_by_zero(self):
        """Test division by zero through factory."""
        with pytest.raises(ValueError, match="Cannot divide by zero!"):
            CalculationFactory.execute_calculation("Divide", 5, 0)
    
    def test_get_supported_operations(self):
        """Test getting list of supported operations."""
        operations = CalculationFactory.get_supported_operations()
        expected_operations = [
            "Add", "add", "addition",
            "Sub", "sub", "subtract", "subtraction", 
            "Multiply", "multiply", "mul", "multiplication",
            "Divide", "divide", "div", "division"
        ]
        
        for op in expected_operations:
            assert op in operations