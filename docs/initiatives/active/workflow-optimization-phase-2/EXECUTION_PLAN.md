# Workflow Optimization Phase 2: Execution Plan

**Created:** 2025-10-21
**Status:** Ready for Execution
**Estimated Effort:** 12-16 hours (4-6 sessions)

---

## Executive Summary

Systematically apply `/improve-prompt` and `/improve-workflow` to all 21 workflows, reduce duplication, add quality gates, and bring token count below 85k threshold.

**Success Criteria:**

- [ ] All workflows improved and validated
- [ ] Combined token count < 85,000
- [ ] Duplication reduced by >30%
- [ ] Quality gates in place
- [ ] Documentation complete

---

## Phase 1: Research & Analysis ✅ COMPLETE

### Key Findings

**Prompt Modularity Research (DEV 2025):**

- Break prompts into reusable components
- Avoid duplicating critical instructions
- Use partials/templates for shared logic

**Duplication Analysis:**

- 21 workflows, 66,355 tokens
- 26 duplication instances
- Est. waste: 8,000-12,000 tokens

#### User Input Refinement Evaluation

Decision: ❌ NOT RECOMMENDED

- Only 1/21 workflows needs it (improve-prompt already has it)
- Existing patterns work well (@-mentions, context detection, clarifying questions)
- Would add 200-300 tokens per workflow for minimal benefit
- Document patterns instead of creating sub-workflow

---

## Phase 2: Batch Workflow Improvements

**Duration:** 4-6 hours
**Status:** ⏳ Pending

### Prioritization

**Tier 1 (High Impact):** consolidate-summaries, implement, plan, improve-workflow, bump-version
**Tier 2 (Moderate):** work-session-protocol, work-routing, meta-analysis, detect-context, work
**Tier 3 (Small):** Remaining 11 workflows

### Validation Protocol (MANDATORY FOR EACH)

```bash
# 1. Run improvement
/improve-prompt @workflow:<name>

# 2-6. Automated validation
python scripts/validate_workflows.py
python scripts/check_workflow_tokens.py --workflow <name>

# 7. Human checklist
- [ ] Intent preserved
- [ ] Examples sufficient (2-3)
- [ ] Task management intact
- [ ] Cross-references valid

# 8. Commit individually
git add .windsurf/workflows/<name>.md
git commit -m "refactor(workflows): apply conciseness to <name> (-X%)"
```

### Iterative Refinement

If improvement suboptimal:

1. Analyze issue (too aggressive? too conservative? broke something?)
2. Adjust improve-workflow techniques
3. Re-run on same workflow
4. Document learnings

---

## Phase 3: Decomposition (Conditional)

**Duration:** 3-4 hours
**Status:** ⏳ Pending (triggers if Phase 2 flags workflows)

**Candidates:** detect-context (complexity 80), work (complexity 85)

**Decision Criteria:**

- DO decompose: Clear boundaries, stages >500 tokens, reusable components
- DON'T decompose: Complexity is inherent, sub-workflows add overhead

---

## Phase 4: Duplication Reduction

**Duration:** 3-4 hours
**Status:** ⏳ Pending

### 4.1 Task Plan Pattern (Est. savings: 2,100 tokens)

Create `.windsurf/docs/task-plan-patterns.md` with standard patterns.
Update workflows to reference instead of duplicating examples.

### 4.2 Validation Pattern (Est. savings: 2,250 tokens)

Enhance `/validate` with composable functions.
Update workflows to reference validate.md instead of duplicating.

### 4.3 Input Handling Documentation

Create `.windsurf/docs/input-handling-patterns.md` documenting 5 patterns:

1. @-Mention (File/Directory)
2. Context Detection (Autonomous)
3. Clarifying Questions (Interactive)
4. Structured Input (Form-like)
5. No Input (State-based)

**Anti-pattern documented:** Generic input refinement sub-workflow (not needed)

### 4.4 Load-Context Enhancement

Add scope=auto for intelligent scope detection.

**Total Est. Reduction:** 6,500 tokens (duplication) + 3,900 tokens (conciseness) = 10,400 tokens

---

## Phase 5: Quality Gates

**Duration:** 2-3 hours
**Status:** ⏳ Pending

### New Validation Scripts

1. **`scripts/validate_cross_references.py`** - Catch broken links
2. **`scripts/validate_task_format.py`** - Ensure update_plan format correct
3. **Enhanced token check** - Add `--enforce` flag

### Pre-commit Hooks

Add to `.pre-commit-config.yaml`:

- validate-cross-references
- validate-task-format
- check-workflow-tokens --enforce

### CI/CD Pipeline

Create `.github/workflows/validate-workflows.yml` for PR validation.

---

## Phase 6: Documentation

**Duration:** 1-2 hours
**Status:** ⏳ Pending

**Create:**

1. `.windsurf/docs/task-plan-patterns.md`
2. `.windsurf/docs/input-handling-patterns.md`
3. `.windsurf/docs/validation-patterns.md`

**Update:**

1. `docs/CONSTITUTION.md` - Workflow modularity section
2. `.windsurf/rules/05_windsurf_structure.md` - Duplication reduction
3. `README.md` - Updated metrics

---

## Phase 7: Validation & Acceptance

**Duration:** 1 hour
**Status:** ⏳ Pending

### Final Checklist

- [ ] All workflows pass validation
- [ ] Token count < 85,000
- [ ] No broken cross-references
- [ ] Pre-commit hooks working
- [ ] CI/CD pipeline green
- [ ] Documentation complete

### Acceptance Criteria

**Must achieve:**

- ✅ Token reduction ≥20%
- ✅ Duplication reduction ≥30%
- ✅ All validation passing

---

## Execution Timeline

| Session | Focus | Duration | Checkpoint |
|---------|-------|----------|------------|
| 1 | Tier 1 improvements (5 workflows) | 2-3h | -1,900 tokens |
| 2 | Tier 2 improvements (5 workflows) | 2-3h | -1,200 tokens |
| 3 | Tier 3 + duplication reduction | 3-4h | -3,600 tokens |
| 4 | Quality gates implementation | 2-3h | All gates passing |
| 5 | Documentation & cleanup | 1-2h | Complete |

**Total Expected Reduction:** 10,400 tokens (15.7% of total)
**Final Token Count:** ~82,700 (below 85k threshold)

---

## Risk Management

| Risk | Impact | Mitigation |
|------|--------|------------|
| Over-optimization | Medium | Validate after each, human review, can rollback |
| Breaking changes | High | Comprehensive validation, individual commits |
| Threshold still exceeded | Low | Conservative estimates, can decompose more |
| Time overrun | Low | Phased approach, each phase delivers value |

---

## Next Steps

**Immediate actions:**

1. Begin Session 1: Tier 1 workflow improvements
2. Apply validation protocol strictly
3. Commit after each validated improvement
4. Track metrics in analysis tool

**Supporting artifacts created:**

- `EXECUTION_PLAN.md` (this file)
- Analysis results in `.windsurf/workflow-improvement-analysis.json`
- Improvement tool: `scripts/analyze_workflow_improvements.py`

---

**Ready to execute** - All research complete, plan validated, tooling in place.
