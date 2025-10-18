---
description: Shared patterns for efficient context loading
category: Reference Guide
---

# Context Loading Patterns

**Purpose:** Reusable patterns for loading files and context efficiently across workflows.

**Used By:** Multiple workflows (consolidate-summaries, load-context, detect-context, etc.)

---

## Overview

Context loading is a frequent operation in workflows. These patterns optimize for speed and reliability.

**Key Principles:**

- Batch operations are 3-10x faster than sequential
- MCP tools require absolute paths
- Parallel operations for I/O-bound tasks
- Graceful error handling

---

## Pattern 1: Batch Reading

### Basic Batch Read

**Purpose:** Load multiple files in parallel

**When to Use:** Loading 3+ files with known paths

**Implementation:**

```python
mcp0_read_multiple_files(paths=[
    "/home/gxx/projects/mcp-web/file1.md",
    "/home/gxx/projects/mcp-web/file2.md",
    "/home/gxx/projects/mcp-web/file3.md"
])
```

**Best Practices:**

- Process 10-15 files per batch (optimal performance)
- Use absolute paths for MCP tools
- Handle missing files gracefully
- See [Batch Operations](./batch-operations.md) for optimization

### Glob-Based Batch Read

**Purpose:** Load all files matching pattern

**When to Use:** Unknown number of files or wildcard patterns

**Implementation:**

```bash
# Find files first
files=$(find docs/initiatives/active -name "*.md")

# Batch read
mcp0_read_multiple_files(paths=files)
```

**Performance:**

- 3-10x faster than sequential reads
- Optimal batch size: 10-15 files
- Use for I/O-bound operations

---

## Pattern 2: Priority-Based Loading

### Load Order Strategy

**Purpose:** Load most important files first

**When to Use:** Large context sets with priority levels

**Implementation:**

```python
# Priority 1: Essential context (load immediately)
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    "/home/gxx/projects/mcp-web/docs/initiatives/active/current-initiative.md"
])

# Priority 2: Related context (load if time permits)
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/docs/adr/relevant-adr.md",
    "/home/gxx/projects/mcp-web/src/module.py"
])

# Priority 3: Optional context (load on demand)
# Skip unless explicitly needed
```

**Priority Levels:**

1. **Essential:** Initiative, PROJECT_SUMMARY (always load)
2. **Related:** Source files, tests, ADRs (load for implementation)
3. **Optional:** Historical summaries, full docs (load on demand)

---

## Pattern 3: Incremental Loading

### Progressive Context Loading

**Purpose:** Load context in stages as needed

**When to Use:** Large codebases or complex initiatives

**Implementation:**

```python
# Stage 1: Core context (50-100 lines)
read_file("initiative.md", limit=100)

# If more detail needed: Stage 2
read_file("initiative.md")  # Full file

# If implementation needed: Stage 3
mcp0_read_multiple_files([
    source_files,
    test_files
])
```

**Benefits:**

- Faster initial load
- Reduced token usage
- Load more only when needed

---

## Pattern 4: Conditional Loading

### Decision-Based Loading

**Purpose:** Load files based on runtime conditions

**When to Use:** Context depends on detected signals

**Implementation:**

```python
if has_test_failures:
    # Load test context
    mcp0_read_multiple_files([test_files])
elif has_active_initiative:
    # Load initiative context
    mcp0_read_multiple_files([initiative_files])
elif needs_planning:
    # Load full context
    mcp0_read_multiple_files([all_files])
```

**Decision Factors:**

- Detected signals (tests, initiatives, git status)
- Workflow type (implement vs plan vs commit)
- User request specificity

---

## Pattern 5: Error Handling

### Graceful Failure

**Purpose:** Handle missing or inaccessible files

**When to Use:** Always (especially with glob patterns)

**Implementation:**

```python
try:
    mcp0_read_multiple_files(paths)
except FileNotFoundError as e:
    # Log and continue
    print(f"Warning: File not found: {e.filename}")
    # Load remaining files
except PermissionError as e:
    # Skip protected files
    print(f"Skipping protected file: {e.filename}")
```

