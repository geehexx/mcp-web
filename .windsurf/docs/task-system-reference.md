---
type: machine-readable-reference
category: quick-reference
purpose: Task format specification and examples for update_plan tool
token_budget: low
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "2025-10-20"
tags: ["task-system", "update_plan", "format", "transparency"]
---

# Task System Quick Reference

**Purpose:** Format specification for `update_plan` tool usage.

**Authority:** [07_task_system.md](../rules/07_task_system.md)

---

## Required Format

```text
<number>. /<workflow> - <deliverable-description>
```

**Components:**

- `<number>`: Sequential (1, 2, 3) or hierarchical (1.1, 1.2)
- `.` (period): Required after number
- ` ` (space): Required after period
- `/<workflow>`: Workflow that EXECUTES this task
- ` - ` (space-dash-space): Required separator
- `<deliverable-description>`: What will be delivered

---

## Status Values

| Status | Meaning | Usage |
|--------|---------|-------|
| `pending` | Not started | Default for future tasks |
| `in_progress` | Currently executing | Max ONE task at a time |
| `completed` | Finished | Never remove from list |

---

## Workflow Attribution

**CRITICAL:** Attribute tasks to the workflow that EXECUTES them, not the caller.

| Caller | Executes | Attribution |
|--------|----------|-------------|
| `/work` | `/detect-context` | `1. /detect-context - ...` |
| `/work` | `/implement` | `3. /implement - ...` |
| `/implement` | `/validate` | `3.5. /validate - ...` |
| `/plan` | `/research` | `2.1. /research - ...` |

---

## Hierarchical Numbering

**Top-level:** Major workflow phases

```text
1. /detect-context - Analyze project state
2. /work-routing - Determine route
3. /implement - Execute implementation
```

**Subtasks:** Use 2-space indent + decimal notation

```text
3. /implement - Execute implementation
  3.1. /load-context - Load initiative files
  3.2. /implement - Design test cases
  3.3. /implement - Write failing tests
```

---

## Common Patterns

### Work Orchestration

```typescript
update_plan({
  explanation: "🔄 Initiating /work orchestration",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "in_progress" },
    { step: "2. /work-routing - Determine workflow route", status: "pending" },
    { step: "3. /<routed-workflow> - Execute primary tasks", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /meta-analysis - Execute session summary", status: "pending" }
  ]
})
```

### Implementation with Subtasks

```typescript
update_plan({
  explanation: "🔀 Routing to /implement. Adding subtasks.",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work-routing - Determine workflow route", status: "completed" },
    { step: "3. /implement - Execute implementation", status: "in_progress" },
    { step: "  3.1. /load-context - Load initiative files", status: "in_progress" },
    { step: "  3.2. /implement - Design test cases", status: "pending" },
    { step: "  3.3. /implement - Write failing tests", status: "pending" },
    { step: "  3.4. /implement - Implement feature code", status: "pending" },
    { step: "  3.5. /validate - Run tests", status: "pending" },
    { step: "  3.6. /commit - Commit changes", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /meta-analysis - Execute session summary", status: "pending" }
  ]
})
```

### Planning Phase

```typescript
update_plan({
  explanation: "📋 Starting /plan workflow",
  plan: [
    { step: "1. /plan - Create comprehensive plan", status: "in_progress" },
    { step: "  1.1. /research - Research best practices", status: "in_progress" },
    { step: "  1.2. /plan - Analyze requirements", status: "pending" },
    { step: "  1.3. /plan - Design solution", status: "pending" },
    { step: "2. /implement - Execute plan", status: "pending" },
    { step: "3. /validate - Verify implementation", status: "pending" }
  ]
})
```

---

## Critical Rules

### ✅ DO

- Attribute to workflow that executes the task
- Keep completed tasks in the list (never remove)
- Use hierarchical numbering for subtasks
- Have at most ONE `in_progress` task
- Print workflow entry/exit announcements
- Update plan when routing changes

### ❌ DON'T

- Attribute to caller workflow
- Remove completed tasks
- Have multiple `in_progress` tasks
- Skip task updates
- Use inconsistent numbering
- Forget to mark tasks complete

---

## Workflow Entry/Exit

**Always print announcements:**

```markdown
🔄 **Entering /workflow-name:** Brief description
```

```markdown
✅ **Completed /workflow-name:** Brief summary
```

---

## Task Attribution Mapping

| Workflow | Typical Tasks |
|----------|---------------|
| `/work` | Orchestration, routing, completion detection |
| `/detect-context` | Signal analysis, context detection |
| `/work-routing` | Routing decisions |
| `/plan` | Planning, analysis, design |
| `/research` | Research, investigation |
| `/implement` | Implementation, coding, testing |
| `/load-context` | Context loading |
| `/validate` | Testing, validation, quality checks |
| `/commit` | Git operations |
| `/archive-initiative` | Initiative archival |
| `/meta-analysis` | Session summary |

---

## Anti-Patterns

### ❌ Wrong Attribution

```typescript
// Bad: Attributed to caller
{ step: "1. /work - Load context files", status: "in_progress" }

// Good: Attributed to executor
{ step: "1. /load-context - Load context files", status: "in_progress" }
```

### ❌ Removing Completed Tasks

```typescript
// Bad: Removed completed tasks
plan: [
  { step: "3. /implement - Current task", status: "in_progress" }
]

// Good: Keep full history
plan: [
  { step: "1. /detect-context - Analyze state", status: "completed" },
  { step: "2. /work-routing - Route decision", status: "completed" },
  { step: "3. /implement - Current task", status: "in_progress" }
]
```

### ❌ Multiple In-Progress

```typescript
// Bad: Multiple in_progress
plan: [
  { step: "1. /implement - Task A", status: "in_progress" },
  { step: "2. /validate - Task B", status: "in_progress" }  // Wrong!
]

// Good: One in_progress
plan: [
  { step: "1. /implement - Task A", status: "completed" },
  { step: "2. /validate - Task B", status: "in_progress" }
]
```

---

## Quick Checklist

Before calling `update_plan`:

- [ ] Tasks attributed to executor workflow
- [ ] Completed tasks preserved
- [ ] At most ONE `in_progress`
- [ ] Hierarchical numbering correct
- [ ] Explanation provided
- [ ] Workflow announcements printed

---

## References

- [07_task_system.md](../rules/07_task_system.md) - Complete specification
- [work.md](../workflows/work.md) - Work orchestration examples
- [implement.md](../workflows/implement.md) - Implementation examples

---

**Version:** 2.0.0 (Streamlined for conciseness)
**Maintained by:** mcp-web core team
