---
description: Intelligent context detection for work continuation
auto_execution_mode: 3
---

# Detect Context Workflow

**Purpose:** Intelligently analyze project state to determine what work should happen next, enabling autonomous work continuation.

**Invocation:** `/detect-context` (called by `/work` or directly)

**Philosophy:** AI should understand project state and continuation points without explicit user direction.

---

## Stage 1: Rapid Project Scan

### 1.1 Load Essential Context

**Batch read key files (MUST use absolute paths for MCP tools):**

```python
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    "/home/gxx/projects/mcp-web/docs/initiatives/active/*.md"  # All active initiatives
])
```

### 1.2 Check Session Summaries

**Load recent session context:**

```bash
# Get 2-3 most recent summaries
ls -t /home/gxx/projects/mcp-web/docs/archive/session-summaries/*.md | head -3

# Read them for "Next Steps" and "Unresolved" sections
```

**Why session summaries matter:**

- Provide cross-session continuity
- Show recent work patterns and decisions
- Identify deferred work and next steps
- Reveal recurring issues or blockers

### 1.3 Check Git Status

**Analyze recent activity:**

```bash
# Recent commits
git log --oneline -5

# Current working tree state
git status --short

# Modified files
git diff --name-only
```

---

## Stage 2: Signal Detection

### 2.1 Search for Continuation Signals

**Priority 1: Session Summary Signals**

```bash
# Read most recent summary
recent_summary=$(ls -t docs/archive/session-summaries/*.md | head -1)

# Look for:
# - "Next Steps" section → continuation points
# - "Unresolved" issues → blockers to address
# - "Key Learnings" → context for decisions
```

**Priority 2: Active Initiative Signals**

```python
# Parse initiative files for:
for initiative in active_initiatives:
    # Unchecked tasks: [ ] Task name
    unchecked_tasks = find_pattern(r"- \[ \]", initiative)

    # Status field
    status = extract_field("Status:", initiative)

    # Next Steps section
    next_steps = extract_section("Next Steps", initiative)
```

**Priority 3: Git Signals**

```bash
# Unstaged changes → incomplete work
git diff --name-only

# Staged but uncommitted → interrupted work
git diff --staged --name-only

# Recent commit types
git log --pretty=format:"%s" -5 | grep -E "^(feat|fix|test|docs):"
```

**Priority 4: Test Signals**

```bash
# Check for test failures
task test:fast 2>&1 | tail -20 | grep -E "(FAILED|ERROR)"

# Check for pending tests
grep -r "pytest.mark.skip" tests/
grep -r "@unittest.skip" tests/
```

**Priority 5: Documentation TODOs**

```bash
# Efficient grep for markers
grep -r "TODO\|FIXME\|XXX" docs/ --include="*.md"
```

### 2.2 Classify Signals

**Signal strength classification:**

| Signal Type | Strength | Example |
|-------------|----------|---------|
| Session summary "Next Steps" | ⭐⭐⭐ High | "Next: Add CLI key management" |
| Unchecked initiative tasks | ⭐⭐⭐ High | "[ ] Implement validation" |
| Unstaged changes | ⭐⭐ Medium | src/auth.py modified |
| Test failures | ⭐⭐⭐ High | 5 tests failing in test_auth.py |
| Recent commit pattern | ⭐ Low | Last 5 commits all "feat(auth)" |
| TODO markers | ⭐ Low | "TODO: Add error handling" |
| Clean state | ⚪ None | No signals, prompt user |

---

## Stage 3: Context Interpretation

### 3.1 Apply Detection Matrix

**Based on detected signals, determine intent:**

| Detection Pattern | Interpretation | Confidence | Route To |
|-------------------|----------------|------------|----------|
| Session summary "Next Steps" + matching initiative | Continue from last session | High | `/implement` with context |
| Unchecked initiative tasks (3+ remaining) | Continue active initiative | High | `/implement` focused work |
| Test failures mentioned in recent summary | Bug fixing needed | High | `/implement` + TDD |
| "Plan" or "Design" keywords in summaries | Planning phase active | High | `/plan` workflow |
| Multiple incomplete features | Needs prioritization | Medium | `/plan` → prioritize |
| Recent ADR + "decide" keywords | Architecture decision in progress | Medium | `/new-adr` or review |
| Unstaged changes + no context | Work interrupted mid-session | Medium | Prompt user |
| Clean state + no initiative | New work starting | Low | Prompt user |

### 3.2 Extract Specific Context

**For each high-confidence signal:**

