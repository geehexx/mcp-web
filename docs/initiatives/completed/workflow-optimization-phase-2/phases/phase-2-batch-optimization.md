# Phase 2: Batch Workflow Optimization

**Status:** ⏳ Pending (POC complete, ready to proceed)
**Duration:** 6-8 hours across 2-3 sessions  
**Priority:** High

---

## Objective

Apply validated intelligent semantic preservation methodology to remaining 16 workflows systematically, achieving 15-30% variable token reduction while maintaining ≥92% semantic preservation.

---

## Prerequisites

- ✅ POC validated on `bump-version.md` (98.63% preservation, 5/5 idempotency tests)
- ✅ Intelligent methodology proven superior to mechanical
- ✅ Workflows updated with methodology (`improve-prompt.md` v3.0, `improve-workflow.md` v2.0)
- ✅ Compression decision matrix established

---

## Workflow Prioritization

### High-Priority Workflows (5 workflows)

**Criteria:** Critical workflows, high complexity, frequent use

| Workflow | Current Tokens | Complexity | Priority Reason |
|----------|---------------|------------|-----------------|
| **work.md** | 1923 | 85 | Central orchestration |
| **detect-context.md** | 2200 | 80 | Core routing logic |
| **implement.md** | 1400 | 75 | Primary dev workflow |
| **validate.md** | 2200 | 70 | Quality gates |
| **research.md** | 2350 | 70 | Common operation |

**Expected Reduction:** 15-25% (variable based on quality assessment)

### Medium-Priority Workflows (6 workflows)

**Criteria:** Moderate complexity, regular use

| Workflow | Current Tokens | Complexity | Priority Reason |
|----------|---------------|------------|-----------------|
| **generate-plan.md** | 2150 | 70 | Planning workflow |
| **load-context.md** | 2300 | 65 | Context loading |
| **plan.md** | 2200 | 70 | Initiative planning |
| **meta-analysis.md** | 1900 | 65 | Session summaries |
| **consolidate-summaries.md** | 2800 | 65 | Consolidation logic |
| **extract-session.md** | 1700 | 60 | Session extraction |

**Expected Reduction:** 20-30% (moderate quality, good compression potential)

### Low-Priority Workflows (5 workflows)

**Criteria:** Simple workflows, occasional use

| Workflow | Current Tokens | Complexity | Priority Reason |
|----------|---------------|------------|-----------------|
| **archive-initiative.md** | 1500 | 55 | Archival |
| **commit.md** | 1812 | 60 | Git operations |
| **new-adr.md** | 995 | 50 | ADR creation |
| **summarize-session.md** | 1350 | 55 | Session summary |
| **update-docs.md** | 1500 | 55 | Doc updates |

**Expected Reduction:** 25-35% (simpler workflows, higher compression potential)

---

## Execution Strategy

### Session 1: High-Priority Workflows (3-4 hours)

**Batch 1 (3 workflows):**
1. `work.md` - Central orchestration
2. `detect-context.md` - Routing logic
3. `implement.md` - Dev workflow

**Process per workflow:**
1. Read current version
2. Apply Layer 1 (Semantic Analysis)
3. Determine strategy from decision matrix
4. Apply Layers 2-3 (Compression)
5. Validate Layer 4 (Semantic Validation ≥92%)
6. Test Layer 5 (Idempotency)
7. Commit with metrics

**Commit message format:**
```
feat(workflows): apply intelligent semantic preservation to <workflow>

Metrics:
- Semantic preservation: X.XX%
- Token reduction: XXXX → XXXX (-XX%)
- Word reduction: XXXX → XXXX (-XX%)
- Idempotency: X/5 tests passed
- Version: v2.0-intelligent-semantic-preservation

Quality Dimensions:
- Entity preservation: XX%
- Decision logic: XX%
- Task syntax: XX%
- Relationships: XX%
- Anchors: XX%

Strategy: [Aggressive/Moderate/Selective/Minimal]
```

**Batch 2 (2 workflows):**
4. `validate.md` - Quality gates
5. `research.md` - Research workflow

### Session 2: Medium-Priority Workflows (2-3 hours)

**Batch 3 (3 workflows):**
6. `generate-plan.md`
7. `load-context.md`
8. `plan.md`

**Batch 4 (3 workflows):**
9. `meta-analysis.md`
10. `consolidate-summaries.md`
11. `extract-session.md`

### Session 3: Low-Priority Workflows (2 hours)

**Batch 5 (5 workflows):**
12. `archive-initiative.md`
13. `commit.md`
14. `new-adr.md`
15. `summarize-session.md`
16. `update-docs.md`

**Final workflow:**
17. `work-routing.md` (1705 tokens) - Already optimized, verify only
18. `work-session-protocol.md` (1550 tokens) - Already optimized, verify only

---

## Quality Assurance Per Workflow

### Pre-Optimization Checklist

- [ ] Read workflow completely
- [ ] Assess quality (1-10 scale)
- [ ] Count tokens accurately
- [ ] Identify critical elements (decision logic, task syntax, examples)
- [ ] Select strategy from decision matrix

