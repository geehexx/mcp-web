# Workflow Artifacts & Transparency Issues - Root Cause Analysis

**Date:** 2025-10-18
**Status:** Analysis Complete
**Category:** Critical System Issues

---

## Executive Summary

Multiple systemic issues discovered affecting workflow outputs, task transparency, and artifact management:

1. **File Structure Violations:** Both flat and folder formats created simultaneously
2. **Missing Task Numbering:** No hierarchical numbering in workflow task generation
3. **Missing Transparency:** Silent task updates, no workflow announcements
4. **Missing Workflow Calls:** Version bumping, ADR creation not triggered
5. **Section Numbering Inconsistencies:** Workflow sections out of sync

**Impact:** User confusion, broken conventions, lost track of work, hard to follow progress

**Root Cause:** Task system integration (2025-10-18) added `update_plan` calls but didn't add numbering or transparency requirements

---

## Issue 1: File Structure Violation

### Problem

In commit `487eae7` (2025-10-18), created both:

- `docs/initiatives/active/2025-10-18-workflow-automation-enhancement.md` (flat file)
- `docs/initiatives/active/2025-10-18-workflow-automation-enhancement/` (folder with subdocs)

This violates ADR-0013 hybrid structure rules:

- **Rule:** Use flat file XOR folder structure, not both
- **Decision criteria:**
  - Flat file: <1000 words, single phase, no artifacts
  - Folder: >1000 words, multiple phases, OR has artifacts

### Root Cause

Scaffolding system wasn't used (didn't exist yet). Manual creation didn't follow decision tree.

**Additional Issue:** `PROPOSAL-folder-based-structure.md` left in `active/` after implementation

- Should have been moved to artifacts or archived
- Created in commit `6f3867f`, never cleaned up

### Impact

- Confusing structure for both AI and humans
- Unclear which file is source of truth
- Violates standards we established

### Solution Design

**Immediate Fix:**

1. Move main content from flat file into folder as `initiative.md`
2. Delete redundant flat file
3. Archive or move PROPOSAL to appropriate location

**Prevention:**

1. Always use scaffold.py for new initiatives
2. Add pre-commit validation for structure violations
3. Document in workflow when to use flat vs folder

---

## Issue 2: Missing Task Numbering

### Problem

**Current Task Creation (ALL workflows):**

```typescript
update_plan({
  explanation: "Starting implementation workflow",
  plan: [
    { step: "Load context files", status: "in_progress" },
    { step: "Design test cases (TDD)", status: "pending" },
    { step: "Write failing tests", status: "pending" }
  ]
})
```

**Expected Task Creation:**

```typescript
update_plan({
  explanation: "Starting /implement workflow",
  plan: [
    { step: "1. /implement - Load context files", status: "in_progress" },
    { step: "2. /implement - Design test cases (TDD)", status: "pending" },
    { step: "3. /implement - Write failing tests", status: "pending" }
  ]
})
```

**When child workflow called:**

```typescript
update_plan({
  explanation: "Routing to /implement workflow. Adding implementation subtasks.",
  plan: [
    { step: "1. /work - Detect project context", status: "completed" },
    { step: "2. /work - Route to appropriate workflow", status: "completed" },
    { step: "3. /work - Execute routed workflow", status: "in_progress" },
    { step: "3.1. /implement - Load context files", status: "in_progress" },  // Child numbering!
    { step: "3.2. /implement - Design test cases (TDD)", status: "pending" },
    { step: "3.3. /implement - Write failing tests", status: "pending" },
    // ... rest of subtasks ...
    { step: "4. /work - Session end protocol", status: "pending" }
  ]
})
```

### Root Cause

Task system integration (commit `9e221ac`, 2025-10-18) added `update_plan` calls but:

- Didn't specify numbering format in examples
- Didn't update Section 1.11 to require numbering
- Didn't add workflow prefix requirement

**Research Confirms:** Microsoft Project uses WBS (Work Breakdown Structure) numbering: `1, 1.1, 1.2, 1.2.1, 5.3` etc.

- Source: https://www.tacticalprojectmanager.com/task-numbers-ms-project/
- Standard format: `<number>. <workflow> - <description>`

### Impact

- User can't tell which workflow created which task
- Can't see hierarchical relationships
- Hard to reference specific tasks ("the 3rd subtask of implementation")
- Loses track of where we are in process

### Solution Design

**Numbering Rules:**

1. **Top-level tasks:** `1. /workflow - Description`
2. **First-level subtasks:** `1.1. /workflow - Description` (2-space indent)
3. **Second-level subtasks:** `1.1.1. /workflow - Description` (4-space indent)
4. **Format:** Always include period after number, workflow name, dash, then description

**Parent-Child Awareness:**

When child workflow is called, it must:

