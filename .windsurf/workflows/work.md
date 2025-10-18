---
description: Intelligent work orchestration and context detection
auto_execution_mode: 3
category: Orchestrator
---

# Work Orchestration Workflow

**Purpose:** Central orchestration workflow that intelligently detects project context and routes to appropriate specialized workflows.

**Category:** Orchestrator (master workflow coordination)

**Invocation:** `/work` (with optional context) or `/work` (autonomous detection)

**Philosophy:** AI agent should understand where to pick up from by analyzing project state, not by requiring explicit direction.

**Workflow Chain:** `/work` → `/detect-context` → [routed workflow] → `/meta-analysis` (at session end)

---

## Stage 1: Create Initial Task Plan

🔄 **Entering Stage 1: Create Initial Task Plan**

**MANDATORY:** Create task list before any other actions.

**Numbering Format:** Attribute tasks to the workflow that EXECUTES them, not the caller.

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

✓ Task plan created with 5 items

**Note:** Step 1 uses `/detect-context` prefix because that workflow executes the analysis. Steps 2-5 use `/work` prefix because the orchestrator performs these coordination tasks itself.

---

## Stage 2: Detect Project Context

**Call `/detect-context` workflow:**

- Analyzes project state (initiatives, git, tests, sessions)
- Classifies signals by confidence level
- Identifies continuation points
- See: `.windsurf/workflows/detect-context.md`

**Returns:** Detection results with routing recommendation

📋 **Task Update:** "1. /detect-context - Analyze project state" → completed

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

### High Confidence (Auto-Proceed)

**If `/detect-context` returns 80%+ confidence:**

**AUTO-PROCEED with detected action - no user confirmation needed.**

| Detected Context | Route To | Action |
|------------------|----------|--------|
| Active initiative with unchecked tasks | `/implement` | Load initiative context, continue work |
| Test failures (blocking) | Fix immediately | Highest priority - unblock test suite |
| Test failures (non-blocking) | `/implement` | Load test context, fix failures |
| Planning markers ("needs design", ADR placeholders) | `/plan` | Create comprehensive plan |
| Completed initiative pending archive | `/archive-initiative` | Archive completed work |
| Clean state, no signals | Prompt user | Ask for direction |

**Output format:**

```markdown
## ✓ Context Detected (High Confidence: 85%)

**Detected:** [Brief description of what was found]

**Auto-routing to:** [workflow name]

**Rationale:** [1-2 sentence explanation]

Proceeding...
```

### Medium Confidence (Auto-Proceed with Recommended)

**If `/detect-context` returns 30-79% confidence:**

**AUTO-PROCEED with recommended option - briefly state alternatives but execute recommendation.**

**Output format:**

```markdown
## ✓ Context Detected (Medium Confidence: 65%)

**Detected:** [N] possible work streams

**Proceeding with recommended:** [Option 1 name]
- [Brief rationale for recommendation]

**Alternative considered:** [Option 2 name] - [why not chosen]

Auto-routing to [workflow]...
```

**Rationale for auto-proceeding:**

- AI has identified a clear recommendation
- User can redirect if wrong (faster than asking permission)
- Follows principle: "Execute and adjust" beats "Ask and wait"
- If user disagrees, they can interrupt and redirect

### Low Confidence (Prompt User)

**If `/detect-context` returns <30% confidence:**

**ONLY NOW prompt user for direction.**

**Output format:**

```markdown
## Project State Analysis (Low Confidence: 35%)

**Detected signals:** [List what was found]

**Unable to determine clear next step** - multiple equally valid options.

What would you like to work on?

1. **[Option 1]** - [brief description]
2. **[Option 2]** - [brief description]
3. **[Option 3]** - [brief description]
4. **Something else** (please specify)
```

**When to prompt:**

- Multiple initiatives equally active
- Conflicting signals (e.g., both new work and urgent fixes)
- Truly clean slate with no history

---

**After routing decision, update task plan with routed workflow steps:**

🔀 **Routing Decision:** Continuing with /implement workflow

