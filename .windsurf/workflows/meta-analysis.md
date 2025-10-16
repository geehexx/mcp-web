---
description: Systematic session review and improvement identification
auto_execution_mode: 3
---

# Meta-Analysis Workflow

**Purpose:** Systematically analyze AI agent sessions to identify improvement opportunities and create consistent, comprehensive session summaries.

**When to Use:** MANDATORY at the end of every work session (part of Session End Protocol)

---

## Invocation

Automatically triggered by Session End Protocol. Can also be manually invoked:

```bash
/meta-analysis
```

---

## Stage 0: Self-Monitoring (AUTOMATIC)

**Purpose:** Detect if meta-analysis is being run correctly and on schedule.

### 0.1 Check Last Execution

Read timestamp file to detect if meta-analysis is being run regularly:

```bash
# Check if .windsurf/.last-meta-analysis exists
cat .windsurf/.last-meta-analysis 2>/dev/null || echo "NEVER"
```

**Warning triggers:**

- File doesn't exist → Meta-analysis never run before
- Timestamp >24 hours old → Overdue for meta-analysis
- Multiple commits since last run → Protocol violation likely

### 0.2 Create/Update Timestamp

Update timestamp file when meta-analysis runs:

```bash
# Write current timestamp
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis
git add .windsurf/.last-meta-analysis
# Will be committed with session summary
```

### 0.3 Protocol Adherence Check

**Check for common violations:**

- Session summary not created in proper location
- Meta-analysis not run after work session completion
- Timestamp file not updated

**If violation detected:**

1. Flag the violation in session summary
2. Document what went wrong
3. Propose workflow improvements to prevent recurrence

---

## Stage 1: Context Gathering

### 1.1 Identify Session Scope

**Extract basic information (use Chain-of-Thought):**

```markdown
Step 1: Determine session boundaries
- Start time (first commit or first significant action)
- End time (current time)
- Approximate duration (calculate from timestamps)

Step 2: Identify primary focus
- What was the main objective? (in 1-3 words)
- What initiative(s) were touched?
- What workflows were invoked?

Step 3: Count artifacts
- Files modified (use git diff)
- Commits made (use git log)
- Tests run (check command history)
- ADRs created/updated
```

### 1.2 Review Work Completed

**Use git to gather concrete data:**

```bash
# Get list of commits since last meta-analysis
git log --oneline --since="$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo '24 hours ago')"

# Get files changed
git diff --name-status HEAD~N..HEAD

# Get commit messages for context
git log --format="%h - %s" --since="$(cat .windsurf/.last-meta-analysis 2>/dev/null || echo '24 hours ago')"
```

### 1.3 Identify Key Artifacts

**Locate relevant documentation:**

```bash
# Check for initiative updates
ls -t docs/initiatives/active/*.md | head -3

# Check for ADRs created/updated
git log --oneline --since="24 hours ago" -- docs/adr/

# Check for test results (if available)
cat .test_durations 2>/dev/null | tail -10
```

---

## Stage 2: Structured Information Extraction

**CRITICAL:** Follow this Chain-of-Thought process to ensure consistency across LLMs.

### 2.1 Extract Session Metadata

```markdown
#### Session Identification
- **Date:** YYYY-MM-DD
- **Title:** [Descriptive name based on primary work]
- **Duration:** ~N hours (or "N minutes" if <1 hour)
- **Focus Area:** [1-3 words: testing, security, documentation, performance, etc.]
- **Workflows Invoked:** [List workflow names if any]
```

### 2.2 Extract Accomplishments (Concrete Actions Only)

**Format:** Use action verbs, be specific

```markdown
For EACH significant accomplishment:
- **[Action verb]**: [What was done] ([File/Component]) — [Brief context]

Examples:
✅ - **Implemented**: Parallel map-reduce optimization (src/mcp_web/processor.py) — 1.17x speedup measured
✅ - **Fixed**: 7 failing security tests (tests/unit/test_security.py) — HTTPS enforcement added
❌ - **Worked on**: Performance improvements (too vague)
❌ - **Made progress**: Testing (not specific)

Constraints:
- Minimum 1 accomplishment (every session does something)
- Maximum 10 accomplishments (focus on major items)
- Each accomplishment must reference a file/component or metric
```

