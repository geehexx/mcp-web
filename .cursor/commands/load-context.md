---
pass_through: true
description: Batch load project context efficiently
title: Load Context Workflow
tags: ['context', 'loading', 'batch', 'efficiency']
related: []
---

# Load Context Workflow

**Purpose:** Efficiently load project context using batch operations (3-10x faster than sequential).

**Invocation:** `/load-context [scope]` (called by `/work`, `/implement`, `/plan`)

**Philosophy:** Batch operations minimize tool calls, maximize understanding.

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

## Stage 1: Determine Context Scope

### 1.1 Analyze Request

**If explicit scope provided:**

```bash
/load-context full          # Load everything
/load-context initiative    # Load active initiatives
/load-context module:auth   # Load auth module context
```

**If no scope provided:**

- Check current work context
- Determine appropriate scope
- Load accordingly

### 1.2 Scope Selection Logic

**Full scope triggers:**

- Planning major changes
- Architecture decisions
- Cross-cutting concerns

**Active scope triggers:**

- Current initiative work
- Recent session continuation
- Ongoing development

**Initiative scope triggers:**

- Specific initiative mentioned
- Initiative file changes
- Related work

**Module scope triggers:**

- Feature development
- Bug fixes
- Refactoring

**Minimal scope triggers:**

- Quick tasks
- Simple changes
- Documentation updates

## Stage 2: Batch Load Files

### 2.1 Full Scope Loading

```python
# Load all documentation and context
files_to_load = [
    # Project overview
    "/home/gxx/projects/mcp-web/README.md",
    "/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",

    # Active initiatives
    "/home/gxx/projects/mcp-web/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/initiative.md",

    # Recent ADRs
    "/home/gxx/projects/mcp-web/docs/adr/0001-use-httpx-playwright-fallback.md",
    "/home/gxx/projects/mcp-web/docs/adr/0002-adopt-windsurf-workflow-system.md",

    # Recent session summaries
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/2025-10-22-*.md",

    # Git context
    "/home/gxx/projects/mcp-web/.git/HEAD"
]

# Batch read all files
mcp0_read_multiple_files(files_to_load)
```

### 2.2 Active Scope Loading

```python
# Load current work context
files_to_load = [
    # Active initiatives
    "/home/gxx/projects/mcp-web/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/initiative.md",

    # Recent summaries
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/2025-10-22-*.md",

    # Current changes
    "/home/gxx/projects/mcp-web/.git/index"
]

mcp0_read_multiple_files(files_to_load)
```

### 2.3 Initiative Scope Loading

```python
# Load specific initiative context
files_to_load = [
    # Initiative file
    "/home/gxx/projects/mcp-web/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/initiative.md",

    # Related ADRs
    "/home/gxx/projects/mcp-web/docs/adr/0002-adopt-windsurf-workflow-system.md",
    "/home/gxx/projects/mcp-web/docs/adr/0018-workflow-architecture-v3.md",

    # Related files
    "/home/gxx/projects/mcp-web/.unified/README.md",
    "/home/gxx/projects/mcp-web/scripts/build_ide_configs.py"
]

mcp0_read_multiple_files(files_to_load)
```

### 2.4 Module Scope Loading

```python
# Load module-specific context
files_to_load = [
    # Source files
    "/home/gxx/projects/mcp-web/src/mcp_web/module.py",

    # Test files
    "/home/gxx/projects/mcp-web/tests/test_module.py",

    # Related docs
    "/home/gxx/projects/mcp-web/docs/api/module.md"
]

mcp0_read_multiple_files(files_to_load)
```

## Stage 3: Process and Summarize

### 3.1 Extract Key Information

- **Initiative Status**: Current phase, completed tasks, next steps
- **Recent Changes**: Git commits, file modifications
- **Dependencies**: Related files, ADRs, documentation
- **Context**: Project state, ongoing work

### 3.2 Generate Context Summary

```markdown
## Context Summary

**Initiative**: [Name and status]
**Phase**: [Current phase]
**Recent Changes**: [Key modifications]
**Dependencies**: [Related files and docs]
**Next Steps**: [Planned actions]
```

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files, complex operations, or memory-intensive tasks
- **Task Orchestration**: `/rules/12_task_orchestration.mdc` - Apply when managing complex task coordination and workflow orchestration

## Workflow References

When this load-context workflow is called:

1. **Load**: `/commands/load-context.md`
2. **Execute**: Follow the context loading stages defined above
3. **Batch**: Use batch operations for efficiency
4. **Summarize**: Provide context summary

## Anti-Patterns

❌ **Don't:**

- Load files sequentially
- Load unnecessary files
- Skip context summarization
- Ignore scope selection

✅ **Do:**

- Use batch operations
- Load only relevant files
- Provide clear summaries
- Select appropriate scope

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Load time | <30s | ✅ |
| File efficiency | 3-10x faster | ✅ |
| Context accuracy | 95%+ | ✅ |
| Scope appropriateness | 90%+ | ✅ |

## Integration

**Called By:**

- `/work` - Main orchestration workflow
- `/implement` - Before implementation
- `/plan` - Before planning
- User - Direct invocation for context loading

**Calls:**

- Various file reading operations
- Git status checks
- Directory listing operations

**Exit:**

```markdown
✅ **Completed /load-context:** Context loading finished
```

---

## Command Metadata

**File:** `load-context.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,610
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Context loading
- Batch operations
- Scope selection
- Efficiency optimization

**Dependencies:**

- None (standalone workflow)
