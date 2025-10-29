---
description: Intelligent work orchestration and context detection
title: Work Orchestration Workflow
type: workflow
category: Orchestrator
complexity: complex
dependencies: ['detect-context', 'load-context', 'implement', 'plan', 'validate', 'commit', 'archive-initiative', 'meta-analysis']
status: active
created: 2025-10-22
updated: 2025-10-22
---

# Work Orchestration Workflow

**Purpose:** Central orchestration detecting project context and routing to specialized workflows.

**Invocation:** `/work` (with optional context) or autonomous

**Philosophy:** AI analyzes project state to determine continuation autonomously.

**Chain:** `/work` → `/detect-context` → [routed workflow] → `/meta-analysis` (session end)

## Critical Workflow Requirements

**🚨 CRITICAL:** Even with specific user instructions (e.g., "@/work Continue Phase 1..."), you MUST follow ALL workflow stages:

1. Create initial task plan (Stage 1)
2. Detect context (Stage 2) - even if user specified, analyze and confirm
3. Route to workflow (Stage 3) - show routing decision
4. Update plan with workflow-specific subtasks (MANDATORY)
5. Execute workflow (Stage 4)
6. Check for completion (Stage 5) - after EVERY major task
7. Session end protocol if triggered (Stage 5)

**Anti-pattern:** "User said do X → skip directly to implementation" ❌
**Correct:** "User said do X → detect context, confirm route to X, show implementation plan, execute" ✅

## Stage 0: Workflow Entry

**Print announcement:**

```markdown
🔄 **Entering /work:** Intelligent work orchestration and routing
```

## Stage 1: Create Initial Task Plan

**MANDATORY:** Create task list before actions. Number tasks by executing workflow.

```typescript
update_plan({
  explanation: "🔄 Initiating /work orchestration",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "in_progress" },
    { step: "2. /work-routing - Determine workflow route", status: "pending" },
    { step: "3. /<routed-workflow> - Execute primary tasks", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /work-session-protocol - Execute session end protocol", status: "pending" }
  ]
})
```

## Stage 2: Detect Project Context

**Call** `/detect-context`:

- Analyzes state (initiatives, git, tests, sessions)
- Classifies signals by confidence
- Returns routing recommendation

```typescript
update_plan({
  explanation: "✅ Context detection complete. Routing decision ready.",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work-routing - Determine workflow route", status: "in_progress" },
    { step: "3. /<routed-workflow> - Execute primary tasks", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /work-session-protocol - Execute session end protocol", status: "pending" }
  ]
})
```

## Stage 3: Route to Workflow

**See:** [work-routing.md](./work-routing.md) for complete logic

### Routing Matrix

| Confidence | Action | Details |
|------------|--------|---------|
| **High (80%+)** | Auto-proceed | No confirmation |
| **Medium (30-79%)** | Auto-proceed with alternatives | State recommendation + alternatives |
| **Low (<30%)** | Prompt user | Ask for direction |

**Routes:** Active initiative → `/implement`, Test failures → `/implement`, Planning → `/plan`, Completed → `/archive-initiative`, Clean slate → Prompt

**🚨 MANDATORY: After routing, update plan with workflow-specific subtasks.**

**This is NOT optional. You MUST show the implementation/research/planning workflow stages.**

```typescript
update_plan({
  explanation: "🔀 Routing to /implement workflow. Adding subtasks.",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work-routing - Determine workflow route", status: "completed" },
    { step: "3. /implement - Execute implementation workflow", status: "in_progress" },
    { step: "  3.1. /load-context - Load initiative files", status: "in_progress" },
    { step: "  3.2. /implement - Design test cases", status: "pending" },
    { step: "  3.3. /implement - Write failing tests", status: "pending" },
    { step: "  3.4. /implement - Implement feature code", status: "pending" },
    { step: "  3.5. /validate - Run tests and validate", status: "pending" },
    { step: "  3.6. /commit - Commit changes", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /work-session-protocol - Execute session end protocol", status: "pending" }
  ]
})
```

## Stage 4: Execute Workflow

**Load Context** (`/load-context`):

- Initiative: initiative + related files
- Planning: full project context
- Module: specific module files

**Chain examples:**

