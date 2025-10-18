---
title: Workflow Development Guide
description: Standards and conventions for creating Windsurf AI workflows
category: Reference Documentation
related_workflows: All workflows in .windsurf/workflows/
---

# Workflow Development Guide

> **📖 Reference Documentation**
>
> This is a reference guide for creating and maintaining Windsurf AI workflows.
> For workflow execution, see individual workflow files in `.windsurf/workflows/`.

**Purpose:** Comprehensive standards for workflow creation, task numbering, transparency, and quality gates.

**Audience:** AI agents (primary), human developers (secondary)

---

## Overview

Workflows in `.windsurf/workflows/` orchestrate complex multi-step processes with:

- Hierarchical task numbering (WBS format)
- Transparent progress reporting
- Quality gates and validation
- Context loading and routing
- Session end protocol integration

---

## Workflow Anatomy

### Required YAML Frontmatter

Every workflow MUST include:

```yaml
---
description: One-line workflow purpose
auto_execution_mode: 1-3  # Windsurf execution mode
category: [Orchestrator | Specialized Operation | Context Handler | Artifact Generator]
---
```

**Categories** (per ADR-0018):

1. **Orchestrators:** Coordinate multiple workflows (`/work`, `/plan`, `/implement`)
2. **Specialized Operations:** Single-purpose tasks (`/commit`, `/validate`, `/new-adr`)
3. **Context Handlers:** Load/manage context (`/detect-context`, `/load-context`)
4. **Artifact Generators:** Create documents (`/generate-plan`, `/extract-session`)

### Standard Sections

```markdown
# [Workflow Name] Workflow

**Purpose:** [One sentence description]

**Category:** [Category from above]

**Invocation:** `/workflow-name [args]`

**Philosophy:** [Core principle guiding this workflow]

**Workflow Chain:** `/workflow` → [child workflows]

---

## Stage 0: Create Initial Task Plan

[Task creation with numbering and transparency]

---

## Stage 1: [First Major Step]

[Implementation details]

---

## Integration

### Called By

- [Parent workflows or user]

### Calls

- [Child workflows]

---

## Anti-Patterns

[What NOT to do]

---

## References

[Links to related docs, ADRs, external sources]
```

---

## Task System Integration

### Mandatory Task Creation

**EVERY workflow with 3+ steps MUST create initial task plan:**

```typescript
update_plan({
  explanation: "🔄 Starting /workflow-name",
  plan: [
    { step: "1. /workflow - First task", status: "in_progress" },
    { step: "2. /workflow - Second task", status: "pending" },
    { step: "3. /workflow - Third task", status: "pending" }
  ]
})
```

**Print confirmation:**

```markdown
✓ Task plan created with N items
```

### Hierarchical Numbering

**Format:** `<number>. /<workflow> - <deliverable>`

**Rules:**

1. **Number with period:** `3.` not `3` or `(3)`
2. **Workflow prefix:** `/implement` shows executor
3. **Dash separator:** ` - ` between workflow and description
4. **Deliverable-focused:** WHAT will be done, not HOW

**Levels:**

- Level 0: `1, 2, 3` - No indent
- Level 1: `3.1, 3.2, 3.3` - 2-space indent
- Level 2: `3.1.1, 3.1.2` - 4-space indent (rare)

**Parent-child numbering:**

```typescript
// Parent task 3 calls child workflow
plan: [
  { step: "3. /work - Execute routed workflow", status: "in_progress" },
  { step: "  3.1. /implement - Load context", status: "in_progress" },  // Child
  { step: "  3.2. /implement - Write tests", status: "pending" },
  { step: "  3.3. /implement - Implement code", status: "pending" },
  { step: "4. /work - Session end protocol", status: "pending" }  // Parent continues
]
```

### Task Attribution

**Tasks MUST be attributed to the workflow that EXECUTES them:**

