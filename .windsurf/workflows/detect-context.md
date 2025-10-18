---
created: "2025-10-17"
updated: "2025-10-18"
description: Intelligent context detection for work continuation
auto_execution_mode: 3
category: Operations
complexity: 80
tokens: 1617
dependencies: []
status: active
---

# Detect Context Workflow

**Purpose:** Analyze project state to determine what work should happen next, enabling autonomous continuation.

**Invocation:** `/detect-context` (called by `/work` or directly)

---

## Stage 1: Rapid Project Scan

### 1.1 Load Essential Context

Batch read key files (MUST use absolute paths for MCP tools):

```python
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/PROJECT_SUMMARY.md",
    "/home/gxx/projects/mcp-web/docs/initiatives/active/*.md"
])
```

### 1.2 Check Session Summaries

```bash
# Get 2-3 most recent summaries
ls -t /home/gxx/projects/mcp-web/docs/archive/session-summaries/*.md | head -3
```

Look for: "Next Steps", "Unresolved" sections, recent decisions

### 1.3 Check Git Status

```bash
git log --oneline -5
git status --short
git diff --name-only
```

---

## Stage 2: Signal Detection

### 2.1 Search for Continuation Signals

**Priority 1: Session Summary**

```bash
recent_summary=$(ls -t docs/archive/session-summaries/*.md | head -1)
# Look for: "Next Steps", "Unresolved" issues, "Key Learnings"
```

**Priority 2: Active Initiatives**

```python
for initiative in active_initiatives:
    unchecked_tasks = find_pattern(r"- \[ \]", initiative)
    status = extract_field("Status:", initiative)
    next_steps = extract_section("Next Steps", initiative)
```

**Priority 3: Git Signals**

```bash
git diff --name-only  # Unstaged changes
git diff --staged --name-only  # Staged but uncommitted
git log --pretty=format:"%s" -5 | grep -E "^(feat|fix|test):"
```

**Priority 4: Test Signals**

```bash
task test:fast 2>&1 | tail -20 | grep -E "(FAILED|ERROR)"
grep -r "pytest.mark.skip" tests/
```

**Priority 5: Documentation Signals**

```bash
grep -r "TODO\|FIXME\|XXX" docs/ --include="*.md"
```

### 2.2 Classify Signals

| Signal Type | Strength | Example |
|-------------|----------|---------|
| Session summary "Next Steps" | ⭐⭐⭐ High | "Next: Add CLI commands" |
| Unchecked initiative tasks | ⭐⭐⭐ High | "[ ] Implement validation" |
| Test failures | ⭐⭐⭐ High | 5 tests failing in test_auth.py |
| Unstaged changes | ⭐⭐ Medium | src/auth.py modified |
| Recent commit pattern | ⭐ Low | Last 5 commits all "feat(auth)" |
| TODO markers | ⭐ Low | "TODO: Add error handling" |
| Clean state | ⚪ None | No signals, prompt user |

---

## Stage 3: Context Interpretation

### 3.1 Detection Matrix

| Pattern | Interpretation | Confidence | Route To |
|---------|----------------|------------|----------|
| Session "Next Steps" + matching initiative | Continue from last session | High | `/implement` |
| Unchecked tasks (3+) | Continue initiative | High | `/implement` |
| Test failures in summary | Bug fixing needed | High | `/implement` + TDD |
| "Plan" keywords in summary | Planning phase active | High | `/plan` |
| Multiple incomplete features | Needs prioritization | Medium | `/plan` |
| Recent ADR + "decide" | Architecture decision | Medium | `/new-adr` |
| Unstaged changes + no context | Work interrupted | Medium | Prompt user |
| Clean state + no initiative | New work | Low | Prompt user |

### 3.2 Extract Specific Context

```python
if signal_type == "initiative_tasks":
    context = {
        "initiative": initiative_file,
        "next_tasks": unchecked[:3],
        "phase": extract_current_phase(initiative_file)
    }

elif signal_type == "session_next_steps":
    context = {
        "summary": summary_file,
        "next_steps": extract_section("Next Steps", summary_file),
        "unresolved": extract_section("Unresolved", summary_file)
    }

elif signal_type == "test_failures":
    failures = parse_pytest_failures(run_command("task test:fast"))
    context = {
        "test_failures": failures,
        "affected_modules": extract_modules(failures)
    }
```

---

## Stage 4: Confidence Assessment

### 4.1 Calculate Confidence Score

```python
confidence_score = 0
if has_next_steps_in_summary: confidence_score += 30
if has_unresolved_in_summary: confidence_score += 30
if has_unchecked_tasks: confidence_score += 25
if initiative_status == "Active": confidence_score += 25
if has_unstaged_changes: confidence_score += 15
if recent_commits_same_area: confidence_score += 15
if has_test_failures: confidence_score += 20
if has_todo_markers: confidence_score += 10
```

**Thresholds:**

