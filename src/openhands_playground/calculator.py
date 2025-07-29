"""Simple calculator module."""

from typing import Union


def add(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Add two numbers together.

    Args:
    ----
        a: First number
        b: Second number

    Returns:
    -------
        The sum of a and b

    """
    return a + b


def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Subtract b from a.

    Args:
    ----
        a: First number
        b: Second number

    Returns:
    -------
        The result of a - b

    """
    return a - b


def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Multiply two numbers.

    Args:
    ----
        a: First number
        b: Second number

    Returns:
    -------
        The product of a and b

    """
    return a * b


def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """
    Divide a by b.

    Args:
    ----
        a: First number
        b: Second number

    Returns:
    -------
        The result of a / b

    Raises:
    ------
        ZeroDivisionError: If b is zero

    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b
