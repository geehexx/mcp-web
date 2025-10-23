---
description: Generate formatted session summary from extracted data
title: Summarize Session Workflow
type: workflow
category: Analysis
complexity: moderate
dependencies: ['extract-session']
status: active
created: 2025-10-22
updated: 2025-10-22
---

related: []

# Summarize Session Workflow

Generate LLM-agnostic session summary using structured template.

**Called by:** `/meta-analysis`
**Input:** Extraction data from `/extract-session`

## Template Structure & Constraints

| Section | Min | Max | Target |
|---------|-----|-----|--------|
| Header | - | - | Required |
| Objectives | 2 sent | 5 sent | 3 sent |
| Completed Work | 1 | 10 items | 5 items |
| Commits | - | - | All |
| Learnings | 0 | 5 items | 2-3 |
| Patterns (+) | 1 | 5 items | 3 |
| Patterns (!) | 0 | 3 items | 1-2 |
| Gaps | 0 | 3 items | 0-1 |
| Next Steps | 0 | 5 items | 2-3 |
| Living Docs | - | - | Required |
| Metrics | - | - | Required |
| Protocol | - | - | Required |
| **Total** | 1000w | 3000w | 1500-2000w |

## Generation Process

### 1. Header

```markdown
# Session Summary: [Title]

**Date:** YYYY-MM-DD
**Duration:** X hours
**Context:** [Initiative/Phase]
**Status:** [Completed/In Progress/Blocked]
```

### 2. Objectives

**Session goals and focus:**

- Primary objective 1
- Primary objective 2
- Primary objective 3

### 3. Completed Work

**Major accomplishments:**

- [ ] Accomplishment 1
- [ ] Accomplishment 2
- [ ] Accomplishment 3
- [ ] Accomplishment 4
- [ ] Accomplishment 5

### 4. Commits

**All commits in session:**

```markdown
## Commits

- `abc123` feat(workflows): add new workflow
- `def456` fix(adapter): handle edge case
- `ghi789` docs(readme): update documentation
```

### 5. Learnings

**Key insights gained:**

- Learning 1: [Description]
- Learning 2: [Description]
- Learning 3: [Description]

### 6. Patterns (+)

**Positive patterns observed:**

- Pattern 1: [Description]
- Pattern 2: [Description]
- Pattern 3: [Description]

### 7. Patterns (!)

**Areas for improvement:**

- Pattern 1: [Description]
- Pattern 2: [Description]

### 8. Gaps

**Identified gaps:**

- Gap 1: [Description]

### 9. Next Steps

**Immediate next actions:**

- [ ] Next step 1
- [ ] Next step 2
- [ ] Next step 3

### 10. Living Documentation

**Documentation updates needed:**

- [ ] Update ARCHITECTURE.md
- [ ] Update CONSTITUTION.md
- [ ] Update README.md

### 11. Metrics

**Session metrics:**

- **Duration:** X hours
- **Commits:** Y commits
- **Files Changed:** Z files
- **Tests:** A passed, B failed
- **Workflows Used:** C workflows

### 12. Protocol

**Session end protocol:**

- [ ] All changes committed
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Session summary created

## Stage 1: Process Session Data

### 1.1 Load Extraction Data

**Load session data from extract-session:**

- Session metadata
- Commit information
- File changes
- Test results
- Workflow usage

### 1.2 Analyze Patterns

**Identify patterns:**

- Work patterns
- Error patterns
- Success patterns
- Improvement areas

### 1.3 Extract Key Information

**Extract key details:**

- Major accomplishments
- Important learnings
- Critical gaps
- Next steps

## Stage 2: Generate Summary

### 2.1 Create Header

**Generate session header:**

- Title based on work done
- Date and duration
- Context and status

### 2.2 Write Objectives

**Document session objectives:**

- Primary goals
- Secondary goals
- Success criteria

### 2.3 List Completed Work

**Document accomplishments:**

- Major features
- Bug fixes
- Documentation
- Improvements

### 2.4 Document Commits

**List all commits:**

- Commit hash
- Type and scope
- Description
- Impact

## Stage 3: Analyze and Learn

### 3.1 Identify Learnings

**Extract key insights:**

- Technical learnings
- Process learnings
- Tool learnings
- Best practices

### 3.2 Recognize Patterns

**Identify patterns:**

- Positive patterns to repeat
- Negative patterns to avoid
- Improvement opportunities
- Success factors

### 3.3 Identify Gaps

**Find knowledge gaps:**

- Missing information
- Unclear requirements
- Technical unknowns
- Process gaps

## Stage 4: Plan Next Steps

### 4.1 Immediate Actions

**Define next steps:**

- Immediate tasks
- Priority order
- Dependencies
- Timeline

### 4.2 Documentation Updates

**Identify doc updates:**

- Architecture changes
- Process changes
- New patterns
- Updated standards

## Stage 5: Generate Metrics

### 5.1 Session Metrics

**Calculate session metrics:**

- Duration
- Productivity
- Quality
- Efficiency

### 5.2 Work Metrics

**Measure work output:**

- Commits
- Files changed
- Tests written
- Documentation updated

## Stage 6: Finalize Summary

### 6.1 Review Content

**Check summary quality:**

- Completeness
- Accuracy
- Clarity
- Actionability

### 6.2 Format Output

**Format final summary:**

- Markdown formatting
- Consistent structure
- Clear sections
- Readable format

### 6.3 Save Summary

**Save session summary:**

- File: `docs/archive/session-summaries/YYYY-MM-DD-HHMMSS-session-summary.md`
- Format: Markdown
- Encoding: UTF-8

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Documentation Standards**: `/rules/03_documentation.mdc` - Apply when creating documentation and summaries
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations

## Workflow References

When this summarize-session workflow is called:

1. **Load**: `/commands/summarize-session.md`
2. **Execute**: Follow the summarization stages defined above
3. **Process**: Analyze session data
4. **Generate**: Create structured summary
5. **Save**: Store summary file

## Anti-Patterns

❌ **Don't:**

- Skip data analysis
- Ignore patterns
- Create incomplete summaries
- Skip documentation updates

✅ **Do:**

- Analyze all data thoroughly
- Identify key patterns
- Create complete summaries
- Update documentation

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Summary completeness | 100% | ✅ |
| Pattern identification | 90%+ | ✅ |
| Documentation updates | 100% | ✅ |
| Actionability | High | ✅ |

## Integration

**Called By:**

- `/meta-analysis` - Session analysis workflow
- User - Direct invocation for session summarization

**Calls:**

- `/extract-session` - Session data extraction
- Various analysis tools

**Exit:**

```markdown
✅ **Completed /summarize-session:** Session summarization finished
```

## Command Metadata

**File:** `summarize-session.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,000
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Session summarization
- Pattern analysis
- Documentation updates
- Metrics generation

**Dependencies:**

- /extract-session - Session data extraction