```yaml
# Implementation
/work → /detect-context → /implement → /validate → /commit

# Planning
/work → /detect-context → /plan → /implement → /validate → /commit

# Quick fix
/work → /detect-context → /implement → /commit
```

**🚨 CRITICAL: After completing each major workflow stage (test, implementation, commit), check for completion:**

```typescript
// After completing substeps 3.1-3.6, update plan:
update_plan({
  explanation: "✅ Implementation complete. Checking for session completion...",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work-routing - Determine workflow route", status: "completed" },
    { step: "3. /implement - Execute implementation workflow", status: "completed" },
    { step: "4. /work - Detect work completion", status: "in_progress" },
    { step: "5. /work-session-protocol - Execute if triggered", status: "pending" }
  ]
})
```

**Check completion triggers:**

- All planned tasks done? → Session end protocol
- Initiative marked completed? → Session end protocol
- More work remaining? → Continue to next task

## Stage 5: Session End Protocol

**See:** [work-session-protocol.md](./work-session-protocol.md)

**🚨 MANDATORY CHECK: After completing ANY major workflow (implement, plan, research), you MUST check if session should end.**

**Trigger if ANY:**

1. Initiative marked "Completed" or "✅" in initiative file
2. All planned tasks in current session are done
3. User signals session end ("wrap up", "end session", "done for now")
4. You completed the user's requested work ("Continue Phase 1..." → Phase 1 work done)

**When triggered:**

```typescript
update_plan({
  explanation: "🏁 Session completion detected. Executing session end protocol...",
  plan: [
    { step: "5.1. /commit - Commit all changes", status: "in_progress" },
    { step: "5.2. /archive-initiative - Archive completed initiatives", status: "pending" },
    { step: "5.3. /meta-analysis - Execute summary workflow", status: "pending" },
    { step: "5.4. /work-session-protocol - Present session summary", status: "pending" }
  ]
})
```

**Protocol:** Commit → Archive (if initiative completed) → Meta-analysis (MANDATORY) → Verify exit → Present summary

**Exit Criteria:** All committed, tests pass, initiatives archived (if applicable), meta-analysis done, summary created

**ONLY present summary after all criteria met.**

**If NOT triggered:** Brief update ("✅ X done, 🔄 continuing with Y") and continue next task WITHOUT asking "shall I continue?"

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Security Practices**: `/rules/06_security_practices.mdc` - Apply when dealing with security-sensitive code including API calls, user input, LLM interactions, and authentication
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files, complex operations, or memory-intensive tasks
- **Task Orchestration**: `/rules/12_task_orchestration.mdc` - Apply when managing complex task coordination and workflow orchestration
- **Workflow Routing**: `/rules/13_workflow_routing.mdc` - Apply when determining workflow routing and context analysis

## Workflow References

When this work orchestration workflow is called:

1. **Load**: `/commands/work.md`
2. **Execute**: Follow the orchestration stages defined above
3. **Route**: Determine appropriate workflow based on context
4. **Chain**: Execute routed workflow and session end protocol

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Ask obvious questions | Detected initiative X (60%). Continuing... |
| Skip session end protocol | Always `/meta-analysis` + archive + commit |
| Over-prompt | Auto-route if 80%+ confidence |
| Skip context detection | Always analyze project state first |
| Skip task planning | Always create task plan before actions |

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Detection + routing | <30s | ✅ |
| Autonomous continuation | 70%+ | ✅ |
| Session end protocol | 100% | ✅ |

## Integration

**Calls:** `/detect-context`, `/load-context`, `/plan`, `/implement`, `/validate`, `/commit`, `/archive-initiative`, `/meta-analysis` (mandatory)

**Called By:** User, other workflows

**Exit:**

```markdown
✅ **Completed /work:** Work orchestration finished
```

## Command Metadata

**File:** `work.yaml`
**Type:** Command/Workflow
**Complexity:** Complex
**Estimated Tokens:** ~1,650
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Work orchestration
- Context detection
- Workflow routing
- Session management

**Dependencies:**

- /detect-context - Context analysis
- /load-context - Context loading
- /implement - Implementation workflow
- /plan - Planning workflow
- /validate - Validation workflow
- /commit - Commit workflow
- /archive-initiative - Initiative archiving
- /meta-analysis - Session analysis
