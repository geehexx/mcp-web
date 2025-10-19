# Automation Scripts

This directory contains automation scripts for the mcp-web project to reduce token expenditure on mechanical workflow tasks.

## Overview

**Completed Automation:**

- **Phase 1:** Template scaffolding (initiative, ADR, session summary)
- **Phase 2:** File operations (archive, move, index)
- **Phase 3:** Frontmatter validation (superseded - delivered via Initiative System)
- **Phase 4:** Session summary automation (superseded - delivered via Consolidation Workflow)

**Token Savings:** 94-97% reduction in mechanical task overhead

---

## Phase 1: Template Scaffolding (Complete)

### Quick Start

```bash
# Create a new initiative
task scaffold:initiative

# Create a new ADR
task scaffold:adr

# Create a new session summary
task scaffold:summary
```

### scaffold.py - Template Generation Tool

**Purpose:** Generate standardized documents from Jinja2 templates with interactive prompts and validation.

**Usage:**

```bash
# Interactive mode (recommended)
task scaffold:initiative
task scaffold:adr
task scaffold:summary

# With config file
python scripts/scaffold.py --type initiative --config config.yaml

# Dry-run (preview without writing)
python scripts/scaffold.py --type adr --dry-run

# Validate template only
python scripts/scaffold.py --type initiative --validate-only
```

**Templates Available:**

- `initiative-flat.md.j2` - Flat file initiative (ADR-0013 format)
- `adr.md.j2` - Architecture Decision Record
- `session-summary.md.j2` - Session summary with metrics

**Features:**

- ✅ Interactive prompts for all fields
- ✅ Config file support (YAML/JSON)
- ✅ Auto-numbering (ADRs)
- ✅ Auto-dating (all templates)
- ✅ Markdown linting validation
- ✅ Frontmatter generation
- ✅ Dry-run mode

**Token Savings:**

- Initiative creation: 1500 tokens → 50 tokens (97% reduction)
- ADR creation: 1200 tokens → 50 tokens (96% reduction)
- Session summary: 2500 tokens → 100 tokens (96% reduction)

### Template Structure

```text
scripts/templates/
├── initiative-flat.md.j2    # Initiative template
├── adr.md.j2                 # ADR template
├── session-summary.md.j2     # Session summary template
└── schemas/                  # Future: validation schemas
```

### Testing

```bash
# Run scaffold tests
uv run python -m pytest tests/test_scaffold.py -c /dev/null

# All 26 tests pass
```

### Dependencies

- `jinja2>=3.1.0` - Template rendering
- `python-frontmatter>=1.0.0` - Markdown frontmatter
- `pyyaml>=6.0.0` - YAML parsing
- `click>=8.1.0` - CLI framework

## Phase 2: File Operations (Complete)

### file_ops.py - File Operation Helpers

**Purpose:** Automate file moves, archival, and reference updates to reduce manual overhead and prevent broken links.

**Usage:**

```bash
# Archive initiative (move to completed/, update references)
task archive:initiative NAME=2025-10-18-my-initiative

# Move file with automatic reference updates
task move:file SRC=docs/old.md DST=docs/new.md

# Update initiative index
task update:index DIR=docs/initiatives

# Dry-run mode (all commands)
task archive:initiative NAME=my-initiative DRY_RUN=true
```

**Functions:**

- `archive_initiative()` - Move initiative to completed/, add archive banner, update cross-references
- `move_file_with_refs()` - Move file and update all repository references automatically
- `update_index()` - Regenerate initiative directory index in README.md

**Features:**

- ✅ Automatic cross-reference updates (repo-wide search and replace)
- ✅ Archive banner insertion (with completion date)
- ✅ Index regeneration (Active/Completed sections)
- ✅ Path safety validation (prevent directory traversal)
- ✅ Dry-run mode for all operations
- ✅ CLI and programmatic access

**Token Savings:**

- Archive operations: Manual (15 min) → Automated (10 sec) - 90x faster
- Reference updates: Error-prone manual → Automatic repo-wide
- Used by `/archive-initiative` workflow

**Testing:**

```bash
# Run file_ops tests
task test:unit FILTER=test_file_ops

# All 4 tests pass (archive file, archive folder, move with refs, index validation)
```

## Phase 3: Frontmatter Management (Superseded)

**Status:** Completed via [Initiative System Lifecycle Improvements](../docs/initiatives/completed/2025-10-19-initiative-system-lifecycle-improvements/initiative.md)

**What Was Delivered:**

- `scripts/validate_initiatives.py` - Comprehensive frontmatter validator (350+ lines)
- Pre-commit hook integration (`.pre-commit-config.yaml`)
- Required field validation (Status, Created, Owner, Priority)
- Date format validation (YYYY-MM-DD)
- Status consistency checks (Active vs location)
- Taskfile commands: `task validate:initiatives`, `task validate:initiatives:ci`
- 12 unit tests (100% passing)

**Usage:**

```bash
# Validate all initiatives
task validate:initiatives

# CI mode (exits with error on failure)
task validate:initiatives:ci
```

## Phase 4: Session Summary Automation (Superseded)

**Status:** Superseded by [Session Summary Consolidation Workflow](../docs/initiatives/completed/2025-10-19-session-summary-consolidation-workflow/initiative.md)

**What Was Delivered:**

- Enhanced `/consolidate-summaries` workflow v2.3.0 with action item extraction
- Manual 5-step extraction process (good-enough for current needs)
- Advanced LLM automation deferred to [Session Summary Mining Advanced](../docs/initiatives/active/2025-10-19-session-summary-mining-advanced/initiative.md) (blocked on MCP file system support)

## Development

### Adding New Templates

**Steps:**

1. Create template file in `scripts/templates/`

   ```jinja2
   # my-template.md.j2
   # {{ title }}

   **Created:** {{ date }}

   {{ content }}
   ```

2. Add to `TemplateType` enum in `scaffold.py`
3. Add schema in `Scaffolder.get_schema()`
4. Add to template_files mapping in `render()` and `validate_template()`
5. Add Taskfile command
6. Write tests

### Template Guidelines

- Use Jinja2 syntax
- Support optional fields with `{% if %}` blocks
- Use `{%- -%}` to control whitespace
- Validate all generated files with markdownlint

## References

- Initiative: [2025-10-18-workflow-automation-enhancement.md](../docs/initiatives/active/2025-10-18-workflow-automation-enhancement.md)
- Technical Design: [technical-design.md](../docs/initiatives/active/2025-10-18-workflow-automation-enhancement/technical-design.md)
- ADR-0013: [Initiative Documentation Standards](../docs/adr/0013-initiative-documentation-standards.md)
