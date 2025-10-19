---
created: "2025-10-19"
updated: "2025-10-19"
trigger: model_decision
description: Apply when using update_plan tool, creating task lists, orchestrating workflows, or managing multi-step work. Essential for /work, /plan, /implement orchestration.
category: operations
tokens: 2800
applyTo:
  - planning
  - orchestration
  - workflow_execution
  - task_tracking
priority: high
status: active
---

# Rule: Task System Usage

**Purpose:** Defines task system usage for transparent progress tracking via Windsurf's Planning Mode (Todo Lists).

**TOOL:** `update_plan` - Creates/updates in-conversation task list

**WHEN REQUIRED:**

- Any work requiring 3+ distinct steps
- Work expected to take >5 minutes
- All `/work` or orchestrator workflow invocations
- Any multi-phase implementation

**MAY SKIP WHEN:**

- Single-step request (e.g., "format this file")
- Quick question/answer in Chat mode
- User explicitly requests no planning overhead

---

## 1. Task Creation

**At workflow start, create initial plan with MANDATORY numbering format:**

**REQUIRED FORMAT:** `<number>. /<workflow> - <description>`

**Examples:**

- Top-level: `1. /detect-context - Analyze project state`
- Subtask: `3.1. /implement - Load context files` (2-space indent)
- Sub-subtask: `3.1.1. /implement - Read initiative file` (4-space indent)

### 1.1 Deliverable-Focused Principle

Tasks should describe WHAT will be delivered, not HOW it will be done:

- ✅ **Good:** `3.2. /implement - Update Section 1.11 (Task System)` (deliverable: updated section)
- ❌ **Bad:** `3.2. /implement - Read file and edit and save` (describes process, not outcome)
- ✅ **Good:** `2. /plan - Create architecture decision record` (deliverable: ADR document)
- ❌ **Bad:** `2. /plan - Open editor and type ADR` (describes keystrokes)

**Focus on outcomes** (files modified, features working, tests passing) **not actions** (reading, writing, calling).

### 1.2 Definition of Done for Tasks

Each task MUST have clear completion criteria:

| Task Type | Definition of Done |
|-----------|--------------------|
| Documentation update | File modified, linted, committed |
| Feature implementation | Code written, tests passing, committed |
| Bug fix | Root cause identified, fix applied, regression test added, committed |
| Research | Summary documented with sources, recommendations made |
| Validation | All checks passed (lint, test, security), issues resolved |
| Workflow creation | File created, examples included, cross-references updated |

### 1.3 Verify Before Planning Checkpoint

Before creating task plan for complex work (>5 tasks or >1 hour), verify:

1. **Context loaded?** Have you read all necessary files?
2. **Requirements clear?** Do you know what success looks like?
3. **Approach decided?** Have you chosen implementation strategy?
4. **Blockers identified?** Are there dependencies or unknowns?

If NO to any → pause, gather information, THEN create plan.

### 1.4 Transparency Requirements

- Print workflow entry announcement: `🔄 **Entering Stage X: [Name]**`
- Print task creation confirmation: `✓ Task plan created with N items`
- Print task updates: `📋 **Task Update:** "X. /workflow - Task" → status`
- Print major milestones: `ℹ️ **[Event]:** [Details]`
- Print workflow exit: `✅ **Completed [Workflow]:** [Summary]`

---

## 2. Task Attribution Rule (CRITICAL)

Tasks MUST be attributed to the workflow that EXECUTES them, not the workflow that CALLS them.

