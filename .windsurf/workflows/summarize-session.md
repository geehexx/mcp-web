---
created: "2025-10-17"
updated: "2025-10-18"
description: Generate formatted session summary from extracted data
auto_execution_mode: 3
category: Analysis
complexity: 55
tokens: 1430
dependencies:
  - extract-session
status: active
---

# Summarize Session Workflow

**Purpose:** Generate LLM-agnostic session summary using structured template and extracted session data.

**Invocation:** Called by `/meta-analysis` (not standalone)

**Input:** Structured extraction data from `/extract-session`

---

## Stage 0: Workflow Entry

🔄 **Entering /summarize-session:** Generate formatted session summary

**Print workflow entry announcement:**

```markdown
🔄 **Entering /summarize-session:** Creating structured LLM-agnostic session summary
```

---

## Stage 1: Task Integration

**Note:** This workflow is called by `/meta-analysis` as a subtask. Parent workflow handles task tracking.

**If called directly** (unusual), create plan:

```typescript
update_plan({
  explanation: "📝 Starting /summarize-session workflow",
  plan: [
    { step: "1. /summarize-session - Format header and objectives", status: "in_progress" },
    { step: "2. /summarize-session - Document completed work and commits", status: "pending" },
    { step: "3. /summarize-session - Add learnings and patterns", status: "pending" },
    { step: "4. /summarize-session - Define next steps and metrics", status: "pending" },
    { step: "5. /summarize-session - Validate and write file", status: "pending" }
  ]
})
```

---

## Template Structure

### Required Sections

1. **Header** - Date, duration, focus, workflows
2. **Objectives** - What session aimed to accomplish
3. **Completed** - Major task categories with accomplishments
4. **Commits** - List of commits with quality assessment
5. **Key Learnings** - Technical insights and process observations
6. **Identified Patterns** - Positive patterns and areas for improvement
7. **High-Priority Gaps** - Critical issues (if any)
8. **Next Steps** - Critical and high priority tasks
9. **Living Documentation** - Update status for PROJECT_SUMMARY and CHANGELOG
10. **Metrics** - Quantitative session data
11. **Workflow Adherence** - Session End Protocol compliance
12. **Session References** - Links to related docs
13. **Metadata** - Session type, autonomy, complexity, quality

---

## Length Constraints

| Section | Min | Max | Target |
|---------|-----|-----|--------|
| Objectives | 2 sent | 5 sent | 3 sent |
| Task narrative | 2 sent | 4 sent | 3 sent |
| Accomplishments | 1 item | 10 items | 5 items |
| Technical Insights | 0 items | 5 items | 2-3 items |
| Positive Patterns | 1 item | 5 items | 3 items |
| Areas for Improvement | 0 items | 3 items | 1-2 items |
| High-Priority Gaps | 0 items | 3 items | 0-1 items |
| Next Steps (Critical) | 0 items | 5 items | 2-3 items |
| **Total Length** | 1000 words | 3000 words | 1500-2000 words |

---

## Generation Process

### 1. Format Header

```markdown
# Session Summary: [Descriptive Title]

**Date:** YYYY-MM-DD
**Duration:** ~N hours
**Focus:** [Primary focus from extraction]
**Workflows Used:** [List or "None (ad-hoc)"]
```

### 2. Write Objectives

**From extraction data:**

- What was the triggering context?
- What were the success criteria?
- Was this a continuation or new work?

**Format:**

```markdown
## Objectives

[2-4 sentences describing aim]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

### 3. Document Completed Work

**Group accomplishments by category:**

```markdown
### 1. [Major Task Category]

[Context paragraph]

**Accomplishments:**
- **[Action]**: [Specific accomplishment] ([File]) — [Context]
- **[Action]**: [Specific accomplishment] ([File]) — [Context]

**Key findings:** [Discoveries]
```

### 4. List Commits

```markdown
## Commits

- `abc1234` - feat(scope): description
- `def5678` - fix(scope): description

**Commit quality:** [Assessment]
```

### 5. Document Learnings

```markdown
## Key Learnings

### Technical Insights

1. **[Technology]:** [Insight with measurements]
[If none: "No significant technical insights (routine work)"]

### Process Observations

1. **[Process]:** [What was learned]
[If none: "No process insights this session"]
```

### 6. Identify Patterns

```markdown
## Identified Patterns