```python
if signal_type == "initiative_tasks":
    # Extract exact tasks
    initiative_file = signal.source
    unchecked = extract_unchecked_tasks(initiative_file)
    context = {
        "initiative": initiative_file,
        "next_tasks": unchecked[:3],  # Next 3 tasks
        "phase": extract_current_phase(initiative_file)
    }

elif signal_type == "session_next_steps":
    # Extract next steps
    summary_file = signal.source
    next_steps = extract_section("Next Steps", summary_file)
    context = {
        "summary": summary_file,
        "next_steps": next_steps,
        "unresolved": extract_section("Unresolved", summary_file)
    }

elif signal_type == "test_failures":
    # Extract failure details
    test_output = run_command("task test:fast")
    failures = parse_pytest_failures(test_output)
    context = {
        "test_failures": failures,
        "affected_modules": extract_modules(failures)
    }
```

---

## Stage 4: Confidence Assessment

### 4.1 Calculate Confidence Score

**Scoring algorithm:**

```python
confidence_score = 0

# Session summary signals (+30 each)
if has_next_steps_in_summary:
    confidence_score += 30
if has_unresolved_in_summary:
    confidence_score += 30

# Initiative signals (+25 each)
if has_unchecked_tasks:
    confidence_score += 25
if initiative_status == "Active":
    confidence_score += 25

# Git signals (+15 each)
if has_unstaged_changes:
    confidence_score += 15
if recent_commits_same_area:
    confidence_score += 15

# Test signals (+20 each)
if has_test_failures:
    confidence_score += 20

# Documentation signals (+10 each)
if has_todo_markers:
    confidence_score += 10
```

**Confidence thresholds:**

| Score | Confidence | Action |
|-------|------------|--------|
| 80+ | High | Auto-route to workflow |
| 50-79 | Medium | Present options with recommendation |
| 20-49 | Low | Present multiple options |
| <20 | None | Prompt user for direction |

### 4.2 Handle Ambiguity

**If multiple strong signals:**

```markdown
## Detected Multiple Work Streams

I found 2 high-confidence continuation points:

1. **Initiative: API Key Authentication** (Phase 2, 60% complete)
   - Session summary: "Next: Add CLI key management commands"
   - 4 unchecked tasks remaining
   - Estimated: 2-3 hours

2. **Test Failures: Security Module** (5 failures)
   - test_security.py: 5/15 tests failing
   - Introduced in last commit (2 hours ago)
   - Estimated: 1 hour to fix

**Recommendation:** Fix test failures first (blocking), then continue initiative.

Which would you like to tackle?
1. Fix test failures (recommended)
2. Continue API Key Authentication
3. Something else
```

---

## Stage 5: Routing Decision

### 5.1 High Confidence Auto-Route

**If confidence ≥80%, automatically route:**

```markdown
## Context Detected ✓

**Source:** docs/archive/session-summaries/2025-10-17-afternoon.md

**Detection:**
- Session summary indicates: "Next: Add CLI key management commands"
- Active initiative: docs/initiatives/active/api-key-auth.md (Phase 2)
- Status: Active, 3/7 tasks complete
- No blockers

**Auto-routing to:** `/implement` with initiative context

Loading initiative and related files...
```

### 5.2 Medium Confidence Recommendation

**If confidence 50-79%, recommend with options:**

```markdown
## Context Analysis

**Primary Signal:** Unchecked tasks in API Key Authentication initiative

**Evidence:**
- 4 tasks remaining in Phase 2
- No test failures
- No unstaged changes
- Last commit: 3 hours ago (feat: add validation)

**Recommendation:** Continue initiative implementation

**Alternative Options:**
1. **Continue initiative** (recommended) - Clear next steps defined
2. **Run validation** - Ensure current state is clean before continuing
3. **Review architecture** - Check if ADR needed before implementation

What would you like to do?
```

### 5.3 Low Confidence Prompt

**If confidence <50%, present options:**

```markdown
## Project State Analysis

**Detected Signals:**
- Clean git state (no uncommitted changes)
- 2 active initiatives (both in progress)
- No test failures
- No recent session summary

**Unable to determine clear next step.**

What would you like to work on?
1. **Continue Initiative A** (API Key Auth)
2. **Continue Initiative B** (Performance Optimization)
3. **Create new plan** for upcoming work
4. **Review and commit** existing work
5. **Something else** (please specify)
```

---

## Stage 6: Load Detailed Context

### 6.1 Load Context for Detected Work

**Once routing decided, load full context:**

```python
if route == "implement_initiative":
    # Load initiative context
    call_workflow("/load-context", scope="initiative")

elif route == "fix_tests":
    # Load test module context
    call_workflow("/load-context", scope="module:tests")

elif route == "planning":
    # Load full context for planning
    call_workflow("/load-context", scope="full")
```

### 6.2 Verify Context Completeness

**Before proceeding:**

```markdown
✅ Initiative file loaded
✅ Related source files loaded (3 files)
✅ Test files loaded (2 files)
✅ Recent commits analyzed (5 commits)
⚠️ No related ADR found (acceptable)

**Context ready.** Proceeding with implementation...
```

---

## Examples

### Example 1: Clear Session Continuation

**Input:** New session, user invokes `/work`

