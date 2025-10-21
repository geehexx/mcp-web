---
created: "2025-10-17"
updated: "2025-10-21"
description: Test-driven implementation workflow
auto_execution_mode: 3
category: Development
complexity: 75
tokens: 1880
version: v2.0-intelligent-semantic-preservation
dependencies:
  - load-context
  - validate
  - commit
status: active
---

# Implementation Workflow

**Purpose:** Implement features using test-driven development with quality gates.

**Invocation:** Called by `/work` when initiative detected or direct for focused implementation.

**Philosophy:** Tests define contract, implementation fulfills it, validation proves it.

**Workflow Chain:** `/implement` → [test-first loop] → `/validate` → `/commit`

---

## Prerequisites

**Before starting:**

- Initiative defined
- Context loaded (`/load-context`)
- Requirements understood (ADR if architectural)
- Success criteria identified

**If missing:** Pause, clarify before proceeding.

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

## Stage 1: Design Test Cases

**Before code, design comprehensive tests:**

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

### Stage 2: Write Failing Tests

1. Create test file (if needed)
2. Write test functions from designed cases
3. Run: `task test:fast` or `pytest path/to/test_file.py`
4. Verify fails with expected errors (not syntax)

**Quality:** Tests fail for RIGHT reason (missing feature, not broken test).

### Stage 3: Implement Feature

**Write minimal code to pass tests:**

1. Implement feature
2. Follow standards (`.windsurf/rules/01_python_code.md`)
3. Add docstrings and type hints
4. Keep focused and testable

**Red-Green-Refactor:**

```python
def new_feature():
    """Implement feature X.

    See: Initiative docs/initiatives/active/feature-x.md
    Tests: tests/unit/test_module.py::test_new_feature
    """
    # Minimal implementation
    return expected
```

---

## Stage 4: Validate

**Call `/validate`:** Formatting, linting, tests (fast + full), security

**If fails:** Fix before commit.

**If passes:** Proceed to commit.

---

## Stage 5: Commit Strategy

**Use `/commit` workflow for guided commits:**

- Atomic commits (one logical change)
- Conventional commit format
- References initiative file

**Good commit:** 3 files, 50 lines, descriptive message with bullet points
**Bad commit:** `git add . && git commit -m "wip"`

**See:** `.windsurf/workflows/commit.md`

---

## Stage 6: Quality Gates

### 6.1 Run All Tests

```bash
# Fast tests (must pass)
task test:fast

# Full tests if available
task test
```

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
```

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
```

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
```

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
```

### The 3-File Rule

**After changing 3 files, run tests:**

```markdown
Modified:
1. src/mcp_web/auth.py
2. tests/unit/test_auth.py
3. src/mcp_web/models.py

→ RUN: task test:fast
```

### The Red-Green-Refactor Cycle

```text
Write Test (RED) → Implement (GREEN) → Refactor (GREEN) → Commit
       ↑                                                      ↓
       └──────────────────────────────────────────────────────┘
                        Next Feature
```

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
✅ **Completed /implement:** Feature implemented and validated, all tests passing, changes committed
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

**Last Updated:** 2025-10-21
**Version:** v2.0-intelligent-semantic-preservation
