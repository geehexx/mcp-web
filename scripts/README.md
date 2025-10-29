# Scripts

Automation and utility scripts for the mcp-web project. All scripts are organized by purpose and use common libraries for consistency.

## Directory Structure

```text
scripts/
├── lib/                      # Common libraries (frontmatter, validation, CLI)
├── validation/              # Validation scripts for docs, code, and configs
├── automation/              # Automation scripts (scaffolding, file operations)
├── analysis/                # Analysis and reporting scripts
├── hooks/                   # Git pre-commit hooks
├── templates/               # Templates for scaffolding
├── manage_optimization_cache.py    # Cache management for workflow optimization
└── test_optimization_idempotency.py # Test workflow optimization stability
```

---

## Common Libraries (`scripts/lib/`)

Shared utilities used across multiple scripts. See individual module docstrings for details.

### `frontmatter.py`

Unified YAML frontmatter parsing for markdown files.

- `extract_frontmatter()` - Standard YAML parsing (strict mode)
- `extract_frontmatter_lenient()` - Windsurf-compatible (handles unquoted globs)
- `validate_frontmatter()` - Field validation
- `has_frontmatter()` - Quick check for frontmatter presence

**Usage:**

```python
from scripts.lib.frontmatter import extract_frontmatter

data = extract_frontmatter(Path("workflow.md"))
```

### `validation.py`

Base classes and utilities for validation scripts.

- `ValidationResult` - Result aggregation with reporting
- `BaseValidator` - Base class for validation scripts
- `walk_files()` - Directory traversal with exclusions
- `collect_errors()` - Error collection helper

**Usage:**

```python
from scripts.lib.validation import BaseValidator

class MyValidator(BaseValidator):
    def validate_file(self, file_path: Path) -> list[str]:
        # validation logic
        return errors
```

### `cli.py`

Common CLI patterns for consistent script interfaces.

- `create_parser()` - Consistent ArgumentParser creation
- `add_common_args()` - Standard --verbose, --dry-run flags
- `handle_exit()` - Exit code handling
- `confirm_action()` - Y/N prompts

---

## Validation Scripts (`scripts/validation/`)

Scripts for validating documentation, code, and configuration files.

### Core Validators

- **`validate_initiatives.py`** - Validate initiative files (frontmatter, status, dependencies)
- **`validate_workflows.py`** - Validate .windsurf/ workflows and rules
- **`validate_references.py`** - Validate internal markdown links
- **`validate_documentation.py`** - Validate documentation structure and consistency
- **`validate_frontmatter.py`** - Validate YAML frontmatter in markdown files
- **`validate_rules_frontmatter.py`** - Validate Windsurf rule frontmatter
- **`validate_generated_sync.py`** - Ensure generated IDE artefacts remain in sync with unified sources
- **`validate_task_format.py`** - Validate task format in documentation
- **`validate_archival.py`** - Validate archival process compliance

**Run via Taskfile:**

```bash
task validate:initiatives
task docs:validate:links
task docs:validate:consistency
```

---

## Automation Scripts (`scripts/automation/`)

Scripts for scaffolding and file operations.

### `scaffold.py`

Create new documents from templates (initiatives, ADRs, summaries).

**Interactive mode (humans):**

```bash
task scaffold:initiative
task scaffold:adr
task scaffold:summary
```

**Config mode (AI agents):**

```bash
task scaffold:initiative:config CONFIG=/path/to/config.yaml
task scaffold:adr:config CONFIG=/path/to/config.yaml
```

**Templates:** `scripts/templates/` (initiative, ADR, summary)

### `file_ops.py`

File operations with automatic reference updating.

**Commands:**

```bash
# Archive initiative
task archive:initiative NAME=my-initiative

# Move file + update refs
task move:file SRC=old.md DST=new.md

# Update documentation index
task update:index DIR=docs/initiatives
```

### `dependency_registry.py`

Initiative dependency management and analysis.

**Commands:**

```bash
# Validate dependencies
task validate:dependencies

# Generate dependency graph (DOT)
task deps:graph

# Show blocker propagation
task deps:blockers

# Export to JSON
task deps:export FILE=deps.json
```

### `extract_action_items.py`

