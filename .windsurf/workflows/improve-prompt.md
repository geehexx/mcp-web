---
created: "2025-10-21"
updated: "2025-10-21"
description: LLM-agnostic prompt optimization with model-specific enhancements and metadata tracking
auto_execution_mode: 2
category: Optimization
complexity: 65
tokens: 9500
dependencies:
  - improve-workflow
status: active
---

# Improve Prompt Workflow

**Purpose:** Systematically optimize prompts for any LLM (Claude, GPT, Gemini, etc.) using cross-model best practices with quantitative validation.

**Invocation:** `/improve-prompt [target_model=auto]` followed by the prompt text, or reference a file containing the prompt

**Philosophy:** Good prompts share universal principles (clarity, structure, reasoning guidance) with model-specific enhancements applied when beneficial.

**Based on:** Cross-model research (2025), Anthropic Prompt Improver, OpenAI GPT-5-Codex patterns, Google Gemini guidelines, Windsurf best practices

**Supported Models:** Claude (3.5+), GPT (4+), Gemini (1.5+), and other instruction-following LLMs

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
    { step: "2. /improve-prompt - Detect target model and context", status: "pending" },
    { step: "3. /improve-prompt - Analyze current prompt quality", status: "pending" },
    { step: "4. /improve-prompt - Apply universal optimizations", status: "pending" },
    { step: "5. /improve-prompt - Apply model-specific enhancements", status: "pending" },
    { step: "6. /improve-prompt - Validate improvements", status: "pending" },
    { step: "7. /improve-prompt - Calculate quantitative metrics", status: "pending" },
    { step: "8. /improve-prompt - Present results with analysis", status: "pending" }
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
  explanation: "Input captured, detecting target model",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Detect target model and context", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 2.5: Model Detection and Context Analysis

🔄 **Entering Stage 2.5: Model Detection**

### 2.5.1 Determine Target Model

**Detection strategy:**

1. **User specified:** Check if user provided `target_model=` parameter
2. **Context clues:** Analyze prompt for model-specific patterns:
   - XML tags (`<thinking>`, `<instructions>`) → Likely Claude
   - Markdown headings (`###`) → Likely GPT
   - System instruction patterns → Likely Gemini
3. **Default:** Use `auto` (apply universal optimizations + optional model-specific)

**Model profiles:**

| Model Family | Preferred Structure | Key Strengths | Optimization Focus |
|--------------|-------------------|---------------|-------------------|
| **Claude (3.5+)** | XML tags | Extended thinking, detailed reasoning | Chain-of-thought, explicit structure |
| **GPT (4+)** | Markdown | Code generation, structured output | Clear format, step-by-step |
| **Gemini (1.5+)** | Hierarchical | Long context, multimodal | System instructions, query placement |
| **Generic/Auto** | GOLDEN framework | Instruction following | Universal patterns only |

### 2.5.2 Calculate Token Count and Conciseness Priority

**Count tokens:**

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")
token_count = len(enc.encode(prompt_text))
word_count = len(prompt_text.split())
```

**Dynamic conciseness weight:**

| Token Count | Word Count | Weight | Priority | Strategy |
|-------------|------------|--------|----------|----------|
| <2000 | <1000 | 1.0x | Low | Standard optimization |
| 2000-4000 | 1000-2000 | 1.5x | Moderate | Conciseness focus |
| 4000-6000 | 2000-3000 | 2.0x | High | Aggressive conciseness |
| >6000 | >3000 | 2.5x | **CRITICAL** | **Decomposition candidate** |

**Apply weight to quality scoring:**

- Multiply "Example inclusion" score by conciseness weight
- Multiply "Instruction density" score by conciseness weight
- Adjust optimization technique priority based on weight

### 2.5.3 Identify Special Constraints

**For Windsurf workflows:**

- Must preserve task management syntax (`update_plan`, stage announcements)
- Must maintain frontmatter structure
- Workflow-specific conventions (stage numbering, etc.)
- **If detected: Route to `/improve-workflow` sub-workflow**

**For project rules:**

- Must preserve trigger conditions
- Must maintain anti-patterns sections
- Cross-reference integrity

**For GPT-5-Codex specifically:**

- "Less is more" principle (minimal prompting)
- No preambles (model doesn't support them)
- Concise tool descriptions
- Terminal + apply_patch tools only

### 2.5.4 Sub-Workflow Routing

**If prompt type is Windsurf workflow:**

```python
if ('.windsurf/workflows/' in file_path and
    'auto_execution_mode' in frontmatter):
    # This is a Windsurf workflow
    # Route to specialized sub-workflow
    result = call_subworkflow('improve-workflow', {
        'prompt': prompt_text,
        'token_count': token_count,
        'conciseness_weight': conciseness_weight,
        'metadata': frontmatter
    })
    return result  # Skip to Stage 8 (present results)
