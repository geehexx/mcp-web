---
created: "2025-10-21"
updated: "2025-10-21"
description: Optimize prompts using modern best practices and quantitative analysis
auto_execution_mode: 2
category: Optimization
complexity: 60
tokens: 6357
dependencies: []
status: active
---

# Improve Prompt Workflow

**Purpose:** Systematically optimize prompts using Claude 3.5 Sonnet 4 and Windsurf best practices with quantitative validation.

**Invocation:** `/improve-prompt` followed by the prompt text, or reference a file containing the prompt

**Philosophy:** Good prompts are specific, structured, and guide model reasoning. Quantify improvements to validate effectiveness.

**Based on:** Anthropic Prompt Improver, Windsurf prompt engineering guidelines, Claude extended thinking capabilities

---

## When to Use

Use this workflow to improve:

- ✅ Workflow prompts (in `.windsurf/workflows/`)
- ✅ Rule definitions (in `.windsurf/rules/`)
- ✅ Ad-hoc prompts for specific tasks
- ✅ System prompts for tools/agents
- ✅ Prompts showing inconsistent results
- ✅ Prompts needing better structure

Do NOT use for:

- ❌ Changing fundamental roles or personas
- ❌ Altering security-critical validation logic
- ❌ Modifying established project rules without approval
- ❌ Prompts that are already highly optimized

---

## Stage 0: Workflow Entry

🔄 **Entering /improve-prompt:** Prompt optimization with quantitative analysis

**Print workflow entry announcement:**

```markdown
🔄 **Entering /improve-prompt:** Analyzing and optimizing prompt with best practices
```

---

## Stage 1: Create Task Plan

🔄 **Entering Stage 1: Create Task Plan**

**MANDATORY:** Create task list before any analysis.

```typescript
update_plan({
  explanation: "🔄 Starting /improve-prompt workflow",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "in_progress" },
    { step: "2. /improve-prompt - Analyze current prompt quality", status: "pending" },
    { step: "3. /improve-prompt - Apply optimization techniques", status: "pending" },
    { step: "4. /improve-prompt - Validate improvements", status: "pending" },
    { step: "5. /improve-prompt - Calculate quantitative metrics", status: "pending" },
    { step: "6. /improve-prompt - Present results with analysis", status: "pending" }
  ]
})
```

✓ Task plan created

---

## Stage 2: Input Capture

🔄 **Entering Stage 2: Input Capture**

### 2.1 Parse Input Prompt

**Prompt can be provided as:**

1. **Inline text** - User provides prompt directly after `/improve-prompt`
2. **File reference** - User mentions file containing prompt (e.g., `@workflow:commit`)
3. **Code block** - User pastes prompt in markdown code block

**Extract:**

- Full original prompt text
- Context type (workflow, rule, ad-hoc, system)
- Current structure (if any)
- Examples (if any)
- Variables/placeholders (e.g., `{{variable}}`, `@mentions`)

**Store original:**

```markdown
**Original Prompt:**
[Capture exact original text here]
```

**Print stage completion:**

