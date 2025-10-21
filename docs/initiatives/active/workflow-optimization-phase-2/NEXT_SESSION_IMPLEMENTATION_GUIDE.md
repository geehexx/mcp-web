# Next Session Implementation Guide

**Date:** 2025-10-21  
**Session:** 5 (Phase 1 Completion)  
**Estimated Duration:** 2-3 hours  
**Priority:** High

---

## Objective

Complete Phase 1 foundation by updating `improve-prompt.md` and `improve-workflow.md` workflows with the intelligent methodology + idempotency framework, then execute POC validation.

---

## Prerequisites

**Already Complete (Session 4):**

- ✅ Intelligent compression methodology V2 (`artifacts/intelligent-compression-v2.md`)
- ✅ Idempotency framework design (`artifacts/idempotency-framework-integration.md`)
- ✅ Comprehensive Plan V3 (`COMPREHENSIVE_PLAN_V3.md`)
- ✅ Initiative updated with Session 4 progress
- ✅ Research completed (LLMLingua, semantic preservation, information theory)

**Required for Next Session:**

- [ ] Update `improve-prompt.md` workflow
- [ ] Update `improve-workflow.md` workflow
- [ ] Execute POC on 1 workflow
- [ ] Validate semantic preservation metrics
- [ ] Commit all changes

---

## Step-by-Step Implementation

### Step 1: Update `improve-prompt.md` (45-60 minutes)

**File:** `.windsurf/workflows/improve-prompt.md`

**Use MCP tools (CRITICAL):**

```bash
# Read current version
mcp0_read_text_file(path="/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md")

# Edit using mcp0_edit_file (NOT regular edit tool)
mcp0_edit_file(path="/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md", ...)
```

**Changes Required:**

#### A. Add to Stage 2.5 (Model Detection)

**Insert after section 2.5.3 (Special Constraints):**

```markdown
### 2.5.5 Idempotency Pre-Check

**Before optimization:**

1. Calculate optimization hash (content + config + methodology v2.0)
2. Check cache: `.windsurf/.optimization-cache.json`
3. If cache hit: Return cached result immediately with note
4. If cache miss: Proceed with optimization

**Hash components:**
- Content SHA-256
- Methodology version: v2.0
- Enabled techniques
- Preservation thresholds
- Model + temperature=0.0 + seed=42
```

#### B. Update Stage 3 (Analyze Current Prompt)

**Replace quality assessment section with:**

```markdown
### 3.1 Semantic Analysis (Layer 1)

**Before any compression, extract semantic structure:**

```python
semantic_profile = {
    "decision_logic": extract_decision_points(content),
    "key_entities": extract_entities_ner(content),  # Technical terms, functions, names
    "examples": identify_examples(content),
    "preservation_zones": identify_critical_sections(content),
    "compression_zones": identify_redundancy(content)
}
```

**Preservation priorities:**

- **Critical (100%):** Decision logic, task syntax, workflow calls
- **High (>90%):** Key entities, technical terms, constraints
- **Medium (>70%):** Examples, explanations
- **Low (<50%):** Redundant phrases, verbose formatting

```

#### C. Update Stage 4 (Apply Universal Optimizations)

**Add at the beginning:**

```markdown
### 4.0 Apply Compression Decision Matrix

**Determine strategy based on quality + token count:**

| Original Quality | Token Count | Strategy | Max Reduction | Validation Level |
|-----------------|-------------|----------|---------------|------------------|
| <6/10 | Any | Aggressive restructure | 60% | Standard |
| 6-7/10 | <2000 | Balanced | 30% | Standard |
| 6-7/10 | >2000 | Moderate | 40% | Enhanced |
| 7-8/10 | <2000 | Light polish | 15% | Strict |
| 7-8/10 | >2000 | Selective | 25% | Strict |
| >8/10 | Any | **Minimal** | 10% | Very strict |

**Apply strategy to technique selection and aggressiveness.**
```

#### D. Add to Stage 6 (Validate Improvements)

