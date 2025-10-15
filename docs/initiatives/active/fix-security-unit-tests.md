# Initiative: Fix Security Unit Tests

**Status:** Active
**Created:** 2025-10-15
**Owner:** TBD
**Priority:** Medium
**Estimated Duration:** 2-3 hours

---

## Objective

Fix all 10 failing unit tests in `tests/unit/test_security.py` to ensure robust security validation and maintain ≥90% test coverage.

## Success Criteria

- [ ] All tests in `tests/unit/test_security.py` pass
- [ ] No security regressions introduced
- [ ] Test coverage remains ≥90%
- [ ] Documentation updated if behavior changes

## Motivation

### Problem

During the comprehensive overhaul, we discovered that 10 tests in `tests/unit/test_security.py` have implementation mismatches with production code:

### Failing Tests (10 total)

1. **`TestPromptInjectionFilter::test_no_false_positives`**
   - Issue: Detecting "Ignore whitespace when formatting" as injection
   - Root cause: Pattern too broad

2. **`TestPromptInjectionFilter::test_sanitize_input`**
   - Issue: `assert 1 == 10000` mismatch
   - Root cause: Max length parameter issue

3. **`TestOutputValidator::test_detect_api_key_exposure`**
   - Issue: Not detecting `sk-proj-` prefixed keys
   - Root cause: Regex pattern incomplete

4-5. **`TestConsumptionLimits` (2 tests)**
   - Issue: `'coroutine' object does not support async context manager`
   - Root cause: Incorrect async usage

6. **`TestURLValidation::test_localhost_blocked`**
   - Issue: IPv6 localhost `[::1]` not blocked
   - Root cause: Missing IPv6 validation

7. **`TestSecurityIntegration::test_combined_input_output_validation`**
   - Issue: Pattern not detected/sanitized
   - Root cause: Similar to #1

8. **`TestSecurityIntegration::test_rate_limit_with_injection_attempts`**
   - Issue: (Async-related)

9-10. **`TestRateLimiter` (2 tests)**
   - Issue: (Async-related)

### Impact

Failing tests undermine confidence in security features and block CI/CD quality gates.

### Value

Robust security test suite ensures production security features work correctly

## Tasks

### Quick Wins

1. **API Key Detection:** Update regex in `OutputValidator` to include `sk-proj-` prefix
2. **IPv6 Localhost:** Add `[::1]` to blocked patterns in URL validation
3. **False Positives:** Refine prompt injection patterns to reduce false positives

### Complex Issues

1. **Async Context Managers:** `ConsumptionLimits.enforce()` needs proper async context manager protocol
2. **Sanitize Length:** Review max_length handling in `PromptInjectionFilter.sanitize()`

### Testing Strategy

Run targeted test:
```bash
uv run pytest tests/unit/test_security.py -v --tb=short
```

After fixes, verify no regressions:
```bash
task test:fast
```

## Related Documentation

- [Security Rules](../../.windsurf/rules/04_security.md)
- [Testing Standards](../../.windsurf/rules/01_testing_and_tooling.md)

## Timeline

- **Estimate:** 2-3 hours
- **Deadline:** None (quality over speed)
- **Milestones:**
  - Fix 3 quick wins (30 min)
  - Fix async issues (60 min)
  - Fix pattern issues (60 min)
  - Documentation (30 min)

## Updates

### 2025-10-15 (Initial Creation)

**Notes:**
- All integration and golden tests are passing
- Security features are working in practice
- Tests are overly strict or have implementation mismatches
- No production security bugs identified

**Next Steps:**
1. Review each failing test individually
2. Determine if test or production code needs fixing
3. Apply fixes with regression testing
4. Update security documentation if needed

---

**Last Updated:** 2025-10-15
**Status:** Active - Not started
