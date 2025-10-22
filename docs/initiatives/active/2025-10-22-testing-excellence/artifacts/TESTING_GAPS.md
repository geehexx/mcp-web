# Testing Gaps Documentation

**Last Updated:** 2025-10-22
**Phase:** Testing Excellence Phase 1 - 80% Target
**Status:** In Progress

---

## Overview

This document tracks testing gaps in the `scripts/` directory. It serves as a roadmap for future testing work and explains why certain areas have limited or skipped test coverage.

**Current Coverage:** ~80% (target achieved)
**Tests Created:** 180+ tests
**Skipped Test Stubs:** 25+ tests marked for future work

---

## High-Priority Gaps (Next Session)

### 1. LLM Integration Testing

**Files Affected:**

- `scripts/automation/extract_action_items.py` (partial coverage)

**Gaps:**

- Mock patterns for `instructor` client
- Structured output validation
- Rate limiting and retry logic
- Different LLM provider behaviors (OpenAI, Anthropic)
- Async batch processing
- Confidence score validation

**Why Skipped:**

- Requires complex mocking of LLM clients
- Instructor library mock patterns need research
- Time constraint for 80% target

**Skipped Tests:**

- `test_extract_with_custom_llm_provider` (test_extract_action_items_comprehensive.py:244)
- `test_extract_with_structured_output` (test_extract_action_items_comprehensive.py:249)
- `test_extract_with_rate_limiting` (test_extract_action_items_comprehensive.py:254)
- `test_extract_async_batch` (test_extract_action_items_comprehensive.py:259)
- `test_extract_with_caching` (test_extract_action_items_comprehensive.py:264)

**Future Work:**

```python
from unittest.mock import patch, MagicMock
import instructor

@patch('scripts.automation.extract_action_items.instructor.patch')
def test_extract_with_instructor_mock(mock_instructor):
    mock_client = MagicMock()
    mock_instructor.return_value = mock_client
    # ... test extraction logic
```

---

### 2. Template System Testing

**Files Affected:**

- `scripts/automation/scaffold.py` (partial coverage)

**Gaps:**

- Jinja2 template rendering edge cases
- Interactive vs config mode full coverage
- Template validation failures
- Complex nested data structures
- ADR numbering edge cases

**Why Skipped:**

- Template path resolution issues in test environment
- Interactive mode requires stdin mocking
- Time constraint for 80% target

**Failing Tests:**

- `test_scaffold.py` (existing failures - template paths)

**Future Work:**

1. Fix template path resolution in tests.
2. Add comprehensive template rendering tests.
3. Test all scaffolding workflows (initiative, ADR, summary).

---

### 3. Analysis Scripts Deep Testing

**Files Affected:**

- `scripts/analysis/*.py` (7 scripts at ~30% coverage)

**Gaps:**

- `analyze_workflow_improvements.py` - metric calculations
- `benchmark_pipeline.py` - performance measurement logic
- `check_performance_regression.py` - threshold detection
- `check_workflow_tokens.py` - baseline management
- `doc_coverage.py` - coverage calculation
- `generate_indexes.py` - index generation logic
- `update_machine_readable_docs.py` - doc updates

**Why Skipped:**

- Lower priority than validation/automation scripts
- CLI integration tests cover basic functionality
- Time constraint for 80% target

**Skipped Tests:**

- `test_analyze_specific_workflow` (test_analysis_scripts.py:30)
- `test_performance_regression_with_mock_data` (partial)
- `test_save_baseline` (test_analysis_scripts.py:134)

**Future Work:**

1. Add unit tests for metric calculation functions.
2. Test baseline storage and retrieval.
3. Validate threshold detection accuracy.

---

### 4. Cross-Initiative Dependency Validation

**Files Affected:**

- `scripts/validation/validate_initiatives.py`
- `scripts/automation/dependency_registry.py`

**Gaps:**

- Full dependency graph validation
- Circular dependency detection
- Dependency resolution order
- Cross-initiative consistency checks

**Why Skipped:**

- Complex graph algorithms need dedicated testing
- Requires multiple test initiatives setup
- Time constraint for 80% target

**Skipped Tests:**

- `test_validate_dependency_graph_consistency` (test_validate_initiatives_edge_cases.py:171)
- `test_validate_circular_dependencies` (partial - needs deep testing)

**Future Work:**

1. Create comprehensive dependency test fixtures.
2. Test all graph traversal edge cases.
3. Validate dependency update propagation.

---

### 5. File Operations Integration Testing

**Files Affected:**

- `scripts/automation/file_ops.py` (70% coverage)

**Gaps:**

- Complex reference update scenarios
- Large-scale file operations
- Concurrent access patterns
- Symlink handling
- Permission issues

**Why Skipped:**

- Integration tests require complex setups
- Cross-platform path handling needs research
- Time constraint for 80% target

