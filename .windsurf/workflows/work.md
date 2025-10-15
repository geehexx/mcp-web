---
description: Intelligent work orchestration and context detection
auto_execution_mode: 3
---

# Work Orchestration Workflow

**Purpose:** Central orchestration workflow that intelligently detects project context and routes to appropriate specialized workflows.

**Invocation:** `/work` (with optional context) or `/work` (autonomous detection)

**Philosophy:** AI agent should understand where to pick up from by analyzing project state, not by requiring explicit direction.

---

## Stage 1: Context Detection (Automatic)

Intelligently analyze project state using **efficient batch operations**.

### 1.1 Rapid Project Scan

**Use batch reads for efficiency:**

```python
# Read multiple key files simultaneously
mcp0_read_multiple_files([
    "docs/PROJECT_SUMMARY.md",
    "docs/initiatives/active/*.md",  # All active initiatives
    ".windsurf/rules/00_agent_directives.md"
])
```

**Scan for:**
- **Session summaries** (`docs/archive/session-summaries/` - most recent 2-3)
- Active initiatives (`docs/initiatives/active/`)
- Recent git activity (last 5 commits)
- Unfinished work markers (`TODO`, `FIXME`, `XXX`, incomplete checklist items)
- Test failures (check CI status if available)
- Open issues mentioned in docs

**Why session summaries matter:**
- Provide cross-session continuity when conversation context lost
- Show recent work patterns and decisions
- Identify deferred work and next steps
- Reveal recurring issues or blockers

### 1.2 Intelligent File System Search

**Prioritized search pattern:**

0. **Recent Session Summaries** (cross-session context)
   ```bash
   # Get 2-3 most recent summaries
   ls -t docs/archive/session-summaries/*.md | head -3
   ```
   - Read "Next Steps" sections
   - Check "Unresolved" issues
   - Review "Key Learnings"
   - Identify continuation points

1. **Initiatives** (highest context value)
   ```
   docs/initiatives/active/
   ```
   - Look for unchecked `[ ]` items
   - Check "Status:" field
   - Identify "Next Steps" sections

2. **Recent Changes** (git intelligence)
   ```bash
   git log --oneline -5
   git status --short
   ```
   - Unstaged changes → incomplete work
   - Recent commits → continuation context

3. **Test Results**
   ```bash
   # Check last test run
   task test:fast 2>&1 | tail -20
   ```
   - Failures → implementation needed
   - Pending tests → TDD workflow

4. **Documentation TODOs**
   ```bash
   # Efficient grep for markers
   grep_search("TODO\\|FIXME\\|XXX", "docs/", recursive=true)
   ```

### 1.3 Context Interpretation Matrix

Based on detected signals, classify intent:

| Detection Pattern | Interpretation | Route To |
|-------------------|----------------|----------|
| Session summary "Next Steps" | Continue from last session | Implementation workflow |
| Unchecked initiative tasks | Continue initiative | Implementation workflow |
| Test failures mentioned | Bug fixing needed | `/implement` + tests first |
| "Plan" or "Design" in recent docs | Planning needed | `/plan` workflow |
| Multiple incomplete features | Needs prioritization | `/plan` → prioritize |
| Meta-analysis doc present | Review improvements | Read then prompt user |
| ADR needed markers | Architecture decision | `/new-adr` workflow |
| Clean state, no context | New work starting | Prompt user for direction |

---

## Stage 2: Smart Routing Decision

### 2.1 Auto-Route (High Confidence)

**If clear signal detected, automatically route:**

**Example 1: Active Initiative**
```markdown
Detected: docs/initiatives/active/fix-security-unit-tests.md
Status: Active, 3/10 tasks completed
→ AUTO-ROUTE: /implement with context loaded
```

**Example 2: Test Failures**
```markdown
Detected: 10 test failures in tests/unit/test_security.py
Last modified: 2 hours ago
→ AUTO-ROUTE: /implement focusing on test fixes
```

**Example 3: Planning Markers**
```markdown
Detected: Multiple "needs design" comments
Detected: ADR placeholder markers
→ AUTO-ROUTE: /plan to create comprehensive plan
```

### 2.2 Clarify (Ambiguous)

**If multiple signals or unclear context:**

Present options to user:

```markdown
## Detected Project Context

I found multiple active work streams:

1. **Initiative: Fix Security Unit Tests** (3/10 complete)
   - 7 failing tests in test_security.py
   - Estimated: 2-3 hours remaining

2. **Initiative: Quality Foundation** (Phase 2 in progress)
   - Documentation linting setup
   - 5 unchecked tasks

3. **Recent Changes**
   - Uncommitted work in src/mcp_web/security.py
   - May indicate work in progress

Which would you like to continue?
1. Fix security tests (/implement)
2. Continue quality foundation (/implement)
3. Review and commit recent changes (/commit)
4. Create new plan (/plan)
5. Something else (please specify)
```

---

## Stage 3: Workflow Execution