| Score | Confidence | Action |
|-------|------------|--------|
| 80+ | High | Auto-route |
| 30-79 | Medium | Auto-proceed with recommendation |
| <30 | Low | Prompt user |

### 4.2 Handle Ambiguity

**Multiple strong signals:**

```markdown
## Detected Multiple Work Streams

1. **Initiative: API Key Auth** (Phase 2, 60% complete)
   - Session: "Next: Add CLI commands"
   - 4 unchecked tasks, ~2-3 hours

2. **Test Failures: Security Module** (5 failures)
   - test_security.py: 5/15 failing
   - ~1 hour to fix

**Recommendation:** Fix tests first (blocking), then continue initiative.

Which would you like?
1. Fix test failures (recommended)
2. Continue initiative
3. Something else
```

---

## Stage 5: Routing Decision

### 5.1 High Confidence (≥80%)

```markdown
## Context Detected ✓

**Source:** docs/archive/session-summaries/2025-10-17-afternoon.md

**Detection:**
- Session: "Next: Add CLI key management commands"
- Initiative: api-key-auth.md (Phase 2, 3/7 tasks complete)
- No blockers

**Auto-routing to:** `/implement` with initiative context
```

### 5.2 Medium Confidence (50-79%)

```markdown
## Context Analysis

**Primary:** 4 unchecked tasks in API Key Auth

**Evidence:**
- No test failures
- No unstaged changes
- Last commit: 3 hours ago (feat: validation)

**Recommendation:** Continue initiative

**Alternatives:**
1. **Continue initiative** (recommended)
2. **Run validation** first
3. **Review architecture**

What would you like?
```

### 5.3 Low Confidence (<50%)

```markdown
## Project State

**Signals:**
- Clean git state
- 2 active initiatives (both in progress)
- No test failures
- No recent summary

**Unable to determine clear next step.**

What would you like?
1. **Continue Initiative A** (API Key Auth)
2. **Continue Initiative B** (Performance Opt)
3. **Create new plan**
4. **Review and commit**
5. **Something else**
```

---

## Stage 6: Load Detailed Context

### 6.1 Load Context for Work

```python
if route == "implement_initiative":
    call_workflow("/load-context", scope="initiative")
elif route == "fix_tests":
    call_workflow("/load-context", scope="module:tests")
elif route == "planning":
    call_workflow("/load-context", scope="full")
```

### 6.2 Verify Completeness

```markdown
✅ Initiative file loaded
✅ Source files loaded (3 files)
✅ Test files loaded (2 files)
✅ Recent commits analyzed (5)
⚠️ No related ADR (acceptable)

**Context ready.** Proceeding...
```

---

## Examples

### Example 1: Clear Continuation

**Detection:**

- ⭐⭐⭐ Session summary: "Next: Add CLI commands"
- ⭐⭐⭐ Matching initiative found
- Confidence: 85%

**Output:**

```markdown
✓ Detected continuation from last session
→ Routing to /implement for "API Key Auth" (Phase 2)
```

### Example 2: Test Failures

**Detection:**

- ⭐⭐⭐ 2 test failures
- ⭐⭐ Recent commits modified security.py
- Confidence: 75%

**Output:**

```markdown
⚠️ Test failures detected (2 failing)

Recommendation: Fix tests first.

1. Fix failures (recommended)
2. Continue initiative work
```

### Example 3: Multiple Initiatives

**Detection:**

- ⭐⭐ Two active initiatives
- ⭐ No clear preference
- Confidence: 40%

**Output:**

```markdown
Found 2 active initiatives:

1. **API Key Auth** (Phase 2, 43% complete)
2. **Performance Opt** (Phase 1, 42% complete)

Which would you like?
```

### Example 4: Clean Slate

**Detection:**

- ⚪ No signals
- Confidence: 0%

**Output:**

```markdown
Project state is clean.

What would you like?
1. Create plan (/plan)
2. Start initiative
3. Review completed work
4. Something else
```

---

## Anti-Patterns

### ❌ Don't: Ignore Session Summaries

- **Bad:** "What did you work on last session?"
- **Good:** "Continuing from last session: Add CLI commands"

### ❌ Don't: Over-Rely on Git Only

- **Bad:** Git clean → "No work to continue"
- **Good:** Check summaries + initiatives → "Continuing feature X"

### ❌ Don't: Auto-Route on Low Confidence

- **Bad:** 35% confidence → "Assuming initiative A..."
- **Good:** 35% confidence → "Which would you like?"

---

## Performance Targets

| Phase | Target |
|-------|--------|
| Load context | <1s |
| Search signals | <2s |
| Analyze | <1s |
| **Total** | **<4s** |

**Optimization:** Batch reads, parallel grep, cache git log

---

## References

- [Factory.ai Context Detection](https://factory.ai/news/context-window-problem)
- [Anthropic Long-Context Tips](https://docs.anthropic.com/claude/docs/long-context-window-tips)
- `.windsurf/workflows/work.md`
- `.windsurf/workflows/load-context.md`

---
