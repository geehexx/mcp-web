---
description: Systematic session review and improvement identification
auto_execution_mode: 3
---

# Meta-Analysis Workflow

**Purpose:** Systematically analyze AI agent sessions to identify improvement opportunities and create consistent, comprehensive session summaries.

**When to Use:** MANDATORY at the end of every work session (part of Session End Protocol)

**Philosophy:** Create LLM-agnostic session summaries that enable cross-session continuity and capture learnings.

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

---

## Stage 2: Extract Session Data

**Call `/extract-session` workflow:**

- Analyzes git history since last meta-analysis
- Extracts accomplishments, decisions, learnings
- Identifies positive and negative patterns
- Checks protocol compliance
- Returns structured data

**See:** `.windsurf/workflows/extract-session.md`

---

## Stage 3: Generate Session Summary

**Call `/summarize-session` workflow:**

- Uses structured template
- Applies length constraints for consistency
- Validates against checklist
- Creates file in proper location

**Output:** `docs/archive/session-summaries/YYYY-MM-DD-description.md`

**See:** `.windsurf/workflows/summarize-session.md`

---

## Stage 4: Living Documentation Check

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

Call `/update-docs` workflow to apply changes

**See:** `.windsurf/workflows/update-docs.md`

---

## Stage 5: Commit Session Summary

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
