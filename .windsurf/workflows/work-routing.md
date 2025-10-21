---
created: "2025-10-18"
updated: "2025-10-18"
description: /work-routing - Routing decision logic for work orchestration
auto_execution_mode: 3
category: Sub-workflow
parent: work.md
complexity: 70
tokens: 1705
dependencies:
  - detect-context
status: active
---

# Work Routing Logic

**Purpose:** Determine which workflow to route to based on context detection confidence and signals.

**Called By:** `/work` (Stage 3)

**Returns:** Routing decision with target workflow

---

## Confidence-Based Routing

| Confidence | Action | User Interaction |
|------------|--------|------------------|
| **High (80%+)** | Auto-route | Announce decision |
| **Medium (30-79%)** | Proceed with recommendation | State alternatives |
| **Low (<30%)** | Prompt user | List options |

### Common Routes

| Signal | Route | Condition |
|--------|-------|-----------|  
| Active initiative + unchecked tasks | `/implement` | No blockers |
| Test failures | Fix/`/implement` | Priority: HIGH |
| Planning markers | `/plan` | Design/ADR needed |
| Completed initiative | `/archive-initiative` | Still in active/ |
| Clean slate | Prompt | No clear direction |

---

## Decision Logic

**Priority Order:**
1. Blocking tests → Fix
2. Completed initiatives → Archive
3. Active initiative → Resume
4. Non-blocking tests → Fix
5. Planning → Create plan
6. Clean slate → Prompt

---

## Priority Rules

**Priority Order (highest to lowest):**

1. **Blocking Test Failures** → Fix immediately
2. **Completed Initiatives** → Archive before new work
3. **Active Initiative Continuation** → Resume in-progress work
4. **Non-Blocking Test Failures** → Fix when convenient
5. **Planning Work** → Create plans for new features
6. **Clean Slate** → Prompt user

**Override Conditions:**

- User explicit direction overrides all priorities
- Security issues override everything
- Broken build overrides everything except security

---

## Context Loading

| Route | Scope | Files |
|-------|-------|-------|
| `/implement` (initiative) | initiative | Initiative + source + tests |
| `/implement` (tests) | module:tests | Tests + module |
| `/plan` | full | PROJECT_SUMMARY + initiatives + ADRs |
| `/archive-initiative` | initiative | Initiative only |

---

## Rules

- ❌ Never ask "what to work on" if 80%+ confident
- ❌ Never ignore priority order (tests before planning)
- ✅ Auto-route on high/medium confidence
- ✅ Respect priority: security > tests > active work

---

## References

- Parent workflow: [work.md](./work.md)
- Context detection: [detect-context.md](./detect-context.md)
- Context loading: [load-context.md](./load-context.md)

---

**Version:** 1.0.0 (Extracted from work.md Phase 4 decomposition)
**Last Updated:** 2025-10-18
