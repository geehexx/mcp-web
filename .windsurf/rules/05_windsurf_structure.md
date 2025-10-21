---
trigger: glob
description: Windsurf directory structure enforcement frontmatter format
globs: ".windsurf/**/*.md, .windsurf/**/*.json"
---

# .windsurf Directory Structure

**Purpose:** Define the canonical directory structure for Windsurf AI agent configuration.

---

## Directory Rules

### Approved Directories

Only the following directories are allowed in `.windsurf/`:

1. **`workflows/`** - Executable workflows only (`.md` files)
2. **`rules/`** - Agent rules only (`.md` files with `XX_name.md` format)
3. **`docs/`** - Supporting documentation and generated indexes
4. **`schemas/`** - JSON schemas for validation

### Directory Purposes

#### `workflows/` - Executable Workflows

**Purpose:** Contains workflow definitions that can be invoked by the agent.

**Rules:**

- **ONLY** executable workflow `.md` files
- Must follow kebab-case naming: `workflow-name.md`
- Must have YAML frontmatter with workflow metadata
- No supporting documentation, templates, or generated files

**Examples:**

- ✅ `work.md` - Work orchestration workflow
- ✅ `detect-context.md` - Context detection workflow
- ✅ `implement.md` - Implementation workflow
- ❌ `INDEX.md` - Generated index (belongs in `docs/`)
- ❌ `DEPENDENCIES.md` - Generated graph (belongs in `docs/`)
- ❌ `common-patterns.md` - Template library (belongs in `docs/`)

#### `rules/` - Agent Rules

**Purpose:** Contains rule definitions that guide agent behavior.

**Rules:**

- **ONLY** rule `.md` files
- Must follow `XX_name.md` format (two-digit prefix + snake_case)
- Must have YAML frontmatter with rule metadata
- No supporting documentation or generated files

**Examples:**

- ✅ `00_agent_directives.md` - Core agent rules
- ✅ `01_testing_and_tooling.md` - Testing standards
- ✅ `02_python_standards.md` - Python coding standards
- ❌ `INDEX.md` - Generated index (belongs in `docs/`)
- ❌ `cheatsheet.md` - Reference doc (belongs in `docs/`)

#### `docs/` - Supporting Documentation

**Purpose:** Contains documentation, templates, and generated indexes that support workflows and rules.

**Rules:**

- Supporting documentation for workflows/rules
- Template libraries (e.g., `common-patterns.md`)
- Generated indexes and graphs
- Must follow kebab-case naming: `document-name.md`

**Examples:**

- ✅ `workflow-index.md` - Generated workflow index
- ✅ `rules-index.md` - Generated rule index
- ✅ `workflow-dependencies.md` - Generated dependency graph
- ✅ `common-patterns.md` - Reusable pattern templates
- ✅ `context-loading-patterns.md` - Context loading strategies
- ✅ `batch-operations.md` - Batch operation patterns
- ✅ `DIRECTORY_STRUCTURE.md` - This file

#### `schemas/` - JSON Schemas

**Purpose:** Contains JSON schemas for validation.

**Rules:**

- **ONLY** `.json` schema files
- Must follow kebab-case naming: `schema-name.json`
- Used for validating frontmatter and other structured data

**Examples:**

- ✅ `frontmatter-schema.json` - Frontmatter validation schema
- ❌ `config.yaml` - Config file (doesn't belong here)

---

## File Naming Conventions

| Directory | Naming Convention | Example |
|-----------|-------------------|---------|
| `workflows/` | kebab-case | `work.md`, `detect-context.md` |
| `rules/` | `XX_snake_case` | `00_agent_directives.md`, `01_testing_and_tooling.md` |
| `docs/` | kebab-case | `workflow-index.md`, `common-patterns.md` |
| `schemas/` | kebab-case | `frontmatter-schema.json` |

---

## Cross-Referencing

### Workflows Referencing Docs

Workflows can reference documentation in `docs/`:

```markdown
**See:** [common-patterns.md](../docs/common-patterns.md) for reusable patterns
**See:** [context-loading-patterns.md](../docs/context-loading-patterns.md) for loading strategies
```

### Rules Referencing Docs

Rules can reference documentation in `docs/`:

```markdown
**Detailed patterns:** [batch-operations.md](../docs/batch-operations.md)
```

### Generated Indexes

Generated indexes are stored in `docs/`:

- `docs/workflow-index.md` - Auto-generated from workflow frontmatter
- `docs/rules-index.md` - Auto-generated from rule frontmatter
- `docs/workflow-dependencies.md` - Auto-generated dependency graph

**Generation Command:**

```bash
python scripts/generate_indexes.py
```

---

## Migration Notes

### 2025-10-19: Directory Cleanup

**Changes:**

- Moved `workflows/INDEX.md` → `docs/workflow-index.md`
- Moved `workflows/DEPENDENCIES.md` → `docs/workflow-dependencies.md`
- Moved `rules/INDEX.md` → `docs/rules-index.md`
- Moved `templates/common-patterns.md` → `docs/common-patterns.md`
- Deleted `templates/` directory (empty)

**Rationale:**

- Keep `workflows/` and `rules/` directories pure (only executable content)
- Centralize supporting documentation in `docs/`
- Improve discoverability and maintainability
- Enforce clear separation of concerns

---

## Enforcement

### ls-lint Configuration

`.ls-lint.yml` enforces naming conventions:

```yaml
.windsurf/workflows:
  .md: kebab-case  # Workflows only

.windsurf/rules:
  .md: regex:\d{2}_[a-z_]+  # Rules only

.windsurf/docs:
  .md: kebab-case  # Supporting docs

.windsurf/schemas:
  .json: kebab-case  # Schemas only
```

### Pre-commit Validation

File naming is validated on every commit via `ls-lint` pre-commit hook.

---

## References

- [generate_indexes.py](../../scripts/generate_indexes.py) - Index generation script
- [.ls-lint.yml](../../.ls-lint.yml) - File naming enforcement
- [frontmatter-schema.json](../schemas/frontmatter-schema.json) - Frontmatter validation

---

**Maintained by:** mcp-web core team
**Version:** 1.0.0
**Status:** Active (enforced via ls-lint)

---

## Rule Metadata

**File:** `05_windsurf_structure.md`
**Trigger:** glob
**Estimated Tokens:** ~1,200
**Last Updated:** 2025-10-21
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- Directory structure
- Forbidden files
- Frontmatter format
- Validation

**Workflow References:**

- All workflows - Enforces structure when editing .windsurf/

**Dependencies:**

- Source: directory-structure.md

**Changelog:**

- 2025-10-21: Created from directory-structure.md
