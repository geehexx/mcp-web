---
trigger: glob
globs: ["**/*.py"]
---

# Python Code Standards

## Code Style (PEP 8)

- Maximum line length: 100 characters
- Use double quotes for strings
- 4 spaces for indentation (never tabs)
- Two blank lines between top-level definitions
- One blank line between methods
- Import order: standard library → third-party → local modules

## Type Hints (PEP 484)

**Always use type hints for:**
- Function parameters
- Return values
- Class attributes
- Complex data structures

```python
from typing import List, Dict, Optional, AsyncIterator

async def fetch_urls(
    urls: List[str],
    timeout: int = 30
) -> Dict[str, str]:
    """Fetch multiple URLs concurrently."""
    ...
```

**For async code:**
```python
from typing import AsyncIterator

async def stream_data() -> AsyncIterator[str]:
    """Stream data incrementally."""
    ...
```

## Docstrings (Google Style)

**All public functions, classes, and modules must have docstrings:**

```python
def process_content(text: str, max_length: int = 1000) -> str:
    """Process and truncate text content.
    
    Args:
        text: Input text to process
        max_length: Maximum allowed length
        
    Returns:
        Processed and truncated text
        
    Raises:
        ValueError: If text is empty
        
    Example:
        >>> process_content("Hello world", max_length=5)
        'Hello'
    """
    ...
```

## Error Handling

**Never use bare except:**
```python
# BAD
try:
    risky_operation()
except:
    pass

# GOOD
try:
    result = risky_operation()
except SpecificError as e:
    logger.error("operation_failed", error=str(e))
    raise
```

**Always clean up resources:**
```python
# Use context managers
async with resource as r:
    await r.process()

# Or explicit finally
try:
    resource = acquire()
    await process(resource)
finally:
    await resource.close()
```

## Async/Await Best Practices

**Use async for I/O operations only:**
```python
# GOOD - Non-blocking I/O
async def fetch_url(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

# BAD - Blocking operation in async
async def compute_hash(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()  # Blocks event loop!
```

**Concurrent operations with asyncio.gather:**
```python
# Process multiple tasks concurrently
results = await asyncio.gather(
    fetch_url(url1),
    fetch_url(url2),
    fetch_url(url3),
    return_exceptions=True  # Don't fail all on one error
)
```

**Use semaphores for rate limiting:**
```python
semaphore = asyncio.Semaphore(5)  # Max 5 concurrent

async def limited_fetch(url: str) -> str:
    async with semaphore:
        return await fetch_url(url)
```

## Logging (structlog)

**Use structured logging with context:**
```python
import structlog

logger = structlog.get_logger()

logger.info(
    "fetch_complete",
    url=url,
    status_code=response.status_code,
    duration_ms=duration,
    from_cache=cached,
)
```

**Log levels:**
- DEBUG: Detailed diagnostic information
- INFO: Normal operation events
- WARNING: Unexpected but handled situations
- ERROR: Serious problems requiring attention

## Testing (pytest)

**Follow AAA pattern:**
```python
def test_token_counting():
    # Arrange
    counter = TokenCounter()
    text = "Hello world"
    
    # Act
    count = counter.count_tokens(text)
    
    # Assert
    assert count > 0
    assert count < 10
```

**Use parametrize for multiple cases:**
```python
@pytest.mark.parametrize("input,expected", [
    ("Hello", 1),
    ("Hello world", 2),
    ("", 0),
])
def test_word_count(input, expected):
    assert count_words(input) == expected
```

**Async tests:**
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_operation()
    assert result is not None
```

## Performance

**Avoid premature optimization, but:**
- Use list comprehensions over loops when appropriate
- Cache expensive computations
- Stream large data instead of loading into memory
- Use generators for large sequences
- Profile before optimizing

## Security

**Input validation:**
```python
def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
```

**Never log sensitive data:**
```python
# BAD
logger.info(f"API key: {api_key}")

# GOOD
logger.info("api_key_loaded", key_prefix=api_key[:4])
```

## Common Patterns

**Singleton pattern:**
```python
_instance = None

def get_instance():
    global _instance
    if _instance is None:
        _instance = MyClass()
    return _instance
```

**Factory pattern:**
```python
def create_fetcher(config: FetcherSettings) -> URLFetcher:
    if config.use_playwright:
        return PlaywrightFetcher(config)
    return HTTPXFetcher(config)
```

**Context manager:**
```python
class ResourceManager:
    async def __aenter__(self):
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
```
