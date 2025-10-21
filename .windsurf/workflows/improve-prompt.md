---
created: "2025-10-21"
updated: "2025-10-21"
description: LLM-agnostic prompt optimization with model-specific enhancements and self-improvement methodology
auto_execution_mode: 2
category: Optimization
complexity: 70
tokens: 3000
dependencies:
  - improve-workflow
status: active
version: "2.0-self-optimized"
---

# Improve Prompt Workflow

**Purpose:** Optimize prompts for any LLM using cross-model best practices with quantitative validation.

**Invocation:** `/improve-prompt [target_model=auto]` + prompt text or file reference

**Philosophy:** Universal principles (clarity, structure, reasoning) + optional model-specific enhancements.

**Supported:** Claude 3.5+, GPT-4+, Gemini 1.5+, instruction-following LLMs

---

## Optimization Research & Learned Techniques (2025)

**Meta-Learning:** This workflow embodies self-improvement through iterative refinement based on empirical results.

### Core Optimization Principles

| Principle | Research Basis | Application |
|-----------|---------------|-------------|
| **Quality ≠ Verbosity** | Structured prompts improve accuracy 15-30% (Anthropic 2025) | Tables/bullets > prose for info density |
| **Strategic Context** | Targeted rationale > comprehensive coverage | Add "why" for key decisions, not everything |
| **Compression Threshold** | Don't exceed 80% reduction without validation | Balance conciseness with context preservation |
| **One Purpose Per Section** | Prevents LLM confusion from mixed topics | Each section answers single question |
| **Contextual Anchors** | Essential keywords guide LLM focus | Retain decision thresholds, quality criteria |

### Token Efficiency Techniques (Proven Effective)

**Priority by baseline quality:**

- **<7/10 quality:** Apply aggressive optimizations (all techniques)
- **7-8/10 quality:** Selective optimization (structure + examples)
- **>8/10 quality:** Maintenance focus (clarity, not transformation)

| Technique | Target | Transformation Example | Expected Savings | Quality Impact |
|-----------|--------|----------------------|------------------|----------------|
| **Information Distillation** | Verbose phrases | "Please provide detailed analysis" → "Analyze:" | 30-50% | Neutral/Positive |
| **Structured Bullets** | Long paragraphs | 200-word paragraph → 5 bullet points | 20-40% | Positive (scannability) |
| **Table Consolidation** | Verbose lists | 8 technique descriptions → compact table | 40-60% | Positive (comparison) |
| **Example Consolidation** | Redundant examples | 8 partial examples → 1 complete + 3 compact | 40-60% | Positive (depth) |
| **Metadata Deduplication** | Frontmatter repeats | Remove body metadata if in YAML frontmatter | 100% of dupes | Neutral |
| **Reference Externalization** | Inline documentation | [5 paragraphs] → "See: [link]" | 50-80% | Context-dependent |
| **Word-Level Optimization** | Common phrases | "in order to" → "to", "utilize" → "use" | 5-15% | Neutral |

**Research Evidence:**

- Explicit reasoning reduces hallucination 20-40% (OpenAI 2025)
- Format specifications improve adherence 50-100% (Google Gemini guidelines)
- Consistent delimiters (tables, XML) aid LLM parsing 25-35% (PromptHub 2025)

### Quality vs Conciseness Balance

**Scoring Framework:** `(Quality × 0.7) + (Efficiency Ratio × 0.3)`

Where:

- Quality = Σ(Completeness, Clarity, Structure, Usability, Context) / 5
- Efficiency Ratio = Quality Score / (tokens / 100)

**Decision Matrix:**

| Baseline Quality | Token Count | Strategy | Rationale |
|-----------------|-------------|----------|-----------|
| <6/10 | Any | Transform aggressively | Low baseline allows experimentation |
| 6-7/10 | <3000 | Balanced optimization | Room for improvement |
| 6-7/10 | >3000 | Prioritize conciseness | High verbosity, medium quality |
| 7-8/10 | <2000 | Maintain, polish | Already efficient |
| 7-8/10 | >2000 | Selective optimization | Focus high-impact areas |
| >8/10 | Any | **Minimal changes** | Risk damaging high baseline |

