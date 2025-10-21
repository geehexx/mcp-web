---
Status: Active
Created: 2025-10-21
Owner: AI Agent
Priority: High
---

# Initiative: Workflow Optimization Phase 2

**Status:** Active
**Start Date:** 2025-10-21
**Target Completion:** 2025-10-25
**Owner:** AI Agent
**Priority:** High

---

## Objective

Systematically apply conciseness optimizations to all workflows, eliminate duplication through shared patterns, implement quality gates, and reduce total token count below 85k threshold.

---

## Success Criteria

- [ ] All 21 workflows improved with `/improve-workflow`
- [ ] Combined token count < 85,000 (currently 93,101)
- [ ] Duplication reduced by ≥30% (~6,500 tokens)
- [ ] Quality gates implemented (cross-ref validation, task format validation)
- [ ] Pre-commit hooks and CI/CD pipeline operational
- [ ] Comprehensive documentation created

---

## Background

**Context:** After creating `/improve-prompt` and `/improve-workflow` with dynamic conciseness features, we now need to apply these capabilities systematically across the repository.

**Current State:**

- 21 workflows, 66,355 tokens
- 16 rules, 26,746 tokens
- Combined: 93,101 tokens (8,101 over 85k threshold)
- Significant duplication identified (task plans, validation blocks, patterns)

**Problem:**

1. Token budget exceeded by 9.5%
2. Duplication wastes 8,000-12,000 tokens
3. No automated quality gates for workflow changes
4. Missing reference documentation for common patterns

---

## Implementation Phases

### Phase 1: Research & Analysis ✅ COMPLETE

**Duration:** 2 hours
**Status:** Complete

**Deliverables:**

- Prompt modularity research
- Duplication analysis (26 instances identified)
- User input refinement evaluation (NOT RECOMMENDED - documented why)
- Comprehensive execution plan

### Phase 2: Batch Workflow Improvements

**Duration:** 4-6 hours
**Status:** Pending

**Tasks:**

- [ ] Apply `/improve-workflow` to Tier 1 workflows (5 largest)
- [ ] Apply to Tier 2 workflows (5 moderate)
- [ ] Batch apply to Tier 3 workflows (11 small)
- [ ] Validate each improvement iteratively
- [ ] Commit individually with metrics

**Expected Outcome:** 3,900 token reduction (14.7%)

### Phase 3: Decomposition (Conditional)

**Duration:** 3-4 hours
**Status:** Pending (triggers if Phase 2 flags workflows)

**Tasks:**

- [ ] Evaluate detect-context (complexity 80) for decomposition
- [ ] Evaluate work (complexity 85) for decomposition
- [ ] Implement decomposition if warranted
- [ ] Update dependencies and cross-references

**Expected Outcome:** Reduced complexity, potential token savings

### Phase 4: Duplication Reduction

**Duration:** 3-4 hours
**Status:** Pending

**Tasks:**

- [ ] Create `.windsurf/docs/task-plan-patterns.md`
- [ ] Create `.windsurf/docs/input-handling-patterns.md`
- [ ] Create `.windsurf/docs/validation-patterns.md`
- [ ] Update workflows to reference patterns vs duplicate
- [ ] Enhance `/validate` for composability
- [ ] Add scope=auto to `/load-context`

**Expected Outcome:** 6,500 token reduction from eliminated duplication

### Phase 5: Quality Gates & Pre-commit Checks

**Duration:** 2-3 hours
**Status:** Pending

**Tasks:**

- [ ] Create `scripts/validate_cross_references.py`
- [ ] Create `scripts/validate_task_format.py`
- [ ] Enhance `scripts/check_workflow_tokens.py` with --enforce
- [ ] Update `.pre-commit-config.yaml`
- [ ] Create `.github/workflows/validate-workflows.yml`

**Expected Outcome:** Automated validation prevents regressions

### Phase 6: Documentation & Cleanup

**Duration:** 1-2 hours
**Status:** Pending

**Tasks:**

