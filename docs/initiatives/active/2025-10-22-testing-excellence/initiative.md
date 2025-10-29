---
Status: In Progress
Created: 2025-10-22
Owner: Core Team
Priority: Critical
Estimated Duration: "7-9 weeks (includes Phase 0: 8-12h scripts audit)"
Target Completion: 2025-12-22
Updated: 2025-10-29
Tags: testing, quality, automation, mutation-testing, property-based-testing
---

# Initiative: Testing Excellence & Automation Hardening

## Objective

Eliminate testing blind spots through comprehensive coverage of automation scripts, mutation testing across all modules, deep property-based testing investment, and continuous quality monitoring. Target **95%+ coverage** with **85%+ mutation scores**.

---

## Success Criteria

- [ ] Scripts coverage ≥90% (currently 17% - only 4/24 scripts tested)
- [ ] Core module mutation score ≥85% (unknown baseline)
- [ ] Scripts mutation score ≥75% (critical scripts)
- [ ] 20+ Hypothesis property-based tests implemented
- [ ] Overall line coverage ≥95% (currently 85%)
- [ ] Test execution time <5min in CI (currently ~5-8min)
- [ ] Flakiness rate <1% (measured via pytest-repeat)
- [ ] Zero untested CLI entry points
- [ ] All 24 scripts have integration tests
- [ ] Test quality metrics dashboard operational

---

## Motivation

### Problem

**Current State:**

- **Scripts Coverage Gap:** 20/24 scripts (83%) have **ZERO** tests
  - Historical regressions in automation confirmed by user
  - Silent failures in `validate_initiatives.py`, `dependency_registry.py`, `extract_action_items.py`
  - No integration tests for script workflows
- **Unknown Test Quality:** No mutation testing = unknown effectiveness of 302 existing tests
  - Tests may pass without actually validating behavior
  - Potential "dormant" test suites (green but not effective)
- **Missing Edge Cases:** No property-based testing
  - Text processing (chunker, extractor) lacks edge case coverage
  - URL validation, frontmatter parsing lack fuzz testing
  - Unicode, emoji, special character handling untested
- **Limited Observability:** No metrics on test health
  - Unknown flakiness rates
  - No performance tracking
  - No mutation score trends

### Impact

**Without This Initiative:**

- ❌ Silent automation failures continue
- ❌ Unknown test effectiveness (tests pass, bugs ship)
- ❌ Edge cases discovered in production
- ❌ Script regressions impact workflows
- ❌ Technical debt accumulates

**With This Initiative:**

- ✅ Hardened automation (6+ months stable)
- ✅ Validated test quality (mutation testing)
- ✅ Discovered edge cases (property-based testing)
- ✅ Continuous quality metrics
- ✅ Proactive improvement

### Value

- **Reliability:** Automation scripts run 6+ months without regression
- **Quality:** Test suite validated effective via mutation testing (85%+ scores)
- **Depth:** Property-based testing discovers 10-30% more edge cases than example-based
- **Sustainability:** Continuous quality metrics enable proactive improvement before production

---

## Scope

### In Scope

- ✅ All 24 scripts in `scripts/` directory
- ✅ All modules in `src/mcp_web/`
- ✅ Mutation testing (mutmut + cosmic-ray)
- ✅ Property-based testing (Hypothesis) - 20+ tests
- ✅ Integration/E2E workflow tests
- ✅ Test observability metrics
- ✅ CI/CD optimization (<5min execution)

### Out of Scope

- ❌ UI/browser testing (Playwright used for fetching only, not browser automation)
- ❌ Load testing beyond current benchmarks (existing pytest-benchmark sufficient)
- ❌ External service mocking infrastructure (use responses library for API mocking)
- ❌ Test data generation tooling beyond Hypothesis

---

## Phases

This initiative is organized into **8 phases** (Phase 0 + 7 core phases) for incremental value delivery:

### [Phase 0: Scripts Audit & Refactoring](artifacts/phase-0-scripts-audit.md) 🔧 **PREP**

**Duration:** 8-12 hours (prep work) | **Priority:** P0

**Objective:** Clean up `scripts/` directory before testing - remove obsolete scripts, extract common lib code, organize structure.

**Key Tasks:**

- Delete 5 obsolete one-time scripts (~900 LOC: fix_frontmatter.py, restore_workflows.py, test_optimization_idempotency.py, manage_optimization_cache.py, backup file)
- Create `scripts/lib/` module (frontmatter, validation, CLI utilities) with 20-30 unit tests
- Refactor 6+ validation scripts to use lib (eliminate duplication)
- Organize scripts into subdirectories (validation/, automation/, analysis/)
- Update Taskfile, pre-commit hooks, documentation

