# ADR-0013: Initiative Documentation Standards and Structure

**Status:** Accepted

**Date:** 2025-10-15

**Deciders:** Core team

**Tags:** documentation, process, project-management

---

## Context

The mcp-web project uses initiatives to track multi-session work efforts (e.g., Quality Foundation, ADR Conversion). However, the initiative documentation structure is inconsistent compared to our well-defined ADR system:

**Current state of initiatives:**
- No README.md explaining purpose or structure
- No template.md for creating new initiatives
- Inconsistent formatting across initiatives
- Unclear lifecycle management (active vs completed)
- No clear guidelines for naming, metadata, or content structure
- Mixed quality and completeness

**Problems this causes:**
- New initiatives created with varying quality
- Difficult to find or navigate initiatives
- Unclear when to create an initiative vs other documentation
- No standardized metadata for tracking
- Hard for AI agents to understand initiative structure
- Inconsistent with ADR professionalism

Our requirements:
1. Professional structure matching ADR quality standards
2. Clear templates and guidelines for creation
3. Proper lifecycle management (proposed → active → completed → archived)
4. Standardized metadata fields
5. Easy navigation and discovery
6. AI-agent friendly format

## Decision

We will establish **comprehensive initiative documentation standards** following project management best practices:

### Initiative Structure

```
docs/initiatives/
├── README.md              # Index and guidelines
├── template.md            # Template for new initiatives
├── active/                # Currently in progress
│   ├── initiative-1.md
│   └── initiative-2.md
├── completed/             # Finished initiatives
│   └── initiative-3.md
└── archived/              # Deprecated/superseded
    └── initiative-4.md
```

### Standard Template Format

Based on GitHub Issues and Jira Epic best practices:

```markdown
# Initiative: [Title]

**Status:** Proposed | Active | Complete | Archived
**Created:** YYYY-MM-DD
**Owner:** [Name/Team]
**Priority:** Critical | High | Medium | Low
**Estimated Duration:** X weeks
**Target Completion:** YYYY-MM-DD (optional)

---

## Objective

[Clear, concise statement of what this initiative aims to achieve]

## Success Criteria

- [ ] Measurable outcome 1
- [ ] Measurable outcome 2
- [ ] Measurable outcome 3

## Motivation

**Problem:** [What problem does this solve?]
**Impact:** [Why is this important?]
**Value:** [What's the benefit?]

## Scope

### In Scope
- Item 1
- Item 2

### Out of Scope
- Item 1
- Item 2

## Tasks

### Phase 1: [Name]
- [ ] Task 1
- [ ] Task 2

### Phase 2: [Name]
- [ ] Task 1
- [ ] Task 2

## Dependencies

- Dependency 1 (external/internal)
- Dependency 2

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Risk 1 | High | Medium | Mitigation strategy |

## Timeline

- **Week 1-2:** Phase 1
- **Week 3-4:** Phase 2

## Related Documentation

- [ADR-XXXX](../adr/XXXX-name.md)
- [Other Initiative](other-initiative.md)

## Updates

### YYYY-MM-DD
- Update content

---

**Last Updated:** YYYY-MM-DD
**Status:** [Current status]
```

### Naming Convention

Initiatives use descriptive kebab-case names:

```
YYYY-QN-brief-description.md
or
descriptive-name.md
```

Examples:
- `2024-q4-quality-foundation.md`
- `fix-security-unit-tests.md`
- `documentation-infrastructure.md`

### Lifecycle Management

1. **Proposed** → Create in `docs/initiatives/active/` with status "Proposed"
2. **Active** → Update status to "Active" when work begins
3. **Complete** → Move to `docs/initiatives/completed/` when all success criteria met
4. **Archived** → Move to `docs/initiatives/archived/` if deprecated or superseded

### README.md Structure

The initiatives README provides:
- Purpose and overview
- How to create new initiatives
- Lifecycle explanation
- Index of active initiatives
- Links to templates and guidelines

## Alternatives Considered

### Alternative 1: Continue Informal Structure

**Description:** Keep initiatives as freeform documents without standards

**Pros:**
- No migration effort
- Flexibility in format
- Minimal overhead