### 3.1 Load Full Context

Before executing routed workflow, load complete context:

**For Implementation:**
```markdown
1. Read initiative file completely
2. Read related source files (identified from initiative)
3. Check test status
4. Review recent commits for this area
5. Execute /implement with full context
```

**For Planning:**
```markdown
1. Read PROJECT_SUMMARY.md
2. Read ARCHITECTURE.md
3. Scan active ADRs
4. Check completed initiatives for patterns
5. Execute /plan with strategic context
```

### 3.2 Workflow Chaining

Workflows can call each other:

```markdown
/work
  → detects planning needed
  → calls /plan
  → plan complete
  → calls /implement with plan context
  → implementation complete (tests integrated)
  → calls /commit
```

---

## Stage 4: Continuation Logic

### 4.1 Session Resumption

**When invoked mid-session:**

1. Check for checkpoint markers in conversation history
2. Review last 10 messages for context
3. Identify last completed task
4. Resume from next logical step

### 4.2 Cross-Session Resumption

**When invoked in new session:**

1. **Cannot access prior conversation** (new session)
2. Rely on file system state and session summaries
3. **Primary context source: Session summaries**
   ```bash
   # Read 2-3 most recent summaries
   ls -t docs/archive/session-summaries/*.md | head -3 | xargs cat
   ```
   - Extract "Next Steps" section
   - Note "Unresolved" issues
   - Review recent decisions
   - Identify work patterns

4. Look for session artifacts:
   - Uncommitted changes
   - In-progress markers in initiatives
   - Recent git activity (correlate with summary dates)
   - Open test failures

**Context compaction strategy** (per Anthropic research):
- Session summaries = compressed context from previous sessions
- Preserve critical decisions, unresolved issues, next steps
- Discard verbose details (available in git history if needed)

---

## Efficiency Optimizations

### Batch Operations (Always)

❌ **Bad** (Sequential reads):
```python
read_file("docs/initiatives/active/initiative1.md")
read_file("docs/initiatives/active/initiative2.md")
read_file("docs/PROJECT_SUMMARY.md")
# 3 separate tool calls → slow
```

✅ **Good** (Batch read):
```python
mcp0_read_multiple_files([
    "docs/initiatives/active/initiative1.md",
    "docs/initiatives/active/initiative2.md",
    "docs/PROJECT_SUMMARY.md"
])
# 1 tool call → 3x faster
```

### Smart Grep (Targeted)

❌ **Bad** (Broad search):
```python
grep_search("TODO", "/", recursive=true)
# Searches entire file system, including node_modules, .git, etc.
```

✅ **Good** (Focused search):
```python
grep_search("TODO", "docs/", recursive=true, includes=["*.md"])
grep_search("FIXME", "src/", recursive=true, includes=["*.py"])
# Targeted, fast, relevant results
```

### Minimal Tool Calls

**Goal:** Understand context in ≤5 tool calls

1. `mcp0_read_multiple_files()` - Batch read key docs
2. `git log` + `git status` - Git context
3. `grep_search()` - Find markers (if needed)
4. `list_dir()` - Scan initiatives (if not batched)
5. Route decision

---

## Anti-Patterns to Avoid

### ❌ Don't: Ask Obvious Questions

```markdown
BAD: "What would you like to work on?"
GOOD: "I detected initiative X is 60% complete. Continuing..."
```

### ❌ Don't: Read Files One-by-One

Use `mcp0_read_multiple_files()` always.

### ❌ Don't: Search Without Focus

Always provide `includes` filters to grep.

### ❌ Don't: Ignore Git State

`git status` is fast and provides critical context.

### ❌ Don't: Overthink

If 80% confident on route, take it. Don't ask permission for obvious continuations.

---

## Examples

### Example 1: Initiative Continuation

**User:** `/work`

**Agent Actions:**
1. Read active initiatives (batch)
2. Found: `fix-security-unit-tests.md` with 3/10 tasks done
3. Auto-route to `/implement`
4. Load test file context
5. Begin fixing next failing test

**Output:**
```markdown
## Continuing: Fix Security Unit Tests (3/10 complete)

Next task: Fix `test_no_false_positives` pattern detection

Loading context...
✓ Read initiative file
✓ Read tests/unit/test_security.py
✓ Read src/mcp_web/security.py
✓ Checked test results

Proceeding with implementation...
```

### Example 2: Clean Slate Planning

**User:** `/work create user authentication`

**Agent Actions:**
1. Detected: New feature request
2. No existing initiative found
3. Auto-route to `/plan`
4. Create comprehensive plan
5. Prompt user for approval
6. Create initiative file
7. Begin implementation

### Example 3: Bug Fix Detection

**User:** `/work`

**Agent Actions:**
1. Run `task test:fast`
2. Detected: 2 new test failures
3. No related initiative
4. Create initiative: `fix-test-failures-YYYY-MM-DD.md`
5. Auto-route to `/implement`
6. Begin debugging

---

## Integration with Other Workflows