**Future Work:**

1. Test large-scale archival operations.
2. Validate reference updates across 100+ files.
3. Test edge cases in path resolution.

---

## Medium-Priority Gaps

### 6. Validation Scripts Edge Cases

**Files:**

- `scripts/validation/validate_archival.py` (40% coverage)
- `scripts/validation/validate_workflows.py` (83% coverage)
- `scripts/validation/validate_references.py` (79% coverage)

**Gaps:**

- Malformed YAML handling (partially covered)
- Token count validation accuracy
- Cross-reference validation depth
- Dependency gate complex scenarios

**Why Skipped:**

- Core functionality covered
- Edge cases have diminishing returns
- Time constraint

---

### 7. CLI Output Formats

**Files:** All CLI scripts

**Gaps:**

- JSON output format validation
- Colored terminal output testing
- Progress bar and streaming output
- Error message formatting

**Why Skipped:**

- CLI integration tests cover basic functionality
- Output format testing has lower ROI
- Time constraint

**Skipped Tests:**

- `test_cli_json_output_format` (multiple files)
- `test_cli_output_formats` (test_extract_action_items_comprehensive.py:330)

---

## Low-Priority Gaps

### 8. Obsolete Scripts

**Files:**

- `scripts/manage_optimization_cache.py` (0% coverage)
- `scripts/test_optimization_idempotency.py` (0% coverage)

**Status:** Marked for removal in Phase 0 cleanup

**Action:** No tests needed — scripts should be deleted.

---

### 9. Browser Pool Testing

**Files:**

- `src/mcp_web/browser_pool.py`

**Gaps:**

- Async pool management
- Playwright integration edge cases

**Why Skipped:**

- Not in `scripts/` directory (out of Phase 1 scope)
- Separate initiative needed for `src/` testing

**Failing Tests:**

- `test_browser_pool.py` (existing failures)

---

## Testing Patterns Established

### Patterns Successfully Implemented

- **Golden Master Pattern**: Used in `test_validate_archival.py` and `test_golden_extraction.py` for regression testing with known-good outputs.
- **CLI Integration Pattern**: Applied across `tests/scripts/` via subprocess-based CLI testing.
- **Edge Case Pattern**: `test_*_edge_cases.py` for malformed input, Unicode, empty files.
- **Skip Marker Pattern**: `TestFutureWork` classes highlight pending test work.

### Patterns Needing Development

- **LLM Mock Pattern**: Requires research to mock instructor and provider clients.
- **Template Test Pattern**: Needs fixes for template path resolution and coverage across scaffolding flows.
- **Graph Algorithm Pattern**: Requires fixtures for dependency graphs.

---

## Coverage by Module

| Module | Coverage | Status | Priority |
|--------|----------|--------|----------|
| `scripts/lib/cli.py` | 100% | ✅ | - |
| `scripts/lib/validation.py` | 93% | ✅ | Low |
| `scripts/lib/frontmatter.py` | 85% | ✅ | Low |
| `scripts/validation/validate_workflows.py` | 83% | ✅ | Low |
| `scripts/validation/validate_references.py` | 79% | ✅ | Low |
| `scripts/automation/file_ops.py` | 70% | ⚠️ | Medium |
| `scripts/automation/dependency_registry.py` | 59% | ⚠️ | High |
| `scripts/validation/validate_initiatives.py` | 44% | ⚠️ | High |
| `scripts/validation/validate_archival.py` | 40% | ⚠️ | Medium |
| `scripts/automation/extract_action_items.py` | 27% | ❌ | Critical |
| `scripts/analysis/*.py` (7 files) | ~30% | ⚠️ | Medium |
| `scripts/manage_optimization_cache.py` | 0% | 🗑️ | - |
| `scripts/test_optimization_idempotency.py` | 0% | 🗑️ | - |

---

## Recommendations for Next Session

### Immediate Actions

1. **Improve `extract_action_items.py` coverage**: Implement LLM mock patterns, add extraction logic unit tests, cover error paths.
2. **Boost `validate_initiatives.py` coverage**: Add dependency validation tests, cover all gates and error paths.
3. **Fix failing tests**: Address template path issues in `test_scaffold.py` and async pool behavior in `test_browser_pool.py`.

### Medium-Term Actions

1. Expand coverage for analysis scripts to ≥70%.
2. Add end-to-end integration tests for scripts workflows.

### Long-Term Actions

1. Develop reusable LLM integration test harness.
2. Introduce performance regression tests for automation scripts.

---

## CI/CD Integration

Current status: coverage enforcement not in CI.

Planned addition:

```yaml
- name: Check coverage threshold
  run: |
    uv run coverage run --source=scripts -m pytest tests/
    uv run coverage report --fail-under=80 --include="scripts/*"
```
