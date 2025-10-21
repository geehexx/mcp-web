---
created: "2025-10-17"
updated: "2025-10-21"
description: Run linting, tests, security checks, cross-reference validation, normative core enforcement
auto_execution_mode: 3
category: Validation
complexity: 62
tokens: 1900
dependencies: []
status: active
---

# Validate Workflow

**Purpose:** Pre-commit quality gate workflow. Runs comprehensive checks before committing or merging.

**Invocation:** `/validate` (called by `/work`, `/implement`, `/commit`, or directly)

**Philosophy:** Catch issues early through automated validation gates.

**For detailed test commands:** [`docs/guides/TESTING_REFERENCE.md`](../../docs/guides/TESTING_REFERENCE.md)

---

## When to Run

| Run Before | Optional For |
|------------|--------------|
| Committing code, PRs, Merging, Releases | Exploratory work, Draft commits, WIP branches |

---

## Stage 1: Create Task Plan

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

## Stage 2: Linting

| Check | Command | If Fails | Auto-Fix |
|-------|---------|----------|----------|
| **Format** | `task format:check` | Report files needing formatting | `task format` |
| **Lint** | `task lint` | Review issues, suppress false positives | `task format` |
| **Type Check** | `task lint:mypy` | Add type hints, use `# type: ignore` with comment | Manual |
| **Docs** | `task docs:lint` | Review issues | `task docs:fix` |

**Pre-flight checks:**

```bash
# Verify environment
uv --version && uv run python --version

# Optional: Check git status
git status --short
```

---

## Stage 3: Testing

### Fast Tests

```bash
task test:fast
# Runs: unit + golden tests in parallel, stops on first failure
```

**Configuration:** pytest-xdist parallel, `-x` stop on failure

### Integration Tests (Conditional)

```bash
task test:integration  # If code affects integration
```

**Skip if:** Documentation-only, test-only, or config-only changes

### Coverage Check

```bash
task test:coverage  # Target: ≥90%
```

**If below threshold:** Add tests for critical paths or document exception

---

## Stage 4: Documentation Validation

### Cross-Reference Validation

```bash
task docs:validate:links
```

**Validates:**

- Workflow internal cross-references (`.windsurf/workflows/*.md`)
- ADR references (ADR-NNNN in `.windsurf/` and `docs/`)
- All referenced files exist

**If fails:** Fix broken links, create missing ADRs, update paths

---

## Stage 5: Security Checks

**Validate against:** `.windsurf/rules/06_security_practices.md`

### Manual Review Checklist (Security-Sensitive Code)

- [ ] OWASP LLM Top 10 compliance (if LLM interactions)
- [ ] Input validation on external inputs
- [ ] Output sanitization before display
- [ ] No hardcoded credentials/API keys
- [ ] Secrets from environment variables
- [ ] SQL injection prevention (parameterized queries)
- [ ] Path traversal protection
- [ ] Command injection prevention (no `shell=True`)
- [ ] Rate limiting on API endpoints
- [ ] Defense-in-depth approach

### Automated Security Checks

| Tool | Command | Detects | Action on Failure |
|------|---------|---------|-------------------|
| **Bandit** | `task security:bandit` | Hardcoded passwords, SQL injection, `eval()`/`exec()`, weak crypto | Fix vulnerabilities, suppress with `# nosec` + comment |
| **Semgrep** | `task security:semgrep` | LLM injection (OWASP LLM01), unsafe fetches, path traversal, command injection | Critical: fix; Medium/Low: review; False positives: ignore list |
| **Safety** | `task security:deps` | Known vulnerabilities in dependencies | Update deps, document risk if upgrade impossible |

---

## Stage 6: Results Summary

### Aggregate Results

```markdown
## Validation Results

### ✅ Passed
- Formatting, Type checking, Unit tests (45/45), Security

### ⚠️ Warnings
- Documentation: 2 minor issues
- Coverage: 88% (below 90% target)

### ❌ Failed
- Integration tests: 2/10 failing

### Summary
Status: ❌ FAILED
Blocker: Integration tests must pass
```