### Post-Optimization Checklist

- [ ] Semantic preservation ≥92% (Layer 4 validation)
- [ ] All 5 idempotency tests pass
- [ ] Markdown linting passes (0 errors)
- [ ] Version field added (v2.0-intelligent-semantic-preservation)
- [ ] Commit message includes detailed metrics
- [ ] Artifacts saved if needed

### Validation Dimensions

| Dimension | Weight | Threshold | Measurement |
|-----------|--------|-----------|-------------|
| Entity preservation | 30% | ≥90% | Count critical terms preserved |
| Decision logic intact | 25% | ≥98% | Verify if/else, thresholds |
| Task syntax valid | 20% | =100% | Check update_plan, stage structure |
| Relationship preserved | 15% | ≥85% | Verify cross-references, dependencies |
| Anchor retention | 10% | ≥90% | Check technical terms, quality criteria |

---

## Token Reduction Targets

### Expected Outcomes (Variable, Not Uniform)

| Priority | Workflows | Current Total | Target Reduction | Expected Total |
|----------|-----------|---------------|------------------|----------------|
| High | 5 | 10,073 | 15-25% | 7,555-8,562 |
| Medium | 6 | 13,050 | 20-30% | 9,135-10,440 |
| Low | 5 | 7,157 | 25-35% | 4,652-5,368 |
| **Total** | **16** | **30,280** | **~20-28%** | **21,342-24,370** |

**Note:** Variance expected and healthy - different workflows have different compression potential

### Combined Token Count Projection

| Checkpoint | Workflows | Rules | Combined | vs Threshold |
|------------|-----------|-------|----------|--------------|
| Before Phase 2 | 40,935 | 26,190 | 67,125 | -17,875 (under) |
| After Phase 2 | ~33,000-36,000 | 26,190 | ~59,190-62,190 | -22,810 to -25,810 (under) |

**Current Status:** Already under 85k threshold after POC

**Phase 2 Goal:** Further reduce while maintaining quality

---

## Risk Management

### Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Semantic loss despite validation | Low | High | Multi-layer validation, manual review for high-complexity workflows |
| Over-compression of critical workflows | Low | High | Use "Minimal" strategy (10% max) for complexity >80 |
| Time overrun (>8 hours) | Medium | Low | Batch size flexible, can pause at any checkpoint |
| Quality regression | Low | Medium | Pre-commit hooks, markdown linting, idempotency tests |

### Quality Gates

**Fail criteria (stop and review):**
- Semantic preservation <92%
- Idempotency tests <4/5 passed
- Markdown linting errors
- Decision logic modified unintentionally

**If fail:** Rollback, analyze, adjust strategy, retry

---

## Success Criteria

### Phase 2 Completion Criteria

- [ ] All 16 workflows optimized with intelligent methodology
- [ ] Average semantic preservation ≥92%
- [ ] All workflows pass idempotency tests (≥4/5)
- [ ] Token reduction shows variance (15-35% range, not uniform)
- [ ] All workflows have version field (v2.0)
- [ ] All changes committed with detailed metrics
- [ ] No markdown linting errors
- [ ] Combined token count remains <85k

### Quality Metrics Targets

- **Average semantic preservation:** ≥92%
- **Entity preservation:** ≥90% across all workflows
- **Decision logic integrity:** 100% (no changes to logic)
- **Idempotency pass rate:** ≥95% (minimum 4/5 tests per workflow)

---

## Artifacts to Create

### Per-Workflow Artifacts (Optional)

Create only if workflow has unique findings:

- `artifacts/phase2-poc/<workflow>-validation.md` - Semantic validation report
- `artifacts/phase2-poc/<workflow>-comparison.md` - Before/after comparison

### Phase 2 Summary Artifact

Create at end of phase:

- `artifacts/phase2-batch-optimization-summary.md` - Complete phase summary
  - Total token reduction
  - Average semantic preservation
  - Idempotency pass rate
  - Variance analysis (prove not uniform)
  - Lessons learned
  - Edge cases encountered

---

## Workflow Decomposition (Conditional)

**Trigger:** If workflow >6000 tokens after optimization OR complexity >85

**Candidates:**
- `work.md` (complexity 85, currently 1923 tokens - unlikely)
- `detect-context.md` (complexity 80, currently 2200 tokens - unlikely)

**Action:** Flag for Phase 3 decomposition evaluation

---

## Next Phase Prep

**Phase 3 (if needed):** Workflow decomposition for flagged workflows

**Phase 4 (always):** Duplication reduction via shared patterns

---

## References

- [Phase 1 Foundation](./phase-1-foundation.md) - Methodology and POC
- [POC Results](../artifacts/phase2-poc/poc-results.md) - bump-version.md validation
- [Intelligent Compression V2](../artifacts/phase1-research/intelligent-compression-v2.md) - 5-layer methodology
- [Idempotency Framework](../artifacts/phase1-research/idempotency-framework-integration.md) - Testing framework

---

**Ready to Execute:** All prerequisites met, methodology validated, tools available