1. Detect parent's last task number (e.g., "3. /work - Execute routed workflow")
2. Generate child numbers as 3.1, 3.2, 3.3, etc.
3. Insert between parent's current task and next task
4. When child completes, parent continues from next number (4, 5, etc.)

**Nested Example:**

```text
1. /work - Detect context
2. /work - Route to workflow
3. /work - Execute workflow (in_progress)
  3.1. /implement - Load context (in_progress)
    3.1.1. /implement - Read initiative file
    3.1.2. /implement - Read source files
  3.2. /implement - Design tests (pending)
  3.3. /implement - Write tests (pending)
4. /work - Session end protocol (pending)
```

**Implementation:**

1. Update ALL workflow templates with numbered examples
2. Update Section 1.11 (Task System Usage) to mandate numbering
3. Create helper guidance: "If parent task is X.Y, child tasks are X.Y.1, X.Y.2, ..."
4. Add to agent directives: "MUST include number, period, workflow prefix in all tasks"

---

## Issue 3: Missing Transparency

### Problem

**Current Behavior:**

- Task updates happen silently
- Workflow transitions invisible
- User has no visual feedback

**User Experience:**

```text
[Agent working silently]
[Agent working silently]
[Agent working silently]
[Suddenly: "Here's what I did"]
```

**Desired Experience:**

```text
🔄 Entering /work workflow
📋 Updating tasks: Detect context → in_progress
✅ Context detection complete
📋 Updating tasks: Detect context → completed, Route to workflow → in_progress
🔀 Routing to /implement workflow
📋 Updating tasks: Adding implementation subtasks
✅ Implementation complete
```

### Root Cause

No guidance in workflows or rules about announcing:

- Workflow entry/exit
- Task transitions
- Important milestones

### Impact

- User doesn't know what's happening
- Can't tell if agent is stuck or working
- Hard to interrupt at right moment
- No sense of progress

### Solution Design

**Transparency Requirements (add to Section 1.11):**

1. **Workflow Entry:** Announce when entering major workflow section
   - Format: `🔄 **Entering [Stage X]: [Description]**`
   - Example: `🔄 **Entering Stage 2: Context Detection**`

2. **Task Updates:** Always show task transition
   - Format: `📋 **Task Update:** [old status] → [new status]`
   - Example: `📋 **Task Update:** "1. /work - Detect context" → completed`

3. **Workflow Exit:** Announce when completing major workflow
   - Format: `✅ **Completed [Workflow]:** [Summary]`
   - Example: `✅ **Completed /implement:** 3 files modified, all tests passing`

4. **Important Milestones:** Announce significant events
   - Routing decisions
   - Error recovery
   - Waiting for user input

**Printing Strategy:**

```markdown
BEFORE calling update_plan:
1. Print announcement to user
2. Call update_plan
3. Continue with work

Example:
```text
🔄 **Entering Stage 1: Create Initial Task Plan**

```typescript
update_plan({ ... })
```text

✓ Task plan created with 5 items
```

**Implementation:**

1. Update Section 1.11 with transparency requirements
2. Update ALL workflow templates with announcement examples
3. Add anti-pattern: "Don't make task updates silently"
4. Validate: Every `update_plan` call should have announcement before/after

---

## Issue 4: Missing Workflow Calls

### Problem

**Version Bumping:**

- `/bump-version` workflow exists but not called automatically
- Changes to conventional commits should trigger version bump
- Results should bubble up to parent workflow summaries

**ADR Creation:**

- `/new-adr` workflow exists but not called when needed
- No guidance in workflows about WHEN to create ADR
- Architectural decisions happen without documentation

### Root Cause

**Version Bumping:**

- `/commit` workflow doesn't call `/bump-version`
- No trigger logic for when bump is needed
- No integration with changelog

**ADR Creation:**

- Workflows mention ADR but don't specify triggers
- `/plan` workflow has "ADR Required: Yes/No" but no automation
- `/implement` mentions calling `/new-adr` but no clear criteria

### Impact

- Versions not bumped consistently
- Architectural decisions undocumented
- Missing cross-references in commits
- Lost history of why decisions made

### Solution Design

**Version Bumping Integration:**

1. **Update `/commit` workflow:**
   - After successful commit, check if version bump needed
   - Logic: If commit type is `feat` or `fix` or `breaking`, check if bump appropriate
   - Call `/bump-version` if needed
   - Report version change in summary

2. **Bubble Up Results:**
   - `/commit` reports to `/implement`: "Committed [sha] + bumped version to X.Y.Z"
   - `/implement` reports to `/work`: "Implementation complete, version bumped"
   - `/work` includes in session summary

**ADR Creation Triggers (add to workflows):**

1. **/plan workflow:**
   - Section 6.1: "If architectural decision required, call `/new-adr`"
   - **Triggers:**
     - Significant architecture change
     - Technology choice with long-term impact
     - Security pattern adoption
     - Breaking change to public API
   - Automate: If any trigger detected during planning, create ADR immediately

2. **/implement workflow:**
   - Add Stage 1.5: "Check if ADR needed"
   - If making architectural choice during implementation, pause and create ADR
   - Link ADR in commit message

**Implementation:**

1. Update `/commit` workflow with version bump logic
2. Update `/plan` workflow Section 6.1 with explicit triggers
3. Update `/implement` workflow with ADR checkpoint
4. Add to Section 1.6: "When architectural decisions made, MUST create ADR"

---

## Issue 5: Section Numbering Inconsistencies

### Problem

**In `work.md`:**

- User already fixed some: Stages 5.1-5.5 (Session End Protocol substages)
- User added Stage 6 (Continue Working)
- But other workflows may have inconsistencies

**Pattern:** When sections converted to headings, numbering fell out of sync with siblings/parents

### Root Cause

- Originally numbered lists converted to `##` headings
- Manual renumbering incomplete
- No validation that numbering is sequential

