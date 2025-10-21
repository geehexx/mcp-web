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
├── README.md                       # This file
├── template.md                     # Legacy flat-file template
├── template/                       # Folder-based template (recommended for large initiatives)
│   ├── initiative.md               # Main initiative document
│   ├── phases/
│   │   └── phase-example.md        # Phase-specific documentation
│   └── artifacts/
│       └── README.md               # Supporting artifacts (research, analysis, diagrams)
│
├── active/                         # In progress
│   ├── simple-initiative.md        # Small initiative (flat file)
│   └── 2025-10-18-complex/         # Large initiative (folder-based)
│       ├── initiative.md           # Main doc
│       ├── phases/
│       │   ├── phase-1-planning.md
│       │   └── phase-2-execution.md
│       └── artifacts/
│           └── research-audit.md   # Supporting research
│
├── completed/                      # Successfully finished
│   └── initiative-3.md
└── archived/                       # Deprecated/superseded
    └── initiative-4.md
```

**New in 2025-10-18:** Initiatives can now be **folder-based** to support:

- Large multi-phase initiatives
- Supporting artifacts (research, analysis, diagrams)
- Better organization of related documents
- Clear distinction between initiative plans and supporting materials

## Creating a New Initiative

### Choosing Structure: Flat File vs Folder-Based

**Use Flat File (`.md`) when:**

- Initiative is small (<1000 words)
- Single phase, straightforward execution
- No supporting artifacts needed
- Example: Bug fix initiatives, simple feature adds

**Use Folder-Based structure when:**

- Initiative is large (>1000 words) OR
- Multiple distinct phases OR
- Supporting artifacts (research, analysis, diagrams) OR
- Complex coordination needed
- Example: Architecture refactors, large feature development

### Step 1: Use Automated Scaffolding

**IMPORTANT:** Always use automated scaffolding to ensure consistency and required metadata.

**Use the scaffolding command:**

```bash
# Scaffold new initiative (interactive prompts)
task scaffold:initiative

