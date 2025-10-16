---
description: Focused implementation with test-first approach
auto_execution_mode: 3
---

# Implementation Workflow

**Purpose:** Execute planned work with test-first discipline and incremental validation.

**Invocation:** `/implement [optional: context or initiative file]`

**Philosophy:** Small steps, test immediately, commit frequently.

---

## Prerequisites

**Before starting:**

- [ ] Plan exists (from `/plan` or initiative file)
- [ ] Requirements clear
- [ ] Tests identified (what to verify)
- [ ] Context loaded (related files read)

**If no plan exists:** Invoke `/plan` first for non-trivial work.

---

## Stage 1: Setup & Context Loading

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
mcp0_read_multiple_files([
    # Source files to modify
    "src/mcp_web/module.py",

    # Related source for context
    "src/mcp_web/related.py",

    # Test files
    "tests/unit/test_module.py",

    # Documentation
    "docs/API.md",
])
```text

### 1.3 Check Current State

```bash
# Git status
git status

# Run relevant tests (establish baseline)
task test:fast
```text

---

## Stage 2: Test-First Implementation

### 2.1 Write Test FIRST

**Before any production code:**

1. **Write failing test**

   ```python
   def test_new_feature():
       """Test for feature X."""
       result = new_feature()
       assert result == expected
   ```text

2. **Run test (verify it fails)**

   ```bash
   uv run pytest tests/path/to/test.py::test_new_feature -xvs
   ```text

3. **Confirm failure reason**
   - Not implemented yet? ✓ Good
   - Wrong failure reason? Fix test first

### 2.2 Implement Minimum Code

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

### 2.3 Verify Test Passes

```bash
uv run pytest tests/path/to/test.py::test_new_feature -xvs
```text

**If fails:** Debug, fix, re-test (don't proceed)
**If passes:** Continue to refactor

### 2.4 Refactor (If Needed)

**Now improve code quality:**

- Extract functions
- Improve names
- Add docstrings
- Follow patterns

**But:** Re-run test after each change

---

## Stage 3: Expand Coverage

### 3.1 Add Edge Case Tests

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

### 3.2 Integration Tests (If Needed)

**For cross-module features:**

```python
# tests/integration/test_feature_integration.py
def test_feature_with_module_b():
    """Test feature X integrated with module B."""
    # Integration test
```text

---

## Stage 4: Documentation

### 4.1 Update API Documentation

**If public API changed:**

```markdown
## Update docs/API.md

Add:
- New function signatures
- Usage examples
- Error cases
```text

### 4.2 Update README (If Needed)

**For user-facing features:**

```markdown
## Update README.md

Add:
- Installation steps (if dependencies added)
- Usage examples
- Configuration options
```text

### 4.3 Inline Documentation

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

## Stage 5: Quality Gates

### 5.1 Run All Tests

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

### 5.2 Linting

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

### 5.3 Security Scan (If Relevant)

```bash
# For security-sensitive code
task security

# Specific scans
task security:bandit
task security:semgrep
```text

---

## Stage 6: Commit Strategy

### 6.1 Atomic Commits

**One logical change per commit:**

✅ **Good:**

```bash
git add src/mcp_web/auth.py tests/unit/test_auth.py
git commit -m "feat(auth): add API key validation

- Add APIKey Pydantic model
- Add validation function with bcrypt
- Add 15 unit tests (100% coverage)
- Follows OWASP API security guidelines

Refs: docs/initiatives/active/2025-10-15-api-key-auth.md"
```text

❌ **Bad:**

```bash
git add .
git commit -m "wip"
```text

### 6.2 Use `/commit` Workflow

**For guided commits:**

```bash
# Review changes
/commit

# Workflow will:
# 1. Show git diff
# 2. Verify ownership
# 3. Guide commit message
# 4. Run pre-commit hooks
```text

---

## Stage 7: Progress Tracking

### 7.1 Update Initiative

**Mark completed tasks:**

```markdown
## Tasks

- [x] Create auth.py module ✓
- [x] Add validation function ✓
- [x] Unit tests (15 tests) ✓
- [ ] Integration with FastAPI
- [ ] CLI key management
```text

### 7.2 Document Decisions

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

### ❌ Don't: Implement Without Tests

**Bad:**

```markdown
1. Write all code
2. Then write tests
3. Find bugs
4. Fix bugs
5. Find more bugs
```text

**Good:**

```markdown
1. Write one test
2. Implement that feature
3. Test passes
4. Next test
```text

### ❌ Don't: Batch Too Many Changes

**Bad:**

```bash
# 50 files changed, 2000+ lines
git commit -m "add feature"
```text

**Good:**

```bash
# 3 files changed, 50 lines
git commit -m "feat(auth): add validation"

# 2 files changed, 30 lines
git commit -m "feat(auth): add CLI commands"
```text

### ❌ Don't: Skip Testing After Refactor

**Bad:**

```markdown
Refactor code → Looks good → Move on
(broke something, didn't notice)
```text

**Good:**

```markdown
Refactor code → Run tests → Verify green → Move on
```text

### ❌ Don't: Ignore Linting Failures

**Bad:**

```bash
$ task lint
ERROR: 5 linting issues
$ git commit  # Commit anyway
```text

**Good:**

```bash
$ task lint
ERROR: 5 linting issues
$ task format  # Auto-fix
$ task lint  # Verify clean
$ git commit
```text

---

## Progress Reporting

### Checkpoint Format

**Every hour or phase completion:**

```markdown
## Checkpoint: [Feature Name] - [Phase]

**Completed:**
- ✓ Task 1
- ✓ Task 2
- ✓ Task 3

**Status:**
- Tests: 45/50 passing (5 new, all green)
- Coverage: 95% (+5% from start)
- Lint: Clean (was 3 issues, fixed)

**Next Steps:**
1. Task 4 (estimated 30 min)
2. Task 5 (estimated 45 min)

**Blockers:** None
```text

---

## Integration with Other Workflows

### Called By

- `/work` - When implementation needed
- `/plan` - After plan approved
- User - Direct invocation

### Calls

- `/test-before-commit` - After each change
- `/commit` - When ready to commit
- `/new-adr` - If architectural decision needed

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
- Project: `.windsurf/rules/01_testing_and_tooling.md`

---

**Last Updated:** October 15, 2025
**Version:** 1.0
