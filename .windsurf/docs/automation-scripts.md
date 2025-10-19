---
type: machine-readable-reference
category: automation-tools
purpose: Quick reference for automation scripts and Taskfile commands
token_budget: medium
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "2025-10-20"
tags: ["automation", "scripts", "taskfile", "efficiency", "file-operations"]
---

# Automation Scripts Reference

**Purpose:** Discovery document for automation scripts that reduce token expenditure on mechanical tasks.

**Key Principle:** Always prefer automation over manual operations for repetitive tasks.

---

## Quick Decision Matrix

| Task | Use This | Token Savings |
|------|----------|---------------|
| Create initiative | `task scaffold:initiative` | 97% (1500→50 tokens) |
| Create ADR | `task scaffold:adr` | 96% (1200→50 tokens) |
| Archive initiative | `task archive:initiative NAME=<name>` | 90x faster (15min→10s) |
| Move file + update refs | `task move:file SRC=<src> DST=<dst>` | 100% (automated) |
| Update initiative index | `task update:index` | 100% (automated) |
| Create session summary | `task scaffold:summary` | 96% (2500→100 tokens) |

---

## Pattern: When to Use Scripts

**✅ USE scripts for:**

- Template generation (initiatives, ADRs, summaries)
- File archival with cross-reference updates
- Index regeneration
- Repetitive file operations
- Validation tasks

**❌ DON'T use scripts for:**

- One-off edits
- Context-heavy decisions
- Content writing
- Code implementation

---

## High-Impact Commands

### 1. Initiative Management

**Create new initiative:**

```bash
task scaffold:initiative
# Interactive prompts for all fields
# Auto-generates frontmatter, dates, structure
```

**Archive completed initiative:**

```bash
task archive:initiative NAME=2025-10-18-my-initiative
# Moves to completed/, updates references, adds archive banner
# Optional: DRY_RUN=true to preview
```

**Validation:**

```bash
task validate:initiatives
# Validates frontmatter, status, dates
# Runs in pre-commit hook
```

---

### 2. Document Generation

**Create ADR:**

```bash
task scaffold:adr
# Interactive: title, status, context, decision
# Auto-numbers (finds highest ADR number + 1)
```

**Create session summary:**

```bash
task scaffold:summary
# Interactive: date, type, duration, objectives
# Auto-generates structure
```

---

### 3. File Operations

**Move file with automatic reference updates:**

```bash
task move:file SRC=docs/old.md DST=docs/new.md
# Updates ALL repository references automatically
# Searches .md, .yml, .yaml, .toml, .json, .py
```

**Update initiative index:**

```bash
task update:index DIR=docs/initiatives
# Regenerates README.md with Active/Completed sections
# Idempotent (safe to run multiple times)
```

---

### 4. Validation & Quality

**Validate workflows:**

```bash
task validate:workflows
# YAML schema, cross-refs, complexity, tokens
# Runs in pre-commit hook
```

**Check token counts:**

```bash
task check:workflow-tokens
# Monitor token budget (60,000 limit)
# Compare to baseline
```

---

## Integration with Workflows

### Archive Initiative Workflow

**OLD (manual):**

```markdown
1. Update initiative status
2. Move file to completed/
3. Search for references manually
4. Update each reference
5. Add archive banner
6. Update index
```

**NEW (automated):**

```bash
task archive:initiative NAME=my-initiative
# All 6 steps automated in 10 seconds
```

### Session End Protocol

**When archiving initiative:**

```markdown
1. Mark initiative "Completed"
2. Run: task archive:initiative NAME=<initiative-folder>
3. Commit changes
4. Run meta-analysis
```

---

## Script Details

### scaffold.py - Template Generation

**Location:** `scripts/scaffold.py`

**Templates:**

- `initiative-flat.md.j2` - Single-file initiative
- `initiative-folder/` - Multi-file initiative with artifacts/phases
- `adr.md.j2` - Architecture Decision Record
- `session-summary.md.j2` - Session summary

**Features:**

- Interactive prompts
- Config file support (YAML/JSON)
- Auto-numbering (ADRs)
- Auto-dating (all templates)
- Markdown validation
- Dry-run mode

**Test coverage:** 26 tests (100% passing)

---

### file_ops.py - File Operations

**Location:** `scripts/file_ops.py`

**Functions:**

- `archive_initiative()` - Archive with reference updates
- `move_file_with_refs()` - Move + update all refs
- `update_index()` - Regenerate initiative index

**Features:**

- Automatic cross-reference updates (repo-wide)
- Archive banner insertion
- Path safety validation
- Dry-run mode
- CLI + programmatic access

**Test coverage:** 4 tests (100% passing)

---

### validate_archival.py - Archival Gates

**Location:** `scripts/validate_archival.py`

**Gates:**

1. Status Completion (CRITICAL)
2. Success Criteria (CRITICAL)
3. Blockers (WARNING)
4. Dependencies (CRITICAL)
5. Documentation (WARNING)

**Usage:**

```bash
python scripts/validate_archival.py docs/initiatives/active/my-initiative/initiative.md
# Returns exit code 0 (pass) or 1 (fail)
```

