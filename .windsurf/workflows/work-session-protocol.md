---
created: "2025-10-18"
updated: "2025-10-21"
description: /work-session-protocol - Session end protocol and completion detection
auto_execution_mode: 3
category: Sub-workflow
parent: work.md
complexity: 75
tokens: 1550
dependencies:
  - archive-initiative
  - meta-analysis
status: active
---

# Work Session End Protocol

**Purpose:** Detect work completion and execute proper session end protocol.

**Called By:** `/work` (Stage 5)

**Triggers:** Initiative completion, all tasks done, or user signals end

---

## Completion Detection

### Trigger If ANY of:

1. **Initiative Completion:** Status = "Completed" or "✅"
2. **All Tasks Done:** All planned tasks complete
3. **User Signal:** "wrap up", "end session", "that's all"

### NOT Triggered By:

❌ Progress updates, questions, quick fixes, ongoing implementation

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "🏁 Session end detected. Executing protocol.",
  plan: [
    { step: "5.1. /commit - Commit all changes", status: "in_progress" },
    { step: "5.2. /archive-initiative - Archive completed initiatives", status: "pending" },
    { step: "5.3. /meta-analysis - Execute session meta-analysis", status: "pending" },
    { step: "5.4. /work-session-protocol - Verify exit criteria", status: "pending" }
  ]
})
```

---

## Stage 2: Commit All Changes

### Check & Commit

```bash
git status --short

# Commit working changes
git add <modified files>
git commit -m "type(scope): description"

# Commit auto-fixes separately
git add <auto-fix files>
git commit -m "style(scope): apply [tool] auto-fixes"
```

**Types:** feat, fix, docs, test, refactor, security, chore

---

## Stage 3: Archive Completed Initiatives

### Find & Archive

```bash
# Find completed initiatives
grep -l "Status.*Completed\|Status.*✅" docs/initiatives/active/*.md

# Archive each (CRITICAL: never skip)
/archive-initiative <initiative-name>
```

**What it does:** Moves to `completed/`, updates metadata, updates PROJECT_SUMMARY.md

---

## Stage 4: Execute Meta-Analysis

### Invoke Meta-Analysis Workflow

**Correct:**

```markdown
/meta-analysis
```

**NEVER:**

```bash
python scripts/meta_analysis.py  # Doesn't exist!
```

### Manual Fallback (If Needed)

```bash
# Extract commits
git log --oneline --since="$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo '24 hours ago')"

# Create summary: docs/archive/session-summaries/YYYY-MM-DD-name.md
# Use template from docs/DOCUMENTATION_STRUCTURE.md

# Update timestamp
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis

# Commit
git add docs/archive/session-summaries/*.md .windsurf/.last-meta-analysis
git commit -m "docs(session): add YYYY-MM-DD session summary"
```

**Creates:**
- Session summary
- Workflow improvements
- Cross-session continuity
- Lessons learned

**Why mandatory:** Enables future context detection, documents decisions/patterns

---

## Stage 5: Verify Exit Criteria

### Checklist

```markdown
- [ ] All changes committed (git status clean)
- [ ] All tests passing (if code changes)
- [ ] Completed initiatives archived
- [ ] Meta-analysis executed
- [ ] Session summary created
- [ ] Living docs updated (if major changes)
```

### Living Documentation Check

**Update if:**
- Major features completed
- Milestones reached
- ADRs created
- Architecture changes

**Skip if:**
- Routine fixes, internal refactoring, WIP

### Final Validation

```bash
# Verify clean
git status --short  # Should be empty

# Verify summary exists
ls -t docs/archive/session-summaries/*.md | head -1

# If code changes: tests pass
task test:fast
```

---

## Stage 6: Present Completion Summary

**ONLY after all criteria met:**

```markdown
## ✅ Session Complete

### Summary
[2-3 sentences on accomplishments]

### Key Accomplishments
- Accomplishment 1
- Accomplishment 2
- Accomplishment 3

### Commits Created
[git log output]

### Documentation Updated
- Session summary: docs/archive/session-summaries/YYYY-MM-DD-name.md
- [Other docs]

### Initiative Progress
- Initiative X: [status]
- Overall: X% → Y%

### Next Steps
- [What to work on next]
- [Blockers/dependencies]

Ready for next session.
```

---

## Continue Working (Protocol NOT Triggered)

**If completion NOT met:**

- Brief progress update
- Continue next task
- **NO** "completion summary"
- **NO** "shall I continue?" (unless blocked)

**Progress Format:**

```markdown
## Progress Update

✅ Completed: [done]
🔄 In Progress: [current]
⏳ Remaining: [left]

Continuing...
```

---

## Anti-Patterns

### ❌ CRITICAL FAILURES

| Never Do | Why |
|----------|-----|
| Skip `/meta-analysis` | Breaks continuity |
| Leave completed initiatives in active/ | Clutters context |
| Uncommitted changes at end | Risks work loss |
| Skip living docs updates | Documentation drift |

### ❌ Don't Confuse Updates with Session End

**Progress (Mid-Session):**

```markdown
✅ Task 1 done, 🔄 Task 2, ⏳ Task 3. Continuing...
```

**Session End (Triggered):**

```markdown
✅ Session Complete [full summary with protocol]
```

---

## Success Metrics

- Session end protocol: 100% execution when triggered
- Meta-analysis: 100% (never skip)
- Initiative archival: 100% (when complete)
- Protocol time: <10 minutes

---

## References

- [work.md](./work.md) - Parent workflow
- [meta-analysis.md](./meta-analysis.md)
- [archive-initiative.md](./archive-initiative.md)
- [00_core_directives.md](../rules/00_core_directives.md)

---

**Version:** 1.0.0
**Last Updated:** 2025-10-21
