---
description: Meta-analysis workflow for continuous AI agent improvement
auto_execution_mode: 3
---

# Meta-Analysis Workflow

**Purpose:** Systematically analyze long AI agent sessions to identify improvement opportunities in rules, documentation, workflows, and processes.

**When to use:** At the end of significant work sessions (2+ hours) or after completing major initiatives.

**Idempotency:** Designed to avoid low-value additions. Only suggests changes when gaps are clearly identified.

---

## Stage 1: Session Analysis (Required)

### 1.1 Review Interaction Patterns

Analyze the current session for:

- **Tool Usage Patterns:**
  - Which tools were used most frequently?
  - Were there inefficient tool call sequences?
  - Were there missing tools that would have helped?
  - Did the agent struggle with any tool parameters?

- **Workflow Usage:**
  - Which workflows were invoked?
  - Were workflows clear and comprehensive?
  - Were there repeated manual processes that should be workflows?

- **Rule Adherence:**
  - Did the agent follow all rules correctly?
  - Were rules ambiguous or contradictory?
  - Were there situations where rules were missing?

- **Documentation Gaps:**
  - What information did the agent need to search for repeatedly?
  - Were there missing code examples or references?
  - Was existing documentation unclear?

### 1.2 Identify Problem Patterns

Look for:

- **Repeated mistakes** (same issue multiple times)
- **Inefficient approaches** (agent took long route when shortcut exists)
- **Knowledge gaps** (agent lacked domain-specific information)
- **Process friction** (manual steps that could be automated)
- **Quality issues** (bugs introduced, tests not run until late)

---

## Stage 2: Gap Analysis (Required)

### 2.1 Categorize Findings

Group identified issues into categories:

1. **Rule Improvements:**
   - Missing rules (new guidance needed)
   - Ambiguous rules (needs clarification)
   - Conflicting rules (needs resolution)
   - Outdated rules (needs update)

2. **Documentation Needs:**
   - Missing technical reference
   - Missing code examples
   - Unclear existing documentation
   - Missing external references

3. **Workflow Opportunities:**
   - Repeated manual processes
   - Complex multi-step operations
   - Common debugging/testing patterns
   - Quality gate enforcement

4. **Tooling Gaps:**
   - Missing automation
   - Inefficient existing tools
   - Configuration improvements

### 2.2 Prioritize by Impact

For each finding, assess:

- **Frequency:** How often does this issue occur?
- **Impact:** How much time/quality does it cost?
- **Scope:** Does this affect one task or many?
- **Effort:** How hard is it to fix?

**Priority formula:** `(Frequency × Impact × Scope) / Effort`

---

## Stage 3: Implementation Planning (Conditional)

**Only proceed if high-priority gaps were identified.**

### 3.1 Create Implementation Plan

For each high-priority item:

1. **Define the fix:**
   - What exactly needs to change?
   - Where does it go (which file/section)?
   - What's the success criterion?

2. **Check for conflicts:**
   - Does this contradict existing guidance?
   - Will this create new problems?
   - Is there a simpler solution?

3. **Draft the content:**
   - Write clear, specific guidance
   - Include examples where helpful
   - Use AI-friendly language (see Stage 4)

### 3.2 Validation Checks

Before implementing, verify:

- [ ] Does not duplicate existing content
- [ ] Does not conflict with established patterns
- [ ] Provides clear, actionable guidance
- [ ] Includes examples or references
- [ ] Uses proper formatting and structure

---

## Stage 4: AI-Friendly Content Guidelines

When creating or updating content for AI agents:

### 4.1 Language Clarity

**DO:**
- Use active voice and imperative mood
- Be specific and explicit (avoid "typically", "usually")
- Use consistent terminology
- Number steps in procedures
- Define acronyms on first use

**DON'T:**
- Use vague qualifiers ("might", "could", "should consider")
- Assume implied context
- Use jargon without explanation
- Create circular references
- Use ambiguous pronouns

### 4.2 Structure