**Success Criteria:**

- [ ] 5 obsolete scripts deleted
- [ ] scripts/lib/ created with 3 modules, 20-30 tests, 100% coverage
- [ ] 6+ scripts refactored to use lib
- [ ] All Taskfile commands functional
- [ ] All pre-commit hooks functional
- [ ] scripts/README.md updated

**Impact:**

- **Testing reduction:** 25% fewer scripts to test (24 → ~18-19 production scripts)
- **Code reduction:** ~1,070 LOC removed (obsolete + duplication)
- **Efficiency:** Test lib once, confidence in 6+ scripts
- **Maintainability:** DRY principle, logical organization, clear patterns

**ROI:** High - reduces Phase 1 scope by 25%, establishes maintainable patterns for 6-8 week initiative

---

### [Phase 1: Scripts & Automation Hardening](phases/phase-1-scripts-hardening.md) ⚡ **CRITICAL**

**Status:** In Progress | **Duration:** Weeks 1-2 (60-80 hours) | **Priority:** P0

**Objective:** Achieve 90%+ coverage on all scripts, prevent automation regressions.

See [phases/phase-1-scripts-hardening.md](phases/phase-1-scripts-hardening.md) for full details, tasks, and progress.

---

### [Phase 2: Core Module Mutation Testing](phases/phase-2-core-mutation-testing.md) 🧬 **HIGH**

**Status:** Not Started | **Duration:** Weeks 3-4 (50-60 hours) | **Priority:** P1

**Objective:** Measure and improve test effectiveness for `src/mcp_web/` modules.

See [phases/phase-2-core-mutation-testing.md](phases/phase-2-core-mutation-testing.md) for full details.

---

### [Phase 3: Scripts Mutation Testing](phases/phase-3-scripts-mutation-testing.md) 🧬 **HIGH**

**Status:** Not Started | **Duration:** Week 5 (30-40 hours) | **Priority:** P1

**Objective:** Validate test quality for critical automation scripts.

See [phases/phase-3-scripts-mutation-testing.md](phases/phase-3-scripts-mutation-testing.md) for full details.

---

### [Phase 4: Property-Based Testing - Core](phases/phase-4-property-based-core.md) 🔬 **MEDIUM**

**Status:** Not Started | **Duration:** Week 6 (30-40 hours) | **Priority:** P2

**Objective:** Deep investment in Hypothesis for core text processing modules.

See [phases/phase-4-property-based-core.md](phases/phase-4-property-based-core.md) for full details.

---

### [Phase 5: Property-Based Testing - Advanced](phases/phase-5-property-based-advanced.md) 🔬 **MEDIUM**

**Status:** Not Started | **Duration:** Week 7 (30-40 hours) | **Priority:** P2

**Objective:** Extend property-based testing to validation and generation scripts.

See [phases/phase-5-property-based-advanced.md](phases/phase-5-property-based-advanced.md) for full details.

---

### [Phase 6: Integration & E2E Workflows](phases/phase-6-integration-e2e.md) 🔄 **MEDIUM**

**Status:** Not Started | **Duration:** Week 7 (30-40 hours) | **Priority:** P2

**Objective:** Full workflow validation from entry point to output.

See [phases/phase-6-integration-e2e.md](phases/phase-6-integration-e2e.md) for full details.

---

### [Phase 7: Observability & Continuous Improvement](phases/phase-7-observability.md) 📊 **LOW**

**Status:** Not Started | **Duration:** Week 8 (30-40 hours) | **Priority:** P3

**Objective:** Establish metrics and continuous monitoring for test health.

See [phases/phase-7-observability.md](phases/phase-7-observability.md) for full details.

---

## Dependencies

**Blocks:** None (can run parallel to Phase 1-3 infrastructure initiatives)

**Blocked By:** None

**Related Initiatives:**

- Phase 1: Resource Stability (testing supports validation)
- Phase 2: Data Integrity (testing supports cache coherency validation)
- Phase 3: Performance Optimization (testing supports regression detection)

---

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Scripts too complex to test | Medium | Medium | Use Approval Testing pattern for behavior capture |
| Mutation testing too slow | Low | Medium | Sample-based in CI, full runs nightly |
| Hypothesis finds critical bugs | High | Medium | **GOOD RISK** - Fix discovered issues immediately, document |
| Timeline overrun | Medium | Low | Phases 1-3 are MVP, Phases 4-7 can defer if needed |
| Test suite becomes slow | Medium | Low | Parallel execution (pytest-xdist), marker-based selection |
| Flaky tests introduced | High | Low | Strict isolation, pytest-repeat validation, quarantine markers |

---

## Timeline

