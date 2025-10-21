---
created: "2025-10-21"
updated: "2025-10-21"
description: Optimize Windsurf workflows with intelligent semantic preservation and idempotency
auto_execution_mode: 2
category: Optimization
complexity: 75
tokens: 2000
dependencies:
  - improve-prompt
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Improve Workflow Sub-Workflow

**Purpose:** Specialized workflow for optimizing Windsurf workflows with deep understanding of workflow structure, task management, and decomposition needs.

**Invocation:** Called by `/improve-prompt` when `prompt_type=workflow` detected

**Philosophy:** Workflows have unique constraints (task management, frontmatter, stages) that require specialized optimization beyond general prompts.

**Parent Workflow:** `/improve-prompt`

---

## When to Use

This sub-workflow is **automatically invoked** by `/improve-prompt` when:

- Input type is detected as Windsurf workflow (`.windsurf/workflows/*.md`)
- File contains workflow frontmatter with `auto_execution_mode`
- Content includes `update_plan` calls or stage structure

**Do NOT call directly** - use `/improve-prompt` on workflow files.

---

## Stage 0: Workflow Context Analysis

🔄 **Entering /improve-workflow:** Specialized workflow optimization

### 0.1 Extract Workflow Metadata

**From frontmatter:**

```yaml
complexity: [N]      # Workflow complexity score
tokens: [N]          # Current token count
dependencies: [...]  # Other workflows it calls
```

**From content:**

- Stage count
- `update_plan` occurrences
- Task management syntax
- Example count
- Cross-references

### 0.2 Apply Compression Decision Matrix

**Use same matrix as `/improve-prompt` Stage 4.0:**

Determine strategy based on workflow quality + token count.

**See:** `improve-prompt.md` Stage 4.0 for complete matrix.

**Workflow-specific adjustments:**

- Complexity >75: Reduce max reduction by 10%
- Stage count >10: Light polish only (max 15% reduction)
- Calls >5 workflows: Preserve all cross-references

### 0.3 Idempotency Pre-Check

**Check if workflow already optimized:**

1. **Method 1:** Cache lookup by hash
2. **Method 2:** Frontmatter `version` field contains "intelligent" or "semantic"
3. **Method 3:** Token count vs target delta < 50 tokens

**If already optimized:**

- Return unchanged with note: "Already optimized (cached/version/stable)"
- Skip all optimization stages

---

## Stage 1: Workflow-Specific Analysis

### 1.1 Workflow Quality Dimensions

**Standard dimensions PLUS workflow-specific:**

| Dimension | Weight | Focus |
|-----------|--------|-------|
| Task management clarity | 1.5x | `update_plan` structure |
| Stage organization | 1.5x | Logical flow |
| Frontmatter accuracy | 1.0x | Metadata correctness |
| Cross-reference integrity | 1.0x | Links to other workflows/rules |
| Example efficiency | **Conciseness weight** | Examples vs explanations |
| Instruction density | **Conciseness weight** | Information per token |

### 1.2 Decomposition Detection

**Trigger decomposition recommendation if ANY:**

- ✅ Token count > 6000 (>3000 words)
- ✅ Complexity score > 75
- ✅ Stage count > 10
- ✅ Multiple distinct responsibilities
- ✅ Workflow calls >5 other workflows

**Decomposition patterns:**

1. **Planner-Executor Split**: Separate planning from execution
2. **Stage Extraction**: Move complex stages to sub-workflows
3. **Responsibility Separation**: Split multi-purpose workflows
4. **Shared Component Extraction**: Common logic → reusable sub-workflow

**Example:**

- `improve-prompt.md` (8500 tokens, 9 stages) → Extract model-specific stages
- `consolidate-summaries.md` (3049 words) → Extract consolidation logic

---

## Stage 2: Apply Windsurf-Aware Conciseness

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

### 2.1 PRESERVE Critical Elements

**NEVER modify these:**

- `update_plan` syntax (exact structure)
- Frontmatter keys (complexity, tokens, dependencies, etc.)
- Stage numbering system
- Task attribution patterns ("N. /workflow-name - description")
- Workflow entry/exit announcements

### 2.2 Conciseness Techniques (Priority Order)

#### Technique 1: Information Distillation (Weight × 2.0)

**Target:** Verbose explanations, redundant phrases

**Examples:**

