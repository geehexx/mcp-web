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

## Stage 2: Methodical Extraction (Information Gathering)

**CRITICAL:** This stage uses structured extraction to ensure consistency across LLMs. Follow the exact process below.

### 2.1 Extract Information Systematically

**Process each summary file individually using this Chain-of-Thought approach:**

```markdown
### For each summary file, extract the following in order:

#### Step 1: Identify Session Metadata
- Session title/name (from filename or document)
- Approximate duration (if mentioned)
- Primary focus area (1-2 words: testing, security, documentation, etc.)

#### Step 2: Extract Accomplishments (Specific Actions)
List ONLY concrete accomplishments in this exact format:
- **[Action verb]**: [What was done] ([File/Component if applicable])

Examples:
- **Created**: Security audit framework (src/mcp_web/security.py)
- **Fixed**: 7 failing unit tests (tests/unit/test_security.py)
- **Updated**: Architecture documentation (docs/architecture/ARCHITECTURE.md)

DO NOT include vague statements like "made progress" or "worked on".

#### Step 3: Extract Decisions (Explicit Choices Made)
List ONLY explicit architectural or technical decisions:
- **[Decision topic]**: [What was decided] - [Brief rationale]

Example:
- **Rate limiting**: Implemented token bucket algorithm - Better handles burst traffic than fixed window

DO NOT include routine implementation choices.

#### Step 4: Extract Technical Learnings (Knowledge Gained)
List ONLY specific technical insights:
- **[Technology/Pattern]**: [What was learned/discovered]

Example:
- **pytest-xdist**: Auto scheduling performs 3x faster than loadscope for IO-bound tests

DO NOT include general observations.

#### Step 5: Extract Issues (Unresolved Problems)
List ONLY problems that remain unresolved:
- **[Component/Area]**: [Problem description] - [Why unresolved]

Example:
- **Playwright fallback**: Timeout handling needs refinement - Requires more testing data

DO NOT include resolved issues.

#### Step 6: Extract Next Steps (Specific Actions)
List ONLY concrete next steps:
- [ ] [Action verb] [specific task]

Example:
- [ ] Add integration tests for rate limiter
- [ ] Document security architecture decisions in ADR

DO NOT include vague intentions like "continue working on".

#### Step 7: Extract Metrics
- Files modified: [count or list if ≤5]
- Commits: [count or list if ≤3]
- Tests: [passing/failing counts]
- ADRs: [created/updated]
```

### 2.2 Create Extraction Matrix (JSON Format)

**IMPORTANT:** After extracting from all summaries, create a JSON structure for systematic consolidation:

```json
{
  "date": "YYYY-MM-DD",
  "sessions": [
    {
      "title": "Session 1 Name",
      "duration": "~2 hours",
      "focus": "testing",
      "accomplishments": [
        {"action": "Created", "what": "Security audit framework", "where": "src/mcp_web/security.py"}
      ],
      "decisions": [
        {"topic": "Rate limiting", "decision": "Implemented token bucket algorithm", "rationale": "Better handles burst traffic"}
      ],
      "learnings": [
        {"category": "pytest-xdist", "insight": "Auto scheduling performs 3x faster for IO-bound tests"}
      ],
      "issues": [
        {"area": "Playwright fallback", "problem": "Timeout handling needs refinement", "reason": "Requires more testing data"}
      ],
      "next_steps": [
        "Add integration tests for rate limiter"
      ],
      "metrics": {
        "files_modified": 5,
        "commits": 3,
        "tests_passing": 45,
        "tests_failing": 2,
        "adrs_created": 1
      }
    }
  ]
}
```

**Why JSON?** It forces structured thinking and prevents LLM from hallucinating or over-summarizing.

---

## Stage 3: Methodical Consolidation (Information Synthesis)

### 3.1 Merge Using Explicit Rules

**Process the extraction matrix systematically:**

#### Rule 1: Deduplicate Accomplishments

```markdown
IF two accomplishments have:
  - Same action verb AND
  - Same file/component
THEN merge them:
  - Keep the more specific description
  - Combine any unique details

Example:
  - "Fixed failing tests (test_security.py)"
  - "Fixed 7 unit tests in security module"
  → "Fixed 7 failing unit tests (tests/unit/test_security.py)"
```

#### Rule 2: Consolidate Decisions

```markdown
IF two decisions have:
  - Same topic area
THEN:
  - Keep both if they represent different aspects
  - Merge if one is an elaboration of the other
  - Note if a decision was revisited/changed

Example:
  - Session 1: "Use httpx for fetching"
  - Session 3: "Add Playwright fallback for JS sites"
  → Keep both (complementary decisions)
```

