---
description: Consolidate historical session summaries into daily comprehensive files
---

# Consolidate Session Summaries Workflow

## Purpose

Merge multiple per-session summaries from the same day into comprehensive daily summaries, reducing redundancy while maintaining all critical information and historical context.

## When to Use

- When a day has accumulated 5+ individual session summaries
- During quarterly documentation reviews
- When session summary proliferation reduces discoverability
- **Never** consolidate current day's summaries (allow ongoing work)

## Invocation

`/consolidate-summaries [date]` (e.g., `/consolidate-summaries 2025-10-15`)

---

## Prerequisites

1. **Date must be in the past** (not current day)
2. **Multiple summaries exist** for the target date
3. **No active work** referencing individual summaries

---

## Stage 1: Analysis

### 1.1 Identify Target Summaries

```bash
# List all summaries for target date
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md

# Count summaries
ls -1 docs/archive/session-summaries/YYYY-MM-DD-*.md | wc -l
```

**Decision criteria:**

- **5+ summaries:** Consolidate highly recommended
- **3-4 summaries:** Consolidate if redundant
- **1-2 summaries:** Leave as-is

### 1.2 Read and Categorize Content

Use batch read for efficiency:

```python
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/YYYY-MM-DD-summary1.md",
    "/home/gxx/projects/mcp-web/docs/archive/session-summaries/YYYY-MM-DD-summary2.md",
    # ... all summaries for that day
])
```

**Extract from each:**

- Session objectives and scope
- Key accomplishments
- Important decisions made
- Files modified and commits
- Lessons learned
- Unresolved issues
- Next steps

### 1.3 Check for External References

```bash
# Check if any files reference individual summaries
grep -r "2025-10-15-specific-session.md" docs/ .windsurf/ --include="*.md"
```

**If references found:** Update them to point to consolidated summary after creation.

---

## Stage 2: Consolidation Strategy

### 2.1 Structure for Consolidated Summary

```markdown
# Daily Summary: [Date]

**Date:** YYYY-MM-DD
**Total Sessions:** N
**Duration:** ~X hours (combined)
**Focus Areas:** [Primary themes]

---

## Overview

[High-level summary of the day's work - 2-3 paragraphs capturing:
- What was accomplished
- Major decisions made
- Progress on initiatives
- Key challenges encountered]

---

## Sessions

### Session 1: [Session Title]
**Duration:** ~X hours
**Focus:** [Brief description]

**Key Accomplishments:**
- [Major items]

**Decisions Made:**
- [Important decisions]

### Session 2: [Session Title]
[Same structure...]

---

## Cumulative Metrics

**Files Modified:** X files
**Commits:** X commits
**Tests:** X passing, Y failing
**ADRs Created:** N
**Initiatives Updated:** N

---

## Key Learnings (Consolidated)

### Technical Insights

1. **[Category]:** [Learning]
2. **[Category]:** [Learning]

### Process Improvements

1. **[Category]:** [Learning]
2. **[Category]:** [Learning]

---

## Unresolved Issues

[Items that need follow-up, carried over from individual sessions]

---

## Next Steps

[Consolidated next steps from all sessions, deduplicated]

---

## Original Sessions

**This consolidated summary synthesizes:**

- `2025-MM-DD-session1.md` (archived)
- `2025-MM-DD-session2.md` (archived)
- `2025-MM-DD-session3.md` (archived)

**Original summaries moved to:** `docs/archive/session-summaries/archived/YYYY-MM-DD/`
```

### 2.2 Information Preservation

**Must preserve:**

- ✅ All unique technical decisions
- ✅ All commits and file changes
- ✅ All lessons learned
- ✅ All unresolved issues
- ✅ References to source summaries

**Can merge/deduplicate:**

- ⚠️ Repetitive descriptions
- ⚠️ Overlapping accomplishments
- ⚠️ Similar lessons learned
- ⚠️ Duplicate next steps

**Can omit:**

- ❌ Verbose session narration
- ❌ Redundant context descriptions
- ❌ Duplicate metric listings

---

## Stage 3: Implementation

### 3.1 Create Consolidated Summary

1. **Create new file:**

```bash
docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
```

1. **Write consolidated content** following structure above
2. **Verify all critical info preserved** (cross-check with originals)

