---
created: "2025-10-17"
updated: "2025-10-18"
description: Batch load project context efficiently
auto_execution_mode: 3
category: Operations
complexity: 65
tokens: 3454
dependencies: []
status: active
---

# Load Context Workflow

**Purpose:** Efficiently load project context using batch operations to minimize tool calls and maximize AI understanding.

**Invocation:** `/load-context [scope]` (called by `/work`, `/implement`, `/plan`)

**Philosophy:** Load smarter, not more. Batch operations are 3-10x faster than sequential reads.

---

## Stage 0: Workflow Entry

🔄 **Entering /load-context:** Efficient batch context loading

**Print workflow entry announcement:**

```markdown
🔄 **Entering /load-context:** Loading project context with batch operations
```

---

## Stage 1: Create Task Plan (If Called Directly)

🔄 **Entering Stage 1: Create Task Plan**

**If called directly by user** (not by parent workflow), create task plan:

```typescript
update_plan({
  explanation: "📂 Starting /load-context workflow",
  plan: [
    { step: "1. /load-context - Determine context scope", status: "in_progress" },
    { step: "2. /load-context - Batch load files", status: "pending" },
    { step: "3. /load-context - Parse and extract key information", status: "pending" },
    { step: "4. /load-context - Validate context completeness", status: "pending" }
  ]
})
```

**If called by parent workflow** (e.g., `/implement` step 3.1), parent already has task tracking.

---

## Scope Options

**Available scopes:**

1. **full** - Complete project context (for planning, major changes)
2. **active** - Current work context (active initiatives, recent changes)
3. **initiative** - Specific initiative context (requires initiative path)
4. **module** - Specific module/feature context (requires module name)
5. **minimal** - Essential context only (for quick tasks)

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

### 1.2 Scope Definitions

**Full Scope:**

- Project summary and changelog
- Architecture documentation
- All active initiatives
- All active ADRs
- Recent session summaries (3 most recent)
- Git log (last 10 commits)

**Active Scope:**

- Project summary
- Active initiatives (1-3 files)
- Recent session summary (1 most recent)
- Git log (last 5 commits)
- Current branch status

**Initiative Scope:**

- Specific initiative file
- Related source files
- Related test files
- Related ADRs
- Recent commits related to initiative

**Module Scope:**

- Module source files
- Module test files
- Module documentation
- Related dependencies

**Minimal Scope:**

- Project summary only
- Git status

---

## Stage 2: Batch Loading Strategy

### 2.1 Use MCP Batch Read

**Always batch reads when loading 3+ files:**

```python
# ❌ BAD: Sequential reads (slow)
mcp0_read_text_file("/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md")
mcp0_read_text_file("/home/gxx/projects/mcp-web/docs/reference/CHANGELOG.md")
mcp0_read_text_file("/home/gxx/projects/mcp-web/docs/architecture/ARCHITECTURE.md")
# 3 tool calls → ~1.5 seconds

# ✅ GOOD: Batch read (fast)
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    "/home/gxx/projects/mcp-web/docs/reference/CHANGELOG.md",
    "/home/gxx/projects/mcp-web/docs/architecture/ARCHITECTURE.md"
])
# 1 tool call → ~0.5 seconds (3x faster)
```

### 2.2 Prioritize Critical Context

**Load in order of importance:**

1. **Essential** (always load first)
   - PROJECT_SUMMARY.md
   - Active initiatives

2. **Important** (load if relevant)
   - Architecture docs
   - Recent session summaries
   - Git log

3. **Optional** (load if needed)
   - All ADRs
   - Full changelog
   - Archived initiatives

---

## Stage 3: Context Loading by Scope

### 3.1 Full Scope Loading

**Maximum context for planning:**

```python
# Batch 1: Core documents
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    "/home/gxx/projects/mcp-web/docs/reference/CHANGELOG.md",
    "/home/gxx/projects/mcp-web/docs/architecture/ARCHITECTURE.md",
    "/home/gxx/projects/mcp-web/docs/CONSTITUTION.md"
])

# Batch 2: Active initiatives (glob pattern)
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/docs/initiatives/active/*.md"
])

# Batch 3: Recent session summaries (3 most recent)
session_files = [
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/2025-10-17-*.md",
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/2025-10-16-*.md",
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/2025-10-15-*.md"
]
mcp0_read_multiple_files(session_files)

# Batch 4: Key ADRs (most recent 5)
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/docs/adr/0017-*.md",
    "/home/gxx/projects/mcp-web/docs/adr/0016-*.md",
    "/home/gxx/projects/mcp-web/docs/adr/0015-*.md",
    "/home/gxx/projects/mcp-web/docs/adr/0014-*.md",
    "/home/gxx/projects/mcp-web/docs/adr/0013-*.md"
])
```

**Estimated load time:** 2-3 seconds (4 batch calls)

### 3.2 Active Scope Loading

**Current work context:**

```python
# Batch 1: Essential context
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    "/home/gxx/projects/mcp-web/docs/initiatives/active/*.md"
])

# Batch 2: Recent context
session_files = list_recent_session_summaries(limit=1)
mcp0_read_multiple_files(session_files)

# Command: Git log
git log --oneline -5
git status --short
```

**Estimated load time:** ~1 second (2 batch calls + git)

### 3.3 Initiative Scope Loading

**Specific initiative context:**

```python
# Read initiative file to identify dependencies
mcp0_read_text_file(f"/home/gxx/projects/mcp-web/docs/initiatives/active/{initiative_name}.md")

# Parse initiative for file references
# Example: Extract "src/mcp_web/auth.py", "tests/unit/test_auth.py"

# Batch load all related files
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/src/mcp_web/auth.py",
    "/home/gxx/projects/mcp-web/tests/unit/test_auth.py",
    "/home/gxx/projects/mcp-web/docs/adr/0012-auth-strategy.md",
    "/home/gxx/projects/mcp-web/docs/guides/SECURITY_GUIDE.md"
])

# Git log for initiative-related commits
git log --grep="auth" --oneline -10
```

**Estimated load time:** ~1 second (2 reads + git)

### 3.4 Module Scope Loading

**Module-specific context:**

```python
module_name = "auth"  # Example

# Batch load module files
mcp0_read_multiple_files([
    f"/home/gxx/projects/mcp-web/src/mcp_web/{module_name}.py",
    f"/home/gxx/projects/mcp-web/tests/unit/test_{module_name}.py",
    f"/home/gxx/projects/mcp-web/tests/integration/test_{module_name}_integration.py"
])

# Grep for related documentation
grep_search(module_name, "/home/gxx/projects/mcp-web/docs/", recursive=True, includes=["*.md"])
```

**Estimated load time:** <1 second (1 batch + grep)

### 3.5 Minimal Scope Loading

**Quick context for simple tasks:**

```python
# Single file read
mcp0_read_text_file("/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md")

# Git status
git status --short
```

**Estimated load time:** <0.5 seconds

---

## Stage 4: Context Parsing

### 4.1 Extract Key Information

**From PROJECT_SUMMARY.md:**

- Current version
- Project status
- Key features
- Recent changes

**From initiatives:**

- Active tasks (unchecked `[ ]` items)
- Status field
- Priority
- Dependencies

**From session summaries:**

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
