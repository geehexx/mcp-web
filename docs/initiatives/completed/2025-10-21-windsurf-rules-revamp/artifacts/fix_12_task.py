#!/usr/bin/env python3
"""Trim 12_task_orchestration.md to <12KB."""

from datetime import date
from pathlib import Path

OUTPUT_DIR = Path("/tmp/windsurf-rules-new")

content = (
    """---
trigger: model_decision
description: Apply when using update_plan creating task lists or orchestrating multi-step workflows
---

# Task Orchestration and update_plan Usage

**Purpose:** Defines task system usage for transparent progress tracking via Windsurf Planning Mode (Todo Lists).

**Tool:** `update_plan` - Creates/updates task list visible in Windsurf Planning Mode

---

## When Required

**MANDATORY for:**
- Any work requiring 3+ distinct steps
- Work expected to take >5 minutes
- All `/work` or orchestrator workflow invocations
- Any multi-phase implementation

**NOT required for:**
- Single-step operations
- Quick fixes (<5 min)
- Direct tool calls
- Simple queries

---

## Format Specification

**Required format:** `<number>. /<workflow> - <description>`

**Examples:**
- `1. /detect-context - Analyze project state`
- `2. /work-routing - Determine workflow route`
- `3. /implement - Execute implementation workflow`

**Hierarchical tasks** (2-space indent):
- `3.1. /load-context - Load initiative files`
- `3.2. /implement - Design test cases`

---

## Core Rules

### Rule 1: Workflow Attribution (CRITICAL)

**Attribute tasks to the workflow that EXECUTES them, not the caller.**

✅ **Correct:**
```typescript
{step: "1. /load-context - Load initiative files", status: "in_progress"}
```

❌ **Wrong:**
```typescript
{step: "1. /implement - Load context files", status: "in_progress"}
```

**Mapping:**
- Context loading → `/load-context`
- Implementation → `/implement`
- Validation → `/validate`
- Git operations → `/commit`
- Archival → `/archive-initiative`

### Rule 2: Never Remove Completed Tasks

**Always preserve full task history.**

❌ **Wrong:** Removing completed tasks
```typescript
plan: [
  {step: "3. /implement - Current task", status: "in_progress"}
]
```

✅ **Correct:** Keep all tasks
```typescript
plan: [
  {step: "1. /detect-context - Analyze state", status: "completed"},
  {step: "2. /work-routing - Route decision", status: "completed"},
  {step: "3. /implement - Current task", status: "in_progress"}
]
```

### Rule 3: One Active Task

**At most ONE task can have `status: "in_progress"` at any time.**

### Rule 4: Print Announcements

**Always print workflow entry/exit:**

```markdown
🔄 **Entering /implement:** Implementation workflow
...
✅ **Completed /implement:** Implementation finished
```

---

## Quick Examples

### Example 1: Simple Linear Tasks

```typescript
update_plan({
  explanation: "Starting implementation",
  plan: [
    {step: "1. /load-context - Load files", status: "completed"},
    {step: "2. /implement - Write tests", status: "in_progress"},
    {step: "3. /validate - Run tests", status: "pending"}
  ]
})
```

### Example 2: Hierarchical Tasks

```typescript
update_plan({
  explanation: "Implementation phase with subtasks",
  plan: [
    {step: "1. /plan - Planning complete", status: "completed"},
    {step: "2. /implement - Execute implementation", status: "in_progress"},
    {step: "  2.1. /implement - Design tests", status: "completed"},
    {step: "  2.2. /implement - Write failing tests", status: "in_progress"},
    {step: "  2.3. /implement - Implement feature", status: "pending"},
    {step: "3. /validate - Validation", status: "pending"}
  ]
})
```

---

## Anti-Patterns

### ❌ Wrong Attribution

```typescript
// BAD: Caller workflow, not executor
{step: "1. /work - Load context files", status: "in_progress"}

// GOOD: Executor workflow
{step: "1. /load-context - Load context files", status: "in_progress"}
```

### ❌ Multiple In-Progress

```typescript
// BAD: Two tasks in_progress
plan: [
  {step: "1. /implement - Task A", status: "in_progress"},
  {step: "2. /validate - Task B", status: "in_progress"}
]
```

### ❌ Removing History

```typescript
// BAD: Lost previous work
plan: [
  {step: "5. /commit - Commit", status: "in_progress"}
]

// GOOD: Full history
plan: [
  {step: "1. /detect-context", status: "completed"},
  {step: "2. /work-routing", status: "completed"},
  {step: "3. /implement", status: "completed"},
  {step: "4. /validate", status: "completed"},
  {step: "5. /commit - Commit", status: "in_progress"}
]
```

---

## Enforcement

**Per user directive (2025-10-18):** Failure to maintain task system is a protocol violation.

**This is NON-NEGOTIABLE.**

---

## References

- [work.md](../workflows/work.md) - Orchestration examples
- [implement.md](../workflows/implement.md) - Implementation examples
- Task system reference documentation (detailed format spec)

---

## Rule Metadata

**File:** `12_task_orchestration.md`
**Trigger:** model_decision
**Estimated Tokens:** ~3,000
**Last Updated:** """
    + date.today().isoformat()
    + """
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**
- update_plan tool usage
- Task format specification
- Workflow attribution rules
- Hierarchical task structure
- Progress transparency

**Workflow References:**
- /work - Task orchestration
- /plan - Planning tasks
- /implement - Implementation tasks
- All workflows using update_plan

**Dependencies:**
- Source: 07_task_system.md (heavily trimmed from 29KB to 3KB)

**Changelog:**
- """
    + date.today().isoformat()
    + """: Created from 07_task_system.md (core only, trimmed 90%)
- Focused on essential rules and format
- Detailed examples moved to reference documentation
"""
)

(OUTPUT_DIR / "12_task_orchestration.md").write_text(content)
print(f"✅ Fixed 12_task_orchestration.md ({len(content)} bytes)")