```typescript
// Example: Routing to /implement
update_plan({
  explanation: "🔀 Routing to /implement workflow. Adding implementation subtasks.",
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "completed" },
    { step: "2. /work - Route to appropriate workflow", status: "completed" },
    { step: "3. /work - Execute routed workflow", status: "in_progress" },
    { step: "  3.1. /implement - Load context files", status: "in_progress" },      // Child workflow uses parent number
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

📋 **Task Update:** Added 6 /implement subtasks (3.1-3.6)

---

## Stage 4: Execute Workflow

### Load Context Before Execution

**Call `/load-context` with appropriate scope:**

- Initiative scope: Load initiative + related files
- Planning scope: Load full project context
- Module scope: Load specific module files
- See: `.windsurf/workflows/load-context.md`

### Execute Routed Workflow

**As routed workflow progresses, update subtask status:**

**Workflow chain examples:**

```yaml
# Implementation workflow
/work → /detect-context → /implement → /validate → /commit

# Planning workflow
/work → /detect-context → /plan → /implement → /validate → /commit

# Quick fix workflow
/work → /detect-context → /implement → /commit
```

---

## Stage 5: Detect Work Completion and Execute Session End Protocol

**Check if Session End Protocol should be triggered:**

### 5.1 Detect Completion Triggers

```bash
# Check if any initiative was marked complete during this work
grep -l "Status.*Completed\|Status.*✅" docs/initiatives/active/*.md

# Check git status for uncommitted changes
git status --short
```

**Trigger Session End Protocol if ANY of:**

1. Initiative marked "Completed" or "✅" (found in grep above)
2. All planned tasks for routed workflow are done
3. User explicitly signals session end

**If triggered, execute FULL protocol:**

### 5.2 Commit All Changes

```bash
# Commit working changes
git add <modified files>
git commit -m "<appropriate conventional commit message>"

# Commit any auto-fixes separately
git add <auto-fix files>
git commit -m "style(scope): apply [tool] auto-fixes"
```

### 5.3 Archive Completed Initiatives

```bash
# For each completed initiative found
/archive-initiative <initiative-name>
```

**MUST call workflow - do not skip!**

### 5.4 Execute Meta-Analysis

```bash
/meta-analysis
```

**This creates:**

- Session summary in `docs/archive/session-summaries/`
- Workflow improvement recommendations
- Cross-session continuity documentation

### 5.5 Exit Criteria Checklist

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

**If Session End Protocol was NOT triggered:**

- Provide brief progress update
- Continue with next task/phase
- Do NOT present "completion summary"
- Do NOT ask "shall I continue?" unless blocked
- Keep working until actual completion or user signals end

---

## Anti-Patterns

### ❌ Don't: Ask Obvious Questions

```markdown
BAD: "What would you like to work on?"
GOOD: "Detected initiative X (60% complete). Continuing..."
```

### ❌ Don't: Skip Session End Protocol

**CRITICAL FAILURE** if:

- Presenting final summary without running `/meta-analysis`
- Leaving completed initiatives in active/ directory
- Uncommitted changes at session end

### ❌ Don't: Over-Prompt

If 80%+ confident on routing, auto-route. User can redirect if wrong.

---

## Success Metrics

✅ **Good Performance:**

- Context detection + routing: <30 seconds
- Autonomous continuation: 70%+ of time
- Session end protocol executed: 100% of time

❌ **Needs Improvement:**

- Asking "what to work on" when context is clear
- Skipping session end protocol
- Requiring user direction for obvious continuations

---

## Integration

### Calls

- `/detect-context` - Context analysis (Stage 1)
- `/load-context` - Efficient context loading (Stage 3)
- `/plan` - Planning workflow
- `/implement` - Implementation workflow (includes testing)
- `/validate` - Quality checks
- `/commit` - Git operations
- `/archive-initiative` - Archive completed work (Stage 4)
- `/meta-analysis` - **MANDATORY** session summary (Stage 4)

### Called By

- User (direct invocation)
- Other workflows (when orchestration needed)

---

## References

- `.windsurf/workflows/detect-context.md` - Context detection logic
- `.windsurf/workflows/load-context.md` - Context loading strategies
- `.windsurf/workflows/meta-analysis.md` - Session end requirements
- `.windsurf/rules/00_agent_directives.md` - Section 1.8 (Session End Protocol)
