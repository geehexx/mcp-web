---
created: "2025-10-17"
updated: "2025-10-21"
description: Intelligent work orchestration and context detection
auto_execution_mode: 3
category: Orchestrator
complexity: 85
tokens: 1650
version: v2.0-intelligent-semantic-preservation
dependencies:
  - detect-context
  - load-context
  - implement
  - plan
  - validate
  - commit
  - archive-initiative
  - meta-analysis
status: active
---

# Work Orchestration Workflow

**Purpose:** Central orchestration workflow that detects project context and routes to specialized workflows.

**Invocation:** `/work` (with optional context) or `/work` (autonomous)

**Philosophy:** AI analyzes project state to determine continuation, no explicit direction required.

**Chain:** `/work` → `/detect-context` → [routed workflow] → `/meta-analysis` (at session end)

---

## Stage 0: Workflow Entry

**Print announcement:**

```markdown
🔄 **Entering /work:** Intelligent work orchestration and routing
```

---

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

---

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

---

## Stage 3: Route to Workflow

**See:** [work-routing.md](./work-routing.md) for complete logic

### Routing Matrix

| Confidence | Action | Details |
|------------|--------|---------|
| **High (80%+)** | Auto-proceed | No user confirmation needed |
| **Medium (30-79%)** | Auto-proceed with alternatives | State recommendation, mention alternatives |
| **Low (<30%)** | Prompt user | Ask for direction |

**Routes:** Active initiative → `/implement`, Test failures → `/implement`, Planning → `/plan`, Completed → `/archive-initiative`, Clean slate → Prompt user

**After routing, update plan with subtasks:**

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

---

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

---

## Stage 5: Session End Protocol

**See:** [work-session-protocol.md](./work-session-protocol.md)

**Trigger if ANY:**

1. Initiative marked "Completed" or "✅"
2. All planned tasks done
3. User explicitly signals session end

**Protocol:** Commit changes → Archive initiatives → Meta-analysis → Verify exit criteria → Present summary

**Exit Criteria:** All committed, tests pass, initiatives archived, meta-analysis done, summary created

**ONLY present summary after all criteria met.**

---

## Stage 6: Continue Working

**If protocol NOT triggered:**

- Brief progress update
- Continue next task
- No "completion summary" or "shall I continue?"
- Work until completion or user signals end

---

## Anti-Patterns

| Don't | Do |
|-------|----|
| Ask obvious questions | "Detected initiative X (60%). Continuing..." |
| Skip session end protocol | **CRITICAL:** Always `/meta-analysis` + archive + commit |
| Over-prompt | Auto-route if 80%+ confidence |

---

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Detection + routing | <30s | ✅ |
| Autonomous continuation | 70%+ | ✅ |
| Session end protocol | 100% | ✅ |

---

## Integration

**Calls:** `/detect-context`, `/load-context`, `/plan`, `/implement`, `/validate`, `/commit`, `/archive-initiative`, `/meta-analysis` (mandatory)

**Called By:** User, other workflows

**Exit:**

```markdown
✅ **Completed /work:** Work orchestration finished
```

---

## Sub-Workflows

This workflow is decomposed into focused sub-workflows:

- [work-routing.md](./work-routing.md) - Routing decision logic
- [work-session-protocol.md](./work-session-protocol.md) - Session end protocol

---

## References

- [detect-context.md](./detect-context.md) - Context detection
- [load-context.md](./load-context.md) - Context loading
- [meta-analysis.md](./meta-analysis.md) - Session summary
- [00_core_directives.md](../rules/00_core_directives.md)

---

**Version:** v2.0-intelligent-semantic-preservation
**Last Updated:** 2025-10-21
