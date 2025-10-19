# Windsurf Workflow Guide

**Purpose:** Comprehensive guide to Windsurf workflow system architecture, transparency standards, and best practices for creating new workflows.

**Location:** `.windsurf/docs/workflow-guide.md` (reference documentation)

**Workflows Location:** `..workflows/` (executable workflows only)

**Last Updated:** 2025-10-19

**Related:**

- [Workflow Index](./workflow-index.md) - Auto-generated workflow catalog
- [Agent Directives](../rules/00_agent_directives.md) - Core agent behavior rules
- [Context Engineering](../rules/06_context_engineering.md) - File operations and structure

---

## Overview

This directory contains **modular, reusable workflows** that orchestrate AI agent operations in this repository. Workflows follow a standardized structure with **mandatory transparency requirements** to ensure users always know what the agent is doing.

### Key Principles

1. **Transparency First** - Every workflow must provide visible progress through announcements and task updates
2. **Modular Composition** - Workflows call sub-workflows rather than duplicating logic
3. **Task System Integration** - All non-trivial work uses the task system (`update_plan` tool)
4. **Deliverable-Focused** - Tasks describe WHAT will be delivered, not HOW
5. **Test-Driven** - Implementation workflows require tests before code changes

---

## Workflow Categories

### Orchestrator Workflows

**Purpose:** Coordinate and delegate to specialized workflows.

**Characteristics:**

- Call multiple sub-workflows
- Manage overall execution flow
- Provide routing/decision logic
- Light on actual implementation

**Examples:**

- `/work` - Central orchestration and routing
- `/plan` - Research-driven planning coordination
- `/meta-analysis` - Session review and summary generation

### Executor Workflows

**Purpose:** Perform specific, focused tasks.

**Characteristics:**

- Execute concrete actions
- May call utilities but not other executors
- Provide detailed progress during execution
- Return structured results

**Examples:**

- `/implement` - Test-driven implementation
- `/research` - Comprehensive research gathering
- `/validate` - Quality checks and testing
- `/commit` - Git operations with validation

### Utility Workflows

**Purpose:** Provide reusable, focused operations.

**Characteristics:**

- Single, well-defined purpose
- No sub-workflow calls
- Fast execution (<30 seconds typical)
- Minimal task overhead

**Examples:**

- `/load-context` - Efficient context loading
- `/detect-context` - Project state analysis
- `/work-routing` - Routing decision logic

---

## Transparency Standards

**MANDATORY FOR ALL WORKFLOWS** - Per agent directives Section 1.11.5

### Progress Announcements

All workflows MUST print announcements at these points:

#### 1. Workflow Entry

```markdown
🔄 **Entering /workflow:** Purpose description
```

**When:** Immediately upon workflow invocation, before any work
**Why:** Users know workflow has started
**Example:**

```markdown
🔄 **Entering /implement:** Focused implementation with test-first approach
```

#### 2. Stage Completion

```markdown
📋 **Stage N Complete:** What finished
```

**When:** After each major stage completes
**Why:** Users see incremental progress
**Example:**

```markdown
📋 **Stage 3 Complete:** External research finished, 7 sources analyzed
```

#### 3. Sub-Workflow Delegation

```markdown
↪️ **Delegating to /sub-workflow:** Reason
```

**When:** Before calling any sub-workflow
**Why:** Users see execution flow
**Example:**

```markdown
↪️ **Delegating to /research:** Gathering best practices and patterns
```

#### 4. Workflow Exit

```markdown
✅ **Completed /workflow:** Summary of results
```

**When:** After all work complete, before returning
**Why:** Confirms successful completion
**Example:**

```markdown
✅ **Completed /validate:** All tests passing, lint clean, security checks passed
```

### Emoji Standards

| Emoji | Meaning | Usage |
|-------|---------|-------|
| 🔄 | Workflow/Stage Entry | Starting workflow or entering new stage |
| 📋 | Progress Update | Stage complete or significant progress |
| ✅ | Success/Complete | Workflow finished successfully |
| ↪️ | Delegation | Calling sub-workflow |
| ⚠️ | Warning | Non-critical issue or caution |
| ❌ | Error/Failure | Critical failure or error |
| ℹ️ | Information | General informational message |