**Key Insight:** Quality improvements + token reduction are NOT mutually exclusive with strategic application.

### Meta-Prompting Self-Improvement

**Iterative Refinement Loop:**

1. **Baseline Assessment** → Measure current quality/efficiency
2. **Apply Techniques** → Selective based on baseline
3. **Validate** → Ensure intent preserved, quality maintained/improved
4. **Measure Delta** → Quantify improvements
5. **Learn** → Update technique weights based on results
6. **Repeat** → Self-apply learnings to workflow itself

**Self-Application Criteria:** Only self-optimize if baseline <8/10 OR tokens >4000. Otherwise, risk over-optimization.

---

## When to Use

**Use for:** Workflows, rules, ad-hoc prompts, system prompts, inconsistent results, structure improvements

**Avoid:** Changing roles/personas, security logic, project rules (without approval), already-optimized prompts

---

## Stage 0: Workflow Entry

🔄 **Entering /improve-prompt:** Prompt optimization with quantitative analysis

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "🔄 Starting /improve-prompt workflow",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input", status: "in_progress" },
    { step: "2. /improve-prompt - Detect model and context", status: "pending" },
    { step: "3. /improve-prompt - Analyze quality", status: "pending" },
    { step: "4. /improve-prompt - Apply universal optimizations", status: "pending" },
    { step: "5. /improve-prompt - Apply model-specific enhancements", status: "pending" },
    { step: "6. /improve-prompt - Validate and present results", status: "pending" }
  ]
})
```

---

## Stage 2: Input Capture

🔄 **Entering Stage 2: Input Capture**

### 2.1 Parse Input

**Input formats:** Inline text, file reference (`@workflow:name`), code block

**Extract:** Original text, context type (workflow/rule/ad-hoc/system), structure, examples, variables

---

## Stage 2.5: Model Detection

### 2.5.1 Determine Target Model

**Detection:** User specified → Context clues (XML=Claude, Markdown=GPT, System=Gemini) → Default: auto

| Model Family | Preferred Structure | Key Strengths | Optimization Focus |
|--------------|-------------------|---------------|-------------------|
| **Claude (3.5+)** | XML tags | Extended thinking, detailed reasoning | Chain-of-thought, explicit structure |
| **GPT (4+)** | Markdown | Code generation, structured output | Clear format, step-by-step |
| **Gemini (1.5+)** | Hierarchical | Long context, multimodal | System instructions, query placement |
| **Generic/Auto** | GOLDEN framework | Instruction following | Universal patterns only |

### 2.5.2 Conciseness Priority

| Token Count | Word Count | Weight | Priority | Strategy |
|-------------|------------|--------|----------|----------|
| <2000 | <1000 | 1.0x | Low | Standard optimization |
| 2000-4000 | 1000-2000 | 1.5x | Moderate | Conciseness focus |
| 4000-6000 | 2000-3000 | 2.0x | High | Aggressive conciseness |
| >6000 | >3000 | 2.5x | **CRITICAL** | **Decomposition candidate** |

**Apply weight:** Multiply "Example inclusion" and "Instruction density" scores by weight

### 2.5.3 Special Constraints

**Windsurf workflows:** Preserve `update_plan`, frontmatter, stage numbering → Route to `/improve-workflow`
**Project rules:** Preserve triggers, anti-patterns, cross-references
**GPT-5-Codex:** Minimal prompting, no preambles, concise tools

### 2.5.4 Sub-Workflow Routing

**If Windsurf workflow:** Route to `/improve-workflow` (handles workflow-specific optimization, decomposition detection, syntax preservation)

**See:** [improve-workflow.md](./improve-workflow.md)

---

## Stage 3: Analyze Current Prompt

🔄 **Entering Stage 3: Analyze Current Prompt**

### 3.1 Quality Assessment

**Score dimensions (0-10):** Clear objective, specific instructions, context, constraints, output format, examples, reasoning guidance, structure

**Identify issues:**

- **Critical:** Ambiguous objective, missing context, no output format, conflicting instructions
- **High:** Add chain-of-thought, structure (XML/Markdown), examples, step-by-step, constraints
- **Medium:** Improve examples, edge cases, terminology

**Complexity:** Cognitive load, task complexity, ambiguity, context dependency

**Recommendations:** Simple → clarity/format | Complex → CoT/examples/structure | High ambiguity → constraints/examples/steps

---

## Stage 4: Apply Universal Optimizations

🔄 **Entering Stage 4: Apply Universal Optimizations**

**Philosophy:** Start with cross-model techniques that work for ALL LLMs, then add model-specific enhancements.

### 4.1 GOLDEN Framework

**Apply:** Goal (objective + success), Output (format/length/tone), Limits (constraints), Data (context/examples), Evaluation (rubric), Next (follow-up/alternatives)

### 4.2 Universal Techniques

**Priority by weight:** 1.0x=standard | 1.5x=prioritize conciseness | 2.0x=aggressive | 2.5x=ALL conciseness+decomposition

#### Technique 1: Chain-of-Thought

**When:** Moderate-high complexity, critical accuracy
**Add:** Step-by-step reasoning, `<analysis>` tags

#### Technique 2: XML Structure

**When:** Multiple sections, complex inputs
**Tags:** `<input>`, `<instructions>`, `<constraints>`, `<output_format>`

#### Technique 3: Standardize Examples

**When:** Inconsistent formatting
**Quality:** Show reasoning, cover edge cases, demonstrate format, 2-5 examples

#### Technique 4: Step-by-Step Instructions

**When:** Multiple phases/decisions
**Format:** Numbered lists, bold step names, decision criteria

#### Technique 5: Output Format

**When:** Format important/unclear
**Specify:** JSON schema, markdown structure, or exact template

#### Technique 6: Constraints

**When:** Unclear boundaries/limitations
**Add:** Length limits, scope, sources, tone, requirements

#### Technique 7: Prefill

**When:** Output should start with specific format
**Add:** Opening phrase or tag instruction

#### Technique 8: Windsurf Context

**Add:** @-mentions (`@file`, `@dir`, `@web`), framework/libraries, complexity constraints, security guidelines

---

### 4.3 Conciseness Techniques (Weight ≥ 1.5x)

| Technique | Target | Transformation | Savings |
|-----------|--------|----------------|----------|
| **9. Information Distillation (×2.0)** | Verbose phrases | "Please provide..." → "Provide..." | 30-50% |
| **10. Structured Bullets (×1.5)** | Long paragraphs | Prose → bullet lists | 20-40% |
| **11. Keyword Extraction (×1.8)** | Detailed descriptions | "Execute the command" → "Run: `cmd`" | 15-30% |
| **12. Example Consolidation (×2.0)** | Redundant examples | 8 verbose → 3 table rows | 40-60% |
| **13. Reference Externalization (×1.3)** | Inline docs | [5 paragraphs] → See: [link] | 50-80% |

### 4.4 Apply Techniques

**Order:** Structure → CoT → Steps → Examples → Format → Constraints → Prefill → Context-specific

---

## Stage 5: Apply Model-Specific Enhancements

🔄 **Entering Stage 5: Apply Model-Specific Enhancements**

| Model | Key Enhancements |
|-------|------------------|
| **Claude 3.5+** | `<thinking>` tags, explicit XML structure, detailed reasoning scaffolds |
| **GPT-4+** | Markdown headings, structured output (JSON schemas), code-first examples |
| **GPT-5-Codex** | Minimal prompting, no preambles, concise tools (terminal + apply_patch) |
| **Gemini 1.5+** | System instructions, hierarchical structure, queries at end (long context) |
| **Auto/Unknown** | Universal only (GOLDEN), avoid model-specific, max compatibility |

---

## Stage 6: Validate Improvements

🔄 **Entering Stage 6: Validate Improvements**

**Verify:** Intent preservation (objective, requirements, constraints, output type) | Coherence (consistent, complete, clear, appropriate length) | Context compatibility (conventions, @-mentions, no conflicts)

---

## Stage 7: Calculate Metrics

**Quality scores (0-10):** Re-assess 8 dimensions (objective, instructions, context, constraints, format, examples, reasoning, structure)

**Structural metrics:** Character/word count, sections, examples, instructions, XML tags (before/after comparison)

**Expected impact:** Accuracy +15-30%, format adherence +50-100%, consistency +20-40%, completion +10-25%

---

## Stage 8: Present Results

🔄 **Entering Stage 8: Present Results with Analysis**

**Output template:**

```markdown
# 🎯 Prompt Optimization Results

