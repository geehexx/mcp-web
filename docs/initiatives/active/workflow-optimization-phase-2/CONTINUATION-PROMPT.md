# Continuation Prompt: Workflow Optimization Phase 2 Batch Optimization

**Purpose:** Optimized prompt to continue Phase 2 batch workflow optimization
**Session:** Next session after 2025-10-21
**Context:** Phase 1 complete (methodology validated), Phase 2 ready to execute
**Copy-paste this entire prompt into your next session**

---

## Context Summary

You are continuing the **workflow-optimization-phase-2** initiative. Phase 1 is complete with validated intelligent semantic preservation methodology. Phase 2 is ready to execute: systematic batch optimization of 16 remaining workflows.

### Current State

**Initiative:** [`docs/initiatives/active/workflow-optimization-phase-2/`](docs/initiatives/active/workflow-optimization-phase-2/)

**Phase 1 Status:** ✅ Complete
- Intelligent 5-layer methodology designed and validated
- POC on `bump-version.md`: 98.63% semantic preservation, 5/5 idempotency tests
- Methodology integrated into `improve-prompt.md` v3.0 and `improve-workflow.md` v2.0
- Proven superior to mechanical optimization despite 8.6% token cost

**Phase 2 Status:** ⏳ Ready to Execute
- 16 workflows awaiting optimization
- Prioritization complete (5 high, 6 medium, 5 low)
- Execution plan ready in [`phases/phase-2-batch-optimization.md`](docs/initiatives/active/workflow-optimization-phase-2/phases/phase-2-batch-optimization.md)

**Token Counts:**
- Workflows: 40,935 tokens (21 workflows)
- Rules: 26,190 tokens (16 rules)
- Combined: 67,125 tokens ✅ (under 85k threshold)

---

## Your Task

Execute **Phase 2: Batch Workflow Optimization** systematically.

**Goal:** Apply intelligent semantic preservation methodology to 16 workflows, achieving:
- ≥92% semantic preservation (average)
- 15-30% variable token reduction (not uniform)
- ≥95% idempotency pass rate
- All workflows pass markdown linting

---

## Execution Plan

### Session 1: High-Priority Workflows (3-4 hours)

**Batch 1 (3 workflows):**
1. `work.md` (1923 tokens, complexity 85)
2. `detect-context.md` (2200 tokens, complexity 80)
3. `implement.md` (1400 tokens, complexity 75)

**Batch 2 (2 workflows):**
4. `validate.md` (2200 tokens, complexity 70)
5. `research.md` (2350 tokens, complexity 70)

### Process Per Workflow

Apply **5-Layer Intelligent Methodology:**

**Layer 1: Semantic Analysis**
1. Read workflow completely
2. Assess quality (1-10 scale)
3. Count tokens accurately  
4. Identify critical elements:
   - Decision logic (if/else, thresholds)
   - Task syntax (`update_plan` calls, stage structure)
   - Key examples (keep 2-3 best)
   - Technical terms and anchors
5. Identify preservation vs compression zones
6. Select strategy from decision matrix

**Layer 2-3: Coarse + Fine Compression**
1. Apply section-level budget allocation:
   - Decision matrices: 90% preservation
   - Examples: 60% preservation
   - Descriptive prose: 40% preservation
2. Apply token-level optimization:
   - Preserve: decision thresholds, function signatures, technical terms
   - Compress: filler phrases, verbose instructions, redundant modifiers
3. Consolidate examples (keep 2-3 representative)
4. Use tables for structured data
5. Remove duplication

**Layer 4: Semantic Validation**

Calculate multi-dimensional preservation score:

| Dimension | Weight | Threshold | Measurement |
|-----------|--------|-----------|-------------|
| Entity preservation | 30% | ≥90% | Count critical terms preserved |
| Decision logic intact | 25% | ≥98% | Verify if/else, thresholds unchanged |
| Task syntax valid | 20% | =100% | Check `update_plan`, stage structure |
| Relationship preserved | 15% | ≥85% | Verify cross-references, dependencies |
| Anchor retention | 10% | ≥90% | Check technical terms, quality criteria |

**Overall score must be ≥92%**

**Layer 5: Idempotency Testing**

Run 5 tests:
1. **Content stability:** Would re-optimization change output? (<5% drift acceptable)
2. **Version field:** Check v2.0-intelligent-semantic-preservation present
3. **Semantic drift:** Compare critical elements (0% drift expected)
4. **Token stability:** Re-optimization token drift ≤10 tokens
5. **Hash match:** Ideally exact match on re-optimization

**Pass criteria:** ≥4/5 tests pass

### Commit Per Workflow

```bash
git commit -m "feat(workflows): apply intelligent semantic preservation to <workflow>

Metrics:
- Semantic preservation: X.XX%
- Token reduction: XXXX → XXXX (-XX.X%)
- Word reduction: XXXX → XXXX (-XX.X%)
- Idempotency: X/5 tests passed
- Version: v2.0-intelligent-semantic-preservation

Quality Dimensions:
- Entity preservation: XX.X%
- Decision logic: XX.X%
- Task syntax: XX.X%
- Relationships: XX.X%
- Anchors: XX.X%

Strategy: [Aggressive/Moderate/Selective/Minimal] (based on quality X/10, tokens XXXX)

Key Changes:
- [List 2-3 most significant changes]

Initiative: workflow-optimization-phase-2
Phase: 2 (batch optimization)
"
```

---

## Compression Decision Matrix

Use this to select strategy per workflow:

