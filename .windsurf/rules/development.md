---
trigger: always_on
---

# MCP Web Development Rules

## Code Style & Standards

### Python Code Style
- Follow PEP 8 style guide strictly
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use double quotes for strings
- Import order: standard library → third-party → local modules

### Docstrings
- Use Google-style docstrings for all public functions, classes, and modules
- Include Args, Returns, Raises, and Example sections
- Reference design decisions (DD-XXX) in docstrings when applicable

### Type Hints
- Always use type hints, including for return types
- Use `Optional[T]` for nullable types
- Use `List[T]`, `Dict[K, V]` for containers
- Import from `typing` module as needed

### Error Handling
- Use specific exception types, never bare `except:`
- Log errors with context using structlog
- Clean up resources in `finally` blocks or use context managers
- Provide user-friendly error messages in streaming output

## Async/Await Patterns

### Async Functions
- Use `async def` for all I/O operations
- Always `await` async function calls
- Use `asyncio.gather()` for concurrent operations
- Implement proper cleanup with `async with` context managers

### Async Generators
- Use `AsyncIterator[str]` for streaming responses
- Yield chunks incrementally for better UX
- Handle exceptions within generator

## Security Guidelines

### LLM Security (OWASP LLM Top 10)

#### Prompt Injection Prevention (LLM01:2025)
- Never pass untrusted content directly to LLM without validation
- Separate user instructions from data using clear delimiters
- Implement output validation to detect instruction leakage
- Use system prompts that explicitly resist instruction override

#### Content Filtering
- Strip HTML comments and script tags from extracted content
- Validate and sanitize all URLs before fetching
- Implement rate limiting for API calls
- Set maximum token limits to prevent unbounded consumption

#### API Key Security
- Never hardcode API keys in code
- Always use environment variables: `os.getenv('OPENAI_API_KEY')`
- Never log or return API keys in outputs
- Use secure storage for production deployments

### Input Validation
- Validate all URLs before fetching (http/https only)
- Sanitize filenames to prevent path traversal
- Limit input sizes (URLs, queries, content length)
- Implement timeout limits for all operations

### Cache Security
- Use collision-resistant cache keys (hashing)
- Set appropriate cache directory permissions (700)
- Implement TTL to prevent stale data attacks
- Validate cached data before use

## Testing Requirements

### Test Organization
```
tests/
├── unit/           # Fast, isolated unit tests
├── integration/    # Multi-component integration tests
├── security/       # Security-focused tests (OWASP)
├── golden/         # Regression tests with static data
├── live/           # Tests requiring network/API
└── benchmarks/     # Performance benchmarks
```

### Test Markers
Use pytest markers to categorize tests:
- `@pytest.mark.unit` - Unit tests (fast)
- `@pytest.mark.integration` - Integration tests
- `@pytest.mark.security` - Security tests
- `@pytest.mark.golden` - Golden/regression tests
- `@pytest.mark.live` - Requires network
- `@pytest.mark.requires_api` - Requires API key
- `@pytest.mark.slow` - Takes > 1 second
- `@pytest.mark.benchmark` - Performance benchmark

### Test Coverage
- Aim for >90% code coverage
- Test both happy paths and error cases
- Include edge cases (empty input, very large input, malformed input)
- Test security vulnerabilities (prompt injection, XSS, path traversal)

### Golden Tests
- Use static HTML samples from `tests/fixtures/golden_data.py`
- Verify extraction against expected results
- Test deterministic behavior with temperature=0

### Security Tests
- Test prompt injection detection and mitigation
- Test input validation (URLs, filenames, paths)
- Test output sanitization (no system prompts, no API keys)
- Test resource limits (rate limiting, token limits)

## Configuration Management

### Pydantic Settings
- Use nested `BaseSettings` classes for configuration groups
- Add `Field()` with descriptions and validation
- Use `env_prefix` for environment variable mapping
- Provide sensible defaults

### Environment Variables
- Prefix all environment variables with `MCP_WEB_`
- Document all configuration options in ARCHITECTURE.md
- Provide runtime overrides for testing

## Metrics & Logging

### Structured Logging
- Use structlog for all logging
- Include context in all log messages
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Log performance metrics for key operations

### Metrics Collection
- Record metrics for all major operations (fetch, extract, chunk, summarize)
- Track duration, token usage, success/failure rates
- Use `MetricsCollector` singleton via `get_metrics_collector()`
- Export metrics for analysis

## Design Decisions

### Referencing Decisions
- Reference design decisions in code comments and docstrings
- Format: `DD-XXX` where XXX is the decision number
- All design decisions documented in `docs/DECISIONS.md`

