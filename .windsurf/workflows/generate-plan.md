---
created: "2025-10-17"
updated: "2025-10-21"
description: Generate structured implementation plan from research
auto_execution_mode: 3
category: Planning
complexity: 60
tokens: 2150
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
    { step: "1. /generate-plan - Load context and analyze requirements", status: "in_progress" },
    { step: "2. /generate-plan - Identify components and dependencies", status: "pending" },
    { step: "3. /generate-plan - Decompose work into phases", status: "pending" },
    { step: "4. /generate-plan - Break phases into tasks", status: "pending" },
    { step: "5. /generate-plan - Estimate effort", status: "pending" },
    { step: "6. /generate-plan - Identify risks", status: "pending" },
    { step: "7. /generate-plan - Define success criteria", status: "pending" },
    { step: "8. /generate-plan - Generate initiative document", status: "pending" },
    { step: "9. /generate-plan - Validate plan", status: "pending" }
  ]
})
```

---

## Stage 2: Define Objectives

### 2.1 Restate Requirements

**From user request and research:**

```markdown
## Objective

[One-sentence description]

**User Need:** [Original request]
**Technical Approach:** [Implementation approach from research]
```

### 2.2 Define Success Criteria

**SMART criteria:**

```markdown
## Success Criteria

- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Quality gate: tests, coverage, security]
- [ ] [Documentation requirement]
- [ ] [Review requirement]

**Verification:** [How to confirm completion]
**Estimated Effort:** [N-M hours]
```

---

## Stage 3: Phase Decomposition

### 3.1 Identify Major Milestones

**Break work into phases:**

- **Phase 1:** Core/foundation (minimal viable)
- **Phase 2:** Enhancement (key features)
- **Phase 3:** Integration (apply everywhere)
- **Phase 4:** Polish (docs, review, deploy)

### 3.2 Define Each Phase

**Template per phase:**

```markdown
### Phase N: [Name] (N hours)

**Goal:** [What this achieves]

**Tasks:**
1. [Concrete task 1] - [Est: N hours]
   - [Sub-task if needed]
2. [Concrete task 2] - [Est: N hours]
3. [Concrete task 3] - [Est: N hours]

**Exit Criteria:** [How to know phase complete]
**Dependencies:** [Prerequisites]
```

**Task sizing guidelines:**

- Each task: <4 hours
- Clear deliverables per phase
- Sequential build-up
- Each phase: 4-12 hours max

---

## Stage 4: Task Breakdown

### 4.1 Identify Dependencies

```markdown
## Dependencies

Phase 1 → Phase 2
       ↘
        → Phase 3 → Phase 4

**Parallel Work:**
- Phases 2+3 can overlap after Phase 1

**Blockers:**
- [External dependencies]
```

### 4.2 Estimate Timeline

```markdown
**Timeline:**
- Phase 1: Session 1 (4h)
- Phase 2: Sessions 1-2 (3h)
- Phase 3: Session 2 (2h)
- Phase 4: Sessions 2-3 (2h)

**Total:** 11 hours across 2-3 sessions
**Buffer:** +20-30% for unknowns
```

---

## Stage 5: Effort Estimation

### 5.1 Estimate Effort

| Task | Estimated Effort |
|------|-----------------|
| [Task 1] | [N] hours |
| [Task 2] | [N] hours |
| **Total** | **[N-M] hours** |

---

## Stage 6: Risk Assessment

### 6.1 Identify Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Prevention/mitigation] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Prevention/mitigation] |

**Common categories:**

- Technical risks
- Dependency risks
- Timeline risks
- Security risks

---

## Stage 7: Document Generation

### 7.1 Generate Initiative File

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

[From Stage 2.1]

---

## Success Criteria

[From Stage 2.2]

---

## Research Summary

**Approach:** [Recommended approach]

**Key Findings:**
- [Finding 1]
- [Finding 2]

**Libraries/Tools:**
- [Library 1] - [Purpose]

**References:**
- [URL 1] - [Description]

---

## Implementation Plan

[All phases from Stage 3.2]

---

## Dependencies

[From Stage 4.1]

---

## Risks & Mitigation

[From Stage 6.1]

**Out of Scope:**
[Explicitly state what's not included]

---

## ADRs

- [ ] [ADR-XXXX]: [Decision if architectural]

**ADR Required:** [Yes/No - explain]

---

## Related Documentation

- [File 1] - [Status: needs update/reference]
- [File 2] - [Status: needs creation]

---

## Updates

### YYYY-MM-DD (Creation)
Initiative created. Research complete. Ready for Phase 1.

[Future updates added here as work progresses]
```

### 7.2 Validate Initiative

**Checklist:**

- [ ] Objective clear and concise
- [ ] Success criteria measurable
- [ ] Tasks sized appropriately (<4h each)
- [ ] Dependencies identified
- [ ] Risks assessed with mitigations
- [ ] Out of scope explicitly stated
- [ ] Effort estimate realistic
- [ ] Target completion reasonable

---

## Stage 8: Plan Validation

### 8.1 Validate Structure

**Final checks:**

- [ ] All tasks have completion criteria
- [ ] Dependencies mapped
- [ ] No task >4 hours
- [ ] Documentation plan included
- [ ] ADR decision documented

**Print workflow exit:**

```markdown
✅ **Completed /generate-plan:** Roadmap created with [N] phases and [M] tasks
```

---

## Quality Standards

### Good Plan Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Actionable** | Concrete tasks, clear acceptance criteria, realistic estimates |
| **Complete** | All phases covered, dependencies identified, risks with mitigations |
| **Maintainable** | Single source of truth, update section, related docs listed |

### Poor Plan Signs

| Issue | Problem |
|-------|---------|
| **Vague** | "Implement feature" (too broad), no concrete tasks |
| **Unrealistic** | 20-hour tasks, no risk assessment, optimistic timeline |
| **Incomplete** | Missing docs plan, no dependency analysis, unclear criteria |

---

## Anti-Patterns

| Anti-Pattern | Bad | Good |
|--------------|-----|------|
| **Mega-Plans** | 50-hour initiative, 20 phases | Split into 2-3 smaller initiatives |
| **Ignore Risks** | "Everything will work" | Identify 3-5 realistic risks with mitigations |
| **Skip Docs** | "Document later" | List exact docs to update per phase |

---

## Integration

### Called By

- `/plan` - After research complete (Stage 3)

### Input

- Research summary with recommendations
- User requirements
- Success criteria

### Output

- Initiative file in `docs/initiatives/active/`
- ADR (if architectural decision)
- Plan summary for user approval

### Calls

- `/new-adr` - If architectural decision needed

---

## References

- `docs/DOCUMENTATION_STRUCTURE.md` - Initiative format
- `docs/initiatives/template.md` - Initiative template
- `.windsurf/workflows/new-adr.md` - ADR creation
- `.windsurf/workflows/research.md` - Research input
