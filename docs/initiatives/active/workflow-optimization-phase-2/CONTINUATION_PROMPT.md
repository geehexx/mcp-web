# Continuation Prompt for Next Session

**Purpose:** Optimized prompt to continue Workflow Optimization Phase 2 - Phase 1 Completion  
**Session:** 5  
**Estimated Duration:** 2-3 hours  
**Copy-paste this entire prompt into next session**

---

## Session Context

Continue workflow optimization initiative Phase 1 completion. Previous session (Session 4) completed research and planning. This session implements the intelligent methodology into optimization workflows and executes POC validation.

**Previous Session Achievements:**
- ✅ Created 5-layer intelligent compression methodology (LLMLingua-based)
- ✅ Designed idempotency framework (hash caching + semantic validation)
- ✅ Created COMPREHENSIVE_PLAN_V3.md with full roadmap
- ✅ Created NEXT_SESSION_IMPLEMENTATION_GUIDE.md with detailed steps
- ✅ Committed planning artifacts (commit 6986b43)

**Key Files to Reference:**
- `docs/initiatives/active/workflow-optimization-phase-2/NEXT_SESSION_IMPLEMENTATION_GUIDE.md` - Complete implementation guide
- `docs/initiatives/active/workflow-optimization-phase-2/COMPREHENSIVE_PLAN_V3.md` - Full roadmap
- `docs/initiatives/active/workflow-optimization-phase-2/artifacts/intelligent-compression-v2.md` - 5-layer methodology
- `docs/initiatives/active/workflow-optimization-phase-2/artifacts/idempotency-framework-integration.md` - Framework design
- `docs/initiatives/active/workflow-optimization-phase-2/initiative.md` - Initiative with Session 4 update

---

## This Session Objectives

**Goal:** Complete Phase 1 foundation by integrating intelligent methodology into optimization workflows and validating with POC.

**Tasks (from NEXT_SESSION_IMPLEMENTATION_GUIDE.md):**

1. Update `.windsurf/workflows/improve-prompt.md` with intelligent methodology (45-60 min)
2. Update `.windsurf/workflows/improve-workflow.md` with intelligent methodology (30-45 min)
3. Execute POC on 1 workflow with semantic validation (30-45 min)
4. Validate semantic preservation metrics (15 min)
5. Commit all changes (15 min)

**Success Criteria:**
- [ ] `improve-prompt.md` updated with 7 sections (A-G from implementation guide)
- [ ] `improve-workflow.md` updated with 5 sections (A-E from implementation guide)
- [ ] POC executed on `bump-version.md` or similar workflow
- [ ] Semantic preservation score ≥ 92%
- [ ] Idempotency test passed (hash match OR similarity ≥98% + drift ≤10)
- [ ] All changes committed with detailed message
- [ ] Phase 1 foundation validated for Phase 2 execution

---

## Critical Implementation Details

### 5-Layer Intelligent Methodology

**Layer 1: Semantic Analysis**
- Extract decision logic, entities, task structures, relationships
- Identify preservation priorities: Critical (100%) → High (>90%) → Medium (>70%) → Low (<50%)

**Layer 2: Coarse-Grained Compression**
- Section-level budget controller
- Different targets per section type (decision matrices 90%, examples 60%)

**Layer 3: Fine-Grained Compression**
- Token-level contextual anchors
- Preserve: decision thresholds, function signatures, technical terms
- Compress: filler phrases, verbose instructions, redundant modifiers

**Layer 4: Semantic Validation**
- Entity preservation: ≥90%
- Decision logic intact: ≥98%
- Task syntax valid: =100%
- Relationship preserved: ≥85%
- Anchor retention: ≥90%
- **Overall score requirement: ≥92%**

**Layer 5: Idempotency Verification**
- Hash-based exact match OR
- Semantic similarity ≥98% AND token drift ≤10

### Compression Decision Matrix

**Apply variable strategies based on quality + token count:**

| Quality | Tokens | Strategy | Max Reduction | Validation |
|---------|--------|----------|---------------|------------|
| <6/10 | Any | Aggressive | 60% | Standard |
| 6-7/10 | <2000 | Balanced | 30% | Standard |
| 6-7/10 | >2000 | Moderate | 40% | Enhanced |
| 7-8/10 | <2000 | Light | 15% | Strict |
| 7-8/10 | >2000 | Selective | 25% | Strict |
| >8/10 | Any | Minimal | 10% | Very strict |