### Making New Decisions
- Document all architectural choices in `docs/DECISIONS.md`
- Include: Context, Decision, Rationale, Alternatives, Consequences
- Assign sequential DD-XXX identifiers
- Update ARCHITECTURE.md as needed

## Module-Specific Patterns

### Fetcher Module
- Try httpx first, fallback to Playwright on failure
- Implement exponential backoff for retries
- Cache responses with ETag/Last-Modified support
- Record fetch metrics (duration, method, size)

### Extractor Module
- Use trafilatura with `favor_recall=True` for HTML
- Strip HTML comments and script tags for security
- Extract links for potential recursive following
- Preserve code blocks and formatting

### Chunker Module
- Default to hierarchical strategy for structured content
- Respect code block boundaries (don't split code)
- Add overlap between chunks (default 50 tokens)
- Track chunk metadata (position, section, heading)

### Summarizer Module
- Use map-reduce for documents > 8k tokens
- Set temperature=0 for deterministic testing
- Implement streaming output via `AsyncIterator[str]`
- Track token usage for cost analysis

### Cache Module
- Use collision-resistant keys (sha256 hashing)
- Implement TTL-based expiration (default 7 days)
- Support LRU/LFU eviction policies
- Track cache hit/miss ratios

## Performance Optimization

### Concurrency
- Use `max_concurrent` to limit parallel operations
- Implement semaphore-based rate limiting
- Use `asyncio.gather()` for concurrent tasks
- Handle timeouts gracefully

### Memory Management
- Avoid loading entire documents into memory when possible
- Stream large responses incrementally
- Clean up resources in `finally` blocks
- Implement size limits for cached data

### Token Efficiency
- Use efficient chunking strategies
- Truncate to token limits before sending to LLM
- Cache summarization results
- Track token usage metrics

## Documentation

### Code Comments
- Explain "why" not "what"
- Reference design decisions
- Document security considerations
- Include examples for complex logic

### Module Documentation
- Every module must have a docstring explaining its purpose
- Reference relevant design decisions
- Include usage examples
- Document security considerations if applicable

### API Documentation
- Keep `docs/API.md` up to date with all public APIs
- Include parameter descriptions, types, and examples
- Document exceptions and error conditions
- Provide usage examples

## Pull Request Guidelines

### Before Submitting
- Run all tests: `pytest`
- Run linting: `ruff check src/ tests/`
- Run type checking: `mypy src/`
- Run security scan: `bandit -r src/`
- Update documentation if needed

### Commit Messages
Use conventional commits format:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `test:` - Test additions/modifications
- `refactor:` - Code refactoring
- `security:` - Security improvements

Example: `feat: add prompt injection detection for LLM inputs`

### Code Review Checklist
- [ ] Tests added/updated and passing
- [ ] Security considerations addressed
- [ ] Documentation updated
- [ ] Type hints present
- [ ] Error handling implemented
- [ ] Metrics/logging added
- [ ] Design decisions documented if needed

## Common Patterns

### Resource Cleanup
```python
async def process_urls(urls: List[str]) -> None:
    """Process URLs with proper cleanup."""
    fetcher = URLFetcher(config.fetcher)
    try:
        results = await fetcher.fetch_multiple(urls)
        # Process results...
    finally:
        await fetcher.close()
```

### Error Context
```python
try:
    result = await risky_operation()
except SpecificError as e:
    logger.error(
        "operation_failed",
        error=str(e),
        context={"url": url, "attempt": attempt},
    )
    raise
```

### Streaming Output
```python
async def generate_summary() -> AsyncIterator[str]:
    """Generate streaming summary."""
    try:
        yield "## Summary\n\n"
        
        async for chunk in llm_stream:
            yield chunk
            
        yield "\n\n---\n\nGenerated by mcp-web"
    except Exception as e:
        logger.error("summary_failed", error=str(e))
        yield f"\n\n**Error:** {e}"
```

## Security Checklist

For any code that:
- Accepts user input → Validate and sanitize
- Makes external requests → Set timeouts and limits
- Parses external content → Strip dangerous elements
- Calls LLM APIs → Separate instructions from data
- Stores data → Implement TTL and size limits
- Returns output → Filter sensitive information

## Performance Checklist

For any code that:
- Processes large data → Stream incrementally
- Makes multiple similar calls → Cache results
- Performs I/O → Use async/await
- Runs concurrently → Implement rate limiting
- Counts tokens → Use efficient tiktoken
- Chunks text → Choose appropriate strategy