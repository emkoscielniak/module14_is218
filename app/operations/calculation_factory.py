# app/operations/calculation_factory.py

from abc import ABC, abstractmethod
from typing import Union
from app.operations import add, subtract, multiply, divide

Number = Union[int, float]

class CalculationStrategy(ABC):
    """Abstract base class for calculation strategies."""
    
    @abstractmethod
    def execute(self, a: Number, b: Number) -> Number:
        """Execute the calculation strategy."""
        pass

class AddStrategy(CalculationStrategy):
    """Strategy for addition operations."""
    
    def execute(self, a: Number, b: Number) -> Number:
        return add(a, b)

class SubtractStrategy(CalculationStrategy):
    """Strategy for subtraction operations."""
    
    def execute(self, a: Number, b: Number) -> Number:
        return subtract(a, b)

class MultiplyStrategy(CalculationStrategy):
    """Strategy for multiplication operations."""
    
    def execute(self, a: Number, b: Number) -> Number:
        return multiply(a, b)

class DivideStrategy(CalculationStrategy):
    """Strategy for division operations."""
    
    def execute(self, a: Number, b: Number) -> Number:
        return divide(a, b)

class CalculationFactory:
    """Factory class for creating and executing calculation strategies."""
    
    _strategies = {
        "Add": AddStrategy,
        "add": AddStrategy,
        "addition": AddStrategy,
        "Sub": SubtractStrategy,
        "sub": SubtractStrategy,
        "subtract": SubtractStrategy,
        "subtraction": SubtractStrategy,
        "Multiply": MultiplyStrategy,
        "multiply": MultiplyStrategy,
        "mul": MultiplyStrategy,
        "multiplication": MultiplyStrategy,
        "Divide": DivideStrategy,
        "divide": DivideStrategy,
        "div": DivideStrategy,
        "division": DivideStrategy,
    }
    
    @classmethod
    def create_calculation(cls, operation_type: str) -> CalculationStrategy:
        """
        Create a calculation strategy based on the operation type.
        
        Args:
            operation_type (str): The type of operation (Add, Sub, Multiply, Divide)
            
        Returns:
            CalculationStrategy: The appropriate strategy instance
            
        Raises:
            ValueError: If the operation type is not supported
        """
        strategy_class = cls._strategies.get(operation_type)
        if strategy_class is None:
            raise ValueError(f"Unsupported operation type: {operation_type}")
        
        return strategy_class()
    
    @classmethod
    def execute_calculation(cls, operation_type: str, a: Number, b: Number) -> Number:
        """
        Execute a calculation using the factory pattern.
        
        Args:
            operation_type (str): The type of operation
            a (Number): First operand
            b (Number): Second operand
            
        Returns:
            Number: The result of the calculation
        """
        strategy = cls.create_calculation(operation_type)
        return strategy.execute(a, b)
    
    @classmethod
    def get_supported_operations(cls) -> list:
        """
        Get a list of all supported operation types.
        
        Returns:
            list: List of supported operation names
        """
        return list(cls._strategies.keys())