| Period | Phase | Effort |
|--------|-------|--------|
| **Weeks 1-2** | Phase 1: Scripts hardening | 60-80h |
| **Weeks 3-4** | Phase 2: Core mutation testing | 50-60h |
| **Week 5** | Phase 3: Scripts mutation testing | 30-40h |
| **Week 6** | Phase 4: Property-based core | 30-40h |
| **Week 7** | Phase 5: Property-based advanced | 30-40h |
| **Week 7** | Phase 6: Integration/E2E | 30-40h |
| **Week 8** | Phase 7: Observability | 30-40h |

**Total:** 260-320 hours (6-8 weeks at 2-3 people)

**Aggressive timeline approved by user - prioritize quality over speed.**

---

## Metrics

### Baseline (2025-10-22)

| Metric | Current |
|--------|---------|
| Line Coverage | 85% |
| Scripts Coverage | 17% (4/24 tested) |
| Test Count | 302 tests across 26 files |
| Mutation Score | Unknown (not measured) |
| Property-Based Tests | 0 |
| CI Test Time | ~5-8 minutes |
| Flakiness Rate | Unknown |

### Target (Post-Initiative)

| Metric | Target |
|--------|--------|
| Line Coverage | ≥95% |
| Scripts Coverage | ≥90% |
| Test Count | 450+ tests |
| Mutation Score | ≥85% (core), ≥75% (scripts) |
| Property-Based Tests | 20+ |
| CI Test Time | <5 minutes |
| Flakiness Rate | <1% |

---

## Related Documentation

- [Testing Guide](../../guides/TESTING_GUIDE.md) - Current testing strategy
- [Security Architecture](../../architecture/SECURITY_ARCHITECTURE.md) - OWASP LLM Top 10 coverage
- [ADR-0020: Markdown Quality Automation](../../adr/0020-comprehensive-markdown-quality-automation.md) - Quality automation patterns
- [Constitution](../../CONSTITUTION.md) - Quality principles

---

## Artifacts

Supporting documents in this initiative folder:

### Research

- [external-sources.md](research/external-sources.md) - 12+ external sources analyzed
- [gap-analysis.md](research/gap-analysis.md) - Current state deep dive
- [tool-evaluation.md](research/tool-evaluation.md) - mutmut vs cosmic-ray vs alternatives
- [historical-issues.md](research/historical-issues.md) - Session summary mining results

### Artifacts

- [scripts-inventory.md](artifacts/scripts-inventory.md) - All 24 scripts categorized by risk
- [dependency-map.md](artifacts/dependency-map.md) - Script interdependencies
- [risk-matrix.md](artifacts/risk-matrix.md) - Risk assessment by module
- [test-strategy-comparison.md](artifacts/test-strategy-comparison.md) - Alternatives analysis

### Progress

- [session-log.md](progress/session-log.md) - Session-by-session updates

---

## Updates

### 2025-10-29 - Phase 1 Dependency Registry Hardening

**Focus:** Dependency parsing robustness and typing hygiene for automation scripts.

- ✅ Strengthened `_parse_dependencies` to correctly classify nested prerequisite, blocking, and synergistic links.
- ✅ Added targeted unit assertions covering dependency-type detection and blocker propagation regressions.
- ✅ Raised typing quality: explicit graph/propagation annotations and narrowed `frontmatter` import ignore, clearing mypy debt for the script.
- ✅ Lint, mypy, and unit suites run green (`task lint`, `uv run mypy scripts/automation/dependency_registry.py`, `uv run pytest tests/unit/test_dependency_registry.py`).
- 📤 Changes landed on `main` via commits `2c7f600` and `989a32f`; branch pushed to origin.

**Status:** Phase 1 test hardening underway with dependency registry now validated by deterministic tests and typing gates.

### 2025-10-22 - Initiative Created

**Comprehensive research complete:**

- 12+ external sources analyzed (Real Python, LambdaTest, Pytest with Eric, etc.)
- 24 scripts inventoried (20 untested)
- 302 existing tests categorized
- User approved: Scripts-first priority, all modules scope, deep property-based investment, aggressive timeline

**Decisions:**

1. **Phase Structure:** 7 phases for granular value delivery
2. **Tool Choices:** mutmut (primary), cosmic-ray (quarterly), Hypothesis (property-based)
3. **Approach:** Golden Master for scripts, mutation testing for quality, Hypothesis for edge cases
4. **Timeline:** 6-8 weeks aggressive, quality prioritized over speed

**Next Steps:**

- Mine session summaries for historical testing issues
- Create detailed phase documents
- Update PROJECT_SUMMARY.md
- Begin Phase 1 planning

---

**Last Updated:** 2025-10-22
**Status:** Proposed
