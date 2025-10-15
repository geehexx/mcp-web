# Taskfile Guide

**Project:** mcp-web  
**Task Version:** 3.x

---

## What is Taskfile?

Taskfile is a task runner and build tool that replaces Make and bash scripts. It's:
- **Cross-platform:** Works on Linux, macOS, Windows
- **Simple:** YAML-based configuration
- **Fast:** Written in Go, minimal overhead
- **Powerful:** Variables, dependencies, parallel execution

### Installation

```bash
# macOS (Homebrew)
brew install go-task/tap/go-task

# Linux (snap)
snap install task --classic

# Or download binary
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin

# Verify
task --version
```

**Documentation:** https://taskfile.dev

---

## Quick Reference

### Essential Commands

```bash
# Show all available tasks
task --list
task -l

# Run default task (shows help)
task

# Run specific task
task test
task lint
task ci

# Run with different options
task test:unit
task test:coverage
task test:parallel
```

### Common Workflows

```bash
# Development setup
task dev:setup              # Complete setup

# Testing
task test                   # All tests except live
task test:fast              # Unit + security + golden
task test:coverage          # With coverage report
task test:parallel          # Parallel execution

# Code quality
task lint                   # All linting
task format                 # Auto-format code
task security               # Security scans

# Analysis
task analyze                # Complete static analysis
task ci                     # Simulate CI pipeline
```

---

## All Tasks by Category

### Installation

| Command | Description |
|---------|-------------|
| `task install` | Install package with dev dependencies |
| `task install:playwright` | Install Playwright browsers |
| `task install:pre-commit` | Install pre-commit hooks |
| `task dev:setup` | Complete development environment setup |

### Testing

| Command | Description |
|---------|-------------|
| `task test` | Run all tests (except live) |
| `task test:unit` | Unit tests only |
| `task test:security` | Security tests |
| `task test:golden` | Golden/regression tests |
| `task test:integration` | Integration tests |
| `task test:live` | Live tests (requires network + API) |
| `task test:bench` | Performance benchmarks |
| `task test:all` | All tests including live |
| `task test:fast` | Fast tests (unit + security + golden) |
| `task test:parallel` | Run tests in parallel |
| `task test:coverage` | With coverage report |
| `task test:coverage:min` | Enforce minimum coverage (90%) |
| `task test:watch` | Watch mode (requires pytest-watch) |

### Code Quality

| Command | Description |
|---------|-------------|
| `task lint` | Run all linting checks |
| `task lint:ruff` | Ruff linter |
| `task lint:format` | Check formatting |
| `task lint:mypy` | Type checking |
| `task format` | Auto-format code |

### Security

| Command | Description |
|---------|-------------|
| `task security` | All security checks |
| `task security:bandit` | Bandit security scanner |
| `task security:semgrep` | Semgrep pattern scanner |
| `task security:safety` | Dependency vulnerability check |

### Analysis

| Command | Description |
|---------|-------------|
| `task analyze` | Complete static analysis |
| `task analyze:complexity` | Code complexity analysis |
| `task analyze:maintainability` | Maintainability index |

### Local LLM

| Command | Description |
|---------|-------------|
| `task llm:ollama:start` | Start Ollama server |
| `task llm:ollama:pull` | Pull recommended models |
| `task llm:test:local` | Test with local LLM |

### Development

| Command | Description |
|---------|-------------|
| `task dev:clean` | Clean build artifacts |
| `task dev:clean:cache` | Clean application cache |
| `task shell` | Python shell with package imported |

### Pre-commit

| Command | Description |
|---------|-------------|
| `task pre-commit` | Run pre-commit checks |
| `task pre-commit:all` | Run on all files |

### CI/CD

| Command | Description |
|---------|-------------|
| `task ci` | Simulate full CI pipeline |
| `task ci:fast` | Fast CI check (no coverage) |

### Benchmarks

| Command | Description |
|---------|-------------|
| `task bench` | Run all benchmarks |
| `task bench:compare` | Compare with previous |
| `task bench:profile` | Profile with cProfile |

