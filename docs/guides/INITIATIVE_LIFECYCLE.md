# Initiative Lifecycle Management Guide

**Version:** 1.0.0  
**Last Updated:** 2025-10-19  
**Related ADR:** ADR-0021 (Initiative System Improvements)

---

## Overview

This guide provides comprehensive documentation on the initiative lifecycle management system, including automated validation, dependency tracking, blocker propagation, and archival workflows.

**Audience:** Developers, AI agents, project managers

**Prerequisites:** Familiarity with markdown, YAML frontmatter, git workflows

---

## Table of Contents

1. [Lifecycle Stages](#lifecycle-stages)
2. [Creating Initiatives](#creating-initiatives)
3. [Managing Dependencies](#managing-dependencies)
4. [Tracking Blockers](#tracking-blockers)
5. [Phase Management](#phase-management)
6. [Validation System](#validation-system)
7. [Archival Process](#archival-process)
8. [Automated Tools](#automated-tools)

---

## Lifecycle Stages

```text
┌──────────┐     ┌────────┐     ┌───────────┐     ┌──────────┐
│ Proposed │ ──> │ Active │ ──> │ Completed │ ──> │ Archived │
└──────────┘     └────────┘     └───────────┘     └──────────┘
      │                                                   │
      └───────────────> Archived (Superseded) <──────────┘
```

### 1. Proposed

- **Location:** `docs/initiatives/active/`
- **Status:** `Proposed`
- **Purpose:** Planning and approval phase
- **Actions:**
  - Objectives defined
  - Success criteria documented
  - Awaiting prioritization or approval

### 2. Active

- **Location:** `docs/initiatives/active/`
- **Status:** `Active`
- **Purpose:** Work in progress
- **Actions:**
  - Tasks being completed
  - Regular updates in Updates section
  - Dependencies tracked
  - Blockers managed

### 3. Completed

- **Location:** `docs/initiatives/completed/`
- **Status:** `Completed` or `✅ Completed`
- **Purpose:** Successfully finished work
- **Actions:**
  - All success criteria met
  - Archival validation passed
  - Moved via `/archive-initiative` workflow

### 4. Archived (Optional)

- **Location:** `docs/initiatives/archived/` or as artifacts in superseding initiative
- **Status:** `Archived`
- **Purpose:** Superseded or deprecated initiatives
- **Actions:**
  - Work replaced by other initiatives
  - Preserved for historical context

---

## Creating Initiatives

### Step 1: Choose Structure

| Criteria | Flat File | Folder-Based |
|----------|-----------|--------------|
| **Size** | <1000 words | >1000 words |
| **Phases** | Single phase | Multiple phases |
| **Artifacts** | None | Research, analysis, diagrams |
| **Complexity** | Simple | Complex |

### Step 2: Use Scaffolding Tool

**ALWAYS use automated scaffolding** to ensure consistency:

```bash
# Interactive mode (recommended)
task scaffold:initiative

# With parameters
task scaffold:initiative NAME="feature-name" TYPE="folder" PRIORITY="high"
```

**The scaffolder will:**

- ✅ Create proper directory structure
- ✅ Generate required frontmatter fields
- ✅ Use correct YYYY-MM-DD date format
- ✅ Initialize phases/ and artifacts/ directories (folder-based)
- ✅ Validate naming conventions

### Step 3: Required Frontmatter

All initiatives MUST have these frontmatter fields (enforced by pre-commit):

```yaml
---
Status: Active
Created: 2025-10-19
Owner: @username
Priority: High
Estimated Duration: 20-28 hours
Target Completion: 2025-11-09
Updated: 2025-10-19
---
```

**Field Validation:**

- `Status`: Must be one of: `Proposed`, `Active`, `Completed`, `✅ Completed`, `Archived`
- `Created`: Must be YYYY-MM-DD format
- `Priority`: Must be one of: `Low`, `Medium`, `High`, `Critical`
- `Updated`: Must be YYYY-MM-DD format

### Step 4: Define Success Criteria

Success criteria MUST use checkbox format for automated validation:

```markdown
## Success Criteria

- [ ] Feature X implemented and tested
- [ ] Documentation updated
- [ ] Performance benchmarks met (>100 req/s)
- [ ] Security review passed
- [ ] All tests passing (≥90% coverage)
```

**Validation:** Archival gates check that all checkboxes are marked `[x]` before completion.

---

## Managing Dependencies

### Dependency Types

The system supports three dependency types:

| Type | Description | Blocker Propagation |
|------|-------------|---------------------|
| **prerequisite** | Must complete before this initiative | ✅ Yes (default) |
| **synergistic** | Benefits from coordination | ❌ No (optional) |
| **blocking** | This initiative blocks others | ✅ Yes |

### Declaring Dependencies

Add to initiative frontmatter:

```yaml
---
Dependencies:
  - initiative: "2025-10-17-workflow-optimization"
    type: "prerequisite"
    blocker_propagation: true
  - initiative: "2025-10-18-security-audit"
    type: "synergistic"
    blocker_propagation: false
---
```

Or in the Dependencies section:

```markdown
## Dependencies

**Prerequisite Initiatives:**

- [Workflow Optimization](../2025-10-17-workflow-optimization/initiative.md) - Must complete Phase 2

**Synergistic Initiatives:**

- [Security Audit](../2025-10-18-security-audit/initiative.md) - Coordinate testing approach
```

### Dependency Validation

**Automated checks:**

```bash
# Validate all dependencies
python scripts/dependency_registry.py --validate

# Generate dependency graph
python scripts/dependency_registry.py --graph > dependencies.dot
dot -Tpng dependencies.dot -o dependencies.png

# Check for circular dependencies
python scripts/dependency_registry.py --validate  # Detects cycles
```

**Pre-commit enforcement:**

- Initiative validation hook checks dependencies
- Blocks commits if prerequisite initiatives are blocked/incomplete
- Detects circular dependency chains

---

## Tracking Blockers

### Blocker Categories

Blockers are automatically classified into four categories:

| Category | Keywords | Example |
|----------|----------|---------|
| **Technical** | api, code, bug, infrastructure, dependency, library, system, integration | "API endpoint returns 500 errors" |
| **People** | team, staff, resource, skill, hire, availability, assignment | "Waiting for senior engineer review" |
| **Logistical** | process, approval, coordination | "Pending architecture committee approval" |
| **Time** | deadline, timeline, schedule, delay, overrun | "Blocked until Q2 2025" |

### Declaring Blockers

Add to Blockers section:

```markdown
## Blockers

**Current Blockers:**

- Waiting for API key approval from infrastructure team (People)
- External dependency library has breaking bug (Technical)

**Resolved Blockers:**

- ~~Database migration completed (2025-10-18)~~
```

### Blocker Propagation

When a blocker is added to Initiative A, it automatically propagates to all dependent initiatives:

```text
Initiative A (has blocker)
    │
    ├─> Initiative B (receives propagated blocker)
    │
    └─> Initiative C (receives propagated blocker)
```

**View blocker impact:**

```bash
# Generate blocker dashboard
python scripts/dependency_registry.py --dashboard blocker-report.md

# Show propagation cascade
python scripts/dependency_registry.py --blockers
```

**Dashboard includes:**

- Summary statistics by category
- Active blockers table with impact analysis
- Propagation cascade visualization

---

## Phase Management

### Phase Structure

Organize work into logical phases:

```markdown
## Phases

### Phase 1: Planning (4-5 hours)

**Goal:** Define architecture and approach

**Tasks:**

- [ ] Research existing solutions
- [ ] Design system architecture
- [ ] Create ADR for key decisions
- [ ] Review with team

**Success Criteria:**

- Architecture documented
- ADR approved
- Team consensus reached

### Phase 2: Implementation (10-12 hours)

**Goal:** Build core functionality

**Tasks:**

- [ ] Implement feature A
- [ ] Implement feature B
- [ ] Write unit tests
- [ ] Write integration tests

**Success Criteria:**

- All features implemented
- Test coverage ≥90%
- All tests passing
```

### Phase Progression Validation

**Automated checks enforce sequential phase completion:**

```bash
# Validate phase progression
python scripts/validate_initiatives.py

# Example validation errors:
# ❌ Phase 3 complete but Phase 1 incomplete
# ❌ Phase 2 complete but Phase 1 has unchecked tasks
```

**Rules:**

1. Phases must be numbered sequentially (1, 2, 3...)
2. Phase N cannot be complete if Phase N-1 is incomplete
3. All tasks in Phase N-1 must be checked before Phase N can be complete

**Validation runs:**

- Pre-commit hook (on initiative file changes)
- Weekly CI validation job
- Before archival (via `/archive-initiative`)

---

## Validation System

### Three-Layer Validation

#### 1. Pre-Commit Validation (Real-time)

Runs automatically on `git commit`:

```yaml
# .pre-commit-config.yaml
- id: validate-initiatives
  name: "📋 initiatives · Validate initiative files"
  entry: uv run python scripts/validate_initiatives.py
  language: system
  files: ^docs/initiatives/(active|completed)/.*\.md$
  args: [--ci]
```

**Checks:**

- Required frontmatter fields present
- Valid field values (Status, Priority, dates)
- YAML frontmatter syntax valid
- Phase progression consistent
- Status matches task completion

#### 2. Initiative Validation (On-demand)

Run manually for detailed analysis:

```bash
# Validate single initiative
python scripts/validate_initiatives.py --file docs/initiatives/active/2025-10-19-example/initiative.md

# Validate all initiatives
python scripts/validate_initiatives.py

# CI mode (exit 1 on failures)
python scripts/validate_initiatives.py --ci

# Generate markdown report
python scripts/validate_initiatives.py --report validation-report.md
```

**Checks include:**

- All pre-commit checks
- Success criteria format
- Task completion consistency
- Status inference (0% → Proposed, 1-99% → Active, 100% → Completed)

#### 3. Archival Validation (Pre-archival)

Five-gate validation before moving to `completed/`:

```bash
# Validate archival readiness
python scripts/validate_archival.py docs/initiatives/active/2025-10-19-example/initiative.md

# Generate archival report
python scripts/validate_archival.py \
  docs/initiatives/active/2025-10-19-example/initiative.md \
  --report archival-validation.md
```

**Five Gates:**

| Gate | Check | Severity | Bypass |
|------|-------|----------|--------|
| **Status Completion** | Status = "Completed" or "✅ Completed" | CRITICAL | No |
| **Success Criteria** | All checkboxes checked ([x]) | CRITICAL | No |
| **Blockers** | All current blockers resolved | WARNING | Yes |
| **Dependencies** | No initiatives depend on this one | CRITICAL | Waiver required |
| **Documentation** | Updates section has completion entry | WARNING | Yes |

---

## Archival Process

### Step 1: Complete Work

1. Mark all success criteria as complete: `- [x]`
2. Resolve all blockers (or document bypass rationale)
3. Update Status to `Completed` or `✅ Completed`
4. Add completion entry to Updates section

### Step 2: Run Archival Validation

```bash
# Validate archival readiness
python scripts/validate_archival.py \
  docs/initiatives/active/2025-10-19-initiative-name/initiative.md
```

**Interpret Results:**

- **Exit code 0:** All gates passed → Proceed to Step 3
- **Exit code 1:** Gate failures → Fix issues or use bypass

**Example Output:**

```text
📋 Archival Validation: initiative.md
============================================================

✅ [CRITICAL]    Status Completion    Status: Completed
✅ [CRITICAL]    Success Criteria     5/5 success criteria met
✅ [WARNING]     Blockers            No active blockers
✅ [CRITICAL]    Dependencies        No dependents
⚠️  [WARNING]     Documentation       No completion entry found
   └─ Add completion entry with date and summary to Updates section

============================================================
Passed: 4/5
Critical failures: 0
Warning failures: 1

✅ ARCHIVAL ALLOWED
```

### Step 3: Use Archival Workflow

```bash
# Via workflow (recommended)
# Workflow automatically runs during session end protocol
```

Or manually:

```bash
# Move to completed
mv docs/initiatives/active/2025-10-19-example/ \
   docs/initiatives/completed/

# Add archived notice to initiative.md
# Commit
git add docs/initiatives/completed/2025-10-19-example/
git commit -m "docs(initiative): archive completed initiative"
```

### Step 4: Handle Waivers (If Needed)

**If WARNING gates fail, use force bypass:**

```bash
python scripts/validate_archival.py \
  docs/initiatives/active/2025-10-19-example/initiative.md \
  --force \
  --reason "Superseded by initiative X, blockers no longer relevant"
```

**Waiver Decision Framework:**

| Decision | Criteria | Action |
|----------|----------|--------|
| **Go** | All gates passed | Proceed to archival |
| **Waiver** | Minor warnings only | Document reason, proceed with `--force` |
| **Waiver with Review** | Multiple warnings | Document issues, archive, review in 30 days |
| **Kill/Recycle** | Critical failures | Return to active, fix issues |

**Waiver documentation must include:**

- Which gates failed
- Business justification for bypass
- Mitigation plan (if applicable)
- Approval authority (if required)

---

## Automated Tools

### Tool Reference

| Tool | Purpose | Usage |
|------|---------|-------|
| `scripts/scaffold.py` | Create new initiatives | `task scaffold:initiative` |
| `scripts/validate_initiatives.py` | Validate initiative files | `python scripts/validate_initiatives.py` |
| `scripts/validate_archival.py` | Validate archival readiness | `python scripts/validate_archival.py <file>` |
| `scripts/dependency_registry.py` | Manage dependencies & blockers | `python scripts/dependency_registry.py --validate` |

### Common Commands

```bash
# Create new initiative
task scaffold:initiative

# Validate single initiative
python scripts/validate_initiatives.py --file <path>

# Validate all initiatives
python scripts/validate_initiatives.py

# Check archival readiness
python scripts/validate_archival.py <path>

# Generate archival report
python scripts/validate_archival.py <path> --report report.md

# Validate dependencies
python scripts/dependency_registry.py --validate

# Generate dependency graph
python scripts/dependency_registry.py --graph

# Show blocker propagation
python scripts/dependency_registry.py --blockers

# Generate blocker dashboard
python scripts/dependency_registry.py --dashboard dashboard.md
```

### Integration with Workflows

**Windsurf Workflows:**

- `/archive-initiative` - Automated archival with validation gates
- `/detect-context` - Uses dependency registry for context detection
- `/work-session-protocol` - Runs archival validation at session end

**Pre-commit Hooks:**

- `validate-initiatives` - Runs on every commit to initiative files
- Blocks commits with validation failures

**CI/CD:**

- Weekly validation job (planned)
- Issue creation for validation failures (planned)

---

## Best Practices

### DO ✅

- **Use automated scaffolding** - Ensures consistency and required metadata
- **Declare dependencies explicitly** - Enables automated blocker propagation
- **Categorize blockers** - Helps with prioritization and reporting
- **Use checkbox format for success criteria** - Enables automated validation
- **Update regularly** - Add updates section entries for major milestones
- **Run validation before archival** - Catch issues early
- **Document waivers** - Justify bypass decisions with rationale

### DON'T ❌

- **Don't manually create initiatives** - Use `task scaffold:initiative`
- **Don't skip frontmatter** - Required fields are enforced by pre-commit
- **Don't ignore validation warnings** - Address issues or document bypass
- **Don't archive without validation** - Use archival workflow
- **Don't leave blockers unresolved** - Resolve or document bypass
- **Don't skip Updates section** - Document completion for archival gate

---

## Troubleshooting

### Common Issues

#### 1. Pre-commit Validation Fails

**Problem:** `validate-initiatives` hook fails on commit

**Solution:**

```bash
# Check validation errors
python scripts/validate_initiatives.py --file <path>

# Fix issues in initiative file
# Re-commit
git add <file>
git commit -m "fix: address validation errors"
```

#### 2. Archival Validation Blocked

**Problem:** Archival validation shows CRITICAL failures

**Solution:**

1. Fix critical issues (cannot bypass)
2. Re-run validation
3. Proceed only when all critical gates pass

#### 3. Circular Dependency Detected

**Problem:** `dependency_registry.py --validate` shows circular dependency chain

**Solution:**

1. Identify cycle: `Initiative A → B → C → A`
2. Break cycle by removing one dependency
3. Re-validate: `python scripts/dependency_registry.py --validate`

#### 4. Blocker Propagation Not Working

**Problem:** Blockers not propagating to dependent initiatives

**Solution:**

1. Check dependency `blocker_propagation: true`
2. Check dependency `type: prerequisite`
3. Verify dependency exists in registry
4. Re-run: `python scripts/dependency_registry.py --blockers`

---

## References

### Internal

- [Initiative README](../initiatives/README.md) - Quick reference
- [ADR-0021: Initiative System Improvements](../adr/0021-initiative-system-lifecycle-improvements.md) - Architecture decision
- [ADR-0013: Initiative Documentation Standards](../adr/0013-initiative-documentation-standards.md) - Original standards
- [Archive Initiative Workflow](../../.windsurf/workflows/archive-initiative.md) - Archival workflow
- [DOCUMENTATION_STRUCTURE.md](../DOCUMENTATION_STRUCTURE.md) - Overall documentation structure

### External

- [Portfolio Management Best Practices (ITONICS)](https://www.itonics-innovation.com/blog/effective-project-portfolio-management)
- [Requirements Traceability Matrix (6Sigma)](https://www.6sigma.us/six-sigma-in-focus/requirements-traceability-matrix-rtm/)
- [Quality Gates (PMI/DTU ProjectLab)](http://wiki.doing-projects.org/index.php/Quality_Gates_in_Project_Management)
- [Blocker Management (Devot Team)](https://devot.team/blog/project-blockers)
- [Stage-Gate Process (ProjectManager)](https://www.projectmanager.com/blog/phase-gate-process)
- [Backstage.io Templates](https://backstage.io/docs/features/software-templates/writing-templates/)

---

**Version History:**

- **1.0.0** (2025-10-19): Initial comprehensive guide

**Maintained By:** Core Team
