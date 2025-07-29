"""Tests for the calculator module."""

import pytest
from openhands_playground.calculator import add, divide, multiply, subtract


class TestCalculator:
    """Test cases for calculator functions."""

    def test_add(self):
        """Test addition function."""
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
        assert add(0, 0) == 0
        assert add(1.5, 2.5) == 4.0

    def test_subtract(self):
        """Test subtraction function."""
        assert subtract(5, 3) == 2
        assert subtract(1, 1) == 0
        assert subtract(0, 5) == -5
        assert subtract(2.5, 1.5) == 1.0

    def test_multiply(self):
        """Test multiplication function."""
        assert multiply(2, 3) == 6
        assert multiply(-2, 3) == -6
        assert multiply(0, 5) == 0
        assert multiply(1.5, 2) == 3.0

    def test_divide(self):
        """Test division function."""
        assert divide(6, 2) == 3
        assert divide(5, 2) == 2.5
        assert divide(-6, 2) == -3
        assert divide(0, 5) == 0

    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(5, 0)