### Task Update Requirements

**Frequency:**

- **Minimum:** After each stage completion
- **Recommended:** Every 30-90 seconds for long workflows
- **Maximum gap:** 3 minutes without update

**Sub-Workflow Pattern:**

When calling a sub-workflow, ALWAYS:

1. **Update plan BEFORE calling** - Add sub-workflow task
2. **Print delegation message** - Show what's being called
3. **Execute sub-workflow** - Let it run
4. **Update plan AFTER returning** - Mark completed
5. **Print completion message** - Confirm return

**Example:**

```typescript
// BEFORE calling sub-workflow
update_plan({
  explanation: "↪️ Delegating to /research for best practices",
  plan: [
    { step: "2. /plan - Create implementation plan", status: "in_progress" },
    { step: "  2.1. /research - Gather requirements", status: "in_progress" }
  ]
})
console.log("↪️ **Delegating to /research:** Gathering best practices")

// Call sub-workflow
call_workflow("/research", ...)

// AFTER sub-workflow returns
console.log("📋 **Research Complete:** 5 sources analyzed")
update_plan({
  explanation: "Research complete, proceeding to plan generation",
  plan: [
    { step: "2. /plan - Create implementation plan", status: "in_progress" },
    { step: "  2.1. /research - Gather requirements", status: "completed" },
    { step: "  2.2. /generate-plan - Structure plan", status: "in_progress" }
  ]
})
```

---

## Task System Integration

### When to Create Task Plans

**REQUIRED:**

- Any work requiring 3+ distinct steps
- Work expected to take >5 minutes
- All orchestrator workflow invocations
- Any multi-phase implementation

**OPTIONAL (may skip):**

- Single-step request (e.g., "format this file")
- Quick question/answer in Chat mode
- User explicitly requests no planning overhead

### Task Numbering Format

**MANDATORY FORMAT:** `<number>. /<workflow> - <description>`

**Rules:**

1. Include hierarchical number (e.g., `3.1.2`)
2. Period after number (`.`)
3. Workflow prefix (`/workflow-name`)
4. Dash separator (` - `)
5. Deliverable-focused description

**Hierarchy:**

- **Level 0:** `1. /workflow - Task` (no indent)
- **Level 1:** `3.1. /workflow - Subtask` (2-space indent)
- **Level 2:** `3.1.2. /workflow - Sub-subtask` (4-space indent)

**Good Examples:**

```typescript
{ step: "1. /plan - Create implementation plan", status: "in_progress" }
{ step: "2. /research - Gather best practices", status: "pending" }
{ step: "  2.1. /research - Search codebase", status: "pending" }
{ step: "  2.2. /research - Run web searches", status: "pending" }
{ step: "3. /generate-plan - Structure implementation roadmap", status: "pending" }
```

**Bad Examples:**

```typescript
// ❌ Missing workflow prefix
{ step: "1. Create plan", status: "in_progress" }

// ❌ No period after number
{ step: "1 /plan - Create plan", status: "in_progress" }

// ❌ Process description instead of deliverable
{ step: "1. /plan - Read files and write document", status: "in_progress" }

// ❌ Wrong workflow attribution (orchestrator vs executor)
{ step: "1. /work - Research best practices", status: "in_progress" }
// Should be: "1. /research - Gather best practices"
```

### Task Attribution Rule

**CRITICAL:** Tasks MUST be attributed to the workflow that **EXECUTES** them, not the workflow that **CALLS** them.

**Orchestrator vs Executor:**

- **Orchestrator tasks:** Coordination work (routing, protocol execution, state management)
- **Executor tasks:** Actual work delegated to specialized workflows

**Example:**

```typescript
// Top-level workflow: /work
update_plan({
  plan: [
    { step: "1. /detect-context - Analyze project state", status: "in_progress" },  // ✅ Executor
    { step: "2. /work-routing - Route to workflow", status: "pending" },  // ✅ Sub-workflow executor
    { step: "3. /implement - Execute implementation", status: "pending" },  // ✅ Executor
    { step: "4. /work - Detect work completion", status: "pending" },  // ✅ Orchestrator (checking state)
    { step: "5. /work-session-protocol - Session end protocol", status: "pending" }  // ✅ Sub-workflow
  ]
})
```