**Error Strategies:**

- **Critical files:** Fail fast, report to user
- **Optional files:** Log warning, continue
- **Missing globs:** Empty result is OK

---

## Pattern 6: Scope-Based Loading

### Context Scopes

**Purpose:** Load appropriate files for workflow type

**Scopes:**

| Scope | Files to Load | Use Case |
|-------|---------------|----------|
| `initiative` | Initiative + related source + tests | Implementation work |
| `module:tests` | Test files + module under test | Test fixes |
| `module:src` | Source files + related tests | Code changes |
| `full` | PROJECT_SUMMARY + all initiatives + ADRs | Planning |
| `docs` | Documentation files only | Doc updates |

**Implementation:**

```python
if scope == "initiative":
    files = [
        initiative_file,
        *related_source_files,
        *related_test_files
    ]
elif scope == "full":
    files = [
        "PROJECT_SUMMARY.md",
        *active_initiatives,
        *recent_adrs
    ]

mcp0_read_multiple_files(files)
```

---

## Pattern 7: Session History Loading

### Recent Session Context

**Purpose:** Load recent session summaries for continuity

**When to Use:** Context detection, continuation

**Implementation:**

```bash
# Get 2-3 most recent summaries
recent_summaries=$(ls -t docs/archive/session-summaries/*.md | head -3)

# Read for "Next Steps" and "Unresolved" sections
mcp0_read_multiple_files(recent_summaries)
```

**Focus Areas:**

- "Next Steps" section → continuation points
- "Unresolved" section → blockers
- "Key Learnings" section → context for decisions

---

## Performance Tips

### Optimization Strategies

1. **Batch over Sequential:** 3-10x faster
2. **Parallel I/O:** Use for independent operations
3. **Limit File Sizes:** Read head/tail for large files
4. **Cache Results:** Within session, avoid re-reads
5. **Filter Early:** Reduce files before loading

### Benchmarks

| Operation | Sequential | Batch | Speedup |
|-----------|-----------|-------|---------|
| 5 files | ~5s | ~1s | 5x |
| 10 files | ~10s | ~2s | 5x |
| 20 files | ~20s | ~4s | 5x |

**Note:** Benchmarks assume I/O-bound operations with typical network/disk latency.

---

## Common Combinations

### Initiative Work Pattern

```python
# Load initiative + context
mcp0_read_multiple_files([
    initiative_file,
    *source_files_from_initiative,
    *test_files_from_initiative,
    *related_adrs
])
```

### Planning Pattern

```python
# Load full context for planning
mcp0_read_multiple_files([
    "PROJECT_SUMMARY.md",
    *active_initiatives,
    *recent_adrs,
    *recent_session_summaries
])
```

### Test Fix Pattern

```python
# Load test context
mcp0_read_multiple_files([
    test_files_with_failures,
    module_under_test,
    related_fixtures
])
```

---

## Tool Selection

### MCP vs Standard Tools

**MCP Tools (mcp0_*):**

- Required for `.windsurf/` directory
- Require absolute paths
- Better error handling

**Standard Tools:**

- Work for regular files
- Accept relative paths
- Simpler API

**Decision:**

```python
if file_path.startswith(".windsurf/"):
    # Use MCP tool with absolute path
    mcp0_read_text_file(f"/home/gxx/projects/mcp-web/{file_path}")
else:
    # Use standard tool
    read_file(file_path)
```

---

## References

- [Batch Operations](./batch-operations.md) - Optimization strategies
- [load-context.md](./load-context.md) - Context loading workflow
- [detect-context.md](./detect-context.md) - Context detection
- Agent directives: [00_agent_directives.md](../rules/00_agent_directives.md) - Section 1.10

---

**Version:** 1.0.0 (Extracted from consolidate-summaries.md Phase 4 decomposition)
**Last Updated:** 2025-10-18
