---
created: "2025-10-18"
updated: "2025-10-21"
description: /work-routing - Routing decision logic for work orchestration
auto_execution_mode: 3
category: Sub-workflow
parent: work.md
complexity: 70
tokens: 1200
dependencies: [detect-context]
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Work Routing Logic

Determine which workflow to route to based on context detection.

**Called by:** `/work` (Stage 3)

## Confidence-Based Routing

| Confidence | Action |
|------------|--------|
| High (80%+) | Auto-route |
| Medium (30-79%) | Recommend |
| Low (<30%) | Prompt |

## Routes

| Signal | Route | Condition |
|--------|-------|-----------|
| Active initiative + unchecked tasks | `/implement` | No blockers |
| Test failures | Fix/`/implement` | Priority HIGH |
| Planning markers | `/plan` | Design/ADR needed |
| Completed initiative | `/archive-initiative` | Still in active/ |
| Clean slate | Prompt | No direction |

## Priority Order

1. **Blocking tests** → Fix
2. **Completed initiatives** → Archive
3. **Active initiative** → Resume
4. **Non-blocking tests** → Fix
5. **Planning** → Create plan
6. **Clean slate** → Prompt

**Overrides:** User explicit > Security > Broken build

## Context Loading

| Route | Scope | Files |
|-------|-------|-------|
| `/implement` (initiative) | initiative | Initiative + source + tests |
| `/implement` (tests) | module:tests | Tests + module |
| `/plan` | full | PROJECT_SUMMARY + initiatives + ADRs |
| `/archive-initiative` | initiative | Initiative only |

## Rules

❌ Never ask "what" if 80%+ confident
❌ Never ignore priority (tests before planning)
✅ Auto-route on high/medium confidence

## References

`work.md`, `detect-context.md`, `load-context.md`
