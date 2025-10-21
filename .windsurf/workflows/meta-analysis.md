---
created: "2025-10-17"
updated: "2025-10-19"
description: Systematic session review with intelligent consolidation detection
auto_execution_mode: 3
category: Analysis
complexity: 60
tokens: 1900
dependencies:
  - extract-session
  - summarize-session
  - consolidate-summaries
status: active
version: 2.0.0
---

# Meta-Analysis Workflow

**Purpose:** Systematically analyze AI agent sessions to identify improvement opportunities and create consistent, comprehensive session summaries.

**When to Use:** MANDATORY at the end of every work session (part of Session End Protocol)

**Philosophy:** Create LLM-agnostic session summaries that enable cross-session continuity and capture learnings.

---

## Workflow Execution

**Task plan:**
```typescript
update_plan({
  explanation: "📊 Starting /meta-analysis",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "in_progress" },
    { step: "2. /meta-analysis - Check for consolidation", status: "pending" },
    { step: "3. /meta-analysis - Extract and summarize session", status: "pending" },
    { step: "4. /meta-analysis - Check living docs", status: "pending" },
    { step: "5. /meta-analysis - Commit summary", status: "pending" }
  ]
})
```

---

## Stage 1: Protocol Check

```bash
# Check last execution and update timestamp
cat .windsurf/.last-meta-analysis 2>/dev/null || echo "NEVER"
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis
```

**Purpose:** Track protocol adherence, detect violations (warn if >24h)

---

## Stage 2: Consolidation Detection

**RARE:** Only consolidate with 70%+ confidence of session continuation.

```bash
TODAY=$(date +"%Y-%m-%d")
ls -1 docs/archive/session-summaries/${TODAY}-*.md 2>/dev/null | wc -l
```

### Decision Logic

| Signal (Weight) | Check |
|-----------------|-------|
| Same initiative (40%) | Explicit mention in conversation |
| Same files (25%) | >50% overlap in modified files |
| Time gap (15%) | <1h |
| Commit messages (10%) | Semantic keyword overlap |
| User signal (10%) | "continue" mentioned |

**Threshold: 70%+ → Consolidate | <70% → Separate**

| Condition | Action |
|-----------|--------|
| Confidence ≥70% + gap <2h | Call `/consolidate-summaries`, skip to Stage 5 |
| Otherwise | Proceed to Stage 3 (new summary) |

**Never consolidate:** Different initiatives, unrelated files, gap >2h, confidence <70%

---

## Stage 3: Extract Session Data

Call `/extract-session` → Analyzes git history, extracts accomplishments/decisions/learnings, checks protocol compliance.

**See:** `.windsurf/workflows/extract-session.md`

---

## Stage 4: Generate Summary

Call `/summarize-session` → Uses template, validates, creates `docs/archive/session-summaries/YYYY-MM-DD-description.md`

**See:** `.windsurf/workflows/summarize-session.md`

---

## Stage 5: Living Documentation

| Document | Update Triggers ✅ | Skip ❌ |
|----------|-------------------|----------|
| **PROJECT_SUMMARY** | Major feature, milestone, architecture change, ADR, initiative status, metrics shift, dependencies | Routine fixes, minor docs, refactoring, test additions |
| **CHANGELOG** | Release prep, breaking changes, user features, major bugs, dependency updates | Internal work, docs-only, WIP features |

**If triggers met:** Call `/update-docs` (see `.windsurf/workflows/update-docs.md`)

---

## Stage 6: Commit

```bash
git add docs/archive/session-summaries/YYYY-MM-DD-*.md .windsurf/.last-meta-analysis
git commit -m "docs(session): add YYYY-MM-DD [focus] session summary

- Duration: ~N hours, Focus: [Primary focus]
- Key accomplishments: [highlights]"
```

---

## Success & Integration

**Complete when:** Summary created, timestamp updated, living docs checked/updated, all committed.

**Troubleshooting:**
- Update PROJECT_SUMMARY? → Check Stage 5 triggers (when in doubt, update)
- Protocol violation? → Document in summary, propose workflow improvements
- No learnings? → Write "No significant insights (routine work)"

**Called by:** `/work` (MANDATORY at session end) | User (direct)

**Calls:** `/extract-session`, `/summarize-session`, `/consolidate-summaries`, `/update-docs`

**See:** `.windsurf/workflows/extract-session.md`, `summarize-session.md`, `update-docs.md`, `.windsurf/rules/10_session_protocols.md`