---

## Creating New Workflows

### Step-by-Step Guide

#### 1. Define Workflow Purpose

**Questions to answer:**

- What problem does this workflow solve?
- Is this an orchestrator, executor, or utility?
- What workflows will it call?
- What are success criteria?

#### 2. Choose Category and Template

**Templates:**

- `scripts/templates/workflow_orchestrator.md.j2` - For orchestrators
- `scripts/templates/workflow_executor.md.j2` - For executors
- `scripts/templates/workflow_utility.md.j2` - For utilities

#### 3. Define Task Granularity

**Guidelines:**

- **Short workflow (<2 min):** 2-3 tasks acceptable
- **Medium workflow (2-5 min):** 4-6 tasks recommended
- **Long workflow (>5 min):** 6-15 tasks (update every 30-60s)

**Each task should complete in 15-90 seconds.**

#### 4. Add Progress Announcements

**Checklist:**

- [ ] Workflow entry message (🔄)
- [ ] Stage entry messages for each stage
- [ ] Stage completion messages (📋)
- [ ] Sub-workflow delegation messages (↪️)
- [ ] Workflow exit message (✅)

#### 5. Document Sub-Workflow Calls

For each sub-workflow call, document:

- When it's called
- What it returns
- How to handle its output
- Task update pattern (before/after)

#### 6. Add Metadata

**Required frontmatter:**

```yaml
---
created: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
description: Brief one-line description
auto_execution_mode: 1-3
category: [Orchestrator|Executor|Utility]
complexity: 1-100
tokens: estimated-token-count
dependencies: [list, of, workflows]
status: [active|deprecated|experimental]
---
```

#### 7. Validate

**Checklist:**

- [ ] Markdown linting passes (`npx markdownlint-cli2 <file>`)
- [ ] Task format valid (if using examples)
- [ ] All stages have entry/completion messages
- [ ] Sub-workflow calls follow pattern
- [ ] Workflow entry/exit messages present

---

## Best Practices

### Granularity

**DO:**

- ✅ Break complex stages into observable substeps
- ✅ Update tasks every 30-90 seconds
- ✅ Print progress messages for long operations

**DON'T:**

- ❌ Have stages that take >2 minutes with no updates
- ❌ Create task plans with <3 steps for multi-minute work
- ❌ Update tasks too frequently (<15 seconds per task)

### Announcements

**DO:**

- ✅ Use consistent emoji standards
- ✅ Include specific details in messages ("5 sources analyzed")
- ✅ Print before AND after sub-workflow calls

**DON'T:**

- ❌ Over-announce every tiny operation
- ❌ Duplicate information (tasks already show status)
- ❌ Skip delegation announcements

### Task Descriptions

**DO:**

- ✅ Focus on deliverables ("Create ADR document")
- ✅ Include context in parentheses ("Update Section 1.11")
- ✅ Use action verbs (Create, Update, Analyze, Implement)

**DON'T:**

- ❌ Describe process ("Read file and write changes")
- ❌ Be vague ("Do Phase 2")
- ❌ Use wrong workflow attribution

---

## Examples

### Example 1: Simple Utility Workflow

```markdown
# Example Utility Workflow

**Purpose:** Load project context efficiently.

**Category:** Utility

---

## Stage 0: Workflow Entry

🔄 **Entering /load-context:** Loading project context

**Print workflow entry:**

```markdown
🔄 **Entering /load-context:** Loading project context with batch operations
```

---

## Stage 1: Load Files

[... implementation ...]

**Print workflow exit:**

```markdown
✅ **Completed /load-context:** Context loaded (5 files in 2 batches)
```

---

### Example 2: Complex Orchestrator Workflow

```markdown
# Example Orchestrator Workflow

**Purpose:** Coordinate multi-phase planning.

**Category:** Orchestrator

---

## Stage 0: Create Task Plan

🔄 **Entering /plan:** Research-driven planning

```typescript
update_plan({
  explanation: "🔄 Starting /plan workflow",
  plan: [
    { step: "1. /plan - Define requirements", status: "in_progress" },
    { step: "2. /plan - Research best practices", status: "pending" },
    { step: "3. /plan - Generate structured plan", status: "pending" }
  ]
})
```

---

## Stage 2: Research Phase

