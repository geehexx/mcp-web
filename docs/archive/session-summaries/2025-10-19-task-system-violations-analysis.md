# Task System Violations Analysis - 2025-10-19 Session

**Date:** 2025-10-19
**Session:** Phase 5 YAML Frontmatter Implementation
**Issue:** Multiple violations of task system rules discovered during session

---

## Violations Identified

### 1. Missing Workflow Names in Tasks

**Rule Violated:** Section 1.11.1 - "EVERY task MUST have `<number>. /<workflow> - <description>` format"

**Examples from session:**
- ❌ `"4.2. Add frontmatter to all workflows (batch 1-8)"`
- ❌ `"4.3. Add frontmatter to all workflows (batch 9-19)"`
- ❌ `"4.4. Add frontmatter to all rules"`
- ❌ `"4.5. Create validation script"`
- ❌ `"4.6. Generate documentation indexes"`
- ❌ `"4.7. Fix validation issues"`

**Should have been:**
- ✅ `"4.2. /implement - Add frontmatter to all workflows (batch 1-8)"`
- ✅ `"4.3. /implement - Add frontmatter to all workflows (batch 9-19)"`
- ✅ `"4.4. /implement - Add frontmatter to all rules"`
- ✅ `"4.5. /implement - Create validation script"`
- ✅ `"4.6. /implement - Generate documentation indexes"`
- ✅ `"4.7. /implement - Fix validation issues"`

### 2. Removing Completed Tasks

**Rule Violated:** Section 1.11.2 - Tasks must be preserved when updating plan

**Problem:** When updating plan to add new subtasks (e.g., 4.7, 4.8), previous completed subtasks (4.1-4.6) were removed from the plan.

**Example:**
```typescript
// WRONG - Loses completed tasks
update_plan({
  plan: [
    { step: "4. /work - Execute Phase 5", status: "in_progress" },
    { step: "  4.7. Fix validation issues", status: "in_progress" },  // Missing 4.1-4.6!
    { step: "  4.8. Commit changes", status: "pending" }
  ]
})

// CORRECT - Preserves all tasks
update_plan({
  plan: [
    { step: "4. /work - Execute Phase 5", status: "in_progress" },
    { step: "  4.1. /implement - Define frontmatter schema", status: "completed" },
    { step: "  4.2. /implement - Add frontmatter (batch 1-8)", status: "completed" },
    { step: "  4.3. /implement - Add frontmatter (batch 9-19)", status: "completed" },
    { step: "  4.4. /implement - Add frontmatter to rules", status: "completed" },
    { step: "  4.5. /implement - Create validation script", status: "completed" },
    { step: "  4.6. /implement - Generate indexes", status: "completed" },
    { step: "  4.7. /implement - Fix validation issues", status: "in_progress" },
    { step: "  4.8. /implement - Commit changes", status: "pending" }
  ]
})
```

### 3. Wrong Workflow Attribution

**Rule Violated:** Section 1.11.1 - "Tasks MUST be attributed to the workflow that EXECUTES them"

**Examples:**
- ❌ `"3. /work - Fix prerequisite issues"` - /work doesn't fix, /implement does
- ❌ `"4. /work - Execute Phase 5"` - /work orchestrates, but subtasks execute
- ❌ `"  3.1. Create .windsurf/docs/"` - No workflow name at all
- ❌ `"5. /work - Session end protocol (not triggered)"` - Should use sub-workflow name

**Should have been:**
- ✅ `"3. /work - Execute prerequisite fixes"` (orchestration)
- ✅ `"  3.1. /implement - Create .windsurf/docs/ structure"`
- ✅ `"4. /work - Execute Phase 5 implementation"` (orchestration)
- ✅ `"5. /work-session-protocol - Execute session end protocol"`

---

## Root Cause Analysis

### Why Violations Occurred

1. **Cognitive Load:** During rapid implementation (Phase 5 with 26 files), shortcuts were taken
2. **No Validation:** No automated check to ensure tasks follow format
3. **Inconsistent Examples:** Some rule examples didn't emphasize workflow prefix clearly enough
4. **Template Fatigue:** Repetitive typing of workflow names led to omissions

### Why Regression Happened

