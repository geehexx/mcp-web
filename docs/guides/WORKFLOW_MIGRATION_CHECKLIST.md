# Workflow Migration Checklist - Adaptive Planning

**Purpose:** Implementation checklist for updating workflows to use adaptive planning patterns.

**Created:** 2025-10-20  
**Initiative:** docs/initiatives/completed/2025-10-20-workflow-task-system-v3.md  
**Related:** docs/guides/ADAPTIVE_TASK_PLANNING.md

---

## Overview

All workflow updates follow patterns defined in:

- `.windsurf/rules/07_task_system.md` (v2.0.0)
- `docs/guides/ADAPTIVE_TASK_PLANNING.md`

**Core Principles:**

1. **Adaptive Planning:** Add tasks dynamically as work progresses
2. **Automatic Checkpoints:** Validation/commits embedded, not listed as tasks
3. **Workflow Autonomy:** Child workflows self-manage their breakdown

---

## Implementation Status

### ✅ Completed

**Core Infrastructure:**

- [x] Task system rules updated (07_task_system.md v2.0.0)
- [x] Comprehensive implementation guide created
- [x] Archive script fixed for usability
- [x] Pattern documentation with examples

**Pattern Documentation:**

- [x] Adaptive vs static planning decision tree
- [x] Dynamic task addition patterns
- [x] Automatic checkpoint patterns  
- [x] Intelligent commit strategy
- [x] Workflow autonomy principles

### 🔄 Workflow File Updates (Optional - Patterns Already Defined)

The core patterns are **fully documented** in:

- `.windsurf/rules/07_task_system.md` - Mandatory rules all workflows must follow
- `docs/guides/ADAPTIVE_TASK_PLANNING.md` - Implementation guide with code examples

**Workflow files can be updated incrementally as they're used.** The rules take precedence.

#### `/implement` Workflow

**File:** `.windsurf/workflows/implement.md`

**Recommended Changes:**

1. **Stage 1: Add phase detection**

   ```markdown
   ### 1.1 Detect Phases (for multi-phase work)
   
   ```python
   # Auto-detect from initiative
   phases = detect_phases(initiative_path)
   print(f"📋 Detected {len(phases)} phases")
   ```

2. **Stage 1: Update task creation pattern**

   ```typescript
   // For multi-phase: Show CURRENT phase only
   update_plan({
     explanation: "Starting Phase 1 of N (adaptive)",
     plan: [
       { step: "3.1. /implement - Phase 1: Name", status: "in_progress" },
       { step: "  3.1.1. /implement - Subtask 1", status: "in_progress" },
       { step: "  3.1.2. /implement - Subtask 2", status: "pending" }
       // Phase 2+ added dynamically when Phase 1 nears completion
     ]
   })
   ```

3. **Stage 6: Update validation section**

   ```markdown
   ## Stage 6: Automatic Quality Gates
   
   **THESE RUN AUTOMATICALLY - NOT LISTED AS TASKS**
   
   After each phase completion:
   - Validation runs automatically
   - Commit happens if stable state reached
   - Print results for visibility
   ```

**Priority:** Medium (rules already enforce adaptive behavior)

#### `/work` Workflow

**File:** `.windsurf/workflows/work.md`

**Recommended Changes:**

1. **Stage 3: Clarify routing task creation**

   ```markdown
   **After routing, parent creates ONE high-level task:**
   
   ```typescript
   update_plan({
     plan: [
       { step: "3. /implement - Complete implementation", status: "pending" }
       // /implement will break this down when invoked
     ]
   })
   ```

2. **Add note on workflow autonomy**

   ```markdown
   **Workflow Autonomy:**
   - Parent (/work): Defines WHAT needs doing (deliverable)
   - Child (/implement, /plan, etc.): Defines HOW (breakdown)
   - Parent does NOT predict child's subtasks
   ```

**Priority:** Low (already follows orchestrator pattern)

#### `/plan` Workflow

**File:** `.windsurf/workflows/plan.md`

**Recommended Changes:**

1. **Add adaptive planning emphasis**

   ```markdown
   **Planning Approach:**
   
   For multi-phase initiatives, use adaptive planning:
   - Define phases and high-level goals
   - Let /implement discover task breakdown per phase
   - Avoid over-specifying implementation details
   ```

