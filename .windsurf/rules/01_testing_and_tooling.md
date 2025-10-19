---
created: "2025-10-15"
updated: "2025-10-18"
trigger: glob
description: Enforces testing standards, tool usage, and development environment practices.
globs:
  - tests/**/*.py
  - src/**/*.py
  - "*.toml"
  - "*.ini"
  - Taskfile.yml
category: testing
tokens: 989
applyTo:
  - testing
  - implementation
priority: high
status: active
---

# Rule: Testing, Tooling, and Development Environment

## 1.1 Development Environment

- **Standardization:** All development uses `uv` as the package manager (October 2025 best practice)
- **Installation:** `uv sync --all-extras` installs all dependencies
- **Virtual environments:** `uv` manages `.venv` automatically
- **Lock file:** `uv.lock` is the source of truth for reproducible builds

## 1.2 Test-Driven Development (TDD)

- **Write tests first:** For new features, write tests before implementation
- **Test pyramid:** More unit tests than integration tests, more integration tests than live tests
- **Coverage requirement:** Maintain ≥90% code coverage (enforced by CI)
- **Test organization:**

  ```text
  tests/
  ├── unit/              # Fast, isolated unit tests
  ├── integration/       # Multi-component tests
  ├── security/          # OWASP LLM Top 10 compliance tests
  ├── golden/            # Regression tests with static data
  ├── live/              # Tests requiring network/API (marked, excluded by default)
  └── benchmarks/        # Performance benchmarks
  ```

## 1.3 Parallel Testing (pytest-xdist)

**Reference:** [pytest-xdist documentation](https://pytest-xdist.readthedocs.io/) (October 2025)

- **Default parallelization:** Use `-n auto` for CPU-bound tests
- **IO-bound optimization:** For external API calls (LLM, web fetching), use `-n 16` or higher
  - Set via: `PYTEST_XDIST_AUTO_NUM_WORKERS=16 task test:parallel`
- **Distribution strategies:**
  - `--dist load` (default): Distribute to any worker
  - `--dist loadscope`: Group by module/class for fixture reuse
  - `--dist worksteal`: Reassign from slow to fast workers
- **Task commands:**
  - `task test:parallel` - Run tests in parallel (auto workers)
  - `task test:unit:parallel` - Parallel unit tests
  - `task test:integration:parallel` - Parallel integration tests
  - `task test:coverage:parallel` - Parallel with coverage

## 1.4 Test Markers

Use pytest markers to categorize and select tests:

```python
@pytest.mark.unit  # Fast, isolated
@pytest.mark.integration  # Multi-component
@pytest.mark.security  # OWASP compliance
@pytest.mark.golden  # Regression with static data
@pytest.mark.live  # Requires network (excluded by default)
@pytest.mark.requires_api  # Needs API key
@pytest.mark.slow  # Takes > 1 second
@pytest.mark.benchmark  # Performance measurement
```

**Running specific markers:**

```bash
task test:unit           # Only unit tests
task test:security       # Only security tests
task test:fast           # unit + security + golden
pytest -m "not live"     # Exclude live tests (default)
```

## 1.5 Code Quality & Automation

- **All tasks via Taskfile:** Use `task <command>` for consistency
- **Linting:**
  - `task lint` - Run all linters (ruff, mypy, docs)
  - `task lint:ruff` - Check Python code style
  - `task lint:mypy` - Type checking
  - `task format` - Auto-format code
- **Security:**
  - `task security` - Run all security checks
  - `task security:bandit` - Scan for vulnerabilities
  - `task security:semgrep` - Pattern-based scanning
- **CI simulation:**
  - `task ci` - Full CI pipeline locally
  - `task ci:fast` - Quick check (parallel tests)
  - `task ci:parallel` - Full CI with parallelization

## 1.6 Coverage Requirements

- **Minimum:** 90% code coverage (enforced)
- **Command:** `task test:coverage:min`
- **Report:** HTML report in `htmlcov/index.html`
- **Parallel coverage:** `task test:coverage:parallel` (faster for IO-bound)

## 1.7 Pre-commit Hooks

- **Installation:** `task install:pre-commit`
- **Hooks include:**
  - ruff formatting and linting
  - mypy type checking
  - trailing whitespace removal
  - YAML/JSON validation
- **Manual run:** `task pre-commit:all`

## 1.8 Editing Workflow

- **Preflight checks:** Verify file/directory exists before editing
- **Create when missing:** Use `mcp1_create_directory` and `mcp1_write_file` for new paths
- **Tool selection:** Follow `docs/tooling/editing-tools.md` when choosing between Windsurf and MCP tools
- **Post-edit validation:** Immediately run relevant tests/linters after modifications
- **Read responses:** Always check tool responses to confirm success

## 1.9 Benchmarking

- **Performance tests:** Use `@pytest.mark.benchmark` for performance-critical code
- **Commands:**
  - `task test:bench` - Run benchmarks
  - `task bench` - Full benchmark suite with autosave
  - `task bench:compare` - Compare with previous run
  - `task bench:profile` - Profile with cProfile

## 1.10 Golden Tests

- **Purpose:** Regression testing with static data (no API calls needed)
- **Data:** Static HTML samples in `tests/fixtures/golden_data.py`
- **Determinism:** Use `temperature=0` for LLM calls
- **Commands:**
  - `task test:golden` - Run golden tests
  - `task golden:verify` - Detailed verification
  - `task golden:update` - Update expectations (use with caution)

## 1.11 Self-Validation

Before delivering checkpoints:

1. Run `task lint` - All linters pass
2. Run `task test:fast:parallel` - Fast tests pass
3. Run `task security` - Security checks pass
4. Review `git diff` output - All changes intentional
5. Verify documentation updated

## 1.12 Network Intelligence

- **Authoritative sources:** Use @web search when official documentation needed
- **Validation:** Cross-reference non-authoritative sources
- **Traceability:** Document fetch rationale in checkpoints
- **Current date awareness:** October 15, 2025 - ensure references are current