Extract action items from documents (used by summarization workflows).

### `update_ide_goldens.py`

Rebuilds IDE configurations and syncs `.cursor/` and `.windsurf/` outputs into
`tests/golden/ide/` snapshots. Use when unified rules/commands change to refresh
the regression baselines.

---

## Analysis Scripts (`scripts/analysis/`)

Scripts for analyzing code, docs, and performance.

### Performance & Benchmarking

- **`benchmark_pipeline.py`** - Pipeline performance benchmarking
- **`check_performance_regression.py`** - Detect performance regressions
- **`check_workflow_tokens.py`** - Monitor workflow token counts

**Run via Taskfile:**

```bash
task test:bench
task test:bench:regression
```

### Documentation Analysis

- **`doc_coverage.py`** - Analyze documentation coverage
- **`analyze_workflow_improvements.py`** - Analyze workflow optimization results
- **`generate_indexes.py`** - Generate documentation indexes
- **`update_machine_readable_docs.py`** - Update machine-readable documentation

---

## Utility Scripts

### `manage_optimization_cache.py`

Manage workflow optimization cache.

**Usage:**

```bash
# View cache stats
python scripts/manage_optimization_cache.py --stats

# Clear entire cache (when optimization prompt changes)
python scripts/manage_optimization_cache.py --clear

# Invalidate specific workflow
python scripts/manage_optimization_cache.py --invalidate implement.md

# List cached workflows
python scripts/manage_optimization_cache.py --list

# Export cache for inspection
python scripts/manage_optimization_cache.py --export cache-backup.json
```

**When to use:**

- After changing workflow optimization prompts
- Before running workflow optimization to clear stale cache
- When debugging optimization issues

### `test_optimization_idempotency.py`

Test workflow optimization idempotency (ensures re-optimization produces no changes).

**Usage:**

```bash
# Test specific workflows
python scripts/test_optimization_idempotency.py --workflows implement.md detect-context.md

# Test all golden workflows
python scripts/test_optimization_idempotency.py --test-golden

# Enable caching (faster, but may hide issues)
python scripts/test_optimization_idempotency.py --test-golden --cache

# Show full diff for non-idempotent workflows
python scripts/test_optimization_idempotency.py --test-golden --show-diff
```

**When to use:**

- Before Phase 2 optimizations (validate Phase 1 stability)
- After optimization prompt changes (validate all workflows)
- When debugging workflow optimization issues

---

## Git Hooks (`scripts/hooks/`)

Pre-commit hooks for automated validation.

- **`validate_task_format_hook.py`** - Validate task format in documentation

**Configuration:** `.pre-commit-config.yaml`

---

## Development Guidelines

### Creating New Scripts

1. **Choose appropriate directory:**
   - `validation/` - Validates existing content
   - `automation/` - Creates or modifies content
   - `analysis/` - Analyzes and reports on content

2. **Use common libraries:**

   ```python
   from scripts.lib.frontmatter import extract_frontmatter
   from scripts.lib.validation import BaseValidator
   from scripts.lib.cli import create_parser, add_common_args
   ```

3. **Follow standards:**
   - Type hints on all functions
   - Google-style docstrings
   - Add to Taskfile.yml if user-facing
   - Add to .pre-commit-config.yaml if validator

### Testing Scripts

```bash
# Run all tests
task test:all

# Run script-specific tests
uv run pytest tests/scripts/ -v

# Test with coverage
uv run pytest tests/scripts/ --cov=scripts.lib --cov-report=term-missing
```

### Adding to Taskfile

```yaml
my:task:
  desc: Description for users
  cmds:
    - "{{.UV}} run python scripts/category/my_script.py"
```

---

## Maintenance

### Code Quality

All scripts pass:

- `task lint` (ruff + mypy)
- `task test:scripts` (if applicable)
- Pre-commit hooks

### Dependencies

Scripts use:

- **uv** for package management
- **Python 3.10+** minimum
- Dependencies in `pyproject.toml`

### Documentation

Update this README when:

- Adding new scripts
- Changing script organization
- Adding new common libraries
- Modifying script interfaces

---

**Last Updated:** 2025-10-22 (Phase 0: Scripts Audit & Refactoring)
