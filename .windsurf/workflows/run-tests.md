---
description: Run comprehensive test suite with options
auto_execution_mode: 2
---

# Run Tests Workflow

Comprehensive testing workflow with various options for different scenarios.

## Quick Commands

```bash
# Fast tests (unit + security + golden) in parallel
task test:fast:parallel

# All tests except live (parallel)
task test:parallel

# With coverage (parallel)
task test:coverage:parallel

# Full CI simulation
task ci:parallel
```

## Detailed Process

1. **Choose test scope:**
   - **Fast iteration:** `task test:fast` - Unit, security, golden only
   - **Integration:** `task test:integration` - Multi-component tests
   - **Full suite:** `task test` - All except live tests
   - **Including live:** `task test:all` - Everything (needs API keys)

2. **Enable parallelization (recommended for IO-bound):**
   - Add `:parallel` suffix: `task test:fast:parallel`
   - Override workers: `PYTEST_XDIST_AUTO_NUM_WORKERS=16 task test:parallel`
   - Distribution strategy: `pytest -n auto --dist worksteal tests/`

3. **Run with coverage:**
   - **Standard:** `task test:coverage`
   - **Parallel:** `task test:coverage:parallel`
   - **Enforced minimum:** `task test:coverage:min` (90% required)

4. **Specific test types:**
   - **Unit:** `task test:unit` or `task test:unit:parallel`
   - **Security:** `task test:security`
   - **Golden:** `task test:golden`
   - **Benchmarks:** `task test:bench`

5. **Manual testing:**
   - **URL summarization:** `task test:manual URL=https://example.com QUERY="topic"`
   - **robots.txt:** `task test:robots URL=https://example.com`

## Parallelization Best Practices

**Reference:** [pytest-xdist](https://pytest-xdist.readthedocs.io/) (October 2025)

### CPU-bound tests (pure Python logic)

```bash
# Use auto (number of CPU cores)
pytest -n auto tests/unit/
```

### IO-bound tests (external APIs, network)

```bash
# Use more workers than CPU cores
PYTEST_XDIST_AUTO_NUM_WORKERS=16 pytest -n auto tests/integration/
```

### Distribution strategies

- `--dist load` (default): Any available worker
- `--dist loadscope`: Group by module/class (better fixture reuse)
- `--dist worksteal`: Reassign from slow to fast workers

## Coverage Analysis

```bash
# Generate HTML report
task test:coverage

# Open report
open htmlcov/index.html

# Check specific module
pytest --cov=src/mcp_web/fetcher tests/unit/test_fetcher.py
```

## Debugging Failed Tests

```bash
# Run with detailed output
pytest -vv --tb=long tests/path/to/test_file.py::test_function

# Run single test
pytest tests/path/to/test_file.py::TestClass::test_method

# Show print statements
pytest -s tests/path/to/test_file.py

# Drop into debugger on failure
pytest --pdb tests/path/to/test_file.py
```

## CI Simulation

```bash
# Full CI pipeline locally
task ci

# Fast CI (parallel, no coverage)
task ci:fast

# Parallel CI with coverage
task ci:parallel
```

## Test Markers

Filter tests by marker:

```bash
# Only unit tests
pytest -m unit

# Only security tests
pytest -m security

# Exclude live tests (default)
pytest -m "not live"

# Multiple markers
pytest -m "unit or integration"
```

## Performance Tips

1. **Use parallelization for IO-bound tests** (external APIs)
2. **Mock external dependencies** in unit tests
3. **Use fixtures efficiently** (scope to session/module where possible)
4. **Run fast tests during development** (`task test:fast:parallel`)
5. **Run full suite before commit** (`task ci`)

## Environment Variables

```bash
# Increase parallel workers for IO-bound
export PYTEST_XDIST_AUTO_NUM_WORKERS=16

# Configure LLM provider for tests
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b

# Skip slow tests
pytest -m "not slow"
```
