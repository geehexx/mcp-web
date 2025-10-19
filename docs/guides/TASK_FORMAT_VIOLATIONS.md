# Common Task Format Violations Guide

**Purpose:** Reference guide for avoiding common task format violations based on Section 1.11 requirements.

**Last Updated:** 2025-10-19

---

## Overview

This guide documents the most common task format violations that occur when using `update_plan()` in workflows and provides correct examples for each.

**Validation Tool:**
`python scripts/validate_task_format.py --validate "task text"`

**Pre-commit Hook:**
Automatically validates task format in workflow documentation (`.windsurf/workflows/*.md`, session summaries)

---

## Violation 1: Missing Workflow Prefix

**Rule:** Every task MUST have `<number>. /<workflow> - <description>` format.

### ❌ **Wrong:**

```typescript
update_plan({
  plan: [
    { step: "1. Analyze project state", status: "in_progress" },
    { step: "2. Execute implementation", status: "pending" },
    { step: "  2.1. Create directory structure", status: "pending" }
  ]
})
```

**Problem:** Missing `/<workflow>` prefix in all tasks.

### ✅ **Correct:**

```typescript
update_plan({
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "in_progress" },
    { step: "2. /implement - Execute implementation", status: "pending" },
    { step: "  2.1. /implement - Create directory structure", status: "pending" }
  ]
})
```

**Fix:** Add workflow prefix between number and description.

---

## Violation 2: Removed Completed Tasks

**Rule:** Completed tasks must be preserved when updating plan (no history loss).

### ❌ **Wrong:**

```typescript
// First update
update_plan({
  plan: [
    { step: "1. /detect-context - Analyze", status: "completed" },
    { step: "2. /implement - Design tests", status: "completed" },
    { step: "3. /implement - Write tests", status: "in_progress" }
  ]
})

// Second update - WRONG! Lost tasks 1-2
update_plan({
  plan: [
    { step: "3. /implement - Write tests", status: "completed" },
    { step: "4. /implement - Implement code", status: "in_progress" }
  ]
})
```

**Problem:** Tasks 1-2 removed from history.

### ✅ **Correct:**

```typescript
// Second update - preserves all tasks
update_plan({
  plan: [
    { step: "1. /detect-context - Analyze", status: "completed" },
    { step: "2. /implement - Design tests", status: "completed" },
    { step: "3. /implement - Write tests", status: "completed" },
    { step: "4. /implement - Implement code", status: "in_progress" }
  ]
})
```

**Fix:** Always include ALL previous tasks with their current status.

---

## Violation 3: Wrong Workflow Attribution

**Rule:** Tasks MUST be attributed to the workflow that EXECUTES them, not the caller.

### ❌ **Wrong:**

```typescript
update_plan({
  plan: [
    { step: "1. /work - Fix prerequisite issues", status: "in_progress" },
    { step: "2. /work - Create validation script", status: "pending" },
    { step: "3. /plan - Write implementation code", status: "pending" }
  ]
})
```

**Problem:**

- `/work` is an orchestrator, doesn't execute fixes
- `/plan` is for planning, not writing code

### ✅ **Correct:**

```typescript
update_plan({
  plan: [
    { step: "1. /implement - Fix prerequisite issues", status: "in_progress" },
    { step: "2. /implement - Create validation script", status: "pending" },
    { step: "3. /implement - Write implementation code", status: "pending" }
  ]
})
```

**Fix:** Use executor workflows (`/implement`, `/validate`) for actual work.

**Workflow Categories:**

| Category | Workflows | Purpose |
|----------|-----------|---------|
| **Orchestrators** | `/work`, `/plan`, `/meta-analysis` | Coordinate, don't execute |
| **Executors** | `/implement`, `/validate`, `/commit` | Perform actual work |
| **Sub-workflows** | `/load-context`, `/detect-context`, `/research` | Called by orchestrators |

---

## Violation 4: Invalid Hierarchical Numbering

**Rule:** Task numbers must be sequential with no gaps.

### ❌ **Wrong:**

```typescript
update_plan({
  plan: [
    { step: "1. /implement - Task 1", status: "completed" },
    { step: "3. /implement - Task 3", status: "in_progress" },  // Skipped 2!
    { step: "  3.1. /implement - Subtask 1", status: "completed" },
    { step: "  3.3. /implement - Subtask 3", status: "pending" }  // Skipped 3.2!
  ]
})
```

