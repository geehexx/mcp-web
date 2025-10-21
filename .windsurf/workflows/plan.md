---
created: "2025-10-17"
updated: "2025-10-21"
description: Research-driven comprehensive project planning
auto_execution_mode: 2
category: Planning
complexity: 70
tokens: 1500
dependencies: [research, generate-plan, load-context]
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Planning Workflow

Create robust, researched plans for features, initiatives, or complex changes.

**Chain:** `/plan` → `/research` → `/generate-plan` → `/implement`

## When to Use

✅ New feature, complex refactoring, architecture change, multi-session work (>4h), cross-cutting concerns, unclear requirements

❌ Simple bugs (<1h), docs updates, routine deps, following existing patterns

## Stage 1: Define Requirements

**Capture:** Restate request, ask ≤3 clarifying questions, document assumptions

**Success criteria (SMART):**

```markdown
- [ ] [Specific deliverable]
- [ ] [Measurable outcome]
- [ ] [Quality gate]
- [ ] [Documentation]

**Verification:** [How to confirm]
**Estimated:** [N-M hours]
```

## Stage 2: Research & Discovery

**Call `/research`:**

- Internal patterns (codebase, ADRs, rules)
- Web research (MANDATORY)
- Dependencies, security, performance
- Alternatives comparison
- Recommendation with sources

**Output:** Research summary

## Stage 3: Generate Implementation Plan

**Call `/generate-plan`:**

- Decompose into phases
- Break into tasks (<4h each)
- Dependency graph
- Risks + mitigations
- Out-of-scope
- Create initiative doc
- Create ADR if needed

**Output:** Initiative in `docs/initiatives/active/`, plan summary

## Stage 4: Review & Approval

**Present:** Phases, tasks, timeline, risks, alternatives, ADR (if any)

**User approves:** → Proceed to `/implement`
**User requests changes:** → Iterate
**User rejects:** → Document reasons, archive planning artifacts

## Integration

**Called by:** User, `/work`
**Calls:** `/research`, `/generate-plan`, `/implement`

## References

`research.md`, `generate-plan.md`, `implement.md`, `02_testing.md`
