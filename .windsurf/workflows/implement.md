---
created: "2025-10-17"
updated: "2025-10-21"
description: Focused implementation with test-first approach
auto_execution_mode: 3
category: Implementation
complexity: 75
tokens: 1400
dependencies:
  - load-context
  - validate
  - commit
status: active
---

# Implementation Workflow

**Purpose:** Execute planned work with test-first discipline and incremental validation.

**Category:** Orchestrator (implementation coordination)

**Invocation:** `/implement [optional: context or initiative file]`

**Philosophy:** Small steps, test immediately, commit frequently.

**Workflow Chain:** `/implement` → [test-first loop] → `/validate` → `/commit`

---

## Prerequisites

**Before starting:**

- [ ] Plan exists (from `/plan` or initiative file)
- [ ] Requirements clear
- [ ] Tests identified (what to verify)
- [ ] Context loaded (related files read)

**If no plan exists:** Invoke `/plan` first for non-trivial work.

---

## Workflow Execution

**Task plan:**
```typescript
update_plan({
  explanation: "🔄 Starting /implement",
  plan: [
    { step: "  3.1. /implement - Load context", status: "in_progress" },
    { step: "  3.2. /implement - Design test cases (TDD)", status: "pending" },
    { step: "  3.3. /implement - Write failing tests", status: "pending" },
    { step: "  3.4. /implement - Implement code", status: "pending" },
    { step: "  3.5. /implement - Verify tests pass", status: "pending" },
    { step: "  3.6. /implement - Run validation", status: "pending" },
    { step: "  3.7. /implement - Commit changes", status: "pending" }
  ]
})
```

**Numbering:** Use parent number if called by parent (e.g., `3.1.`), top-level if direct (e.g., `1.`)

**Adjust plan based on work scope** (e.g., remove test steps for documentation-only changes).

---

## Stage 2: Setup & Context Loading

### 1.1 Load Initiative Context

**If initiative provided:**

```markdown
Read initiative file:
- Current phase
- Unchecked tasks
- Acceptance criteria
- References
```text

**If no initiative:**

```markdown
Clarify:
- What to implement?
- Expected behavior?
- How to verify?
```text

### 1.2 Identify Files

**Batch read relevant files:**

```python
# IMPORTANT: MCP tools require absolute paths
mcp0_read_multiple_files([
    # Source files to modify
    "/home/gxx/projects/mcp-web/src/mcp_web/module.py",

    # Related source for context
    "/home/gxx/projects/mcp-web/src/mcp_web/related.py",

    # Test files
    "/home/gxx/projects/mcp-web/tests/unit/test_module.py",

    # Documentation
    "/home/gxx/projects/mcp-web/docs/API.md",
])
```text

### 1.3 Check Current State

```bash
# Git status
git status

# Run relevant tests (establish baseline)
task test:fast
```

**Print stage completion:**

```markdown
📋 **Stage 2 Complete:** Context loaded, baseline established
```

---

## Stage 2.5: Check ADR Requirement (Conditional)

**Before implementing, assess if ADR needed:**

| Scenario | ADR? | Examples |
|----------|------|----------|
| New dependency/library | ✅ | httpx, redis, playwright |
| Security decision | ✅ | Auth strategy, encryption |
| Performance-critical | ✅ | Caching strategy, parallelism |
| API contract | ✅ | REST design, GraphQL schema |
| Core architecture | ✅ | Event-driven, microservices |
| Algorithm/implementation | ❌ | Sort choice, code patterns |
| Bug fix | ❌ | Just fix and test |

**If ADR needed:** Call `/new-adr` workflow (add to task plan, delegate, document decision, then proceed)
**If no ADR:** Continue to Stage 3

**IMPORTANT:** Document architectural decisions BEFORE implementing.

---

## Stage 3: Test-First Implementation

### 3.1 Write Test FIRST

**Before any production code:**

1. **Write failing test**

   ```python
   def test_new_feature():
       """Test for feature X."""
       result = new_feature()
       assert result == expected
   ```

2. **Run test (verify it fails)**

   ```bash
   uv run pytest tests/path/to/test.py::test_new_feature -xvs
   ```

3. **Confirm failure reason**

   - Not implemented yet? ✓ Good
   - Wrong failure reason? Fix test first

### 3.2 Implement Minimum Code

**Write simplest code to pass test:**

```python
def new_feature():
    """Implement feature X.

    See: Initiative docs/initiatives/active/feature-x.md
    Tests: tests/unit/test_module.py::test_new_feature
    """
    # Minimal implementation
    return expected
```text

**DO NOT:**

- Add extra features
- Optimize prematurely
- Handle untested edge cases

### 3.3 Verify Test Passes

```bash
uv run pytest tests/path/to/test.py::test_new_feature -xvs
```text