### 3.2 Archive Original Summaries

**Create archive subdirectory:**

```bash
mkdir -p docs/archive/session-summaries/archived/YYYY-MM-DD
```

**Move original summaries:**

```bash
mv docs/archive/session-summaries/YYYY-MM-DD-session*.md \
   docs/archive/session-summaries/archived/YYYY-MM-DD/
```

**Add README in archived directory:**

```markdown
# Archived Session Summaries: YYYY-MM-DD

These individual session summaries have been consolidated into:
`docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md`

**Original sessions:**
- YYYY-MM-DD-session1.md
- YYYY-MM-DD-session2.md
- YYYY-MM-DD-session3.md

Archived on: YYYY-MM-DD
```

### 3.3 Update References

**Search for references:**

```bash
grep -r "YYYY-MM-DD-session" docs/ .windsurf/ --include="*.md"
```

**Update each reference to:** `YYYY-MM-DD-daily-summary.md`

---

## Stage 4: Verification

### 4.1 Quality Checks

**Completeness:**

- [ ] All sessions represented
- [ ] All commits listed
- [ ] All decisions captured
- [ ] All learnings preserved
- [ ] All unresolved issues noted

**Structure:**

- [ ] Markdown linting passes
- [ ] Headings properly hierarchical
- [ ] Links work correctly
- [ ] Code blocks formatted

**Archival:**

- [ ] Original summaries moved to archived/
- [ ] Archive README created
- [ ] No broken references

### 4.2 Git Commit

```bash
git add docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
git add docs/archive/session-summaries/archived/YYYY-MM-DD/
git commit -m "docs(archive): consolidate YYYY-MM-DD session summaries

- Created comprehensive daily summary
- Archived 15 individual session summaries
- Updated all references
- Preserved all critical information"
```

---

## Best Practices

### DO

✅ **Wait 24-48 hours** after date before consolidating (ensure no late additions)
✅ **Preserve unique insights** even if brief
✅ **Cross-reference initiatives** mentioned
✅ **Include metrics** for measurability
✅ **Cite original sources** for traceability
✅ **Update external references** to new location

### DON'T

❌ **Don't consolidate current day** (ongoing work)
❌ **Don't omit unresolved issues** (needed for continuity)
❌ **Don't delete originals** (move to archived/)
❌ **Don't lose commit history** (git mv for file moves)
❌ **Don't skip reference updates** (breaks navigation)

---

## Examples

### Before Consolidation

```text
docs/archive/session-summaries/
├── 2025-10-15-comprehensive-overhaul.md
├── 2025-10-15-improvements-v2.md
├── 2025-10-15-testing-implementation.md
├── 2025-10-15-workflow-optimization.md
├── 2025-10-15-initiative-documentation.md
├── ... (10 more files)
```

**Problems:**

- Hard to find information (15 files)
- Redundant context across files
- Unclear which to read first
- Navigation overhead

### After Consolidation

```text
docs/archive/session-summaries/
├── 2025-10-15-daily-summary.md (comprehensive)
├── archived/
│   └── 2025-10-15/
│       ├── README.md
│       ├── 2025-10-15-comprehensive-overhaul.md
│       ├── 2025-10-15-improvements-v2.md
│       └── ... (13 more originals)
```

**Benefits:**

- Single entry point for Oct 15 work
- All info preserved but organized
- Originals available if needed
- Clear historical record

---

## Success Criteria

- [ ] Single consolidated summary created
- [ ] All unique information preserved
- [ ] Original summaries archived (not deleted)
- [ ] All references updated
- [ ] Markdown linting passes
- [ ] Git commit completed with descriptive message

---

## Maintenance

**Frequency:** Monthly or as needed

**Trigger points:**

- Day has 5+ summaries
- Quarterly documentation review
- Historical research becomes difficult

**Review:** Annual assessment of consolidation effectiveness

---

## References

- [CONSTITUTION.md](../../docs/CONSTITUTION.md) - Documentation standards
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md) - Archive policies
- [ADR-0003](../../docs/adr/0003-documentation-standards-and-structure.md) - Documentation decisions

---

**Last Updated:** 2025-10-16
**Version:** 1.0.0
