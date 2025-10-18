---
created: "2025-10-18"
updated: "2025-10-18"
description: /work-session-protocol - Session end protocol and completion detection
auto_execution_mode: 3
category: Sub-workflow
parent: work.md
complexity: 75
tokens: 1372
dependencies:
  - archive-initiative
  - meta-analysis
status: active
---

# Work Session End Protocol

**Purpose:** Detect when work is complete and execute proper session end protocol.

**Called By:** `/work` (Stage 5)

**Triggers:** Initiative completion, all planned tasks done, or user signals end

---

## Overview

The Session End Protocol ensures proper closure of work sessions with full documentation, archival, and meta-analysis. It is **MANDATORY** when triggered—never skip steps.

**Protocol Phases:**

1. Detect completion triggers
2. Commit all changes
3. Archive completed initiatives
4. Execute meta-analysis
5. Verify exit criteria

---

## Phase 1: Detect Completion Triggers

### Trigger Detection

Run these checks to determine if protocol should execute:

```bash
# Check if initiative marked complete
grep -l "Status.*Completed\|Status.*✅" docs/initiatives/active/*.md

# Check git status
git status --short

# Check if all planned tasks done (review task list state)
```

### Trigger Conditions

**Execute Session End Protocol if ANY of:**

1. **Initiative Completion:** Initiative marked "Completed" or "✅" (found in grep above)
2. **All Tasks Done:** All planned tasks for routed workflow are complete
3. **User Signal:** User explicitly says "that's all", "let's wrap up", "end session", etc.

### NOT Triggered By

❌ Mid-work progress updates
❌ Answering questions
❌ Quick fixes or patches
❌ Ongoing implementation (unless initiative complete)

---

## Phase 2: Commit All Changes

### 2.1 Check Working Tree

```bash
git status --short
```

**If unstaged or staged changes exist:**

### 2.2 Commit Working Changes

```bash
# Stage modified files
git add <modified files>

# Commit with conventional commit message
git commit -m "type(scope): description

- Detail 1
- Detail 2"
```

**Commit Types:** feat, fix, docs, test, refactor, security, chore

### 2.3 Commit Auto-Fixes Separately

**If linters/formatters made changes:**

```bash
git add <auto-fix files>
git commit -m "style(scope): apply [tool] auto-fixes"
```

**Examples:**

- `style(docs): apply markdownlint auto-fixes`
- `style(workflows): apply markdownlint auto-fixes`

---

## Phase 3: Archive Completed Initiatives

### 3.1 Find Completed Initiatives

```bash
# Get list of completed initiatives from Phase 1 detection
grep -l "Status.*Completed\|Status.*✅" docs/initiatives/active/*md
```

### 3.2 Archive Each Initiative

**For each completed initiative:**

```bash
/archive-initiative <initiative-name>
```

**CRITICAL:** Do NOT skip this step. Completed initiatives must be archived before session end.

**What the workflow does:**

- Moves initiative from `active/` to `completed/`
- Updates initiative with completion metadata
- Creates archive entry
- Updates PROJECT_SUMMARY.md (if major)

---

## Phase 4: Execute Meta-Analysis

### 4.1 Run Meta-Analysis Workflow

```bash
/meta-analysis
```

**This workflow creates:**

- Session summary in `docs/archive/session-summaries/YYYY-MM-DD-description.md`
- Workflow improvement recommendations
- Cross-session continuity documentation
- Lessons learned capture

**Why mandatory:**

- Enables context detection in future sessions
- Documents decisions and rationale
- Identifies patterns and improvements
- Maintains project knowledge continuity

### 4.2 What Gets Documented

**Session summary includes:**

- Work accomplished (specific changes)
- Decisions made (technical, architectural)
- Files modified (with context)
- Commits created (with hashes)
- Learnings (technical insights)
- Unresolved issues (blockers, TODOs)
- Next steps (continuation points)

---

## Phase 5: Verify Exit Criteria

