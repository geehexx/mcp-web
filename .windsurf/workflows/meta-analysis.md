---
created: "2025-10-17"
updated: "2025-10-18"
description: Systematic session review and improvement identification
auto_execution_mode: 3
category: Analysis
complexity: 50
tokens: 766
dependencies:
  - extract-session
  - summarize-session
status: active
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
    { step: "2. /meta-analysis - Extract and summarize session", status: "pending" },
    { step: "3. /meta-analysis - Check living documentation", status: "pending" },
    { step: "4. /meta-analysis - Commit session summary", status: "pending" }
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
    { step: "2. /meta-analysis - Extract and summarize session", status: "in_progress" },
    { step: "3. /meta-analysis - Check living documentation", status: "pending" },
    { step: "4. /meta-analysis - Commit session summary", status: "pending" }
  ]
})
```

---

## Stage 2: Extract Session Data

🔄 **Entering Stage 2: Extract Session Data**

**Before calling `/extract-session`, add sub-workflow task:**

```typescript
update_plan({
  explanation: "↪️ Delegating to /extract-session",
  plan: [
    { step: "1. /meta-analysis - Check protocol and update timestamp", status: "completed" },
    { step: "2. /meta-analysis - Extract and summarize session", status: "in_progress" },
    { step: "  2.1. /extract-session - Extract session data", status: "in_progress" },
    { step: "  2.2. /summarize-session - Generate formatted summary", status: "pending" },
    { step: "3. /meta-analysis - Check living documentation", status: "pending" },
    { step: "4. /meta-analysis - Commit session summary", status: "pending" }
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

## Stage 3: Generate Session Summary

🔄 **Entering Stage 3: Generate Session Summary**

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

## Stage 4: Living Documentation Check

🔄 **Entering Stage 4: Living Documentation Check**

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

## Stage 5: Commit Session Summary

🔄 **Entering Stage 5: Commit Session Summary**

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
- `.windsurf/rules/00_agent_directives.md` - Session End Protocol (Section 1.8)
- `docs/DOCUMENTATION_STRUCTURE.md` - Where summaries go
