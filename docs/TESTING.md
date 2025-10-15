# Testing & Validation Strategy

**Project:** mcp-web
**Version:** 0.2.0
**Last Updated:** 2025-10-15

---

## Table of Contents

1. [Overview](#overview)
2. [Test Categories](#test-categories)
3. [Security Testing](#security-testing)
4. [Golden Tests](#golden-tests)
5. [Live Tests](#live-tests)
6. [Benchmarks](#benchmarks)
7. [Static Analysis](#static-analysis)
8. [Running Tests](#running-tests)
9. [CI/CD Integration](#cicd-integration)

---

## Overview

The mcp-web project implements a comprehensive multi-layered testing strategy focused on:

- **Deterministic behavior** via golden tests and fixed random seeds
- **Security** via OWASP LLM Top 10 focused tests
- **Performance** via benchmarks and profiling
- **Reliability** via live tests against static URLs
- **Code quality** via static analysis tools

### Test Pyramid

```
 Live Tests (Slow, Few)
 ┌────────────────────────┐
 │ Network + API required │
 └────────────────────────┘
 
 Integration Tests (Medium)
 ┌──────────────────────────────┐
 │ Multi-component testing │
 └──────────────────────────────┘
 
 Unit Tests (Fast, Many)
 ┌────────────────────────────────────┐
 │ Isolated component testing │
 └────────────────────────────────────┘
```

---

## Test Categories

### Unit Tests (`tests/unit/`)

**Purpose:** Fast, isolated tests of individual components

**Markers:** `@pytest.mark.unit`

**Coverage:**

- `test_utils.py` - TokenCounter, URL validation, formatting
- `test_config.py` - Configuration loading and validation
- `test_cache.py` - Cache CRUD operations, TTL, eviction
- `test_chunker.py` - Chunking strategies, overlap, metadata

**Characteristics:**

- No external dependencies (network, filesystem, APIs)
- Fast execution (< 100ms per test)
- High coverage target (>90%)
- Use mocks for external services

**Example:**

```python
@pytest.mark.unit
def test_token_counting():
 """Test token counting accuracy."""
 counter = TokenCounter()
 assert counter.count_tokens("Hello world") > 0
```

### Integration Tests (`tests/integration/`)

**Purpose:** Test interactions between multiple components

**Markers:** `@pytest.mark.integration`

**Coverage:**

- `test_pipeline.py` - Full pipeline integration
- Fetch → Extract → Chunk → Summarize flow
- Cache integration across modules
- Metrics collection

**Characteristics:**

- May use filesystem (temp directories)
- No network or API calls (use mocks)
- Medium execution time (< 1s per test)

### Security Tests (`tests/security/`)

**Purpose:** Test security vulnerabilities and mitigations

**Markers:** `@pytest.mark.security`

**Focus Areas (OWASP LLM Top 10):**

1. **LLM01: Prompt Injection**

- Direct instruction override detection
- Indirect injection via external content
- Role confusion attempts
- Data exfiltration patterns

2. **LLM05: Improper Output Handling**

- System prompt leakage prevention
- API key exposure prevention
- Output sanitization

3. **LLM10: Unbounded Consumption**

- Token limit enforcement
- Rate limiting
- Concurrent request limits

**Additional Security:**

- Input validation (URL, filename, path)
- XSS prevention (HTML sanitization)
- Path traversal prevention
- Cache security and isolation

**Files:**

- `test_prompt_injection.py` - Comprehensive prompt injection tests

**Example:**

```python
@pytest.mark.security
def test_prompt_injection_detection():
 """Test detection of prompt injection attempts."""
 malicious_content = "IGNORE ALL PREVIOUS INSTRUCTIONS"
 # Assert detection logic...
```

### Golden/Regression Tests (`tests/golden/`)

**Purpose:** Test against static HTML with expected results

**Markers:** `@pytest.mark.golden`

**Characteristics:**

- Uses predetermined HTML samples from `tests/fixtures/golden_data.py`
- Verifies extraction consistency
- Tests against known-good outputs
- Ensures no regression in extraction quality

**Golden HTML Samples:**

1. **Simple Article** - Basic blog post with code examples
2. **Technical Documentation** - API docs with JSON examples
3. **News Article** - Article with quotes and citations
4. **Blog Post** - Multiple links and sections

**Example:**

```python
@pytest.mark.golden
@pytest.mark.asyncio
async def test_simple_article_extraction():
 """Test extraction matches golden expectations."""
 extracted = await extractor.extract(SIMPLE_ARTICLE_HTML)
 
 # Verify expected keywords
 for keyword in EXPECTED["keywords"]:
 assert keyword in extracted.content
```

### Live Tests (`tests/live/`)

**Purpose:** Test against real URLs with static content

**Markers:** `@pytest.mark.live`, `@pytest.mark.requires_network`

**Golden URLs:**

1. **example.com** - IANA example domain
2. **Python PEP 8** - Style guide (static)
3. **IETF RFC** - HTTP/1.1 spec (text)
4. **W3C HTML5 Spec** - Historical snapshot

**Characteristics:**

- Requires internet connectivity
- May require API keys for summarization tests
- Slower execution (seconds per test)
- Used as acceptance tests

**Example:**

```python
@pytest.mark.live
@pytest.mark.requires_api
@pytest.mark.asyncio
async def test_summarize_golden_url():
 """Test full summarization pipeline."""
 summary = await pipeline.summarize_urls(["https://example.com"])
 assert len(summary) > 100
```

### Benchmark Tests (`tests/benchmarks/`)

**Purpose:** Measure and track performance

**Markers:** `@pytest.mark.benchmark`

**Metrics:**

- Token counting speed
- Chunking performance (hierarchical, semantic, fixed)
- Cache read/write speeds
- Extraction throughput
- Memory usage
- Scalability with increasing data size

**Example:**

```python
@pytest.mark.benchmark
def test_chunking_speed(benchmark):
 """Benchmark chunking performance."""
 result = benchmark(chunker.chunk_text, large_text)
 assert len(result) > 0
```

---

## Security Testing

### OWASP LLM Top 10 Coverage

Based on research from:

- https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- https://www.hackerone.com/blog/how-prompt-injection-vulnerability-led-data-exfiltration

#### LLM01:2025 Prompt Injection

**Vulnerability:** Malicious inputs alter LLM behavior

**Test Coverage:**

- Direct prompt injection (jailbreaking attempts)
- Indirect injection via external content
- Hidden instructions in HTML comments
- Unicode obfuscation
- Nested/encoded instructions
- Role confusion patterns

**Mitigation Tests:**

```python
def test_instruction_override_detection():
 """Test detection of instruction override attempts."""
 content = "IGNORE ALL PREVIOUS INSTRUCTIONS..."
 # Verify filtering or detection
```

**Prevention Strategies Tested:**

1. Input sanitization
2. System prompt protection
3. Output validation
4. Content filtering

#### LLM05: Improper Output Handling

**Vulnerability:** Sensitive data in outputs

**Test Coverage:**

- System prompt leakage prevention
- API key exposure prevention
- Internal path disclosure
- Conversation history leakage

**Example:**

```python
def test_no_api_key_in_output():
 """Ensure API keys never appear in output."""
 output = generate_summary(...)
 assert "sk-" not in output
 assert os.getenv("OPENAI_API_KEY") not in output
```

#### LLM10: Unbounded Consumption

**Vulnerability:** Resource exhaustion via API abuse

**Test Coverage:**

- Token limit enforcement
- Rate limiting
- Concurrent request limits
- Timeout enforcement
- Cache size limits

**Example:**

```python
def test_token_limit_enforced():
 """Verify max token limits prevent unbounded consumption."""
 assert config.summarizer.max_tokens > 0
 assert config.summarizer.max_tokens <= 10000
```

### Additional Security Tests

#### Input Validation

- URL scheme validation (http/https only)
- Path traversal prevention
- Filename sanitization
- Query length limits

#### XSS Prevention

- HTML script tag stripping
- Event handler removal
- Iframe filtering

#### Cache Security

- Cache key collision resistance
- Directory permission checks
- TTL enforcement

---

## Golden Tests

### Purpose

Golden tests provide deterministic validation against known-good data, ensuring:

1. Extraction consistency across versions
2. No regression in content quality
3. Proper handling of various HTML structures

### Test Data Location

All golden test data is in: `tests/fixtures/golden_data.py`

### Samples Included

1. **SIMPLE_ARTICLE_HTML**

- Content: Async/await tutorial
- Tests: Title extraction, keyword presence, code blocks, links

2. **TECHNICAL_DOC_HTML**

- Content: API documentation
- Tests: Endpoint extraction, JSON examples, structure preservation

3. **NEWS_ARTICLE_HTML**

- Content: Quantum computing breakthrough
- Tests: Quote preservation, metadata extraction, citations

4. **BLOG_POST_HTML**

- Content: Python best practices
- Tests: Multiple sections, link extraction

5. **PROMPT_INJECTION_SAMPLES**

- Content: Malicious injection attempts
- Tests: Detection and mitigation

### Expected Results

Each sample has associated expected results:

```python
SIMPLE_ARTICLE_EXPECTED = {
 "title": "Understanding Async/Await in Python",
 "content_keywords": ["async", "await", "asyncio"],
 "sections": ["Introduction", "Basic Concepts"],
 "code_blocks": 2,
 "min_content_length": 500,
}
```

### Running Golden Tests

```bash
# Run all golden tests
pytest -m golden -v

# Run specific golden test
pytest tests/golden/test_golden_extraction.py::test_simple_article_extraction -v
```

---

## Live Tests

### Purpose

Live tests validate the complete system against real-world URLs, ensuring:

1. Network fetching works correctly
2. Real content extraction succeeds
3. Full pipeline integration functions
4. Cache behavior is correct

### Golden URLs

Selected for:

- Static, unchanging content
- Public availability
- No authentication required
- Simple, predictable structure

| URL | Description | Tests |
|-----|-------------|-------|
| https://example.com | IANA example domain | Fetch, extract, summarize |
| https://peps.python.org/pep-0008/ | PEP 8 Style Guide | Content extraction, code examples |
| https://www.rfc-editor.org/rfc/rfc2616.txt | HTTP/1.1 RFC | Plain text handling |
| https://www.w3.org/TR/2011/WD-html5-20110405/ | W3C HTML5 Spec | Large document handling |

### Configuration

Live tests require:

```bash
# For summarization tests
export OPENAI_API_KEY="sk-..."

# Network access (no proxy configuration needed for these URLs)
```

### Skipping Live Tests

Tests automatically skip if:

- Network unavailable
- API key not set
- URL returns error

### Running Live Tests

```bash
# Run all live tests
pytest -m live -v

# Run without API-requiring tests
pytest -m "live and not requires_api" -v

# Run specific golden URL test
pytest tests/live/test_live_urls.py::test_fetch_golden_url -v
```

---

## Benchmarks

### Purpose

Track performance over time and identify bottlenecks.

### Metrics Tracked

1. **Token Counting**

- Speed for various text sizes
- Truncation performance

2. **Chunking**

- Hierarchical vs semantic vs fixed
- Scalability with document size

3. **Cache Operations**

- Read/write throughput
- Concurrent operation performance

4. **Memory Usage**

- Peak memory for large documents
- Cache memory overhead

5. **Concurrency**

- Parallel vs sequential speedup
- Async operation efficiency

### Running Benchmarks

```bash
# Run all benchmarks
pytest -m benchmark --benchmark-only -v

# Save benchmark results
pytest -m benchmark --benchmark-autosave

# Compare with previous run
pytest -m benchmark --benchmark-compare
```

### Performance Targets

| Operation | Target | Current |
|-----------|--------|---------|
| Token counting (1k tokens) | < 10ms | TBD |
| Chunking (10k tokens) | < 100ms | TBD |
| Cache read | < 5ms | TBD |
| Cache write | < 10ms | TBD |
| Extraction (10KB HTML) | < 50ms | TBD |

---

## Static Analysis

### Tools Used

1. **Ruff** - Fast Python linter

- Replaces flake8, isort, pyupgrade
- Configuration in `pyproject.toml`

2. **MyPy** - Static type checker

- Enforces type hints
- Configuration in `pyproject.toml`

3. **Bandit** - Security vulnerability scanner

- Checks for common security issues
- Configuration in `.bandit`

4. **Semgrep** - Pattern-based code scanner

- Custom rules for LLM security
- Configuration in `.semgrep.yml`

5. **Safety** - Dependency vulnerability scanner

- Checks for known CVEs in dependencies

### Custom Semgrep Rules

Located in `.semgrep.yml`:

1. **potential-prompt-injection-risk** - Direct LLM input
2. **llm-unvalidated-external-content** - Indirect injection
3. **hardcoded-api-key** - Credentials in code
4. **llm-no-token-limit** - Unbounded consumption
5. **dangerous-eval** - Code execution risks
6. **sql-injection-format-string** - SQL injection
7. **path-traversal-risk** - File access vulnerabilities
8. **dangerous-pickle** - Deserialization risks

### Running Analysis

```bash
# Run all static analysis
./scripts/run_analysis.sh

# Individual tools
ruff check src/ tests/
mypy src/
bandit -r src/ -c .bandit
semgrep --config=.semgrep.yml src/
safety check
```

---

## Running Tests

### Quick Start

```bash
# Install dependencies
pip install -e ".[dev]"
playwright install chromium

# Run unit and security tests (fast)
pytest -m "unit or security" -v

# Run all except live tests
pytest -m "not live" -v

# Run with coverage
pytest --cov=mcp_web --cov-report=html

# Run in parallel
pytest -n auto
```

### Using Test Scripts

```bash
# Run standard test suite
./scripts/run_tests.sh

# Run all tests including live
./scripts/run_tests.sh --all --live

# Run with benchmarks
./scripts/run_tests.sh --bench

# Run in parallel
./scripts/run_tests.sh --parallel

# Skip coverage
./scripts/run_tests.sh --no-coverage
```

### Test Markers

```bash
# Run by marker
pytest -m unit # Unit tests only
pytest -m security # Security tests only
pytest -m golden # Golden tests only
pytest -m live # Live tests only
pytest -m benchmark # Benchmarks only
pytest -m slow # Slow tests only

# Combine markers
pytest -m "unit or security" # Unit OR security
pytest -m "live and not requires_api" # Live without API
```

### Environment Variables

```bash
# Required for summarization tests
export OPENAI_API_KEY="sk-..."

# Optional configuration
export MCP_WEB_CACHE_DIR="/tmp/test-cache"
export MCP_WEB_SUMMARIZER_TEMPERATURE="0.0"
export MCP_WEB_METRICS_LOG_LEVEL="DEBUG"
```

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
 test:
 runs-on: ubuntu-latest
 steps:
 - uses: actions/checkout@v3
 
 - name: Set up Python
 uses: actions/setup-python@v4
 with:
 python-version: '3.10'
 
 - name: Install dependencies
 run: |
 pip install -e ".[dev]"
 playwright install chromium
 
 - name: Run linting
 run: ruff check src/ tests/
 
 - name: Run type checking
 run: mypy src/
 
 - name: Run security scan
 run: bandit -r src/ -c .bandit
 
 - name: Run unit tests
 run: pytest -m "unit or security or golden" --cov=mcp_web
 
 - name: Upload coverage
 uses: codecov/codecov-action@v3
```

### Pre-commit Hook

```bash
# .git/hooks/pre-commit
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Run fast tests
pytest -m "unit or security" -x

echo "All checks passed!"
```

---

## Best Practices

### Writing Tests

1. **Use descriptive names**: `test_extraction_handles_malformed_html`
2. **One assertion per test** (when possible)
3. **Use fixtures** for shared setup
4. **Add docstrings** explaining what's being tested
5. **Mark appropriately** with pytest markers
6. **Handle async properly** with `@pytest.mark.asyncio`

### Test Organization

```python
class TestFeatureName:
 """Test suite for specific feature."""
 
 @pytest.fixture
 def setup_data(self):
 """Fixture for test data."""
 return {"key": "value"}
 
 @pytest.mark.unit
 def test_happy_path(self, setup_data):
 """Test normal operation."""
 # Test code
 
 @pytest.mark.unit
 def test_error_handling(self):
 """Test error conditions."""
 with pytest.raises(ValueError):
 # Code that should raise
```

### Security Testing

1. **Test both detection and prevention**
2. **Include false positive checks** (benign content)
3. **Test edge cases** (Unicode, encoding, nested)
4. **Document vulnerability references** (CVE, OWASP)

### Performance Testing

1. **Set realistic performance targets**
2. **Track trends over time**
3. **Test with realistic data sizes**
4. **Measure memory in addition to time**

---

## Troubleshooting

### Common Issues

**Import errors:**

```bash
# Ensure package is installed in editable mode
pip install -e .
```

**Playwright errors:**

```bash
# Install browsers
playwright install chromium
```

**API key errors:**

```bash
# Set environment variable
export OPENAI_API_KEY="sk-..."
# Or use .env file (python-dotenv)
```

**Cache permission errors:**

```bash
# Clear cache
rm -rf ~/.cache/mcp-web

# Or use temp directory
export MCP_WEB_CACHE_DIR="/tmp/mcp-web-test"
```

---

## Resources

### References

- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Semgrep Rules](https://semgrep.dev/docs/)
- [Bandit Documentation](https://bandit.readthedocs.io/)

### Project Docs

- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [DECISIONS.md](DECISIONS.md) - Design decisions
- [API.md](API.md) - API reference
- [SECURITY.md](../SECURITY.md) - Security policy

---

**Last Updated:** 2025-10-15
**Version:** 0.2.0
**Status:** ✅ Comprehensive testing framework implemented
