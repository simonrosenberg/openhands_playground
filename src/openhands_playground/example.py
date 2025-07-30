"""Example module to demonstrate pre-commit hooks."""

from typing import List, Optional


def add_numbers(a: int, b: int) -> int:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of the two numbers
    """
    return a + b


def get_greeting(name: Optional[str] = None) -> str:
    """Return a greeting message.

    Args:
        name: Name to greet, defaults to "World"

    Returns:
        Greeting message
    """
    if name is None:
        name = "World"
    return f"Hello, {name}!"


def process_items(items: List[str]) -> List[str]:
    """Process a list of items.

    Args:
        items: List of items to process

    Returns:
        Processed items
    """
    return [item.strip().upper() for item in items if item.strip()]