**Insert new validation section:**

```markdown
### 6.5 Semantic Preservation Validation (Layer 4)

**Multi-dimensional quality check:**

```python
scores = {
    "entity_preservation": measure_overlap(original_entities, compressed_entities),  # Target: ≥90%
    "decision_logic_intact": verify_all_present(decision_points, compressed),         # Target: ≥98%
    "examples_sufficient": count_examples(compressed) >= 2,                            # Target: 2-3 per concept
    "anchors_retained": measure_anchor_overlap(original_anchors, compressed)          # Target: ≥90%
}

total_score = (
    scores["entity_preservation"] * 0.30 +
    scores["decision_logic_intact"] * 0.25 +
    scores["examples_sufficient"] * 0.20 +
    scores["anchors_retained"] * 0.25
)

# PASS criteria: total_score >= 0.92 (92%)
```

**If validation fails:** Reduce compression aggressiveness and retry.

```

#### E. Add New Stage 6.6 (Idempotency Testing)

**Insert before Stage 7:**

```markdown
### 6.6 Idempotency Verification (Layer 5)

**Test that re-optimization produces NO changes:**

```python
# Test 1: Hash-based exact match
re_compressed = optimize(compressed_content, same_config)
hash_match = (sha256(compressed) == sha256(re_compressed))

# Test 2: Semantic similarity (allow minor variations)
similarity = semantic_similarity_score(compressed, re_compressed)

# Test 3: Token drift
token_drift = abs(count_tokens(compressed) - count_tokens(re_compressed))

# PASS criteria:
assert hash_match OR (similarity >= 0.98 AND token_drift <= 10)
```

**If idempotency fails:** Flag for manual review, do NOT cache.

**If idempotency passes:** Update cache with result.

```

#### F. Update Stage 8 (Present Results)

**Add to output template:**

```markdown
## Semantic Preservation Metrics

| Dimension | Score | Threshold | Status |
|-----------|-------|-----------|--------|
| Entity Preservation | [N]/10 | ≥9.0 | ✅/❌ |
| Decision Logic Intact | [N]/10 | ≥9.8 | ✅/❌ |
| Examples Sufficient | [N]/10 | ≥7.0 | ✅/❌ |
| Anchor Retention | [N]/10 | ≥9.0 | ✅/❌ |
| **Overall Score** | **[N]/10** | **≥9.2** | **✅/❌** |

## Idempotency Test

- Hash Match: ✅/❌
- Semantic Similarity: [N]% (threshold: ≥98%)
- Token Drift: [N] tokens (threshold: ≤10)
- **Status:** ✅ PASSED / ❌ FAILED

## Cache Status

- ✅ Cached for future optimizations (hash: [first 8 chars])
- ❌ Not cached (idempotency failed)
```

#### G. Update Frontmatter

```yaml
---
created: "2025-10-21"
updated: "2025-10-21"
description: LLM-agnostic prompt optimization with intelligent semantic preservation and idempotency
auto_execution_mode: 2
category: Optimization
complexity: 75  # Increased due to semantic validation
tokens: 3500    # Estimate (will be updated after implementation)
dependencies:
  - improve-workflow
status: active
version: "3.0-intelligent-semantic-preservation"
---
```

---

### Step 2: Update `improve-workflow.md` (30-45 minutes)

**File:** `.windsurf/workflows/improve-workflow.md`

**Changes Required:**

#### A. Update Stage 0.2 (Conciseness Priority)

**Replace with Compression Decision Matrix reference:**

```markdown
### 0.2 Apply Compression Decision Matrix

**Use same matrix as `/improve-prompt` Stage 4.0:**

Determine strategy based on workflow quality + token count.

**See:** `improve-prompt.md` Stage 4.0 for complete matrix.

**Workflow-specific adjustments:**
- Complexity >75: Reduce max reduction by 10%
- Stage count >10: Light polish only (max 15% reduction)
- Calls >5 workflows: Preserve all cross-references
```

