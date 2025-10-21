---
created: "2025-10-17"
updated: "2025-10-19"
description: Systematic session review with intelligent consolidation detection
auto_execution_mode: 3
category: Analysis
complexity: 60
tokens: 3893
dependencies:
  - extract-session
  - summarize-session
  - consolidate-summaries
status: active
version: 2.0.0
---

# Meta-Analysis Workflow

**Purpose:** Systematically analyze AI agent sessions to identify improvement opportunities and create consistent, comprehensive session summaries.

**When to Use:** MANDATORY at the end of every work session (part of Session End Protocol)

**Philosophy:** Create LLM-agnostic session summaries that enable cross-session continuity and capture learnings.

---

## Stage 0: Create Task Plan

🔄 **Entering Stage 0: Create Task Plan**

**Print workflow entry announcement:**

```markdown
🔄 **Entering /meta-analysis:** Systematic session review and summary generation
```

**Create task plan:**

```typescript
update_plan({
  explanation: "📊 Starting /meta-analysis workflow",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "in_progress" },
    { step: "2. /meta-analysis - Check for existing summaries (consolidation detection)", status: "pending" },
    { step: "3. /meta-analysis - Extract and summarize session", status: "pending" },
    { step: "4. /meta-analysis - Check living documentation", status: "pending" },
    { step: "5. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

✓ Task plan created

---

## Stage 1: Protocol Check

### 1.1 Check Last Execution

```bash
# Verify when meta-analysis last ran
cat .windsurf/.last-meta-analysis 2>/dev/null || echo "NEVER"

