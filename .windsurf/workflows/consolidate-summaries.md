---
created: "2025-10-17"
updated: "2025-10-19"
description: Consolidate historical session summaries into daily comprehensive files
auto_execution_mode: 3
category: Analysis
complexity: 65
tokens: 2150
dependencies:
  - extract-session
  - summarize-session
status: active
version: 2.2.0
---

# Consolidate Session Summaries Workflow

## Purpose

Merge multiple per-session summaries from the same day into comprehensive daily summaries, reducing redundancy while maintaining critical information.

## When to Use

- Day has 5+ individual session summaries
- Quarterly documentation reviews
- Session summary proliferation reduces discoverability
- **Never** consolidate current day (allow ongoing work)

## Invocation

`/consolidate-summaries [date]` (e.g., `/consolidate-summaries 2025-10-15`)

---

## Prerequisites

1. Date must be in the past (not current day)
2. Multiple summaries exist for target date
3. No active work referencing individual summaries

---

## Stage 1: Analysis

### 1.1 Identify Target Summaries

```bash
# List summaries for target date
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md | wc -l
```

**Decision criteria:**

- 5+ summaries: Consolidate highly recommended
- 3-4 summaries: Consolidate if redundant
- 1-2 summaries: Leave as-is

### 1.2 Read and Categorize Content

⚠️ **CRITICAL:** Use batch reading for efficiency. Reading files sequentially is 7x slower.