```

**Sub-workflow handles:**

- Workflow-specific analysis
- Conciseness-focused optimization
- Decomposition detection (>6000 tokens)
- Windsurf syntax preservation
- Validation and metrics

**See:** [improve-workflow.md](./improve-workflow.md) for details

**Print stage completion:**

```markdown
📋 **Stage 2.5 Complete:** Target model: [detected/specified], Context: [type], Special constraints: [N] identified
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Model detected, proceeding to analysis",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Detect target model and context", status: "completed" },
    { step: "3. /improve-prompt - Analyze current prompt quality", status: "in_progress" },
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

## Stage 4: Apply Universal Optimizations

🔄 **Entering Stage 4: Apply Universal Optimizations**

**Philosophy:** Start with cross-model techniques that work for ALL LLMs, then add model-specific enhancements.

### 4.1 GOLDEN Framework (Universal)

**Apply the GOLDEN checklist to all prompts:**

1. **Goal** - One clear objective and success criteria
2. **Output** - Required format, length, and tone
3. **Limits** - Constraints (scope, sources, policy, budget, tokens)
4. **Data** - Minimum context or examples
5. **Evaluation** - Rubric to verify the result
6. **Next** - Ask for follow-up plan or alternatives

**Template:**

```text
Goal: {{objective and success criteria}}
Output: {{format, length, tone}}
Limits: {{scope, rules, budget, tokens}}
Data: {{context, examples, sources}}
Evaluation: {{rubric or acceptance criteria}}
Next: Provide next steps or 2 alternatives if confidence < 0.7
```

### 4.2 Core Universal Optimization Strategies

Apply techniques in priority order based on analysis (these work across all models).

**CRITICAL:** Apply conciseness weight to technique priority:

- Weight 1.0x (low): Apply techniques 1-8 normally
- Weight 1.5x (moderate): Prioritize techniques 9-11 (conciseness)
- Weight 2.0x (high): Aggressively apply techniques 9-12
- Weight 2.5x (critical): Apply ALL conciseness techniques + flag decomposition

#### Universal Technique 1: Add Chain-of-Thought Reasoning

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

---

### 4.3 Conciseness-Focused Techniques

#### When to Apply

**Apply when conciseness weight ≥ 1.5x (tokens > 2000)**

These techniques prioritize token reduction while preserving meaning.

#### Technique 9: Information Distillation (Weight × 2.0)

**Target:** Verbose explanations, redundant phrases

**Transforms:**

```text
❌ "Please provide a comprehensive explanation of..."
✅ "Explain..."

❌ "It is important to note that you should..."
✅ "Must..."

❌ "In order to accomplish this task..."
✅ "To accomplish..."

❌ "You will need to make sure that you..."
✅ "Ensure..."
```

**Savings:** 30-50% on instructional text

#### Technique 10: Structured Bullet Points (Weight × 1.5)

**Target:** Long paragraphs, narrative text

**Transform:**

```text
❌ Before:
The system analyzes various indicators including active
initiatives, git status, test results, and session history.
Based on this comprehensive analysis, it makes a routing
decision to determine the next appropriate workflow.

✅ After:
Analyzes:
- Active initiatives
- Git status
- Test results
- Session history
→ Routes to appropriate workflow
```

