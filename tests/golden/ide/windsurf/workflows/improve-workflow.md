---
description: Workflow-specific optimization with intelligent semantic preservation
title: Improve Workflow Workflow
type: workflow
category: Optimization
complexity: moderate
dependencies: ['improve-prompt']
status: active
created: 2025-10-22
updated: 2025-10-22
---

**Purpose:** Workflow-specific optimization with syntax preservation and decomposition detection.

**Called By:** `/improve-prompt` when target is a Windsurf workflow

**Scope:** Conciseness optimization, workflow syntax validation, decomposition detection

## Stage 0: Workflow Entry

🔄 **Entering /improve-workflow:** Workflow optimization sub-routine

## Stage 1: Parse Workflow Structure

### 1.1 Extract Components

**Parse:**

- Frontmatter (YAML metadata)
- Stage headings (`## Stage N:`)
- `update_plan` calls with task structure
- Tables, code blocks, examples
- Cross-references and dependencies

### 1.2 Identify Preservation Zones

**Critical (100% preservation):**

- All `update_plan({...})` syntax
- Frontmatter keys
- Stage numbering sequence
- Workflow entry/exit markers

**High (>90%):**

- Task attribution (`/workflow-name - Description`)
- Decision thresholds and criteria
- Validation checkpoints
- Cross-references

**Medium (>70%):**

- Examples and demonstrations
- Process descriptions
- Background explanations

### 1.3 Calculate Conciseness Weight

**See:** [improve-prompt.md Stage 3.5.2](./improve-prompt.md) for weight calculation logic

## Stage 2: Apply Conciseness Techniques

### 2.1 Technique Selection

**Based on conciseness weight:**

| Weight | Priority | Techniques |
|--------|----------|------------|
| 1.0x | Low | Minor cleanup only |
| 1.5x | Moderate | 1, 2, 3 |
| 2.0x | High | 1-4 |
| 2.5x | Critical | All + decomposition |

**Techniques:**

1. Information Distillation (eliminate verbose phrases)
2. Structured Bullets (paragraphs → bullet lists)
3. Keyword Extraction (compact command descriptions)
4. Example Consolidation (multiple examples → tables)
5. Reference Externalization (duplicate content → refs)

### 2.2 Example: Information Distillation (Weight × 1.5)

| Before | After | Savings |
|--------|-------|---------|
| "The workflow begins by analyzing..." | "Analyzes project state:" | ~60% |
| "Execute the following command in your terminal..." | "Run: `command`" | ~70% |
| "Please provide detailed analysis of..." | "Analyze:" | ~75% |

**Target:** Remove filler words while preserving meaning.

### 2.3 Example: Structured Bullets (Weight × 1.6)

**Before (paragraph):**

```markdown
The workflow begins by analyzing the project state. It looks at
various indicators including active initiatives, git status, test
results, and session history. Based on this analysis, it makes a
routing decision.
```

**After (bullets):**

```markdown
Analyzes project state:
- Active initiatives
- Git status
- Test results
- Session history
→ Routes based on analysis
```

**Savings:** 20-40%

### 2.4 Example Consolidation (Weight × 2.0)

**Strategy:**

- Keep 2-3 best examples
- Remove duplicate patterns
- Use tables for multiple examples
- Inline short examples

| Before | After | Savings |
|--------|-------|---------|
| 8 verbose examples (200 tokens) | 3-column table (80 tokens) | 60% |

### 2.5 Reference Externalization (Weight × 1.3)

| Before | After | Savings |
|--------|-------|---------|
| [3 paragraphs on task management] | See: [12_task_orchestration.md](../rules/12_task_orchestration.md) | 50-80% |

### 2.6 Quality Gates

**After applying techniques, verify:**

- ✅ Intent preserved
- ✅ Task management intact (all `update_plan` calls work)
- ✅ Examples sufficient (2-3 remain)
- ✅ Stage flow clear
- ✅ References valid

**Target reduction:**

- Low (1.0x): 10-15%
- Moderate (1.5x): 20-30%
- High (2.0x): 30-40%
- Critical (2.5x): 40-50% + decomposition

## Stage 3: Workflow-Specific Validation

### 3.1 Syntax Validation

```bash
# Frontmatter valid
python scripts/validate_workflows.py

# Task syntax valid
grep "step:.*status:" improved.md | validate format
```

### 3.2 Semantic Validation

**Check:**

- Stage numbering sequential
- Task attributions correct
- Dependencies accurate
- Complexity score reasonable
- Token count matches estimate

### 3.3 Integration Validation

**Test:**

- Can be called by other workflows
- Dependency calls work
- Cross-references resolve
- Examples run correctly

### 3.4 Pre-Commit Validation (RESTORATION_PROTOCOL)

**MANDATORY before ANY commit:**

#### 3.4.1 Quantitative Validation

```bash
original_words=$(wc -w < /tmp/TARGET-baseline.md)
new_words=$(wc -w < .windsurf/workflows/TARGET.md)
reduction_pct=$(echo "scale=2; 100 * ($original_words - $new_words) / $original_words" | bc)
```

**FAIL if:** reduction_pct > 15%

#### 3.4.2 Structural Validation

