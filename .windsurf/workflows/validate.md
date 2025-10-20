---
description: Run linting, tests, security checks, cross-reference validation, normative core enforcement
---

# Validate Workflow

**Purpose:** Pre-commit quality gate workflow. Runs comprehensive checks (linting, tests, security) before committing or merging code.

**Category:** Specialized Operation (atomic quality gate)

**Invocation:** `/validate` (called by `/work`, `/implement`, `/commit`, or directly)

**Philosophy:** Catch issues early through automated validation gates.

**For detailed test commands and options, see:** [`docs/guides/testing-reference.md`](../../docs/guides/testing-reference.md)

---

## Stage 0: Create Task Plan

🔄 **Entering /validate workflow**

**Create task plan:**

```typescript
update_plan({
  explanation: "✅ Starting /validate workflow",
  plan: [
    { step: "1. /validate - Run linting checks", status: "in_progress" },
    { step: "2. /validate - Run fast tests", status: "pending" },
    { step: "3. /validate - Run documentation validation", status: "pending" },
    { step: "4. /validate - Run security checks", status: "pending" },
    { step: "5. /validate - Generate validation report", status: "pending" }
  ]
})
```

---

## When to Run

**Always run before:**

- Committing code
- Creating pull requests
- Merging to main branch
- Releasing versions

**Optional for:**

- Exploratory work
- Draft commits
- WIP branches

---

## Stage 1: Pre-Flight Checks

### 1.1 Verify Clean State (Optional)

```bash
# Check for uncommitted changes (warning only)
git status --short

# If unstaged changes present, warn but continue
# Validation runs on current file state, not just staged
```

### 1.2 Check Python Environment

```bash
# Verify uv is available
uv --version

# Check Python version
uv run python --version
```

---

## Stage 2: Linting

### 2.1 Ruff Format Check

**Check code formatting:**

```bash
task format:check
# Equivalent to: uv run ruff format --check .
```

**If fails:**