```markdown
📋 **Stage 2 Complete:** Input prompt captured ([N] characters, [type])
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Input captured, proceeding to analysis",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Analyze current prompt quality", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 3: Analyze Current Prompt

🔄 **Entering Stage 3: Analyze Current Prompt**

### 3.1 Quality Assessment

**Analyze against best practices:**

#### Clarity Dimensions

| Dimension | Score (0-10) | Issues Identified |
|-----------|--------------|-------------------|
| **Clear objective** | [N] | [What's unclear about the goal?] |
| **Specific instructions** | [N] | [What steps are missing/vague?] |
| **Context provision** | [N] | [What context is missing?] |
| **Constraint definition** | [N] | [What constraints are unspecified?] |
| **Output format** | [N] | [How is output format unclear?] |
| **Example inclusion** | [N] | [Are examples present and clear?] |
| **Reasoning guidance** | [N] | [Does it guide step-by-step thinking?] |
| **Structure/organization** | [N] | [How could structure improve?] |

**Overall Baseline Score:** [Average of dimensions]/10

#### Specific Issues Matrix

**Critical Issues** (must fix):

- [ ] Ambiguous objective
- [ ] Missing critical context
- [ ] No output format specification
- [ ] Conflicting instructions

**High-Priority Improvements**:

- [ ] Add chain-of-thought reasoning
- [ ] Structure with XML tags
- [ ] Standardize examples
- [ ] Add step-by-step instructions
- [ ] Specify constraints clearly

**Medium-Priority Enhancements**:

- [ ] Improve example quality
- [ ] Add edge case handling
- [ ] Clarify terminology
- [ ] Enhance context references

**Low-Priority Polish**:

- [ ] Grammar/spelling corrections
- [ ] Formatting consistency
- [ ] Tone adjustment

### 3.2 Complexity Analysis

**Prompt Complexity Metrics:**

- **Cognitive Load:** [Low/Medium/High] - How much understanding required
- **Task Complexity:** [Simple/Moderate/Complex] - Nature of the task
- **Ambiguity Level:** [Low/Medium/High] - How much is left to interpretation
- **Context Dependency:** [Low/Medium/High] - How much external knowledge needed

**Recommendation:**

- Simple prompts → Focus on clarity and format
- Complex prompts → Add chain-of-thought, examples, structure
- High ambiguity → Add constraints, examples, step-by-step guidance

### 3.3 Context-Specific Analysis

**For Windsurf workflows:**

- [ ] Uses `@-mentions` appropriately for context
- [ ] Specifies frameworks/libraries if applicable
- [ ] Includes constraints (time, space complexity)
- [ ] Provides clear examples with context

**For project rules:**

- [ ] Follows `.windsurf/rules/` structure
- [ ] Has appropriate trigger conditions
- [ ] Includes anti-patterns section
- [ ] References related rules/workflows

**For ad-hoc prompts:**

- [ ] Task-specific enough
- [ ] Includes all necessary context
- [ ] Specifies desired output format

**Print stage completion:**

```markdown
📋 **Stage 3 Complete:** Analysis complete - Baseline score: [N]/10, [X] critical issues, [Y] improvements identified
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Analysis complete, applying optimizations",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Analyze current prompt quality", status: "completed" },
    { step: "3. /improve-prompt - Apply optimization techniques", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 4: Apply Optimization Techniques

🔄 **Entering Stage 4: Apply Optimization Techniques**

### 4.1 Core Optimization Strategies

Apply techniques in priority order based on analysis:

#### Technique 1: Add Chain-of-Thought Reasoning

**When:** Task complexity is moderate-high, or accuracy is critical

**How:**

```markdown
Before providing your final answer, think through the problem step by step:

1. [Step 1 description]
2. [Step 2 description]
3. [Step 3 description]

Wrap your analysis in <analysis> tags, then provide your final response.
```

**Example transformation:**

```markdown
<!-- Before -->
Summarize this article in 3 sentences.

<!-- After -->
Summarize this article in 3 sentences. Follow these steps:

1. Identify the main topic and key arguments
2. Note supporting evidence and examples
3. Synthesize into 3 concise sentences

Wrap your analysis in <analysis> tags:
<analysis>
[Your step-by-step thinking]
</analysis>

Then provide your final 3-sentence summary.
```

#### Technique 2: Structure with XML Tags

**When:** Prompt has multiple sections or complex inputs

**How:**

```markdown
<input>
[User input data]
</input>

<instructions>
[What to do with the input]
</instructions>

<constraints>
[Limitations and requirements]
</constraints>

<output_format>
[Expected output structure]
</output_format>
```

**Benefits:**

- Clear separation of concerns
- Easier for model to parse
- Reduces ambiguity
- Enables better context handling

#### Technique 3: Standardize Examples

**When:** Examples exist but inconsistently formatted

**How:**

```markdown
<examples>
  <example>
    <input>
    [Example input]
    </input>
    <reasoning>
    [Step-by-step thought process]
    </reasoning>
    <output>
    [Expected output]
    </output>
  </example>
</examples>
```

**Quality criteria:**

- Examples show reasoning, not just input/output
- Examples cover edge cases
- Examples demonstrate format exactly
- 2-5 examples (more = diminishing returns)

#### Technique 4: Add Step-by-Step Instructions

**When:** Task has multiple phases or decisions

**How:**

```markdown
Complete this task by following these steps in order:

1. **[Step 1 Name]:** [Detailed description]
   - [Sub-step 1a]
   - [Sub-step 1b]

2. **[Step 2 Name]:** [Detailed description]
   - [Sub-step 2a]
   - [Sub-step 2b]

3. **[Step 3 Name]:** [Detailed description]
```

**Best practices:**

- Use numbered lists for sequential steps
- Use bold for step names
- Include decision criteria
- Specify what to do at each step

#### Technique 5: Specify Output Format

**When:** Output format is important or currently unclear

**How:**

```markdown
Provide your response in this exact format:

```json
{
  "field1": "value",
  "field2": ["list", "of", "items"],
  "field3": {
    "nested": "structure"
  }
}
```

OR

```markdown
Format your response as:

**Section 1:** [Content]
**Section 2:** [Content]
**Section 3:** [Content]
```

#### Technique 6: Add Constraints

**When:** Boundaries or limitations are unclear

**How:**

```markdown
<constraints>
  - Output must be between 100-150 words
  - Use only information from the provided context
  - Do not include speculation or external knowledge
  - Maintain objective tone
  - Include at least 2 specific examples
</constraints>
```

#### Technique 7: Include Prefill Strategy

**When:** Output should always start with specific format

**How:**

Add prefill instruction:

```markdown
Begin your response with: "Analysis complete. "
```

Or for structured output:

```markdown
Start your response with the opening tag: <response>
```

#### Technique 8: Windsurf-Specific Enhancements

**For Windsurf context:**

```markdown
Use @-mentions to reference specific context:
- `@file:path/to/file.py` for specific files
- `@dir:src/module` for directories
- `@web` for web search when needed

Specify technical requirements:
- Framework: [FastAPI, React, etc.]
- Libraries: [specific versions if critical]
- Complexity constraints: [O(n) time, O(1) space]
- Security: [OWASP guidelines, input validation]
```

### 4.2 Apply Selected Techniques

**Based on analysis, apply techniques in optimal order:**

1. First: Structure (XML tags if beneficial)
2. Second: Chain-of-thought (if complex task)
3. Third: Step-by-step instructions
4. Fourth: Examples (standardize or add)
5. Fifth: Output format specification
6. Sixth: Constraints
7. Seventh: Prefill (if beneficial)
8. Eighth: Context-specific enhancements

**Generate improved prompt:**

```markdown
**Improved Prompt:**
[Full improved prompt here]
```

**Print stage completion:**

```markdown
📋 **Stage 4 Complete:** [N] optimization techniques applied
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Optimizations applied, validating improvements",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Analyze current prompt quality", status: "completed" },
    { step: "3. /improve-prompt - Apply optimization techniques", status: "completed" },
    { step: "4. /improve-prompt - Validate improvements", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 5: Validate Improvements

🔄 **Entering Stage 5: Validate Improvements**

### 5.1 Intent Preservation Check

**Verify improved prompt maintains:**

- [ ] Original objective/goal
- [ ] Core requirements
- [ ] Key constraints
- [ ] Intended output type

**If ANY check fails:** Revise improvements to preserve intent

### 5.2 Coherence Check

**Verify improved prompt is:**

- [ ] Internally consistent (no contradictions)
- [ ] Complete (all necessary info included)
- [ ] Clear (no new ambiguities introduced)
- [ ] Appropriate length (not overly verbose)

### 5.3 Context Compatibility

**For Windsurf workflows/rules:**

- [ ] Follows repository conventions
- [ ] Uses appropriate @-mentions
- [ ] Compatible with existing workflows
- [ ] Doesn't conflict with project rules

**Print stage completion:**

```markdown
📋 **Stage 5 Complete:** Validation passed - intent preserved, coherence confirmed
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Validation complete, calculating metrics",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Analyze current prompt quality", status: "completed" },
    { step: "3. /improve-prompt - Apply optimization techniques", status: "completed" },
    { step: "4. /improve-prompt - Validate improvements", status: "completed" },
    { step: "5. /improve-prompt - Calculate quantitative metrics", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 6: Calculate Metrics

🔄 **Entering Stage 6: Calculate Quantitative Metrics**

### 6.1 Quality Score Comparison

**Re-assess improved prompt on same dimensions:**

| Dimension | Before | After | Δ | Notes |
|-----------|--------|-------|---|-------|
| Clear objective | [N] | [N] | +[N] | [How it improved] |
| Specific instructions | [N] | [N] | +[N] | [How it improved] |
| Context provision | [N] | [N] | +[N] | [How it improved] |
| Constraint definition | [N] | [N] | +[N] | [How it improved] |
| Output format | [N] | [N] | +[N] | [How it improved] |
| Example inclusion | [N] | [N] | +[N] | [How it improved] |
| Reasoning guidance | [N] | [N] | +[N] | [How it improved] |
| Structure/organization | [N] | [N] | +[N] | [How it improved] |

**Overall Scores:**

- **Before:** [N]/10
- **After:** [N]/10
- **Improvement:** +[N] points ([X]% increase)

### 6.2 Structural Metrics

**Before:**

- Character count: [N]
- Word count: [N]
- Sections: [N]
- Examples: [N]
- Instructions: [N steps]
- XML tags: [N]

**After:**

- Character count: [N] ([+/-X]%)
- Word count: [N] ([+/-X]%)
- Sections: [N] ([+/-X])
- Examples: [N] ([+/-X])
- Instructions: [N steps] ([+/-X])
- XML tags: [N] ([+X])

**Analysis:**

- Length increase justified by: [clarity, examples, structure]
- Structural improvements: [what changed]
- Organization: [how it's better organized]

### 6.3 Technique Application Summary

**Techniques Applied:**

- [✓] Chain-of-thought reasoning → +[N] clarity points
- [✓] XML structuring → +[N] organization points
- [✓] Step-by-step instructions → +[N] specificity points
- [✓] Output format specification → +[N] format points
- [✓] Constraint definition → +[N] constraint points
- [✓] Example standardization → +[N] example points
- [✓] Windsurf enhancements → +[N] context points

**Total techniques applied:** [N]/8

### 6.4 Expected Impact

**Based on Anthropic research:**

- **Accuracy improvement:** ~[15-30]% (typical for chain-of-thought addition)
- **Format adherence:** ~[50-100]% improvement (with clear format specification)
- **Consistency:** ~[20-40]% improvement (with examples and structure)
- **Task completion:** ~[10-25]% improvement (with step-by-step guidance)

**Project-specific benefits:**

- Reduces ambiguity for AI agents
- Improves workflow reliability
- Enhances maintainability
- Facilitates easier updates

**Print stage completion:**

```markdown
📋 **Stage 6 Complete:** Metrics calculated - Overall improvement: +[N] points ([X]%)
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Metrics complete, preparing final presentation",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Analyze current prompt quality", status: "completed" },
    { step: "3. /improve-prompt - Apply optimization techniques", status: "completed" },
    { step: "4. /improve-prompt - Validate improvements", status: "completed" },
    { step: "5. /improve-prompt - Calculate quantitative metrics", status: "completed" },
    { step: "6. /improve-prompt - Present results with analysis", status: "in_progress" }
  ]
})
```

---

## Stage 7: Present Results

🔄 **Entering Stage 7: Present Results with Analysis**

### 7.1 Comprehensive Output Format

```markdown
# 🎯 Prompt Optimization Results