```markdown
❌ Before: "Please provide a comprehensive and detailed explanation..."
✅ After: "Explain..."

❌ Before: "It is important to note that you should..."
✅ After: "Must..."

❌ Before: "In order to accomplish this task, you will need to..."
✅ After: "To accomplish: ..."
```

**Savings:** 30-50% on instructional text

#### Technique 2: Structured Bullet Points (Weight × 1.5)

**Target:** Long paragraphs, narrative text

**Transform:**

```markdown
❌ Before:
The workflow begins by analyzing the project state. It looks at
various indicators including active initiatives, git status, test
results, and session history. Based on this analysis, it makes a
routing decision.

✅ After:
Analyzes project state:
- Active initiatives
- Git status
- Test results
- Session history
→ Routes based on analysis
```

**Savings:** 20-40% on process descriptions

#### Technique 3: Keyword Extraction (Weight × 1.8)

**Target:** Detailed descriptions, examples

**Transform:**

```markdown
❌ Before: "Analyze the provided documentation to identify..."
✅ After: "Identify from docs..."

❌ Before: "Execute the following command in your terminal..."
✅ After: "Run: `command`"
```

**Savings:** 15-30% on command/action descriptions

#### Technique 4: Example Consolidation (Weight × 2.0)

**Target:** Redundant examples, verbose demonstrations

**Strategy:**

- Keep 2-3 best examples
- Remove duplicate patterns
- Use tables for multiple examples
- Inline short examples

**Before (8 examples, 200 tokens):**

```markdown
Example 1: ...detailed...
Example 2: ...detailed...
...
Example 8: ...detailed...
```

**After (3 examples, 80 tokens):**

```markdown
| Pattern | Example |
|---------|---------|
| Simple | `short` |
| Moderate | `medium` |
| Complex | `longer` |
```

**Savings:** 40-60% on examples section

#### Technique 5: Reference Externalization (Weight × 1.3)

**Target:** Inline documentation, repeated concepts

**Strategy:**

- Move detailed explanations to rules/docs
- Reference external sources
- Use "See: [link]" pattern

**Transform:**

```markdown
❌ Before: [3 paragraphs explaining task management]

✅ After: See: [12_task_orchestration.md](../rules/12_task_orchestration.md)
```

**Savings:** 50-80% on repeated concepts

### 2.3 Conciseness Quality Gates

**After applying techniques, verify:**

- ✅ **Intent preserved**: Core workflow logic unchanged
- ✅ **Task management intact**: All `update_plan` calls work
- ✅ **Examples sufficient**: 2-3 clear examples remain
- ✅ **Navigation clear**: Stage flow understandable
- ✅ **References valid**: All links functional

**Target reduction:**

- Low priority (weight 1.0x): 10-15% token reduction
- Moderate (weight 1.5x): 20-30% token reduction
- High (weight 2.0x): 30-40% token reduction
- Critical (weight 2.5x): 40-50% + decomposition recommendation

---

## Stage 3: Workflow-Specific Validation

### 3.1 Syntax Validation

**Verify:**

```bash
# Frontmatter valid
python scripts/validate_workflows.py

# Links valid
# Check all markdown links are valid

# Task syntax valid
grep "step:.*status:" improved.md | validate format
```

### 3.2 Semantic Validation

**Check:**

- Stage numbering sequential
- Task attributions correct (workflow names)
- Dependencies list accurate
- Complexity score reasonable
- Token count matches estimate

### 3.3 Integration Validation

**Test:**

- Can be called by other workflows
- Calls to dependencies work
- Cross-references resolve
- Examples run correctly

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

---

## Stage 4: Generate Decomposition Recommendation

**If token count > 6000 OR complexity > 75:**

### 4.1 Analyze Decomposition Opportunities

**Identify:**

1. **Distinct responsibilities**: Multiple purposes
2. **Complex stages**: Stages > 500 tokens each
3. **Reusable logic**: Patterns used >2 times
4. **Optional features**: Can be separated

### 4.2 Propose Decomposition Strategy

**Template:**