**If fails:** Debug, fix, re-test (don't proceed)
**If passes:** Continue to refactor

### 3.4 Refactor (If Needed)

**Now improve code quality:**

- Extract functions
- Improve names
- Add docstrings
- Follow patterns

**But:** Re-run test after each change

---

## Stage 4: Expand Coverage

### 4.1 Add Edge Case Tests

**For each edge case:**

1. Write test
2. Run (verify fails or passes correctly)
3. Fix if needed
4. Move to next

**Common edge cases:**

- Empty input
- None/null values
- Boundary conditions
- Error conditions

### 4.2 Integration Tests (If Needed)

**For cross-module features:**

```python
# tests/integration/test_feature_integration.py
def test_feature_with_module_b():
    """Test feature X integrated with module B."""
    # Integration test
```text

---

## Stage 5: Documentation

### 5.1 Update API Documentation

**If public API changed:**

```markdown
## Update docs/API.md

Add:
- New function signatures
- Usage examples
- Error cases
```text

### 5.2 Update README (If Needed)

**For user-facing features:**

```markdown
## Update README.md

Add:
- Installation steps (if dependencies added)
- Usage examples
- Configuration options
```text

### 5.3 Inline Documentation

**Ensure docstrings complete:**

```python
def function(arg: type) -> return_type:
    """One-line summary.

    Longer description if needed.

    Args:
        arg: Description

    Returns:
        Description of return

    Raises:
        ErrorType: When error occurs

    Example:
        >>> function(value)
        result
    """
```text

---

## Stage 6: Quality Gates

### 6.1 Run All Tests

```bash
# Fast tests (must pass)
task test:fast

# Full tests if available
task test
```text

**Requirements:**

- Zero failures (except known async issues)
- Zero regressions
- New tests passing

### 6.2 Linting

```bash
# Auto-fix what's possible
task format

# Check remaining issues
task lint
```text

**Requirements:**

- Zero auto-fixable issues
- Address or suppress remaining
- Follow project style

### 6.3 Security Scan (If Relevant)

```bash
# For security-sensitive code
task security

# Specific scans
task security:bandit
task security:semgrep
```

**Print stage completion:**

```markdown
📋 **Stage 6 Complete:** All quality gates passed
```

---

## Stage 7: Commit Strategy

**Use `/commit` workflow for guided commits:**
- Atomic commits (one logical change)
- Conventional commit format
- References initiative file

**Good commit:** 3 files, 50 lines, descriptive message with bullet points
**Bad commit:** `git add . && git commit -m "wip"`

**See:** `.windsurf/workflows/commit.md`

---

## Stage 8: Progress Tracking

### 8.1 Update Initiative

**Mark completed tasks:**

```markdown
## Tasks

- [x] Create auth.py module ✓
- [x] Add validation function ✓
- [x] Unit tests (15 tests) ✓
- [ ] Integration with FastAPI
- [ ] CLI key management
```text

### 8.2 Document Decisions

**If architectural choice made:**

```markdown
## Updates

### 2025-10-15 (Session 1)

Completed Phase 1 (Core Authentication):
- Used bcrypt for password hashing (industry standard)
- Chose Bearer token format (RESTful convention)
- 100% test coverage achieved

**Decision:** Bcrypt over Argon2
**Reason:** Better library support, sufficient security for API keys

Next session: Phase 2 (CLI key management)
```text

---

## Incremental Validation Pattern

### The 15-Minute Rule

**Test every 15 minutes or less:**

```markdown
00:00 - Write test
00:05 - Implement feature
00:10 - Run test (verify pass)
00:15 - Refactor + retest
↓
Commit if green
↓
Next feature
```text

### The 3-File Rule

**After changing 3 files, run tests:**

```markdown
Modified:
1. src/mcp_web/auth.py
2. tests/unit/test_auth.py
3. src/mcp_web/models.py

→ RUN: task test:fast
```text

### The Red-Green-Refactor Cycle

```text
Write Test (RED) → Implement (GREEN) → Refactor (GREEN) → Commit
       ↑                                                      ↓
       └──────────────────────────────────────────────────────┘
                        Next Feature
```text

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| Implement without tests | Write test first (TDD) |
| Batch 50 files in one commit | Atomic commits (3-5 files) |
| Skip testing after refactor | Always re-run tests |
| Ignore linting failures | Fix with `task format` before commit |
| Large infrequent commits | Commit every 30-60 minutes |
| Write all code then test | Test-driven development (RED-GREEN-REFACTOR) |

---

## Progress Reporting

**Every hour or phase completion:** Update initiative document with completed tasks, test status, and blockers (if any).

---

## Integration with Other Workflows

### Called By

- `/work` - When implementation needed
- `/plan` - After plan approved
- User - Direct invocation

### Calls

- `/new-adr` - If architectural decision during implementation (Stage 2.5, conditional)
- `/test-before-commit` - After each change
- `/commit` - When ready to commit (Stage 7)

**Print workflow exit:**

```markdown
✅ **Completed /implement:** Implementation finished, all tests passing, changes committed
```

---

## Success Metrics

✅ **Good Implementation:**

- Tests written first (or simultaneously)
- Commits every 30-60 minutes
- Zero failing tests
- Lint clean
- Documentation updated

❌ **Poor Implementation:**

- Tests written after code
- Large infrequent commits
- Failing tests ignored
- Lint issues accumulating
- Missing documentation

---

## References

- [Test-Driven Development (TDD)](https://martinfowler.com/bliki/TestDrivenDevelopment.html)
- [Agentic TDD Best Practices (2025)](https://www.latent.space/p/anita-tdd)
- [Red-Green-Refactor Cycle](https://www.jamesshore.com/v2/books/aoad1/test_driven_development)
- Project: `.windsurf/workflows/test-before-commit.md`
- Project: `.windsurf/rules/02_testing.md`

---

**Last Updated:** October 21, 2025
**Version:** 2.0.0