### Golden Tests

| Command | Description |
|---------|-------------|
| `task golden:verify` | Verify golden tests with details |
| `task golden:update` | Update expectations (use with caution!) |

### Dependencies

| Command | Description |
|---------|-------------|
| `task deps:update` | Update dependencies |
| `task deps:tree` | Show dependency tree |
| `task deps:outdated` | Check for outdated packages |

### Information

| Command | Description |
|---------|-------------|
| `task info` | Show project information |
| `task info:env` | Show environment configuration |

### Release

| Command | Description |
|---------|-------------|
| `task release:check` | Check if ready for release |
| `task release:build` | Build distribution packages |
| `task release:test-pypi` | Upload to TestPyPI |
| `task release:pypi` | Upload to PyPI |

---

## Detailed Examples

### Development Workflow

```bash
# 1. Initial setup
task dev:setup

# 2. Start development
task test:watch          # Terminal 1: Tests in watch mode
task llm:ollama:start    # Terminal 2: Local LLM (optional)

# 3. Before committing
task pre-commit          # Runs lint + fast tests

# 4. Pre-push
task ci                  # Full CI simulation
```

### Testing Workflow

```bash
# Quick iteration
task test:fast           # Unit + security + golden (< 10s)

# Before PR
task test:coverage       # All tests with coverage
task test:coverage:min   # Enforce 90% coverage

# Full validation
task test:all            # Including live tests
task analyze             # Static analysis
task security            # Security scans
```

### Local LLM Workflow

```bash
# 1. Setup Ollama
task llm:ollama:pull     # Pull recommended models

# 2. Start server
task llm:ollama:start    # In separate terminal

# 3. Test with local LLM
task llm:test:local      # Run golden tests

# 4. Check config
task info:env            # Verify provider settings
```

### CI/CD Workflow

```bash
# Fast check (< 30s)
task ci:fast

# Full check (< 2min)
task ci

# With live tests (requires API key)
export OPENAI_API_KEY="sk-..."
task test:all
```

---

## Configuration

### Environment Variables

Taskfile respects all `MCP_WEB_*` environment variables:

```bash
# Summarizer config
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.0

# Cache config
export MCP_WEB_CACHE_DIR=~/.cache/mcp-web
export MCP_WEB_CACHE_TTL=604800

# Run tests with config
task test:golden
```

### Parallel Execution

```bash
# Automatic parallel execution
task test:parallel

# Pytest-xdist controls (set NUM_WORKERS)
NUM_WORKERS=4 task test:parallel
```

### Coverage Threshold

The minimum coverage is set to 90% in the Taskfile:

```yaml
vars:
  COVERAGE_MIN: 90
```

Change if needed:

```bash
# Edit Taskfile.yml
vars:
  COVERAGE_MIN: 85
```

---

## Task Dependencies

Some tasks have dependencies that run automatically:

```bash
# This runs lint, then test:coverage:min, then security
task ci

# Equivalent to:
task lint
task test:coverage:min
task security
```

Dependency graph:
```
ci
├── lint
│   ├── lint:ruff
│   ├── lint:format
│   └── lint:mypy
├── test:coverage:min
└── security
    ├── security:bandit
    ├── security:semgrep
    └── security:safety
```

---

## Comparison: Taskfile vs Bash Scripts

### Old Approach (Bash)

```bash
./scripts/run_tests.sh --all --parallel
./scripts/run_analysis.sh
```

**Problems:**
- ❌ Not cross-platform (bash-specific)
- ❌ Manual dependency management
- ❌ No task discovery
- ❌ Limited error handling
- ❌ Hard to compose tasks

### New Approach (Taskfile)

```bash
task test:parallel
task analyze
```

**Benefits:**
- ✅ Cross-platform (Linux, macOS, Windows)
- ✅ Automatic dependency resolution
- ✅ Built-in task listing (`task -l`)
- ✅ Better error handling
- ✅ Easy task composition
- ✅ Variables and templating
- ✅ Parallel execution support

---

## Tips & Tricks

### Dry Run

```bash
# See what would be executed
task --dry test
```

