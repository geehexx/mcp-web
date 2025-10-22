# Scripts Inventory & Risk Assessment

**Initiative:** Testing Excellence & Automation Hardening
**Date:** 2025-10-22
**Total Scripts:** 24

---

## Risk Classification

| Risk Level | Count | Description |
|------------|-------|-------------|
| **CRITICAL** | 8 | Core validation, extraction, generation - failures cause data corruption |
| **HIGH** | 6 | Workflow automation, benchmarking - failures cause workflow breakage |
| **MEDIUM** | 7 | Utility scripts, helpers - failures cause inconvenience |
| **LOW** | 3 | One-time fixes, archival tools - limited usage |

---

## CRITICAL (P0) - 8 Scripts

### 1. `validate_initiatives.py` ❌ **NO TESTS**

**Purpose:** Validates initiative frontmatter, structure, folder vs flat file

**Risk:** High - Invalid initiatives break workflows, archival, tracking

**Dependencies:** frontmatter, pathlib

**Testing Gap:** No tests for validation logic, frontmatter parsing, error handling

**Priority:** Phase 1 (Week 1)

---

### 2. `validate_task_format.py` ❌ **NO TESTS**

**Purpose:** Validates Taskfile.yml format and task definitions

**Risk:** High - Invalid tasks break CI/CD, automation

**Dependencies:** pyyaml

**Testing Gap:** No tests for YAML parsing, validation rules

**Priority:** Phase 1 (Week 1)

---

### 3. `validate_references.py` ❌ **NO TESTS**

**Purpose:** Cross-reference validation (ADRs, docs, broken links)

**Risk:** High - Broken links in docs, missing ADRs

**Dependencies:** pathlib, markdown parsing

**Testing Gap:** No tests for link extraction, validation logic

**Priority:** Phase 1 (Week 1)

---

### 4. `extract_action_items.py` ❌ **NO TESTS**

**Purpose:** LLM-powered extraction of action items from session summaries

**Risk:** High - Incorrect extraction causes lost tasks, planning errors

**Dependencies:** openai, anthropic, pydantic

**Testing Gap:** No LLM mocking, no validation of extraction logic

**Priority:** Phase 1 (Week 2)

---

### 5. `dependency_registry.py` ❌ **NO TESTS**

**Purpose:** Tracks cross-file dependencies for refactoring safety

**Risk:** High - Incorrect dependencies break refactoring workflows

**Dependencies:** ast, pathlib

**Testing Gap:** No AST parsing tests, no dependency graph validation

**Priority:** Phase 1 (Week 2)

---

### 6. `generate_indexes.py` ❌ **NO TESTS**

**Purpose:** Auto-generates README.md indexes for docs directories

**Risk:** Medium-High - Incorrect indexes cause navigation issues

**Dependencies:** pathlib, markdown generation

**Testing Gap:** No tests for index generation, no idempotency tests

**Priority:** Phase 1 (Week 2)

---

### 7. `update_machine_readable_docs.py` ❌ **NO TESTS**

**Purpose:** Updates machine-readable documentation (AGENTS.md, etc.)

**Risk:** Medium-High - Incorrect updates break automation tooling

**Dependencies:** frontmatter, markdown parsing

**Testing Gap:** No tests for doc parsing, updating logic

**Priority:** Phase 1 (Week 2)

---

### 8. `fix_frontmatter.py` ❌ **NO TESTS**

**Purpose:** Repairs malformed YAML frontmatter in markdown files

**Risk:** Medium - Incorrect fixes corrupt frontmatter

**Dependencies:** frontmatter, pyyaml

**Testing Gap:** No tests for frontmatter parsing, repair logic

**Priority:** Phase 1 (Week 2)

---

## HIGH (P1) - 6 Scripts

### 9. `benchmark_pipeline.py` ❌ **NO TESTS**

**Purpose:** Comprehensive pipeline benchmarking, load testing

**Risk:** Medium - Incorrect metrics cause wrong optimization decisions

**Dependencies:** asyncio, custom profiler

**Testing Gap:** No self-testing benchmarks, no metrics validation

**Priority:** Phase 1 (Week 2)

---

### 10. `check_performance_regression.py` ❌ **NO TESTS**

**Purpose:** Compares benchmark results, detects regressions

**Risk:** Medium - False positives/negatives in regression detection

**Dependencies:** json, statistics

**Testing Gap:** No tests for regression logic, threshold calculation

**Priority:** Phase 1 (Week 2)

---

### 11. `scaffold.py` ✅ **26 TESTS** (test_scaffold.py)

**Purpose:** Template scaffolding for initiatives, ADRs, summaries

**Risk:** Low (well tested)

**Test Coverage:** 100% - Jinja2 rendering, config parsing, path generation

**Status:** ✅ Complete

---

### 12. `file_ops.py` ✅ **TESTED** (test_file_ops.py)

**Purpose:** File operations (archive, move, update refs)

**Risk:** Low (well tested)

**Test Coverage:** High - archive_initiative, move_file_with_refs, update_index