### Exit Code Logic

```python
if critical_failures > 0:
    status = "FAILED"; exit_code = 1
elif warnings > 0:
    status = "PASSED WITH WARNINGS"; exit_code = 0
else:
    status = "PASSED"; exit_code = 0
```

**Critical failures:** Test failures, security issues (high/critical), type errors (unless suppressed)

**Non-critical warnings:** Formatting issues, doc lint, coverage 85-89%

---

## Stage 7: Remediation Guidance

### Auto-Fixable Issues

```bash
task format      # Fix formatting/linting
task docs:fix    # Fix documentation
/validate        # Re-run validation
```

### Manual Fixes

**Test failure example:**

```markdown
**Test:** test_playwright_fallback_timeout
**Root Cause:** Timeout too low (5s)
**Fix:** Increase timeout in conftest.py OR mock slow network
**Rerun:** `uv run pytest tests/integration/test_playwright_fallback.py::test_playwright_fallback_timeout -xvs`
```

**Security issue example:**

```markdown
**Issue:** [B303:blacklist] Use of insecure MD5
**Location:** src/mcp_web/cache.py:45
**Fix:** Replace with `sha256()` OR add `# nosec B303` if non-cryptographic use
**Rerun:** `task security:bandit`
```

---

## Optimization Strategies

### Parallel Execution

```bash
# Sequential: ~60s
task format:check && task lint && task test:fast

# Parallel: ~25s (if supported)
task format:check & task lint & task test:fast & wait
```

### Incremental Validation

```bash
# Only validate changed files
changed_files=$(git diff --name-only HEAD)
uv run ruff check $changed_files

# Run last failed tests only
uv run pytest --lf
```

### Caching

```bash
# First run: ~20s, subsequent (no changes): ~2s
task test:fast  # Leverages pytest cache
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| Skip validation (`--no-verify`) | Run `/validate` before commit |
| Ignore warnings (proceed at 75% coverage) | Add tests to reach 90% |
| Over-suppress (`# type: ignore`, `# nosec` everywhere) | Specific suppressions with comments: `# nosec B303 - MD5 for cache key only` |

---

## Integration Points

**Called By:** `/work`, `/implement`, `/commit`, CI/CD, User

**Calls:** None (leaf workflow)

---

## Examples

### Clean Pass

```bash
✅ Format (ruff)      PASSED
✅ Lint (ruff)        PASSED
✅ Type (mypy)        PASSED
✅ Tests              PASSED (45/45)
✅ Security (bandit)  PASSED
✅ Security (semgrep) PASSED

🎉 All checks passed! Ready to commit.
```

### Auto-Fixable Issues

```bash
❌ Format              FAILED (3 files)
⚠️  Lint               WARNINGS (5 auto-fixable)

→ Run `task format` then re-validate
```

### Test Failures

```bash
❌ Unit tests          FAILED (2/45)
   - test_cache_expiration: AssertionError
   
❌ VALIDATION FAILED - Fix tests before committing

Debug: uv run pytest tests/unit/test_cache.py::test_cache_expiration -xvs
```

---

## Configuration Files

- `pyproject.toml` - Ruff, mypy, pytest
- `.bandit` - Bandit security rules
- `.semgrep.yml` - Semgrep patterns
- `pytest.ini` - Pytest config
- `.markdownlint-cli2.jsonc` - Markdown linting

---

## References

- [Ruff](https://docs.astral.sh/ruff/)
- [mypy](https://mypy.readthedocs.io/)
- [pytest](https://docs.pytest.org/)
- [Bandit](https://bandit.readthedocs.io/)
- [Semgrep](https://semgrep.dev/docs/)
- Project: `Taskfile.yml`, `.windsurf/rules/02_testing.md`
