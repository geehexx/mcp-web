---
trigger: model_decision
description: Apply for context loading batch operations or performance optimization work
---

# Context and Performance Optimization

## When to Batch Operations

| Scenario | Batch? | Reason |
|----------|--------|--------|
| 3+ independent items | ✅ Yes | 3-10x faster |
| I/O-bound operations | ✅ Yes | Parallelism wins |
| Items depend on previous | ❌ No | Sequential required |
| CPU-bound tasks | ⚠️ Maybe | Use different parallelization |
| Memory constrained | ❌ No | Stream instead |

---

## Optimal Batch Sizes

| Operation | Batch Size | Reason |
|-----------|------------|--------|
| Local file reads | 10-15 | Balance parallelism vs overhead |
| Network file reads | 5-10 | Network latency dominates |
| URL fetches | 3-5 | Rate limiting, politeness |
| LLM API calls | 1-3 | API rate limits |
| Database queries | 50-100 | Connection pooling |

---

## Context Loading Patterns

Initiative Context

**Use:** Load all files for an active initiative

```python
# 1. Identify initiative files
initiative_dir = "docs/initiatives/active/feature-x/"
core_files = [
    f"{initiative_dir}initiative.md",
    f"{initiative_dir}plan.md",
    "src/feature_x.py",
    "tests/test_feature_x.py"
]

# 2. Batch load
mcp0_read_multiple_files(core_files)
```

**Performance:** 5-10x faster than sequential

---

## Pattern 2: Hierarchical Loading

**Use:** Load project context progressively

```python
# Phase 1: High-level overview
overview_files = [
    "README.md",
    "docs/CONSTITUTION.md",
    "docs/DOCUMENTATION_STRUCTURE.md"
]
mcp0_read_multiple_files(overview_files)

# Phase 2: Relevant subsystem (based on Phase 1)
subsystem_files = find_by_name(
    SearchDirectory="src/subsystem/",
    Pattern="*.py",
    MaxDepth=2
)
mcp0_read_multiple_files(subsystem_files[:10])

# Phase 3: Deep dive (if needed)
# Load specific files identified in Phase 2
```

**Benefits:** Minimal tokens, targeted loading, progressive refinement

---

## Quick Reference

**Batch file reads:** Use `mcp0_read_multiple_files` for 3+ files (3-10x faster)
**Optimal size:** 10-15 files per batch
**Parallel searches:** Independent grep_search calls in parallel

**Performance targets:**
- 5 files: <1s
- 10 files: <2s  
- 15 files: <3s



---

## Rule Metadata

**File:** `07_context_optimization.md`  
**Trigger:** model_decision  
**Estimated Tokens:** ~2,500  
**Last Updated:** 2025-10-21  
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)


**Topics Covered:**
- Batch operations
- Parallel loading
- Context patterns
- Performance optimization

**Workflow References:**
- /load-context - Context loading
- /work - Batch optimization

**Dependencies:**
- Merged: batch-operations.md + context-loading-patterns.md

**Changelog:**
- 2025-10-21: Created from batch-operations.md and context-loading-patterns.md