```bash
grep "^##" /tmp/TARGET-baseline.md | sort > /tmp/baseline-structure.txt
grep "^##" .windsurf/workflows/TARGET.md | sort > /tmp/optimized-structure.txt
diff /tmp/baseline-structure.txt /tmp/optimized-structure.txt
```

**FAIL if:** Any Stage heading missing

#### 3.4.3 Critical Element Validation

```bash
baseline_update_plans=$(grep -c "update_plan" /tmp/TARGET-baseline.md)
optimized_update_plans=$(grep -c "update_plan" .windsurf/workflows/TARGET.md)

baseline_critical=$(grep -c "CRITICAL\|MANDATORY" /tmp/TARGET-baseline.md)
optimized_critical=$(grep -c "CRITICAL\|MANDATORY" .windsurf/workflows/TARGET.md)
```

**FAIL if:** update_plans OR critical markers reduced

#### 3.4.4 Restoration Decision

**If ANY validation fails:**

```bash
cp /tmp/TARGET-baseline.md .windsurf/workflows/TARGET.md
echo "❌ VALIDATION FAILED: Restored from baseline"
```

**See:** [RESTORATION_PROTOCOL.md](../../docs/initiatives/completed/workflow-optimization-phase-2/artifacts/RESTORATION_PROTOCOL.md)

### 3.5 Idempotency Testing

**Test multiple dimensions:**

```python
# Test 1: Re-optimize produces no changes
exact_match = (compressed == re_optimized)

# Test 2: update_plan calls unchanged
plans_match = (original_plans == re_optimized_plans)

# Test 3: Frontmatter integrity
frontmatter_intact = verify_frontmatter(compressed, re_optimized)

# Test 4: Workflow markers preserved
markers_intact = verify_workflow_markers(compressed, re_optimized)

# PASS: ALL tests pass
assert exact_match AND plans_match AND frontmatter_intact AND markers_intact
```

## Stage 4: Decomposition Detection

**If tokens > 6000 OR complexity > 75:**

### 4.1 Identify Opportunities

- **Distinct responsibilities** (multiple purposes)
- **Complex stages** (>500 tokens each)
- **Reusable logic** (patterns used >2 times)
- **Optional features** (separable)

### 4.2 Propose Strategy

```markdown
## 🔄 DECOMPOSITION RECOMMENDED

**Current:** [N] tokens, complexity [N]
**Target:** <6000 tokens, <75 complexity

**Proposed:**

- Extract: [What to separate]
- New files: `part1.md` ([N] tokens), `part2.md` ([N] tokens)
- Benefits: [Token/complexity reduction, maintainability]
- Implementation: [Steps]

**Recommendation:** [Chosen option] because [reason]
```

## Stage 5: Output Format

### 5.1 Standard Output

```markdown
# 🎯 Workflow Optimization Results

## Summary
- **Original:** [N] tokens, complexity [N]
- **Improved:** [N] tokens, complexity [N]
- **Reduction:** -[N] tokens (-[X]%)
- **Weight:** [N]x ([priority])

## Changes
1. Information Distillation: -[N] tokens
2. Structured Bullets: -[N] tokens
3. Keyword Extraction: -[N] tokens
4. Example Consolidation: -[N] tokens
5. Reference Externalization: -[N] tokens

## Validation
✅ Intent preserved
✅ Task management intact
✅ Syntax valid
✅ Links functional

## Improved Workflow
[Full content]
```

### 5.2 With Decomposition

Include everything from 5.1 PLUS decomposition proposal from Stage 4.2.

## Integration

### Called By

`/improve-prompt` when detecting Windsurf workflow (`.windsurf/workflows/*.md` with `auto_execution_mode` frontmatter)

### Returns To

`/improve-prompt` with response:

```json
{
  "improved_content": "[full workflow]",
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

## Anti-Patterns

**❌ Don't:**

- Over-compress critical instructions
- Remove all examples (need 2-3)
- Break `update_plan` syntax
- Ignore decomposition signals (>6000 tokens)

**✅ Do:**

- Preserve task management structure
- Keep concrete examples
- Validate before committing
- Recommend decomposition when needed

## Success Metrics

| Metric | Target |
|--------|--------|
| Token reduction | >20% |
| Quality preservation | >90% |
| Syntax correctness | 100% |
| Decomposition detection | >95% (for >6000 tokens) |

## References

- [improve-prompt.md](./improve-prompt.md) - Parent workflow
- [detect-context.md](./detect-context.md) - Example well-structured workflow
- [12_task_orchestration.md](../rules/12_task_orchestration.md) - Task system
- [RESTORATION_PROTOCOL.md](../../docs/initiatives/completed/workflow-optimization-phase-2/artifacts/RESTORATION_PROTOCOL.md)

**External:**

- [Token Optimization](https://10clouds.com/blog/a-i/mastering-ai-token-optimization-proven-strategies-to-cut-ai-cost/) (2025)
- [Prompt Compression](https://medium.com/@sahin.samia/prompt-compression-in-large-language-models-llms-making-every-token-count-078a2d1c7e03) (2025)
- [Workflow Patterns](https://skywork.ai/blog/agentic-ai-examples-workflow-patterns-2025/) (2025)

**Version:** 2.1-self-optimized
**Last Updated:** 2025-10-21