**Savings:** 20-40% on process descriptions

#### Technique 11: Keyword Extraction (Weight × 1.8)

**Target:** Detailed descriptions

**Transform:**

```text
❌ "Analyze the provided documentation to identify..."
✅ "Identify from docs..."

❌ "Execute the following command in your terminal..."
✅ "Run: `command`"

❌ "Navigate to the directory where the file is located..."
✅ "Navigate to file directory..."
```

**Savings:** 15-30% on action descriptions

#### Technique 12: Example Consolidation (Weight × 2.0)

**Target:** Redundant examples, verbose demonstrations

**Strategy:**

- Keep 2-3 best examples
- Remove duplicate patterns
- Use tables for multiple examples
- Inline short examples

**Transform:**

```text
❌ Before (8 examples, 500 tokens):
Example 1: [detailed explanation]
Example 2: [detailed explanation]
...
Example 8: [detailed explanation]

✅ After (3 examples, 150 tokens):
| Pattern | Example |
|---------|----------|
| Simple | `short` |
| Moderate | `medium` |
| Complex | `detailed` |
```

**Savings:** 40-60% on examples section

#### Technique 13: Reference Externalization (Weight × 1.3)

**Target:** Inline documentation, repeated concepts

**Transform:**

```text
❌ Before: [5 paragraphs explaining task management]

✅ After: See: [12_task_orchestration.md](../rules/12_task_orchestration.md)
```

**Savings:** 50-80% on repeated concepts

### 4.4 Apply Selected Techniques

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

## Stage 5: Apply Model-Specific Enhancements

🔄 **Entering Stage 5: Apply Model-Specific Enhancements**

**Philosophy:** Add model-specific optimizations only when target model is known and enhancements won't reduce cross-model compatibility.

### 5.1 Claude-Specific Enhancements

**Apply when:** Target model is Claude 3.5+ or patterns suggest Claude

**Enhancements:**

1. **Extended Thinking Tags:**

   ```xml
   <thinking>
   [Let Claude reason through the problem]
   </thinking>
   ```

2. **Explicit XML Structure:**
   - Prefer `<instructions>`, `<context>`, `<constraints>` over markdown
   - Use detailed nested structure
   - Claude excels at parsing complex XML

3. **Detailed Reasoning Scaffolds:**
   - Add more granular reasoning steps
   - Claude benefits from explicit step breakdowns
   - Encourage self-critique and verification

### 5.2 GPT-Specific Enhancements

**Apply when:** Target model is GPT-4+ or Codex variant

**Enhancements:**

1. **Markdown Structure:**
   - Use `###` headings for sections
   - Prefer markdown over XML
   - Clear delimiter cues (`---`, triple backticks)