- Auto-fix available: Run `task format` to fix
- Report which files need formatting
- Continue to next check (don't halt)

### 2.2 Ruff Lint Check

**Check code style and errors:**

```bash
task lint
# Runs: ruff check, mypy, markdownlint
```

**If fails:**

- Auto-fix available: Run `task format` first
- Review remaining issues
- Suppress false positives if needed
- Continue to next check

### 2.3 Type Checking (mypy)

**Verify type hints:**

```bash
task lint:mypy
# Equivalent to: uv run mypy src/
```

**If fails:**

- Add missing type hints
- Use `# type: ignore` for false positives (with comment explaining why)
- Continue to next check

### 2.4 Documentation Linting

**Check markdown syntax:**

```bash
task docs:lint
# Equivalent to: npx markdownlint-cli2 "**/*.md"
```

**If fails:**

- Auto-fix: Run `task docs:fix`
- Review remaining issues
- Continue to next check

---

## Stage 3: Testing

### 3.1 Fast Tests

**Run unit tests in parallel:**

```bash
task test:fast
# Equivalent to: uv run pytest tests/unit tests/golden -n auto -x
```

**Configuration:**

- Runs unit and golden tests only
- Parallel execution (pytest-xdist)
- Stop on first failure (-x)

**If fails:**

- Review failure output
- Fix failing tests
- Re-run before continuing

### 3.2 Integration Tests (Conditional)

**If code changes affect integration:**

```bash
task test:integration
# Equivalent to: uv run pytest tests/integration -n auto
```

**Skip if:**

- Only documentation changes
- Only test changes (unit tests)
- Only configuration changes

### 3.3 Coverage Check

**Verify ≥90% coverage:**

```bash
task test:coverage
# Generates coverage report
```

**If below threshold:**

- Identify uncovered lines
- Add tests for critical paths
- Document why coverage is acceptable (if valid reason)

---

## Stage 4: Documentation Validation

### 4.1 Cross-Reference Validation

**Check workflow and documentation links:**

```bash
task docs:validate:links
# Validates:
# - Workflow internal cross-references (.windsurf/workflows/*.md)
# - ADR references (ADR-NNNN in .windsurf/ and docs/)
# - Ensures all referenced files exist
```

**If fails:**

- Fix broken workflow links
- Create missing ADR files
- Update references to use correct paths

---

## Stage 5: Security Checks

**Validate against security rules:** `.windsurf/rules/04_security.md`

### 5.0 Security Rules Checklist

**Manual review for security-sensitive code:**

- [ ] OWASP LLM Top 10 compliance (if LLM interactions)
- [ ] Input validation on all external inputs
- [ ] Output sanitization before display
- [ ] No hardcoded credentials or API keys
- [ ] Secrets loaded from environment variables
- [ ] SQL injection prevention (parameterized queries)
- [ ] Path traversal protection (validate file paths)
- [ ] Command injection prevention (avoid shell=True)
- [ ] Rate limiting on API endpoints
- [ ] Defense-in-depth approach

**See:** `.windsurf/rules/04_security.md` for complete security guidelines

**Automated checks below validate subset of these rules:**

### 5.1 Bandit (Python Security Linter)

**Scan for security issues:**

```bash
task security:bandit
# Equivalent to: uv run bandit -c .bandit -r src/
```

**Common issues caught:**

- Hardcoded passwords
- SQL injection risks
- Use of `eval()`, `exec()`
- Insecure random number generation
- Weak cryptography

**If fails:**

- Review each issue
- Fix security vulnerabilities
- Suppress false positives with `# nosec` and comment

### 5.2 Semgrep (Semantic Security Analysis)

**Advanced security patterns:**

```bash
task security:semgrep
# Equivalent to: uv run semgrep --config .semgrep.yml
```

**Patterns checked:**

- LLM injection risks (OWASP LLM01)
- Unsafe external fetches
- Path traversal
- Command injection

**If fails:**

- Critical issues: Must fix
- Medium/Low: Review and decide
- False positives: Add to ignore list

### 5.3 Dependency Audit

**Check for known vulnerabilities:**

```bash
task security:deps
# Equivalent to: uv run safety check
```

**If vulnerabilities found:**

- Update vulnerable dependencies
- Check if exploit is applicable to our usage
- Document risk acceptance if upgrade not possible

---

## Stage 6: Results Summary

### 6.1 Aggregate Results

**Collect all check results:**

```markdown
## Validation Results

### ✅ Passed
- Formatting (ruff format)
- Type checking (mypy)
- Unit tests (45/45 passing)
- Security (bandit, semgrep)

### ⚠️ Warnings
- Documentation lint: 2 minor issues
- Coverage: 88% (below 90% target)

### ❌ Failed
- Integration tests: 2/10 failing
  - test_playwright_fallback_timeout
  - test_concurrent_fetches

### Summary
Status: ❌ FAILED
Blocker: Integration tests must pass before commit
```

### 6.2 Exit Code Logic

**Determine overall status:**

```python
if critical_failures > 0:
    status = "FAILED"
    exit_code = 1
elif warnings > 0:
    status = "PASSED WITH WARNINGS"
    exit_code = 0  # Don't block commit
else:
    status = "PASSED"
    exit_code = 0
```

**Critical failures:**

- Any test failures
- Security issues (high/critical severity)
- Type errors (unless suppressed)

**Non-critical (warnings):**

- Formatting issues (auto-fixable)
- Documentation lint issues
- Coverage slightly below target (85-89%)

---

## Stage 7: Remediation Guidance

### 7.1 Fix Auto-Fixable Issues

**If auto-fixes available:**

```bash
# Fix formatting and linting
task format

# Fix documentation
task docs:fix

# Re-run validation
/validate
```

### 7.2 Manual Fix Guidance

**For test failures:**

```markdown
**Test Failure:** test_playwright_fallback_timeout

**Root Cause:** Playwright timeout set too low (5s)

**Fix:**
1. Increase timeout in tests/integration/conftest.py
2. Or: Mock slow network in test
3. Re-run: `uv run pytest tests/integration/test_playwright_fallback.py::test_playwright_fallback_timeout -xvs`
```

**For security issues:**

```markdown
**Security Issue:** [B303:blacklist] Use of insecure MD5 hash function

**Location:** src/mcp_web/cache.py:45

**Fix:**
1. Replace `hashlib.md5()` with `hashlib.sha256()`
2. Or: Add `# nosec` if MD5 is acceptable (e.g., non-cryptographic use)
3. Re-run: `task security:bandit`
```

---

## Integration Points

### 6.1 Called By

- `/work` - Before committing work
- `/implement` - After implementation phase
- `/commit` - Pre-commit validation
- CI/CD pipeline - On every push
- User - Direct invocation

### 6.2 Calls

- None (leaf workflow - calls tasks only)

---

## Examples

### Example 1: Clean Pass

```bash
$ /validate

Running validation checks...

✅ Format check (ruff)         PASSED
✅ Lint check (ruff)           PASSED
✅ Type check (mypy)           PASSED
✅ Unit tests                  PASSED (45/45)
✅ Security (bandit)           PASSED
✅ Security (semgrep)          PASSED

🎉 All checks passed! Ready to commit.
```

### Example 2: Auto-Fixable Issues

```bash
$ /validate

Running validation checks...

❌ Format check                FAILED (3 files need formatting)
⚠️  Lint check                 WARNINGS (5 auto-fixable issues)
✅ Type check                  PASSED
✅ Tests                       PASSED

Recommendation:
Run `task format` to auto-fix issues, then re-validate.

$ task format
Fixed 3 files, 5 issues

$ /validate
🎉 All checks passed!
```

### Example 3: Test Failures

```bash
$ /validate

Running validation checks...

✅ Format check                PASSED
✅ Lint check                  PASSED
✅ Type check                  PASSED
❌ Unit tests                  FAILED (2/45 failing)
   - test_cache_expiration: AssertionError
   - test_summarizer_empty_input: AttributeError

❌ VALIDATION FAILED
Fix failing tests before committing.

Debug failing tests:
$ uv run pytest tests/unit/test_cache.py::test_cache_expiration -xvs
```

---

## Optimization Strategies

### Parallel Execution

**Run independent checks in parallel:**

```bash
# Sequential (slow)
task format:check && task lint && task test:fast
# ~60 seconds

# Parallel (fast) - if supported by task runner
task format:check & task lint & task test:fast &
wait
# ~25 seconds
```

### Incremental Validation

**Only validate changed files:**

```bash
# Get changed files
changed_files=$(git diff --name-only HEAD)

# Run ruff only on changed files
uv run ruff check $changed_files

# Run pytest only for tests related to changed modules
uv run pytest --lf  # Last failed tests
```

### Caching

**Leverage pytest cache:**

```bash
# First run: ~20s
task test:fast

# Subsequent run (no code changes): ~2s
task test:fast  # Uses cache
```

---

## Anti-Patterns

### ❌ Don't: Skip Validation

**Bad:**

```bash
git commit -m "quick fix" --no-verify
git push
# CI fails, blocks team
```

**Good:**

```bash
/validate
# Fix issues
git commit -m "fix: resolve cache expiration bug"
```

### ❌ Don't: Ignore Warnings

**Bad:**

```markdown
⚠️ Coverage: 75% (below 90% target)
AI: "Proceeding anyway..."
```

**Good:**

```markdown
⚠️ Coverage: 75% (below 90% target)
AI: "Adding tests to reach 90% coverage..."
```

### ❌ Don't: Over-Suppress Issues

**Bad:**

```python
# type: ignore
# nosec
# noqa
# "It's fine, just ignore everything"
```

**Good:**

```python
# type: ignore[attr-defined]  # third-party library missing type stubs
# nosec B303  # MD5 used for non-cryptographic cache key only
```

---

## Configuration Files

**Validation behavior controlled by:**

- `pyproject.toml` - Ruff, mypy, pytest settings
- `.bandit` - Bandit security rules
- `.semgrep.yml` - Semgrep security patterns
- `pytest.ini` - Pytest configuration
- `.markdownlint-cli2.jsonc` - Markdown linting rules

---

## References

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Semgrep Documentation](https://semgrep.dev/docs/)
- Project: `Taskfile.yml`
- Project: `.windsurf/rules/01_testing_and_tooling.md`

---