1. **No Enforcement Mechanism:** Rules are documentation-only, not programmatically enforced
2. **Multiple Update Patterns:** Different ways to update plan (add vs replace) caused confusion
3. **Long Task Lists:** With 10+ tasks, easy to accidentally drop completed ones
4. **No Pre-commit Hook:** No validation of task format before committing

---

## Prevention Measures

### 1. Enhanced Rule Documentation

**Add to 00_agent_directives.md Section 1.11.2:**

```markdown
### CRITICAL: Never Remove Completed Tasks

**When updating plan:**
- ✅ **ALWAYS include all previous tasks** with their current status
- ✅ **Preserve hierarchical structure** (keep parent and children together)
- ✅ **Only change status** of tasks that have progressed
- ❌ **NEVER create fresh plan** that drops completed tasks
- ❌ **NEVER omit workflow prefix** from any task

**Anti-pattern (WRONG):**
```typescript
// This LOSES tasks 4.1-4.6!
update_plan({
  plan: [
    { step: "4. Execute Phase 5", status: "in_progress" },  // Missing workflow!
    { step: "  4.7. Fix issues", status: "in_progress" },   // Missing workflow!
    { step: "  4.8. Commit", status: "pending" }            // Missing workflow!
  ]
})
```

**Correct pattern:**
```typescript
update_plan({
  plan: [
    { step: "1. /detect-context - Analyze state", status: "completed" },
    { step: "2. /work - Route to workflow", status: "completed" },
    { step: "3. /work - Execute routed workflow", status: "completed" },
    { step: "4. /work - Execute Phase 5", status: "in_progress" },
    { step: "  4.1. /implement - Task 1", status: "completed" },
    { step: "  4.2. /implement - Task 2", status: "completed" },
    // ... keep ALL previous tasks ...
    { step: "  4.6. /implement - Task 6", status: "completed" },
    { step: "  4.7. /implement - Fix issues", status: "in_progress" },  // New!
    { step: "  4.8. /implement - Commit", status: "pending" }           // New!
  ]
})
```
```

### 2. Validation Script

Create `scripts/validate_task_format.py`:
- Check all task updates in conversation history
- Verify workflow prefix present
- Verify no completed tasks removed
- Report violations

### 3. Pre-Update Checklist

**Before calling update_plan, verify:**
- [ ] Every task has `<number>. /<workflow> - <description>` format
- [ ] All previous tasks from last update are included
- [ ] Workflow attribution is correct (executor, not caller)
- [ ] Only status changes for progressed tasks
- [ ] Hierarchical numbering is consistent

### 4. Template for Updates

**Use this template structure:**

```typescript
// Step 1: Copy ENTIRE previous plan
const previousPlan = [/* all tasks from last update */];

// Step 2: Update only the status changes
previousPlan.find(t => t.id === "current").status = "completed";
previousPlan.find(t => t.id === "next").status = "in_progress";

// Step 3: Insert any NEW tasks (don't replace!)
if (newTasksNeeded) {
  previousPlan.splice(insertIndex, 0, ...newTasks);
}

// Step 4: Call update_plan with FULL list
update_plan({
  explanation: "Progress update with new tasks",
  plan: previousPlan  // COMPLETE list, not subset
});
```

---

## Action Items

1. ✅ Document violations (this file)
2. ⏳ Update 00_agent_directives.md with enhanced anti-patterns
3. ⏳ Create validation script
4. ⏳ Add validation to pre-commit hooks (future enhancement)
5. ⏳ Update workflow templates with correct examples

---

## Lessons Learned

1. **Automation > Documentation:** Rules alone don't prevent violations, need tooling
2. **Visibility Matters:** Task list is living documentation, must be complete
3. **Shortcuts Have Costs:** Omitting workflow names seems minor but breaks traceability
4. **Regression Prevention:** Need both documentation AND enforcement mechanisms

---

## References

- Rule Section: [00_agent_directives.md](../../.windsurf/rules/00_agent_directives.md) Section 1.11
- Related: [work.md](../../.windsurf/workflows/work.md) - Task system usage
- Related: [implement.md](../../.windsurf/workflows/implement.md) - Task attribution examples