- ❌ **WRONG:** `{ step: "1. /work - Detect project context" }` (/work doesn't detect!)
- ✅ **CORRECT:** `{ step: "1. /detect-context - Analyze project state" }` (executor)

**Orchestrator vs Executor:**

- Orchestrator tasks: Coordination (routing, protocol execution) → use orchestrator prefix
- Executor tasks: Actual work → use executor's prefix

### Definition of Done

**Each task MUST have clear completion criteria:**

| Task Type | Definition of Done |
|-----------|-------------------|
| Documentation update | File modified, linted, committed |
| Feature implementation | Code written, tests passing, committed |
| Validation | All checks passed, issues resolved |
| Workflow creation | File created, examples included, cross-references updated |

---

## Transparency Requirements

### Workflow Entry

**Print stage/section entry:**

```markdown
🔄 **Entering Stage 2: Context Detection**
```

**Format:** `🔄 **Entering [Stage/Section]: [Name]**`

### Task Updates

**Print task status changes:**

```markdown
📋 **Task Update:** "1. /workflow - Task name" → completed
```

**Format:** `📋 **Task Update:** "[task]" → [status]`

**Always show:**

- Task completions
- Status transitions
- Major milestones

### Workflow Exit

**Print completion summary:**

```markdown
✅ **Completed /implement:** 3 files modified, 26 tests passing, all quality gates passed
```

**Format:** `✅ **Completed [Workflow]:** [Summary]`

### Important Events

**Print routing decisions, waiting states:**

```markdown
ℹ️ **Routing Decision:** High confidence (90%) - continuing with /implement workflow
ℹ️ **Waiting for User:** Review changes before committing
```

**Format:** `ℹ️ **[Event]:** [Details]`

---

## Context Loading

### Use `/load-context` Workflow

**Never load context ad-hoc. Always use workflow:**

```bash
# Load initiative context
/load-context --scope=initiative --path=/path/to/initiative.md

# Load module context
/load-context --scope=module --path=src/mcp_web/module.py
```

### Batch Operations

**ALWAYS batch file reads (3-10x faster):**

```python
# ✅ GOOD: Batch read
mcp0_read_multiple_files([
    "/absolute/path/file1.py",
    "/absolute/path/file2.py",
    "/absolute/path/file3.py"
])

# ❌ BAD: Sequential reads
mcp0_read_text_file("/absolute/path/file1.py")
mcp0_read_text_file("/absolute/path/file2.py")
mcp0_read_text_file("/absolute/path/file3.py")
```

**MCP tools require ABSOLUTE paths:**

- ✅ `/home/gxx/projects/mcp-web/src/file.py`
- ❌ `src/file.py` (relative path fails with MCP)

---

## Quality Gates

### Validation Integration

**Call `/validate` before committing:**

```bash
# Pre-commit validation
/validate

# Specific checks
/validate --scope=lint
/validate --scope=security
```

### Linting Requirements

**All markdown in workflows MUST pass:**

```bash
npx markdownlint-cli2 .windsurf/workflows/*.md
```

**Common violations to avoid:**

- MD040: Fenced code blocks need language identifier
- MD031: Fenced code blocks need blank lines before/after
- MD036: Emphasis used instead of heading
- Custom: Closing fences must not include info string

### Version Control

**NEVER commit:**

- Workflows with lint errors
- Workflows without YAML frontmatter
- Workflows with broken cross-references
- Workflows without examples

---

## Workflow Patterns

### Orchestrator Pattern

**Master workflow routes to specialized workflows:**

```markdown
## Stage 1: Detect Context

Call `/detect-context` workflow

## Stage 2: Route

Based on detection, call appropriate workflow:
- `/implement` for active work
- `/plan` for planning needed
- `/validate` for quality checks

## Stage 3: Execute

Selected workflow performs work

## Stage 4: Session End Protocol

If work complete, execute protocol
```

### Specialized Operation Pattern

**Single-purpose workflow performs task:**

```markdown
## Prerequisites

Check requirements before starting

## Process

1. Prepare
2. Execute
3. Validate
4. Report

## Integration

Document what calls this workflow
```

### Context Handler Pattern

**Load and manage context:**

```markdown
## Stage 1: Determine Scope

What context is needed?

## Stage 2: Load Files

Batch read relevant files

## Stage 3: Validate

Ensure context complete

## Stage 4: Return

Provide loaded context to caller
```

---

## Integration Points

### Version Bump Integration

**For `/commit` workflow:**

```bash
# After successful commit
if commit_type in ['feat', 'fix', 'BREAKING CHANGE']:
    /bump-version  # Automatic semantic versioning
```

### ADR Triggers

**For `/plan` and `/implement` workflows:**

```markdown
## Stage X: Check ADR Requirement

**ADR Assessment:**

Does this involve:
- [ ] New dependency or technology?
- [ ] Architecture pattern change?
- [ ] Security-sensitive decision?

If YES → Call `/new-adr` before proceeding
```

---

## Anti-Patterns

### ❌ Don't: Skip Task System

**Bad:**

```markdown
# Just do work without task plan
```

**Good:**

```typescript
update_plan({
  explanation: "Starting workflow",
  plan: [...]
})
```

### ❌ Don't: Silent Task Updates

**Bad:**

```typescript
// Update task silently
update_plan({ plan: [...] })
```

**Good:**

```markdown
📋 **Task Update:** "Task" → completed

```typescript
update_plan({ plan: [...] })
```

### ❌ Don't: Process-Focused Tasks

**Bad:**

```typescript
{ step: "3. /implement - Read files and edit them" }
```

**Good:**

```typescript
{ step: "3. /implement - Update Section 1.11 (Task System)" }
```

### ❌ Don't: Missing Attribution

**Bad:**

```typescript
{ step: "1. Detect context" }  // No workflow prefix!
```

**Good:**

```typescript
{ step: "1. /detect-context - Analyze project state" }
```

---

## Testing Checklist

**Before committing new workflow:**

- [ ] YAML frontmatter present and valid
- [ ] Task system integration (if 3+ steps)
- [ ] Hierarchical numbering in examples
- [ ] Transparency announcements in all stages
- [ ] Markdown linting passes (0 errors)
- [ ] Cross-references valid
- [ ] Examples include actual commands
- [ ] Integration section documents callers/callees
- [ ] Anti-patterns section included

---

## Examples

### Minimal Workflow

```yaml
---
description: Example minimal workflow
auto_execution_mode: 3
category: Specialized Operation
---

# Example Workflow

**Purpose:** Demonstrate minimal workflow structure.

**Category:** Specialized Operation

**Invocation:** `/example`

---

## Process

### Step 1: Prepare

Do preparation work.

### Step 2: Execute

Perform main task.

### Step 3: Validate

Check results.

---

## Integration

### Called By

- User - Direct invocation

### Calls

- None
```

### Orchestrator Workflow

```yaml
---
description: Example orchestrator workflow
auto_execution_mode: 3
category: Orchestrator
---

# Example Orchestrator Workflow

**Purpose:** Demonstrate orchestration pattern.

**Category:** Orchestrator

**Invocation:** `/example-orchestrator`

---

## Stage 1: Create Initial Task Plan

```typescript
update_plan({
  explanation: "🔄 Starting orchestration",
  plan: [
    { step: "1. /example-orchestrator - Detect context", status: "in_progress" },
    { step: "2. /example-orchestrator - Route to workflow", status: "pending" },
    { step: "3. /example-orchestrator - Execute workflow", status: "pending" }
  ]
})
```

✓ Task plan created with 3 items

---

## Stage 2: Detect and Route

[Detection and routing logic]

---

## Stage 3: Execute

[Execution with subtask numbering]

```typescript
update_plan({
  explanation: "🔀 Routing to /child workflow",
  plan: [
    { step: "1. /example-orchestrator - Detect context", status: "completed" },
    { step: "2. /example-orchestrator - Route to workflow", status: "completed" },
    { step: "3. /example-orchestrator - Execute workflow", status: "in_progress" },
    { step: "  3.1. /child - Load context", status: "in_progress" },
    { step: "  3.2. /child - Process", status: "pending" },
    { step: "  3.3. /child - Validate", status: "pending" }
  ]
})
```

---

## References

- [ADR-0002: Windsurf Workflow System](../adr/0002-adopt-windsurf-workflow-system.md)
- [ADR-0018: Workflow Architecture V3](../adr/0018-workflow-architecture-v3.md)
- [Agent Directives: Section 1.11](../../.windsurf/rules/00_agent_directives.md#111-task-system-usage)
- [WBS Numbering Standard](https://www.tacticalprojectmanager.com/task-numbers-ms-project/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

**Last Updated:** 2025-10-18
**Version:** 1.0.0
**Maintained By:** mcp-web core team