### Called By

- User (direct invocation)
- Other workflows (when context needed)

### Calls

- `/plan` - When planning needed
- `/implement` - For execution (includes testing)
- `/commit` - For committing work
- `/new-adr` - For architectural decisions
- `/run-tests` - For testing guidance
- `/archive-initiative` - For completing initiatives
- `/meta-analysis` - **AUTOMATIC at session end** (captures learnings)

### Session End Protocol

**When work is complete or context window filling:**

1. Check for uncommitted changes (`git status`)
2. Commit any remaining work (`/commit`)
3. **Run `/meta-analysis`** - Creates session summary and captures learnings
4. Final commit of meta-analysis

**This ensures:**
- ✅ Session summaries always created in proper location
- ✅ Learnings captured for future sessions
- ✅ Cross-session context preserved
- ✅ Improvements identified and documented

**Not optional:** Meta-analysis MUST run at end of every work session.

### Validation Checks

Before finishing `/work`, verify:

- [ ] All work committed to git
- [ ] `/meta-analysis` workflow executed
- [ ] Session summary created in `docs/archive/session-summaries/`
- [ ] Timestamp file `.windsurf/.last-meta-analysis` updated
- [ ] No uncommitted changes remain

**If meta-analysis not run:**
- **STOP** - Do not proceed
- Execute `/meta-analysis` immediately
- Document violation in session summary
- Propose workflow improvements

**Auto-detection:**
```bash
# Check if meta-analysis is overdue
if [ -f .windsurf/.last-meta-analysis ]; then
  LAST=$(cat .windsurf/.last-meta-analysis)
  echo "Last meta-analysis: $LAST"
  # Agent should compare timestamp and warn if >24h old
else
  echo "WARNING: Meta-analysis never run before"
fi
```

---

---

## Stage 5: Session End Protocol (MANDATORY)

**CRITICAL:** This stage MUST execute before presenting final summary to user.

### 5.1 Exit Criteria Checklist

Before ending any work session, verify:

```markdown
## Exit Criteria (ALL MUST BE TRUE)

- [ ] All changes committed (git status clean OR only .windsurf/.last-meta-analysis unstaged)
- [ ] All tests passing (if code changes made)
- [ ] Completed initiatives archived (see 5.2)
- [ ] Meta-analysis executed (see 5.3)
- [ ] Session summary created in proper location
```

### 5.2 Archive Completed Initiatives (AUTOMATIC)

**Check for initiatives marked complete:**

```bash
# Search for completed status markers in active initiatives
grep -l "Status.*Completed\|Status.*✅" docs/initiatives/active/*.md
```

**If any found:**
1. MUST call `/archive-initiative` workflow for each
2. Do NOT skip this - completed initiatives pollute active directory
3. Archiving must complete before meta-analysis

**Why this matters:**
- Active directory should only contain active work
- Completed initiatives provide historical context when archived
- Skipping creates clutter and confusion in next session

### 5.3 Execute Meta-Analysis (MANDATORY)

**MUST call `/meta-analysis` workflow:**

```bash
# This is NOT optional - it's a mandatory exit gate
/meta-analysis
```

**Why this is mandatory:**
- Creates session summary for cross-session continuity
- Identifies workflow/rule improvements
- Enables next session to pick up context
- Documents decisions and learnings

**Enforcement:**
- Agent MUST NOT present final summary without running meta-analysis
- User should never see work completion without session summary created
- If skipped, this is a CRITICAL workflow violation

### 5.4 Final Presentation

**ONLY after all exit criteria met:**

Present structured summary to user:
```markdown
# ✅ Session Complete

## Work Completed
[Brief bullet list from commits]

## Tests Status
[Pass/fail counts]

## Session Summary
Created: docs/archive/session-summaries/YYYY-MM-DD-description.md

## Archived Initiatives
[List any initiatives archived]

## Next Session Starting Points
[Top 3 priorities from session summary]
```

---

## Success Metrics

✅ **Good Performance:**
- Context detection in <30 seconds
- <5 tool calls for context gathering
- Correct routing 90%+ of time
- Autonomous continuation (no user prompt) 70%+ of time
- **Session end protocol executed 100% of time**

❌ **Needs Improvement:**
- >1 minute for context detection
- >10 tool calls
- Asking user "what to work on" when context is clear
- Requiring user direction for obvious continuations
- **Skipping session end protocol (CRITICAL FAILURE)**

---

## References

- [Agentic AI Workflows Guide (2025)](https://devcom.com/tech-blog/ai-agentic-workflows/)
- [Claude Agent SDK Best Practices (2025)](https://skywork.ai/blog/claude-agent-sdk-best-practices-ai-agents-2025/)
- [AI Agents for Enterprise Workflows (2025)](https://www.ampcome.com/post/ai-agents-enterprise-workflows-2025-guide)
- hexacore-command project: Intelligent documentation search patterns

---

**Last Updated:** October 15, 2025
**Version:** 1.0
