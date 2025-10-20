---
created: "2025-10-17"
updated: "2025-10-19"
description: Consolidate historical session summaries into daily comprehensive files
auto_execution_mode: 3
category: Analysis
complexity: 70
tokens: 2850
dependencies:
  - extract-session
  - summarize-session
status: active
version: 2.3.0
---

# Consolidate Session Summaries Workflow

## Purpose

Merge multiple per-session summaries from the same day into comprehensive daily summaries, reducing redundancy while maintaining critical information.

---

## Stage 0: Create Task Plan

🔄 **Entering /consolidate-summaries workflow**

**Create task plan:**

```typescript
update_plan({
  explanation: "📋 Starting /consolidate-summaries workflow",
  plan: [
    { step: "1. /consolidate-summaries - Identify and analyze target summaries", status: "in_progress" },
    { step: "2. /consolidate-summaries - Extract information systematically", status: "pending" },
    { step: "2.5. /consolidate-summaries - Extract action items (optional)", status: "pending" },
    { step: "3. /consolidate-summaries - Apply consolidation rules", status: "pending" },
    { step: "4. /consolidate-summaries - Validate and create consolidated summary", status: "pending" },
    { step: "5. /consolidate-summaries - Delete originals and commit", status: "pending" }
  ]
})
```

---

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

## Stage 2.5: Action Item Extraction (Optional)

**Purpose:** Extract actionable insights from summaries - pain points, missing capabilities, regressions, and improvement opportunities.

**When to Use:** Mining summaries for initiative planning, quarterly reviews, or systematic improvement cycles.

### 2.5.1 Manual Extraction Process

For each summary:

#### Step 1: Read Section by Section

Read systematically through each major section:

- Accomplishments → look for workarounds indicating missing features
- Decisions → look for forced choices indicating constraints
- Learnings → look for surprises indicating gaps
- Unresolved Issues → explicit pain points
- Next Steps → deferred work indicating priority/capacity issues

#### Step 2: Identify Action Items

Capture four types of action items:

**1. Pain Points** - Problems explicitly mentioned or implied

- Example: "Manual file operations time-consuming" → Need automation
- Example: "Task system violations occurred 3 times" → Need validation

**2. Missing Capabilities** - Features/workflows identified as needed

- Example: "No cross-reference validation" → Need validation tool
- Example: "Cannot use MCP for local files" → Need file system support

**3. Regressions** - Issues that recurred or weren't fully fixed

- Example: "Workflow violations despite mandatory rules" → Enforcement gap
- Example: "Markdown linting errors reappeared" → CI integration needed

**4. Improvement Opportunities** - Suggestions or ideas mentioned

- Example: "Could parallelize test execution" → Performance optimization
- Example: "Workflow decomposition worked well" → Apply pattern elsewhere

#### Step 3: Categorize by Theme

Assign primary category:

- `workflow` - Workflow improvements, automation
- `testing` - Test infrastructure, coverage, performance
- `documentation` - Docs quality, structure, automation
- `security` - Security checks, validation, compliance
- `performance` - Speed, efficiency, resource usage
- `automation` - Scaffolding, code generation, tooling
- `infrastructure` - Dev environment, CI/CD, tooling
- `quality` - Linting, validation, standards enforcement

#### Step 4: Note Source Information

For each action item, record:

- **File:** Summary filename
- **Section:** Section where found (e.g., "Unresolved Issues", "Learnings")
- **Quote:** Verbatim quote if available (preserves context)

Example:

```yaml
- file: 2025-10-18-task-system-violations.md
  section: "Recommendations"
  quote: "Add task format validation pre-commit hook"
```

#### Step 5: Assign Impact and Confidence

**Impact** (effect if implemented):

- `high` - Blocks work, affects quality, or prevents major issues
- `medium` - Improves efficiency, reduces friction
- `low` - Nice-to-have, cosmetic improvement

**Confidence** (how certain this is needed):

- `high` - Mentioned 3+ times OR explicit user directive OR blocking issue
- `medium` - Mentioned 1-2 times, clear benefit
- `low` - Implied need, inferred from context

**Frequency heuristics:**

- Same issue across 3+ sessions → High confidence
- Explicit in unresolved issues → High confidence
- Mentioned in passing once → Low confidence

### 2.5.2 Create Action Items YAML

**Template:**

```yaml
action_items:
  - id: "YYYY-MM-DD-summary#section#index"
    title: "Concise action item title (5-10 words)"
    description: "Detailed description with context"
    category: "workflow"  # See Step 3 for categories
    impact: "high"  # high | medium | low
    confidence: "high"  # high | medium | low

    # Source tracking
    source_summary: "2025-10-18-task-system-violations.md"
    source_section: "Recommendations"
    source_quote: "Add task format validation pre-commit hook"
    session_date: "2025-10-18"

    # Context
    related_files: []  # Files mentioned in context
    related_initiatives: []  # Initiatives mentioned

    # Mapping (filled during validation)
    suggested_initiative: null  # Which initiative this belongs to
    create_new_initiative: false  # Whether this needs new initiative

  - id: "YYYY-MM-DD-summary#section#2"
    # ... next item
```

### 2.5.3 Cross-Reference Validation

**Purpose:** Avoid duplicate initiatives, map to existing work.

For each HIGH impact + HIGH confidence action item:

#### Step 1: Check Active Initiatives

Read all active initiatives:

```bash
ls -1 docs/initiatives/active/*/initiative.md
```

Compare action item against:

- Initiative objectives
- Success criteria
- In-scope items
- Related initiatives

**Match criteria:**

- Same problem statement
- Overlapping solution
- Same files/components mentioned

#### Step 2: Categorize Action Items

##### Category A: Already Covered

- Action item matches existing initiative scope
- Mark: `suggested_initiative: <initiative-name>`
- Action: None (already tracked)

##### Category B: Gap in Existing Initiative

- Related to initiative but not explicitly in scope
- Mark: `suggested_initiative: <initiative-name>`
- Action: Update initiative to add this item

##### Category C: New Initiative Needed

- Not covered by any active initiative
- Mark: `create_new_initiative: true`
- Action: Create new initiative

##### Category D: Low Priority

- Impact: low OR Confidence: low
- Action: Document but defer

#### Step 3: Deduplication

Check for duplicates across summaries:

- Same category + similar title → Likely duplicate
- Same related files → Check if same issue
- Same initiative mentioned → Consolidate

**Deduplication strategy:**

- Keep highest confidence version
- Merge source quotes from all mentions
- Increment frequency counter

### 2.5.4 Output Format

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
