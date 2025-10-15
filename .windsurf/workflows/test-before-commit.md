---
description: AI agent testing workflow for incremental validation
auto_execution_mode: 3
---

# Test-Before-Commit Workflow

**Purpose:** Guide AI agents to test changes incrementally, preventing compound errors and reducing debugging time.

**Philosophy:** "Test early, test often" - validate changes before they accumulate into hard-to-debug problems.

---

## When to Test

### Critical Test Points

**MUST test immediately after:**

1. **Modifying production code**
   - Changed function signature
   - Altered business logic
   - Fixed a bug
   - Refactored structure

2. **Modifying test code**
   - Added new test
   - Changed test expectations
   - Updated test fixtures

3. **Modifying dependencies**
   - Updated `pyproject.toml` or `uv.lock`
   - Changed import statements
   - Added new packages

4. **Modifying configuration**
   - Changed `pytest.ini`, `pyproject.toml`, `Taskfile.yml`
   - Updated environment variables
   - Modified CI/CD scripts

### Recommended Test Points

**SHOULD test after:**

- Completing a logical unit of work (even if tests don't exist yet)
- Making multiple small changes (every 3-5 files)
- Before switching to a different task
- After resolving merge conflicts

---

## Testing Strategy

### Level 1: Fast Feedback (30 seconds - 2 minutes)

Run targeted fast tests immediately:

```bash
# If you changed a specific module
uv run pytest tests/unit/test_<module>.py -xvs

# If you changed security code
uv run pytest -m security -xvs

# If you modified multiple files
task test:fast
```

**Purpose:** Catch obvious errors (syntax, import, basic logic)

**When to use:** After every code change

### Level 2: Comprehensive Validation (2-10 minutes)

Run full test suite periodically:

```bash
# All tests except live/network tests
task test

# With coverage report
task test:coverage
```

**Purpose:** Catch integration issues, regressions, edge cases

**When to use:**
- Before committing
- After making 5+ changes
- Before pushing to remote
- End of work session

### Level 3: Quality Gates (10+ minutes)

Run full CI checks:

```bash
# Full CI simulation
task ci

# Or separately:
task lint
task format
task test:coverage
```

**Purpose:** Ensure production readiness

**When to use:**
- Before creating pull request
- After major refactoring
- Before releasing

---

## Decision Tree

```
Did you change production code?
├─ YES → Run Level 1 tests for that module
│        ├─ Tests PASS → Continue work
│        └─ Tests FAIL → Fix immediately (don't compound)
└─ NO → Did you change test code?
         ├─ YES → Run Level 1 tests for that test file
         │        ├─ Tests PASS → Continue
         │        └─ Tests FAIL → Fix test logic
         └─ NO → Did you change config?
                  └─ YES → Run Level 2 tests
                           └─ Check for unexpected changes

After 3-5 file changes → Run Level 2 tests
Before commit → Run Level 2 tests + linting
Before PR → Run Level 3 quality gates
```

---

## AI Agent Testing Protocol

### Protocol 1: Incremental Validation

```markdown
1. Make a focused change (1-3 related files)
2. Identify relevant test category:
   - unit → `task test:fast`
   - security → `uv run pytest -m security`
   - integration → needs LLM (defer to Level 2)
3. Run tests
4. IF tests fail:
   a. Read failure message carefully
   b. Fix root cause (not symptom)
   c. Re-run tests
   d. GOTO 4 if still failing
5. IF tests pass:
   a. Proceed to next change
   b. After 3-5 changes, run Level 2
```

### Protocol 2: Pre-Commit Validation

```markdown
Before running `git commit`:

1. Check git status
   ```bash
   git status
   ```

2. Review all changed files
   - Are all changes intentional?
   - Did you forget to add any files?

3. Run appropriate test level:
   ```bash
   # For minor changes (1-5 files)
   task test:fast

   # For major changes (6+ files, refactoring)
   task test
   ```

4. Run linting
   ```bash
   task lint
   ```

5. Fix any issues

6. If all pass, proceed with commit
```

### Protocol 3: Compound Error Prevention

```markdown
IF you find yourself debugging complex issues:

1. STOP making new changes
2. Identify the last known good state
   ```bash
   git log --oneline -5
   ```
3. Consider reverting to good state
   ```bash
   git diff HEAD~1  # Review what changed
   git checkout HEAD~1 -- <file>  # Revert specific file if needed
   ```
4. Re-apply changes incrementally with testing
5. Document the lesson learned
```

---

## Test Output Interpretation

### Successful Test Run

```
============================= test session starts ==============================
...
========================== 54 passed in 5.23s ===========================
```

**Action:** Continue work ✅

### Failed Tests (Fixable)

```
FAILED tests/unit/test_security.py::test_sanitize - AssertionError: ...
```

**Action:**
1. Read the assertion message
2. Fix the specific issue
3. Re-run the test
4. Don't proceed until passing

### Import Errors

```
ModuleNotFoundError: No module named 'new_package'
```

**Action:**
1. Check if package is in `pyproject.toml`
2. Run `uv sync`
3. Re-run tests

### Syntax Errors

```
SyntaxError: invalid syntax
```

**Action:**
1. Fix syntax immediately
2. Run `task lint` to catch others
3. Re-test

### Timeout/Hanging

```
++++++++++++++++++++++++++ Timeout ++++++++++++++++++++++++++
```

**Action:**
1. Kill the test (Ctrl+C)
2. Identify the hanging test
3. Check for infinite loops or missing mocks
4. Fix and re-run

---

## Common Anti-Patterns

### ❌ Anti-Pattern 1: "I'll test it all at the end"

**Problem:** Accumulates errors, hard to debug

**Solution:** Test after each logical change

### ❌ Anti-Pattern 2: "The tests are probably fine"

**Problem:** Assumptions lead to broken main branch

**Solution:** Always run tests, never assume

### ❌ Anti-Pattern 3: "I'll just commit and fix it later"

**Problem:** Pollutes git history, wastes others' time

**Solution:** Fix before committing

### ❌ Anti-Pattern 4: "These test failures are unrelated"

**Problem:** They're usually related

**Solution:** Investigate thoroughly

### ❌ Anti-Pattern 5: "I don't have time to run tests"

**Problem:** Creates more work later

**Solution:** Testing saves time in the long run

---

## Performance Optimization

### Parallel Testing (Default)

Tests run in parallel automatically:

```bash
# Uses all CPU cores
task test
task test:fast
```

### Test Selection

Run only affected tests:

```bash
# By marker
uv run pytest -m "unit and not slow"

# By path
uv run pytest tests/unit/test_cache.py

# By name pattern
uv run pytest -k "test_sanitize"

# Stop on first failure
uv run pytest -x
```

### Skipping Slow Tests

```bash
# Exclude slow tests
uv run pytest -m "not slow"

# Exclude network tests
uv run pytest -m "not requires_network"
```

---

## Integration with Development

### VSCode Integration

Add to `.vscode/settings.json`:

```json
{
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--tb=short"
  ],
  "python.testing.unittestEnabled": false,
  "python.testing.pytestEnabled": true
}
```

### Watch Mode (Optional)

For TDD workflow:

```bash
# Install pytest-watch
uv add --dev pytest-watch

# Run in watch mode
uv run ptw -- -x
```

---

## Troubleshooting

### Tests pass locally but fail in CI

**Causes:**
- Missing test fixtures
- Hardcoded paths
- Missing dependencies in `pyproject.toml`
- Environment-specific behavior

**Solution:**
```bash
# Run CI locally
task ci

# Check for implicit dependencies
uv run pytest --collect-only
```

### Tests are too slow

**Solutions:**
1. Use markers to separate fast/slow tests
2. Ensure pytest-xdist is enabled (it is by default)
3. Mock external services
4. Use fixtures efficiently

### Flaky tests

**Indicators:**
- Pass sometimes, fail sometimes
- Timing-dependent
- Order-dependent

**Solution:**
1. Identify flaky tests
2. Add proper fixtures/mocks
3. Use `pytest-repeat` to verify fix:
   ```bash
   uv run pytest --count=10 tests/path/to/flaky_test.py
   ```

---

## Success Criteria

A good testing workflow results in:

- ✅ **High first-pass rate:** Changes work correctly the first time
- ✅ **Fast feedback:** Know within seconds if something broke
- ✅ **Clear errors:** Test failures point directly to the problem
- ✅ **No broken commits:** Every commit passes tests
- ✅ **Confidence:** Can refactor without fear

---

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-xdist (Parallel Testing)](https://pytest-xdist.readthedocs.io/)
- [Test-Driven Development (TDD) with AI](https://www.builder.io/blog/test-driven-development-ai)
- [Agentic TDD Best Practices](https://www.latent.space/p/anita-tdd)

---

**Last Updated:** October 15, 2025
**Version:** 1.0
