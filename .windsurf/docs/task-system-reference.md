---
type: machine-readable-reference
category: quick-reference
purpose: Task system format specification and examples for update_plan tool
token_budget: low
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "2025-10-20"
tags: ["task-system", "update_plan", "format", "transparency"]
---

# Task System Quick Reference

**Purpose:** Quick reference for `update_plan` tool usage and task format specification.

**Authority:** [07_task_system.md](../rules/07_task_system.md)

---

## Required Format

```text
<number>. /<workflow> - <deliverable-description>
```

**Components:**

- `<number>`: Sequential number (1, 2, 3) or hierarchical (1.1, 1.2)
- `.` (period): Required after number
- ` ` (space): Required after period
- `/<workflow>`: Workflow name that EXECUTES this task
- ` - ` (space-dash-space): Required separator
- `<deliverable-description>`: What will be produced (not how)

---

## Hierarchical Numbering

| Level | Format | Indent | Example |
|-------|--------|--------|---------|
| Top-level | `N.` | None | `1. /plan - Create implementation plan` |
| Subtask | `N.N.` | 2 spaces | `1.1. /research - Gather best practices` |
| Sub-subtask | `N.N.N.` | 4 spaces | `1.1.1. /research - Search codebase` |

---

## Workflow Attribution

**CRITICAL:** Attribute tasks to the workflow that **EXECUTES** them, not the caller.

### Orchestrator vs Executor

| Task Type | Workflow Attribution | Example |
|-----------|---------------------|---------|
| Delegation | Executor workflow | `1. /research - Gather findings` (not /plan) |
| Coordination | Orchestrator workflow | `2. /work - Detect work completion` |
| Sub-workflow | Sub-workflow name | `3. /work-routing - Determine route` |

### Common Mappings

| Caller | Delegates To | Task Attribution |
|--------|-------------|------------------|
| `/work` | `/detect-context` | `1. /detect-context - Analyze project state` |
| `/work` | `/implement` | `3. /implement - Execute implementation` |
| `/plan` | `/research` | `2. /research - Gather best practices` |
| `/plan` | `/generate-plan` | `3. /generate-plan - Structure roadmap` |
| `/implement` | `/validate` | `5. /validate - Run quality checks` |
| `/implement` | `/commit` | `6. /commit - Commit changes` |

---

## Status Values

| Status | Meaning | Usage |
|--------|---------|-------|
| `pending` | Not started | Future tasks |
| `in_progress` | Currently executing | **Only ONE task at a time** |
| `completed` | Finished | Never remove from list |

---

## Complete Example

```typescript
update_plan({
  explanation: "🔄 Starting /plan workflow",
  plan: [
    { step: "1. /plan - Define requirements", status: "completed" },
    { step: "2. /plan - Research best practices", status: "in_progress" },
    { step: "  2.1. /research - Search codebase", status: "in_progress" },
    { step: "  2.2. /research - Run web searches", status: "pending" },
    { step: "3. /generate-plan - Structure implementation roadmap", status: "pending" },
    { step: "4. /plan - Review and finalize", status: "pending" }
  ]
})
```

---

## When to Use

**REQUIRED for:**

- Any work requiring 3+ distinct steps
- Work expected to take >5 minutes
- All `/work` or orchestrator workflow invocations
- Any multi-phase implementation

**OPTIONAL for:**

- Single-step operations (<1 minute)
- Direct tool calls with no logic
- User explicitly requests no planning

---

## Update Frequency

**Guidelines:**

- Update every 30-90 seconds during active work
- Each task should complete in 15-90 seconds
- Never leave >2 minutes without update
- Print announcement with each update

---

## Common Patterns

### Pattern 1: Workflow Entry

```typescript
update_plan({
  explanation: "🔄 Initiating /work orchestration",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "in_progress" },
    { step: "2. /work-routing - Determine workflow route", status: "pending" },
    { step: "3. /<routed-workflow> - Execute primary tasks", status: "pending" }
  ]
})
```

### Pattern 2: Sub-Workflow Delegation

```typescript
// Before calling /research
update_plan({
  explanation: "↪️ Delegating to /research",
  plan: [
    { step: "1. /plan - Define requirements", status: "completed" },
    { step: "2. /plan - Research best practices", status: "in_progress" },
    { step: "  2.1. /research - Gather findings", status: "in_progress" },
    { step: "3. /generate-plan - Structure roadmap", status: "pending" }
  ]
})
```

### Pattern 3: Task Completion

```typescript
// After completing task
update_plan({
  explanation: "✅ Research complete. Moving to planning.",
  plan: [
    { step: "1. /plan - Define requirements", status: "completed" },
    { step: "2. /plan - Research best practices", status: "completed" },
    { step: "  2.1. /research - Gather findings", status: "completed" },
    { step: "3. /generate-plan - Structure roadmap", status: "in_progress" }
  ]
})
```

---

## Anti-Patterns

### ❌ Wrong Workflow Attribution

```typescript
// ❌ Wrong: Attributed to caller, not executor
{ step: "1. /plan - Research best practices", status: "in_progress" }

// ✅ Correct: Attributed to executor
{ step: "1. /research - Gather best practices", status: "in_progress" }
```

### ❌ Process Description Instead of Deliverable

```typescript
// ❌ Wrong: Describes process
{ step: "1. /plan - Read files and write document", status: "in_progress" }

// ✅ Correct: Describes deliverable
{ step: "1. /plan - Create implementation plan", status: "in_progress" }
```

### ❌ Multiple Tasks In Progress

```typescript
// ❌ Wrong: Two tasks in_progress
{ step: "1. /research - Gather findings", status: "in_progress" }
{ step: "2. /plan - Create roadmap", status: "in_progress" }

// ✅ Correct: Only one in_progress
{ step: "1. /research - Gather findings", status: "completed" }
{ step: "2. /plan - Create roadmap", status: "in_progress" }
```

### ❌ Removing Completed Tasks

```typescript
// ❌ Wrong: Removed completed tasks
update_plan({
  plan: [
    { step: "2. /plan - Research complete", status: "in_progress" }
  ]
})

// ✅ Correct: Preserve all tasks
update_plan({
  plan: [
    { step: "1. /plan - Define requirements", status: "completed" },
    { step: "2. /plan - Research best practices", status: "in_progress" }
  ]
})
```

---

## Validation

**Pre-commit hook:** `scripts/hooks/validate_task_format_hook.py`

**Checks:**

- Format: `N. /workflow - description`
- Period after number
- Workflow prefix with `/`
- Separator ` - ` present
- No missing components

**Note:** Some orchestrator coordination tasks may be flagged but are legitimate.

---

## References

- [07_task_system.md](../rules/07_task_system.md) - Complete task system documentation
- [00_agent_directives.md](../rules/00_agent_directives.md) - Section 11 (Task System Usage)
- [workflow-guide.md](../../docs/guides/WORKFLOW_GUIDE.md) - Workflow transparency guide

---

**Maintained by:** mcp-web core team
**Version:** 1.0.0
