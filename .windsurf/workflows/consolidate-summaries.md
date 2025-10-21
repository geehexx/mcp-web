---
created: "2025-10-17"
updated: "2025-10-19"
description: Consolidate historical session summaries into daily comprehensive files
auto_execution_mode: 3
category: Analysis
complexity: 70
tokens: 5758
dependencies:
  - extract-session
  - summarize-session
status: active
version: 2.3.0
---

# Consolidate Session Summaries Workflow

## Purpose

Merge multiple per-session summaries from same day into comprehensive daily summaries. Reduces redundancy, preserves critical information.

---

## Usage

**Invocation:** `/consolidate-summaries [date]` (e.g., `/consolidate-summaries 2025-10-15`)

**When to use:**

- 5+ summaries in single day
- Quarterly documentation reviews
- **Never:** Current day (allow ongoing work)

**Prerequisites:**

- Date in past (not today)
- Multiple summaries exist
- No active work references

**Task plan:**

```typescript
update_plan({
  explanation: "📋 Starting /consolidate-summaries",
  plan: [
    { step: "1. /consolidate-summaries - Identify and analyze targets", status: "in_progress" },
    { step: "2. /consolidate-summaries - Extract information systematically", status: "pending" },
    { step: "3. /consolidate-summaries - Apply consolidation rules", status: "pending" },
    { step: "4. /consolidate-summaries - Validate and create consolidated summary", status: "pending" },
    { step: "5. /consolidate-summaries - Delete originals and commit", status: "pending" }
  ]
})
```

---

## Stage 1: Analysis

### 1.1 Identify & Read Targets

```bash
# Count summaries
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md | wc -l
```

**Decision:** 5+ → Consolidate | 3-4 → If redundant | 1-2 → Skip

**Batch read (CRITICAL - 7x faster):**

```typescript
mcp0_read_multiple_files([
  "docs/archive/session-summaries/YYYY-MM-DD-*.md"
])
```

See: [07_context_optimization.md](../rules/07_context_optimization.md), [15_tool_patterns.md](../rules/15_tool_patterns.md)

**Extract:** objectives, accomplishments, decisions, files, commits, learnings, issues, next steps

### 1.2 Check References

```bash
grep -r "2025-10-15-specific-session.md" docs/ .windsurf/ --include="*.md"
```

Update references after consolidation.

---

## Stage 2: Structured Extraction

**Extract from each summary (10 steps):**

| Step | Extract | Format |
|------|---------|--------|
| 1 | Metadata | Title, duration, focus |
| 2 | Context | 2-3 sentences (≤120 words), objectives, observations |
| 3 | Accomplishments | **[Verb]**: [What] ([File]) — [Context] |
| 4 | Decisions | **[Topic]**: [Decision] - [Rationale] (trade-offs) |
| 5 | Learnings | **[Tech]**: [Learning] (measurements) |
| 6 | Issues | **[Component]**: [Problem] - [Why unresolved] |
| 7 | Dependencies | Upstream/downstream, cross-session continuity |
| 8 | Evidence | Commits, benchmarks, quotes |
| 9 | Next Steps | - [ ] [Action] — [Owner] |
| 10 | Metrics | Files, commits, tests, ADRs, duration |

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

## Stage 2.5: Action Item Extraction (Optional)

**Purpose:** Mine summaries for initiatives (pain points, gaps, regressions, improvements)
**When:** Quarterly reviews, initiative planning

### Process (5 Steps)

| Step | Action | Output |
|------|--------|--------|
| 1 | **Read sections** | Accomplishments → workarounds<br>Decisions → constraints<br>Learnings → gaps<br>Issues → pain points<br>Next Steps → deferred work |
| 2 | **Identify types** | Pain Points, Missing Capabilities, Regressions, Improvements |
| 3 | **Categorize** | workflow, testing, docs, security, performance, automation, infra, quality |
| 4 | **Track source** | File, section, quote |
| 5 | **Score** | Impact: high/medium/low<br>Confidence: high (3+ mentions)/medium/low |

### YAML Template

```yaml
action_items:
  - id: "YYYY-MM-DD#section#N"
    title: "Title (5-10 words)"
    category: "workflow"  # Step 3 categories
    impact: "high"  # high | medium | low
    confidence: "high"  # high | medium | low
    source: {file, section, quote, date}
    context: {related_files, related_initiatives}
    mapping: {suggested_initiative, create_new_initiative}
```

### Cross-Reference Validation (HIGH impact+confidence only)

1. Check active initiatives: `ls -1 docs/initiatives/active/*/initiative.md`
2. Categorize:
   - **A:** Already covered → Mark `suggested_initiative`
   - **B:** Gap in existing → Add to initiative
   - **C:** New needed → Mark `create_new_initiative: true`
   - **D:** Low priority → Backlog only
3. Group Category C items by theme → Propose new initiatives

### Output Format

Create two files:

**1. Action Items Extract:** `YYYY-MM-DD-action-items.yaml`