🔄 **Entering Stage 2: Research Phase**

**Before calling /research:**

```typescript
update_plan({
  explanation: "↪️ Delegating to /research",
  plan: [
    { step: "1. /plan - Define requirements", status: "completed" },
    { step: "2. /plan - Research best practices", status: "in_progress" },
    { step: "  2.1. /research - Gather findings", status: "in_progress" },
    { step: "3. /plan - Generate structured plan", status: "pending" }
  ]
})
```

**Print delegation:**

```markdown
↪️ **Delegating to /research:** Gathering best practices
```

**After /research returns:**

```markdown
📋 **Research Complete:** 5 sources analyzed
```

```typescript
update_plan({
  explanation: "Research complete",
  plan: [
    { step: "2. /plan - Research best practices", status: "completed" },
    { step: "  2.1. /research - Gather findings", status: "completed" },
    { step: "3. /plan - Generate structured plan", status: "in_progress" }
  ]
})
```

---

## Workflow Exit

```markdown
✅ **Completed /plan:** Planning complete, implementation ready
```

---

## Workflow Metrics

Track these metrics to assess workflow quality:

### Transparency Metrics

- **Progress announcements:** 100% (entry + exit minimum)
- **Sub-workflow visibility:** 100% (all calls shown in task list)
- **Task update frequency:** ≥1 update per 2 minutes
- **Tool call overhead:** ≤15% increase

### Quality Metrics

- **Average task duration:** 30-90 seconds (good granularity)
- **User comprehension:** Reduced "what's it doing?" questions
- **Debugging efficiency:** Can identify stall points
- **Trust score:** Users confident in agent operations

---

## Validation Tools

### Manual Validation

```bash
# Check markdown linting
npx markdownlint-cli2 .windsurf/workflows/<workflow>.md

# Verify task format (if examples included)
python scripts/validate_task_format.py --file <workflow>.md
```

### Automated Validation

Pre-commit hooks automatically validate:

- Markdown linting (markdownlint-cli2)
- Task format compliance (validate_task_format.py)

**Note:** Some orchestrator coordination tasks may be flagged by validators but are legitimate operations.

---

## References

### Internal Documentation

- [Agent Directives Section 1.11](.../rules/00_agent_directives.md) - Task system requirements
- [ADR-0018: Workflow Architecture V3](../../docs/adr/0018-workflow-architecture-v3.md) - Design decisions
- [ADR-0002: Workflow System](../../docs/adr/0002-adopt-windsurf-workflow-system.md) - Original adoption
- [Initiative: Transparency Improvements](../../docs/initiatives/active/2025-10-19-workflow-transparency-improvements/initiative.md)

### External Best Practices

- [Azure AI Agent Service Patterns](https://learn.microsoft.com/en-us/azure/ai-services/) - AI agent orchestration
- [AWS Step Functions Best Practices](https://docs.aws.amazon.com/step-functions/) - Workflow state management
- [Anthropic Agentic Workflows](https://www.anthropic.com/research/) - LLM agent patterns

---

## FAQ

### Q: When should I create a new workflow vs extending existing?

**A:** Create new if:

- Distinct purpose not covered by existing workflows
- Would require significant changes to existing workflow
- Reusability across multiple scenarios

Extend existing if:

- Adding a new stage to current flow
- Enhancing granularity of existing stages
- Minor feature addition

### Q: How granular should task breakdowns be?

**A:** Aim for **30-90 second task completion time**. If a task takes >2 minutes, break it into subtasks.

### Q: Should I add progress announcements to utility workflows?

**A:** Yes, but minimal:

- Entry message (always)
- Exit message (always)
- Skip stage messages if <30 seconds total

### Q: What if my workflow doesn't call sub-workflows?

**A:** That's fine! Just follow the other transparency requirements (entry/exit/stage messages).

### Q: Can I skip the task system for quick operations?

**A:** Yes, for:

- Single-step operations (<1 minute)
- Direct tool calls with no logic
- User explicitly requests no planning

### Q: How do I handle errors in workflows?

**A:** Print error announcement with ❌ emoji, update task to failed status, and return structured error.

---

**Version:** 1.0.0
**Last Updated:** 2025-10-19
**Maintained By:** mcp-web core team
