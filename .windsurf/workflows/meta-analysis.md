---
created: "2025-10-17"
updated: "2025-10-21"
description: Systematic session review with intelligent consolidation detection
auto_execution_mode: 3
category: Analysis
complexity: 60
tokens: 1300
dependencies: [extract-session, summarize-session, consolidate-summaries]
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Meta-Analysis Workflow

MANDATORY at session end. Creates LLM-agnostic summaries for cross-session continuity.

```typescript
update_plan({
  explanation: "📊 /meta-analysis",
  plan: [
    { step: "1. Check protocol, update timestamp", status: "in_progress" },
    { step: "2. Check consolidation", status: "pending" },
    { step: "3. Extract and summarize", status: "pending" },
    { step: "4. Check living docs", status: "pending" },
    { step: "5. Commit", status: "pending" }
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

**Never:** Different initiatives, unrelated files, gap >2h, confidence <70%

## Stage 3: Extract Session

Call `/extract-session` → Git history, accomplishments, decisions, learnings, protocol compliance

## Stage 4: Generate Summary

Call `/summarize-session` → Template, validate, create `docs/archive/session-summaries/YYYY-MM-DD-*.md`

## Stage 5: Living Documentation

| Doc | Update ✅ | Skip ❌ |
|-----|----------|----------|
| PROJECT_SUMMARY | Major feature, milestone, ADR, initiative, metrics | Routine fixes, minor docs, tests |
| CHANGELOG | Release, breaking change, user feature, major bug | Internal, docs-only, WIP |

If triggers: Call `/update-docs`

## Stage 6: Commit

```bash
git add docs/archive/session-summaries/YYYY-MM-DD-*.md .windsurf/.last-meta-analysis
git commit -m "docs(session): add YYYY-MM-DD [focus] session summary

- Duration: ~Nh, Focus: [Primary]
- Key: [highlights]"
```

## References

`extract-session.md`, `summarize-session.md`, `update-docs.md`, `10_session_protocols.md`
