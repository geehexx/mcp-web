# Phase 1: Scripts & Automation Hardening ⚡

**Duration:** Weeks 1-2 (60-80 hours)
**Priority:** P0 (CRITICAL)
**Status:** In Progress

---

## Objective

Achieve 90%+ coverage on all 24 scripts, prevent automation regressions.

---

## Key Tasks

- [ ] Audit all 24 scripts (categorize by risk, map dependencies)
- [ ] Golden Master test suite (capture current behavior)
- [ ] CLI integration tests (subprocess + mocks pattern)
- [ ] Deep dive on critical scripts (validate_initiatives.py, dependency_registry.py, extract_action_items.py)
- [ ] CI integration (pytest discovery, pre-commit hooks, 90% coverage enforcement)

---

## Success Criteria

- [ ] 90%+ line coverage on `scripts/`
- [ ] Zero untested CLI entry points
- [ ] Golden Master suite for all validators
- [ ] CI fails on script changes without tests

---

## Progress

### 2025-10-22

#### Checkpoint 1: Import Fixes (Session 1)

- ✅ Fixed 8 test files after Phase 0 reorganization
- ✅ 139/152 tests passing (91.4% pass rate)
- ✅ Commit `2a2219b` delivered
- ⏭️ 13 scaffold test failures documented (template path issues from Phase 0)

**Status:** Checkpoint delivered. Import errors resolved.

#### Checkpoint 2: Additional Test Fixes (Session 2)

- ✅ Fixed 34 inline import errors in validation tests (`test_validate_references.py`, `test_validate_task_format.py`)
- ✅ Fixed 22 AsyncMock usage errors in `test_browser_pool.py`
- ✅ 317/318 tests passing (99.7% pass rate)
- ✅ Commit `26a6cb6` delivered
- ⏭️ 1 scaffold template failure remaining (from Phase 0)

**Status:** Import/mock cleanup complete. Ready for Phase 1 core work (Golden Master tests, coverage push).

---

## Related

- **Depends On:** Phase 0 (Scripts Audit & Refactoring) - Complete
- **Blocks:** Phase 2 (Core Module Mutation Testing)
- **Initiative:** [Testing Excellence & Automation Hardening](../initiative.md)
