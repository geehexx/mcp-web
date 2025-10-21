---
created: "2025-10-21"
updated: "2025-10-21"
description: LLM-agnostic prompt optimization with intelligent semantic preservation and idempotency
auto_execution_mode: 2
category: Optimization
complexity: 70
tokens: 3500
dependencies:
  - improve-workflow
status: active
version: "3.1-self-optimized"
---

# Improve Prompt Workflow

**Purpose:** Optimize prompts for any LLM using cross-model best practices with quantitative validation.

**Invocation:** `/improve-prompt [target_model=auto]` + prompt text or file reference

**Philosophy:** Universal principles (clarity, structure, reasoning) + optional model-specific enhancements.

**Supported:** Claude 3.5+, GPT-4+, Gemini 1.5+, instruction-following LLMs

---

## Optimization Methodology (2025)

### Core Principles

| Principle | Application | Research Basis |
|-----------|-------------|----------------|
| Quality ≠ Verbosity | Tables/bullets > prose | Structured prompts improve accuracy 15-30% (Anthropic 2025) |
| Strategic Context | Add "why" for key decisions only | Targeted rationale > comprehensive coverage |
| Compression Threshold | Don't exceed 80% reduction | Balance conciseness with context |
| One Purpose Per Section | Each section answers single question | Prevents LLM confusion |
| Contextual Anchors | Retain decision thresholds, criteria | Essential keywords guide LLM focus |

### Token Efficiency Techniques

| Technique | Target | Example | Savings | Quality |
|-----------|--------|---------|---------|---------|
| Information Distillation | Verbose phrases | "Please provide..." → "Analyze:" | 30-50% | Neutral/+ |
| Structured Bullets | Long paragraphs | 200w paragraph → 5 bullets | 20-40% | + |
| Table Consolidation | Verbose lists | 8 descriptions → compact table | 40-60% | + |
| Example Consolidation | Redundant examples | 8 partial → 1 complete + 3 compact | 40-60% | + |
| Reference Externalization | Inline docs | [5 paragraphs] → "See: [link]" | 50-80% | Context-dep |

**Evidence:** Explicit reasoning reduces hallucination 20-40% (OpenAI 2025), Format specs improve adherence 50-100% (Gemini)

### Decision Matrix

| Quality | Tokens | Strategy | Rationale |
|---------|--------|----------|-----------|
| <6/10 | Any | Aggressive | Low baseline allows experimentation |
| 6-7/10 | <3k | Balanced | Room for improvement |
| 6-7/10 | >3k | Prioritize conciseness | High verbosity, medium quality |
| 7-8/10 | <2k | Maintain, polish | Already efficient |
| 7-8/10 | >2k | Selective | Focus high-impact areas |
| >8/10 | Any | **Minimal** | Risk damaging high baseline |

**Self-Application:** Only self-optimize if baseline <8/10 OR tokens >4000.

---

## When to Use

**Use:** Workflows, rules, ad-hoc prompts, system prompts, inconsistent results, structure improvements

**Avoid:** Changing roles/personas, security logic, project rules (without approval), already-optimized prompts

---

## Stage 0: Workflow Entry

🔄 **Entering /improve-prompt:** Prompt optimization with quantitative analysis

---

## Stage 1: Pre-Optimization Validation (Workflows Only)

**If optimizing Windsurf workflow (`.windsurf/workflows/*.md`):**

### 1.1 Create Baseline Snapshot

```bash
git show HEAD:.windsurf/workflows/TARGET.md > /tmp/TARGET-baseline.md
wc -w /tmp/TARGET-baseline.md
```

### 1.2 Check Restored Workflows

```bash
git log --oneline --all --grep="restore.*workflows" -- .windsurf/workflows/TARGET.md
```

**If restored (detect-context, implement, validate, research):** Return unchanged, exit workflow.

**See:** [RESTORATION_PROTOCOL.md](../../docs/initiatives/completed/workflow-optimization-phase-2/artifacts/RESTORATION_PROTOCOL.md)

---

## Stage 2: Create Task Plan

```typescript
update_plan({
  explanation: "🔄 Starting /improve-prompt workflow",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input", status: "in_progress" },
    { step: "2. /improve-prompt - Detect model and context", status: "pending" },
    { step: "3. /improve-prompt - Analyze quality", status: "pending" },
    { step: "4. /improve-prompt - Apply optimizations", status: "pending" },
    { step: "5. /improve-prompt - Validate and present", status: "pending" }
  ]
})
```

---

## Stage 3: Input Capture

### 3.1 Parse Input

**Formats:** Inline text, file reference (`@workflow:name`), code block

**Extract:** Original text, context type (workflow/rule/ad-hoc/system), structure, examples, variables

---

## Stage 4: Model Detection & Configuration

### 4.1 Target Model

| Model | Structure | Strengths | Optimization Focus |
|-------|-----------|-----------|-------------------|
| Claude 3.5+ | XML tags | Extended thinking, reasoning | Chain-of-thought, explicit structure |
| GPT 4+ | Markdown | Code generation, structured output | Clear format, step-by-step |
| Gemini 1.5+ | Hierarchical | Long context, multimodal | System instructions, query placement |
| Generic/Auto | GOLDEN | Instruction following | Universal patterns only |

### 4.2 Conciseness Priority