#### B. Add Stage 0.3 (Idempotency Pre-Check)

**Insert after 0.2:**

```markdown
### 0.3 Idempotency Pre-Check

**Check if workflow already optimized:**

1. **Method 1:** Cache lookup by hash
2. **Method 2:** Frontmatter `version` field contains "intelligent" or "semantic"
3. **Method 3:** Token count vs target delta < 50 tokens

**If already optimized:**
- Return unchanged with note: "Already optimized (cached/version/stable)"
- Skip all optimization stages
```

#### C. Update Stage 2 (Windsurf-Aware Conciseness)

**Add semantic preservation layer:**

```markdown
### 2.0 Semantic Preservation Layer

**Before applying conciseness techniques:**

1. Extract `update_plan` calls (100% preserve syntax)
2. Extract stage numbering (100% preserve)
3. Extract workflow entry/exit announcements (100% preserve)
4. Extract cross-references (100% preserve)
5. Identify task attribution patterns (preserve format)

**Apply conciseness techniques ONLY to:**
- Explanatory prose
- Examples (keep 2-3 best)
- Verbose instructions
- Redundant descriptions
```

#### D. Update Stage 3.4 (Idempotency Testing)

**Replace with comprehensive version:**

```markdown
### 3.4 Idempotency Testing

**For workflows, test multiple dimensions:**

```python
# Test 1: Re-optimize produces no changes
re_optimized = optimize_workflow(compressed, same_config)
exact_match = (compressed == re_optimized)

# Test 2: update_plan calls unchanged
original_plans = extract_update_plan_calls(compressed)
re_optimized_plans = extract_update_plan_calls(re_optimized)
plans_match = (original_plans == re_optimized_plans)

# Test 3: Frontmatter integrity
frontmatter_intact = verify_frontmatter(compressed, re_optimized)

# Test 4: Workflow entry/exit preserved
markers_intact = verify_workflow_markers(compressed, re_optimized)

# PASS criteria: ALL tests pass
assert exact_match AND plans_match AND frontmatter_intact AND markers_intact
```

**Golden tests:** Use 4 previously optimized workflows as baselines.

```

#### E. Update Frontmatter

```yaml
---
created: "2025-10-21"
updated: "2025-10-21"
description: Optimize Windsurf workflows with intelligent semantic preservation and idempotency
auto_execution_mode: 2
category: Optimization
complexity: 75
tokens: 2000  # Estimate
dependencies:
  - improve-prompt
status: active
version: "2.0-intelligent-semantic-preservation"
---
```

---

### Step 3: Execute POC (30-45 minutes)

**Select POC workflow:** `bump-version.md` (medium complexity, good test case)

**Process:**

1. **Read original workflow:**

```bash
mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/workflows/bump-version.md")
```