```yaml
extraction_date: "2025-10-19"
summaries_analyzed: 21
action_items: [... items from 2.5.2 ...]
```

**2. Gap Analysis:** `YYYY-MM-DD-gap-analysis.md`

```markdown
# Gap Analysis: Oct 15-19 Summaries

## Summary
- Total action items: 45
- High impact + high confidence: 12
- Already covered: 5
- Gaps in existing initiatives: 4
- New initiatives needed: 3

## Category A: Already Covered (5 items)
- [Item 1] → Performance Optimization (Phase 2 includes this)
- ...

## Category B: Gaps to Address (4 items)
- [Item 5] → Windsurf V2 (add to Phase 8: Quality Automation)
- ...

## Category C: New Initiatives Needed (3 items)
- **Task System Validation** (HIGH PRIORITY)
  - 3 action items grouped
  - Impact: CRITICAL (violations despite mandatory rules)
  - Estimated effort: 6-8 hours
- ...

## Category D: Deferred (23 items)
- Low impact or low confidence
- Document for future consideration
```

### 2.5.5 Best Practices

**DO:**

- ✅ Read entire summary before extracting (context matters)
- ✅ Use verbatim quotes when possible
- ✅ Check frequency across multiple summaries
- ✅ Cross-reference against ALL active initiatives
- ✅ Group related action items into potential initiatives

**DON'T:**

- ❌ Extract from accomplishments without pain point evidence
- ❌ Create action items from speculation
- ❌ Skip cross-reference validation
- ❌ Create duplicate initiatives for covered work
- ❌ Ignore low-confidence items entirely (document them)

---

## Stage 3: Consolidation

### 3.1 Merge Rules

| Rule | Action |
|------|--------|
| 1. Accomplishments | Same action+component → merge, keep specific |
| 2. Decisions | Same topic → both if complementary, merge if elaboration |
| 3. Learnings | Same tech → combine, preserve measurements |
| 4. Issues | Group by component, distinct only, prioritize by frequency |
| 5. Next Steps | Remove duplicates, merge overlapping, group by component |

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

## Stage 5: Implementation and Cleanup

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

### 5.4 Delete Original Files

⚠️ **CRITICAL SAFETY:** Do NOT delete consolidated summary.

**Rationale:** Per industry best practices, consolidation = compress data + purge/delete originals. The consolidated summary preserves all critical information in compressed format. Originals are redundant and should be deleted, not archived.

**Reference:** [Database consolidation best practices](https://www.sedatasolutions.io/whats-the-difference-between-purging-deleting-and-archiving-in-a-database/) - "Purging keeps a copy of the data... more beneficial when removing large amounts of records."

**After validation:**

```bash
# List files to be deleted (verify before running)
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md | grep -v "daily-summary"

# Delete originals (EXCLUDES daily-summary.md)
find docs/archive/session-summaries -name "YYYY-MM-DD-*.md" ! -name "*daily-summary.md" -delete
```

**Validation:** Ensure consolidated summary exists and is complete before deletion.

**DO NOT:**

- ❌ Create `consolidated/` subdirectories
- ❌ Move files to archive subdirectories
- ❌ Use `git mv` to "archive" originals
- ✅ Use `git rm` or `find ... -delete` to purge originals

See [Error Handling Patterns](../rules/11_error_handling.md) for safe file operations.

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

- Created comprehensive daily summary consolidating N sessions
- Deleted N individual summaries (information preserved in daily summary)
- Updated references
- All critical information preserved in compressed format"
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
- [ ] Original summaries deleted after verification (not archived)
- [ ] All references updated
- [ ] No `consolidated/` subdirectories created
- [ ] Markdown linting passes
- [ ] Git commit completed

---

## References

- [CONSTITUTION.md](../../docs/CONSTITUTION.md)
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md)
- [ADR-0003](../../docs/adr/0003-documentation-standards-and-structure.md)

---

## Changelog

### v2.3.0 (2025-10-19)

#### Feature: Action Item Extraction

1. **Stage 2.5 added** - Optional action item extraction from summaries
2. **Manual extraction process** - 5-step systematic approach:
   - Read section by section (what to look for in each section)
   - Identify 4 types: pain points, missing capabilities, regressions, improvements
   - Categorize by theme (8 categories defined)
   - Note source (file, section, quote)
   - Assign impact/confidence (with frequency heuristics)
3. **YAML template** - Structured format for action items
4. **Cross-reference validation** - Avoid duplicate initiatives:
   - Check against active initiatives
   - Categorize: Already covered, Gap, New needed, Deferred
   - Deduplication strategy
5. **Output format** - Two files: action-items.yaml + gap-analysis.md
6. **Best practices** - DO/DON'T guidance

**Use case:** Mining summaries for initiative planning, quarterly reviews, systematic improvement cycles.

**Estimated time:** +30-60 min per 20 summaries

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

**Version:** 2.3.0 (Added action item extraction capability, Oct 2025)
