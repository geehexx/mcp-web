---
created: "2025-10-17"
updated: "2025-10-21"
description: Batch load project context efficiently
auto_execution_mode: 3
category: Operations
complexity: 65
tokens: 2300
dependencies: []
status: active
---

# Load Context Workflow

**Purpose:** Efficiently load project context using batch operations to minimize tool calls and maximize AI understanding.

**Invocation:** `/load-context [scope]` (called by `/work`, `/implement`, `/plan`)

**Philosophy:** Load smarter, not more. Batch operations are 3-10x faster than sequential reads.

---

## Execution

**Task plan:** Only if called directly (not by parent)

**Scope options:**

| Scope | When | Files Loaded |
|-------|------|-------------|
| **full** | Planning, major changes | All docs, initiatives, ADRs, summaries (3), git log (10) |
| **active** | Current work | Active initiatives, recent summaries (3), unstaged changes |
| **initiative** | Specific initiative | Initiative file, related ADRs, module files, tests |
| **module** | Module/feature work | Module source + tests, related docs |
| **minimal** | Quick tasks | PROJECT_SUMMARY only |

---

## Stage 1: Determine Context Scope

### 1.1 Analyze Request

**If explicit scope provided:**

```bash
/load-context full          # Load everything
/load-context initiative    # Load active initiatives
/load-context module:auth   # Load auth module context
```

**If implicit (called by workflow):**

```yaml
/work → load-context active
/plan → load-context full
/implement → load-context initiative
```

**Scope routing:** `/work` → active, `/plan` → full, `/implement` → initiative

---

## Stage 2: Batch Loading

**Use `mcp0_read_multiple_files` for 3+ files (3-10x faster than sequential)**

**Priority order:** Essential (PROJECT_SUMMARY, initiatives) → Important (architecture, summaries) → Optional (ADRs, changelog)

---

## Stage 3: Load Files

**Implementation:** Use `mcp0_read_multiple_files` with paths from scope table above. Parse initiative files to extract related source/test files. Run git commands for commit history.

**Load times:** full=2-3s, active=1s, initiative=1s, module<1s, minimal<0.5s

---

## Stage 4: Parse Context

**Extract:** Version, status, active tasks (`[ ]`), priorities, next steps from summaries

- Next steps
- Unresolved issues
- Key decisions
- Work patterns

**From git log:**

- Recent commit types
- Active areas of development
- Commit patterns

### 4.2 Identify Next Steps

**Combine information to determine:**

```markdown
## Context Summary

**Current State:**
- Version: 0.2.1
- Active Initiative: API Key Authentication (Phase 2)
- Last Session: 2025-10-17 (implemented validation logic)

**Next Steps (from session summary):**
1. Add CLI key management commands
2. Add integration tests for key rotation
3. Update documentation

**Blockers:** None

**Related Files:**
- src/mcp_web/auth.py (modified 2h ago)
- tests/unit/test_auth.py (15 tests passing)
- docs/initiatives/active/api-key-auth.md (Phase 2 in progress)
```

---

## Stage 5: Optimization Techniques

### 5.1 Avoid Redundant Reads

**Cache loaded context within session:**

```python
# ❌ BAD: Re-read same file multiple times
load_context("full")  # Reads PROJECT_SUMMARY.md
# ... later in session ...
load_context("active")  # Reads PROJECT_SUMMARY.md again

# ✅ GOOD: Reuse already loaded context
if not context_cache.has("PROJECT_SUMMARY.md"):
    load_project_summary()
```

### 5.2 Use Glob Patterns

**Load multiple files with one pattern:**

```python
# ❌ BAD: List files then read individually
files = list_dir("docs/initiatives/active/")
for file in files:
    read_file(file)

# ✅ GOOD: Use glob in batch read
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/docs/initiatives/active/*.md"
])
```

### 5.3 Lazy Loading

**Load only when needed:**

```python
# Load essential context first
load_essential_context()

# Load additional context only if required
if task_requires_architecture_context():
    load_architecture_docs()
```

---

## Stage 6: Context Validation

### 6.1 Verify All Files Loaded

**Check for load errors:**

```python
loaded_files = context.get_loaded_files()
expected_files = [
    "PROJECT_SUMMARY.md",
    "docs/initiatives/active/api-key-auth.md"
]

missing = [f for f in expected_files if f not in loaded_files]
if missing:
    print(f"⚠️ Warning: Could not load {missing}")
```

### 6.2 Check Context Completeness