```markdown
## 🔄 DECOMPOSITION RECOMMENDED

**Current State:**
- Tokens: [N] (Target: <6000)
- Complexity: [N] (Target: <75)
- Stages: [N]

**Proposed Decomposition:**

### Option 1: [Strategy Name]
**Extract:** [What to separate]
**New Files:**
- `workflow-name-part1.md` ([N] tokens)
- `workflow-name-part2.md` ([N] tokens)

**Benefits:**
- Token reduction: [N]% → [new total]
- Complexity reduction: [old] → [new]
- Maintainability: [improvement]

**Implementation:**
1. Create sub-workflow for [X]
2. Extract stages [N-M]
3. Update parent workflow to call sub-workflow
4. Update dependencies

### Option 2: [Alternative Strategy]
[Similar structure]

**Recommendation:** Option [N] because [reason]
```

---

## Stage 5: Output Format

### 5.1 Standard Output (No Decomposition)

```markdown
# 🎯 Workflow Optimization Results

## Summary
- **Original:** [N] tokens, complexity [N]
- **Improved:** [N] tokens, complexity [N]
- **Reduction:** -[N] tokens (-[X]%)
- **Conciseness Weight:** [N]x (priority: [low/moderate/high])

## Changes Applied
1. **Information Distillation**: -[N] tokens
2. **Structured Bullets**: -[N] tokens
3. **Keyword Extraction**: -[N] tokens
4. **Example Consolidation**: -[N] tokens
5. **Reference Externalization**: -[N] tokens

## Validation
✅ Intent preserved
✅ Task management intact
✅ Syntax valid
✅ Links functional

## Improved Workflow
[Full improved workflow]
```

### 5.2 With Decomposition Recommendation

**Include everything from 5.1 PLUS:**

```markdown
## 🔄 DECOMPOSITION RECOMMENDED

[Output from Stage 4.2]

**Next Steps:**
1. Review decomposition proposal
2. If approved, create sub-workflows
3. Re-run /improve-workflow on each part
4. Validate integration
```

---

## Integration with Parent Workflow

### Called By: `/improve-prompt`

**Detection logic in parent:**

```python
if file_path.endswith('.md') and '.windsurf/workflows/' in file_path:
    # Check frontmatter
    if 'auto_execution_mode' in frontmatter:
        # This is a workflow
        call_subworkflow('improve-workflow')
```

### Returns To: `/improve-prompt`

**Response format:**

```json
{
  "improved_content": "[full improved workflow]",
  "metrics": {
    "tokens_before": 8500,
    "tokens_after": 5200,
    "reduction_percent": 38.8,
    "conciseness_weight": 2.0
  },
  "decomposition": {
    "recommended": true,
    "strategy": "Stage extraction",
    "details": "[proposal]"
  },
  "validation": {
    "syntax_valid": true,
    "links_valid": true,
    "task_management_intact": true
  }
}
```

---

## Anti-Patterns

### ❌ Don't: Over-Compress Critical Instructions

**Bad:**

```markdown
Do X.
```

**Good:**

```markdown
Execute X:
- Step 1
- Step 2
Result: [expected]
```

### ❌ Don't: Remove All Examples

Need 2-3 concrete examples for clarity.

### ❌ Don't: Break Task Management Syntax

`update_plan` structure is sacred - never modify.

### ❌ Don't: Ignore Decomposition Signals

If >6000 tokens after optimization → MUST recommend decomposition.

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Token reduction | >20% | Before/after count |
| Quality preservation | >90% | Validation checks |
| Syntax correctness | 100% | Script validation |
| Decomposition detection | >95% | For workflows >6000 tokens |

---

## References

### Parent Workflow

- [improve-prompt.md](./improve-prompt.md) - Main optimization workflow

### Related Workflows

- [detect-context.md](./detect-context.md) - Example of well-structured workflow
- [work.md](./work.md) - Orchestration pattern

### Rules

- [12_task_orchestration.md](../rules/12_task_orchestration.md) - Task management system
- [05_windsurf_structure.md](../rules/05_windsurf_structure.md) - Workflow structure rules

### External Research

- [10clouds Token Optimization](https://10clouds.com/blog/a-i/mastering-ai-token-optimization-proven-strategies-to-cut-ai-cost/) (2025)
- [Prompt Compression Techniques](https://medium.com/@sahin.samia/prompt-compression-in-large-language-models-llms-making-every-token-count-078a2d1c7e03) (2025)
- [Workflow Decomposition Patterns](https://skywork.ai/blog/agentic-ai-examples-workflow-patterns-2025/) (2025)

---

**Version:** 1.0.0
**Last Updated:** 2025-10-21
