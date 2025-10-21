---
created: "2025-10-17"
updated: "2025-10-21"
description: Comprehensive validation and quality checks
auto_execution_mode: 3
category: Quality
complexity: 70
tokens: 1650
version: v2.0-intelligent-semantic-preservation
dependencies: []
status: active
---

# Validate Workflow

**Purpose:** Run comprehensive quality checks before committing to catch issues early.

**Invocation:** Called by `/implement` after implementation or directly before commit.

**Philosophy:** Catch issues early through automated validation gates.

**For detailed test commands, see:** [`docs/guides/TESTING_REFERENCE.md`](../../docs/guides/TESTING_REFERENCE.md)

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "🔍 Starting /validate",
  plan: [
    { step: "1. /validate - Format check", status: "in_progress" },
    { step: "2. /validate - Lint", status: "pending" },
    { step: "3. /validate - Type check", status: "pending" },
    { step: "4. /validate - Tests", status: "pending" },
    { step: "5. /validate - Security", status: "pending" }
  ]
})
```

**When to run:**

| Scenario | Required? |
|----------|-----------|
| Committing code | ✅ Yes |
| Creating PRs | ✅ Yes |
| Merging to main | ✅ Yes |
| Releasing versions | ✅ Yes |
| Exploratory work | ❌ Optional |
| Draft commits | ❌ Optional |

---

## Stage 2: Pre-Flight Checks

### 2.1 Verify Environment

```bash
# Verify uv available
uv --version

# Check Python version
uv run python --version

# Check git status (warning only)
git status --short
```

---

## Stage 3: Linting

### 3.1 Format Check

```bash
task format:check
# Equivalent to: uv run ruff format --check .
```

**If fails:** Run `task format` to auto-fix

### 3.2 Lint Check

```bash
task lint
# Runs: ruff check, mypy, markdownlint
```

**If fails:** Review issues, run `task format` for auto-fixes

### 3.3 Type Checking

```bash
task lint:mypy
# Equivalent to: uv run mypy src/
```

**If fails:** Add type hints or use `# type: ignore` with justification

### 3.4 Documentation Linting

```bash
task docs:lint
# Equivalent to: npx markdownlint-cli2 "**/*.md"
```

**If fails:** Run `task docs:fix` for auto-fixes

---

## Stage 4: Testing

### 4.1 Fast Tests (Unit + Golden)

```bash
task test:fast
# Equivalent to: uv run pytest tests/unit tests/golden -n auto -x
```

**Configuration:**

- Parallel execution (pytest-xdist)
- Stop on first failure (-x)
- ~5-10 seconds typical runtime

### 4.2 Integration Tests (Conditional)

```bash
task test:integration
# Equivalent to: uv run pytest tests/integration -n auto
```

**Skip if:** Only docs/tests/config changes

### 4.3 Coverage Check

```bash
task test:coverage
# Verifies ≥90% coverage threshold
```

**If below threshold:** Add tests for critical paths or document justification

---

## Stage 5: Documentation Validation

### 5.1 Cross-Reference Validation

```bash
task docs:validate:links
```

**Validates:**

- Workflow internal cross-references (`.windsurf/workflows/*.md`)
- ADR references (ADR-NNNN format)
- File existence for all references

**If fails:** Fix broken links, create missing files, update references

---

## Stage 6: Security Checks

**Reference:** `.windsurf/rules/06_security_practices.md`

### 6.1 Security Checklist (Manual Review)

**For security-sensitive code:**

- [ ] OWASP LLM Top 10 compliance
- [ ] Input validation on external inputs
- [ ] Output sanitization before display
- [ ] No hardcoded credentials
- [ ] Secrets from environment variables
- [ ] SQL injection prevention
- [ ] Path traversal protection
- [ ] Command injection prevention
- [ ] Rate limiting on endpoints
- [ ] Defense-in-depth approach

### 6.2 Bandit (Python Security)

```bash
task security:bandit
# Equivalent to: uv run bandit -c .bandit -r src/
```

**Catches:**

- Hardcoded passwords
- SQL injection risks
- Use of `eval()`, `exec()`
- Weak cryptography
- Insecure random generation

### 6.3 Semgrep (Semantic Analysis)

```bash
task security:semgrep
# Equivalent to: uv run semgrep --config .semgrep.yml
```

**Patterns:**

- LLM injection risks (OWASP LLM01)
- Unsafe external fetches
- Path traversal
- Command injection

### 6.4 Dependency Audit

```bash
task security:deps
# Equivalent to: uv run safety check
```

**If vulnerabilities found:** Update dependencies or document risk acceptance

---

## Stage 7: Results Summary

### 7.1 Aggregate Results

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

### Summary
Status: ❌ FAILED
Blocker: Integration tests must pass before commit
```

### 7.2 Exit Determination

| Condition | Status | Exit Code |
|-----------|--------|-----------|
| Any test failures | FAILED | 1 |
| Security issues (high/critical) | FAILED | 1 |
| Type errors (not suppressed) | FAILED | 1 |
| Warnings only | PASSED WITH WARNINGS | 0 |
| All checks passed | PASSED | 0 |

---

## Stage 8: Remediation Guidance

### 8.1 Auto-Fix Commands

```bash
# Fix formatting and linting
task format

# Fix documentation
task docs:fix

# Re-run validation
/validate
```

### 8.2 Manual Fix Examples

**Test failure:**

```markdown
**Issue:** test_playwright_fallback_timeout
**Cause:** Timeout too low (5s)
**Fix:** Increase timeout or mock slow network
**Verify:** uv run pytest tests/integration/test_playwright_fallback.py -xvs
```

**Security issue:**

```markdown
**Issue:** [B303] Use of insecure MD5 hash
**Location:** src/mcp_web/cache.py:45
**Fix:** Replace with `hashlib.sha256()` or add `# nosec` with justification
**Verify:** task security:bandit
```

---

## Examples

### Example 1: Clean Pass

```bash
$ /validate

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

❌ Format check                FAILED (3 files)
⚠️  Lint check                 WARNINGS (5 issues)
✅ Type check                  PASSED
✅ Tests                       PASSED

$ task format
Fixed 3 files, 5 issues

$ /validate
🎉 All checks passed!
```

### Example 3: Test Failures

```bash
$ /validate

✅ Format/Lint/Type           PASSED
❌ Unit tests                  FAILED (2/45 failing)

❌ VALIDATION FAILED

Debug: uv run pytest tests/unit/test_cache.py::test_cache_expiration -xvs
```

---

## Optimization

**Parallel:** `task format:check & task lint & task test:fast`

**Incremental:** Fast checks first → If pass → Full validation

**CI/CD:**
```yaml
- name: Validate
  run: |
    task format:check
    task lint
    task test:fast
    task security:bandit
```

---

## Anti-Patterns

| Anti-Pattern | Issue | Solution |
|--------------|-------|----------|
| **Skip validation** | Merge broken code | Always run before commit |
| **Ignore warnings** | Technical debt accumulates | Fix or document why acceptable |
| **Override failures** | Security risks | Fix critical issues, never bypass |
| **Manual checks only** | Inconsistent, error-prone | Use automated task commands |

---

## Integration

### Called By

- `/work` - Before committing
- `/implement` - After implementation
- `/commit` - Pre-commit gate
- CI/CD - On every push
- User - Direct invocation

### Calls

- None (leaf workflow)

---

## References

- `docs/guides/TESTING_REFERENCE.md` - Detailed test commands
- `.windsurf/rules/06_security_practices.md` - Security guidelines
- `.windsurf/rules/02_testing.md` - Testing standards
