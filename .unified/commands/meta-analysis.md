---
title: "Meta-Analysis Workflow"
description: "Systematic session review with intelligent consolidation detection"
type: "command"
status: "active"

# Windsurf workflow metadata
windsurf:
  type: "workflow"
  category: "Analysis"
  complexity: "moderate"
  dependencies: ["extract-session", "summarize-session", "consolidate-summaries"]

# Cursor command metadata
cursor:
  pass_through: true

tags: ["analysis", "session", "summary", "consolidation"]

---

# Meta-Analysis Workflow

MANDATORY at session end. Creates LLM-agnostic summaries for cross-session continuity.

```typescript
update_plan({
  explanation: "📊 /meta-analysis",
  plan: [
    { step: "1. /work-session-protocol - Update meta-analysis protocol timestamp", status: "in_progress" },
    { step: "2. /extract-session - Gather session context", status: "pending" },
    { step: "3. /summarize-session - Generate session summary", status: "pending" },
    { step: "4. /update-docs - Review living documentation", status: "pending" },
    { step: "5. /commit - Record meta-analysis outputs", status: "pending" }
  ]
})
```

## Stage 1: Protocol Check

```bash
cat .windsurf/.last-meta-analysis 2>/dev/null || echo "NEVER"
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis
```

## Stage 2: Consolidation Detection

**RARE.** Only with 70%+ confidence of session continuation.

```bash
TODAY=$(date +"%Y-%m-%d")
ls -1 docs/archive/session-summaries/${TODAY}-*.md 2>/dev/null | wc -l
```

**Signals:** Same initiative (40%), Same files (25%), Time gap <1h (15%), Commit overlap (10%), User signal (10%)

**Threshold:** ≥70% + gap <2h → Call `/consolidate-summaries`, skip to Stage 5

## Stage 3: Extract and Summarize

**Call** `/extract-session` → `/summarize-session`

**Output:** `docs/archive/session-summaries/YYYY-MM-DD-HHMMSS-session-summary.md`

## Stage 4: Living Documentation

**Check for updates needed:**

- `docs/ARCHITECTURE.md` - Major architectural changes
- `docs/CONSTITUTION.md` - Process or standard changes
- `docs/DOCUMENTATION_STRUCTURE.md` - Documentation structure changes
- `README.md` - Project overview changes

**Update if:** Significant changes detected (new patterns, processes, or standards)

## Stage 5: Commit

**Commit all changes:**

```bash
git add .
git commit -m "docs: session summary and documentation updates

- Session summary: YYYY-MM-DD-HHMMSS
- Updated: [list of updated docs]
- Changes: [brief description]"
```

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files, complex operations, or memory-intensive tasks
- **Documentation Standards**: `/rules/03_documentation.mdc` - Apply when updating documentation and maintaining standards

## Workflow References

When this meta-analysis workflow is called:

1. **Load**: `/commands/meta-analysis.md`
2. **Execute**: Follow the analysis stages defined above
3. **Consolidate**: Check for session consolidation opportunities
4. **Summarize**: Extract and summarize session data
5. **Update**: Update living documentation as needed

## Integration

**Called By:**

- `/work` - Session end protocol
- User - Direct invocation for session analysis

**Calls:**

- `/extract-session` - Extract session data
- `/summarize-session` - Create session summary
- `/consolidate-summaries` - Consolidate multiple sessions (rare)

## Anti-Patterns

❌ **Don't:**

- Skip session summarization
- Ignore consolidation opportunities
- Skip living documentation updates
- Commit without proper message

✅ **Do:**

- Always create session summary
- Check for consolidation when appropriate
- Update living docs when significant changes
- Use proper commit messages

## Command Metadata

**File:** `meta-analysis.yaml`
**Type:** Command/Workflow
**Complexity:** Medium
**Estimated Tokens:** ~1,300
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Session analysis
- Summary generation
- Documentation updates
- Consolidation detection

**Dependencies:**

- /extract-session - Extract session data
- /summarize-session - Create session summary
- /consolidate-summaries - Consolidate multiple sessions
