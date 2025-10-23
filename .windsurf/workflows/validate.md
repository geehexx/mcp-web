---
description: Validate code quality, security, and tests before committing
title: Quality Validation Workflow
type: workflow
category: Validation
complexity: moderate
dependencies: []
status: active
created: 2025-10-22
updated: 2025-10-22
---

# Quality Validation Workflow

**Purpose:** Comprehensive validation of code quality, security, and tests before committing changes.

**Invocation:** `/validate` or called automatically by `/commit`

## Prerequisites

- [ ] Code changes are staged or committed
- [ ] Tests are written and passing
- [ ] Dependencies are up to date

## Validation Steps

### 1. Code Quality Checks

```bash
# Linting and formatting
task lint
task format

# Type checking
task type-check

# Security scanning
task security:bandit
task security:semgrep
```

### 2. Test Validation

```bash
# Run all tests
task test:unit
task test:integration

# Coverage check
task test:coverage

# Security tests
task test:security
```

### 3. Documentation Validation

```bash
# Documentation linting
task docs:lint

# Link checking
task docs:links
```

### 4. Performance Checks

```bash
# Performance benchmarks
task test:benchmark

# Memory usage
task test:memory
```

## Expected Output

- ✅ All linting passes
- ✅ All tests pass
- ✅ Coverage ≥90%
- ✅ No security vulnerabilities
- ✅ Documentation is valid
- ✅ Performance within limits

## Success Criteria

Validation passes if:

1. Zero linting errors
2. Zero test failures
3. Coverage threshold met
4. No security issues
5. Documentation is complete

## Failure Handling

If validation fails:

1. Fix issues identified
2. Re-run validation
3. Do not proceed until all checks pass

## Integration

**Called By:**

- `/commit` workflow (mandatory)
- `/implement` workflow (after implementation)
- Manual invocation

**Calls:**

- Various task commands for validation
- Security scanning tools
- Test runners

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Security Practices**: `/rules/06_security_practices.mdc` - Apply when dealing with security-sensitive code including API calls, user input, LLM interactions, and authentication
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files, complex operations, or memory-intensive tasks
- **Testing Standards**: `/rules/02_testing.mdc` - Apply when validating test coverage and test quality

## Workflow References

When this validation workflow is called by other workflows:

1. **Load**: `/commands/validate.md`
2. **Execute**: Follow the validation steps defined above
3. **Report**: Document validation results
4. **Chain**: Proceed to commit workflow if validation passes

## Anti-Patterns

❌ **Don't:**

- Skip validation steps
- Ignore security warnings
- Commit with failing tests
- Bypass coverage requirements

✅ **Do:**

- Run full validation before commits
- Address all security issues
- Maintain high test coverage
- Keep documentation up to date

---

## Command Metadata

**File:** `validate.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~800
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Code quality validation
- Security scanning
- Test validation
- Documentation checks
- Performance validation

**Dependencies:**

- task commands for validation
- Security scanning tools
- Test frameworks
