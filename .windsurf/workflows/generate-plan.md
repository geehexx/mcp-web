---
created: "2025-10-17"
updated: "2025-10-18"
description: Generate structured implementation plan from research
auto_execution_mode: 3
category: Planning
complexity: 60
tokens: 1585
dependencies:
  - research
status: active
---

# Generate Plan Workflow

**Purpose:** Transform research into concrete implementation plan with phases, tasks, and timelines.

**Invocation:** Called by `/plan` (Stage 3)

**Input:** Research summary from `/research`

---

## Stage 0: Create Task Plan

🔄 **Entering /generate-plan workflow**

**Create task plan:**

```typescript
update_plan({
  explanation: " Starting /generate-plan workflow",
  plan: [
    { step: "1. /generate-plan - Define initiative and success criteria", status: "in_progress" },
    { step: "2. /generate-plan - Break down work into phases", status: "pending" },
    { step: "3. /generate-plan - Identify dependencies and constraints", status: "pending" },
    { step: "4. /generate-plan - Assess risks and define scope", status: "pending" },
    { step: "5. /generate-plan - Create initiative document", status: "pending" },
    { step: "6. /generate-plan - Present plan for approval", status: "pending" }
  ]
})
```

---

## Stage 1: Define Objectives

### 1.1 Restate Requirements

**From user request and research:**

```markdown
## Objective

[One-sentence description of what will be achieved]

**User Need:** [Original request in plain language]
**Technical Approach:** [How it will be implemented based on research]
```

### 1.2 Define Success Criteria

**SMART criteria:**

```markdown
## Success Criteria

- [ ] [Specific deliverable 1]
- [ ] [Specific deliverable 2]
- [ ] [Quality gate: tests, coverage, security]
- [ ] [Documentation requirement]
- [ ] [Review requirement]

**Verification:** [How to confirm completion]
**Estimated Effort:** [N-M hours based on task breakdown]
```

---

## Stage 2: Decompose into Phases

### 2.1 Identify Major Milestones

**Break work into phases:**

**Pattern:**

- Phase 1: Core/foundation (minimal viable)
- Phase 2: Enhancement (key features)
- Phase 3: Integration (apply everywhere)
- Phase 4: Polish (docs, review, deploy)

### 2.2 Define Each Phase

**Template per phase:**

```markdown
### Phase N: [Name] (N hours)

**Goal:** [What this phase achieves]

**Tasks:**
1. [Concrete task 1]
   - [Sub-task if needed]
2. [Concrete task 2]
3. [Concrete task 3]

**Exit Criteria:** [How to know phase is complete]

**Dependencies:** [What must complete first]
```

**Task sizing:**

- Each task: <4 hours
- Each phase: <8 hours
- Total: Avoid >20 hour plans (split initiative if needed)

---

## Stage 3: Create Task Dependency Graph

### 3.1 Identify Dependencies

```markdown
## Dependencies

Phase 1 (Foundation) → Phase 2 (Features)
                    ↘
                     → Phase 3 (Integration)
                                           ↘
                                            → Phase 4 (Docs)

**Parallel Work:**
- Phase 2 + Phase 3 can partially overlap after Phase 1
- Documentation can start during Phase 3

**Blockers:**
- [Any external dependencies]
```

### 3.2 Estimate Timeline

```markdown
**Timeline:**
- Phase 1: Session 1 (4h)
- Phase 2: Session 1-2 (3h)
- Phase 3: Session 2 (2h)
- Phase 4: Session 2-3 (2h)

**Total:** 11 hours across 2-3 sessions
**Calendar:** 3-5 days with normal work pace
```

---

## Stage 4: Risk Assessment

### 4.1 Identify Risks

**For each potential risk:**

```markdown
## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk 1] | High/Med/Low | High/Med/Low | [How to prevent/mitigate] |
| [Risk 2] | High/Med/Low | High/Med/Low | [How to prevent/mitigate] |
```

**Common risk categories:**

- Technical (integration issues, bugs)
- Security (vulnerabilities, exposure)
- Performance (latency, memory)
- Scope (feature creep, unclear requirements)
- Dependencies (library issues, external APIs)

### 4.2 Define Out of Scope

**Explicitly list what's NOT included:**

```markdown
**Out of Scope:**
- [Feature A] — Reason: [Too complex for v1, plan separately]
- [Feature B] — Reason: [Not needed for MVP]
- [Technology C] — Reason: [Overkill for use case]

**Future Considerations:**
- [Feature D] — May add in Phase 2 initiative if needed
```

---

## Stage 5: Create Initiative Document

### 5.1 Generate Initiative File

**Filename:** `docs/initiatives/active/YYYY-MM-DD-descriptive-name.md`

