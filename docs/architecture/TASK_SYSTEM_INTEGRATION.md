# Task System Integration: Design Document

**Status:** Implementation in Progress
**Date:** 2025-10-18
**Author:** Cascade (via user directive)

---

## Executive Summary

This document defines how Cascade (Windsurf's AI agent) must use the task system (`update_plan` tool) to mirror its real workflow and provide transparent progress tracking. This is **not optional** — task system usage is a protocol requirement.

---

## 1. What is the Task System?

### 1.1 Technical Foundation

**Tool:** `update_plan`
**Purpose:** Planning Mode / Todo Lists for longer tasks
**Architecture:** Specialized planning agent refines long-term plan while execution model focuses on short-term actions
**UI:** Todo list widget within Cascade conversation

**Tool Signature:**

```typescript
update_plan({
  explanation: string,        // Why this update is happening
  plan: Array<{
    step: string,             // Specific, measurable task
    status: "pending" | "in_progress" | "completed"
  }>
})
```

**Returns:**

```json
{
  "content": "Task description",
  "id": "system-generated-uuid",
  "priority": "medium",
  "status": "pending" | "in_progress" | "completed"
}
```

**Constraints:**

- At most **one** step can be `in_progress` at a time
- Tasks persist for the conversation's lifetime
- Plan updates automatically integrate new information (Memories, workflow outputs, etc.)

### 1.2 Authoritative Sources

- **Windsurf Docs:** [Planning Mode](https://docs.windsurf.com/windsurf/cascade/planning-mode)
- **Tool Definition:** Available in Cascade system prompt as `update_plan`
- **Use Case:** Designed for "longer tasks" requiring multi-step planning

---

## 2. Why This Matters

### 2.1 User Benefits

1. **Visual Progress:** Real-time task list updates in conversation UI
2. **Context Persistence:** Understand what's done, what's next, what's blocked
3. **Workflow Transparency:** See agent decision-making as task transitions
4. **Resumability:** Clear continuation point if session interrupted

### 2.2 Agent Benefits

1. **Self-Discipline:** Forces explicit task decomposition before execution
2. **Memory Aid:** Persistent checklist prevents forgotten steps
3. **Error Recovery:** Clear state to revert to if approach fails
4. **Quality Gate:** Each task completion is a checkpoint for validation

### 2.3 Protocol Compliance

Per user directive (2025-10-18):
> "Failure to enforce or maintain the task system is a protocol violation."

This is **non-negotiable**. Task system usage is as mandatory as code testing or security checks.

---

## 3. Operational Requirements

### 3.1 When to Create Initial Plan

**MUST create plan when:**

1. `/work` or any orchestrator workflow invoked
2. User request requires 3+ distinct steps
3. Work duration expected >5 minutes
4. Multiple phases with dependencies

**MAY skip plan when:**

- Single-step request (e.g., "format this file")
- Quick question/answer (Chat mode)
- User explicitly requests no planning overhead

**Initial plan example:**

```typescript
update_plan({
  explanation: "Initializing implementation plan for API key authentication",
  plan: [
    { step: "Research best practices for API key storage", status: "in_progress" },
    { step: "Design key rotation strategy", status: "pending" },
    { step: "Implement CLI key management commands", status: "pending" },
    { step: "Add integration tests", status: "pending" },
    { step: "Update documentation", status: "pending" }
  ]
})
```

### 3.2 When to Update Plan

**MUST update when:**

1. Marking task complete (move to `completed`, advance next to `in_progress`)
2. Discovering new required tasks (insert before dependent tasks)
3. Workflow routing decision made (add routed workflow tasks)
4. Blocked/blocked state encountered (add unblocking task)
5. User requests plan change

**MAY update when:**

- Refining task description for clarity
- Breaking large task into subtasks
- Reordering tasks based on new information

**Update example:**

```typescript
update_plan({
  explanation: "Research complete. Moving to design phase.",
  plan: [
    { step: "Research best practices for API key storage", status: "completed" },
    { step: "Design key rotation strategy", status: "in_progress" },
    { step: "Implement CLI key management commands", status: "pending" },
    { step: "Add integration tests", status: "pending" },
    { step: "Update documentation", status: "pending" }
  ]
})
```

### 3.3 Task Granularity Guidelines

**Good task:**

- ✅ "Update PROJECT_SUMMARY.md with new initiative status"
- ✅ "Replace mcp2_git_status with standard git status command"
- ✅ "Run /meta-analysis workflow"

**Bad task:**

- ❌ "Fix everything" (not measurable)
- ❌ "Write code" (not specific)
- ❌ "Phase 1" (vague boundary)

**Granularity rules:**

1. **Completion check:** Can you unambiguously tell when this task is done?
2. **Single responsibility:** Does this task do one thing well?
3. **Reasonable scope:** Can this be completed in one focused work session (15-60 min)?
4. **Dependency clarity:** Is it clear what must happen before/after this task?

### 3.4 Hierarchical Task Decomposition

**When parent task branches, insert subtasks in-place:**

```typescript
// Initial plan
plan: [
  { step: "Implement feature X", status: "in_progress" },
  { step: "Write tests", status: "pending" }
]

// After discovering complexity, decompose:
plan: [
  { step: "Implement feature X", status: "in_progress" },
  { step: "  1.1 Design data model", status: "in_progress" },    // Indent indicates subtask
  { step: "  1.2 Implement validation logic", status: "pending" },
  { step: "  1.3 Add error handling", status: "pending" },
  { step: "Write tests", status: "pending" }
]
```

**Numbering convention:**

- Top-level: `1, 2, 3`
- Subtasks: `1.1, 1.2, 1.3` (2-space indent)
- Sub-subtasks: `1.1.1, 1.1.2` (4-space indent, rare)

---

## 4. Workflow Integration Points

### 4.1 Orchestrator Workflows

**`/work` workflow:**

```markdown
Stage 1: Detect Context
→ update_plan: Create initial plan with detected context
  Tasks: [Context detection, Routing decision, Execute routed workflow, Session end protocol]

Stage 2: Route
→ update_plan: Insert routed workflow tasks into plan
  Example: If routing to /implement, add [Design, Code, Test, Validate, Commit]

Stage 3: Execute
→ update_plan: Mark tasks completed as workflows finish
  Each workflow completion = task status update

Stage 4: Session End Protocol
→ update_plan: Mark protocol steps as they execute
  Tasks: [Commit changes, Archive initiatives, Run meta-analysis, Update docs]
```

**`/plan` workflow:**

```markdown
Stage 1: Research
→ update_plan: Create research plan
  Tasks: [Web search, Read sources, Analyze patterns, Document findings]

Stage 2: Generate Plan
→ update_plan: Create implementation plan
  Tasks: [Define phases, List tasks per phase, Estimate durations, Identify risks]

Stage 3: Output
→ update_plan: Mark planning complete
  Status: Planning complete, ready for /implement
```

**`/implement` workflow:**

```markdown
Stage 1: Load Context
→ update_plan: Create implementation plan
  Tasks: [Load files, Design approach, Write code, Run tests, Commit]

Stage 2: Test-First
→ update_plan: Mark test design complete, move to implementation
  Tasks: Design tests [completed], Write tests, Implement feature, Verify tests pass

Stage 3: Validate
→ update_plan: Run validation tasks
  Tasks: [Lint, Type check, Security scan, Test suite, Git commit]
```

### 4.2 Specialized Workflows

**All specialized workflows MUST:**

1. Accept parent plan context (which task they're executing)
2. Create subtasks if work is non-trivial (>2 steps)
3. Mark parent task complete upon successful exit

**Example (`/validate`):**

```typescript
// Parent task from /implement: "Run validation checks"

update_plan({
  explanation: "Running validation workflow subtasks",
  plan: [
    // ... previous tasks ...
    { step: "Run validation checks", status: "in_progress" },
    { step: "  1. Run ruff linter", status: "in_progress" },      // Subtask
    { step: "  2. Run mypy type checker", status: "pending" },
    { step: "  3. Run security scanners", status: "pending" },
    { step: "  4. Run test suite", status: "pending" },
    { step: "Commit changes", status: "pending" }
  ]
})
```

### 4.3 Session End Protocol Integration

**CRITICAL:** Session End Protocol (Rule 1.8) MUST be tracked as tasks:

```typescript
update_plan({
  explanation: "Initiating session end protocol",
  plan: [
    // ... completed work tasks ...
    { step: "Session End Protocol", status: "in_progress" },
    { step: "  1. Commit all changes (including auto-fixes)", status: "in_progress" },
    { step: "  2. Archive completed initiatives", status: "pending" },
    { step: "  3. Run /meta-analysis workflow", status: "pending" },
    { step: "  4. Update living documentation (if triggers met)", status: "pending" },
    { step: "  5. Verify exit criteria checklist", status: "pending" }
  ]
})
```

**This ensures:**

- Protocol steps are visible to user
- Each step completion is explicit
- Forgotten steps are immediately obvious
- Session summary includes protocol status

---

## 5. Implementation Checklist

### 5.1 Rule Updates Required

**File:** `.windsurf/rules/00_agent_directives.md`

**Section 1.2 (North Stars):** Add "Task Transparency" principle
**Section 1.7 (Session End Protocol):** Add task system requirements
**New Section 1.11:** Task System Usage

### 5.2 Workflow Updates Required

**Orchestrator workflows:**

- [ ] `/work`: Add task creation at Stage 1, updates at each stage transition
- [ ] `/plan`: Add task tracking for research and planning phases
- [ ] `/implement`: Add test-first task decomposition
- [ ] `/meta-analysis`: Add protocol task tracking

**Specialized workflows:**

- [ ] `/validate`: Add validation subtasks
- [ ] `/commit`: Add git operation tasks
- [ ] `/detect-context`: Add context scanning tasks
- [ ] `/load-context`: Add batch loading tasks

### 5.3 Success Criteria

**After implementation, verify:**

1. Every `/work` invocation creates initial task plan
2. Task list updates visible in conversation after each major step
3. Session end protocol tracked as tasks 100% of time
4. Routed workflows add their own subtasks
5. Task completion unambiguous (clear done state)

---

## 6. Anti-Patterns (What NOT to Do)

### ❌ Don't: Create Vague Tasks

**Bad:**

```typescript
{ step: "Do Phase 2", status: "pending" }
```

**Good:**

```typescript
{ step: "Implement user authentication", status: "pending" },
{ step: "Add password hashing", status: "pending" },
{ step: "Create session management", status: "pending" }
```

### ❌ Don't: Forget to Update Status

**Bad:** Complete work without marking task complete

**Good:** After finishing subtask, update immediately:

```typescript
update_plan({
  explanation: "Linting complete, moving to type checking",
  plan: [
    { step: "Run ruff linter", status: "completed" },
    { step: "Run mypy type checker", status: "in_progress" }
  ]
})
```

### ❌ Don't: Skip Initial Plan

**Bad:** Start work without creating plan

**Good:** Always call `update_plan` before first tool invocation:

```typescript
update_plan({
  explanation: "Creating implementation plan",
  plan: [
    { step: "Research approach", status: "in_progress" },
    { step: "Implement changes", status: "pending" },
    { step: "Run tests", status: "pending" },
    { step: "Commit", status: "pending" }
  ]
})
```

### ❌ Don't: Have Multiple In-Progress Tasks

**Bad:**

```typescript
plan: [
  { step: "Task A", status: "in_progress" },
  { step: "Task B", status: "in_progress" }  // ❌ Violates constraint
]
```

**Good:**

```typescript
plan: [
  { step: "Task A", status: "completed" },
  { step: "Task B", status: "in_progress" }  // ✅ Only one active
]
```

---

## 7. Examples

### Example 1: Simple Bug Fix

```typescript
// Initial plan
update_plan({
  explanation: "Planning bug fix for rate limiting issue",
  plan: [
    { step: "Reproduce bug in test", status: "in_progress" },
    { step: "Identify root cause", status: "pending" },
    { step: "Implement fix", status: "pending" },
    { step: "Verify fix with test", status: "pending" },
    { step: "Commit changes", status: "pending" }
  ]
})

// After reproducing bug
update_plan({
  explanation: "Bug reproduced. Investigating root cause.",
  plan: [
    { step: "Reproduce bug in test", status: "completed" },
    { step: "Identify root cause", status: "in_progress" },
    { step: "Implement fix", status: "pending" },
    { step: "Verify fix with test", status: "pending" },
    { step: "Commit changes", status: "pending" }
  ]
})

// ... continue until all complete
```

### Example 2: Complex Feature with Workflow Routing

```typescript
// /work invocation - initial plan
update_plan({
  explanation: "Detected active initiative, routing to /implement",
  plan: [
    { step: "Detect context", status: "completed" },
    { step: "Route to /implement workflow", status: "completed" },
    { step: "Execute implementation workflow", status: "in_progress" },
    { step: "Session end protocol", status: "pending" }
  ]
})

// /implement adds subtasks
update_plan({
  explanation: "Decomposing implementation into subtasks",
  plan: [
    { step: "Detect context", status: "completed" },
    { step: "Route to /implement workflow", status: "completed" },
    { step: "Execute implementation workflow", status: "in_progress" },
    { step: "  Load context files", status: "in_progress" },
    { step: "  Design test cases", status: "pending" },
    { step: "  Write tests", status: "pending" },
    { step: "  Implement feature code", status: "pending" },
    { step: "  Run validation checks", status: "pending" },
    { step: "  Commit changes", status: "pending" },
    { step: "Session end protocol", status: "pending" }
  ]
})

// Continue updating as subtasks complete...
```

### Example 3: Session End Protocol

```typescript
// Work complete, entering protocol
update_plan({
  explanation: "All implementation complete. Starting session end protocol.",
  plan: [
    // ... completed work tasks ...
    { step: "Session end protocol", status: "in_progress" },
    { step: "  Commit working changes", status: "in_progress" },
    { step: "  Commit auto-fixes separately", status: "pending" },
    { step: "  Archive completed initiative", status: "pending" },
    { step: "  Run /meta-analysis", status: "pending" },
    { step: "  Update PROJECT_SUMMARY (if needed)", status: "pending" },
    { step: "  Update CHANGELOG (if needed)", status: "pending" }
  ]
})

// After committing
update_plan({
  explanation: "Changes committed. Archiving initiative.",
  plan: [
    // ... completed work tasks ...
    { step: "Session end protocol", status: "in_progress" },
    { step: "  Commit working changes", status: "completed" },
    { step: "  Commit auto-fixes separately", status: "completed" },
    { step: "  Archive completed initiative", status: "in_progress" },
    { step: "  Run /meta-analysis", status: "pending" },
    { step: "  Update PROJECT_SUMMARY (if needed)", status: "pending" },
    { step: "  Update CHANGELOG (if needed)", status: "pending" }
  ]
})

// Continue until all protocol steps complete
```

---

## 8. Integration Timeline

### Phase 1: Rules Update (Immediate)

- Update `.windsurf/rules/00_agent_directives.md`
- Add task system mandate
- Document task granularity guidelines

### Phase 2: Workflow Updates (Next Session)

- Update `/work`, `/plan`, `/implement`, `/meta-analysis`
- Add task checkpoints to all workflows
- Test with real workflow executions

### Phase 3: Validation (Ongoing)

- Self-audit: Check task system usage in each session
- User feedback: Verify task transparency improves UX
- Iterate on task decomposition patterns

---

## 9. References

**Official Documentation:**

- [Windsurf Planning Mode](https://docs.windsurf.com/windsurf/cascade/planning-mode)
- [Cascade Overview](https://docs.windsurf.com/windsurf/cascade/cascade)

**Internal Documentation:**

- `.windsurf/rules/00_agent_directives.md` - Section 1.8 (Session End Protocol)
- `.windsurf/workflows/work.md` - Master orchestrator
- `.windsurf/workflows/implement.md` - Test-first implementation

**Tool Reference:**

- Cascade system prompt - `update_plan` tool definition

---

**Document Status:** ✅ Complete - Ready for implementation

**Next Steps:**

1. Update rules (`.windsurf/rules/00_agent_directives.md`)
2. Update workflows (`.windsurf/workflows/*.md`)
3. Execute current session using task system (demonstration)
