# Contributing to mcp-web

Thank you for your interest in contributing to mcp-web! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Coding Standards](#coding-standards)
5. [Testing Guidelines](#testing-guidelines)
6. [Documentation](#documentation)
7. [Pull Request Process](#pull-request-process)
8. [Release Process](#release-process)

---

## Code of Conduct

This project follows a code of conduct to ensure a welcoming and inclusive environment for all contributors. Please:

- Be respectful and considerate
- Welcome newcomers and help them get started
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- OpenAI API key (for testing LLM features)

### Setup Development Environment

1. **Fork and clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/mcp-web.git
cd mcp-web
```

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install development dependencies**

```bash
pip install -e ".[dev]"
playwright install chromium
```

4. **Set up environment variables**

```bash
export OPENAI_API_KEY="sk-..."
export MCP_WEB_CACHE_DIR="/tmp/mcp-web-cache"
export MCP_WEB_METRICS_LOG_LEVEL="DEBUG"
```

5. **Run tests to verify setup**

```bash
pytest -v
```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:

- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions/improvements

### 2. Make Your Changes

- Write code following the [Coding Standards](#coding-standards)
- Add tests for new functionality
- Update documentation as needed
- Keep commits atomic and well-described

### 3. Test Your Changes

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit
pytest -m integration

# Run with coverage
pytest --cov=mcp_web --cov-report=html
```

### 4. Lint and Format

```bash
# Check code style
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

### 5. Commit Your Changes

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```bash
git commit -m "feat: add PDF OCR support"
git commit -m "fix: handle empty extraction results"
git commit -m "docs: update API documentation"
git commit -m "test: add chunker edge case tests"
```

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or modifications
- `chore`: Maintenance tasks

---

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use double quotes for strings

### Code Organization

```python
"""Module docstring explaining purpose.

Design decisions referenced: DD-XXX
"""

import standard_library
import third_party
from local_module import something

# Constants
CONSTANT_VALUE = 42

# Classes and functions with docstrings
class MyClass:
    """Class docstring with example.
    
    Example:
        >>> obj = MyClass()
        >>> obj.method()
    """
    
    def method(self, arg: str) -> bool:
        """Method docstring.
        
        Args:
            arg: Description
            
        Returns:
            Description
            
        Raises:
            Exception: When error occurs
        """
        pass
```

### Docstring Style

Use Google-style docstrings:

```python
def function(arg1: str, arg2: int) -> bool:
    """Short description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When validation fails

    Example:
        >>> function("test", 42)
        True
    """
    pass
```

### Type Hints

Always use type hints:

```python
from typing import List, Optional, Dict, Any

def fetch_urls(
    urls: List[str],
    timeout: Optional[int] = None,
) -> Dict[str, Any]:
    """Fetch multiple URLs."""
    pass
```

### Error Handling

- Use specific exception types
- Never use bare `except`
- Log errors with context
- Clean up resources in `finally` or use context managers

```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error("operation_failed", error=str(e), context={"url": url})
    raise
finally:
    cleanup()
```

---

## Testing Guidelines

### Test Structure

```python
"""Tests for module_name."""

import pytest
from module_name import function_to_test

class TestFunctionName:
    """Tests for function_name."""
    
    @pytest.fixture
    def sample_data(self):
        """Fixture for test data."""
        return {"key": "value"}
    
    def test_happy_path(self, sample_data):
        """Test normal operation."""
        result = function_to_test(sample_data)
        assert result is not None
    
    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            function_to_test(None)
```

### Test Categories

Mark tests appropriately:

```python
@pytest.mark.unit
def test_unit_level():
    """Fast, isolated unit test."""
    pass

@pytest.mark.integration
def test_integration_level():
    """Integration test with dependencies."""
    pass

@pytest.mark.slow
def test_slow_operation():
    """Test that takes > 1 second."""
    pass

@pytest.mark.requires_api
def test_with_external_api():
    """Test requiring external API."""
    pass
```

### Test Coverage

- Aim for >90% code coverage
- Test both happy paths and edge cases
- Test error conditions
- Use mocks for external dependencies

```python
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_with_mock():
    """Test using mock."""
    with patch("module.external_call", new_callable=AsyncMock) as mock:
        mock.return_value = "mocked result"
        result = await function_under_test()
        assert result == "expected"
        mock.assert_called_once()
```

---

## Documentation

### When to Update Documentation

Update documentation when:

- Adding new features or tools
- Changing existing APIs
- Adding configuration options
- Fixing bugs that affect behavior
- Adding examples or use cases

### Documentation Files

- **README.md**: User-facing overview and quick start
- **docs/ARCHITECTURE.md**: System design and decisions
- **docs/API.md**: Complete API reference
- **docs/DECISIONS.md**: Design decision log
- **Docstrings**: All public functions, classes, modules

### Writing Good Documentation

1. **Be Clear and Concise**
   - Use simple language
   - Provide examples
   - Explain "why" not just "what"

2. **Keep It Updated**
   - Update docs in the same PR as code changes
   - Mark deprecated features

3. **Include Examples**
   - Show realistic use cases
   - Provide copy-pasteable code

---

## Pull Request Process

### Before Submitting

- [ ] Tests pass locally (`pytest`)
- [ ] Code is formatted (`ruff format`)
- [ ] Linting passes (`ruff check`)
- [ ] Type checking passes (`mypy`)
- [ ] Documentation is updated
- [ ] Commit messages follow conventions

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass
- [ ] No new warnings

## Related Issues
Closes #123
```

### Review Process

1. Automated checks must pass (CI/CD)
2. At least one maintainer review required
3. Address review feedback
4. Squash commits before merge (if requested)

---

## Release Process

### Version Numbers

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create release branch: `release/v0.x.0`
4. Run full test suite
5. Update documentation
6. Create GitHub release with notes
7. Tag release: `git tag v0.x.0`
8. Push to PyPI (if applicable)

---

## Getting Help

- **Questions**: Open a [Discussion](https://github.com/geehexx/mcp-web/discussions)
- **Bugs**: Open an [Issue](https://github.com/geehexx/mcp-web/issues)
- **Feature Requests**: Open an Issue with `enhancement` label

---

## Recognition

Contributors will be:

- Listed in the project README
- Credited in release notes
- Acknowledged in commit history

Thank you for contributing to mcp-web! 🎉
