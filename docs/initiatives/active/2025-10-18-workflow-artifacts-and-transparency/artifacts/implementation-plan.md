# Implementation Plan: Workflow Artifacts & Transparency Fixes

**Initiative:** 2025-10-18-workflow-artifacts-and-transparency
**Status:** In Progress
**Phase:** Implementation

---

## Changes Required

### ✅ Phase 1: File Structure (COMPLETE)

- [x] Move flat file to folder/initiative.md
- [x] Move PROPOSAL to new initiative artifacts
- [x] Verify structure compliant

### Phase 2: Core Workflow Updates (IN PROGRESS)

**Priority Workflows (Update First):**

1. **/work** - Master orchestrator
   - Add numbering: `1. /work - [description]`
   - Add transparency announcements
   - Add substask numbering logic

2. **/implement** - Implementation orchestrator
   - Add numbering: `1. /implement - [description]`
   - Add transparency announcements
   - Add ADR checkpoint

3. **/plan** - Planning orchestrator
   - Add numbering: `1. /plan - [description]`
   - Add ADR creation triggers
   - Add transparency announcements

### Phase 3: Specialized Workflow Updates

**Update These:**

4. /commit - Add version bump integration
5. /validate - Add numbering
6. /new-adr - Add numbering
7. /archive-initiative - Add numbering
8. /bump-version - Add numbering
9. /consolidate-summaries - Add numbering
10. /detect-context - Add numbering
11. /extract-session - Add numbering
12. /generate-plan - Add numbering
13. /load-context - Add numbering
14. /meta-analysis - Add numbering
15. /research - Add numbering
16. /summarize-session - Add numbering
17. /update-docs - Add numbering

### Phase 4: Rules & Documentation Updates

**Update Rules:**

- Section 1.11 (Task System Usage):
  - Add mandatory numbering requirement
  - Add workflow prefix requirement
  - Add transparency requirements
  - Add hierarchical numbering guide

- Section 1.6 (File Operations):
  - Add artifact management rules
  - Add when to use scaffold.py
  - Add structure decision tree

**Create Documentation:**

- Workflow Development Guide
- Task Numbering Conventions
- Transparency Best Practices

### Phase 5: Validation

- [ ] All workflows have proper numbering
- [ ] All workflows have transparency announcements
- [ ] Rules updated and validated
- [ ] Documentation complete
- [ ] Test workflow invocations
- [ ] Commit all changes

---

## Numbering Format Standard

### Basic Format

```typescript
{ step: "<number>. /<workflow> - <description>", status: "<status>" }
```

### Examples

**Top-level (no parent):**

```typescript
{ step: "1. /work - Detect project context", status: "in_progress" }
{ step: "2. /work - Route to appropriate workflow", status: "pending" }
```

**First-level subtasks (2-space indent):**

```typescript
{ step: "3. /work - Execute routed workflow", status: "in_progress" }
{ step: "  3.1. /implement - Load context files", status: "in_progress" }
{ step: "  3.2. /implement - Design test cases", status: "pending" }
```

**Second-level subtasks (4-space indent):**

```typescript
{ step: "  3.1. /implement - Load context", status: "in_progress" }
{ step: "    3.1.1. /implement - Read initiative file", status: "in_progress" }
{ step: "    3.1.2. /implement - Read source files", status: "pending" }
```

### Hierarchical Number Detection

**When child workflow called:**

1. Parse parent's current task number
2. If parent is `3. /work - Execute`, children are `3.1, 3.2, 3.3`
3. If parent is `3.2. /implement - Design`, children are `3.2.1, 3.2.2`
4. Use appropriate indentation (2 spaces per level)

**Logic:**

```python
def get_child_number(parent_number: str, child_index: int) -> str:
    """
    Examples:
    - get_child_number("3", 1) → "3.1"
    - get_child_number("3.2", 1) → "3.2.1"
    - get_child_number("3.2.1", 1) → "3.2.1.1"
    """
    return f"{parent_number}.{child_index}"

def get_indent(level: int) -> str:
    """
    Level 0: "" (no indent)
    Level 1: "  " (2 spaces)
    Level 2: "    " (4 spaces)
    """
    return "  " * level
```

---

## Transparency Format Standard

### Workflow Entry

**Format:** `🔄 **Entering [Stage/Section]: [Name]**`

**Example:**

```markdown
🔄 **Entering Stage 1: Create Initial Task Plan**

```typescript
update_plan({ ... })
```

### Task Updates

**Format:** `📋 **Task Update:** "[task]" → [status]`

**Example:**

```markdown
📋 **Task Update:** "1. /work - Detect context" → completed
📋 **Task Update:** "2. /work - Route to workflow" → in_progress
```

### Workflow Exit

**Format:** `✅ **Completed [Workflow/Stage]:** [Summary]**

**Example:**

```markdown
✅ **Completed /implement:** 3 files modified, 26 tests passing, all quality gates passed
```

### Important Milestones

**Format:** `ℹ️ **[Event]:** [Details]`

**Example:**

```markdown
ℹ️ **Routing Decision:** High confidence (90%) - continuing with /implement workflow
ℹ️ **Waiting for User:** Review changes before committing
```

---

## Implementation Strategy

### Batch 1: Critical Orchestrators (Do First)

1. Update /work with full example
2. Update /implement with full example
3. Update /plan with full example
4. Test these three work correctly together
5. Commit changes

### Batch 2: Specialized Workflows (Do Second)

6-17. Update remaining workflows with same pattern

- Copy-paste format from orchestrators
- Adjust numbering examples to fit workflow
- Add appropriate transparency points
- Commit in groups of 3-4

### Batch 3: Rules & Documentation (Do Third)

- Update Section 1.11 with mandatory requirements
- Update Section 1.6 with file operations guidance
- Create workflow development guide
- Commit documentation changes

### Batch 4: Validation (Do Last)

- Test each workflow manually
- Verify numbering works
- Verify transparency shows
- Fix any issues
- Final commit

---

## Testing Checklist

After implementation, verify:

- [ ] /work creates numbered tasks (1, 2, 3, ...)
- [ ] /work routes to child with subtasks (3.1, 3.2, 3.3, ...)
- [ ] Child workflow (/implement) uses parent numbering correctly
- [ ] All task updates show announcements
- [ ] Workflow entry/exit shows announcements
- [ ] Version bump triggers in /commit
- [ ] ADR creation triggers in /plan and /implement
- [ ] All workflows follow same format
- [ ] Rules updated and clear
- [ ] Documentation complete

---

## Risk Mitigation

**Risk:** Breaking existing workflows
**Mitigation:** Test after each batch, commit incrementally

**Risk:** Numbering logic complex
**Mitigation:** Provide clear examples, start simple (no nesting first)

**Risk:** Too many announcements (spam)
**Mitigation:** Only announce at major transitions, not every line

**Risk:** Forgot a workflow
**Mitigation:** Audit list of all workflows before starting

---

## Success Criteria

### Immediate (This Session)

- [ ] File structure fixed
- [ ] Core 3 workflows updated
- [ ] Rules updated
- [ ] Can demonstrate working example

### Complete (Full Implementation)

- [ ] All 17 workflows updated
- [ ] Documentation complete
- [ ] Validation passed
- [ ] User approves changes

---

**Status:** Phase 1 complete, Phase 2 in progress
**Next:** Update core orchestrator workflows (/work, /implement, /plan)