| Tokens | Words | Weight | Priority | Strategy |
|--------|-------|--------|----------|----------|
| <2k | <1k | 1.0x | Low | Standard |
| 2k-4k | 1k-2k | 1.5x | Moderate | Conciseness focus |
| 4k-6k | 2k-3k | 2.0x | High | Aggressive |
| >6k | >3k | 2.5x | **CRITICAL** | **Decomposition candidate** |

### 4.3 Special Constraints

- **Windsurf workflows:** Preserve `update_plan`, frontmatter, stages → Route to `/improve-workflow`
- **Project rules:** Preserve triggers, anti-patterns, cross-refs
- **GPT-5-Codex:** Minimal prompting, no preambles

### 4.4 Idempotency Pre-Check

1. Calculate hash (content + config + methodology v3.0)
2. Check cache: `.windsurf/.optimization-cache.json`
3. If hit: Return cached result
4. If miss: Proceed

**Hash:** Content SHA-256 + methodology v3.0 + techniques + thresholds + model + temp=0.0 + seed=42

### 4.5 Sub-Workflow Routing

**If Windsurf workflow:** Route to `/improve-workflow`

**See:** [improve-workflow.md](./improve-workflow.md)

---

## Stage 5: Analyze Current Prompt

### 5.1 Semantic Analysis (Layer 1)

```python
semantic_profile = {
    "decision_logic": extract_decision_points(content),
    "key_entities": extract_entities_ner(content),
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

### 5.2 Quality Assessment

**Dimensions (0-10):** Clear objective, specific instructions, context, constraints, output format, examples, reasoning guidance, structure

**Issues:** Ambiguous objective, missing context, no output format, unclear constraints, redundant sections

---

## Stage 6: Apply Universal Optimizations

### 6.1 Structural Improvements

**Structure patterns:**

- Clear objective statement
- Numbered/bulleted instructions
- Explicit constraints
- Format specification
- Concrete examples (2-3)
- Reasoning guidance

### 6.2 Clarity Enhancements

**Apply:**

- Active voice
- Imperative mood for instructions
- Specific terminology (not generic)
- Explicit relationships between sections
- Remove ambiguity

### 6.3 Context Optimization

**Balance:**

- Essential context (keep)
- Redundant context (remove)
- Implicit knowledge (make explicit for LLM)
- Token budget vs comprehension

---

## Stage 7: Model-Specific Enhancements (Optional)

**If target model specified:**

| Model | Enhancements |
|-------|--------------|
| Claude | Add XML tags, <thinking> blocks, explicit reasoning |
| GPT | Structured markdown, clear sections, tool schemas |
| Gemini | System instructions, hierarchical structure, examples first |

**If `target_model=auto`:** Skip model-specific, use universal only.

---

## Stage 8: Validation & Quality Gates

### 8.1 Intent Preservation

**Check:**

- Core objective unchanged
- All constraints preserved
- Output format maintained
- Critical examples retained

### 8.2 Quantitative Metrics

**Measure:**

- Token count (before/after)
- Quality score (0-10)
- Efficiency ratio
- Semantic preservation (>92%)

### 8.3 Idempotency Test

```python
# Re-optimize with same config
re_optimized = optimize(improved, same_config)
assert improved == re_optimized  # Must be identical
```

---

## Stage 9: Output & Presentation

### 9.1 Results Format

```markdown
# 🎯 Prompt Optimization Results

## Summary
- **Original:** [N] tokens, quality [N]/10
- **Improved:** [N] tokens, quality [N]/10
- **Reduction:** -[N] tokens (-[X]%)
- **Semantic Preservation:** [X]%

## Changes Applied
[List of techniques used]

## Validation
✅ Intent preserved
✅ Quality maintained/improved
✅ Idempotency verified

## Improved Prompt
[Full improved content]
```

### 9.2 Recommendations

**If applicable:**

- Decomposition recommendation (>6k tokens)
- Further optimization opportunities
- Model-specific suggestions

---

## Integration

### Calls

- `/improve-workflow` (for Windsurf workflows)

### Returns

JSON with improved content, metrics, validation status, recommendations

---

## Anti-Patterns

**❌ Don't:**

- Change core objective/role
- Remove all examples (need 2-3)
- Exceed 80% reduction without validation
- Ignore decomposition signals (>6k tokens)
- Modify security-critical prompts without review

**✅ Do:**

- Preserve intent while improving clarity
- Measure before/after quantitatively
- Test idempotency
- Recommend decomposition when needed
- Document changes applied

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Token reduction | >15% |
| Quality preservation | >92% |
| Idempotency | 100% |
| Validation pass rate | >95% |

---

## References

### Workflows

- [improve-workflow.md](./improve-workflow.md) - Workflow-specific optimization
- [work.md](./work.md) - Orchestration example

### Rules

- [12_task_orchestration.md](../rules/12_task_orchestration.md) - Task system
- [00_core_directives.md](../rules/00_core_directives.md) - Core principles

### External

- [Token Optimization](https://10clouds.com/blog/a-i/mastering-ai-token-optimization-proven-strategies-to-cut-ai-cost/) (2025)
- [Prompt Compression](https://medium.com/@sahin.samia/prompt-compression-in-large-language-models-llms-making-every-token-count-078a2d1c7e03) (2025)
- [LLM Best Practices](https://www.anthropic.com/index/prompt-engineering) (Anthropic 2025)

---

**Version:** 3.1-self-optimized
**Last Updated:** 2025-10-21