| Quality | Tokens | Strategy | Max Reduction | Validation |
|---------|--------|----------|---------------|------------|
| <6/10 | Any | Aggressive restructure | 60% | Standard |
| 6-7/10 | <2000 | Balanced | 30% | Standard |
| 6-7/10 | >2000 | Moderate | 40% | Enhanced |
| 7-8/10 | <2000 | Light polish | 15% | Strict |
| 7-8/10 | >2000 | Selective | 25% | Strict |
| >8/10 | Any | **Minimal** | 10% | Very Strict |

**Key Principle:** Variable reduction based on content, NOT uniform percentages

---

## Quality Gates

### Pre-Optimization Checklist

Before optimizing each workflow:
- [ ] Workflow read completely
- [ ] Quality assessed (1-10)
- [ ] Token count accurate
- [ ] Critical elements identified
- [ ] Strategy selected from matrix

### Post-Optimization Checklist

After optimizing each workflow:
- [ ] Semantic preservation ≥92%
- [ ] Idempotency tests ≥4/5 pass
- [ ] Markdown linting passes (0 errors)
- [ ] Version field added (v2.0-intelligent-semantic-preservation)
- [ ] Commit message includes detailed metrics

### Fail Criteria (Stop and Review)

- Semantic preservation <92%
- Idempotency tests <4/5 pass
- Markdown linting errors
- Decision logic modified unintentionally

**If fail:** Rollback, analyze, adjust strategy, retry

---

## Success Criteria

**For Phase 2 completion:**

- [ ] All 16 workflows optimized with intelligent methodology
- [ ] Average semantic preservation ≥92%
- [ ] Token reduction shows variance (15-35% range, not uniform)
- [ ] All workflows pass idempotency tests (≥4/5)
- [ ] All workflows have version field (v2.0)
- [ ] All changes committed with detailed metrics
- [ ] No markdown linting errors
- [ ] Combined token count remains <85k

---

## Reference Documents

**Load these for context:**

1. **[phases/phase-2-batch-optimization.md](docs/initiatives/active/workflow-optimization-phase-2/phases/phase-2-batch-optimization.md)**
   - Complete execution plan
   - Workflow prioritization matrix
   - Session-by-session breakdown
   - Risk management

2. **[phases/phase-1-foundation.md](docs/initiatives/active/workflow-optimization-phase-2/phases/phase-1-foundation.md)**
   - 5-layer methodology details
   - Research findings (LLMLingua, semantic preservation)
   - Compression decision matrix
   - POC results and learnings

3. **[artifacts/phase2-poc/poc-results.md](docs/initiatives/active/workflow-optimization-phase-2/artifacts/phase2-poc/poc-results.md)**
   - POC example (bump-version.md)
   - Validation metrics
   - What worked well

4. **[initiative.md](docs/initiatives/active/workflow-optimization-phase-2/initiative.md)**
   - Initiative overview
   - Current status
   - Success criteria

---

## Commands

### Start Session

```bash
# Navigate to project
cd /home/gxx/projects/mcp-web

# Load initiative context
/work  # Will detect active initiative and route to implementation
```

### During Session

```bash
# Check current token count
python scripts/check_workflow_tokens.py

# Run markdown linting
task docs:lint:markdown

# Check git status
git status
```

---

## Expected Outcomes

**After Session 1 (5 high-priority workflows):**
- ~10,073 tokens → ~7,555-8,562 tokens (15-25% reduction)
- Average semantic preservation: ≥92%
- All workflows: v2.0 version field
- 5 commits with detailed metrics

**After Complete Phase 2 (16 workflows):**
- ~30,280 tokens → ~21,342-24,370 tokens (20-28% reduction)
- Average semantic preservation: ≥92%
- Combined total: ~59,190-62,190 tokens (well under 85k)

---

## Anti-Patterns to Avoid

❌ **Don't:**
- Apply uniform reduction percentages (mechanical approach)
- Remove concrete examples entirely
- Over-compress high-complexity workflows (use "Minimal" strategy)
- Skip semantic validation
- Skip idempotency testing
- Commit without detailed metrics

✅ **Do:**
- Use quality-based strategies (decision matrix)
- Preserve 2-3 best examples
- Match compression to workflow complexity
- Validate every dimension
- Test idempotency
- Document metrics thoroughly

---

## Workflow Locations

All workflows in: `.windsurf/workflows/`

**High-Priority (Session 1):**
- work.md
- detect-context.md
- implement.md
- validate.md
- research.md

**Medium-Priority (Session 2):**
- generate-plan.md
- load-context.md
- plan.md
- meta-analysis.md
- consolidate-summaries.md
- extract-session.md

**Low-Priority (Session 3):**
- archive-initiative.md
- commit.md
- new-adr.md
- summarize-session.md
- update-docs.md

---

## Notes

- **POC Proven:** bump-version.md achieved 98.63% preservation
- **Methodology Validated:** 5-layer approach works
- **Variable Reduction Expected:** Different workflows will have different percentages (15-35% range)
- **Quality First:** Semantic preservation > token count
- **Idempotency Matters:** Version tracking prevents re-optimization

---

## Tips for Success

1. **Read completely before optimizing** - Understand structure
2. **Use decision matrix consistently** - Match strategy to quality/tokens
3. **Validate rigorously** - All 5 layers, every workflow
4. **Commit individually** - One workflow per commit with metrics
5. **Track variance** - Expect and celebrate different reduction percentages
6. **Document learnings** - Note edge cases for future workflows

---

**Ready to Execute:** Phase 1 complete, Phase 2 ready, methodology validated

**Estimated Time:** 2-3 hours for first batch (5 workflows)

**Start Command:** `/work` → Will detect initiative and route to implementation

---

**Good luck with Phase 2 batch optimization!**