**Ensure critical information present:**

```markdown
✅ Project version: Found (0.2.1)
✅ Active initiatives: Found (1)
✅ Recent commits: Found (5)
⚠️ Session summary: Not found (new session)
```

---

## Examples

### Example 1: Planning New Feature

**Invocation:** `/plan` → calls `/load-context full`

**Loads:**

```python
# Batch 1: Core docs (4 files)
- PROJECT_SUMMARY.md
- docs/reference/CHANGELOG.md
- ARCHITECTURE.md
- CONSTITUTION.md

# Batch 2: Active initiatives (2 files)
- docs/initiatives/active/api-key-auth.md
- docs/initiatives/active/performance-optimization.md

# Batch 3: Recent summaries (3 files)
- docs/archive/session-summaries/2025-10-17-*.md
- docs/archive/session-summaries/2025-10-16-*.md
- docs/archive/session-summaries/2025-10-15-*.md

# Git log (command)
git log --oneline -10
```

**Time:** ~2.5 seconds
**Context:** Complete understanding for planning

### Example 2: Continuing Work

**Invocation:** `/work` → calls `/load-context active`

**Loads:**

```python
# Batch 1: Essential (2 files + glob)
- PROJECT_SUMMARY.md
- docs/initiatives/active/*.md

# Batch 2: Recent summary (1 file)
- docs/archive/session-summaries/2025-10-17-afternoon.md

# Git status (command)
git status --short
git log --oneline -5
```

**Time:** ~1 second
**Context:** Current work state and next steps

### Example 3: Quick Bug Fix

**Invocation:** `/implement bug-fix` → calls `/load-context minimal`

**Loads:**

```python
# Single file
- PROJECT_SUMMARY.md

# Git status
git status --short
```

**Time:** <0.5 seconds
**Context:** Basic project info, ready to work

---

## Anti-Patterns

### ❌ Don't: Sequential Reads

**Bad:**

```python
read_file("PROJECT_SUMMARY.md")  # Tool call 1
read_file("docs/reference/CHANGELOG.md")             # Tool call 2
read_file("ARCHITECTURE.md")          # Tool call 3
# 3 calls → ~1.5 seconds
```

**Good:**

```python
mcp0_read_multiple_files([
    "PROJECT_SUMMARY.md",
    "docs/reference/CHANGELOG.md",
    "ARCHITECTURE.md"
])
# 1 call → ~0.5 seconds
```

### ❌ Don't: Over-Load Context

**Bad:**

```python
# Load every file in project
load_all_source_files()
load_all_tests()
load_all_docs()
# Result: Context window overflow, slow loading
```

**Good:**

```python
# Load only what's needed for task
if task == "implement auth":
    load_context("module:auth")
```

### ❌ Don't: Under-Load Context

**Bad:**

```python
# Start implementing without any context
implement_feature()
# Result: Missing critical information, incorrect approach
```

**Good:**

```python
# Load relevant context first
load_context("initiative")
understand_requirements()
implement_feature()
```

---

## Performance Metrics

**Measured load times (approximate):**

| Scope | Files | Tool Calls | Time |
|-------|-------|-----------|------|
| Minimal | 1 | 1 | 0.3s |
| Module | 3-5 | 1 | 0.8s |
| Active | 5-8 | 2 | 1.2s |
| Initiative | 8-12 | 2-3 | 1.5s |
| Full | 15-25 | 4-5 | 2.5s |

**Optimization impact:**

- Batch reads: 3-5x faster than sequential
- Glob patterns: 2-3x faster than list+read
- Smart scoping: 5-10x faster than loading everything

---

## Integration Points

### Called By

- `/work` - Automatic context detection
- `/plan` - Full context for planning
- `/implement` - Initiative or module context
- User - Direct invocation with scope

### Calls

- MCP filesystem tools (batch reads)
- Git commands (log, status)
- Directory listing (for file discovery)

**Print workflow entry:**

```markdown
✅ **Starting /load-context:** Loading context for task...
```

**Print workflow exit:**

```markdown
✅ **Completed /load-context:** Context loaded successfully ([N] files in [N] batches)
```

---

## References

- [Anthropic Context Window Best Practices](https://docs.anthropic.com/claude/docs/context-window)
- [Factory.ai Context Stack Pattern](https://factory.ai/news/context-window-problem)
- Project: `.windsurf/rules/07_context_optimization.md`
- Project: `.windsurf/workflows/work.md` (Context loading examples)

---