### Verbose Output

```bash
# Show all commands
task --verbose test
task -v test
```

### List Tasks

```bash
# List all tasks
task --list
task -l

# List with descriptions
task --list-all
```

### Run Multiple Tasks

```bash
# Sequential
task lint format test

# The same as
task lint && task format && task test
```

### Task Aliases

Add to your `.bashrc` or `.zshrc`:

```bash
alias t='task'
alias tl='task --list'
alias tt='task test:fast'
alias tc='task test:coverage'
```

Then:
```bash
t test:fast   # Instead of task test:fast
tl            # Instead of task --list
```

---

## Advanced Usage

### Custom Variables

```bash
# Pass variables to tasks
COVERAGE_MIN=85 task test:coverage:min
```

### Watch Mode

```bash
# Requires pytest-watch
task test:watch

# Or manual
task test:fast --watch
```

### Profiling

```bash
# Profile test execution
task bench:profile

# View results
python -m pstats profile.stats
```

### Docker Integration

```bash
# Build and test in Docker
task docker:build
task docker:test
```

---

## Troubleshooting

### Task Not Found

```bash
# Error: task: Task "xyz" not found
# Solution: List available tasks
task --list
```

### Command Not Found

```bash
# Error: command not found: ruff
# Solution: Install dev dependencies
task install
```

### Permission Denied

```bash
# Error: permission denied
# Solution: Make sure Taskfile.yml is in current directory
pwd
ls Taskfile.yml
```

### Python Environment

```bash
# Task uses system Python by default
# To use virtual environment:
source venv/bin/activate  # Then run task
# Or
task --init  # Creates venv if needed (if configured)
```

---

## Integration with IDEs

### VS Code

Add to `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Test: Fast",
      "type": "shell",
      "command": "task test:fast",
      "group": "test"
    },
    {
      "label": "Test: All",
      "type": "shell",
      "command": "task test",
      "group": "test"
    },
    {
      "label": "Lint",
      "type": "shell",
      "command": "task lint",
      "group": "build"
    }
  ]
}
```

### JetBrains (PyCharm, IntelliJ)

1. Settings → Tools → External Tools
2. Add new tool:
   - Name: Task Test Fast
   - Program: task
   - Arguments: test:fast
   - Working directory: $ProjectFileDir$

---

## Migration from Bash Scripts

### Old → New Mapping

| Old Script | New Task | Notes |
|------------|----------|-------|
| `./scripts/run_tests.sh` | `task test` | More options available |
| `./scripts/run_tests.sh --all --live` | `task test:all` | Includes live tests |
| `./scripts/run_tests.sh --bench` | `task test:bench` | Benchmarks only |
| `./scripts/run_tests.sh --parallel` | `task test:parallel` | Parallel execution |
| `./scripts/run_analysis.sh` | `task analyze` | All static analysis |
| `ruff check src/ tests/` | `task lint:ruff` | Ruff linting |
| `mypy src/` | `task lint:mypy` | Type checking |
| `bandit -r src/` | `task security:bandit` | Security scan |

### Benefits of Migration

1. **Cross-platform:** Works on Windows natively
2. **Composable:** Easy to chain tasks
3. **Discoverable:** `task -l` shows all options
4. **Maintainable:** YAML is easier to maintain than bash
5. **Extensible:** Easy to add new tasks

---

## Resources

### Taskfile

- **Documentation:** https://taskfile.dev
- **GitHub:** https://github.com/go-task/task
- **Examples:** https://github.com/go-task/examples

### Project

- **Taskfile.yml:** `/Taskfile.yml` in project root
- **Testing Guide:** `docs/TESTING.md`
- **Local LLM Guide:** `docs/LOCAL_LLM_GUIDE.md`

---

## Getting Help

```bash
# Show task help
task --help

# Show specific task
task test --help

# List all tasks with descriptions
task --list-all

# Show Taskfile version
task --version
```

---

**Last Updated:** 2025-10-15  
**Taskfile Version:** 3.x  
**Status:** ✅ Complete migration from bash scripts