**Detection:**

```bash
# Load recent summary
$ cat docs/archive/session-summaries/2025-10-17-afternoon.md

## Next Steps
1. Add CLI key management commands (add, revoke, list)
2. Implement key rotation logic
3. Add integration tests for key lifecycle
```

**Analysis:**

- ⭐⭐⭐ Session summary with clear next steps
- ⭐⭐⭐ Matching active initiative found
- Confidence: 85% (High)

**Decision:** Auto-route to `/implement` with initiative context

**Output:**

```markdown
✓ Detected continuation point from last session
→ Routing to /implement for "API Key Authentication" (Phase 2)
→ Next task: Add CLI key management commands
```

### Example 2: Test Failure Detected

**Input:** User invokes `/work` after failed CI

**Detection:**

```bash
# Run tests
$ task test:fast
FAILED tests/unit/test_security.py::test_xss_sanitization
FAILED tests/unit/test_security.py::test_sql_injection_prevention
```

**Analysis:**

- ⭐⭐⭐ Test failures (2 tests)
- ⭐⭐ Recent commits modified security.py
- Confidence: 75% (Medium)

**Decision:** Recommend test fix first

**Output:**

```markdown
⚠️ Test failures detected (2 failing tests)

Recommendation: Fix failing tests before continuing other work.

Would you like to:
1. Fix test failures (recommended)
2. Continue with initiative work
```

### Example 3: Multiple Initiatives

**Input:** User invokes `/work`, multiple active initiatives

**Detection:**

```bash
# Active initiatives
- docs/initiatives/active/api-key-auth.md (Status: Active, 3/7 tasks)
- docs/initiatives/active/performance-opt.md (Status: Active, 5/12 tasks)

# No recent session summary
# No clear signals
```

**Analysis:**

- ⭐⭐ Two active initiatives
- ⭐ No clear preference signal
- Confidence: 40% (Low)

**Decision:** Prompt user to choose

**Output:**

```markdown
Found 2 active initiatives:

1. **API Key Authentication** (Phase 2, 43% complete)
   - 4 tasks remaining
   - Last updated: 3 hours ago

2. **Performance Optimization** (Phase 1, 42% complete)
   - 7 tasks remaining
   - Last updated: 2 days ago

Which would you like to continue?
```

### Example 4: Clean Slate

**Input:** User invokes `/work`, no active work

**Detection:**

```bash
# No active initiatives
# No unstaged changes
# No test failures
# Clean git state
```

**Analysis:**

- ⚪ No signals detected
- Confidence: 0% (None)

**Decision:** Prompt for new work

**Output:**

```markdown
Project state is clean with no active work detected.

What would you like to do?
1. Create a new plan (/plan)
2. Start a new initiative
3. Review and archive completed work
4. Something else
```

---

## Anti-Patterns

### ❌ Don't: Ignore Session Summaries

**Bad:**

```markdown
AI: *ignores session summaries*
AI: "What would you like to work on?"
User: "Continue from last session"
AI: "What did you work on last session?"
```

**Good:**

```markdown
AI: *reads session summary*
AI: "Detected continuation point: Add CLI key management"
AI: "Loading context and proceeding..."
```

### ❌ Don't: Over-Rely on Git Status

**Bad:**

```markdown
# Only checks git status
git status: clean
AI: "No work to continue"
# Ignores active initiatives and session summaries
```

**Good:**

```markdown
# Checks multiple signals
git status: clean
session summary: "Next: Implement feature X"
initiative: [ ] Feature X implementation
AI: "Continuing feature X from last session"
```

### ❌ Don't: Auto-Route on Low Confidence

**Bad:**

```markdown
Confidence: 35%
AI: "Assuming you want to continue initiative A..."
# Might be wrong assumption
```

**Good:**

```markdown
Confidence: 35%
AI: "Found multiple possible work streams. Which would you like?"
# Let user decide when ambiguous
```

---

## Integration Points

### Called By

- `/work` - Primary caller for context detection
- User - Direct invocation for analysis

### Calls

- `/load-context` - Load detailed context after detection
- Git commands - Analyze repository state
- File system tools - Read summaries and initiatives

---

## Performance

**Detection time targets:**

| Phase | Target Time |
|-------|-------------|
| Load essential context | <1 second |
| Search for signals | <2 seconds |
| Analyze and classify | <1 second |
| **Total detection** | **<4 seconds** |

**Optimization:**

- Batch reads for file loading
- Parallel grep searches where possible
- Cache git log results within session

---

## References

- [Factory.ai Context Detection](https://factory.ai/news/context-window-problem)
- [Anthropic Long-Context Patterns](https://docs.anthropic.com/claude/docs/long-context-window-tips)
- Project: `.windsurf/workflows/work.md` (Context detection strategy)
- Project: `.windsurf/workflows/load-context.md` (Context loading)

---