# Warning if >24h or never run
```

### 1.2 Update Timestamp

```bash
# Write current timestamp
date -u +"%Y-%m-%dT%H:%M:%SZ" > .windsurf/.last-meta-analysis
```

**Purpose:** Track protocol adherence and detect violations

**Print stage completion:**

```markdown
📋 **Stage 1 Complete:** Protocol timestamp updated
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Protocol check complete",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "completed" },
    { step: "2. /meta-analysis - Check for existing summaries (consolidation detection)", status: "in_progress" },
    { step: "3. /meta-analysis - Extract and summarize session", status: "pending" },
    { step: "4. /meta-analysis - Check living documentation", status: "pending" },
    { step: "5. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

---

## Stage 2: Consolidation Detection

🔄 **Entering Stage 2: Consolidation Detection**

### 2.1 Check for Today's Summaries

```bash
# Get today's date
TODAY=$(date +"%Y-%m-%d")

# Check for existing summaries from today
ls -1 docs/archive/session-summaries/${TODAY}-*.md 2>/dev/null | wc -l
```

### 2.2 Consolidation Decision Logic

**CRITICAL:** Consolidation is RARE. Only consolidate when HIGH CONFIDENCE of:

1. Session continuation (not a new session)
2. High semantic overlap (same initiative/topic)
3. Low information loss risk

**IF existing summaries found for today:**

#### Step 1: Check conversation history (if available)

- Look for explicit session continuation signals
- Check if user said "continue from previous session"
- Verify initiative/topic mentioned in current conversation

#### Step 2: Analyze most recent summary

```bash
# Get most recent summary from today
LATEST=$(ls -t docs/archive/session-summaries/${TODAY}-*.md 2>/dev/null | head -1)

# Extract key indicators:
# - Primary initiative name
# - Focus area
# - Files modified
# - Commit messages
```

#### Step 3: Compare with current session

```bash
# Get current session info
git log --oneline --since="$(cat .windsurf/.last-meta-analysis)" | head -10

# Check overlap:
# - Same initiative mentioned?
# - Same files being modified?
# - Related commit messages?
# - Time gap < 2 hours?
```

#### Step 4: Calculate confidence score

| Signal | Weight | Check |
|--------|--------|-------|
| Same initiative in conversation history | 40% | Explicit mention |
| Same files modified (>50% overlap) | 25% | Git diff comparison |
| Time gap < 1 hour | 15% | Timestamp check |
| Related commit messages (semantic) | 10% | Keyword overlap |
| User explicitly said "continue" | 10% | Conversation analysis |

#### Confidence Threshold: 70%+

**Decision Matrix:**

| Confidence | Time Gap | Action |
|------------|----------|--------|
| ≥70% | <1h | **CONSOLIDATE** - High confidence continuation |
| ≥70% | 1-2h | **CONSOLIDATE** - Likely continuation |
| 50-69% | <1h | **SEPARATE** - Uncertain, preserve context |
| <50% | Any | **SEPARATE** - Different work, keep separate |
| Any | >2h | **SEPARATE** - Different session |

**NEVER consolidate if:**

- ❌ Different initiatives
- ❌ Unrelated file changes
- ❌ Time gap >2 hours
- ❌ Confidence <70%
- ❌ User started new topic

**Example Scenarios:**

✅ **CONSOLIDATE** (Confidence: 85%):

- Previous summary: "Workflow Transparency Initiative - Phase 2"
- Current session: User says "continue Phase 3 of transparency work"
- Same files: `.windsurf/workflows/*.md`
- Time gap: 45 minutes
- Commits: Both about workflow enhancements
➡️ **Action:** Merge into single comprehensive summary

❌ **SEPARATE** (Confidence: 35%):

- Previous summary: "Workflow Transparency Initiative"
- Current session: "Fix security vulnerabilities"
- Different files: `src/mcp_web/*.py` vs `.windsurf/workflows/*.md`
- Time gap: 3 hours
- Commits: Unrelated topics
➡️ **Action:** Create new summary, preserve previous context

❌ **SEPARATE** (Confidence: 55%):

- Previous summary: "Initiative planning"
- Current session: "Implementation work" (same initiative)
- Same files: 60% overlap
- Time gap: 30 minutes
- BUT: Different phase, different focus
➡️ **Action:** Keep separate - different aspects deserve separate summaries

### 2.3 Execute Consolidation (if triggered)

**If consolidation triggered:**

**Print delegation announcement:**

```markdown
↪️ **Delegating to /consolidate-summaries:** Merging with existing summary from today
```

**Add sub-workflow task:**

```typescript
update_plan({
  explanation: "↪️ Consolidating with existing summary",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "completed" },
    { step: "2. /meta-analysis - Check for existing summaries (consolidation detection)", status: "in_progress" },
    { step: "  2.1. /consolidate-summaries - Merge summaries", status: "in_progress" },
    { step: "3. /meta-analysis - Extract and summarize session", status: "pending" },
    { step: "4. /meta-analysis - Check living documentation", status: "pending" },
    { step: "5. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

**Call `/consolidate-summaries` with specific summaries:**

```bash
# Only consolidate the current session with the most recent summary
# NOT all summaries from today (preserves other unrelated sessions)
/consolidate-summaries --target "${LATEST}" --merge-with-current
```

**Note:** This consolidates ONLY the current session with the most recent summary,
preserving all other summaries from today as separate contexts.

**After consolidation returns:**

```markdown
📋 **Consolidation Complete:** Merged with existing summary
```

**SKIP to Stage 4** (living documentation check) - no need to extract/summarize again

### 2.4 Proceed with Normal Flow (if no consolidation)

**If no consolidation needed:**

**Print stage completion:**

```markdown
📋 **Stage 2 Complete:** No consolidation needed, proceeding with new summary
```

**Update task plan:**

```typescript
update_plan({
  explanation: "No consolidation needed",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "completed" },
    { step: "2. /meta-analysis - Check for existing summaries (consolidation detection)", status: "completed" },
    { step: "3. /meta-analysis - Extract and summarize session", status: "in_progress" },
    { step: "4. /meta-analysis - Check living documentation", status: "pending" },
    { step: "5. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

---

## Stage 3: Extract Session Data

🔄 **Entering Stage 3: Extract Session Data**

**Before calling `/extract-session`, add sub-workflow task:**

```typescript
update_plan({
  explanation: "↪️ Delegating to /extract-session",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "completed" },
    { step: "2. /meta-analysis - Check for existing summaries (consolidation detection)", status: "completed" },
    { step: "3. /meta-analysis - Extract and summarize session", status: "in_progress" },
    { step: "  3.1. /extract-session - Extract session data", status: "in_progress" },
    { step: "  3.2. /summarize-session - Generate formatted summary", status: "pending" },
    { step: "4. /meta-analysis - Check living documentation", status: "pending" },
    { step: "5. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

**Print delegation announcement:**

```markdown
↪️ **Delegating to /extract-session:** Analyzing git history and session artifacts
```

**Call `/extract-session` workflow:**

- Analyzes git history since last meta-analysis
- Extracts accomplishments, decisions, learnings
- Identifies positive and negative patterns
- Checks protocol compliance
- Returns structured data

**See:** `.windsurf/workflows/extract-session.md`

**After `/extract-session` returns, print completion:**

```markdown
📋 **Extraction Complete:** Session data structured for summary generation
```

---

## Stage 4: Generate Session Summary

🔄 **Entering Stage 4: Generate Session Summary**

**Before calling `/summarize-session`, update task:**

```typescript
update_plan({
  explanation: "↪️ Delegating to /summarize-session",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "completed" },
    { step: "2. /meta-analysis - Extract and summarize session", status: "in_progress" },
    { step: "  2.1. /extract-session - Extract session data", status: "completed" },
    { step: "  2.2. /summarize-session - Generate formatted summary", status: "in_progress" },
    { step: "3. /meta-analysis - Check living documentation", status: "pending" },
    { step: "4. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

**Print delegation announcement:**

```markdown
↪️ **Delegating to /summarize-session:** Creating formatted session summary
```

**Call `/summarize-session` workflow:**

- Uses structured template
- Applies length constraints for consistency
- Validates against checklist
- Creates file in proper location

**Output:** `docs/archive/session-summaries/YYYY-MM-DD-description.md`

**See:** `.windsurf/workflows/summarize-session.md`

**After `/summarize-session` returns, print completion:**

```markdown
📋 **Summary Complete:** Session summary created in docs/archive/session-summaries/
```

**Update task plan:**

```typescript
update_plan({
  explanation: "Session summary generated",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "completed" },
    { step: "2. /meta-analysis - Extract and summarize session", status: "completed" },
    { step: "  2.1. /extract-session - Extract session data", status: "completed" },
    { step: "  2.2. /summarize-session - Generate formatted summary", status: "completed" },
    { step: "3. /meta-analysis - Check living documentation", status: "in_progress" },
    { step: "4. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

---

## Stage 5: Living Documentation Check

🔄 **Entering Stage 5: Living Documentation Check**

### 4.1 PROJECT_SUMMARY.md Update Triggers

**Update if:**

- ✅ New major feature completed
- ✅ Significant milestone reached
- ✅ Architecture changes made
- ✅ New ADR created
- ✅ Initiative status changed
- ✅ Metrics significantly changed
- ✅ New dependencies added

**Skip if:**

- ❌ Routine bug fixes
- ❌ Minor documentation updates
- ❌ Internal refactoring
- ❌ Test additions (unless coverage milestone)

### 4.2 CHANGELOG.md Update Triggers

**Update if:**

- ✅ Preparing for release
- ✅ Breaking changes made
- ✅ New features added (user-facing)
- ✅ Significant bugs fixed
- ✅ Dependencies updated (major versions)

**Skip if:**

- ❌ Internal work (no release)
- ❌ Documentation-only changes
- ❌ Work-in-progress features

### 4.3 Apply Updates (if needed)

**If triggers met:**

**Print delegation announcement:**

```markdown
↪️ **Delegating to /update-docs:** Updating PROJECT_SUMMARY and CHANGELOG
```

**Add sub-workflow task before calling:**

```typescript
update_plan({
  explanation: "↪️ Delegating to /update-docs",
  plan: [
    // ... completed tasks ...
    { step: "3. /meta-analysis - Check living documentation", status: "in_progress" },
    { step: "  3.1. /update-docs - Update living documents", status: "in_progress" },
    { step: "4. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

Call `/update-docs` workflow to apply changes

**See:** `.windsurf/workflows/update-docs.md`

**After `/update-docs` returns (if called):**

```markdown
📋 **Documentation Updates Complete:** Living documents synchronized
```

**Print stage completion:**

```markdown
📋 **Stage 4 Complete:** Living documentation status verified
```

---

## Stage 6: Commit Session Summary

🔄 **Entering Stage 6: Commit Session Summary**

### 5.1 Stage Files

```bash
# Stage session summary and timestamp
git add docs/archive/session-summaries/YYYY-MM-DD-*.md
git add .windsurf/.last-meta-analysis
```

### 5.2 Commit

```bash
git commit -m "docs(session): add YYYY-MM-DD [focus] session summary

- Duration: ~N hours
- Focus: [Primary focus]
- Key accomplishments: [highlights]"
```

**Print workflow exit:**

```markdown
✅ **Completed /meta-analysis:** Session summary created and committed
```

---

## Success Criteria

**Meta-analysis is complete when:**

- [ ] Session summary created in `docs/archive/session-summaries/`
- [ ] Timestamp file updated (`.windsurf/.last-meta-analysis`)
- [ ] Living documentation status checked (PROJECT_SUMMARY, CHANGELOG)
- [ ] Updates applied if triggers met
- [ ] All changes committed with descriptive message
- [ ] Ready for next session (context preserved)

---

## Troubleshooting

**Issue:** "Should I update PROJECT_SUMMARY?"

**Solution:** Check Stage 4.1 triggers. When in doubt, lean toward updating (better current than stale).

**Issue:** "I violated Session End Protocol"

**Solution:** Document violation in session summary's "High-Priority Gaps" section. Propose workflow improvements.

**Issue:** "No significant learnings this session"

**Solution:** Write "No significant technical insights (routine implementation work)". Not every session produces deep learnings.

---

## Integration

### Called By

- `/work` - MANDATORY at session end
- User - Direct invocation

### Calls

- `/extract-session` - Extract structured session data (Stage 2)
- `/summarize-session` - Generate formatted summary (Stage 3)
- `/update-docs` - Update living documentation if needed (Stage 4)

---

## References

- `.windsurf/workflows/extract-session.md` - Data extraction
- `.windsurf/workflows/summarize-session.md` - Summary generation
- `.windsurf/workflows/update-docs.md` - Living documentation updates
- `.windsurf/rules/10_session_protocols.md` - Session End Protocol
- `docs/DOCUMENTATION_STRUCTURE.md` - Where summaries go
