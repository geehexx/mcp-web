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

**Output:**

```markdown
## ✓ Context Detected (High Confidence: 85%)

**Detected:** [Brief description]

**Auto-routing to:** [workflow name]

**Rationale:** [1-2 sentences]

Proceeding...
```

### Medium Confidence (30-79%)

**AUTO-PROCEED with recommended - state alternatives but execute.**

**Output:**

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

---

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

### 5.1 Detect Completion Triggers

```bash
# Check if initiative marked complete
grep -l "Status.*Completed\|Status.*✅" docs/initiatives/active/*.md

# Check git status
git status --short
```

**Trigger Session End Protocol if ANY of:**

1. Initiative marked "Completed" or "✅"
2. All planned tasks done
3. User explicitly signals session end

**If triggered, execute FULL protocol:**

### 5.2 Commit All Changes

```bash
git add <modified files>
git commit -m "<conventional commit message>"

# Commit auto-fixes separately
git add <auto-fix files>
git commit -m "style(scope): apply [tool] auto-fixes"
```

### 5.3 Archive Completed Initiatives

```bash
/archive-initiative <initiative-name>
```

**MUST call workflow - do not skip!**

### 5.4 Execute Meta-Analysis

```bash
/meta-analysis
```

**Creates:**

- Session summary in `docs/archive/session-summaries/`
- Workflow improvement recommendations
- Cross-session continuity documentation

### 5.5 Exit Criteria

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

## References

- `.windsurf/workflows/detect-context.md`
- `.windsurf/workflows/load-context.md`
- `.windsurf/workflows/meta-analysis.md`
- `.windsurf/rules/00_agent_directives.md` (Section 1.8)

---
