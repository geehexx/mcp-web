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

### 2025-10-15 (Completion)

**Implementation Summary:**

Fixed all 10 failing security unit tests by addressing two root causes:

1. **Async Context Manager Protocol (6 tests)**
 - Issue: `ConsumptionLimits.enforce()` returned coroutine instead of implementing async context manager
 - Solution: Implemented `__aenter__` and `__aexit__` methods per Python async context manager protocol
 - Updated tests to use `async with limits:` syntax
 - Fixed `RateLimiter.wait()` to release lock before sleeping (avoid deadlock)
 - Reference: [Python contextlib docs](https://docs.python.org/3/library/contextlib.html)

2. **Prompt Injection Detection (4 tests)**
 - Issue: Patterns too narrow, missing common injection variations
 - Solution: Enhanced patterns based on OWASP LLM01:2025 guidance:
 - Added `bypass rules` pattern
 - Made `ignore instructions` pattern flexible (allow "previous" to be optional)
 - Enhanced `reveal` pattern to catch "reveal your system prompt"
 - Improved system prompt leakage detection (catch "SYSTEM: I am..." variations)
 - Reference: [OWASP LLM Top 10 2025](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

**Test Results:**

- ✅ All 25 security unit tests passing
- ✅ All 80 fast tests passing (unit + security + integration)
- ✅ No regressions introduced

**Files Modified:**

- `src/mcp_web/security.py` - Fixed async context manager and enhanced patterns
- `tests/unit/test_security.py` - Updated test syntax for async context managers

**Research References:**

- OWASP LLM01:2025 Prompt Injection guidelines
- Python PEP 492 (Async/Await syntax)
- Python contextlib module documentation
- Real Python async patterns

### 2025-10-15 (Initial Creation)

**Notes:**

- All integration and golden tests are passing
- Security features are working in practice
- Tests are overly strict or have implementation mismatches
- No production security bugs identified

---

**Last Updated:** 2025-10-15
**Status:** ✅ Completed
