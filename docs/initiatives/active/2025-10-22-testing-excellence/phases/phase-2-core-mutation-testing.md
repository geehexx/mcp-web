# Phase 2: Core Module Mutation Testing 🧬

**Duration:** Weeks 3-4 (50-60 hours)
**Priority:** P1 (HIGH)
**Status:** Not Started

---

## Objective

Measure and improve test effectiveness for `src/mcp_web/` modules.

---

## Key Tasks

- [ ] mutmut setup and configuration
- [ ] Baseline mutation score measurement
- [ ] Mutation testing on fetcher, extractor, chunker, summarizer
- [ ] Kill surviving mutants (write tests for uncaught mutations)
- [ ] CI integration (sample-based for PRs, full runs nightly)

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