- ❌ **WRONG:** `{ step: "1. /work - Detect project context", status: "in_progress" }` (=/work/ doesn't detect, /detect-context does!)
- ✅ **CORRECT:** `{ step: "1. /detect-context - Analyze project state", status: "in_progress" }` (attributes to executor)

### 2.1 Orchestrator vs Executor

- **Orchestrator tasks:** Coordination work (routing, protocol execution, state management) → use orchestrator prefix
- **Executor tasks:** Actual work delegated to specialized workflows → use executor's prefix

```typescript
// Top-level workflow (called directly)
update_plan({
  explanation: "🔄 Starting /work orchestration",  // Announce what we're doing
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "in_progress" },  // Executor!
    { step: "2. /work-routing - Route to appropriate workflow", status: "pending" },  // Sub-workflow executor
    { step: "3. /implement - Execute implementation workflow", status: "pending" },  // Executor
    { step: "4. /work - Detect work completion", status: "pending" },  // Orchestrator
    { step: "5. /work-session-protocol - Session end protocol", status: "pending" }  // Sub-workflow executor
  ]
})
// After call, print: "✓ Task plan created with 5 items"
// Note: Steps 1, 2, 3, 5 use executor workflow names. Only step 4 uses /work.
```

### 2.2 Common Workflow Attribution Mapping

| Stage | ❌ WRONG Prefix | ✅ CORRECT Prefix | Reason |
|-------|----------------|------------------|--------|
| Context detection | `/work` | `/detect-context` | detect-context.md executes this |
| Research | `/work` | `/research` | research.md executes this |
| Routing decision | `/work` | `/work-routing` | work-routing.md sub-workflow |
| Implementation | `/work` | `/implement` | implement.md executes this |
| Load context | `/implement` | `/load-context` | load-context.md executes this |
| Planning | `/work` | `/plan` | plan.md executes this |
| Generate plan | `/plan` | `/generate-plan` | generate-plan.md executes this |
| Validation | `/implement` | `/validate` | validate.md executes this |
| Commit | `/implement` | `/commit` | commit.md executes this |
| Session end protocol | `/work` | `/work-session-protocol` | work-session-protocol.md sub-workflow |
| Archive initiative | `/work` or `/work-session-protocol` | `/archive-initiative` | archive-initiative.md executes this |
| Meta-analysis | `/work` or `/work-session-protocol` | `/meta-analysis` | meta-analysis.md executes this |
| Extract session | `/meta-analysis` | `/extract-session` | extract-session.md executes this |
| Summarize session | `/meta-analysis` | `/summarize-session` | summarize-session.md executes this |

**Key Principle:** Always use the name of the .md file that contains the workflow logic, NOT the name of the workflow that calls it.

### 2.3 Child Workflow Task Insertion

**When child workflow called (e.g., /implement as step 3):**

```typescript
// Parent already has tasks 1, 2, 3, 4, 5
// Child inserts as subtasks of parent's current task (3)
update_plan({
  explanation: "🔀 Routing to /implement workflow. Adding subtasks.",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work - Route to appropriate workflow", status: "completed" },
    { step: "3. /work - Execute routed workflow", status: "in_progress" },
    { step: "  3.1. /implement - Load context files", status: "in_progress" },  // Child executes this
    { step: "  3.2. /implement - Write failing tests", status: "pending" },
    { step: "  3.3. /implement - Implement feature code", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },  // Orchestrator task
    { step: "5. /work - Session end protocol (if triggered)", status: "pending" }  // Orchestrator task
  ]
})
// After call, print: "📋 **Task Update:** Added 3 /implement subtasks (3.1-3.3)"
```

---

## 3. Critical Task Format Rules

**MANDATORY for every task:**

1. **Numbering:** EVERY task MUST have `<number>. /<workflow> - <description>` format
2. **Workflow prefix:** ALWAYS include workflow name (e.g., `/work`, `/implement`, `/detect-context`)
3. **Executor attribution:** Attribute tasks to the workflow that EXECUTES them, not the caller
4. **Period after number:** Required for readability (WBS standard)
5. **Hierarchical numbering:** Parent 3 → children 3.1, 3.2; Parent 3.2 → children 3.2.1, 3.2.2
6. **Indentation:** 2 spaces per hierarchy level (0, 2, 4, 6 spaces)
7. **One active task:** At most ONE step can be `in_progress` at a time
8. **Specific tasks:** Each step must have clear completion criteria
9. **Reasonable scope:** Tasks should be 15-60 min each (decompose if larger)
10. **Sequential order:** List tasks in execution order
11. **Print announcements:** ALWAYS print workflow entry and task updates to user

---

## 4. Task Updates

**MUST update when:**

1. **Task completed:** Mark `completed`, advance next to `in_progress`
2. **New tasks discovered:** Insert before dependent tasks
3. **Workflow routing:** Add routed workflow tasks as subtasks
4. **Blocked state:** Add unblocking task
5. **User requests change:** Adjust plan accordingly

### 4.1 Never Remove Completed Tasks

**When updating plan:**

- ✅ **ALWAYS include all previous tasks** with their current status
- ✅ **Preserve hierarchical structure** (keep parent and children together)
- ✅ **Only change status** of tasks that have progressed
- ✅ **ALWAYS include workflow prefix** in every task (no exceptions)
- ❌ **NEVER create fresh plan** that drops completed tasks
- ❌ **NEVER omit workflow name** from any task
- ❌ **NEVER replace entire plan** with subset of tasks

**Anti-pattern (WRONG):**

```typescript
// This LOSES tasks 4.1-4.6 and omits workflow names!
update_plan({
  explanation: "Fixing validation issues",
  plan: [
    { step: "4. Execute Phase 5", status: "in_progress" },       // Missing /work
    { step: "  4.7. Fix validation issues", status: "in_progress" }, // Missing /implement
    { step: "  4.8. Commit changes", status: "pending" }          // Missing /implement
  ]
})
```

**Correct pattern:**

```typescript
update_plan({
  explanation: "Research complete, moving to implementation",
  plan: [
    { step: "1. /research - Gather requirements", status: "completed" },
    { step: "2. /implement - Design solution", status: "in_progress" },  // Advanced
    { step: "3. /implement - Run tests", status: "pending" },
    { step: "4. /commit - Commit changes", status: "pending" }
  ]
})
```

**Adding new tasks (CORRECT):**

```typescript
// Previous plan had tasks 1-4, now discovering new work
update_plan({
  explanation: "Validation failed, adding fix task",
  plan: [
    { step: "1. /research - Gather requirements", status: "completed" },
    { step: "2. /implement - Design solution", status: "completed" },
    { step: "3. /implement - Run tests", status: "completed" },
    { step: "  3.1. /implement - Fix test failures", status: "in_progress" },  // NEW
    { step: "4. /commit - Commit changes", status: "pending" }
  ]
})
// Note: ALL previous tasks preserved, new task inserted with workflow prefix
```

---

## 5. Task Hierarchy and Numbering

**Hierarchical numbering follows WBS (Work Breakdown Structure) standard:**

**Numbering Scheme:**

- **Level 0 (Top-level):** `1, 2, 3, 4, 5` - No indent
- **Level 1 (Subtasks):** `3.1, 3.2, 3.3` - 2-space indent (child of task 3)
- **Level 2 (Sub-subtasks):** `3.1.1, 3.1.2` - 4-space indent (child of task 3.1)
- **Level 3 (Rare):** `3.1.2.1` - 6-space indent (child of 3.1.2)

**Parent-Child Numbering Logic:**

When child workflow called at parent task N:

1. Child tasks numbered: `N.1, N.2, N.3, ...`
2. Inserted after parent task N
3. Use 2-space indent per level
4. After child completes, parent continues from N+1

**Complete Example:**

```typescript
plan: [
  { step: "1. /detect-context - Analyze project state", status: "completed" },
  { step: "2. /work - Route to appropriate workflow", status: "completed" },
  { step: "3. /work - Execute routed workflow", status: "in_progress" },
  { step: "  3.1. /implement - Load context files", status: "completed" },     // Level 1
  { step: "    3.1.1. /implement - Read initiative file", status: "completed" }, // Level 2 (rare)
  { step: "    3.1.2. /implement - Read source files", status: "completed" },
  { step: "  3.2. /implement - Design test cases", status: "in_progress" },
  { step: "  3.3. /implement - Write tests", status: "pending" },
  { step: "  3.4. /implement - Implement feature", status: "pending" },
  { step: "4. /work - Session end protocol", status: "pending" }  // Parent continues
]
```

**MUST include in every task:**

1. **Number with period:** `3.` not `3` or `(3)`
2. **Workflow prefix:** `/implement` shows which workflow executes
3. **Dash separator:** ` - ` between workflow and description
4. **Deliverable description:** What will be done, not how

**Quick Reference:**

| Format Element | Example | Required? |
|----------------|---------|----------|
| Hierarchical number | `3.2.1` | ✅ Yes |
| Period after number | `.` | ✅ Yes |
| Workflow prefix | `/implement` | ✅ Yes |
| Dash separator | ` - ` | ✅ Yes |
| Deliverable description | `Update Section 1.11` | ✅ Yes |
| Indent (subtasks) | 2 spaces per level | ✅ Yes |

---

## 6. Session End Protocol Integration

**Session End Protocol MUST be tracked as tasks:**

```typescript
update_plan({
  explanation: "Work complete. Executing session end protocol.",
  plan: [
    // ... completed work tasks ...
    { step: "N. /work-session-protocol - Execute session end protocol", status: "in_progress" },
    { step: "  N.1. /commit - Commit all changes", status: "in_progress" },
    { step: "  N.2. /archive-initiative - Archive completed initiatives", status: "pending" },
    { step: "  N.3. /meta-analysis - Run meta-analysis", status: "pending" },
    { step: "  N.4. /work-session-protocol - Update living docs", status: "pending" },
    { step: "  N.5. /work-session-protocol - Verify exit criteria", status: "pending" }
  ]
})
```

**Update as each protocol step completes.**

---

## 7. Progress Transparency Requirements

**MANDATORY:** All workflows MUST provide visible progress through:

1. **Progress Announcements** - Print workflow entry/exit/stage messages
2. **Task Updates** - Update task status after each significant step
3. **Sub-Workflow Visibility** - Show sub-workflow calls in task list

**Progress Announcement Standards:**

Print at these transition points:

- Workflow entry: `🔄 **Entering /workflow:** Purpose`
- Stage complete: `📋 **Stage N Complete:** What finished`
- Sub-workflow call: `↪️ **Delegating to /sub-workflow:** Reason`
- Workflow exit: `✅ **Completed /workflow:** Summary`
- Long operations: Every 2-3 minutes

**Emoji Standards:**

- 🔄 = Workflow entry
- 📋 = Stage complete / progress update
- ✅ = Workflow complete (success)
- ⚠️ = Warning / non-critical issue
- ❌ = Error / failure
- ↪️ = Delegation to sub-workflow
- ℹ️ = Informational message

**Task Update Frequency:**

- **Minimum:** After each stage completion
- **Recommended:** Every 30-90 seconds for long workflows
- **Maximum gap:** 3 minutes without update (print progress message)

**Sub-Workflow Task Pattern:**

When workflow calls sub-workflow:

1. Update plan BEFORE calling (add sub-workflow task as N.1)
2. Print delegation message: `↪️ **Delegating to /sub-workflow**`
3. Execute sub-workflow
4. Update plan AFTER returning (mark N.1 completed)
5. Print completion message

**Example:**

```typescript
// Before calling /research
update_plan({
  explanation: "↪️ Delegating to /research for best practices",
  plan: [
    { step: "2. /plan - Create implementation plan", status: "in_progress" },
    { step: "  2.1. /research - Gather requirements", status: "in_progress" }
  ]
})
console.log("↪️ **Delegating to /research:** Gathering best practices")

// Call /research
call_workflow("/research", ...)

// After /research returns
console.log("📋 **Research Complete:** 5 sources analyzed")
update_plan({
  explanation: "Research complete, proceeding to plan generation",
  plan: [
    { step: "2. /plan - Create implementation plan", status: "in_progress" },
    { step: "  2.1. /research - Gather requirements", status: "completed" },
    { step: "  2.2. /generate-plan - Structure plan", status: "in_progress" }
  ]
})
```

**Rationale:**

Users trust agents that show their work. Visibility enables:

- **User confidence:** See progress happening
- **Early intervention:** Spot wrong direction before completion
- **Better debugging:** Identify where workflows stall
- **Learning:** Understand workflow execution patterns

---

## 8. Anti-Patterns

**❌ DON'T:**

- Create vague tasks ("Do Phase 2", "Fix everything")
- Skip initial plan for non-trivial work
- Forget to update status after completing tasks
- Have multiple `in_progress` tasks simultaneously
- Use task system for trivial single-step requests

**✅ DO:**

- Create specific, measurable tasks
- Update immediately after each major step
- Keep one task active at a time
- Decompose large tasks into subtasks
- Track session end protocol as tasks

---

## 9. Enforcement

**Per user directive (2025-10-18):**

> "Failure to enforce or maintain the task system is a protocol violation."

**This is NON-NEGOTIABLE.** Task system usage is mandatory for workflow transparency.

**Validation checkpoints:**

- All orchestrator workflows (`/work`, `/plan`, `/implement`) create initial plan
- Task list visible in conversation after each major step
- Session end protocol tracked as tasks 100% of time
- Routed workflows add their own subtasks

---

## 10. Automated Validation

**Available tools (2025-10-19):**

**1. Validation Script:**

```bash
python scripts/validate_task_format.py --validate "task text"
```

**2. Pre-commit Hook:**

- Automatically validates task format in workflow documentation
- Targets: `.windsurf/workflows/*.md`, session summaries
- Bypass: `git commit --no-verify` (not recommended)

**3. Test Suite:**

```bash
uv run pytest tests/unit/test_validate_task_format.py -v
```

**Violation types detected:**

- Missing workflow prefixes (`/<workflow>` format)
- Removed completed tasks (history loss)
- Wrong workflow attribution (orchestrator vs executor)
- Invalid hierarchical numbering
- Multiple in-progress tasks

---

## References

- Core directives: [00_agent_directives.md](./00_agent_directives.md)
- Operational protocols: [05_operational_protocols.md](./05_operational_protocols.md)
- Work orchestration: [work.md](../workflows/work.md)
- Task format validation: [validate_task_format.py](../../scripts/validate_task_format.py)

---

**Version:** 1.0.0 (Extracted from 00_agent_directives.md for size optimization)
**Last Updated:** 2025-10-19
