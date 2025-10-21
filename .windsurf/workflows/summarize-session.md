---
created: "2025-10-17"
updated: "2025-10-21"
description: Generate formatted session summary from extracted data
auto_execution_mode: 3
category: Analysis
complexity: 55
tokens: 1000
dependencies:
  - extract-session
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Summarize Session Workflow

Generate LLM-agnostic session summary using structured template.

**Called by:** `/meta-analysis`
**Input:** Extraction data from `/extract-session`

---

## Template Structure & Constraints

| Section | Min | Max | Target |
|---------|-----|-----|--------|
| Header | - | - | Required |
| Objectives | 2 sent | 5 sent | 3 sent |
| Completed Work | 1 | 10 items | 5 items |
| Commits | - | - | All |
| Learnings | 0 | 5 items | 2-3 |
| Patterns (+) | 1 | 5 items | 3 |
| Patterns (\!) | 0 | 3 items | 1-2 |
| Gaps | 0 | 3 items | 0-1 |
| Next Steps | 0 | 5 items | 2-3 |
| Living Docs | - | - | Required |
| Metrics | - | - | Required |
| Protocol | - | - | Required |
| **Total** | 1000w | 3000w | 1500-2000w |

---

## Generation Process

### 1. Header

```markdown
# Session Summary: [Title]

**Date:** YYYY-MM-DD
**Duration:** ~N hours
**Focus:** [Primary]
**Workflows Used:** [List or "None"]
```

### 2. Objectives

```markdown
## Objectives

[2-4 sentences]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

### 3. Completed Work

```markdown
### 1. [Task Category]

[Context]

**Accomplishments:**
- **[Action]**: [What] ([File]) — [Context]

**Key findings:** [Discoveries]
```

### 4. Commits

```markdown
## Commits

- `abc1234` - feat(scope): description

**Quality:** [Assessment]
```

### 5. Learnings

```markdown
## Key Learnings

### Technical
1. **[Tech]:** [Insight with measurements]

### Process
1. **[Process]:** [What learned]
```

### 6. Patterns

```markdown
## Identified Patterns

### ✅ Positive
1. **[Pattern]:** [Description] — [Why] — [When]

### ⚠️ Improvements
1. **[Issue]:** [What] — [Why] — [Better]
```

### 7. Gaps

```markdown
## High-Priority Gaps

[If any:]
1. **[Category]:** [Missing] — [Impact] — [Fix]

[Else:] None identified.
```

### 8. Next Steps

```markdown
## Next Steps

### Critical
1. **[Task]:** [Description] ([File]) — [Why]

### High Priority
1. **[Task]:** [Description]
```

### 9. Living Docs

```markdown
## Living Documentation

**PROJECT_SUMMARY.md:** [Updated/No update/Recommended] — [Reason]
**CHANGELOG.md:** [Status] — [Reason]
```

### 10. Metrics

```markdown
## Metrics

| Metric | Value |
|--------|-------|
| Duration | ~Nh |
| Commits | N |
| Files | N |
| Tests | N |
| Coverage | N% |
```

### 11. Protocol

```markdown
## Workflow Adherence

**Session End Protocol:**
- ✅ Summary created
- ✅ Meta-analysis executed
- ✅ Timestamp updated
- ✅ All committed
- ✅ Tests passing
- ✅ Initiatives archived

[If violations, note]
```

### 12. References

```markdown
## Session References

- **Previous:** [filename or "None"]
- **Related initiative:** [path]
- **External:** [URLs]

**Metadata:**
- **Type:** [Implementation/Planning/Research/Mixed]
- **Autonomy:** [High/Medium/Low]
- **Complexity:** [High/Medium/Low]
- **Quality:** ✅ [All met/Partial/Issues]
```

---

## Validation

- [ ] Template structure
- [ ] Action verbs
- [ ] File/metric refs
- [ ] Decisions have rationale
- [ ] Length constraints
- [ ] No vague language
- [ ] All commits listed
- [ ] Learnings captured
- [ ] LLM-agnostic (verifiable facts)

---

## File Creation

**Naming:** `YYYY-MM-DD-descriptive-name.md` (2-4 words, kebab-case, unique)

**Path:** `docs/archive/session-summaries/`

---

## References

- `meta-analysis.md`, `extract-session.md`, `DOCUMENTATION_STRUCTURE.md`
