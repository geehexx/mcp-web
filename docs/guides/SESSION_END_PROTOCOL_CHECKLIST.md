# Session End Protocol Checklist

**Purpose:** Quick reference for executing the mandatory session end protocol.

**Created:** 2025-10-20
**Related:** `.windsurf/workflows/work-session-protocol.md`, `.windsurf/workflows/meta-analysis.md`

---

## Quick Checklist

At the end of **every work session**, execute these steps in order:

- [ ] 1. **Commit all changes** (working tree clean)
- [ ] 2. **Archive completed initiatives** (if any completed)
- [ ] 3. **Run meta-analysis** (MANDATORY - creates session summary)
- [ ] 4. **Verify exit criteria** (all tests pass, docs updated)
- [ ] 5. **Present completion summary** (only after all above complete)

---

## Detailed Steps

### Step 1: Commit All Changes

```bash
# Check status
git status

# Stage all changes
git add -A

# Commit with descriptive message
git commit -m "type(scope): description

- Detail 1
- Detail 2

Initiative/Ref: [if applicable]"
```

**Verify:** `git status` shows "nothing to commit, working tree clean"

---

### Step 2: Archive Completed Initiatives

**Only if initiative marked "Completed" or "✅":**

```bash
# Archive using automation script
task archive:initiative NAME=initiative-name

# Or with path
task archive:initiative NAME=docs/initiatives/active/initiative-name.md
```

**Supported formats:**

- Just name: `2025-10-20-feature-name`
- Relative path: `docs/initiatives/active/2025-10-20-feature-name.md`
- Absolute path: `/home/user/project/docs/initiatives/active/...`

**Verify:** Initiative moved to `docs/initiatives/completed/` and references updated

---

### Step 3: Run Meta-Analysis (MANDATORY)

**CRITICAL:** This is a **workflow invocation**, not a script!

#### ❌ WRONG

```bash
python scripts/meta_analysis.py  # This script doesn't exist!
```

#### ✅ CORRECT

**Option A: Via Windsurf IDE** (Recommended)

1. Type `/meta-analysis` in chat
2. Let workflow execute fully
3. Review generated session summary

**Option B: Manual execution** (if workflow unavailable)

1. Extract session data:

   ```bash
   # Get commits since last session
   git log --oneline --since="12 hours ago"

   # Identify key accomplishments
   # - What was completed?
   # - What decisions were made?
   # - What was learned?
   ```

2. Create session summary:

   ```bash
   # Create file: docs/archive/session-summaries/YYYY-MM-DD-description.md
   # Use template from docs/DOCUMENTATION_STRUCTURE.md
   ```

3. Update timestamp:

   ```bash
   date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis
   ```

4. Commit:

   ```bash
   git add docs/archive/session-summaries/*.md .windsurf/.last-meta-analysis
   git commit -m "docs(session): add YYYY-MM-DD session summary"
   ```

**Verify:**

- Session summary exists in `docs/archive/session-summaries/`
- Timestamp file updated: `.windsurf/.last-meta-analysis`

---

### Step 4: Verify Exit Criteria

Run quality gates:

```bash
# All tests pass
task test:fast
# Expected: 269 passed

# Linting clean
task lint
# Expected: All checks passed!

# Markdown quality
task docs:lint
# Expected: 0 error(s)
```

**Verify:**

- [ ] All tests passing
- [ ] Linting clean
- [ ] Markdown formatting compliant
- [ ] No uncommitted changes
- [ ] Working tree clean

---

### Step 5: Present Completion Summary

**ONLY after Steps 1-4 complete**, present a summary like:

```markdown
## ✅ Session Complete: [Initiative/Task Name]

**Status:** [Completed/In Progress]
**Duration:** ~N hours
**Commits:** N commits

### Achievements
- Completed X
- Implemented Y
- Fixed Z

### Quality Verification
✅ All tests passing (269/269)
✅ Linting clean
✅ Markdown quality verified
✅ Working tree clean

### Next Steps
[What to do in next session, if applicable]
```

---

## Common Issues

### Issue: "Meta-analysis script not found"

**Symptom:**

```text
python3: can't open file 'scripts/meta_analysis.py': [Errno 2] No such file or directory
```

**Cause:** Attempting to run meta-analysis as a script instead of workflow

**Solution:** Use `/meta-analysis` workflow invocation (see Step 3 above)

---

### Issue: "Archive script can't find initiative"

**Symptom:**

```text
Initiative not found: initiative-name
```

**Solution:** Use one of the supported input formats:

```bash
# Just the name (most common)
task archive:initiative NAME=2025-10-20-feature-name

# With .md extension
task archive:initiative NAME=2025-10-20-feature-name.md

# Full relative path
task archive:initiative NAME=docs/initiatives/active/2025-10-20-feature-name.md
```

---

### Issue: "Should I skip meta-analysis for small changes?"

**Answer:** **NO.** Meta-analysis is MANDATORY for every session, regardless of size. Even small sessions need:

- Context preservation for next session
- Protocol compliance tracking
- Consistent session history

If truly trivial (e.g., fixing a typo), document: "Routine maintenance, no significant changes."

---

## Anti-Patterns

### ❌ Don't: Skip Steps

**Bad:**

```text
✅ Commit changes
❌ Skip archive (initiative done but not archived)
❌ Skip meta-analysis (no session summary)
✅ Present summary
```

**Why it's bad:**

- Breaks cross-session continuity
- Violates protocol
- Loses context for future work

**Correct:** Execute ALL steps in order, every time.

---

### ❌ Don't: Present Summary Before Meta-Analysis

**Bad:**

```markdown
## Session Complete!
[Summary here]

(But meta-analysis not run yet, initiatives not archived)
```

**Why it's bad:**

- User thinks session is done
- Critical protocol steps skipped
- Future sessions lack context

**Correct:** Complete ALL protocol steps, THEN present summary.

---

### ❌ Don't: Run Python script for meta-analysis

**Bad:**

```bash
python scripts/meta_analysis.py  # Doesn't exist!
```

**Correct:**

```bash
# Invoke workflow via Windsurf IDE
/meta-analysis
```

---

## Automation Integration

### Pre-Commit Hooks

The following hooks validate protocol compliance:

- `check-workflow-tokens` - Ensures workflow files within budget
- `markdownlint` - Validates session summary format
- `validate-frontmatter` - Checks YAML frontmatter

**Never bypass with `--no-verify` for protocol violations.**

---

## References

**Workflows:**

- `.windsurf/workflows/work-session-protocol.md` - Full protocol definition
- `.windsurf/workflows/meta-analysis.md` - Meta-analysis orchestrator
- `.windsurf/workflows/extract-session.md` - Session data extraction
- `.windsurf/workflows/summarize-session.md` - Summary generation

**Rules:**

- `.windsurf/rules/00_agent_directives.md` - Section 8 (Session End Protocol)
- `.windsurf/rules/05_operational_protocols.md` - Operational guidelines

**Automation:**

- `scripts/file_ops.py` - Archive automation (via `task archive:initiative`)
- `docs/DOCUMENTATION_STRUCTURE.md` - Session summary template

---

**Last Updated:** 2025-10-20
**Version:** 1.0.0
**Maintainer:** Core Team