#### Rule 3: Synthesize Learnings

```markdown
IF two learnings are about:
  - Same technology/pattern
THEN:
  - Combine into single insight
  - Preserve specific numbers/measurements
  - Note progression if learning evolved

Example:
  - "pytest-xdist speeds up tests"
  - "Auto scheduling mode in pytest-xdist is 3x faster"
  → "pytest-xdist auto scheduling performs 3x faster than loadscope for IO-bound tests"
```

#### Rule 4: Aggregate Issues

```markdown
FOR unresolved issues:
  - Group by component/area
  - Keep all distinct issues (do not merge)
  - Note if issue was mentioned multiple times
  - Prioritize by frequency of mention
```

#### Rule 5: Consolidate Next Steps

```markdown
FOR next steps:
  - Remove duplicates (exact matches)
  - Merge overlapping tasks
  - Group by component/initiative
  - Prioritize by dependency order
```

### 3.2 Generate Consolidated Summary Structure

**Use this EXACT template (strict format constraint):**

```markdown
# Daily Summary: [Date]

**Date:** YYYY-MM-DD
**Total Sessions:** N
**Duration:** ~X hours (combined)
**Focus Areas:** [List 2-4 primary themes]

---

## Executive Overview

**Accomplishments:** [1 sentence summarizing major achievements]
**Decisions:** [1 sentence summarizing key decisions]
**Status:** [1 sentence on overall progress]

---

## Sessions Timeline

### Session 1: [Title] (~X hours)
**Focus:** [1-2 word category]
**Key Actions:**
- [Accomplishment 1]
- [Accomplishment 2]
- [Accomplishment 3]

**Decisions:** [List if any, or "None"]

### Session 2: [Title] (~X hours)
[Same structure...]

---

## Consolidated Accomplishments

### Code Changes
- [List all code-related accomplishments]

### Documentation
- [List all documentation accomplishments]

### Testing
- [List all testing accomplishments]

### Infrastructure/Tooling
- [List all infrastructure accomplishments]

---

## Technical Decisions

1. **[Decision Topic]**
   **Decision:** [What was decided]
   **Rationale:** [Why]
   **Impact:** [Expected effect]

---

## Key Learnings

### Technical Insights
1. **[Technology/Pattern]:** [Specific insight with measurements]
2. **[Technology/Pattern]:** [Specific insight with measurements]

### Process Improvements
1. **[Process/Workflow]:** [What was learned]
2. **[Process/Workflow]:** [What was learned]

---

## Metrics (Cumulative)

| Metric | Count | Details |
|--------|-------|----------|
| Files Modified | N | [List if ≤ 5] |
| Commits | N | [List if ≤ 3] |
| Tests Passing | N | [Context if changed] |
| Tests Failing | N | [List issues] |
| ADRs Created | N | [List titles] |
| Initiatives Updated | N | [List names] |

---

## Unresolved Issues

### [Component/Area 1]
- **Issue:** [Problem description]
  **Reason:** [Why unresolved]
  **Priority:** [High/Medium/Low based on mention frequency]

### [Component/Area 2]
[Same structure...]

---

## Next Steps (Prioritized)

### Immediate (Next Session)
- [ ] [Highest priority task]
- [ ] [Second priority task]

### Short-term (This Week)
- [ ] [Important but not urgent]
- [ ] [Important but not urgent]

### Future Considerations
- [ ] [Nice to have]
- [ ] [Nice to have]

---

## Metadata

**Original Sessions:**
- `2025-MM-DD-session1.md` → Session 1 above
- `2025-MM-DD-session2.md` → Session 2 above

**Consolidation Method:** Methodical extraction with structured merge rules
**Workflow Version:** 2.0.0 (LLM-agnostic)
```

---

## Stage 4: Quality Validation

### 4.1 Validation Checklist

**Information Preservation (MUST verify each):**

```markdown
For EACH original summary:
  ✓ All unique accomplishments captured (check extraction matrix)
  ✓ All decisions documented (compare decision sections)
  ✓ All learnings preserved (verify no technical insights lost)
  ✓ All unresolved issues listed (cross-reference issues section)
  ✓ All next steps included (deduplicated but present)
  ✓ All metrics aggregated (sum/count matches)
```

**Format Compliance (MUST verify):**

