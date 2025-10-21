---
created: "2025-10-17"
updated: "2025-10-21"
description: Generate formatted session summary from extracted data
auto_execution_mode: 3
category: Analysis
complexity: 55
tokens: 1350
dependencies:
  - extract-session
status: active
---

# Summarize Session Workflow

**Purpose:** Generate LLM-agnostic session summary using structured template and extracted data.

**Invocation:** Called by `/meta-analysis` (not standalone)

**Input:** Structured extraction data from `/extract-session`

---

## Stage 1: Task Integration

**Note:** Called by `/meta-analysis` as subtask. Parent handles task tracking.

**If called directly** (unusual):

```typescript
update_plan({
  explanation: "📝 Starting /summarize-session workflow",
  plan: [
    { step: "1. /summarize-session - Format header, objectives, work", "status": "in_progress" },
    { step: "2. /summarize-session - Add learnings, patterns, next steps", "status": "pending" },
    { step: "3. /summarize-session - Validate and write file", "status": "pending" }
  ]
})
```

---

## Template Structure & Length Constraints

### Required Sections

| Section | Min | Max | Target |
|---------|-----|-----|--------|
| 1. Header | - | - | Required |
| 2. Objectives | 2 sent | 5 sent | 3 sent |
| 3. Completed Work | 1 item | 10 items | 5 items |
| 4. Commits | - | - | All commits |
| 5. Key Learnings | 0 items | 5 items | 2-3 items |
| 6. Patterns (Positive) | 1 item | 5 items | 3 items |
| 7. Patterns (Improvements) | 0 items | 3 items | 1-2 items |
| 8. High-Priority Gaps | 0 items | 3 items | 0-1 items |
| 9. Next Steps (Critical) | 0 items | 5 items | 2-3 items |
| 10. Living Documentation | - | - | Required |
| 11. Metrics | - | - | Required |
| 12. Protocol Adherence | - | - | Required |
| 13. References | - | - | Required |
| 14. Metadata | - | - | Required |
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

```markdown
## Objectives

[2-4 sentences describing aim]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

### 3. Document Completed Work

```markdown
### 1. [Major Task Category]

[Context paragraph]

**Accomplishments:**
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

[If any:]
1. **[Category]:** [What's missing] — [Impact] — [Recommended fix]

[If none:]
None identified. Session followed standard practices.
```

### 8. Define Next Steps

```markdown
## Next Steps

### Critical (Must Address)
[If any:]
1. **[Task]:** [Description] ([File]) — [Why critical]

### High Priority
1. **[Task]:** [Description] ([File]) — [Context]
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

### 10. Add Metrics

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
- ✅ Session summary created
- ✅ Meta-analysis executed
- ✅ Timestamp updated
- ✅ All changes committed
- ✅ Tests passing
- ✅ Completed initiatives archived

[If violations, note and propose improvements]
```

### 12. Add References & Metadata

```markdown
## Session References

- **Previous session:** [filename or "None"]
- **Related initiative:** [filepath if relevant]
- **External references:** [URLs if used]

**Metadata:**
- **Session type:** [Implementation / Planning / Research / Maintenance / Mixed]
- **Autonomy level:** [High / Medium / Low]
- **Complexity:** [High / Medium / Low]
- **Quality:** ✅ [All objectives met / Partial / Issues]
```

---

## Validation Checklist

### Format Compliance

- [ ] Exact template structure
- [ ] Action verbs for accomplishments
- [ ] File/metric references
- [ ] Decisions include rationale
- [ ] Length constraints met
- [ ] No vague language

### Content Completeness

- [ ] Objectives clear
- [ ] All commits listed
- [ ] Files accounted for
- [ ] Learnings captured
- [ ] Patterns identified
- [ ] Next steps specific
- [ ] Living docs checked
- [ ] Metrics complete
- [ ] Protocol verified

### LLM-Agnostic Quality

- [ ] Another LLM could produce similar output
- [ ] Facts verifiable from git/files
- [ ] Sections length-constrained
- [ ] Language concrete
- [ ] Technical claims have evidence

---

## File Creation

### Naming Convention

```bash
# Format: YYYY-MM-DD-descriptive-name.md
docs/archive/session-summaries/2025-10-18-workflow-optimization.md

# Descriptive name: 2-4 words (kebab-case), primary focus, unique
```

### Write and Save

1. Generate summary using template
2. Validate against checklist
3. Write to `docs/archive/session-summaries/`
4. Return filename for commit

---

## Integration

**Called By:** `/meta-analysis`

**Input:** Extraction data from `/extract-session`, session metadata

**Output:** Formatted session summary file, filename for git commit

**Print exit:**

```markdown
✅ **Completed /summarize-session:** Session summary created at [filepath]
```

---

## References

- [meta-analysis.md](./meta-analysis.md) - Parent workflow
- [extract-session.md](./extract-session.md) - Data source
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md) - File location