---

### validate_workflows.py - Workflow Quality

**Location:** `scripts/validate_workflows.py`

**Checks:**

- YAML frontmatter schema
- Cross-reference validity
- Complexity metrics
- Token count accuracy
- Outdated tool references

**Integration:** Pre-commit hook + CI/CD

---

### check_workflow_tokens.py - Token Monitoring

**Location:** `scripts/check_workflow_tokens.py`

**Features:**

- Token counting (workflows + rules)
- Baseline tracking
- Threshold enforcement (60,000)
- Historical tracking (`.benchmarks/`)

**Usage:**

```bash
python scripts/check_workflow_tokens.py --threshold 60000
python scripts/check_workflow_tokens.py --save-baseline
```

---

## Taskfile Command Reference

### Testing

- `task test` - All tests (parallel)
- `task test:fast` - Fast tests only
- `task test:unit` - Unit tests
- `task lint` - All linters
- `task security` - Security checks

### Scaffolding

- `task scaffold:initiative` - New flat initiative
- `task scaffold:initiative-folder` - New folder initiative
- `task scaffold:adr` - New ADR
- `task scaffold:summary` - New session summary

### File Operations

- `task archive:initiative NAME=<name>` - Archive initiative
- `task move:file SRC=<src> DST=<dst>` - Move + update refs
- `task update:index DIR=<dir>` - Update index

### Validation

- `task validate:initiatives` - Validate all initiatives
- `task validate:workflows` - Validate workflows/rules
- `task check:workflow-tokens` - Check token budget

### Documentation

- `task docs:lint` - Lint all docs
- `task docs:lint:markdown` - Markdown linting
- `task docs:lint:prose` - Prose quality

---

## Performance Benefits

| Operation | Manual | Automated | Speedup |
|-----------|--------|-----------|---------|
| Create initiative | 5 min | 30 sec | 10x |
| Archive initiative | 15 min | 10 sec | 90x |
| Move file + refs | 10 min | 5 sec | 120x |
| Update index | 5 min | 2 sec | 150x |
| Create ADR | 5 min | 30 sec | 10x |

**Total token savings:** 94-97% for template generation

---

## Task System Compatibility

**Scripts that appear in task lists:**

✅ **Pre-commit validation scripts** - Silent, don't need task tracking:

- `validate_workflows.py`
- `check_workflow_tokens.py`
- `validate_task_format.py`
- `validate_initiatives.py`

✅ **User-invoked scripts** - Task tracking when called from workflows:

- `task archive:initiative` - Track as `/archive-initiative` workflow step
- `task scaffold:initiative` - Track as manual user action (not in workflow)

**Rule:** Only track scripts when they're part of a workflow. Pre-commit hooks run silently and don't need task tracking.

---

## Common Patterns

### Pattern 1: Create New Initiative

```bash
# 1. Run scaffolder
task scaffold:initiative

# 2. Follow interactive prompts
# Title: My New Feature
# Owner: AI Agent Team
# Priority: High

# 3. Edit generated file
# (scaffold creates docs/initiatives/active/2025-10-20-my-new-feature.md)
```

### Pattern 2: Archive Completed Initiative

```bash
# 1. Mark initiative "Completed" in frontmatter
# 2. Run archival
task archive:initiative NAME=2025-10-18-my-feature

# 3. Verify
git status  # Check moved files and updated references
```

### Pattern 3: Move File Safely

```bash
# Preview changes first
task move:file SRC=docs/old.md DST=docs/new.md DRY_RUN=true

# Execute move
task move:file SRC=docs/old.md DST=docs/new.md

# All references automatically updated
```

---

## Anti-Patterns

### ❌ Don't: Manually Archive Initiatives

```markdown
# ❌ Wrong: Manual 6-step process (error-prone, slow)
1. Edit status...
2. Move file...
3. Find references...
4. Update each...
5. Add banner...
6. Update index...

# ✅ Correct: One command
task archive:initiative NAME=my-initiative
```

### ❌ Don't: Manual Template Creation

```markdown
# ❌ Wrong: Copy-paste from old initiative (1500 tokens)
# ✅ Correct: Use scaffolder (50 tokens)
task scaffold:initiative
```

### ❌ Don't: Move Files Without Updating References

```bash
# ❌ Wrong: Broken links
mv docs/old.md docs/new.md

# ✅ Correct: Automatic reference updates
task move:file SRC=docs/old.md DST=docs/new.md
```

---

## References

- **Full documentation:** [scripts/README.md](../../scripts/README.md)
- **Taskfile:** [Taskfile.yml](../../Taskfile.yml)
- **Source code:** `scripts/*.py`
- **Tests:** `tests/unit/test_*.py`

**External Research:**

- [GitHub: Agentic Primitives](https://github.blog/ai-and-ml/github-copilot/how-to-build-reliable-ai-workflows-with-agentic-primitives-and-context-engineering/)
- [Anthropic: Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

---

**Maintained by:** mcp-web core team
**Version:** 1.0.0
**Last verified:** 2025-10-20
