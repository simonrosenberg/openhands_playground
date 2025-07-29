"""Tests for the calculator module."""

import pytest

from openhands_playground.calculator import add, divide, multiply, subtract


def test_add() -> None:
    """Test the add function."""
    assert add(1, 2) == 3
    assert add(1.5, 2.5) == 4.0
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract() -> None:
    """Test the subtract function."""
    assert subtract(3, 2) == 1
    assert subtract(5.5, 2.5) == 3.0
    assert subtract(1, 1) == 0
    assert subtract(0, 5) == -5


def test_multiply() -> None:
    """Test the multiply function."""
    assert multiply(2, 3) == 6
    assert multiply(2.5, 2) == 5.0
    assert multiply(-1, 1) == -1
    assert multiply(0, 5) == 0


def test_divide() -> None:
    """Test the divide function."""
    assert divide(6, 3) == 2
    assert divide(5, 2) == 2.5
    assert divide(-6, 3) == -2
    assert divide(0, 5) == 0


def test_divide_by_zero() -> None:
    """Test that dividing by zero raises an error."""
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
