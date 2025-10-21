---
trigger: glob
description: Configuration file best practices TOML YAML Taskfile
globs: "pyproject.toml, *.ini, Taskfile.yml, .pre-commit-config.yaml"
---

# Configuration File Standards

## TOML Files (pyproject.toml)

**Best practices:**
- Use tables for organization
- Keep dependencies alphabetized
- Version constraints: Use `>=` for lower bound, `<` for upper
- Document non-obvious choices with inline comments

```toml
[project]
name = "mcp-web"
version = "0.1.0"
requires-python = ">=3.10"

[tool.ruff]
line-length = 100
target-version = "py310"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
```

## YAML Files

**Common pitfalls:**
- Avoid quotes unless necessary (YAML auto-detects types)
- Use consistent indentation (2 spaces)
- Lists: Use `-` with space
- Multiline strings: Use `|` for preserving newlines

```yaml
# Good
key: value
list:
  - item1
  - item2

# Bad
key: "value"  # Unnecessary quotes
list:
- item1     # Inconsistent spacing
```

## Taskfile.yml

**Organization:**
- Group related tasks
- Use `desc:` for user-facing tasks
- Internal tasks: Prefix with `internal:`
- Dependencies: Use `deps:` array

```yaml
tasks:
  test:fast:
    desc: "Run fast unit tests"
    cmd: pytest -xvs tests/unit --maxfail=1
  
  internal:setup:
    cmd: uv sync
```

## Pre-commit Config

**Structure:**
- Order hooks by execution speed (fast → slow)
- Use `args:` for configuration
- Set `pass_filenames: false` for hooks that need it

```yaml
repos:
  - repo: local
    hooks:
      - id: validate-rules
        name: Validate rules
        entry: python scripts/validate_rules.py
        language: system
        files: \.windsurf/rules/.*\.md$
```



---

## Rule Metadata

**File:** `04_config_files.md`  
**Trigger:** glob  
**Estimated Tokens:** ~1,500  
**Last Updated:** 2025-10-21  
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)


**Topics Covered:**
- TOML best practices
- YAML pitfalls
- Taskfile organization
- Pre-commit configuration

**Workflow References:**
- /implement - When editing config files

**Dependencies:**
- Consolidated from project experience

**Changelog:**
- 2025-10-21: Created (new consolidated rule)