## Summary

**Optimization Date:** YYYY-MM-DD
**Original Score:** [N]/10
**Improved Score:** [N]/10
**Improvement:** +[N] points ([X]% increase)
**Techniques Applied:** [N]/8

---

## Quantitative Improvements

| Metric | Before | After | Change | Impact |
|--------|--------|-------|--------|--------|
| Overall Quality | [N]/10 | [N]/10 | +[N] | [X]% increase |
| Clarity | [N]/10 | [N]/10 | +[N] | [description] |
| Specificity | [N]/10 | [N]/10 | +[N] | [description] |
| Structure | [N]/10 | [N]/10 | +[N] | [description] |
| Completeness | [N]/10 | [N]/10 | +[N] | [description] |

**Expected Performance Gains:**

- Accuracy: ~[X]% improvement
- Format adherence: ~[X]% improvement
- Consistency: ~[X]% improvement
- Task completion: ~[X]% improvement

---

## Key Changes Made

### 1. [Change Category 1]

**What changed:**
[Description of change]

**Why it helps:**
[Explanation of benefit]

**Example:**
```text
Before: [snippet]
After: [snippet]
```

### 2. [Change Category 2]

**What changed:**
[Description of change]

**Why it helps:**
[Explanation of benefit]

**Example:**

```text
Before: [snippet]
After: [snippet]
```