### 2.3 Extract Technical Decisions

**Format:** Decision + rationale + impact

```markdown
For EACH explicit decision made:
- **[Decision topic]**: [What was decided] — [Rationale] — [Expected impact]

Examples:
✅ - **Rate limiting**: Token bucket algorithm — Better handles burst traffic than fixed window — Prevents abuse while allowing legitimate bursts
✅ - **Test parallelization**: n=16 for IO-bound tests — Network calls benefit from higher concurrency — 8x test speedup
❌ - **Code organization**: Moved files around (not a decision, just an action)

Constraints:
- Only include explicit architectural/technical decisions
- Must include rationale (why this over alternatives)
- Must note impact or trade-offs
- If no decisions made, write "None - Implementation session"
```

### 2.4 Extract Learnings and Insights

**Format:** Technology/pattern + insight + evidence

```markdown
For EACH technical learning:
- **[Technology/Pattern]**: [Specific insight] (include measurements/benchmarks)

Examples:
✅ - **pytest-xdist**: Auto scheduling performs 3x faster than loadscope for IO-bound tests (measured at n=16 workers)
✅ - **Markdown linting**: markdownlint-cli2 catches 40% more issues than markdownlint-cli (150+ violations found)
❌ - **Testing**: Tests are important (too generic, not a learning)
❌ - **Performance**: Made things faster (no measurement, no specifics)

Constraints:
- Minimum 0 learnings (routine work may not produce insights)
- Maximum 5 learnings (focus on significant insights)
- Must include quantitative evidence when possible
- Must be specific enough to apply in future sessions
```

### 2.5 Identify Patterns (Positive and Negative)

**Positive Patterns (What Worked Well):**

```markdown
For EACH effective pattern observed:
✅ [Pattern name]: [Description] — [Why it worked] — [Frequency: Always/Often/Sometimes]

Examples:
- **Batch file reads**: Using mcp0_read_multiple_files for 3+ files — 3x faster context loading — Always recommended
- **Test-first approach**: Writing tests before implementation — Caught 5 regressions early — Often useful for complex features
```

**Constraints:**

- Minimum 1 positive pattern
- Maximum 5 positive patterns
- Focus on repeatable, actionable patterns
- Include frequency guidance (when to apply)