# Or specify parameters directly
task scaffold:initiative NAME="your-initiative-name" TYPE="folder" PRIORITY="high"
```

**The scaffolding system will:**

- ✅ Create proper directory structure (folder-based or flat-file)
- ✅ Generate initiative file with required frontmatter fields
- ✅ Use correct `YYYY-MM-DD` date format automatically
- ✅ Create `phases/` and `artifacts/` directories (folder-based)
- ✅ Validate naming conventions
- ✅ Initialize with template content

**Decision criteria (scaffolding will prompt):**

- **Flat file (`.md`)**: Small (<1000 words), single phase, no artifacts
- **Folder-based**: Large (>1000 words), multiple phases, or supporting artifacts

**Examples of generated names:**

- `2025-10-15-quality-foundation/` (folder-based)
- `2025-10-18-new-feature.md` (flat-file)
- `2025-10-20-documentation-infrastructure/` (folder-based)

> **⚠️ DEPRECATED:** Manual `cp`/`mkdir` commands are no longer recommended. Use `task scaffold:initiative` for consistency and automated validation.

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

## Comprehensive Guide

For detailed documentation on the complete initiative lifecycle system, see:

**📖 [Initiative Lifecycle Management Guide](../guides/INITIATIVE_LIFECYCLE.md)**

This comprehensive guide covers:

- Complete lifecycle stages with validation
- Dependency management and blocker propagation
- Phase management with automated validation
- Three-layer validation system (pre-commit, on-demand, archival)
- Archival process with five-gate validation
- Automated tools reference
- Troubleshooting common issues

## References

- **[Initiative Lifecycle Guide](../guides/INITIATIVE_LIFECYCLE.md)** - Comprehensive lifecycle documentation
- [ADR-0021: Initiative System Lifecycle Improvements](../adr/0021-initiative-system-lifecycle-improvements.md) - Architecture decision
- [ADR-0013: Initiative Documentation Standards](../adr/0013-initiative-documentation-standards.md) - Original standards
- [ADR-0003: Documentation Standards and Structure](../adr/0003-documentation-standards-and-structure.md) - Overall documentation structure
- [Template](template.md) - Legacy template (use scaffolding tool instead)
- [Archive Initiative Workflow](../../.windsurf/workflows/archive-initiative.md) - Archival workflow
- [GitHub: Planning and Tracking Work](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/planning-and-tracking-work-for-your-team-or-project)

---

## Recently Completed

- **2025-10-18:** Quality Foundation & Testing Excellence (100% complete - mypy strict mode, py.typed marker, comprehensive testing)

---

**Last Updated:** 2025-10-18
**Maintained By:** Core Team

## Initiative Directory Index
<!-- AUTO:INITIATIVE-INDEX:START -->
### Active Initiatives

- [`2025-10-15-performance-optimization-pipeline/`](docs/initiatives/active/2025-10-15-performance-optimization-pipeline)
- [`2025-10-19-session-summary-mining-advanced.md`](docs/initiatives/active/2025-10-19-session-summary-mining-advanced.md)
- [`2025-10-20-phase-0-security-hardening.md`](docs/initiatives/active/2025-10-20-phase-0-security-hardening.md)
- [`2025-10-20-phase-1-resource-stability.md`](docs/initiatives/active/2025-10-20-phase-1-resource-stability.md)
- [`2025-10-20-phase-2-data-integrity.md`](docs/initiatives/active/2025-10-20-phase-2-data-integrity.md)
- [`2025-10-20-phase-3-performance-optimization.md`](docs/initiatives/active/2025-10-20-phase-3-performance-optimization.md)

### Completed Initiatives

- [`2025-10-15-quality-foundation/`](docs/initiatives/completed/2025-10-15-quality-foundation)
- [`2025-10-16-convert-decisions-to-adrs.md`](docs/initiatives/completed/2025-10-16-convert-decisions-to-adrs.md)
- [`2025-10-16-fix-security-unit-tests.md`](docs/initiatives/completed/2025-10-16-fix-security-unit-tests.md)
- [`2025-10-16-windsurf-workflow-rules-improvements.md`](docs/initiatives/completed/2025-10-16-windsurf-workflow-rules-improvements.md)
- [`2025-10-17-windsurf-workflows-v2-optimization/`](docs/initiatives/completed/2025-10-17-windsurf-workflows-v2-optimization)
- [`2025-10-18-markdown-quality-comprehensive-fix/`](docs/initiatives/completed/2025-10-18-markdown-quality-comprehensive-fix)
- [`2025-10-18-workflow-architecture/`](docs/initiatives/completed/2025-10-18-workflow-architecture)
- [`2025-10-18-workflow-artifacts-and-transparency/`](docs/initiatives/completed/2025-10-18-workflow-artifacts-and-transparency)
- [`2025-10-18-workflow-automation-enhancement/`](docs/initiatives/completed/2025-10-18-workflow-automation-enhancement)
- [`2025-10-18-workflow-automation-enhancement.md`](docs/initiatives/completed/2025-10-18-workflow-automation-enhancement.md)
- [`2025-10-19-initiative-system-lifecycle-improvements/`](docs/initiatives/completed/2025-10-19-initiative-system-lifecycle-improvements)
- [`2025-10-19-mcp-file-system-support.md`](docs/initiatives/completed/2025-10-19-mcp-file-system-support.md)
- [`2025-10-19-quality-automation-and-monitoring.md`](docs/initiatives/completed/2025-10-19-quality-automation-and-monitoring.md)
- [`2025-10-19-session-summary-consolidation-workflow/`](docs/initiatives/completed/2025-10-19-session-summary-consolidation-workflow)
- [`2025-10-19-task-system-validation-enforcement.md`](docs/initiatives/completed/2025-10-19-task-system-validation-enforcement.md)
- [`2025-10-19-workflow-transparency-improvements.md`](docs/initiatives/completed/2025-10-19-workflow-transparency-improvements.md)
- [`2025-10-20-workflow-task-system-v3.md`](docs/initiatives/completed/2025-10-20-workflow-task-system-v3.md)
- [`2025-10-21-windsurf-rules-revamp/`](docs/initiatives/completed/2025-10-21-windsurf-rules-revamp)
<!-- AUTO:INITIATIVE-INDEX:END -->