### ✅ Positive Patterns

1. **[Pattern]:** [Description] — [Why worked] — [When: Always/Often/Sometimes]

### ⚠️ Areas for Improvement

[If any:]
1. **[Issue]:** [What happened] — [Why suboptimal] — [Better approach]
```

### 7. Flag Critical Gaps

```markdown
## High-Priority Gaps

[If any critical issues:]
1. **[Category]:** [What's missing] — [Impact] — [Recommended fix]

[If none:]
None identified. Session followed standard practices.
```

### 8. Define Next Steps

```markdown
## Next Steps

### Critical (Must Address)

[If any:]
1. **[Task]:** [Description] ([File reference]) — [Why critical]

### High Priority

1. **[Task]:** [Description] ([File reference]) — [Context]
2. **[Task]:** [Description] ([File reference]) — [Context]

### Medium Priority

[Optional - only if relevant]
```

### 9. Check Living Documentation

```markdown
## Living Documentation

### PROJECT_SUMMARY.md

**Status:** [Updated / No update needed / Update recommended]
**Reason:** [Why updated or why not]

### CHANGELOG.md

**Status:** [Updated / No update needed / Update recommended]
**Reason:** [Why updated or why not]
```

### 10. Add Metrics Table

```markdown
## Metrics

| Metric | Value |
|--------|-------|
| Duration | ~N hours |
| Commits | N |
| Files Modified | N |
| Lines Added | +N |
| Lines Removed | -N |
| Tests Added | N |
| Coverage | N% |
```

### 11. Document Protocol Adherence

```markdown
## Workflow Adherence

**Session End Protocol:**
- ✅ Session summary created in proper location
- ✅ Meta-analysis executed
- ✅ Timestamp updated
- ✅ All changes committed
- ✅ Tests passing
- ✅ Completed initiatives archived

[If violations, note and propose improvements]
```

### 12. Add References

```markdown
## Session References

- **Previous session:** [filename or "None"]
- **Related initiative:** [filepath if relevant]
- **External references:** [URLs if used]
```

### 13. Add Metadata

```markdown
**Metadata:**
- **Session type:** [Implementation / Planning / Research / Maintenance / Mixed]
- **Autonomy level:** [High / Medium / Low]
- **Complexity:** [High / Medium / Low]
- **Quality:** ✅ [All objectives met / Partial / Issues]
```

---

## Validation Checklist

Before finalizing:

### Format Compliance

- [ ] Exact template structure followed
- [ ] YAML frontmatter correct
- [ ] All accomplishments use action verbs
- [ ] All accomplishments reference files/metrics
- [ ] All decisions include rationale
- [ ] Length constraints met
- [ ] Tables formatted correctly
- [ ] No vague language

### Content Completeness

- [ ] Objectives clearly stated
- [ ] All commits listed
- [ ] All files modified accounted for
- [ ] Key learnings captured
- [ ] Patterns identified
- [ ] Next steps are specific
- [ ] Living documentation checked
- [ ] Metrics table complete
- [ ] Protocol compliance verified

### LLM-Agnostic Quality

- [ ] Another LLM could produce similar output
- [ ] All facts verifiable from git/files
- [ ] Sections constrained to specified lengths
- [ ] Language concrete, not vague
- [ ] Technical claims supported by evidence

---

## File Creation

### Naming Convention

```bash
# Format: YYYY-MM-DD-descriptive-name.md
docs/archive/session-summaries/2025-10-18-workflow-optimization.md

# Descriptive name:
# - 2-4 words (kebab-case)
# - Indicates primary focus
# - Unique for the day
```

### Write and Save

1. Generate summary using template
2. Validate against checklist
3. Write to file in proper location
4. Return filename for commit

---

## Integration

### Called By

- `/meta-analysis` - Primary caller

### Input

- Extraction data from `/extract-session`
- Session metadata

### Output

- Formatted session summary file
- Filename for git commit

**Print workflow exit:**

```markdown
✅ **Completed /summarize-session:** Session summary created at [filepath]
```

---

## References

- `.windsurf/workflows/meta-analysis.md` - Parent workflow
- `.windsurf/workflows/extract-session.md` - Data source
- `docs/DOCUMENTATION_STRUCTURE.md` - File location requirements