- [ ] Update `docs/CONSTITUTION.md` with modularity section
- [ ] Update `.windsurf/rules/05_windsurf_structure.md`
- [ ] Update `README.md` with new metrics
- [ ] Create session summary
- [ ] Run final validation sweep

**Expected Outcome:** Complete documentation, clean state

### Phase 7: Validation & Acceptance

**Duration:** 1 hour
**Status:** Pending

**Tasks:**

- [ ] Run full validation suite
- [ ] Verify token count < 85,000
- [ ] Confirm all quality gates passing
- [ ] Review acceptance criteria
- [ ] Archive initiative if complete

**Expected Outcome:** Initiative complete, goals achieved

---

## Dependencies

### Prerequisite Work (Complete)

- ✅ `/improve-prompt` workflow created
- ✅ `/improve-workflow` sub-workflow created
- ✅ Dynamic conciseness system implemented
- ✅ Analysis tooling created (`analyze_workflow_improvements.py`)

### External Dependencies

- None (all work internal to repository)

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Over-optimization loses critical details | Medium | Medium | Validate each workflow, human review checklist, individual commits allow rollback |
| Breaking changes to workflows | High | Low | Comprehensive validation suite, pre-commit hooks, can git revert |
| Token threshold still exceeded after work | Low | Low | Conservative estimates, decomposition available, can adjust threshold if justified |
| Time overrun | Low | Medium | Phased approach allows stopping at checkpoints, each phase delivers independent value |

---

## Out of Scope

- ❌ Creating generic user input refinement sub-workflow (analysis showed not beneficial)
- ❌ Major workflow restructuring (focus is conciseness, not redesign)
- ❌ Modifying rule files (focus is workflows first)
- ❌ Changing Windsurf IDE behavior (work within existing constraints)

---

## Related ADRs

- ADR-0018: Workflow Architecture V3 (decomposition patterns)
- ADR-0002: Adopt Windsurf Workflow System

---

## Metrics & Progress Tracking

### Token Count Tracking

| Checkpoint | Workflows | Rules | Combined | vs Threshold |
|------------|-----------|-------|----------|--------------|
| Baseline | 66,355 | 26,746 | 93,101 | +8,101 |
| After Phase 2 | ~62,455 | 26,746 | ~89,201 | +4,201 |
| After Phase 4 | ~55,955 | 26,746 | ~82,701 | -2,299 |
| **Target** | **<60,000** | **26,746** | **<85,000** | **Under** |

### Duplication Reduction

| Category | Before | After | Reduction |
|----------|--------|-------|-----------|
| Task plans | 4,200 | ~2,100 | 50% |
| Validation blocks | 2,500 | ~750 | 70% |
| Stage patterns | 3,000 | ~1,800 | 40% |
| **Total** | **12,000** | **~5,500** | **54%** |

---

## Updates

### 2025-10-21: Initiative Created

**Progress:**

- ✅ Phase 1 complete (research & analysis)
- ✅ Comprehensive execution plan created
- ✅ Analysis tooling validated
- ✅ Decision made on user input refinement (not pursuing)

**Next Steps:**

- Begin Phase 2: Apply improvements to Tier 1 workflows
- Strict validation protocol for each workflow
- Individual commits with metrics

**Blockers:** None

---

## Files Modified (To Be Updated)

**Workflows:**

- All 21 workflow files in `.windsurf/workflows/`

**New Documentation:**

- `.windsurf/docs/task-plan-patterns.md`
- `.windsurf/docs/input-handling-patterns.md`
- `.windsurf/docs/validation-patterns.md`

**New Scripts:**

- `scripts/validate_cross_references.py`
- `scripts/validate_task_format.py`

**Configuration:**

- `.pre-commit-config.yaml`
- `.github/workflows/validate-workflows.yml` (new)

**Updated Documentation:**

- `docs/CONSTITUTION.md`
- `.windsurf/rules/05_windsurf_structure.md`
- `README.md`

---

**Estimated Total Effort:** 12-16 hours across 4-6 sessions
**Expected Completion:** 2025-10-25