Use [Batch Reading Pattern](../docs/context-loading-patterns.md#pattern-1-batch-reading):

```python
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/YYYY-MM-DD-*.md",
])
```

See [Batch Operations Guide](../docs/batch-operations.md#pattern-2-chunked-processing) for optimal batch sizes (10-15 files).

Extract from each: objectives, accomplishments, decisions, files modified, commits, learnings, unresolved issues, next steps

### 1.3 Check External References

```bash
grep -r "2025-10-15-specific-session.md" docs/ .windsurf/ --include="*.md"
```

Update references to consolidated summary after creation if found.

---

## Stage 2: Methodical Extraction

**CRITICAL:** Follow structured extraction for consistency.

### 2.1 Extract Information Systematically

For each summary file:

#### Step 1: Session Metadata

- Title, duration, primary focus area

#### Step 2: Context Narrative (2-3 sentences, ≤120 words)

- Objectives, constraints, triggering events
- Critical observations
- Cross-session references

#### Step 3: Accomplishments (concrete actions only)

- **[Action verb]**: [What] ([File/Component]) — [Context clause if needed]

#### Step 4: Decisions (explicit choices)

- **[Topic]**: [Decision] - [Rationale] (trade-offs/alternatives)

#### Step 5: Technical Learnings (specific insights)

- **[Technology]**: [Learning] (measurements/data)

#### Step 6: Issues (unresolved only)

- **[Component]**: [Problem] - [Why unresolved] (blockers/dependencies)

#### Step 7: Dependencies & Interactions

- Upstream/downstream work, open questions
- **Cross-session continuity**: How does this session connect to others? What themes span multiple sessions?

#### Step 8: Supporting Evidence

- Commit hashes, benchmarks, source quotes

#### Step 9: Next Steps (concrete actions)

- [ ] [Action] [task] — [Owner/dependency]

#### Step 10: Metrics

- Files modified, commits, tests, ADRs, duration

### 2.2 Create Extraction Matrix (JSON Format)

```json
{
  "date": "YYYY-MM-DD",
  "sessions": [
    {
      "title": "Session Name",
      "duration": "~2 hours",
      "focus": "testing",
      "context": "2-3 sentences preserving narrative.",
      "accomplishments": [
        {"action": "Created", "what": "Feature", "where": "file.py", "context": "Why"}
      ],
      "decisions": [
        {"topic": "Topic", "decision": "Choice", "rationale": "Why", "tradeoffs": "Alternatives"}
      ],
      "learnings": [
        {"category": "Tool", "insight": "Discovery", "measurement": "Data"}
      ],
      "issues": [
        {"area": "Component", "problem": "Issue", "reason": "Blocker", "owner": "Team"}
      ],
      "dependencies": {
        "upstream": ["ref"], "downstream": ["ref"], "notes": "Context"
      },
      "evidence": {
        "commits": ["hash"], "benchmarks": ["path"], "quotes": [{"speaker": "X", "text": "Quote"}]
      },
      "next_steps": ["Task"],
      "metrics": {
        "files_modified": 5, "commits": 3, "tests_passing": 45, "adrs_created": 1
      }
    }
  ]
}
```

---

## Stage 3: Methodical Consolidation

### 3.1 Merge Using Explicit Rules

#### Rule 1: Deduplicate Accomplishments

- Same action + same component → merge, keep specific description

#### Rule 2: Consolidate Decisions

- Same topic: Keep both if complementary, merge if elaboration

#### Rule 3: Synthesize Learnings

- Same tech: Combine, preserve measurements, note progression

#### Rule 4: Aggregate Issues

- Group by component, keep distinct issues, prioritize by frequency

#### Rule 5: Consolidate Next Steps

- Remove exact duplicates, merge overlapping, group by component, prioritize by dependency

### 3.2 Generate Consolidated Summary

**Template:**

```markdown
# Daily Summary: [Date]

- **Date:** YYYY-MM-DD
- **Total Sessions:** N
- **Duration:** ~X hours
- **Focus Areas:** [2-4 themes]
- **Major Initiatives:** [List + progress]

---

## Executive Overview

**Purpose:** Enable 30-second understanding. Each subsection should be 2-3 sentences.

**Accomplishments:** [2-3 sentences summarizing key achievements across all sessions]

**Decisions:** [2-3 sentences on critical technical/architectural decisions]

**Learnings:** [2-3 sentences on key insights and discoveries]

---

## Session Timeline

### Session 1: [Name] (~X hours)

**Context:** [2-3 sentences from extraction - situate the work]

**What Was Done:**

- [Accomplishment 1]
- [Accomplishment 2]

**Why:** [1-2 sentences linking to larger goals/initiatives]

---

## Major Accomplishments (Grouped)

**Categorization Guide:** Group by domain (Performance, Testing, Documentation, Infrastructure, Security, Configuration, Code Quality).

### [Category 1: e.g., Testing Infrastructure]

1. **[Action]**: [What] ([Component]) — [Context]
2. **[Action]**: [What] ([Component]) — [Context]

### [Category 2: e.g., Documentation]

1. **[Action]**: [What] ([Component]) — [Context]

---

## Architectural & Technical Decisions

### [Decision Topic 1]
   - **Decision:** [What was chosen]
   - **Rationale:** [Why; alternatives considered/rejected]
   - **Impact:** [Effect with metrics]
   - **Follow-up:** [Actions if any]

---

## Key Learnings

### Technical Insights
1. **[Technology]:** [Insight with measurements]
2. **[Technology]:** [Insight with measurements]

### Process Improvements
1. **[Process]:** [Learning, triggering event]

---

## Cross-Session Dynamics

**Purpose:** Synthesize patterns across sessions that aren't visible in individual summaries. HIGH VALUE section.

**Continuity Threads:**

- [Initiative/Theme]: [How sessions connected, progression]
  - Session X: [Contribution]
  - Session Y: [Contribution]

**Unblocked Work:**

- Session X ([What]) → Enabled [downstream work]

**Outstanding Questions:**

- [Question]? (Requires [what])

---

## Metrics (Cumulative)

| Metric | Count | Details |
|--------|-------|----------|
| Files Modified | N | [List if ≤5] |
| Commits | N | [Hashes if ≤5] |
| Tests Passing | N | [Context] |
| Tests Failing | N | [Issues + owners] |
| ADRs Created | N | [Titles] |
| Initiatives Updated | N | [Names + progress] |
| Total Duration | ~N hours | [Breakdown] |

---

## Unresolved Issues

### [Component 1]
- **Issue:** [Problem]
- **Reason:** [Why unresolved]
- **Owner:** [Team]
- **Priority:** [High/Med/Low]

---

## Next Steps (Prioritized)

### Immediate (Next Session)
- [ ] [Task 1] — [Owner]
- [ ] [Task 2] — [Owner]

### Short-term (This Week)
- [ ] [Task 3] — [Owner]

### Future Considerations
- [ ] [Task 4] — [Context]

---

## Supporting Evidence Index

- **Commits:** [Hash → description + initiative]
- **Benchmarks:** [Files/links with context]
- **Key Quotes:** [Speaker → "Quote" (source)]

---

## Metadata

**Original Sessions:**
- `YYYY-MM-DD-session1.md` → Session 1 above
- `YYYY-MM-DD-session2.md` → Session 2 above

**Consolidation Method:** Structured extraction + merge rules
**Workflow Version:** 2.1.0
```

---

## Stage 4: Quality Validation

### 4.1 Validation Checklist

**Information Preservation:**

```markdown
For EACH original summary:
  ✓ All accomplishments captured
  ✓ All decisions documented
  ✓ All learnings preserved
  ✓ All issues listed
  ✓ All next steps included
  ✓ All metrics aggregated
```

**Format Compliance:**

```markdown
  ✓ Template structure followed
  ✓ No vague statements
  ✓ Action verbs consistent
  ✓ File references included
  ✓ Measurements preserved
  ✓ Tables formatted
  ✓ Checkboxes use [ ]
```

**Content Quality:**

```markdown
  ✓ Executive overview ≤3 sentences
  ✓ Accomplishments specific
  ✓ Decisions include rationale
  ✓ Learnings include measurements
  ✓ Issues explain why unresolved
  ✓ Next steps concrete
  ✓ No duplicates
```

### 4.2 LLM-Agnostic Verification

1. Can another person reconstruct day's work? → Add context if no
2. Are metrics verifiable from git/files? → Correct if no
3. Could any LLM following rules produce this? → Add constraints if no
4. Is every accomplishment verifiable? → Add details if no
5. Would ChatGPT/Claude/Gemini produce similar output? → Tighten instructions if no

---

## Stage 5: Implementation

### 5.1 Create Consolidated Summary

```bash
docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
```

### 5.2 Write Content

1. Copy template from Stage 3.2
2. Fill extracted/consolidated information
3. Follow template exactly
4. Do not skip sections (use "None" if empty)

### 5.3 Verify Content

Run validation checklist (Stage 4.1) line by line

### 5.4 Remove Original Files

⚠️ **CRITICAL SAFETY:** Do NOT delete consolidated summary.

**After validation:**

```bash
# List files to be deleted (verify before running)
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md | grep -v "daily-summary"

# Remove originals (EXCLUDES daily-summary.md)
find docs/archive/session-summaries -name "YYYY-MM-DD-*.md" ! -name "*daily-summary.md" -delete
```

**Validation:** Ensure consolidated summary exists and is complete before deletion.

See [Error Handling Pattern](../docs/batch-operations.md#pattern-4-error-handling-in-batches) for safe file operations.

### 5.5 Update References

```bash
grep -r "YYYY-MM-DD-session" docs/ .windsurf/ --include="*.md"
```

Update each to `YYYY-MM-DD-daily-summary.md`

---

## Stage 6: Final Verification

### 6.1 Automated Checks

```bash
task lint:docs
markdown-link-check docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
```

### 6.2 Manual Checks

**Completeness:**

- [ ] All sessions in timeline
- [ ] All commits in metrics
- [ ] All decisions with rationale
- [ ] All learnings with measurements
- [ ] All issues with reasons

**Format:**

- [ ] Template followed
- [ ] Tables formatted
- [ ] No vague language
- [ ] Checkboxes use [ ]
- [ ] File paths backticked

**Clean-up:**

- [ ] Originals deleted
- [ ] No broken references
- [ ] Metadata correct

### 6.3 Git Commit

```bash
git add docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
git commit -m "docs(archive): consolidate YYYY-MM-DD session summaries

- Created comprehensive daily summary
- Archived N individual summaries
- Updated references
- Preserved all critical information"
```

---

## Best Practices

### DO

✅ Wait 24-48 hours after date before consolidating
✅ Preserve unique insights
✅ Cross-reference initiatives
✅ Include metrics
✅ Cite original sources
✅ Update external references

### DON'T

❌ Don't consolidate current day
❌ Don't omit unresolved issues
❌ Don't delete originals until verified
❌ Don't lose commit history
❌ Don't skip reference updates

---

## Success Criteria

- [ ] Single consolidated summary created
- [ ] All unique information preserved
- [ ] Original summaries removed after verification
- [ ] All references updated
- [ ] Markdown linting passes
- [ ] Git commit completed

---

## References

- [CONSTITUTION.md](../../docs/CONSTITUTION.md)
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md)
- [ADR-0003](../../docs/adr/0003-documentation-standards-and-structure.md)

---

## Changelog

### v2.2.0 (2025-10-19)

**Improvements based on 2025-10-16 consolidation fitness analysis:**

1. **Batch reading emphasis** - Added CRITICAL callout (7x performance impact)
2. **Cross-session dynamics** - Enhanced template guidance (HIGH VALUE section)
3. **Session timeline format** - Standardized "What Was Done" / "Why" structure
4. **Executive overview clarity** - Clarified 2-3 sentences per subsection
5. **File removal safety** - Added explicit exclusion for daily-summary.md
6. **Grouped accomplishments** - Added categorization guide
7. **Cross-session continuity** - Added to Step 7 extraction process

**Validation:**

- Tested on 2025-10-16 (7 sessions → 1 file)
- Information preservation: 95%+
- Compression ratio: 71% line reduction, 52% size reduction
- Quality score: 9/10 discoverability

---

**Version:** 2.2.0 (Enhanced with fitness analysis improvements, Oct 2025)