### 5.1 Exit Criteria Checklist

```markdown
- [ ] All changes committed (git status clean)
- [ ] All tests passing (if code changes made)
- [ ] Completed initiatives archived
- [ ] Meta-analysis executed
- [ ] Session summary created
- [ ] Living documentation updated (if major changes)
```

### 5.2 Living Documentation Check

**Update if ANY of these apply:**

**PROJECT_SUMMARY.md:**

- Major features completed
- Milestones reached
- ADRs created
- Initiative status changed (completed/started)
- Architecture changes

**CHANGELOG.md:**

- Preparing release
- Breaking changes
- New user-facing features

**Skip updates if:**

- Routine bug fixes
- Internal refactoring
- Work-in-progress (not ready for users)

### 5.3 Final Validation

**Before presenting completion summary:**

```bash
# Verify git clean
git status --short
# Output should be empty

# Verify session summary exists
ls -t docs/archive/session-summaries/*.md | head -1
# Should show today's summary

# If code changes: verify tests pass
task test:fast
# Should show all passing
```

---

## Phase 6: Present Completion Summary

**ONLY after all exit criteria met, present:**

```markdown
## ✅ Session Complete

### Summary

[2-3 sentences on what was accomplished]

### Key Accomplishments

- Accomplishment 1 (with specifics)
- Accomplishment 2 (with specifics)
- Accomplishment 3 (with specifics)

### Commits Created

[bash]
<git log output showing commits>
[/bash]

### Documentation Updated

- Session summary: docs/archive/session-summaries/YYYY-MM-DD-name.md
- [Any other docs updated]

### Initiative Progress

- Initiative X: [status update]
- Overall progress: X% → Y%

### Next Steps

- [What to work on next session]
- [Any blockers or dependencies]

Ready for next session.
```

---

## Continue Working (If Protocol NOT Triggered)

**If completion triggers NOT met:**

- Provide brief progress update
- Continue with next task/phase
- Do NOT present "completion summary"
- Do NOT ask "shall I continue?" unless blocked
- Keep working until actual completion or user signals end

**Progress Update Format:**

```markdown
## Progress Update

✅ Completed: [what's done]
🔄 In Progress: [current task]
⏳ Remaining: [what's left]

Continuing with [next task]...
```

---

## Anti-Patterns

### ❌ CRITICAL FAILURES

**Never Do This:**

1. **Presenting final summary without `/meta-analysis`**
   - Breaks cross-session continuity
   - Loses valuable context

2. **Leaving completed initiatives in active/ directory**
   - Clutters active work
   - Confuses context detection

3. **Uncommitted changes at session end**
   - Risks losing work
   - Creates merge conflicts

4. **Skipping living documentation updates**
   - Documentation drifts from reality
   - Users miss important changes

### ❌ Don't: Confuse Progress Updates with Session End

**Progress Update (Mid-Session):**

```markdown
✅ Task 1 done
🔄 Working on Task 2
⏳ Task 3 pending

Continuing...
```

**Session End (Triggers Met):**

```markdown
✅ Session Complete

[Full completion summary with all protocol steps]
```

---

## Success Metrics

**Protocol Execution:**

- Session end protocol: 100% execution when triggered
- Meta-analysis creation: 100% (never skip)
- Initiative archival: 100% (when complete)
- Documentation updates: 100% (when applicable)

**Timing:**

- Protocol execution: <5 minutes
- Meta-analysis: <3 minutes
- Total session end: <10 minutes

---

## References

- Parent workflow: [work.md](./work.md)
- Meta-analysis workflow: [meta-analysis.md](./meta-analysis.md)
- Archive workflow: [archive-initiative.md](./archive-initiative.md)
- Agent directives: [00_agent_directives.md](../.windsurf/rules/00_agent_directives.md) (Section 1.8)

---

**Version:** 1.0.0 (Extracted from work.md Phase 4 decomposition)
**Last Updated:** 2025-10-18