**Problem:** Gap in numbering (1 → 3, 3.1 → 3.3).

### ✅ **Correct:**

```typescript
update_plan({
  plan: [
    { step: "1. /implement - Task 1", status: "completed" },
    { step: "2. /implement - Task 2", status: "completed" },
    { step: "3. /implement - Task 3", status: "in_progress" },
    { step: "  3.1. /implement - Subtask 1", status: "completed" },
    { step: "  3.2. /implement - Subtask 2", status: "in_progress" },
    { step: "  3.3. /implement - Subtask 3", status: "pending" }
  ]
})
```

**Fix:** Ensure sequential numbering (1, 2, 3... and 3.1, 3.2, 3.3...).

---

## Violation 5: Multiple In-Progress Tasks

**Rule:** Only one task can be `in_progress` at a time (except parent-child chains).

### ❌ **Wrong:**

```typescript
update_plan({
  plan: [
    { step: "1. /implement - Task A", status: "in_progress" },
    { step: "2. /implement - Task B", status: "in_progress" },  // Violation!
    { step: "3. /implement - Task C", status: "pending" }
  ]
})
```

**Problem:** Two unrelated tasks both `in_progress`.

### ✅ **Correct:**

```typescript
// Option 1: Only one in_progress
update_plan({
  plan: [
    { step: "1. /implement - Task A", status: "completed" },
    { step: "2. /implement - Task B", status: "in_progress" },
    { step: "3. /implement - Task C", status: "pending" }
  ]
})

// Option 2: Parent-child chain (allowed)
update_plan({
  plan: [
    { step: "1. /work - Orchestrate work", status: "in_progress" },
    { step: "  1.1. /implement - Design tests", status: "in_progress" },  // OK!
    { step: "  1.2. /implement - Write code", status: "pending" }
  ]
})
```

**Fix:** Mark previous task `completed` before starting next, OR use parent-child hierarchy.

---

## Quick Reference

### Valid Task Format Pattern

```text
<indent><number>. /<workflow> - <description>

Examples:
- 1. /detect-context - Analyze project state
-   1.1. /load-context - Load initiative files
-     1.1.1. /implement - Read configuration
```

### Workflow Attribution Rules

**Use orchestrators when:**

- Coordinating multiple sub-workflows
- Making routing decisions
- Managing workflow lifecycle

**Use executors when:**

- Writing code, tests, documentation
- Running validation, linting, type checks
- Committing changes, archiving initiatives

**Common Mistakes:**

- ❌ `/work - Fix bug` → ✅ `/implement - Fix bug`
- ❌ `/plan - Write code` → ✅ `/implement - Write code`
- ❌ `/work - Run tests` → ✅ `/validate - Run tests`

---

## Validation Tools

### 1. CLI Validation

```bash
# Validate a single task
python scripts/validate_task_format.py --validate "1. /implement - Add feature"

# Validate session summary file
python scripts/validate_task_format.py --session path/to/summary.md
```

### 2. Pre-commit Hook

Automatically runs on commit for:

- `.windsurf/workflows/*.md`
- `docs/archive/session-summaries/*.md`

**Bypass (not recommended):**

```bash
git commit --no-verify
```

### 3. Unit Tests

```bash
# Run task format validation tests
uv run pytest tests/unit/test_validate_task_format.py -v
```

---

## Historical Context

**Violations Analyzed:** 3 incidents (Oct 18-19, 2025)
**Most Common:** Missing workflow prefixes (60% of violations)
**Root Cause:** Cognitive load during rapid implementation
**Solution:** Automated validation + pre-commit hooks

**References:**

- [Task System Violations Analysis](../archive/session-summaries/2025-10-19-task-system-violations-analysis.md)
- [Task System Fix Session](../archive/session-summaries/2025-10-19-task-system-fix-session.md)
- [Section 1.11: Task System Usage](../../.windsurf/rules/00_agent_directives.md#111-task-system-usage)

---

## Related Documentation

- [Agent Directives - Section 1.11](../../.windsurf/rules/00_agent_directives.md#111-task-system-usage)
- [Task System Integration](../architecture/TASK_SYSTEM_INTEGRATION.md)
- [Validation Script](../../scripts/validate_task_format.py)
- [Pre-commit Hook](../../scripts/hooks/validate_task_format_hook.py)

---

**Maintained By:** mcp-web core team
**Version:** 1.0.0
**Status:** Active