**Content template:**

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

[From Stage 1.1]

---

## Success Criteria

[From Stage 1.2]

---

## Research Summary

**Approach:** [Recommended approach from research]

**Key Findings:**
- [Finding 1]
- [Finding 2]

**Libraries/Tools:**
- [Library 1] - [Purpose]

**References:**
- [URL 1] - [Description]

---

## Implementation Plan

[Copy all phases from Stage 2.2]

---

## Dependencies

[From Stage 3.1]

---

## Risks & Mitigation

[From Stage 4.1]

**Out of Scope:**
[From Stage 4.2]

---

## ADRs

- [ ] [ADR-XXXX]: [Decision title if architectural]

**ADR Required:** [Yes/No - explain why]

---

## Related Documentation

- [File 1] - [Status: needs update/reference only]
- [File 2] - [Status: needs creation/update]

---

## Updates

### YYYY-MM-DD (Creation)
Initiative created. Research complete. Ready for Phase 1.

[Future updates will be added here as work progresses]
```

### 5.2 Validate Initiative

**Checklist:**

- [ ] Objective clear and concise
- [ ] Success criteria measurable
- [ ] Tasks sized appropriately (<4h each)
- [ ] Dependencies identified
- [ ] Risks assessed with mitigations
- [ ] Out of scope explicitly stated
- [ ] Estimated effort realistic
- [ ] Target completion reasonable

---

## Stage 6: Create Supporting Documents

### 6.1 ADR Creation (if needed)

**If architectural decision required:**

```bash
# Call ADR workflow
/new-adr "[Decision title]"
```

**ADR needed when:**

- Significant architecture change
- Technology choice with long-term impact
- Security pattern adoption
- Breaking change to public API

### 6.2 Update Related Docs

**Document what needs updating:**

```markdown
## Documentation Updates Required

**During implementation:**
- [ ] docs/API.md - Add auth section
- [ ] README.md - Add auth setup instructions
- [ ] .env.example - Add API_KEY_SECRET

**After completion:**
- [ ] PROJECT_SUMMARY.md - Add to features list
- [ ] docs/reference/CHANGELOG.md - Note in Unreleased
```

---

## Stage 7: Present Plan to User

### 7.1 Summary Format

```markdown
## 📋 Plan Complete: [Title]

**Estimated Effort:** [N hours] ([M sessions])
**Phases:** [Count] ([Phase names])
**Complexity:** [High/Medium/Low]

---

### Key Decisions

1. **[Decision 1]:** [What was decided] — [Rationale]
2. **[Decision 2]:** [What was decided] — [Rationale]

---

### Implementation Phases

**Phase 1 ([N]h):** [Brief description]
**Phase 2 ([N]h):** [Brief description]
[...]

---

### Risks Identified

[Count] risks identified with mitigation strategies:
- [Risk 1] - [Mitigation]
- [Risk 2] - [Mitigation]

---

### Next Steps

1. ✅ Review this plan
2. ✅ Approve or request changes
3. ⏭️ Begin Phase 1 implementation

**Ready to proceed?**
```

---

## Quality Standards

### Good Plan Characteristics

✅ **Actionable:**

- Concrete tasks, not vague goals
- Clear acceptance criteria
- Realistic effort estimates

✅ **Complete:**

- All phases covered
- Dependencies identified
- Risks with mitigations
- Documentation plan included

✅ **Maintainable:**

- Initiative file is single source of truth
- Updates section for tracking progress
- Related docs clearly listed

### Poor Plan Signs

❌ **Vague:**

- "Implement feature" (too broad)
- "Add security" (not specific)
- No concrete tasks

❌ **Unrealistic:**

- 20-hour task in single item
- No risk assessment
- Overly optimistic timeline

❌ **Incomplete:**

- Missing documentation plan
- No dependency analysis
- Unclear success criteria

---

## Anti-Patterns

### ❌ Don't: Create Mega-Plans

**Bad:** 50-hour initiative with 20 phases
**Good:** Split into 2-3 smaller initiatives

### ❌ Don't: Ignore Risks

**Bad:** "Everything will work fine"
**Good:** Identify 3-5 realistic risks with mitigations

### ❌ Don't: Skip Documentation Planning

**Bad:** "We'll document later"
**Good:** List exact docs to update per phase

---

## Integration

### Called By

- `/plan` - After research complete (Stage 3+)

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

- `docs/DOCUMENTATION_STRUCTURE.md` - Initiative file format
- `docs/initiatives/template.md` - Initiative template (if exists)
- `.windsurf/workflows/new-adr.md` - ADR creation
- `.windsurf/workflows/research.md` - Research input
