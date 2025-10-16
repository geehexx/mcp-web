# Project Initiatives

This directory tracks multi-session work efforts for the mcp-web project. Initiatives are larger bodies of work that span multiple days or weeks and require coordination across multiple commits and sessions.

## What is an Initiative?

An **initiative** is a planned, goal-oriented work effort that:

- Spans multiple work sessions (typically 1-4 weeks)
- Has clear, measurable success criteria
- Requires multiple commits and potentially multiple phases
- Addresses significant improvements or features
- Needs proper planning, tracking, and documentation

**Examples:**

- Quality Foundation & Testing Excellence
- Security Audit and Hardening
- Documentation Infrastructure Overhaul
- Performance Optimization Campaign

**Not initiatives:**

- Single bug fixes (use git commits)
- Small features (use git commits)
- Quick improvements (use git commits)
- One-session tasks (use git commits)

## When to Create an Initiative

Create an initiative when:

- **Effort:** Work will take more than one session (>4 hours)
- **Complexity:** Multiple interrelated tasks or phases
- **Coordination:** Requires planning and tracking across sessions
- **Scope:** Clear boundaries and measurable outcomes needed
- **Visibility:** Important enough to warrant dedicated tracking

**Rule of thumb:** If it takes more than 3 commits or 2 sessions, it's probably an initiative.

## Initiative Lifecycle

```text
Proposed → Active → Complete → (Archived if superseded)
```

### 1. Proposed

- Created in `active/` directory with status "Proposed"
- Objectives and scope defined
- Awaiting approval or prioritization
- May be deferred or rejected

### 2. Active

- Status changed to "Active"
- Work is in progress
- Tasks are being completed
- Regular updates in "Updates" section

### 3. Complete

- All success criteria met
- Status changed to "Complete"
- **Moved to `completed/` directory**
- Becomes part of historical record

### 4. Archived (Optional)

- Initiative deprecated or superseded
- Status changed to "Archived"
- **Moved to `archived/` directory**
- Provides historical context

## Directory Structure

```text
docs/initiatives/
├── README.md # This file
├── template.md # Template for new initiatives
├── active/ # In progress
│ ├── initiative-1.md
│ └── initiative-2.md
├── completed/ # Successfully finished
│ └── initiative-3.md
└── archived/ # Deprecated/superseded
 └── initiative-4.md
```

## Creating a New Initiative

### Step 1: Copy the Template

```bash
cp docs/initiatives/template.md docs/initiatives/active/your-initiative-name.md
```

### Step 2: Fill in Required Sections

- **Metadata:** Status, dates, owner, priority
- **Objective:** Clear, concise goal statement
- **Success Criteria:** Measurable checkboxes
- **Motivation:** Problem, impact, value
- **Scope:** What's in/out
- **Tasks:** Organized by phases
- **Dependencies:** What's required
- **Risks:** Identified with mitigation
- **Timeline:** High-level schedule

### Step 3: Review Checklist

Before committing, verify:

- [ ] Title is descriptive and concise
- [ ] All required metadata filled in
- [ ] Success criteria are measurable (checkboxes)
- [ ] Tasks are broken down into phases
- [ ] Risks identified with mitigation strategies
- [ ] Dependencies documented
- [ ] Related documentation linked
- [ ] Filename follows naming convention

### Step 4: Commit

```bash
git add docs/initiatives/active/your-initiative-name.md
git commit -m "docs(initiative): create [initiative name]"
```

## Naming Convention

Use descriptive kebab-case names:

### Pattern 1: Quarterly Initiatives

```text
YYYY-QN-brief-description.md
```

Examples:

- `2025-q4-quality-foundation.md`
- `2026-q1-security-hardening.md`

### Pattern 2: Descriptive Names

```text
descriptive-name.md
```

Examples:

- `fix-security-unit-tests.md`
- `documentation-infrastructure.md`
- `performance-optimization.md`

**Guidelines:**

- Use lowercase
- Hyphenate words (kebab-case)
- Be specific but concise (2-5 words)
- Avoid version numbers (use dates instead)

## Updating Initiatives

### Regular Updates

Add to the "Updates" section at the bottom:

