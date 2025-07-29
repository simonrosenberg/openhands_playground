# OpenHands Playground

A Python project for OpenHands playground.

## Setup

This project uses Poetry for dependency management.

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

## Development

### Running Tests

```bash
pytest
```

### Linting

```bash
ruff check .
```

### Type Checking

```bash
mypy src
```

## Project Structure

- `src/openhands_playground/`: Source code
- `test/`: Test files