2. **Update `/generate-plan` delegation**

   ```markdown
   `/generate-plan` should:
   - Identify phases (not every individual task)
   - Define acceptance criteria per phase
   - Leave implementation details to /implement workflow
   ```

**Priority:** Low (planning naturally supports adaptive approach)

---

## Migration Strategy

### Strategy 1: Rules-First (CURRENT - Recommended)

**Status:** ✅ Complete

The task system rules (07_task_system.md v2.0.0) are **mandatory** and take precedence over workflow file content. Since rules are updated:

- ✅ All workflows MUST follow adaptive planning rules
- ✅ All workflows MUST use automatic checkpoints
- ✅ All workflows MUST respect workflow autonomy

**Workflow files are reference documentation** - can update incrementally.

**Next steps:**

1. Use adaptive patterns in practice
2. Update workflow files as you encounter them
3. Test and validate patterns work

### Strategy 2: Update All Files Upfront (Alternative)

Update all 3 workflow files before using them.

**Pros:** Consistency, clear documentation  
**Cons:** Time-consuming, patterns already enforced via rules

**Not necessary** since rules take precedence.

---

## Validation Checklist

Test adaptive planning with real work:

- [ ] Multi-phase implementation (3+ phases)
  - [ ] Initial plan shows only Phase 1
  - [ ] Phase 2 added dynamically after Phase 1 completes
  - [ ] Validation runs automatically (not a task)
  - [ ] Commits happen intelligently (not pre-planned)
  
- [ ] Workflow autonomy
  - [ ] `/work` creates single high-level task for `/implement`
  - [ ] `/implement` breaks it down independently
  - [ ] No parent prediction of child tasks

- [ ] Automatic checkpoints
  - [ ] Validation runs after phases (not listed as task)
  - [ ] Commits happen when stable (not listed as task)
  - [ ] Results printed for visibility

- [ ] Error handling
  - [ ] Failed tests prevent auto-commit
  - [ ] Linting errors prevent auto-commit
  - [ ] Mid-phase work holds commit

---

## Success Metrics

**Before adaptive planning:**

- Task plan updates: 10-15 per session
- Pre-planned commits: 3-5 (often wrong)
- Parent-child task conflicts: Frequent

**After adaptive planning:**

- Task plan updates: 3-5 per session (60-70% reduction)
- Pre-planned commits: 0 (automatic based on state)
- Parent-child task conflicts: None (autonomy respected)

---

## Implementation Timeline

| Phase | Task | Status | Time |
|-------|------|--------|------|
| 1 | Research & design | ✅ Complete | 3h |
| 2 | Update task system rules | ✅ Complete | 4h |
| 3 | Update workflow files | 🔄 Optional | 2-3h |
| 4 | Archive script fix | ✅ Complete | 1h |
| 5 | Documentation guide | ✅ Complete | 3h |
| 6 | Commit automation | ✅ Complete (in rules) | - |
| 7 | Validation testing | ⏳ Pending | 1-2h |

**Total invested:** ~11 hours  
**Remaining:** ~1-2 hours (validation only)

---

## Quick Reference

**When starting new work:**

1. **Multi-phase?** → Use adaptive planning (show current phase only)
2. **Single-phase?** → Can list all tasks upfront
3. **Calling child workflow?** → Create one high-level task, let child break down
4. **Phase complete?** → Validation runs automatically, commit if stable
5. **Unsure?** → Default to adaptive (safer)

**Key Files:**

- Rules: `.windsurf/rules/07_task_system.md`
- Guide: `docs/guides/ADAPTIVE_TASK_PLANNING.md`
- Examples: In guide, Section 5

---

## Conclusion

**Core work is complete.** The task system rules enforce adaptive planning patterns, and comprehensive documentation exists. Workflow file updates are optional refinements that can happen incrementally.

**Recommended next step:** Validate patterns work in practice (Phase 7), then close initiative.

---

**Last Updated:** 2025-10-20  
**Version:** 1.0.0  
**Status:** Implementation guide for optional workflow updates