**Cons:**
- Continued inconsistency
- Poor discoverability
- Unprofessional appearance
- AI agents struggle to parse
- No clear ownership or tracking

**Reason for rejection:** Inconsistency undermines project professionalism

### Alternative 2: Use GitHub Issues/Projects

**Description:** Track initiatives as GitHub issues with projects board

**Pros:**
- Built-in tooling
- Good for collaboration
- Status tracking built-in
- Integrates with PRs

**Cons:**
- Locked into GitHub ecosystem
- Not portable (can't backup in repo)
- Less readable for AI agents
- Mixed with code issues
- No offline access

**Reason for rejection:** File-based approach preferred for portability and AI-friendliness

### Alternative 3: Lightweight Structure (README only)

**Description:** Add only README.md, no template or strict format

**Pros:**
- Faster to implement
- Less restrictive
- Still provides some structure

**Cons:**
- Won't solve consistency issues
- No clear template for new initiatives
- Minimal improvement over current state
- Quality will still vary

**Reason for rejection:** Doesn't adequately address the problems

### Alternative 4: Use Jira/External Tool

**Description:** Track initiatives in external project management tool

**Pros:**
- Rich features (dashboards, reporting)
- Collaboration tools built-in
- Established workflows

**Cons:**
- External dependency
- Not in git (poor for AI agents)
- Cost (if not free tier)
- Context switching overhead
- Not suitable for single-developer projects

**Reason for rejection:** File-based approach aligns with project philosophy

## Consequences

### Positive Consequences

- **Professional quality:** Initiatives match ADR professionalism
- **Consistency:** All initiatives follow same structure
- **Discoverability:** README provides clear index and navigation
- **AI-friendly:** Standard format enables intelligent parsing
- **Lifecycle clarity:** Clear progression from proposed → complete
- **Better planning:** Template prompts for risks, dependencies, success criteria
- **Improved tracking:** Standardized metadata enables reporting

### Negative Consequences

- **Migration effort:** Must update existing initiatives (2-3 hours)
- **Template overhead:** Creating initiative requires more fields
- **Maintenance:** README index must be kept updated
- **Learning curve:** Contributors must learn new structure

### Neutral Consequences

- **Template evolution:** May need to refine template based on usage
- **Automation opportunities:** Could create tools for initiative management
- **Integration:** May want to link initiatives to commits/PRs in future

## Implementation

**Key files created:**
- `docs/initiatives/README.md` - Index and guidelines
- `docs/initiatives/template.md` - Standard template
- `docs/adr/0013-initiative-documentation-standards.md` - This ADR

**Migration required:**
- Update `docs/initiatives/active/2024-q4-quality-foundation.md`
- Update `docs/initiatives/active/fix-security-unit-tests.md`
- Update `docs/initiatives/completed/convert-decisions-to-adrs.md`

**Metadata fields:**
- **Status:** Lifecycle stage
- **Created:** Start date
- **Owner:** Responsible party
- **Priority:** Importance level
- **Estimated Duration:** Time expectation
- **Target Completion:** Deadline (optional)

**Content requirements:**
- **Objective:** Single paragraph, clear goal
- **Success Criteria:** Checkboxes, measurable outcomes
- **Motivation:** Problem/impact/value
- **Scope:** What's included/excluded
- **Tasks:** Organized by phases with checkboxes
- **Dependencies:** Internal/external blockers
- **Risks:** Identified with mitigation strategies
- **Timeline:** High-level schedule
- **Related Documentation:** Cross-references

## References

- [GitHub: Planning and tracking work](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)
- [ProjectManager: 20 Essential Project Documents](https://www.projectmanager.com/blog/great-project-documentation)
- [Atlassian: Configuring initiatives](https://confluence.atlassian.com/advancedroadmapsserver0329/configuring-initiatives-and-other-hierarchy-levels-1021218664.html)
- [RFC Template Process](https://github.com/ghostinthewires/Rfcs-Template)
- Related ADR: [0003-documentation-standards-and-structure.md](0003-documentation-standards-and-structure.md)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-10-15 | Initial proposal and acceptance | Cascade |
| 2025-10-15 | Implementation in progress | Cascade |
