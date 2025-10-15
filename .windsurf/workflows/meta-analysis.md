---
description: Systematic session review and improvement identification
auto_execution_mode: 3
---

# Meta-Analysis Workflow

**Purpose:** Systematically analyze AI agent sessions to identify improvement opportunities and create session summaries.

**When to invoke:** Automatically at end of work sessions via `/work` workflow.

**Critical Rules:**

1. **Always create session summary** in `docs/archive/session-summaries/YYYY-MM-DD-description.md`
2. **Never create summary documents** outside session-summaries directory
3. **Never add historical context** to live documentation (except ADRs)
4. **Keep summaries concise** - focus on key decisions and learnings
5. **Use consistent format** - see docs/standards/SUMMARY_STANDARDS.md

---

## Stage 0: Self-Monitoring (AUTOMATIC)

**Purpose:** Detect if meta-analysis is being run correctly and on schedule.

### 0.1 Check Last Execution

Read timestamp file to detect if meta-analysis is being run regularly:

```bash
# Check if .windsurf/.last-meta-analysis exists
cat .windsurf/.last-meta-analysis 2>/dev/null || echo "NEVER"
```

**Warning triggers:**

- File doesn't exist → Meta-analysis never run before
- Timestamp >24 hours old → Overdue for meta-analysis
- Multiple commits since last run → Protocol violation likely

### 0.2 Create/Update Timestamp

Update timestamp file when meta-analysis runs:

```bash
# Write current timestamp
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis
git add .windsurf/.last-meta-analysis
# Will be committed with session summary
```

### 0.3 Protocol Violation Detection

**Check for common violations:**

- Session summary not created in proper location
- Meta-analysis not run after work session completion
- Timestamp file not updated

**If violation detected:**

1. Document in session summary "Critical Improvements" section
2. Propose workflow fixes
3. Flag for immediate attention

---

## Stage 1: Create Session Summary (REQUIRED)

### 1.1 Summary Location and Naming

**CRITICAL:** Always create in `docs/archive/session-summaries/YYYY-MM-DD-description.md`

**Never create:**

- Summary documents in `docs/` root
- Files like `CURRENT_WORK_STATUS.md`, `SESSION_NOTES.md`
- Historical content in live documentation

**Naming format:** `YYYY-MM-DD-brief-description.md`

- Use actual date (not placeholder)
- 2-5 words for description
- Hyphenated lowercase

### 1.2 Summary Content (Concise Format)

**Required sections:**

1. **Header** - Date, duration, focus
2. **Objectives** - What was the goal
3. **Completed** - What was achieved (bullet list)
4. **Commits** - List commit hashes and messages
5. **Key Learnings** - 2-3 most important insights
6. **Next Steps** - What's queued for next session

**Keep it concise:**

- Total length: 200-400 lines (not 1000+)
- Focus on decisions and learnings
- Avoid repeating what's in commits
- No verbose explanations

### 1.3 Validate Context-Friendly Format

**CRITICAL:** Session summaries must enable cross-session context detection.

**Validation checklist for "Next Steps" section:**

- [ ] **Specific file paths** - Not "fix the tests" but "Fix tests in tests/unit/test_security.py"
- [ ] **Initiative links** - Reference active initiatives by full path
- [ ] **Commands included** - Exact commands to run (e.g., `task test:security`)
- [ ] **Priority indicators** - Use 🔴🟡🟢⚪ emojis for clarity
- [ ] **No assumptions** - Readable without prior conversation context
- [ ] **Continuation points** - Clear what phase/step to resume

**Test:** Could a new AI agent pick up work from this summary alone?

**Good example:**

```markdown
## Next Steps

1. 🔴 **Critical:** Fix 4 async test timeouts in `tests/unit/test_security.py`
   - Tests: `test_rate_limit_concurrent`, `test_consumption_limits_async`
   - Command: `task test:security`

2. 🟡 **High:** Continue docs/initiatives/active/quality-foundation.md Phase 2
   - Tasks: Install markdownlint-cli2, configure Vale
   - Estimated: 1-2 hours
```

**Bad example:**

```markdown
## Next Steps

1. Continue the work from earlier
2. Fix remaining issues
3. Complete the feature
```

### 1.4 Identify Critical Improvements

**Focus only on:**

- **Protocol violations** - Meta-analysis not run, Session End Protocol skipped
- **Documentation pollution** - Summary docs created outside proper location
- **Workflow gaps** - Missing automation that caused friction
- **Rule violations** - Agent didn't follow established rules
- **Commit patterns** - Not committing frequently enough
- **Context detection failures** - Summary lacked cross-session continuity info

**Ignore:**

- Minor inefficiencies
- One-time issues
- Already-documented patterns
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
