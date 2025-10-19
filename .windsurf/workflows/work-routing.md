---
created: "2025-10-18"
updated: "2025-10-18"
description: /work-routing - Routing decision logic for work orchestration
auto_execution_mode: 3
category: Sub-workflow
parent: work.md
complexity: 70
tokens: 1221
dependencies:
  - detect-context
status: active
---

# Work Routing Logic

**Purpose:** Determine which workflow to route to based on context detection confidence and signals.

**Called By:** `/work` (Stage 3)

**Returns:** Routing decision with target workflow

---

## Stage 0: Workflow Entry

🔄 **Entering /work-routing:** Routing decision logic

**Print workflow entry announcement:**

```markdown
🔄 **Entering /work-routing:** Determining optimal workflow route based on context
```

---

## Confidence-Based Routing

### High Confidence (80%+)

**AUTO-PROCEED - no user confirmation needed.**

| Detected Context | Route To | Action |
|------------------|----------|--------|
| Active initiative with unchecked tasks | `/implement` | Load initiative context, continue work |
| Test failures (blocking) | Fix immediately | Highest priority |
| Test failures (non-blocking) | `/implement` | Load test context, fix |
| Planning markers | `/plan` | Create plan |
| Completed initiative pending archive | `/archive-initiative` | Archive |
| Clean state, no signals | Prompt user | Ask for direction |

**Output Format:**

```markdown
## ✓ Context Detected (High Confidence: 85%)

**Detected:** [Brief description]

**Auto-routing to:** [workflow name]

**Rationale:** [1-2 sentences]

Proceeding...
```

### Medium Confidence (30-79%)

**AUTO-PROCEED with recommended - state alternatives but execute.**

**Output Format:**

```markdown
## ✓ Context Detected (Medium Confidence: 65%)

**Detected:** [N] possible work streams

**Proceeding with recommended:** [Option 1]
- [Brief rationale]

**Alternative considered:** [Option 2] - [why not chosen]

Auto-routing to [workflow]...
```

**Rationale:** AI has recommendation, user can redirect if wrong (faster than asking).

### Low Confidence (<30%)

**ONLY NOW prompt user.**

**Output Format:**

```markdown
## Project State Analysis (Low Confidence: 35%)

**Detected signals:** [List what found]

**Unable to determine clear next step.**

What would you like to work on?

1. **[Option 1]** - [brief description]
2. **[Option 2]** - [brief description]
3. **[Option 3]** - [brief description]
4. **Something else**
```

**When to Prompt:**

- Multiple initiatives equally active
- Conflicting signals (e.g., both new work and urgent fixes)
- Truly clean slate with no history

---

## Routing Decision Matrix

### Initiative-Based Routing

```yaml
IF: Active initiative with unchecked tasks
AND: No blocking issues
AND: No higher-priority work
THEN: Route to /implement with initiative context
CONFIDENCE: High (85-95%)
```

### Test-Based Routing

```yaml
IF: Test failures detected
AND: Failures introduced in last commit OR
     Failures mentioned in session summary
THEN: Route to /implement with test context
PRIORITY: HIGH (fix before continuing)
CONFIDENCE: High (90%+)
```

### Planning-Based Routing

```yaml
IF: "Plan", "Design", "Architecture" keywords in summary OR
    ADR placeholder detected OR
    Multiple incomplete features
THEN: Route to /plan
CONFIDENCE: Medium-High (65-80%)
```

### Archive-Based Routing

```yaml
IF: Initiative marked "Completed" or "✅"
AND: Still in active/ directory
THEN: Route to /archive-initiative
CONFIDENCE: High (100%)
```

### Clean Slate Routing

```yaml
IF: No active initiatives
AND: No unstaged changes
AND: No test failures
AND: No session summary "Next Steps"
THEN: Prompt user for direction
CONFIDENCE: Low (<30%)
```

---

## Priority Rules

**Priority Order (highest to lowest):**

1. **Blocking Test Failures** → Fix immediately
2. **Completed Initiatives** → Archive before new work
3. **Active Initiative Continuation** → Resume in-progress work
4. **Non-Blocking Test Failures** → Fix when convenient
5. **Planning Work** → Create plans for new features
6. **Clean Slate** → Prompt user

**Override Conditions:**

- User explicit direction overrides all priorities
- Security issues override everything
- Broken build overrides everything except security

---

## Context-Specific Loading

After routing decision, call `/load-context` with appropriate scope:

| Route | Context Scope | Files to Load |
|-------|---------------|---------------|
| `/implement` (initiative) | `initiative` | Initiative file + related source + tests |
| `/implement` (tests) | `module:tests` | Test files + module under test |
| `/plan` | `full` | PROJECT_SUMMARY + all active initiatives + ADRs |
| `/archive-initiative` | `initiative` | Initiative file only |

---

## Task Plan Update

**After routing decision, update plan with routed workflow steps:**

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

**Numbering Rule:** Child workflow tasks use parent step number (3.1, 3.2, etc.)

---

## Anti-Patterns

### ❌ Don't: Ask Obvious Questions

- **Bad:** "What would you like to work on?"
- **Good:** "Detected initiative X (60% complete). Continuing..."

### ❌ Don't: Over-Prompt

If 80%+ confident, auto-route. User can redirect if wrong.

### ❌ Don't: Ignore Priority Rules

**Bad:** Route to planning when tests are failing
**Good:** Fix tests first, then route to planning

---

## Success Metrics

**Good Routing:**

- Context detection + routing: <30s
- Autonomous routing: 70%+ of time
- Correct initial routing: 90%+ accuracy

**Needs Improvement:**

- Asking "what to work on" when context clear (should be <10%)
- Routing to wrong workflow (should be <5%)
- Missing priority violations (should be 0%)

---

## References

- Parent workflow: [work.md](./work.md)
- Context detection: [detect-context.md](./detect-context.md)
- Context loading: [load-context.md](./load-context.md)

---

**Version:** 1.0.0 (Extracted from work.md Phase 4 decomposition)
**Last Updated:** 2025-10-18