```markdown
  ✓ Exact template structure followed (headings match)
  ✓ No vague statements ("made progress", "worked on")
  ✓ Action verbs used consistently
  ✓ Specific file/component references included
  ✓ Measurements/numbers preserved
  ✓ Tables formatted correctly
  ✓ Checkboxes use [ ] format
```

**Content Quality (MUST verify):**

```markdown
  ✓ Executive overview is ≤ 3 sentences
  ✓ Each accomplishment is specific and actionable
  ✓ Decisions include rationale and impact
  ✓ Learnings include specific measurements
  ✓ Issues explain why unresolved
  ✓ Next steps are concrete (not vague)
  ✓ No duplicate information across sections
```

### 4.2 LLM-Agnostic Verification

**Test your consolidation by asking:**

1. **Can another person reconstruct the day's work from this summary?**
   If no → Add missing context

2. **Are all numbers/metrics verifiable from git/files?**
   If no → Correct or remove unverifiable claims

3. **Could this be generated by any LLM following the rules?**
   If no → You introduced model-specific bias

4. **Is every accomplishment specific enough to verify?**
   If no → Add file references or specific details

5. **Would ChatGPT, Claude, and Gemini produce similar output?**
   If no → Your instructions need more constraints

---

## Stage 5: Implementation

### 5.1 Create Consolidated Summary File

```bash
# Create with exact naming convention
docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
```

### 5.2 Write Content (Following Template Exactly)

1. Copy the template from Stage 3.2
2. Fill in extracted and consolidated information
3. DO NOT deviate from template structure
4. DO NOT add explanatory text outside template
5. DO NOT skip sections (use "None" if empty)

### 5.3 Verify Content (Before Committing)

**Run through validation checklist (Stage 4.1) line by line**

### 5.4 Remove Original Session Files

After validating the consolidated summary, delete the original session files to keep the archive lean:

```bash
rm docs/archive/session-summaries/YYYY-MM-DD-*.md
```

⚠️ **Safety check:** Ensure the new `YYYY-MM-DD-daily-summary.md` is complete and backed up in version control before deleting originals. If unsure, pause and review with the team.

### 5.5 Update References

**Search for references:**

```bash
grep -r "YYYY-MM-DD-session" docs/ .windsurf/ --include="*.md"
```

**Update each reference to:** `YYYY-MM-DD-daily-summary.md`

---

## Stage 6: Final Verification

### 6.1 Automated Quality Checks

```bash
# Run markdown linting
task lint:docs

# Check for broken links (if available)
markdown-link-check docs/archive/session-summaries/YYYY-MM-DD-daily-summary.md
```

### 6.2 Manual Quality Checks

**Completeness (verify against original files):**

- [ ] All sessions represented in timeline
- [ ] All commits listed in metrics table
- [ ] All decisions captured with rationale
- [ ] All learnings preserved with measurements
- [ ] All unresolved issues noted with reasons

**Format Compliance:**

- [ ] Template structure exactly followed
- [ ] Tables formatted correctly
- [ ] No vague language ("made progress", "worked on")
- [ ] All action items use [ ] checkbox format
- [ ] File paths use backticks

**Clean-up:**

- [ ] Original session files deleted
- [ ] No broken references to removed files
- [ ] Metadata section correctly lists original files

### 6.3 Git Commit

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
❌ **Don't delete originals until the consolidated summary is verified**
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
```

**Benefits:**

- Single entry point per day
- Reduced clutter and redundancy
- Historical context retained in consolidated file

---

## Success Criteria

- [ ] Single consolidated summary created
- [ ] All unique information preserved
- [ ] Original summaries removed after verification
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
**Version:** 2.0.0 (Methodical LLM-agnostic approach)

---

## Changelog

### Version 2.0.0 (2025-10-16)

- **BREAKING:** Complete methodology overhaul for LLM-agnostic consolidation
- Added: Chain-of-Thought extraction process (Stage 2)
- Added: Structured JSON extraction matrix
- Added: Explicit merge rules with examples
- Added: Strict format constraints to reduce model variance
- Added: LLM-agnostic verification checklist
- Changed: Template structure with executive overview
- Changed: Accomplishments grouped by category
- Changed: Next steps prioritized by urgency
- Improved: Validation checklist with specific criteria
- Research: Based on October 2025 prompt engineering best practices
  - Chain-of-Thought reasoning (Lakera AI Guide, 2025)
  - Format constraints (Towards Data Science, 2025)
  - Structured extraction (Matt Stockton LLM Summarization, 2025)

### Version 1.0.0 (2025-10-15)

- Initial workflow version
