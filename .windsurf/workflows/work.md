---
description: Intelligent work orchestration and context detection
auto_execution_mode: 3
---

# Work Orchestration Workflow

**Purpose:** Central orchestration workflow that intelligently detects project context and routes to appropriate specialized workflows.

**Invocation:** `/work` (with optional context) or `/work` (autonomous detection)

**Philosophy:** AI agent should understand where to pick up from by analyzing project state, not by requiring explicit direction.

---

## Stage 1: Detect Project Context

**Call `/detect-context` workflow:**

- Analyzes project state (initiatives, git, tests, sessions)
- Classifies signals by confidence level
- Identifies continuation points
- See: `.windsurf/workflows/detect-context.md`

**Returns:** Detection results with routing recommendation

---

## Stage 2: Route to Appropriate Workflow

### High Confidence (Auto-Route)

**If `/detect-context` returns 80%+ confidence:**

| Detected Context | Route To | Action |
|------------------|----------|--------|
| Active initiative with unchecked tasks | `/implement` | Load initiative context, continue work |
| Test failures | `/implement` | Load test context, fix failures |
| Planning markers ("needs design", ADR placeholders) | `/plan` | Create comprehensive plan |
| Completed initiative pending archive | `/archive-initiative` | Archive completed work |
| Clean state, no signals | Prompt user | Ask for direction |

### Medium Confidence (Present Options)

**If `/detect-context` returns 50-79% confidence:**

Present detected options to user with recommendation:

```markdown
## Detected Context (Multiple Options)

I found [N] possible work streams:

1. **[Option 1]** ([details])
   - Estimated: [time]
   - Recommended: [reason]

2. **[Option 2]** ([details])
   - Estimated: [time]

Which would you like to continue?
```

### Low Confidence (Prompt User)

**If `/detect-context` returns <50% confidence:**

List available options:

1. Create new plan (`/plan`)
2. Review open initiatives
3. Run validation checks (`/validate`)
4. Something else (specify)

---

## Stage 3: Execute Workflow

### Load Context Before Execution

**Call `/load-context` with appropriate scope:**

- Initiative scope: Load initiative + related files
- Planning scope: Load full project context
- Module scope: Load specific module files
- See: `.windsurf/workflows/load-context.md`

### Execute Routed Workflow

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

## Stage 4: Session End Protocol (MANDATORY)

**Before presenting final summary, verify exit criteria:**

### 4.1 Check Completed Initiatives

```bash
# Find initiatives marked complete
grep -l "Status.*Completed\|Status.*✅" docs/initiatives/active/*.md
```

**If found:** MUST call `/archive-initiative` for each (do not skip)

### 4.2 Execute Meta-Analysis

**MUST call `/meta-analysis` workflow:**

- Creates session summary for cross-session continuity
- Identifies workflow/rule improvements
- Documents decisions and learnings
- **NOT OPTIONAL** - This is a mandatory quality gate

### 4.3 Exit Criteria Checklist

```markdown
- [ ] All changes committed (git status clean)
- [ ] All tests passing (if code changes made)
- [ ] Completed initiatives archived
- [ ] Meta-analysis executed
- [ ] Session summary created in docs/archive/session-summaries/
```

**ONLY present final summary after all criteria met.**

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