[Continue for all major changes...]

---

## Techniques Applied

| Technique | Applied | Impact Score | Rationale |
|-----------|---------|--------------|-----------|
| Chain-of-thought reasoning | ✓ | +[N] | [Why applied] |
| XML structuring | ✓ | +[N] | [Why applied] |
| Step-by-step instructions | ✓ | +[N] | [Why applied] |
| Output format specification | ✓ | +[N] | [Why applied] |
| Constraint definition | ✓ | +[N] | [Why applied] |
| Example standardization | ✓ | +[N] | [Why applied] |
| Prefill strategy | ✗ | N/A | [Why not applied] |
| Context enhancements | ✓ | +[N] | [Why applied] |

**Total Impact Score:** +[N] points

---

## Improved Prompt

Use four backticks to ensure proper code block nesting:

````markdown
[FULL IMPROVED PROMPT HERE]

[Preserve all formatting, XML tags, examples, structure]
```

---

## Validation Results

**Intent Preservation:** ✓ Passed

- Original objective maintained
- Core requirements preserved
- Key constraints intact

**Coherence Check:** ✓ Passed

- Internally consistent
- Complete information
- Clear instructions
- Appropriate length

**Context Compatibility:** ✓ Passed

- Follows repository conventions
- Compatible with existing workflows
- No conflicts with project rules

---

## Implementation Recommendations

### Immediate Actions

1. **Test the improved prompt** with representative inputs
2. **Compare outputs** between original and improved versions
3. **Measure actual performance** against expected gains
4. **Iterate if needed** based on real-world results

### Long-term Considerations

- **Monitor effectiveness** over multiple uses
- **Gather feedback** from users/agents
- **Refine further** based on edge cases discovered
- **Document lessons learned** for future optimizations

### If Using in `.windsurf/` Directory

- **Update workflow file** if this is a workflow prompt
- **Update rule file** if this is a rule definition
- **Run validation:** `task validate:workflows` or equivalent
- **Commit with message:** `feat(workflows): optimize [name] prompt for clarity and accuracy`

---

## References & Sources

**Based on:**

- [Anthropic Prompt Improver](https://www.anthropic.com/news/prompt-improver)
- [Claude Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Windsurf Prompt Engineering Best Practices](https://docs.windsurf.com/best-practices/prompt-engineering)
- Claude 3.5 Sonnet 4 (Extended Thinking) capabilities
- Project constitution: `docs/CONSTITUTION.md`
- Workflow patterns: `.windsurf/workflows/`

**Research conducted:** YYYY-MM-DD

---

## Next Steps

- [ ] Test improved prompt with real inputs
- [ ] Measure actual vs. expected improvements
- [ ] Implement in target location (if applicable)
- [ ] Document results
- [ ] Share learnings with team (if applicable)

---

✅ **Workflow Complete:** Prompt optimization finished with comprehensive analysis

**Print workflow completion:**

```markdown
✅ **Completed /improve-prompt:** Optimization complete - +[N] point improvement ([X]%), [Y] techniques applied
```

**Update final task plan:**

```typescript
update_plan({
  explanation: "✅ Optimization complete and presented",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Analyze current prompt quality", status: "completed" },
    { step: "3. /improve-prompt - Apply optimization techniques", status: "completed" },
    { step: "4. /improve-prompt - Validate improvements", status: "completed" },
    { step: "5. /improve-prompt - Calculate quantitative metrics", status: "completed" },
    { step: "6. /improve-prompt - Present results with analysis", status: "completed" }
  ]
})
```

---

## Anti-Patterns

### ❌ Don't: Blindly Apply All Techniques

**Bad:** Apply every optimization regardless of need

**Good:** Assess prompt type and complexity, apply only beneficial techniques

**Reason:** Over-engineering simple prompts wastes tokens and adds unnecessary complexity

### ❌ Don't: Change Intent or Role

**Bad:** Modify the fundamental purpose or role definition

**Good:** Preserve original intent while improving clarity and structure

**Reason:** Optimization should enhance, not alter, the prompt's purpose

### ❌ Don't: Ignore Context

**Bad:** Apply generic improvements without considering where prompt will be used

**Good:** Tailor improvements to context (Windsurf, production system, etc.)

**Reason:** Context-specific enhancements provide better results

### ❌ Don't: Skip Validation

**Bad:** Present improved prompt without checking intent preservation

**Good:** Always validate that improvements maintain original objectives

**Reason:** Broken prompts are worse than unoptimized ones

### ❌ Don't: Provide Only Improved Prompt

**Bad:** Just show the new prompt without explanation

**Good:** Include analysis, metrics, and rationale for changes

**Reason:** Understanding WHY changes were made enables learning and iteration

### ❌ Don't: Over-Optimize Length

**Bad:** Make prompt as short as possible

**Good:** Balance clarity and conciseness

**Reason:** Clarity is more important than brevity; extra words that add clarity are worth it

---

## Workflow Integration

### Called By

- User (direct invocation)
- Other workflows when prompt optimization needed
- During workflow development/refinement

### Calls

- None (this is a leaf workflow)

### Output

- Comprehensive improvement analysis
- Quantitative metrics (before/after scores)
- Improved prompt in markdown code block
- Implementation recommendations

---

## Performance Characteristics

**Typical Execution Time:** 2-5 minutes (depends on prompt complexity)

**Token Usage:** ~8,000-15,000 tokens (analysis + generation)

**Complexity Score:** 60/100 (moderate complexity)

**Success Rate:** >95% for well-formed inputs

---

## Troubleshooting

### Issue: Analysis shows little room for improvement

**Cause:** Prompt is already well-optimized

**Solution:** Provide minor polish only; explain that prompt is already high-quality

### Issue: Improved prompt changes intent

**Cause:** Over-optimization or misunderstanding of objective

**Solution:** Revert problematic changes, focus on structure/clarity only

### Issue: Metrics don't show expected improvement

**Cause:** Baseline was already high, or improvements are qualitative

**Solution:** Explain that some improvements (like better examples) may not show in numeric scores but still add value

### Issue: User disagrees with improvements

**Cause:** Different priorities or constraints not captured

**Solution:** Ask for specific feedback, iterate with user's guidance

---

## References

### External Sources

- [Anthropic: Prompt Improver](https://www.anthropic.com/news/prompt-improver)
- [Claude Docs: Prompt Engineering](https://docs.anthropic.com/claude/docs/prompt-engineering)
- [Claude Docs: Extended Thinking](https://docs.anthropic.com/claude/docs/extended-thinking)
- [Windsurf: Prompt Engineering](https://docs.windsurf.com/best-practices/prompt-engineering)
- [Windsurf: Workflows](https://docs.windsurf.com/plugins/cascade/workflows)

### Internal References

- `docs/CONSTITUTION.md` - Project prompt standards
- `.windsurf/workflows/` - Workflow patterns
- `.windsurf/rules/` - Rule definitions
- [Task Orchestration](../rules/12_task_orchestration.md)

### Research Date

**External research conducted:** 2025-10-21

**Sources verified:** 2025-10-21

---

**Created:** 2025-10-21
**Version:** 1.0.0
**Maintained by:** mcp-web core team
**Status:** Active
