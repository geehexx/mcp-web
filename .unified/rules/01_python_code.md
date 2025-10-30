---
description: "Python code style type hints async patterns and best practices"
status: "active"
tags: ["python", "code", "style", "type-hints", "async"]
type: "rule"

windsurf:
  trigger: "glob"
  globs: "*.py, **/*.py"

cursor:
  alwaysApply: false
  globs: "*.py, **/*.py"

ide:
  hidden_sections:
    - "Rule Metadata"
  metadata:
    file: "01_python_code.md"
    trigger: "glob (Windsurf) / globs (Cursor)"
    estimated_tokens: 2200
    last_updated: "2025-10-22"
    status: "Active"
    can_be_mentioned: "Yes (hybrid loading)"
    topics_covered:
      - "PEP 8 style"
      - "Type hints (PEP 484)"
      - "Async/await patterns"
      - "Docstrings (Google style)"
    workflow_references:
      - "/implement - Always loaded when editing Python"
    dependencies:
      - "Source: 02_python_standards.md"
---
# Python Code Standards

## 2.1 Code Style (PEP 8)

**Reference:** [PEP 8 Style Guide](https://peps.python.org/pep-0008/) (October 2025)

- **Line length:** 100 characters maximum
- **Quotes:** Double quotes for strings, single for dictionary keys
- **Import order:**
  1. Standard library
  2. Third-party packages
  3. Local modules
- **Naming conventions:**
  - `snake_case` for functions, variables, modules
  - `PascalCase` for classes
  - `UPPER_CASE` for constants
  - `_leading_underscore` for internal/private

## 2.2 Type Hints (PEP 484)

**Reference:** [PEP 484 Type Hints](https://peps.python.org/pep-0484/)

- **Always use type hints** on all function signatures
- **Return types:** Always specify, use `-> None` for procedures
- **Optional types:** Use `Optional[T]` or `T | None` (Python 3.10+)
- **Collections:** Use `list[str]`, `dict[str, int]` (Python 3.9+ built-ins)
- **Type aliases:** Define for complex types

```python
from typing import Optional, AsyncIterator
from collections.abc import Callable

# Good examples
def process_url(url: str, timeout: int = 30) -> dict[str, str]:
    """Process URL with type hints."""
    pass

async def fetch_multiple(
    urls: list[str],
    callback: Optional[Callable[[str], None]] = None
) -> list[dict[str, str]]:
    """Async function with type hints."""
    pass

async def stream_response() -> AsyncIterator[str]:
    """Async generator with type hint."""
    yield "chunk"
```

## 2.3 Docstrings (Google Style)

**Reference:** [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

- **All public functions, classes, modules** must have docstrings
- **Format:** Google style (not NumPy or Sphinx)
- **Sections:** Args, Returns, Raises, Yields, Example
- **ADR references:** Reference decisions where applicable

```python
def summarize_content(
    content: str,
    query: Optional[str] = None,
    max_tokens: int = 1000
) -> str:
    """Summarize content with optional query focus.

    Implements map-reduce summarization strategy per ADR-0006.
    Uses query-aware chunking per ADR-0003.

    Args:
        content: The text content to summarize
        query: Optional query to focus the summary
        max_tokens: Maximum tokens in summary (default: 1000)

    Returns:
        Generated summary as string

    Raises:
        ValueError: If content is empty or too short
        TokenLimitError: If content exceeds maximum processable size

    Example:
        >>> summary = summarize_content(
        ...     "Long article text...",
        ...     query="security best practices"
        ... )
        >>> print(summary)
        'Summary focused on security...'
    """
    pass
```

## 2.4 Async/Await Patterns

**Reference:** [Real Python - Async IO](https://realpython.com/async-io-python/) (October 2025)

- **Use `async def` only for I/O operations**
- **Always `await` async calls** - never block in async context
- **Concurrency:** Use `asyncio.gather()` for parallel operations
- **Resource cleanup:** Use `async with` context managers
- **Semaphores:** Use for rate limiting concurrent operations

```python
import asyncio
from typing import AsyncIterator

# Proper async function
async def fetch_url(url: str) -> bytes:
    """Async I/O operation."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content

# Concurrent operations
async def fetch_multiple(urls: list[str]) -> list[bytes]:
    """Fetch multiple URLs concurrently."""
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return [r for r in results if not isinstance(r, Exception)]

# Rate-limited concurrency
async def process_with_limit(
    items: list[str],
    max_concurrent: int = 5
) -> list[str]:
    """Process items with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def process_one(item: str) -> str:
        async with semaphore:
            return await process_item(item)

    return await asyncio.gather(*[process_one(item) for item in items])

# Async generator (streaming)
async def stream_chunks(data: str) -> AsyncIterator[str]:
    """Stream data in chunks."""
    chunk_size = 100
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        yield chunk
        await asyncio.sleep(0)  # Allow other tasks to run

# Proper cleanup
async def process_with_cleanup():
    """Resource cleanup in async context."""
    client = HttpxClient()
    try:
        result = await client.fetch()
        return result
    finally:
        await client.close()
```

## 2.5 Error Handling

- **Specific exceptions:** Never use bare `except:`
- **Context logging:** Use structlog with context
- **Resource cleanup:** Use `finally` or context managers
- **User-friendly errors:** Provide actionable error messages in streaming output

```python
import structlog

logger = structlog.get_logger()

async def safe_operation(url: str) -> dict[str, str]:
    """Operation with proper error handling."""
    try:
        result = await risky_operation(url)
        return result
    except httpx.TimeoutException as e:
        logger.error(
            "operation_timeout",
            url=url,
            timeout=30,
            error=str(e)
        )
        raise TimeoutError(f"Request to {url} timed out after 30s") from e
    except httpx.HTTPError as e:
        logger.error(
            "http_error",
            url=url,
            status_code=getattr(e.response, 'status_code', None),
            error=str(e)
        )
        raise
    except Exception as e:
        logger.exception(
            "unexpected_error",
            url=url,
            error_type=type(e).__name__
        )
        raise RuntimeError(f"Unexpected error processing {url}") from e
```

## 2.6 Performance Patterns

### Efficient Data Structures

```python
# Use generators for large datasets
def process_large_file(path: str) -> Iterator[str]:
    """Process file line by line (memory efficient)."""
    with open(path) as f:
        for line in f:
            yield process_line(line)

# Use sets for membership testing
known_urls = set(url_list)  # O(1) lookup vs O(n) for list

# Use dict comprehensions for transformations
result = {k: transform(v) for k, v in data.items() if condition(v)}
```

### Caching

```python
from functools import lru_cache
import functools

# Function result caching
@lru_cache(maxsize=1000)
def expensive_computation(n: int) -> int:
    """Cache expensive computation results."""
    return complex_calculation(n)

# Async caching (manual)
_cache: dict[str, str] = {}

async def cached_fetch(url: str) -> str:
    """Fetch with caching."""
    if url in _cache:
        return _cache[url]

    result = await fetch(url)
    _cache[url] = result
    return result
```

## 2.7 Code Organization

### Module Structure

```python
"""Module docstring explaining purpose.

References:
    - ADR-0001: Architecture decision
    - https://docs.example.com/api
"""

# Imports (standard, third-party, local)
import asyncio
from typing import Optional

import httpx
import structlog

from mcp_web.config import Settings
from mcp_web.utils import validate_url

# Constants
DEFAULT_TIMEOUT = 30
MAX_RETRIES = 3

# Module-level logger
logger = structlog.get_logger(__name__)

# Classes and functions
class Fetcher:
    """Class for fetching URLs."""
    pass

def helper_function() -> None:
    """Helper function."""
    pass
```

## 2.8 Testing Patterns

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.unit
@pytest.mark.asyncio
async def test_async_function():
    """Test async function with proper setup."""
    # Arrange
    fetcher = URLFetcher(config)

    # Act
    result = await fetcher.fetch("https://example.com")

    # Assert
    assert result.status_code == 200
    assert len(result.content) > 0

@pytest.mark.unit
def test_with_mock():
    """Test with mocking."""
    with patch('mcp_web.fetcher.httpx.AsyncClient') as mock_client:
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

        # Test code here
        pass

@pytest.fixture
async def async_fixture():
    """Async fixture with cleanup."""
    resource = await setup_resource()
    yield resource
    await resource.cleanup()
```

## 2.9 Common Anti-Patterns to Avoid

```python
# BAD: Mutable default argument
def process(items: list[str] = []):  # ❌
    items.append("new")
    return items

# GOOD: Use None with initialization
def process(items: Optional[list[str]] = None) -> list[str]:  # ✅
    if items is None:
        items = []
    items.append("new")
    return items

# BAD: Bare except
try:
    risky_operation()
except:  # ❌
    pass

# GOOD: Specific exception
try:
    risky_operation()
except ValueError as e:  # ✅
    logger.error("invalid_value", error=str(e))
    raise

# BAD: Not awaiting async function
result = fetch_data()  # ❌ Returns coroutine, doesn't execute

# GOOD: Await async function
result = await fetch_data()  # ✅

# BAD: Blocking in async function
async def bad_async():
    time.sleep(1)  # ❌ Blocks event loop

# GOOD: Async sleep
async def good_async():
    await asyncio.sleep(1)  # ✅
```

## 2.10 Quality Checklist

Before committing Python code:

- ✅ Type hints on all function signatures
- ✅ Google-style docstrings on public APIs
- ✅ Proper async/await usage (no blocking in async)
- ✅ Specific exception handling (no bare except)
- ✅ Structured logging with context
- ✅ Tests written (TDD) with appropriate markers
- ✅ `task lint` passes (ruff + mypy)
- ✅ `task test:unit` passes

## Rule Metadata

**File:** `01_python_code.yaml`
**Trigger:** glob (Windsurf) / globs (Cursor)
**Estimated Tokens:** ~2,200
**Last Updated:** 2025-10-22
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- PEP 8 style
- Type hints (PEP 484)
- Async/await patterns
- Docstrings (Google style)

**Workflow References:**

- /implement - Always loaded when editing Python

**Dependencies:**

- Source: 02_python_standards.md
