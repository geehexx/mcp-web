---
created: "2025-10-17"
updated: "2025-10-21"
description: Consolidate historical session summaries into daily comprehensive files
auto_execution_mode: 3
category: Analysis
complexity: 70
tokens: 2000
dependencies:
  - extract-session
  - summarize-session
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Consolidate Session Summaries Workflow

Merge multiple per-session summaries from same day into comprehensive daily summaries.

---

## Usage

**Invocation:** `/consolidate-summaries [date]`

**When:** 5+ summaries in single day, quarterly reviews

**Prerequisites:** Date in past, multiple summaries exist

```typescript
update_plan({
  explanation: "📋 /consolidate-summaries",
  plan: [
    { step: "1. Analyze targets", status: "in_progress" },
    { step: "2. Extract information", status: "pending" },
    { step: "3. Apply consolidation rules", status: "pending" },
    { step: "4. Validate and create", status: "pending" },
    { step: "5. Delete originals, commit", status: "pending" }
  ]
})
```

---

## Stage 1: Analysis

```bash
# Count
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md | wc -l
```

**Decision:** 5+→Consolidate | 3-4→If redundant | 1-2→Skip

**Batch read (7x faster):**

```typescript
mcp0_read_multiple_files(["docs/archive/session-summaries/YYYY-MM-DD-*.md"])
```

**Check refs:**

```bash
grep -r "2025-10-15-specific-session.md" docs/ .windsurf/ --include="*.md"
```

---

## Stage 2: Structured Extraction

**Extract from each:** metadata, context, accomplishments, decisions, learnings, issues, dependencies, evidence, next steps, metrics

**JSON format:**

```json
{
  "date": "YYYY-MM-DD",
  "sessions": [
    {
      "title": "Session Name",
      "duration": "~2h",
      "focus": "testing",
      "context": "2-3 sentences",
      "accomplishments": [{"action": "Created", "what": "Feature", "where": "file.py", "context": "Why"}],
      "decisions": [{"topic": "Topic", "decision": "Choice", "rationale": "Why", "tradeoffs": "Alternatives"}],
      "learnings": [{"category": "Tool", "insight": "Discovery", "measurement": "Data"}],
      "issues": [{"area": "Component", "problem": "Issue", "reason": "Blocker", "owner": "Team"}],
      "dependencies": {"upstream": [], "downstream": [], "notes": ""},
      "evidence": {"commits": [], "benchmarks": [], "quotes": []},
      "next_steps": [],
      "metrics": {"files_modified": 5, "commits": 3, "tests_passing": 45, "adrs_created": 1}
    }
  ]
}
```

---

## Stage 2.5: Action Item Extraction (Optional)

**When:** Quarterly reviews, initiative planning

**Process:**

1. **Read sections** → Extract pain points, gaps, regressions, improvements
2. **Identify types** → Pain Points, Missing Capabilities, Regressions, Improvements
3. **Categorize** → workflow, testing, docs, security, performance, automation
4. **Track source** → File, section, quote
5. **Score** → Impact (high/med/low), Confidence (high=3+ mentions)

**YAML:**

```yaml
action_items:
  - id: "YYYY-MM-DD#section#N"
    title: "Title"
    category: "workflow"
    impact: "high"
    confidence: "high"
    source: {file, section, quote, date}
    context: {related_files, related_initiatives}
    mapping: {suggested_initiative, create_new_initiative}
```

**Cross-ref:** Check active initiatives → Categorize (A: covered, B: gap, C: new needed, D: backlog)

**Output:** `YYYY-MM-DD-action-items.yaml`, `YYYY-MM-DD-gap-analysis.md`

---

## Stage 3: Consolidation

**Merge rules:**

1. Accomplishments: Same action+component→merge
2. Decisions: Same topic→both if complementary
3. Learnings: Same tech→combine, preserve measurements
4. Issues: Group by component, distinct only
5. Next Steps: Remove duplicates, group by component

**Template:** `docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md`

**Sections:** Header, Executive (≤120w), Timeline, Accomplishments (grouped), Decisions, Learnings, Cross-Session Dynamics, Metrics, Issues, Next Steps, Evidence, Metadata

---

## Stage 4: Validation

- **Info:** All items from originals
- **Format:** Template structure, action verbs, file refs
- **Quality:** Executive ≤3 sent/each, specific, no duplicates
- **LLM-Agnostic:** Reproducible, verifiable, consistent

---

## Stage 5: Implementation

1. Create `YYYY-MM-DD-daily-summary.md`
2. Fill template, "None" if section empty
3. Validate (Stage 4)
4. Delete: `find docs/archive/session-summaries -name "YYYY-MM-DD-*.md" ! -name "*daily-summary.md" -delete`
5. Update refs

---

## Stage 6: Commit

```bash
task docs:lint && task test:fast
git add docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
git commit -m "docs(summaries): consolidate YYYY-MM-DD (N sessions)"
```

---

## References

- `extract-session.md`, `summarize-session.md`
- `07_context_optimization.md`, `15_tool_patterns.md`
