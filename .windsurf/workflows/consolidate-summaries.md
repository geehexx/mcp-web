---
created: "2025-10-17"
updated: "2025-10-19"
description: Consolidate historical session summaries into daily comprehensive files
auto_execution_mode: 3
category: Analysis
complexity: 70
tokens: 2800
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

**Template structure (file: `docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md`):**

| Section | Content | Format |
|---------|---------|--------|
| **Header** | Date, sessions, duration, focus areas, initiatives | Metadata list |
| **Executive Overview** | 2-3 sentences each: Accomplishments, Decisions, Learnings | Prose (≤120 words total) |
| **Session Timeline** | Per session: Context (2-3 sent), What Was Done (bullets), Why (1-2 sent) | Chronological |
| **Accomplishments** | Grouped by domain (Testing, Docs, Infra, etc.) | Numbered lists with **[Action]**: [What] ([Component]) |
| **Decisions** | Per topic: Decision, Rationale, Impact, Follow-up | Structured bullets |
| **Learnings** | Technical (with measurements), Process (with triggers) | Numbered lists |
| **Cross-Session Dynamics** | Continuity threads, Unblocked work, Outstanding questions | Bullet synthesis |
| **Metrics** | Files, commits, tests, ADRs, initiatives, duration | Table (cumulative) |
| **Issues** | Per component: Issue, Reason, Owner, Priority | Structured list |
| **Next Steps** | Immediate (next session), Short-term (this week), Future | Checkboxes with owners |
| **Evidence** | Commits, benchmarks, quotes | Index with links |
| **Metadata** | Original filenames, method, version | Footer |

---

## Stage 4: Validation

| Check Type | Criteria |
|------------|----------|
| **Info Preservation** | All items from originals: accomplishments, decisions, learnings, issues, steps, metrics |
| **Format** | Template structure, action verbs, file refs, measurements, tables, checkboxes [ ] |
| **Quality** | Executive ≤3 sent/each, specific accomplishments, rationale in decisions, no duplicates |
| **LLM-Agnostic** | Reproducible by another person, verifiable metrics, consistent across LLMs |

---

## Stage 5: Implementation

| Step | Action |
|------|--------|
| 1. **Create** | `docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md` |
| 2. **Write** | Fill template (Stage 3.2), follow structure exactly, use "None" if section empty |
| 3. **Validate** | Run Stage 4 checks line by line |
| 4. **Delete Originals** | `find docs/archive/session-summaries -name "YYYY-MM-DD-*.md" ! -name "*daily-summary.md" -delete`<br>⚠️ Verify consolidated exists first |
| 5. **Update Refs** | `grep -r "YYYY-MM-DD-session" docs/ .windsurf/ --include="*.md"` → Update to daily-summary |

---

## Stage 6: Commit

| Check | Items |
|-------|-------|
| **Automated** | `task lint:docs`, `markdown-link-check` |
| **Completeness** | Sessions in timeline, commits in metrics, decisions with rationale, learnings with measurements, issues with reasons |
| **Format** | Template followed, tables formatted, no vague language, checkboxes [ ], paths backticked |
| **Cleanup** | Originals deleted, no broken refs, metadata correct |

**Commit:**

```bash
git add docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
git commit -m "docs(archive): consolidate YYYY-MM-DD (N sessions)

- Created daily summary, deleted N originals
- Updated references, preserved all critical info"
```

---

## Guidelines

| DO ✅ | DON'T ❌ |
|--------|----------|
| Wait 24-48h before consolidating | Consolidate current day |
| Preserve unique insights, cite sources | Omit unresolved issues |
| Cross-reference initiatives, include metrics | Delete before verification |
| Update external references | Lose commit history |

**Success:** Single summary, all info preserved, originals deleted (not archived), refs updated, linting passes

---

## References

- [CONSTITUTION.md](../../docs/CONSTITUTION.md)
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md)
- [ADR-0003](../../docs/adr/0003-documentation-standards-and-structure.md)

---

## Changelog

| Version | Changes |
|---------|----------|
| **v2.4.0** (2025-10-21) | Optimized for token efficiency: Compressed template to table format, consolidated validation/commit stages, table-based guidelines. 50% token reduction (5758 → 2800). |
| v2.3.0 (2025-10-19) | Added Stage 2.5 (action item extraction), 5-step process, YAML template, cross-ref validation. +30-60 min per 20 summaries. |
| v2.2.0 (2025-10-19) | Batch reading emphasis (7x faster), cross-session dynamics, timeline format, safety improvements. Tested: 7 sessions, 95%+ preservation, 52% compression. |

---

**Version:** 2.4.0 (Optimized for token efficiency, Oct 2025)
