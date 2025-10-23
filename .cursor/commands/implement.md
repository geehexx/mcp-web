---
pass_through: true
description: Focused implementation with test-first approach
title: Implementation Workflow
tags: ['implementation', 'testing', 'development', 'tdd']
---

related: []

# Implementation Workflow

**Purpose:** Execute planned work with test-first discipline and incremental validation.

**Invocation:** `/implement [optional: context or initiative file]`

**Philosophy:** Small steps, test immediately, commit frequently.

**Workflow Chain:** `/implement` → [test-first loop] → `/validate` → `/commit`

## Prerequisites

**Before starting:**

- [ ] Plan exists (from `/plan` or initiative file)
- [ ] Requirements clear
- [ ] Tests identified (what to verify)
- [ ] Context loaded (related files read)

**If no plan exists:** Invoke `/plan` first for non-trivial work.

## Workflow Execution

### Stage 1: Setup & Context Loading

**Load Context** (`/load-context`):

- Initiative: initiative + related files
- Planning: full project context
- Module: specific module files

**Identify Files:**

```python
# IMPORTANT: MCP tools require absolute paths
mcp0_read_multiple_files([
    # Source files to modify
    "/home/gxx/projects/mcp-web/src/mcp_web/module.py",
    # Test files
    "/home/gxx/projects/mcp-web/tests/test_module.py",
    # Configuration files
    "/home/gxx/projects/mcp-web/pyproject.toml"
])
```

### Stage 2: Test-First Implementation Loop

**For each planned task:**

1. **Write Failing Test** (Red)
   - Test the specific behavior you're implementing
   - Run test to confirm it fails
   - Commit: `test: add failing test for [feature]`

2. **Implement Feature** (Green)
   - Write minimal code to make test pass
   - Run test to confirm it passes
   - Commit: `feat: implement [feature]`

3. **Refactor** (Refactor)
   - Improve code without changing behavior
   - Run tests to confirm they still pass
   - Commit: `refactor: improve [feature] implementation`

**Loop until all planned tasks complete.**

### Stage 3: Validation

**Call** `/validate`:

- Run all tests
- Check linting
- Verify type checking
- Security checks

### Stage 4: Commit

**Call** `/commit`:

- Stage all changes
- Create conventional commit message
- Push to repository

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Python Code Standards**: `/rules/01_python_code.mdc` - Apply when writing Python code
- **Testing Standards**: `/rules/02_testing.mdc` - Apply when writing and running tests
- **Security Practices**: `/rules/06_security_practices.mdc` - Apply when dealing with security-sensitive code
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations

## Workflow References

When this implementation workflow is called:

1. **Load**: `/commands/implement.md`
2. **Execute**: Follow the test-first implementation stages
3. **Validate**: Run validation checks
4. **Commit**: Commit changes with proper messages

## Anti-Patterns

❌ **Don't:**

- Skip writing tests first
- Implement large features in one go
- Skip validation steps
- Commit without proper messages

✅ **Do:**

- Write failing tests first (Red-Green-Refactor)
- Implement small, incremental changes
- Validate after each major change
- Use conventional commit messages

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Test coverage | ≥90% | ✅ |
| Implementation time | <2h per feature | ✅ |
| Validation passes | 100% | ✅ |
| Commit frequency | Every 15-30min | ✅ |

## Integration

**Called By:**

- `/work` - Main orchestration workflow
- User - Direct invocation for implementation

**Calls:**

- `/load-context` - Load relevant files
- `/validate` - Validate implementation
- `/commit` - Commit changes

**Exit:**

```markdown
✅ **Completed /implement:** Implementation workflow finished
```

## Command Metadata

**File:** `implement.yaml`
**Type:** Command/Workflow
**Complexity:** Complex
**Estimated Tokens:** ~1,800
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Test-driven development
- Implementation patterns
- Validation processes
- Commit practices

**Dependencies:**

- /load-context - Load relevant files
- /validate - Validate implementation
- /commit - Commit changes
