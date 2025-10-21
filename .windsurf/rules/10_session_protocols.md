---
trigger: model_decision
description: Apply at session end when completing work or managing work transitions
---

# Session Protocols and Progress Communication

## Session End Protocol

**TRIGGERS:** This protocol MUST be executed when ANY of the following occur:

1. **User says session is ending** ("that's all for now", "let's wrap up", etc.)
2. **Initiative marked "Completed" or "✅"** in status field
3. **All planned work for current request is done** (no more tasks to execute)
4. **User explicitly requests summary** of completed work

**NOT triggered by:**

- Mid-work progress updates
- Answering questions
- Quick fixes or patches
- Ongoing implementation (unless initiative complete)

### 1.1 Mandatory Steps

**Execute in order:**

1. **Commit all changes first:**
   - Run `git status` to check for unstaged changes
   - Commit working changes with proper message
   - If auto-fixes present, commit separately: `style(scope): apply [tool] auto-fixes`

2. **Archive completed initiatives:** Check `docs/initiatives/active/` for status "Completed" or "✅"
   - If found, MUST call `/archive-initiative` workflow for each
   - Do NOT skip - this is a quality gate

3. **Run meta-analysis:** MUST call `/meta-analysis` workflow
   - Creates session summary for cross-session continuity
   - Identifies workflow/rule improvements
   - This is NOT optional

4. **Update living documentation:** Check if PROJECT_SUMMARY or CHANGELOG need updates
   - Update PROJECT_SUMMARY.md if: major features completed, milestones reached, ADRs created, initiative status changed
   - Update CHANGELOG.md if: preparing release, breaking changes, new user-facing features
   - See `/meta-analysis` workflow Stage 6 for detailed triggers
   - Skip if: routine bug fixes, internal refactoring, work-in-progress

5. **Verify exit criteria:**
   - All changes committed (including auto-fixes and documentation updates)
   - Tests passing (if code changes made)
   - Session summary created in `docs/archive/session-summaries/`
   - Living documentation current (PROJECT_SUMMARY, CHANGELOG checked)

### 1.2 Critical Violations

**Never do these:**

- ❌ Never present "work complete" summary without running full protocol
- ❌ Never mark initiative as complete without archiving it
- ❌ Never leave unstaged changes when presenting completion summary
- ❌ The session end protocol is NOT optional when initiative completes

### 1.3 References

- Detailed protocol: [work-session-protocol.md](../workflows/work-session-protocol.md)
- Meta-analysis workflow: [meta-analysis.md](../workflows/meta-analysis.md)
- Archive workflow: [archive-initiative.md](../workflows/archive-initiative.md)

---

## Progress Communication

Strategy

### 2.1 During Active Work (NOT at session end)

- Provide brief progress updates every 5-10 minutes of work
- No approval needed for routine changes (formatting, type hints, docs)
- Continue working autonomously unless blocked or uncertain

**Progress Update Format:**

```markdown
## Progress Update

✅ Completed: [what's done]
🔄 In Progress: [current task]
⏳ Remaining: [what's left]

Continuing with [next task]...
```

### 2.2 When to Pause and Ask for Direction

**Pause and ask when:**

- Before major architectural changes (new patterns, breaking changes)
- When multiple valid approaches exist (user preference needed)
- If blocked by missing requirements or unclear specifications
- After discovering unexpected complexity (scope change needed)

**Don't pause for:**

- Routine implementation decisions
- Formatting or style choices
- Minor refactoring
- Documentation updates

### 2.3 Communication Anti-Patterns

**DO NOT confuse progress updates with session end:**

- ❌ DON'T present "completion summary" mid-session
- ❌ DON'T ask "shall I continue?" unless blocked
- ✅ DO keep working until initiative/request is complete OR user signals session end
- ✅ DO run Session End Protocol (Section 1) when work is actually complete

---

## Workflow Invocation

**Critical:** Workflows are NOT Python scripts

- ✅ Invoke via workflow name: `/meta-analysis`
- ❌ Never: `python scripts/meta_analysis.py`
- See full details in operational protocols

---

## Rule Metadata

**File:** `10_session_protocols.md`
**Trigger:** model_decision
**Estimated Tokens:** ~2,000
**Last Updated:** 2025-10-21
**Status:** Active

**Can be @mentioned:** Yes (hybrid loading)

**Topics Covered:**

- Session end protocol
- Progress communication
- Workflow invocation
- Exit criteria

**Workflow References:**

- /work-session-protocol - Session end
- /meta-analysis - Session summary

**Dependencies:**

- Source: 05_operational_protocols.md

**Changelog:**

- 2025-10-21: Created from 05_operational_protocols.md
