# Initiative: [Title - Brief Description of the Initiative]

**Status:** Proposed | Active | Complete | Archived
**Created:** YYYY-MM-DD
**Owner:** [Name/Team - Who is responsible]
**Priority:** Critical | High | Medium | Low
**Estimated Duration:** X weeks
**Target Completion:** YYYY-MM-DD (optional)

---

## Objective

[Clear, single-paragraph statement of what this initiative aims to achieve. Should answer: What are we doing and why does it matter?]

Example: "Establish comprehensive test coverage (≥90%) and documentation quality standards to ensure production-ready code quality and maintainability."

---

## Success Criteria

Define measurable outcomes. Each criterion should be a checkbox that can be objectively verified.

- [ ] Criterion 1 (specific, measurable)
- [ ] Criterion 2 (specific, measurable)
- [ ] Criterion 3 (specific, measurable)
- [ ] Criterion 4 (specific, measurable)

**Examples:**

- [ ] Test coverage reaches ≥90% across all modules
- [ ] All documentation passes markdownlint and Vale
- [ ] Zero P0/P1 security vulnerabilities in security scan
- [ ] Performance benchmarks improve by ≥20%

---

## Motivation

### Problem

[What problem does this initiative solve? What pain points exist currently?]

### Impact

[Why is this important? What's the cost of not doing this?]

### Value

[What benefits will this deliver? How does it improve the project/product/team?]

---

## Scope

### In Scope

List what IS included in this initiative:

- Item 1
- Item 2
- Item 3

### Out of Scope

List what is explicitly NOT included (to avoid scope creep):

- Item 1
- Item 2
- Item 3

---

## Tasks

Organize work into logical phases. Use checkboxes for trackable progress.

### Phase 1: [Phase Name]

- [ ] Task 1 with specific deliverable
- [ ] Task 2 with specific deliverable
- [ ] Task 3 with specific deliverable

### Phase 2: [Phase Name]

- [ ] Task 1 with specific deliverable
- [ ] Task 2 with specific deliverable

### Phase 3: [Phase Name]

- [ ] Task 1 with specific deliverable
- [ ] Task 2 with specific deliverable

---

## Dependencies

List anything this initiative depends on (or that depends on it).

### Prerequisites

- Dependency 1 (external library, approval, etc.)
- Dependency 2

### Blockers

- Current blocker 1 (remove when resolved)
- Current blocker 2

### Downstream Impact

- What will be blocked by this initiative
- Teams/projects affected

---

## Risks and Mitigation

Identify potential risks and how to address them.

| Risk | Impact | Likelihood | Mitigation Strategy |
|------|--------|------------|---------------------|
| Example: Scope creep | High | Medium | Fixed scope, defer non-critical items |
| Example: Technical complexity | High | Low | Spike work in Phase 1, adjust if needed |
| Example: Resource constraints | Medium | High | Prioritize critical path items |

**Impact levels:** Critical, High, Medium, Low
**Likelihood levels:** Very Likely, Likely, Possible, Unlikely

---

## Timeline

Provide high-level schedule. Adjust as needed based on actual progress.

- **Week 1:** Phase 1 - [Key milestones]
- **Week 2:** Phase 1 completion, Phase 2 start
- **Week 3:** Phase 2 - [Key milestones]
- **Week 4:** Phase 3, final testing, documentation

**Milestones:**

- Milestone 1 (Date): Description
- Milestone 2 (Date): Description

---

## Metrics

How will we measure success beyond binary checkboxes?

**Baseline metrics (before):**

- Metric 1: Current value
- Metric 2: Current value

**Target metrics (after):**

- Metric 1: Target value
- Metric 2: Target value

**Example:**

- Test coverage: 65% → 90%
- Build time: 180s → <120s
- Documentation lint errors: 50 → 0

---

## Related Documentation

Cross-reference relevant files and documentation.

- [ADR-XXXX: Related Decision](../adr/XXXX-name.md)
- [Related Initiative](other-initiative.md)
- [Technical Guide](../guides/guide-name.md)
- [External Reference](https://example.com)

---

## Updates

Document major milestones, blockers, and progress. Add new entries at the top (most recent first).

### YYYY-MM-DD (Update Title)

**Completed:**

- Item 1
- Item 2

**In Progress:**

- Item 1 (X% complete)

**Blockers:**

- Blocker description and status

**Next Steps:**

- Next action 1
- Next action 2

---

### YYYY-MM-DD (Initial Creation)

Initiative created and approved for work.

---

**Last Updated:** YYYY-MM-DD
**Status:** [Current status with brief context]

---

## Completion and Archival

When this initiative is complete:

1. Mark all success criteria as `[x]` checked
2. Update **Status:** to "Complete" or "✅ Completed"
3. Add **Completed:** date in metadata
4. **IMPORTANT:** The `/archive-initiative` workflow will automatically move this to `completed/` directory

- This happens automatically as part of session end protocol
- Do NOT manually move the file
- Ensures proper tracking and historical record

---

## Template Usage Notes

**Remove this section when creating actual initiative.**

### Required Sections

These must be filled in:

- Title
- All metadata fields
- Objective
- Success Criteria (minimum 3)
- Motivation (all subsections)
- Scope (In/Out)
- Tasks (minimum 1 phase)

### Optional Sections

These can be omitted if not applicable:

- Target Completion (if no deadline)
- Dependencies (if none)
- Risks (if low-risk initiative)
- Metrics (if success criteria sufficient)
- Downstream Impact (if isolated work)

### Tips

1. **Be specific:** "Add tests" → "Add 10 unit tests covering security.py functions"
2. **Use numbers:** "Improve performance" → "Reduce latency by 30%"
3. **Link files:** Reference specific paths, not "the code"
4. **Prioritize tasks:** Mark critical path items clearly
5. **Update regularly:** Add Updates entry after each session
6. **Be realistic:** Estimate conservatively, adjust as you learn

### When to Use This Template

✅ **Use for:**

- Multi-session work (>1 day)
- Complex features requiring planning
- Work affecting multiple areas
- Efforts requiring coordination

❌ **Don't use for:**

- Single bug fixes
- Quick improvements (<4 hours)
- Exploratory work (create ADR instead)
- Routine maintenance

### Example Titles

Good:

- "Quality Foundation & Testing Excellence"
- "Security Audit and Hardening"
- "API Rate Limiting Implementation"

Bad:

- "Improvements" (too vague)
- "Fix stuff" (not descriptive)
- "V2" (use descriptive name)
