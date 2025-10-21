---
created: "2025-10-17"
updated: "2025-10-21"
description: Generate structured implementation plan from research
auto_execution_mode: 3
category: Planning
complexity: 60
tokens: 1950
dependencies:
  - research
status: active
---

# Generate Plan Workflow

**Purpose:** Transform research into concrete implementation plan with phases, tasks, and timelines.

**Invocation:** Called by `/plan` (Stage 3)

**Input:** Research summary from `/research`

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "🔄 Starting /generate-plan workflow",
  plan: [
    { step: "1. /generate-plan - Define objectives and success criteria", status: "in_progress" },
    { step: "2. /generate-plan - Decompose into phases and tasks", status: "pending" },
    { step: "3. /generate-plan - Estimate effort and identify risks", status: "pending" },
    { step: "4. /generate-plan - Generate and validate initiative document", status: "pending" }
  ]
})
```

---

## Stage 2: Define Objectives & Success Criteria

### Objectives

```markdown
## Objective
[One-sentence description of what will be achieved]

**User Need:** [Original request]
**Technical Approach:** [Implementation based on research]
```

### Success Criteria

```markdown
## Success Criteria

- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Quality gate: tests, coverage, security]
- [ ] [Documentation requirement]

**Verification:** [How to confirm completion]
**Estimated Effort:** [N-M hours based on task breakdown]
```

**Update plan:**

```typescript
update_plan({
  explanation: "Objectives defined, decomposing into phases",
  plan: [
    { step: "1. /generate-plan - Define objectives and success criteria", status: "completed" },
    { step: "2. /generate-plan - Decompose into phases and tasks", status: "in_progress" },
    // ...
  ]
})
```

---

## Stage 3: Phase Decomposition & Task Breakdown

### Phase Pattern

**Standard decomposition:**
- Phase 1: Core/foundation (minimal viable)
- Phase 2: Enhancement (key features)
- Phase 3: Integration (apply everywhere)
- Phase 4: Polish (docs, review, deploy)

### Phase Template

```markdown
### Phase N: [Name] (N hours)

**Goal:** [What this phase achieves]

**Tasks:**
1. [Concrete task 1] (<4h)
2. [Concrete task 2] (<4h)
3. [Concrete task 3] (<4h)

**Exit Criteria:** [How to know phase is complete]
**Dependencies:** [What must complete first]
```

### Dependencies & Timeline

```markdown
## Dependencies

Phase 1 → Phase 2 → Phase 3 → Phase 4

**Parallel Work:**
- Phase 2 + 3 can overlap after Phase 1
- Documentation starts during Phase 3

**Timeline:**
- Phase 1: Session 1 (4h)
- Phase 2: Sessions 1-2 (3h)
- Phase 3: Session 2 (2h)
- Phase 4: Sessions 2-3 (2h)

**Total:** 11h across 2-3 sessions
**Buffer:** +20-30% for unknowns
```

**Update plan:**

```typescript
update_plan({
  explanation: "Phases defined, estimating effort and risks",
  plan: [
    { step: "2. /generate-plan - Decompose into phases and tasks", status: "completed" },
    { step: "3. /generate-plan - Estimate effort and identify risks", status: "in_progress" },
    // ...
  ]
})
```

---

## Stage 4: Effort Estimation & Risk Assessment

### Effort Estimation

| Task | Estimated Effort |
|------|-----------------|
| [Task 1] | [N] hours |
| [Task 2] | [N] hours |
| **Total** | **[N-M] hours** |

### Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Prevention/mitigation] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Prevention/mitigation] |

**Risk categories:** Technical, dependency, timeline, security

**Update plan:**

```typescript
update_plan({
  explanation: "Effort estimated, risks identified, generating document",
  plan: [
    { step: "3. /generate-plan - Estimate effort and identify risks", status: "completed" },
    { step: "4. /generate-plan - Generate and validate initiative document", status: "in_progress" }
  ]
})
```

---

## Stage 5: Document Generation

### Initiative File

**Filename:** `docs/initiatives/active/YYYY-MM-DD-descriptive-name.md`

**Template:**

```markdown
# Initiative: [Title]

**Status:** Active
**Created:** YYYY-MM-DD
**Target Completion:** YYYY-MM-DD
**Owner:** @agent
**Priority:** [High/Medium/Low]
**Estimated Effort:** [N hours]

---

## Objective

[From Stage 2]

---

## Success Criteria

[From Stage 2]

---

## Research Summary

**Approach:** [Recommended approach]

**Key Findings:**
- [Finding 1]
- [Finding 2]

**Libraries/Tools:**
- [Library] - [Purpose]

**References:**
- [URL] - [Description]

---

## Implementation Plan

[All phases from Stage 3]

---

## Dependencies

[From Stage 3]

---

## Risks & Mitigation

[From Stage 4]

**Out of Scope:**
[Explicitly state what's not included]

---

## ADRs

- [ ] [ADR-XXXX]: [Decision title if architectural]

**ADR Required:** [Yes/No - explain why]

---

## Related Documentation

- [File 1] - [Status: needs update/reference]
- [File 2] - [Status: needs creation]

---

## Updates

### YYYY-MM-DD (Creation)
Initiative created. Research complete. Ready for Phase 1.
```

### Validation Checklist

- [ ] Objective clear and concise
- [ ] Success criteria measurable
- [ ] Tasks sized <4h each
- [ ] Dependencies identified
- [ ] Risks assessed with mitigations
- [ ] Out of scope stated
- [ ] Estimated effort realistic
- [ ] Target completion reasonable

**Update plan:**

```typescript
update_plan({
  explanation: "Initiative document generated and validated",
  plan: [
    { step: "4. /generate-plan - Generate and validate initiative document", status: "completed" }
  ]
})
```

---

## Quality Standards

### Good Plan ✅

| Characteristic | Description |
|----------------|-------------|
| **Actionable** | Concrete tasks with clear acceptance criteria, realistic estimates |
| **Complete** | All phases covered, dependencies identified, risks with mitigations, documentation plan |
| **Maintainable** | Initiative file is source of truth, updates section for tracking, related docs listed |

### Poor Plan ❌

| Issue | Example | Fix |
|-------|---------|-----|
| **Vague** | "Implement feature" | Break into specific tasks |
| **Unrealistic** | 20-hour single task | Split into <4h tasks |
| **Incomplete** | No doc plan, missing deps, unclear criteria | Add all required sections |

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Create mega-plans (50h, 20 phases) | Split into 2-3 smaller initiatives |
| Ignore risks ("Everything will work") | Identify 3-5 realistic risks with mitigations |
| Skip documentation planning | List exact docs to update per phase |

---

## Integration

**Called By:** `/plan` - After research complete (Stage 3+)

**Input:**
- Research summary with recommendations
- User requirements
- Success criteria

**Output:**
- Initiative file in `docs/initiatives/active/`
- ADR (if architectural decision)
- Plan summary for user approval

**Calls:** `/new-adr` - If architectural decision needed

**Print exit:**

```markdown
✅ **Completed /generate-plan:** Implementation roadmap created with [N] phases and [M] tasks
```

---

## References

- `docs/DOCUMENTATION_STRUCTURE.md` - Initiative format
- `.windsurf/workflows/new-adr.md` - ADR creation
- `.windsurf/workflows/research.md` - Research input
