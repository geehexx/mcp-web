---
description: Archive completed initiative or handle superseded initiatives
title: Archive Initiative Workflow
type: workflow
category: Documentation
complexity: moderate
dependencies: ['scripts/validate_archival.py']
status: active
created: 2025-10-22
updated: 2025-10-22
---

# Archive Initiative Workflow

Archive completed initiatives with validation and automation.

## Stage 1: Task Plan

```typescript
update_plan({
  explanation: "📦 /archive-initiative",
  plan: [
    { step: "1. Validate gates", status: "in_progress" },
    { step: "2. Execute archival", status: "pending" },
    { step: "3. Commit", status: "pending" }
  ]
})
```

## Stage 2: Validation (MANDATORY)

```bash
python scripts/validate_archival.py docs/initiatives/active/[name]/initiative.md
```

**Gates:** Status=Completed, Success Criteria all checked, No blockers, No dependents, Completion entry

**Exit:** 0=Pass, 1=Fail

**CRITICAL failures:** Fix, re-run (cannot bypass)
**WARNING failures:** Fix or force:

```bash
python scripts/validate_archival.py \
  docs/initiatives/active/[name]/initiative.md \
  --force
```

## Stage 3: Execute Archival

### 3.1 Move Initiative

**Move to archive:**

```bash
mv docs/initiatives/active/[name] docs/initiatives/archive/[name]
```

### 3.2 Update Initiative Status

**Update initiative file:**

```markdown
---
Status: "Archived"
Completed: "YYYY-MM-DD"
Archived: "YYYY-MM-DD"
# ... other metadata
---
```

### 3.3 Create Archive Entry

**Add to archive index:**

```markdown
## [Initiative Name]

**Status:** Archived
**Completed:** YYYY-MM-DD
**Duration:** X weeks
**Outcome:** [Success/Failure/Partial]
**Key Deliverables:** [List of key deliverables]
**Lessons Learned:** [Key lessons learned]
```

## Stage 4: Update Related Documentation

### 4.1 Update Project Status

**Update project documentation:**

- Remove from active initiatives list
- Add to completed initiatives list
- Update project status

### 4.2 Update Dependencies

**Update dependent initiatives:**

- Remove dependencies on archived initiative
- Update status if dependencies were blocking
- Notify stakeholders of changes

### 4.3 Update Metrics

**Update project metrics:**

- Completion rate
- Average duration
- Success rate
- Lessons learned

## Stage 5: Clean Up

### 5.1 Remove Temporary Files

**Clean up temporary files:**

- Remove draft documents
- Clean up artifacts
- Remove temporary configurations

### 5.2 Archive Artifacts

**Move artifacts to archive:**

- Move to archive/artifacts/
- Organize by date
- Ensure accessibility

## Stage 6: Commit Changes

### 6.1 Commit Archive

```bash
git add docs/initiatives/archive/[name]/
git add docs/initiatives/archive/README.md
git commit -m "docs(initiative): archive [name] initiative

- Status: Completed
- Duration: X weeks
- Outcome: [Success/Failure/Partial]
- Key Deliverables: [List]"
```

### 6.2 Update Index

```bash
git add docs/initiatives/README.md
git commit -m "docs(initiative): update index for archived [name]"
```

## Context Loading

Load these rules if you determine you need them based on their descriptions:

- **Documentation Standards**: `/rules/03_documentation.mdc` - Apply when updating documentation and archives
- **Context Optimization**: `/rules/07_context_optimization.mdc` - Apply when dealing with large files or complex operations

## Workflow References

When this archive-initiative workflow is called:

1. **Load**: `/commands/archive-initiative.md`
2. **Execute**: Follow the archival stages defined above
3. **Validate**: Ensure all gates are met
4. **Archive**: Move initiative to archive
5. **Update**: Update related documentation

## Anti-Patterns

❌ **Don't:**

- Skip validation
- Archive incomplete initiatives
- Ignore dependencies
- Skip documentation updates

✅ **Do:**

- Validate all gates
- Ensure completion
- Check dependencies
- Update all documentation

## Success Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Validation passes | 100% | ✅ |
| Documentation updated | 100% | ✅ |
| Dependencies resolved | 100% | ✅ |
| Archive organized | 100% | ✅ |

## Integration

**Called By:**

- `/work` - Session end protocol
- User - Direct invocation for archival

**Calls:**

- `scripts/validate_archival.py` - Validation script
- Various file operations

**Exit:**

```markdown
✅ **Completed /archive-initiative:** Initiative archival finished
```

---

## Command Metadata

**File:** `archive-initiative.yaml`
**Type:** Command/Workflow
**Complexity:** Moderate
**Estimated Tokens:** ~1,100
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Initiative archival
- Validation processes
- Documentation updates
- Cleanup procedures

**Dependencies:**

- scripts/validate_archival.py - Validation script