2. **For GPT-5-Codex specifically:**
   - **MINIMIZE prompting** ("less is more")
   - **Remove preambles** (model doesn't support them)
   - **Concise tool descriptions**
   - Focus on terminal + apply_patch tools only

3. **Structured Output Emphasis:**
   - Explicit JSON schemas
   - Code-first examples
   - Numeric constraints ("3 bullets", "under 50 words")

### 5.3 Gemini-Specific Enhancements

**Apply when:** Target model is Gemini 1.5+

**Enhancements:**

1. **System Instructions:**
   - Use dedicated system instruction section
   - Define role at system level

2. **Hierarchical Structure:**
   - Clear heading hierarchy
   - Consistent formatting throughout

3. **Long Context Optimization:**
   - Place queries at END of long contexts
   - Experiment with example quantities
   - Leverage multimodal capabilities when applicable

### 5.4 Auto Mode (No Model-Specific)

**Apply when:** Target model is `auto` or unknown

**Strategy:**

- Use **only** universal optimizations from Stage 4
- Avoid XML tags (use markdown)
- Avoid model-specific features
- Focus on GOLDEN framework compliance
- Maximum cross-model compatibility

**Print stage completion:**

```markdown
📋 **Stage 5 Complete:** Model-specific enhancements applied for [model_name]
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Model-specific enhancements applied, validating",
  plan: [
    { step: "1. /improve-prompt - Capture and parse input prompt", status: "completed" },
    { step: "2. /improve-prompt - Detect target model and context", status: "completed" },
    { step: "3. /improve-prompt - Analyze current prompt quality", status: "completed" },
    { step: "4. /improve-prompt - Apply universal optimizations", status: "completed" },
    { step: "5. /improve-prompt - Apply model-specific enhancements", status: "completed" },
    { step: "6. /improve-prompt - Validate improvements", status: "in_progress" },
    // ... rest of tasks
  ]
})
```

---

## Stage 6: Validate Improvements

🔄 **Entering Stage 6: Validate Improvements**

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

## Stage 7: Calculate Metrics

🔄 **Entering Stage 7: Calculate Quantitative Metrics**

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

## Stage 8: Present Results

🔄 **Entering Stage 8: Present Results with Analysis**

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

## Stage 9: Record Metadata (Optional)

🔄 **Entering Stage 9: Record Metadata**

**Purpose:** Track optimization runs for pattern analysis and threshold refinement.

### 9.1 Metadata Collection

**Collect and save:**

```json
{
  "run_id": "[UUID]",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "input": {
    "prompt_type": "workflow|rule|ad-hoc|system",
    "char_count": 1234,
    "word_count": 234,
    "has_examples": true|false,
    "has_structure": true|false
  },
  "detection": {
    "target_model": "claude|gpt|gemini|auto",
    "detected_model": "claude|gpt|gemini|unknown",
    "special_constraints": ["windsurf-workflow", "gpt-codex"]
  },
  "analysis": {
    "baseline_score": 6.5,
    "complexity": "low|medium|high",
    "ambiguity": "low|medium|high",
    "critical_issues": 2,
    "improvements_identified": 5
  },
  "optimizations": {
    "universal_techniques_applied": ["chain-of-thought", "constraints", "format"],
    "model_specific_applied": ["xml-structure", "extended-thinking"],
    "total_techniques": 5
  },
  "results": {
    "improved_score": 8.5,
    "improvement_delta": 2.0,
    "improvement_percent": 30.8,
    "char_count_after": 2134,
    "validation_passed": true
  },
  "performance": {
    "execution_time_seconds": 45,
    "stages_completed": 8
  }
}
```

### 9.2 Storage Location

**Save to:** `.windsurf/prompt-optimization-history.jsonl`

**Format:** JSON Lines (one JSON object per line)

**Example:**
```bash
{"run_id":"abc123","timestamp":"2025-10-21T12:00:00Z",...}
{"run_id":"def456","timestamp":"2025-10-21T14:30:00Z",...}
```

### 9.3 Analysis Queries

**Usage pattern analysis:**

```bash
# Most common prompt types
jq -s 'group_by(.input.prompt_type) | map({type: .[0].input.prompt_type, count: length})' .windsurf/prompt-optimization-history.jsonl

# Average improvement by model
jq -s 'group_by(.detection.target_model) | map({model: .[0].detection.target_model, avg_improvement: (map(.results.improvement_delta) | add / length)})' .windsurf/prompt-optimization-history.jsonl

# Most effective techniques
jq -s 'map(.optimizations.universal_techniques_applied[]) | group_by(.) | map({technique: .[0], count: length}) | sort_by(.count) | reverse' .windsurf/prompt-optimization-history.jsonl
```

### 9.4 Threshold Refinement

**Monitor and adjust:**

- **Baseline scores:** Track average to calibrate scoring
- **Improvement patterns:** Which techniques provide most value
- **Model detection accuracy:** Validate auto-detection logic
- **Execution time:** Optimize slow stages

**Print stage completion:**

```markdown
📋 **Stage 9 Complete:** Metadata recorded to prompt-optimization-history.jsonl
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
