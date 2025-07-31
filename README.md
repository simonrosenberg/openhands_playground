# OpenHands Playground

A playground repository for OpenHands development featuring a flexible LLM factory pattern implementation.

## Project Structure

```
openhands_playground/
├── src/
│   └── openhands_playground/
│       ├── __init__.py
│       └── llm/
│           ├── __init__.py
│           ├── base.py
│           ├── factory.py
│           └── llms/
│               ├── __init__.py
│               ├── mock_llm.py
│               └── openai_llm.py
├── test/
│   ├── __init__.py
│   └── test_llm.py
├── .env.example
├── pyproject.toml
└── README.md
```

## Development Setup

This project uses [Poetry](https://python-poetry.org/) for dependency management.

### Pre-commit Hooks

This repository uses pre-commit hooks to ensure code quality. The hooks include:

- **ruff**: A fast Python linter and formatter
- **mypy**: Static type checking for Python

### Installation

1. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

4. Install the git hooks:
   ```bash
   pre-commit install
   ```

### Running the Hooks

The hooks will run automatically on git commit. To run them manually:

```bash
pre-commit run --all-files
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

## Continuous Integration

This project uses GitHub Actions for CI/CD. The workflow runs on Python 3.8, 3.9, 3.10, and 3.11.

### CI Configuration

The CI workflow includes:
- Dependency installation with Poetry
- Running tests with pytest
- Code linting with ruff
- Type checking with mypy

### OpenAI API Key for CI

The CI workflow requires access to the OpenAI API key to run integration tests. The API key should be configured as a GitHub repository secret:

1. Go to your repository settings
2. Navigate to "Secrets and variables" → "Actions"
3. Add a new repository secret named `OPENAI_API_KEY`
4. Set the value to your OpenAI API key

The tests are designed to gracefully skip OpenAI integration tests if the API key is not available, so the CI will still pass without the secret, but some tests will be skipped.

## LLM Usage

This package provides a factory pattern for creating and using different LLM providers.

### Basic Usage

```python
from openhands_playground.llm import LLMFactory

# Create a mock LLM for testing
llm = LLMFactory.create_mock_llm()

# Generate text
response = llm.generate("Tell me a joke")
print(response)

# Chat with messages
messages = [
    {"role": "user", "content": "Hello, how are you?"}
]
response = llm.chat(messages)
print(response)
```

### OpenAI Integration

```python
from openhands_playground.llm import LLMFactory

# Create OpenAI LLM (requires API key)
llm = LLMFactory.create_openai_llm(
    model_name="gpt-3.5-turbo",
    api_key="your-api-key-here"
)

# Or use environment variable OPENAI_API_KEY
llm = LLMFactory.create_openai_llm()

# Generate text with parameters
response = llm.generate(
    "Explain quantum computing",
    max_tokens=100,
    temperature=0.7
)
print(response)
```

### Environment Variables

Create a `.env` file in your project root:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### Available Providers

```python
from openhands_playground.llm import LLMFactory

# List available providers
providers = LLMFactory.get_available_providers()
print(providers)  # ['mock', 'openai']

# Create LLM by provider name
llm = LLMFactory.create_llm("mock", model_name="test-model")
```

### Custom Providers

You can register custom LLM implementations:

```python
from openhands_playground.llm import LLMFactory, BaseLLM

class CustomLLM(BaseLLM):
    def generate(self, prompt, **kwargs):
        return f"Custom response to: {prompt}"
    
    def chat(self, messages, **kwargs):
        return "Custom chat response"

# Register the custom provider
LLMFactory.register_provider("custom", CustomLLM)

# Use the custom provider
llm = LLMFactory.create_llm("custom", model_name="custom-model")
```
