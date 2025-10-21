---
created: "2025-10-18"
updated: "2025-10-21"
description: /work-session-protocol - Session end protocol and completion detection
auto_execution_mode: 3
category: Sub-workflow
parent: work.md
complexity: 75
tokens: 1100
dependencies: [archive-initiative, meta-analysis]
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Work Session End Protocol

Detect work completion and execute session end protocol.

**Called by:** `/work` (Stage 5)

## Completion Detection

**Trigger if ANY:**

1. Initiative Status = "Completed" or "✅"
2. All planned tasks complete
3. User signal: "wrap up", "end session", "done"

**NOT triggered:** Progress updates, questions, quick fixes, ongoing work

## Protocol

```typescript
update_plan({
  explanation: "🏁 Session end detected",
  plan: [
    { step: "5.1. /commit - Commit all", status: "in_progress" },
    { step: "5.2. /archive-initiative - Archive completed", status: "pending" },
    { step: "5.3. /meta-analysis - Execute", status: "pending" },
    { step: "5.4. /work-session-protocol - Verify exit criteria", status: "pending" }
  ]
})
```

### Stage 1: Commit All

```bash
git status --short
git add <files> && git commit -m "type(scope): description"
# Auto-fixes separately: style(scope): apply [tool] auto-fixes
```

### Stage 2: Archive Completed Initiatives

```bash
grep -l "Status.*Completed\|✅" docs/initiatives/active/*.md
/archive-initiative <name>  # CRITICAL: never skip
```

### Stage 3: Execute Meta-Analysis

**Correct:** `/meta-analysis`

**Manual fallback:**

```bash
git log --oneline --since="$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo '24h ago')"
# Create docs/archive/session-summaries/YYYY-MM-DD-*.md
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis
git add docs/archive/session-summaries/*.md .windsurf/.last-meta-analysis
git commit -m "docs(session): add YYYY-MM-DD session summary"
```

### Stage 4: Verify Exit Criteria

- [ ] All committed (git status clean)
- [ ] Tests passing (if code changes)
- [ ] Completed initiatives archived
- [ ] Meta-analysis executed
- [ ] Session summary created
- [ ] Living docs updated (if major)

```bash
git status --short  # Empty
ls -t docs/archive/session-summaries/*.md | head -1
task test:fast  # If code changes
```

### Stage 5: Completion Summary

**ONLY after all criteria met:**

```markdown
## ✅ Session Complete

### Summary
[2-3 sentences]

### Key Accomplishments
- [Item 1]
- [Item 2]

### Commits
[git log]

### Documentation
- Session: docs/archive/session-summaries/YYYY-MM-DD-*.md
- [Other]

### Next Steps
- [What next]
- [Blockers]

Ready for next session.
```

## Continue Working (NOT Session End)

**Progress update:**

```markdown
✅ [Done], 🔄 [Current], ⏳ [Remaining]. Continuing...
```

## Anti-Patterns

❌ Skip `/meta-analysis` → Breaks continuity
❌ Leave completed in active/ → Clutters
❌ Uncommitted at end → Work loss
❌ Confuse progress with session end

## References

`work.md`, `meta-analysis.md`, `archive-initiative.md`, `00_core_directives.md`
