# OpenHands Playground

A playground repository for OpenHands.

## Development Setup

### Pre-commit Hooks

This repository uses pre-commit hooks to ensure code quality. The hooks include:

- **ruff**: A fast Python linter and formatter
- **mypy**: Static type checking for Python

### Installation

1. Install pre-commit:

```bash
pip install pre-commit
```

2. Install the git hooks:

```bash
pre-commit install
```

### Running the Hooks

The hooks will run automatically on git commit. To run them manually:

```bash
pre-commit run --all-files
```
