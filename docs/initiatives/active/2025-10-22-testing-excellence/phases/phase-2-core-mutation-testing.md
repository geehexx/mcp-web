# Phase 2: Core Module Mutation Testing 🧬

**Duration:** Weeks 3-4 (50-60 hours)
**Priority:** P1 (HIGH)
**Status:** In Progress

---

## Objective

Measure and improve test effectiveness for `src/mcp_web/` modules.

---

## Key Tasks

- [x] mutmut setup and configuration
- [ ] Baseline mutation score measurement
- [ ] Mutation testing on fetcher, extractor, chunker, summarizer
- [ ] Kill surviving mutants (write tests for uncaught mutations)
- [ ] CI integration (sample-based for PRs, full runs nightly)

---

## Current Configuration Snapshot

- `[tool.mutmut]` now targets `fetcher.py`, `extractor.py`, `chunker.py`, `summarizer.py`
- `tests_dir` narrowed to `tests/unit/` to keep runs scoped to true unit tests
- `also_copy` includes `scripts/` for action-item extraction fixtures
- Pytest marker registry updated with `golden` to unblock mutation stats collection

---

## Progress Log (2025-10-26)

- **[MUTMUT-SLOW-001]** Enforced `pytest-timeout` at 10s and limited mutmut to coverage-guided selection (`use_coverage = true`) to reduce the number of executed tests per mutant (`pyproject.toml`).
- **[MUTMUT-SLOW-002]** Introduced mutation-only skip for `tests/unit/test_security.py::TestConsumptionLimits::test_rate_limiting_realistic_timing` using the `MUTMUT_RUNNING` environment toggle; normal pytest runs still execute the test.
- **[MUTMUT-SLOW-003]** Performed `pytest --durations=50` audit; all remaining unit tests finish <1s (0.63s max) so no additional skips were added yet.
- **[MUTMUT-SLOW-004]** Mutmut cache primed once manually, but subsequent `task mutate:core` runs still hit timeouts around prompt summarizer mutants; no successful end-to-end run completed this session.

---

## Open Issues (`MUTMUT-SLOW`)

- **[MUTMUT-SLOW-010]** Replace real wall-clock sleeps in `test_rate_limiting_realistic_timing()` with a time-travel utility (e.g., freezegun or pytest-time-machine) so the mutation-only skip can be removed.
- **[MUTMUT-SLOW-011]** Investigate surviving/timeout mutants once a full run completes; current blockers prevent collecting an initial mutation score.
- **[MUTMUT-SLOW-012]** Evaluate whether additional slow markers (≥1s runtime under mutation) should be guarded by the `MUTMUT_RUNNING` check after the next baseline run.

---

## Next Steps for Follow-on Agent

- **[resume-run]** Start from `PYTEST_ADDOPTS="--maxfail=1" MUTMUT_RUNNING=1 task mutate:core` after clearing `.mutmut-cache/` if the cache becomes inconsistent.
- **[triage-timeouts]** Capture `uv run mutmut results` output to identify specific surviving or timed-out mutants once the run completes.
- **[remove-skips]** Once `MUTMUT-SLOW-010` is resolved, delete the skip guard and lower the global timeout threshold further if practical.
- **[ci-integration]** Defer wiring mutmut into CI or pre-commit until the baseline suite stays under 30 minutes locally (`MUTMUT-SLOW` tag indicates manual-only state).

---

## Success Criteria

- [ ] Mutation score ≥85% for src/mcp_web/ core modules
- [ ] Document mutation-resistant patterns
- [ ] CI mutation testing on PR (sample-based)
- [ ] Zero equivalent mutants (false positives)

---

## Related

- **Depends On:** Phase 1 (Scripts & Automation Hardening)
- **Blocks:** Phase 3 (Scripts Mutation Testing)
- **Initiative:** [Testing Excellence & Automation Hardening](../initiative.md)