### Impact

- Hard to reference specific sections
- Breaks cross-references
- Confusing navigation

### Solution Design

**Audit All Workflows:**

1. Check every workflow for section numbering
2. Verify:
   - Sequential numbering (no skips)
   - Parent-child relationships correct
   - Siblings at same level use same numbering depth
   - Cross-references use correct numbers

**Standard Format:**

```markdown
## Stage 1: Title
### 1.1 Subsection
### 1.2 Subsection
## Stage 2: Title
### 2.1 Subsection
#### 2.1.1 Sub-subsection
#### 2.1.2 Sub-subsection
### 2.2 Subsection
```

**Implementation:**

1. Audit all 17 workflows
2. Fix numbering inconsistencies
3. Add to workflow template: "Use sequential numbering"
4. Consider: Pre-commit hook to validate section numbering

---

## Prevention Strategy

### Immediate Actions

1. **Fix Current Issues:**
   - Resolve file structure violation
   - Add numbering to all workflows
   - Add transparency requirements
   - Add missing workflow calls
   - Fix section numbering

2. **Update Rules:**
   - Section 1.11: Mandate numbering and transparency
   - Section 1.6: File operations guidance
   - Add anti-patterns for each issue

3. **Update Workflows:**
   - All workflows get numbered examples
   - All workflows get transparency examples
   - /commit gets version bump integration
   - /plan and /implement get ADR triggers

### Long-Term Prevention

1. **Pre-Commit Validation:**
   - Check for file structure violations
   - Validate section numbering sequences
   - Check for missing workflow prefixes

2. **Workflow Templates:**
   - Create standardized workflow template
   - Includes numbering placeholders
   - Includes transparency placeholders
   - Makes it obvious what's required

3. **Documentation:**
   - Create "Workflow Development Guide"
   - Include all conventions
   - Provide copy-paste examples
   - Link from ADR-0002

4. **Testing:**
   - Add workflow linting
   - Check for required patterns
   - Validate cross-references

---

## Implementation Priority

### Phase 1: Critical Fixes (This Session)

1. ✅ Fix file structure violation
2. ✅ Add numbering to core workflows (/work, /implement, /plan)
3. ✅ Add transparency requirements to Section 1.11
4. ✅ Update workflow templates with examples

### Phase 2: Missing Integrations (This Session)

5. ✅ Add version bump to /commit
6. ✅ Add ADR triggers to /plan and /implement
7. ✅ Fix all section numbering

### Phase 3: Documentation (This Session)

8. ✅ Update all affected rules
9. ✅ Create comprehensive guide
10. ✅ Document conventions

### Phase 4: Prevention (Future Session)

11. ⏭️ Create pre-commit validation
12. ⏭️ Create workflow template
13. ⏭️ Add workflow linting
14. ⏭️ Testing framework

---

## Success Criteria

**This Session:**

- [ ] File structure compliant with ADR-0013
- [ ] All core workflows have numbered tasks
- [ ] Transparency requirements in rules
- [ ] Version bump integrated
- [ ] ADR triggers documented
- [ ] Section numbering fixed
- [ ] All changes committed and validated

**Future Validation:**

- [ ] Pre-commit catches structure violations
- [ ] Workflow template used for new workflows
- [ ] No more silent task updates
- [ ] ADRs created when needed
- [ ] Versions bumped appropriately

---

## References

- **Task System Integration:** Session 2025-10-18 (commit 9e221ac)
- **Folder-Based Structure:** ADR-0013, Session 2025-10-18 (commit 6f3867f)
- **Session End Protocol:** Rule 1.8, Session 2025-10-18 (workflow fixes)
- **WBS Numbering:** https://www.tacticalprojectmanager.com/task-numbers-ms-project/
- **Conventional Commits:** https://www.conventionalcommits.org/

---

**Analysis Status:** ✅ Complete
**Ready For:** Implementation Phase
**Estimated Effort:** 3-4 hours (comprehensive fixes across 17 workflows)