**Negative Patterns (What Didn't Work):**

```markdown
For EACH ineffective pattern observed:
❌ [Pattern name]: [Description] — [Why it failed] — [Better alternative]

Examples:
- **Sequential file reads**: Reading files one-by-one — 3x slower than batch reads — Use mcp0_read_multiple_files instead
- **Pre-commit without formatting**: Committing without running formatters first — Required reset and re-commit — Always run 'task format' before committing
```

**Constraints:**

- Minimum 0 negative patterns (session may be flawless)
- Maximum 3 negative patterns
- Must include better alternative approach
- Focus on preventable issues

### 2.6 Identify High-Priority Gaps

**ONLY flag if critical impact:**

```markdown
For EACH critical gap or violation:
❌ [Gap category]: [What's missing/wrong] — [Impact] — [Recommended fix]

Categories:
- Protocol violations (Session End Protocol skipped, etc.)
- Critical tool/workflow gaps
- Security vulnerabilities discovered
- Documentation pollution (files in wrong location)

Constraints:
- Minimum 0 gaps (most sessions are compliant)
- Maximum 3 gaps (focus on critical issues only)
- Must explain impact (why this matters)
- Must propose concrete fix
- Do NOT include minor inconveniences
```

---

## Stage 3: Generate Structured Session Summary

**CRITICAL:** Use this EXACT template. Do not deviate from structure.

### 3.1 Session Summary Template

```markdown
# Session Summary: [Descriptive Title]

**Date:** YYYY-MM-DD
**Duration:** ~N hours (or ~N minutes)
**Focus:** [Primary focus area in 1-3 words]
**Workflows Used:** [List or "None (ad-hoc)"]

---

## Objectives

[2-4 sentences describing what this session aimed to accomplish. Include triggering context if relevant (e.g., "Continue from previous session on X" or "Address user request for Y").]

**Success Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

---

## Completed

### 1. [Major Task Category 1]

[Brief paragraph (2-4 sentences) providing context and narrative for this work. Explain why this was done, what challenges were encountered, and how they were resolved.]

**Accomplishments:**
- **[Action]**: [Specific accomplishment] ([File/Component]) — [Context]
- **[Action]**: [Specific accomplishment] ([File/Component]) — [Context]

**Key findings:** [1-2 sentences on discoveries or insights specific to this task]

### 2. [Major Task Category 2]

[Same structure...]

### N. [Additional categories as needed]

---

## Commits

[List commit hashes and messages in chronological order]

- `abc1234` - [conventional commit message]
- `def5678` - [conventional commit message]

**Commit quality:** [Brief assessment: well-scoped, atomic, good messages, etc.]

---

## Key Learnings

### Technical Insights (Minimum 0, Maximum 5)

1. **[Technology/Pattern]:** [Specific insight with measurements/benchmarks]
2. **[Technology/Pattern]:** [Specific insight with measurements/benchmarks]
[If none, write: "No significant technical insights this session (routine implementation work)"]

### Process Observations (Minimum 0, Maximum 3)

1. **[Process/Pattern]:** [What was learned about workflow, tooling, or collaboration]
[If none, write: "No process insights this session"]

---

## Identified Patterns

### ✅ Positive Patterns (Minimum 1, Maximum 5)

1. **[Pattern name]:** [Description] — [Why it worked] — [When to apply: Always/Often/Sometimes]
2. **[Pattern name]:** [Description] — [Why it worked] — [When to apply]

### ⚠️ Areas for Improvement (Minimum 0, Maximum 3)

[If any issues encountered:]

1. **[Issue pattern]:** [What happened] — [Why it's suboptimal] — [Better approach for next time]

[If none, write: "No significant friction or issues this session"]

---

## High-Priority Gaps (CRITICAL ISSUES ONLY)

[If any critical protocol violations, security issues, or workflow gaps:]

### ❌ [Gap Category]

- **Issue:** [Specific problem]
- **Impact:** [Why this matters]
- **Recommendation:** [Concrete fix]

[If none, write: "**None identified** — Session followed all protocols and best practices"]

---

## Changes Implemented

### Code Changes (If any)

**Files Modified:** [Count, or list if ≤5]

[Brief description of code changes by category:]
- **Feature:** [What was added]
- **Fix:** [What was repaired]
- **Refactor:** [What was improved]
- **Test:** [What test coverage was added]

### Documentation Changes (If any)

[List documentation updates:]
- [File path]: [What changed]
- [File path]: [What changed]

### Configuration Changes (If any)

[List config/tooling updates:]
- [File path]: [What changed and why]

---

## Deferred Items

[Items intentionally not addressed - NOT unresolved issues]

### Low-Priority Items NOT Addressed

1. **[Item]:** [What was deferred] — [Why deferred] — [Defer to: When/Condition]
2. **[Item]:** [What was deferred] — [Why deferred] — [Defer to: When/Condition]

[If none, write: "None - all identified work completed"]

---

## Verification

**How to verify this work:**

```text
# Command 1 to verify
[command with explanation]

# Command 2 to verify
[command with explanation]
```

**Expected outcomes:**

- [Specific expected result 1]
- [Specific expected result 2]

---

## Next Steps

### 🔴 Critical (Next Session)

[Highest priority items that must be addressed soon:]

1. **[Task]:** [What needs doing] — [Why critical] — [Owner/Dependency]

[If none, write: "None - no blocking issues"]

### 🟡 High Priority (This Week)

[Important but not urgent:]

1. **[Task]:** [What needs doing] — [Context] — [Estimated effort]

[If none, write: "None - current work stream complete"]

### 🟢 Medium Priority (Future)

[Nice to have items:]

1. **[Task]:** [What could be done] — [Context] — [Triggering condition]

[If none, write: "None"]

---

## Living Documentation Updates

**Check if updates needed:**

- [ ] **PROJECT_SUMMARY.md**: [Needs update? Yes/No — If yes, why]
- [ ] **CHANGELOG.md**: [Needs update? Yes/No — If yes, what to add]
- [ ] **Initiative files**: [Updated? List files if yes]
- [ ] **ADRs**: [Created/updated? List if yes]

**Actions taken:**
[If updates made, list them. If deferred, explain why]

---

## Metrics

| Metric | Count | Details |
|--------|-------|----------|
| **Files Modified** | N | [List if ≤5, else summarize by category] |
| **Commits** | N | [All used conventional format: Yes/No] |
| **Tests Added** | N | [Coverage impact if known] |
| **Tests Fixed** | N | [Which test suites] |
| **ADRs Created** | N | [List titles if any] |
| **Initiatives Updated** | N | [List names if any] |
| **Duration** | ~N hours | [Breakdown if multiple work streams] |

---

## Workflow Adherence

**Protocol Compliance:**

- ✅ Session summary created in proper location (`docs/archive/session-summaries/`)
- ✅ Meta-analysis workflow executed
- ✅ Timestamp file updated (`.windsurf/.last-meta-analysis`)
- ✅ All changes committed (git status clean or only timestamp file unstaged)
- ✅ Tests passing (if code changes made)
- ✅ Completed initiatives archived (if any)

[If any violations, note them here and propose improvements]

---

## Session References

- **Previous session:** [filename if continuation, or "None - new work stream"]
- **Related initiative:** [filepath if relevant]
- **External references:** [URLs to research/documentation if used]

---

**Metadata:**

- **Session type:** [Implementation / Planning / Research / Maintenance / Mixed]
- **Autonomy level:** [High / Medium / Low - based on user intervention needed]
- **Complexity:** [High / Medium / Low]
- **Quality:** ✅ [All objectives met / Partial / Issues encountered]

### 3.2 Length Constraints (LLM-Agnostic Quality Control)

**CRITICAL:** Follow these constraints to ensure consistency across different LLMs.

| Section | Minimum | Maximum | Target |
|---------|---------|---------|--------|
| **Objectives** | 2 sentences | 5 sentences | 3 sentences |
| **Task narrative** | 2 sentences | 4 sentences | 3 sentences |
| **Accomplishments** (total) | 1 item | 10 items | 5 items |
| **Technical Insights** | 0 items | 5 items | 2-3 items |
| **Positive Patterns** | 1 item | 5 items | 3 items |
| **Areas for Improvement** | 0 items | 3 items | 1-2 items |
| **High-Priority Gaps** | 0 items | 3 items | 0-1 items |
| **Next Steps (Critical)** | 0 items | 5 items | 2-3 items |
| **Next Steps (High)** | 0 items | 5 items | 2-3 items |
| **Total Summary Length** | 1000 words | 3000 words | 1500-2000 words |

**Enforcement Strategy:**

- If section exceeds maximum → Consolidate and prioritize
- If below minimum → Add necessary detail
- Use bullets and tables (not prose) where appropriate
- Preserve specific details (file paths, metrics, commands)

---

## Stage 4: Quality Validation

### 4.1 Validation Checklist

**Format Compliance:**

```markdown
✓ Exact template structure followed (all sections present)
✓ YAML frontmatter correct (date, duration, focus)
✓ All accomplishments use action verbs
✓ All accomplishments reference files/components or metrics
✓ All decisions include rationale
✓ All learnings include measurements where applicable
✓ Length constraints met for each section
✓ Tables formatted correctly
✓ Checkboxes use [ ] or [x] format
✓ File paths use backticks
✓ No vague language ("worked on", "made progress")
```

**Content Completeness:**

```markdown
✓ Objectives clearly stated with success criteria
✓ All commits listed in Commits section
✓ All files modified accounted for
✓ Key learnings captured (if any)
✓ Patterns identified (positive and negative)
✓ Next steps are specific and actionable
✓ Living documentation update status checked
✓ Metrics table complete
✓ Workflow adherence section confirms protocol compliance


**LLM-Agnostic Quality:**

```markdown
✓ Could another LLM generate similar output from same inputs?
✓ Are all facts verifiable from git/files?
✓ Are sections constrained to specified lengths?
✓ Is language concrete (not vague or subjective)?
✓ Are all technical claims supported by evidence?
```

### 4.2 Self-Review Questions

1. **Can someone reconstruct what happened from this summary?**
   If no → Add missing context

2. **Are all metrics verifiable from git/files?**
   If no → Correct or remove

3. **Is this summary LLM-agnostic (any model could produce it)?**
   If no → Remove model-specific biases

4. **Are all next steps specific and actionable?**
   If no → Add file references or specific details

5. **Does this follow all Session End Protocol requirements?**
   If no → Document violations and propose improvements

---

## Stage 5: File Creation and Commit

### 5.1 Create Session Summary File

**Naming convention:**

```bash
# Format: YYYY-MM-DD-descriptive-name.md
docs/archive/session-summaries/2025-10-16-windsurf-improvements.md

# Descriptive name should be:
# - 2-4 words (kebab-case)
# - Indicate primary focus
# - Unique for the day (if multiple sessions)
```

### 5.2 Write Content

1. Copy the template from Stage 3.1
2. Fill in extracted information from Stage 2
3. Follow length constraints from Stage 3.2
4. Run through validation checklist (Stage 4.1)

### 5.3 Update Timestamp File

```bash
# Update timestamp
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis

# Stage for commit
git add .windsurf/.last-meta-analysis
```

### 5.4 Commit Session Summary

```bash
# Stage session summary
git add docs/archive/session-summaries/YYYY-MM-DD-*.md

# Commit with conventional format
git commit -m "docs(session): add YYYY-MM-DD [focus area] session summary

  - Duration: ~N hours
  - Focus: [Primary focus]
  - Key accomplishments: [1-2 highlights]
```

---

## Stage 6: Living Documentation Check

**MANDATORY:** Check if PROJECT_SUMMARY or CHANGELOG needs updating.

### 6.1 PROJECT_SUMMARY.md Update Triggers

**Update if:**

- ✅ New major feature completed
- ✅ Significant milestone reached
- ✅ Architecture changes made
- ✅ New ADR created (add to ADR list)
- ✅ Initiative status changed (update status table)
- ✅ Metrics significantly changed (test coverage, type coverage, etc.)
- ✅ New dependencies added
- ✅ Major accomplishments (mention in "Recent Accomplishments")

**Skip if:**

- ❌ Routine bug fixes
- ❌ Minor documentation updates
- ❌ Internal refactoring (no user impact)
- ❌ Test additions (unless coverage milestone)

### 6.2 CHANGELOG.md Update Triggers

**Update if:**

- ✅ Preparing for release (version bump)
- ✅ Breaking changes made
- ✅ New features added (user-facing)
- ✅ Significant bugs fixed
- ✅ Dependencies updated (major versions)
- ✅ API changes

**Skip if:**

- ❌ Internal work (no release)
- ❌ Documentation-only changes
- ❌ Work-in-progress features
- ❌ Test improvements

### 6.3 Update Process

If updates needed:

```bash
# 1. Make updates to PROJECT_SUMMARY.md and/or CHANGELOG.md
# 2. Stage changes
git add PROJECT_SUMMARY.md docs/reference/CHANGELOG.md

# 3. Commit separately (after session summary)
git commit -m "docs: update PROJECT_SUMMARY and CHANGELOG for [feature/milestone]

- [Summary of what was updated]"
```

---

## Best Practices

### DO

✅ **Run at end of EVERY session** (part of Session End Protocol)
✅ **Follow template exactly** (ensures consistency)
✅ **Use concrete language** (verifiable facts, not vague statements)
✅ **Include measurements** (benchmarks, test counts, file counts)
✅ **Preserve technical details** (file paths, commands, metrics)
✅ **Check living documentation** (PROJECT_SUMMARY, CHANGELOG)
✅ **Be honest about issues** (document what went wrong)
✅ **Propose improvements** (workflow/rule changes to prevent issues)

### DON'T

❌ **Don't skip meta-analysis** (violates Session End Protocol)
❌ **Don't use vague language** ("worked on", "made progress")
❌ **Don't omit failures** (learnings come from mistakes)
❌ **Don't exceed length limits** (causes inconsistency across LLMs)
❌ **Don't skip validation** (quality depends on following checklist)
❌ **Don't forget timestamp** (breaks protocol monitoring)
❌ **Don't create summaries outside proper location** (causes documentation pollution)

---

## Success Criteria

- [ ] Session summary created in `docs/archive/session-summaries/`
- [ ] Timestamp file updated (`.windsurf/.last-meta-analysis`)
- [ ] Template structure followed exactly
- [ ] Length constraints met for all sections
- [ ] All validation checks passed
- [ ] Living documentation status checked
- [ ] Git commit completed with descriptive message
- [ ] Ready for next session (context preserved)

---

## Troubleshooting

**Issue:** "I don't know what to write in Technical Insights"

**Solution:** If no significant technical insights, write: "No significant technical insights this session (routine implementation work)". Not every session produces deep learnings.

**Issue:** "The summary feels too long/short"

**Solution:** Check length constraints table (Stage 3.2). Use bullets and tables to compress information. Remove redundant context.

**Issue:** "I violated Session End Protocol"

**Solution:** Document the violation in "High-Priority Gaps" section. Explain what went wrong, why, and propose workflow improvements to prevent recurrence.

**Issue:** "Should I update PROJECT_SUMMARY?"

**Solution:** Check Stage 6.1 triggers. When in doubt, lean toward updating (better to keep it current than let it stale).

---

## References

- [Session End Protocol](../.windsurf/rules/00_agent_directives.md#18-session-end-protocol) - Requirements
- [Consolidate Summaries Workflow](./consolidate-summaries.md) - Similar structured approach
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md) - Where summaries go
- [CONSTITUTION.md](../../docs/CONSTITUTION.md) - Documentation principles

---

**Last Updated:** 2025-10-16
**Version:** 2.0.0 (Structured LLM-agnostic approach)

---

## Workflow Changelog

### Version 2.0.0 (2025-10-16)

- **BREAKING:** Complete workflow overhaul for consistency and LLM-agnostic output
- Added: Chain-of-Thought structured extraction (Stage 2)
- Added: Strict template with all mandatory sections (Stage 3.1)
- Added: Length constraints table for quality control (Stage 3.2)
- Added: Comprehensive validation checklist (Stage 4)
- Added: Living documentation update protocol (Stage 6)
- Changed: Template structure now consistent with consolidate-summaries
- Changed: All sections have clear minimum/maximum constraints
- Improved: Concrete examples for each section type
- Improved: Self-review questions for quality assurance
- Research: Based on October 2025 prompt engineering best practices
  - Structured output formats (Windsurf documentation, 2025)
  - Length constraints for consistency (Lakera AI Guide, 2025)
  - LLM-agnostic design (Azure AI Agent Patterns, 2025)

### Version 1.0.0 (2025-10-15)

- Initial workflow version
- Basic session summary structure
- Protocol violation detection