```markdown
## Updates

### 2025-10-15
- Completed Phase 1 (tasks 1-5)
- Identified blocker: dependency on external library
- Next: Begin Phase 2 after resolution
```

### Completing an Initiative

1. Mark all success criteria as complete: `- [x]`
2. Update status: `**Status:** Complete` or `**Status:** ✅ Completed`
3. Add completion date: `**Completed:** YYYY-MM-DD`
4. **Archive via workflow:** The `/archive-initiative` workflow will automatically:

- Move file to `completed/` directory
- Update this README index
- Create proper git commit
- This runs automatically during session end protocol

1. Manual archival (if needed):

```bash
git mv docs/initiatives/active/name.md docs/initiatives/completed/name.md
git commit -m "docs(initiative): complete [initiative name]"
```

**Note:** Step 4 (automatic archival) is preferred and happens as part of the session end protocol.

## Active Initiatives

### High Priority

| Initiative | Owner | Started | Target | Progress |
|------------|-------|---------|--------|----------|
| [Quality Foundation](active/2025-q4-quality-foundation.md) | Core Team | 2025-10-15 | 2025-11-15 | Phase 2 |

### Medium Priority

_No medium priority initiatives at this time._

## Recently Completed

| Initiative | Owner | Completed | Duration |
|------------|-------|-----------|----------|
| [Fix Security Unit Tests](completed/fix-security-unit-tests.md) | AI Agent | 2025-10-15 | ~1.5 hours |
| [Convert Decisions to ADRs](completed/convert-decisions-to-adrs.md) | AI Agent | 2025-10-15 | 1.5 hours |

## Archived Initiatives

None yet.

## Best Practices

### DO

✅ **Break down into phases** - Organize tasks into logical groups
✅ **Make success criteria measurable** - Use checkboxes, numbers, specific outcomes
✅ **Update regularly** - Add updates section entries for major milestones
✅ **Link related docs** - Cross-reference ADRs, guides, issues
✅ **Identify risks early** - Document risks and mitigation strategies
✅ **Track dependencies** - Note external/internal blockers
✅ **Set realistic timelines** - Estimate conservatively
✅ **Move when complete** - Archive to completed/ directory

### DON'T

❌ **Don't create for small tasks** - Use git commits for <4 hour work
❌ **Don't leave stale** - Update or close if no longer relevant
❌ **Don't be vague** - "Improve system" is not a good objective
❌ **Don't skip scope** - Define what's in/out explicitly
❌ **Don't ignore risks** - Identify and document mitigation
❌ **Don't duplicate** - Check if similar initiative exists
❌ **Don't overcomplicate** - Keep format simple and scannable

## Template Customization

The template is flexible. Adapt sections as needed:

**Add sections for:**

- Technical design details
- API specifications
- Performance benchmarks
- Security considerations

**Remove sections if:**

- No dependencies (skip Dependencies)
- No identified risks (skip Risks)
- Simple timeline (simplify Timeline)

**Core sections are required:**

- Objective
- Success Criteria
- Motivation
- Tasks

## Metrics and Reporting

Track initiative health:

- **Completion rate:** % of success criteria met
- **Timeline adherence:** On track / behind / ahead
- **Blocker count:** Number of unresolved blockers
- **Update frequency:** Days since last update

**Red flags:**

- No updates in 7+ days
- >50% behind timeline
- Multiple unresolved blockers
- Success criteria changed multiple times

## AI Agent Guidance

When creating or updating initiatives:

1. **Always check existing initiatives first** - Avoid duplication
2. **Use the template** - Consistency is key
3. **Be specific in tasks** - "Add tests" → "Add 10 unit tests to test_security.py"
4. **Link to files/paths** - Reference specific files, not "the code"
5. **Make success criteria boolean** - Must be clearly met or not met
6. **Update after each session** - Document progress in Updates section
7. **Move when complete** - Don't leave completed initiatives in active/

## References

- [ADR-0013: Initiative Documentation Standards](../adr/0013-initiative-documentation-standards.md)
- [ADR-0003: Documentation Standards and Structure](../adr/0003-documentation-standards-and-structure.md)
- [Template](template.md)
- [GitHub: Planning and Tracking Work](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)

---

**Last Updated:** 2025-10-15
**Maintained By:** Core Team