---

## Implementation Instructions

### CRITICAL: Use MCP Tools for Windsurf Files

**ALWAYS use MCP tools for `.windsurf/` files:**

```python
# ✅ CORRECT
mcp0_read_text_file(path="/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md")
mcp0_edit_file(path="/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md", edits=[...])

# ❌ WRONG (will fail)
read_file("/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md")
edit(file_path="/home/gxx/projects/mcp-web/.windsurf/workflows/improve-prompt.md", ...)
```

### Step-by-Step Process

1. **Read NEXT_SESSION_IMPLEMENTATION_GUIDE.md fully** - Contains exact sections to add
2. **Update improve-prompt.md** - 7 sections (A-G): idempotency pre-check, semantic analysis, compression matrix, semantic validation, idempotency testing, results template, frontmatter
3. **Update improve-workflow.md** - 5 sections (A-E): compression matrix, idempotency pre-check, semantic preservation layer, idempotency testing, frontmatter
4. **Execute POC** - Apply methodology to 1 workflow (e.g., `bump-version.md`)
5. **Measure metrics** - Calculate all 5 semantic preservation scores + idempotency
6. **Document results** - Create `artifacts/poc-validation-results.md`
7. **Commit changes** - Detailed commit message with metrics

---

## Expected Outcomes

**After this session:**
- Phase 1 foundation complete (100%)
- Workflows updated with intelligent methodology
- POC validated with ≥92% semantic preservation
- Idempotency verified
- Ready for Phase 2 (restore + re-optimize 17 workflows)

**Metrics to measure:**
- Entity preservation: ≥90%
- Decision logic intact: ≥98%
- Task syntax valid: =100%
- Relationship preserved: ≥85%
- Anchor retention: ≥90%
- Overall semantic score: ≥92%
- Idempotency: Hash match OR (similarity ≥98% + drift ≤10)

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Semantic validation scores low | Reduce compression aggressiveness, keep more examples |
| Idempotency test fails | Check for non-deterministic elements (temp, seed, timestamps) |
| Time overrun | Focus on workflow updates first, POC can be next session if needed |
| MCP tools fail | Use absolute paths, correct tool names |

---

## Anti-Patterns to Avoid

❌ **Don't:** Apply uniform percentages (e.g., "reduce all by 30%")
❌ **Don't:** Replace concrete examples with generic placeholders
❌ **Don't:** Collapse detailed steps into parent steps
❌ **Don't:** Use regular `edit` tool for `.windsurf/` files (use MCP tools)

✅ **Do:** Apply variable reduction based on content quality
✅ **Do:** Preserve concrete, specific examples
✅ **Do:** Maintain appropriate task granularity
✅ **Do:** Use context-aware optimization strategies

---

## Workflow: @[/work] Command

**Start session with:** `/work`

This will:
1. Detect project context
2. Load initiative files efficiently
3. Route to appropriate workflow (should detect continuation)
4. Execute implementation tasks
5. Detect completion and run session end protocol
6. Generate meta-analysis

**Expected routing:** `/work` → `/detect-context` → `/implement` → `/validate` → `/commit` → `/meta-analysis`

---

## Session End Checklist

- [ ] `improve-prompt.md` updated (7 sections)
- [ ] `improve-workflow.md` updated (5 sections)
- [ ] POC executed with results documented
- [ ] Semantic preservation ≥92% verified
- [ ] Idempotency test passed
- [ ] `artifacts/poc-validation-results.md` created
- [ ] All changes committed
- [ ] Initiative.md updated with Session 5 progress
- [ ] Meta-analysis generated
- [ ] Repository in clean state (no uncommitted changes)

---

**Start Session Command:**

```
@[/work] Continue workflow optimization Phase 1 completion. Implement intelligent methodology into improve-prompt.md and improve-workflow.md as detailed in NEXT_SESSION_IMPLEMENTATION_GUIDE.md. Execute POC with semantic validation. Reference COMPREHENSIVE_PLAN_V3.md for full context.
```

---

**Estimated Duration:** 2-3 hours
**Priority:** High
**Phase:** 1 (Foundation - Final step)
**Next Phase:** 2 (Restore + re-optimize 17 workflows)
