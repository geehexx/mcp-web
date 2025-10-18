---
description: Run comprehensive test suite with options
auto_execution_mode: 2
---

# Run Tests Workflow

**Purpose:** Quick reference for test execution commands and options.

**Note:** For pre-commit validation (linting + tests + security), use `/validate` instead.

---

## Quick Commands

**Most Common:**

```bash
# Fast iteration (unit + security + golden, parallel)
task test:fast

# All tests with coverage
task test:coverage

# Full CI simulation
task ci
```

**Always run pytest through uv:** `uv run pytest [options]`

---

## Test Scopes

| Command | What It Runs | Use When |
|---------|--------------|----------|
| `task test:fast` | Unit + security + golden | Fast iteration during development |
| `task test:integration` | Integration tests only | Testing multi-component interactions |
| `task test` | All except live tests | Pre-commit validation |
| `task test:all` | Everything including live | Full validation (needs API keys) |
| `task test:unit` | Unit tests only | Isolated component testing |
| `task test:security` | Security tests only | Validating security patterns |
| `task test:golden` | Golden file tests only | Output regression testing |

---

## Parallelization

**Enable with `:parallel` suffix:**

```bash
task test:fast:parallel        # Fast tests in parallel
task test:parallel             # All tests in parallel
task test:coverage:parallel    # Coverage with parallelization
```

**Override worker count:**

```bash
# Default: auto (uses CPU cores)
task test:fast

# Custom worker count (good for IO-bound tests)
PYTEST_XDIST_AUTO_NUM_WORKERS=16 task test:integration
```

**Reference:** [pytest-xdist docs](https://pytest-xdist.readthedocs.io/)

---

## Coverage

```bash
# Generate coverage report
task test:coverage

# Enforce minimum (90% required)
task test:coverage:min

# Open HTML report
open htmlcov/index.html

# Coverage for specific module
uv run pytest --cov=src/mcp_web/fetcher tests/unit/test_fetcher.py
```

---

## Debugging

```bash
# Verbose output
uv run pytest -vv --tb=long tests/path/to/test_file.py::test_function

# Single test
uv run pytest tests/path/to/test_file.py::TestClass::test_method

# Show print statements
uv run pytest -s tests/path/to/test_file.py

# Drop into debugger on failure
uv run pytest --pdb tests/path/to/test_file.py
```

---

## Test Markers

**Filter by marker:**

```bash
# Only unit tests
uv run pytest -m unit

# Only security tests
uv run pytest -m security

# Exclude live tests (default)
uv run pytest -m "not live"

# Multiple markers
uv run pytest -m "unit or integration"
```

---

## Manual Testing

```bash
# Test URL summarization
task test:manual URL=https://example.com QUERY="topic"

# Test robots.txt handling
task test:robots URL=https://example.com
```

---

## Environment Variables

```bash
# Parallel worker count
export PYTEST_XDIST_AUTO_NUM_WORKERS=16

# LLM provider for tests
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b
```

---

## Performance Tips

1. **Use `:parallel` for IO-bound tests** (network, external APIs)
2. **Mock external dependencies** in unit tests for speed
3. **Run `task test:fast` during development** (quick feedback)
4. **Run `task ci` before committing** (full validation)

---

## Integration

### Called By

- `/implement` - After implementation phase
- User - Direct invocation for testing

### Related Workflows

- `/validate` - Full quality gate (linting + tests + security)
- `/implement` - Implementation workflow (includes testing)

---

## References

- [pytest documentation](https://docs.pytest.org/)
- [pytest-xdist documentation](https://pytest-xdist.readthedocs.io/)
- Project: `Taskfile.yml` - Task definitions
- Project: `pyproject.toml` - pytest configuration
- `.windsurf/workflows/validate.md` - Pre-commit validation workflow
