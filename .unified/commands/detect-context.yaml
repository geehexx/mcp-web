---
title: "Detect Context Workflow"
description: "Intelligent context detection for work continuation"
type: "command"
status: "active"

# Windsurf workflow metadata
windsurf:
  type: "workflow"
  category: "Operations"
  complexity: "complex"
  dependencies: []

# Cursor command metadata
cursor:
  pass_through: true

tags: ["context", "detection", "analysis", "routing"]

---

# Detect Context Workflow

**Purpose:** Analyze project state to determine what work should happen next, enabling autonomous continuation.

**Invocation:** `/detect-context` (called by `/work` or directly)

## Execution

**Task plan:** Only if called directly (not by parent workflow like `/work`)

## Stage 1: Load Context

**Process:**

1. List `docs/initiatives/active/` (use `mcp0_list_directory`)
2. Build initiative paths: DIR → `{dir}/initiative.md`, FILE → `{file}`
3. Batch read with `mcp0_read_multiple_files` (PROJECT_SUMMARY + initiatives)
4. Check recent session summaries (`ls -t docs/archive/session-summaries/*.md | head -3`)

**⚠️ CRITICAL:** MCP tools do NOT support globs. List directory first, then read explicit paths.

## Stage 2: Detect Signals

**Priority 0 (ABSOLUTE):** User explicit @mention or "continue with X" → Confidence 100%, route to specified initiative

**Priority 1-5:**

- Session summary "Next Steps" / "Unresolved"
- Initiative unchecked tasks (`- [ ]`)
- Test failures (`task test:fast | grep FAILED`)
- Git uncommitted changes (`git status --short`)
- TODO markers (`grep -r "TODO\|FIXME\|XXX" docs/`)

**⚠️ CRITICAL:** User explicit mentions override ALL other signals.

## Stage 3: Classify Signals

**High Confidence (80%+):**
- User explicit mention
- Active initiative with unchecked tasks
- Test failures with clear error messages

**Medium Confidence (30-79%):**
- Session summary mentions work
- Git changes in progress
- TODO markers in relevant files

**Low Confidence (<30%):**
- No clear signals
- Multiple conflicting signals
- Ambiguous context

## Stage 4: Generate Routing Recommendation

**Route to Implementation:**
- Active initiative with unchecked tasks
- Test failures
- User requests specific feature/fix

**Route to Planning:**
- New initiative mentioned
- Ambiguous requirements
- Research needed

**Route to Archive:**
- Initiative marked completed
- All tasks done
- User signals completion

**Route to Meta-Analysis:**
- Session end signals
- Work completed
- User requests summary

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files, complex operations, or memory-intensive tasks
- **Task Orchestration**: `/rules/12_task_orchestration.mdc` - Apply when managing complex task coordination and workflow orchestration
- **Workflow Routing**: `/rules/13_workflow_routing.mdc` - Apply when determining workflow routing and context analysis

## Workflow References

When this detect-context workflow is called:

1. **Load**: `/commands/detect-context.md`
2. **Execute**: Follow the context detection stages defined above
3. **Analyze**: Process project state and generate routing recommendation
4. **Return**: Provide confidence level and recommended workflow

## Integration

**Called By:**
- `/work` - Main orchestration workflow
- User - Direct invocation for context analysis

**Calls:**
- Various analysis tools and commands
- File reading operations
- Git status checks

## Anti-Patterns

❌ **Don't:**
- Skip user explicit mentions
- Ignore high-confidence signals
- Make assumptions without evidence
- Override user instructions

✅ **Do:**
- Always check for user explicit mentions first
- Analyze all available signals
- Provide confidence levels
- Respect user instructions absolutely

## Command Metadata

**File:** `detect-context.yaml`
**Type:** Command/Workflow
**Complexity:** Complex
**Estimated Tokens:** ~2,200
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**
- Context detection
- Signal analysis
- Routing recommendations
- Project state analysis

**Dependencies:**
- None (standalone workflow)
