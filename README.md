# OpenHands Playground

A playground repository for OpenHands development with a basic Python project structure.

## Project Structure

```
openhands_playground/
├── src/
│   └── openhands_playground/
│       ├── __init__.py
│       └── calculator.py
├── test/
│   ├── __init__.py
│   └── test_calculator.py
├── pyproject.toml
└── README.md
```

## Development Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management.

### Installation

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

### Development Tools

This project includes the following development tools:

- **pytest**: For running tests
- **ruff**: For linting and code formatting
- **mypy**: For static type checking

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=openhands_playground
```

### Code Quality

```bash
# Run linting
poetry run ruff check .

# Format code
poetry run ruff format .

# Run type checking
poetry run mypy src/
```

### Running All Quality Checks

```bash
# Run all quality checks
poetry run ruff check . && poetry run ruff format --check . && poetry run mypy src/ && poetry run pytest
```

## Usage

```python
from openhands_playground.calculator import add, subtract, multiply, divide

result = add(2, 3)  # Returns 5
```