**Status:** ✅ Complete

---

### 13. `check_workflow_tokens.py` ❌ **NO TESTS**

**Purpose:** Analyzes workflow token counts for optimization

**Risk:** Low-Medium - Incorrect counts cause optimization errors

**Dependencies:** tiktoken

**Testing Gap:** No tests for token counting, analysis logic

**Priority:** Phase 2

---

### 14. `analyze_workflow_improvements.py` ❌ **NO TESTS**

**Purpose:** Analyzes workflow optimization results

**Risk:** Low-Medium - Incorrect analysis causes wrong conclusions

**Dependencies:** json, statistics

**Testing Gap:** No tests for analysis algorithms

**Priority:** Phase 2

---

## MEDIUM (P2) - 7 Scripts

### 15. `validate_documentation.py` ❌ **NO TESTS**

**Purpose:** Validates documentation structure and completeness

**Dependencies:** pathlib, markdown

**Testing Gap:** No tests for validation rules

**Priority:** Phase 2

---

### 16. `validate_frontmatter.py` ❌ **NO TESTS**

**Purpose:** Validates YAML frontmatter across all markdown files

**Dependencies:** frontmatter, pyyaml

**Testing Gap:** No tests for validation logic

**Priority:** Phase 2

---

### 17. `validate_rules_frontmatter.py` ❌ **NO TESTS**

**Purpose:** Validates `.windsurf/rules/` frontmatter

**Dependencies:** frontmatter

**Testing Gap:** No tests for rule-specific validation

**Priority:** Phase 2

---

### 18. `validate_workflows.py` ❌ **NO TESTS**

**Purpose:** Validates `.windsurf/workflows/` structure and frontmatter

**Dependencies:** frontmatter

**Testing Gap:** No tests for workflow validation

**Priority:** Phase 2

---

### 19. `doc_coverage.py` ❌ **NO TESTS**

**Purpose:** Analyzes documentation coverage for code modules

**Dependencies:** ast, pathlib

**Testing Gap:** No tests for AST analysis, coverage calculation

**Priority:** Phase 2

---

### 20. `test_optimization_idempotency.py` ❌ **NO TESTS** (Ironic!)

**Purpose:** Tests workflow optimization idempotency

**Risk:** Low - Test script itself

**Testing Gap:** Meta - script that tests other scripts has no tests

**Priority:** Phase 3

---

### 21. `manage_optimization_cache.py` ❌ **NO TESTS**

**Purpose:** Manages workflow optimization cache

**Dependencies:** json, hashlib

**Testing Gap:** No tests for cache operations

**Priority:** Phase 3

---

## LOW (P3) - 3 Scripts

### 22. `validate_archival.py` ❌ **NO TESTS**

**Purpose:** Validates archived initiatives/documents

**Dependencies:** pathlib

**Testing Gap:** No tests for archival validation

**Priority:** Phase 3

---

### 23. `restore_workflows.py` ❌ **NO TESTS**

**Purpose:** One-time restoration script (historical)

**Risk:** Very Low - rarely used

**Testing Gap:** No tests (acceptable for one-time scripts)

**Priority:** Optional

---

### 24. `hooks/validate_task_format_hook.py` ❌ **NO TESTS**

**Purpose:** Pre-commit hook for task format validation

**Dependencies:** subprocess

**Testing Gap:** No tests for hook execution

**Priority:** Phase 2

---

## Summary Statistics

| Category | Tested | Untested | % Untested |
|----------|--------|----------|------------|
| **CRITICAL (P0)** | 0 | 8 | 100% |
| **HIGH (P1)** | 2 | 4 | 67% |
| **MEDIUM (P2)** | 0 | 7 | 100% |
| **LOW (P3)** | 0 | 3 | 100% |
| **TOTAL** | **2** | **22** | **92%** |

---

## Testing Strategy by Risk Level

### Phase 1: CRITICAL Scripts (Weeks 1-2)

**Approach:** Golden Master + Integration Tests

- Capture current behavior with Approval Testing
- Add integration tests for CLI invocation
- Critical path unit tests for key functions
- Target: 90%+ coverage

### Phase 2: HIGH Scripts (Week 3)

**Approach:** Behavioral Testing + Mocking

- Mock external dependencies (LLMs, file system)
- Integration tests for workflows
- Target: 80%+ coverage

### Phase 3: MEDIUM/LOW Scripts (Week 4+)

**Approach:** Smoke Tests + Selective Deep Dives

- Basic smoke tests for all
- Deep dive on frequently used scripts
- Target: 70%+ coverage

---

## Historical Regressions

**Evidence from Session Summaries:**

1. **scaffold.py regression:** Config file parsing broke, caused by string splitting bug (Fixed 2025-10-22)
2. **validate_initiatives.py gap:** No tests caught empty folder detection logic errors
3. **extract_action_items.py:** LLM rate limiting not tested, caused production failures

**Impact:** Script regressions delayed workflows by 2-4 hours per incident

---

**Last Updated:** 2025-10-22
**Status:** Complete