## Summary
**Date:** YYYY-MM-DD | **Original:** [N]/10 | **Improved:** [N]/10 | **Change:** +[N] ([X]%) | **Techniques:** [N]

## Quantitative Improvements
| Metric | Before | After | Δ | Impact |
|--------|--------|-------|---|--------|
| Overall | [N]/10 | [N]/10 | +[N] | [X]% |
| Clarity/Specificity/Structure/Completeness | [scores] | [scores] | [deltas] | [impacts] |

**Expected gains:** Accuracy +15-30%, Format +50-100%, Consistency +20-40%, Completion +10-25%

## Key Changes
1. **[Category]:** [Change] → [Benefit]
2. **[Category]:** [Change] → [Benefit]
[Continue...]

## Techniques Applied
| Technique | ✓/✗ | Impact | Rationale |
|-----------|-----|--------|----------|
[List applied techniques with impact scores]

## Improved Prompt
````markdown
[FULL IMPROVED PROMPT]
````

## Validation

✓ Intent preserved | ✓ Coherent | ✓ Context compatible

## Next Steps

1. Test with representative inputs
2. Compare original vs improved outputs
3. Measure actual vs expected performance
4. Iterate based on results

```

✅ **Completed /improve-prompt:** +[N] points ([X]%), [Y] techniques

---

## Anti-Patterns

❌ **Don't:** Blindly apply all techniques | Change intent/role | Ignore context | Skip validation | Provide only improved prompt without analysis | Over-optimize length at expense of clarity

✅ **Do:** Assess needs, apply beneficial techniques | Preserve intent | Tailor to context | Always validate | Include analysis + rationale | Balance clarity with conciseness

---

## Integration & Performance

**Called by:** User, other workflows, workflow development
**Calls:** `/improve-workflow` (for Windsurf workflows)
**Output:** Analysis, metrics, improved prompt, recommendations

**Performance:** 2-5 min execution | ~8-15k tokens | 60/100 complexity | >95% success

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Little room for improvement | Minor polish only, explain prompt is high-quality |
| Intent changed | Revert, focus on structure/clarity only |
| Metrics don't show improvement | Explain qualitative improvements (examples, etc.) |
| User disagrees | Ask for feedback, iterate with guidance |

---

## References

**External:** [Anthropic Prompt Improver](https://www.anthropic.com/news/prompt-improver) | [Claude Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering) | [Windsurf Best Practices](https://docs.windsurf.com/best-practices/prompt-engineering)

**Internal:** [improve-workflow.md](./improve-workflow.md) | [12_task_orchestration.md](../rules/12_task_orchestration.md) | `docs/CONSTITUTION.md`

**Research date:** 2025-10-21

---

**Created:** 2025-10-21
**Version:** 1.0.0
**Maintained by:** mcp-web core team
**Status:** Active