2. **Run `/improve-workflow` on it** (manually, since workflows can't call themselves in this context)

3. **Apply intelligent methodology:**
   - Semantic analysis (extract entities, decision logic, examples)
   - Determine strategy (based on quality + token count)
   - Apply compression techniques (table consolidation, example pruning, information distillation)
   - Validate semantic preservation (measure scores)
   - Test idempotency (re-optimize and compare)

4. **Measure metrics:**

```markdown
## POC Results: bump-version.md

**Original:**
- Token count: [N]
- Quality score: [N]/10
- Complexity: [N]

**Optimized:**
- Token count: [N] (-[X]%, [N] tokens saved)
- Quality score: [N]/10
- Complexity: [N]

**Semantic Preservation:**
- Entity preservation: [N]/10
- Decision logic intact: [N]/10
- Examples sufficient: [N]/10
- Anchor retention: [N]/10
- **Overall:** [N]/10 (threshold: ≥9.2)

**Idempotency:**
- Hash match: ✅/❌
- Semantic similarity: [N]%
- Token drift: [N]
- **Status:** ✅ PASSED / ❌ FAILED

**Conclusion:** ✅ Methodology validated / ❌ Needs refinement
```

5. **Document results:**

Create `artifacts/poc-validation-results.md` with full analysis.

---

### Step 4: Validate and Commit (15-20 minutes)

**Validation:**

```bash
# Documentation linting
task docs:lint

# Fix auto-fixable issues
task docs:fix
```

**Commit strategy:**

```bash
# Commit 1: Planning artifacts
git add docs/initiatives/active/workflow-optimization-phase-2/
git commit -m "docs(workflow-opt): Phase 1 foundation - intelligent methodology + idempotency framework

- Created intelligent-compression-v2.md (5-layer LLMLingua-based approach)
- Created idempotency-framework-integration.md (hash caching + semantic validation)
- Created COMPREHENSIVE_PLAN_V3.md (full roadmap with all phases)
- Created NEXT_SESSION_IMPLEMENTATION_GUIDE.md (detailed implementation steps)
- Updated initiative.md with Session 4 progress

Research:
- LLMLingua (Microsoft 2024): 20x compression with minimal loss
- Semantic preservation: >95% entity retention with NER
- Information theory: lossless compression principles

Key methodology:
- 5 layers: Semantic analysis → Coarse/Fine compression → Validation → Idempotency
- Compression decision matrix (variable 15-30% based on quality + token count)
- Multi-dimensional validation (≥92% semantic preservation required)
- Idempotency testing (hash match OR 98% similarity + ≤10 token drift)

Next session: Update improve-prompt.md + improve-workflow.md + execute POC

Refs: #workflow-optimization-phase-2
See: COMPREHENSIVE_PLAN_V3.md for complete plan"

# Commit 2: Workflow updates (next session)
# Commit 3: POC results (next session)
```

---

## Success Criteria

- [ ] `improve-prompt.md` updated with all 7 sections (A-G)
- [ ] `improve-workflow.md` updated with all 5 sections (A-E)
- [ ] POC executed on 1 workflow with full metrics
- [ ] Semantic preservation score ≥ 92%
- [ ] Idempotency test passed
- [ ] All changes committed with detailed messages
- [ ] Documentation linting passed

---

## Troubleshooting

### Issue: MCP tools not working

**Solution:** Use absolute paths and correct tool names:

```python
# ✅ CORRECT
mcp0_read_text_file(path="/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md")

# ❌ WRONG
read_file("/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md")
```

### Issue: Semantic validation scores low

**Solution:** Reduce compression aggressiveness:

- Increase preservation thresholds (decision logic 98% → 100%)
- Keep more examples (2-3 → 3-5)
- Preserve more contextual anchors
- Use less aggressive technique (moderate → light polish)

### Issue: Idempotency test fails

**Solution:** Check for non-deterministic elements:

- Temperature not 0.0
- Seed not fixed
- Timestamp or random data in output
- Re-run with stricter preservation

---

## Estimated Effort Breakdown

| Task | Duration | Complexity |
|------|----------|------------|
| Update improve-prompt.md | 45-60 min | Medium |
| Update improve-workflow.md | 30-45 min | Medium |
| Execute POC | 30-45 min | Medium |
| Validate + commit | 15-20 min | Low |
| **Total** | **2-3 hours** | **Medium** |

---

## Files to Modify (Next Session)

**Primary:**

- `.windsurf/workflows/improve-prompt.md`
- `.windsurf/workflows/improve-workflow.md`

**Create:**

- `artifacts/poc-validation-results.md`
- `.windsurf/.optimization-cache.json` (empty initial structure)

**Update:**

- `initiative.md` (Session 5 progress)

---

## After Completion

**Phase 1 Status:** ✅ Complete

**Next Phase (Phase 2):**

- Restore remaining 17 workflows from git history
- Re-optimize systematically (3-5 per session)
- Validate each with semantic preservation metrics
- Build golden test suite
- Target: 15-30% VARIABLE reduction with >92% semantic preservation

---

**Version:** 1.0  
**Last Updated:** 2025-10-21  
**Status:** Ready for execution
