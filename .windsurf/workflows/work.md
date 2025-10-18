---
description: Intelligent work orchestration and context detection
auto_execution_mode: 3
category: Orchestrator
---

# Work Orchestration Workflow

**Purpose:** Central orchestration workflow that intelligently detects project context and routes to specialized workflows.

**Invocation:** `/work` (with optional context) or `/work` (autonomous detection)

**Philosophy:** AI should understand where to pick up from by analyzing project state, not requiring explicit direction.

**Workflow Chain:** `/work` → `/detect-context` → [routed workflow] → `/meta-analysis` (at session end)

---

## Stage 1: Create Initial Task Plan

**MANDATORY:** Create task list before any actions.

**Numbering:** Attribute tasks to workflow that EXECUTES them.

```typescript
update_plan({
  explanation: "🔄 Initiating /work orchestration",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "in_progress" },
    { step: "2. /work - Route to appropriate workflow", status: "pending" },
    { step: "3. /work - Execute routed workflow", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /work - Session end protocol (if triggered)", status: "pending" }
  ]
})
```

---

## Stage 2: Detect Project Context

Call `/detect-context` workflow:

- Analyzes project state (initiatives, git, tests, sessions)
- Classifies signals by confidence level
- Identifies continuation points

**Returns:** Detection results with routing recommendation

```typescript
update_plan({
  explanation: "✅ Context detection complete. Routing decision ready.",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work - Route to appropriate workflow", status: "in_progress" },
    { step: "3. /work - Execute routed workflow", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /work - Session end protocol (if triggered)", status: "pending" }
  ]
})
```

---

## Stage 3: Route to Appropriate Workflow

**See:** [work-routing.md](./work-routing.md) for complete routing logic

### Quick Reference

| Confidence | Action | Details |
|------------|--------|---------|
| **High (80%+)** | Auto-proceed | No user confirmation needed |
| **Medium (30-79%)** | Auto-proceed with alternatives | State recommendation, mention alternatives |
| **Low (<30%)** | Prompt user | Ask for direction |

**Common Routes:**

- Active initiative → `/implement`
- Test failures → Fix immediately or `/implement`
- Planning markers → `/plan`
- Completed initiative → `/archive-initiative`
- Clean slate → Prompt user

**After routing, update plan with routed workflow steps:**

```typescript
update_plan({
  explanation: "🔀 Routing to /implement workflow. Adding subtasks.",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work - Route to appropriate workflow", status: "completed" },
    { step: "3. /work - Execute routed workflow", status: "in_progress" },
    { step: "  3.1. /implement - Load context files", status: "in_progress" },
    { step: "  3.2. /implement - Design test cases", status: "pending" },
    { step: "  3.3. /implement - Write failing tests", status: "pending" },
    { step: "  3.4. /implement - Implement feature code", status: "pending" },
    { step: "  3.5. /implement - Run tests and validate", status: "pending" },
    { step: "  3.6. /implement - Commit changes", status: "pending" },
    { step: "4. /work - Detect work completion", status: "pending" },
    { step: "5. /work - Session end protocol (if triggered)", status: "pending" }
  ]
})
```

---

## Stage 4: Execute Workflow

### Load Context

Call `/load-context` with scope:
- Initiative: initiative + related files
- Planning: full project context
- Module: specific module files

### Execute Routed Workflow

**Workflow chain examples:**

```yaml
# Implementation
/work → /detect-context → /implement → /validate → /commit

# Planning
/work → /detect-context → /plan → /implement → /validate → /commit

# Quick fix
/work → /detect-context → /implement → /commit
```

---

## Stage 5: Detect Work Completion and Execute Session End Protocol

**See:** [work-session-protocol.md](./work-session-protocol.md) for complete protocol

### Quick Reference

**Trigger Session End Protocol if ANY of:**

1. Initiative marked "Completed" or "✅"
2. All planned tasks done
3. User explicitly signals session end

**Protocol Steps:**

1. Commit all changes (working + auto-fixes)
2. Archive completed initiatives (`/archive-initiative`)
3. Execute meta-analysis (`/meta-analysis`)
4. Verify exit criteria (all committed, tests pass, docs updated)
5. Present completion summary

**Exit Criteria:**

```markdown
- [ ] All changes committed (git status clean)
- [ ] All tests passing (if code changes made)
- [ ] Completed initiatives archived
- [ ] Meta-analysis executed
- [ ] Session summary created
```

**ONLY present final summary after all criteria met.**

---

## Stage 6: Continue Working (If Protocol Not Triggered)

**If Session End Protocol NOT triggered:**

- Provide brief progress update
- Continue with next task/phase
- Do NOT present "completion summary"
- Do NOT ask "shall I continue?" unless blocked
- Keep working until actual completion or user signals end

---

## Anti-Patterns

### ❌ Don't: Ask Obvious Questions

- **Bad:** "What would you like to work on?"
- **Good:** "Detected initiative X (60% complete). Continuing..."

### ❌ Don't: Skip Session End Protocol

**CRITICAL FAILURE:**
- Presenting summary without `/meta-analysis`
- Leaving completed initiatives in active/
- Uncommitted changes at session end

### ❌ Don't: Over-Prompt

If 80%+ confident, auto-route. User can redirect if wrong.

---

## Success Metrics

✅ **Good:**
- Context detection + routing: <30s
- Autonomous continuation: 70%+
- Session end protocol: 100%

❌ **Needs Improvement:**
- Asking "what to work on" when context clear
- Skipping session end protocol
- Requiring direction for obvious continuations

---

## Integration

### Calls

- `/detect-context` - Context analysis
- `/load-context` - Efficient loading
- `/plan` - Planning
- `/implement` - Implementation (includes testing)
- `/validate` - Quality checks
- `/commit` - Git operations
- `/archive-initiative` - Archive completed
- `/meta-analysis` - **MANDATORY** session summary

### Called By

- User (direct)
- Other workflows (when orchestration needed)

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
- [00_agent_directives.md](../rules/00_agent_directives.md) - Section 1.8

---

**Version:** 2.0.0 (Decomposed for modularity - Phase 4)
**Last Updated:** 2025-10-18