**Effective Patterns:**
- **Hierarchical:** Clear heading structure (H1 → H2 → H3)
- **Sequential:** Numbered steps for procedures
- **Categorical:** Grouped related concepts
- **Exemplar:** Show, don't just tell (code examples)
- **Referenced:** Link to authoritative sources

**Ineffective Patterns:**
- Long prose paragraphs without structure
- Mixing multiple concepts in one section
- Missing context or prerequisites
- Nested conditionals without clear logic
- Inconsistent formatting

### 4.3 Content Types

**Rules (`.windsurf/rules/`):**
```markdown
# Imperative statement

## Context
Why this rule exists

## Directive
Exactly what to do (MUST/SHOULD/MAY per RFC 2119)

## Examples
Concrete code/command examples

## References
Links to official documentation
```

**Workflows (`.windsurf/workflows/`):**
```markdown
---
description: Short action phrase
---

# Workflow Name

## Prerequisites
What must be true to start

## Steps
1. Specific action with example
2. Next action with expected result
...

## Verification
How to confirm success

## Troubleshooting
Common issues and fixes
```

**Documentation (`docs/`):**
```markdown
# Topic

## Overview
High-level summary (2-3 sentences)

## Key Concepts
Essential terms and relationships

## Implementation
How to use (with examples)

## Common Patterns
Typical use cases

## References
External authoritative sources with URLs
```

---

## Stage 5: Execution (Conditional)

**Only execute if validation passed and user approved plan.**

### 5.1 Implement Changes

For each approved item:

1. Create/update the file
2. Follow the appropriate template (Stage 4.3)
3. Test the change (if applicable)
4. Document the rationale

### 5.2 Cross-Reference Updates

When adding new content:

- [ ] Update related rules that reference this topic
- [ ] Add to relevant workflow where applicable
- [ ] Link from documentation structure
- [ ] Update any indexes or navigation

### 5.3 Commit Strategy

Group related changes:

```bash
git add .windsurf/rules/
git commit -m "docs(rules): add guidance for [specific topic]

- Add [specific rule]
- Clarify [specific ambiguity]
- Update [outdated reference]

Rationale: [why this improves agent performance]"
```

---

## Stage 6: Output Summary (Required)

Generate a structured summary:

### Changes Made

```markdown
## Meta-Analysis Summary

### Session Scope
- Duration: [X hours]
- Major tasks: [list]
- Files changed: [count]
- Commits: [count]

### Identified Patterns
[List key patterns observed]

### High-Priority Gaps
[List items that WERE fixed]

### Deferred Items
[List low-priority items NOT worth fixing now]

### Changes Implemented
[Detailed list of actual changes with rationale]

### Verification
[How to verify improvements in future sessions]

### Recommendations for Next Session
[Specific action items for user or future agents]
```

---

## Anti-Patterns to Avoid

**DO NOT:**

1. **Create documentation for rare edge cases**
   - Only document patterns that occur 3+ times

2. **Add rules that restate obvious best practices**
   - Don't write "Always use descriptive variable names"
   - Do write "Use verb_noun format for function names (e.g., `fetch_url`, `parse_html`)"

3. **Create workflows for one-off operations**
   - Workflows are for repeated patterns (5+ uses)

4. **Duplicate existing guidance in multiple places**
   - Link to canonical source instead

5. **Write vague or aspirational rules**
   - "Be thorough" ❌
   - "Run `task test:fast` after modifying test files" ✅

6. **Add content without clear success criteria**
   - Every addition should have measurable benefit

---

## Success Metrics

Track improvement over time:

- **Efficiency:** Time from task start to completion
- **Quality:** Tests passing first try, linting issues
- **Autonomy:** Frequency of user clarification requests
- **Correctness:** Bugs introduced vs. fixed
- **Coverage:** Percentage of known patterns documented

---

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/en/v1.0.0/)
- [RFC 2119 - Key words for use in RFCs](https://www.ietf.org/rfc/rfc2119.txt)
- [Google Technical Writing Style Guide](https://developers.google.com/tech-writing)
- [The Documentation System (Diátaxis)](https://diataxis.fr/)
- [Coding Guidelines for AI Agents](https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/)

---

**Last Updated:** October 15, 2025
**Version:** 1.0
