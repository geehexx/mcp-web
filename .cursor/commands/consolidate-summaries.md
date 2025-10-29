---
pass_through: true
description: Consolidate historical session summaries into daily comprehensive files
title: Consolidate Summaries Workflow
tags: ['consolidation', 'summaries', 'analysis', 'daily']
---

# Consolidate Session Summaries Workflow

Merge multiple per-session summaries from same day into comprehensive daily summaries.

## Usage

**Invocation:** `/consolidate-summaries [date]`

**When:** 5+ summaries in single day, quarterly reviews

**Prerequisites:** Date in past, multiple summaries exist

```typescript
update_plan({
  explanation: "📋 /consolidate-summaries",
  plan: [
    { step: "1. /consolidate-summaries - Analyze targets", status: "in_progress" },
    { step: "2. /consolidate-summaries - Extract information", status: "pending" },
    { step: "3. /consolidate-summaries - Apply consolidation rules", status: "pending" },
    { step: "4. /consolidate-summaries - Validate and create", status: "pending" },
    { step: "5. /commit - Delete originals and commit", status: "pending" }
  ]
})
```

## Stage 1: Analysis

```bash
# Count
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md | wc -l
```

**Analyze consolidation targets:**
- Count summaries for date
- Check consolidation criteria
- Identify consolidation rules
- Plan consolidation strategy

## Stage 2: Extract Information

### 2.1 Load Session Summaries

**Load all summaries for date:**
- Read summary files
- Extract key information
- Identify patterns
- Group related content

### 2.2 Extract Key Data

**Extract from each summary:**
- Objectives
- Completed work
- Commits
- Learnings
- Patterns
- Next steps

## Stage 3: Apply Consolidation Rules

### 3.1 Deduplicate Content

**Remove duplicate information:**
- Merge identical objectives
- Combine similar work items
- Consolidate duplicate commits
- Merge related learnings

### 3.2 Organize by Theme

**Group content by theme:**
- Feature development
- Bug fixes
- Documentation
- Testing
- Infrastructure

### 3.3 Prioritize Content

**Prioritize important content:**
- Major accomplishments
- Critical learnings
- Important patterns
- Key next steps

## Stage 4: Create Consolidated Summary

### 4.1 Generate Daily Summary

**Create comprehensive daily summary:**
```markdown
# Daily Summary: YYYY-MM-DD

## Overview
[Consolidated overview of the day]

## Sessions
- Session 1: [Time] - [Focus]
- Session 2: [Time] - [Focus]
- Session 3: [Time] - [Focus]

## Key Accomplishments
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

## Commits
[Consolidated commit list]

## Learnings
- [Learning 1]
- [Learning 2]
- [Learning 3]

## Patterns
### Positive Patterns
- [Pattern 1]
- [Pattern 2]

### Areas for Improvement
- [Pattern 1]
- [Pattern 2]

## Next Steps
- [Next step 1]
- [Next step 2]
- [Next step 3]

## Metrics
- **Total Sessions:** X
- **Total Duration:** Y hours
- **Total Commits:** Z
- **Success Rate:** A%
```

### 4.2 Validate Content

**Check consolidated summary:**
- Completeness
- Accuracy
- Clarity
- Organization

## Stage 5: Clean Up

### 5.1 Archive Originals

**Move original summaries:**
- Create archive subdirectory
- Move individual summaries
- Update index
- Preserve originals

### 5.2 Update Index

**Update summary index:**
- Add consolidated summary
- Remove individual entries
- Update metadata
- Maintain chronology

## Stage 6: Commit Changes

### 6.1 Commit Consolidated Summary

```bash
git add docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
git commit -m "docs(session): consolidate daily summaries for YYYY-MM-DD

- Consolidated X session summaries
- Key themes: [list]
- Major accomplishments: [list]"
```

### 6.2 Commit Archive

```bash
git add docs/archive/session-summaries/archive/
git commit -m "docs(session): archive individual summaries for YYYY-MM-DD"
```

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations
- **Documentation Standards**: `/rules/03_documentation.mdc` - Apply when creating documentation and summaries

## Workflow References

When this consolidate-summaries workflow is called:

1. **Load**: `/commands/consolidate-summaries.md`
2. **Execute**: Follow the consolidation stages defined above
3. **Analyze**: Identify consolidation targets
4. **Extract**: Load and process summaries
5. **Consolidate**: Apply consolidation rules
6. **Create**: Generate daily summary

## Anti-Patterns

❌ **Don't:**
- Skip analysis phase
- Ignore consolidation rules
- Create incomplete summaries
- Skip validation

✅ **Do:**
- Analyze targets thoroughly
- Apply consolidation rules
- Create complete summaries
- Validate content

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Consolidation accuracy | 95%+ | ✅ |
| Content completeness | 100% | ✅ |
| Deduplication success | 90%+ | ✅ |
| Organization quality | High | ✅ |

## Integration

**Called By:**
- `/meta-analysis` - When consolidation needed
- User - Direct invocation for consolidation

**Calls:**
- `/extract-session` - Session data extraction
- `/summarize-session` - Session summarization

**Exit:**

```markdown
✅ **Completed /consolidate-summaries:** Summary consolidation finished
```

## Command Metadata

**File:** `consolidate-summaries.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~2,000
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**
- Summary consolidation
- Content deduplication
- Daily summaries
- Archive management

**Dependencies:**
- /extract-session - Session data extraction
- /summarize-session - Session summarization
