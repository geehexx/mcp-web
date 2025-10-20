---
description: Generate structured implementation plan from research
---

# Generate Plan Workflow

**Purpose:** Transform research into concrete implementation plan with phases, tasks, and timelines.

**Invocation:** Called by `/plan` (Stage 3)

**Input:** Research summary from `/research`

---

## Stage 0: Task Plan Setup

🔄 **Entering Stage 0: Task Plan Setup**

**Print workflow entry announcement:**

```markdown
🔄 **Entering /generate-plan:** Creating structured implementation roadmap
```

**Create task plan with enhanced granularity:**

```typescript
update_plan({
  explanation: "🔄 Starting /generate-plan workflow",
  plan: [
    { step: "1. /generate-plan - Load context and analyze requirements", status: "in_progress" },
    { step: "2. /generate-plan - Identify key components and dependencies", status: "pending" },
    { step: "3. /generate-plan - Decompose work into phases", status: "pending" },
    { step: "4. /generate-plan - Break phases into concrete tasks", status: "pending" },
    { step: "5. /generate-plan - Estimate effort for each task", status: "pending" },
    { step: "6. /generate-plan - Identify risks and mitigations", status: "pending" },
    { step: "7. /generate-plan - Define success criteria", status: "pending" },
    { step: "8. /generate-plan - Generate initiative document", status: "pending" },
    { step: "9. /generate-plan - Validate plan structure", status: "pending" }
  ]
})
```

✓ Task plan created with 9 granular steps

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

**Extract:**

- User requirements
- Research findings
- Existing patterns
- Related ADRs
- Success criteria

**Print stage completion:**

```markdown
📋 **Stage 1 Complete:** Requirements analyzed, [N] key components identified
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Requirements analysis complete",
  plan: [
    { step: "1. /generate-plan - Load context and analyze requirements", status: "completed" },
    { step: "2. /generate-plan - Identify key components and dependencies", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 2: Phase Decomposition

🔄 **Entering Stage 2: Phase Decomposition**

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
- Each phase has clear deliverables
- Phases build on each other
- Each phase ~4-12 hours max

**Print stage completion:**

```markdown
📋 **Stage 2 Complete:** Work decomposed into [N] phases
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Phase decomposition complete",
  plan: [
    { step: "1. /generate-plan - Load context and analyze requirements", status: "completed" },
    { step: "2. /generate-plan - Identify key components and dependencies", status: "completed" },
    { step: "3. /generate-plan - Decompose work into phases", status: "completed" },
    { step: "4. /generate-plan - Break phases into concrete tasks", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 3: Task Breakdown

🔄 **Entering Stage 3: Task Breakdown**

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
**Total effort:** Sum of all task estimates

**Buffer:** Add 20-30% for unknowns

**Print stage completion:**

```markdown
📋 **Stage 3 Complete:** [N] concrete tasks defined across all phases
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Task breakdown complete",
  plan: [
    // ... completed tasks ...
    { step: "4. /generate-plan - Break phases into concrete tasks", status: "completed" },
    { step: "5. /generate-plan - Estimate effort for each task", status: "in_progress" },
    // ... pending tasks
  ]
})
```

---

## Stage 4: Effort Estimation

🔄 **Entering Stage 4: Effort Estimation**

### 4.1 Estimate Effort

**For each task:**

```markdown
## Effort Estimation

| Task | Estimated Effort |
|------|-----------------|
| [Task 1] | [N] hours |
| [Task 2] | [N] hours |
```

**Print stage completion:**

```markdown
📋 **Stage 4 Complete:** Total effort estimated at [N-M] hours
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Effort estimation complete",
  plan: [
    // ... completed tasks ...
    { step: "5. /generate-plan - Estimate effort for each task", status: "completed" },
    { step: "6. /generate-plan - Identify risks and mitigations", status: "in_progress" },
    // ... pending tasks
  ]
})
```

---

## Stage 5: Risk Assessment

🔄 **Entering Stage 5: Risk Assessment**

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

- Technical risks
- Dependency risks
- Timeline risks
- Security risks

**Print stage completion:**

```markdown
📋 **Stage 5 Complete:** [N] risks identified with mitigations
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Risk assessment complete",
  plan: [
    // ... completed tasks ...
    { step: "6. /generate-plan - Identify risks and mitigations", status: "completed" },
    { step: "7. /generate-plan - Define success criteria", status: "in_progress" },
    // ... pending tasks
  ]
})
```

---

## Stage 6: Document Generation

🔄 **Entering Stage 6: Document Generation**

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

**Print stage completion:**

```markdown
📋 **Stage 6 Complete:** Initiative document generated
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Initiative document generated",
  plan: [
    // ... completed tasks ...
    { step: "8. /generate-plan - Generate initiative document", status: "completed" },
    { step: "9. /generate-plan - Validate plan structure", status: "in_progress" },
    // ... pending tasks
  ]
})
```

---

## Stage 7: Plan Validation

🔄 **Entering Stage 7: Plan Validation**

### 6.1 Validate Plan Structure

**Checklist:**

- [ ] All tasks have clear completion criteria
- [ ] Dependencies mapped
- [ ] No task >4 hours estimated

**Print stage completion:**

```markdown
📋 **Stage 7 Complete:** Plan structure validated
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Plan structure validated",
  plan: [
    // ... completed tasks ...
    { step: "9. /generate-plan - Validate plan structure", status: "completed" },
  ]
})
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

**Print workflow exit:**

```markdown
✅ **Completed /generate-plan:** Implementation roadmap created with [N] phases and [M] tasks
```

---

## References

- `docs/DOCUMENTATION_STRUCTURE.md` - Initiative file format
- `docs/initiatives/template.md` - Initiative template (if exists)
- `.windsurf/workflows/new-adr.md` - ADR creation
- `.windsurf/workflows/research.md` - Research input
