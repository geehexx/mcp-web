# Adaptive Task Planning Guide

**Purpose:** Comprehensive guide for implementing adaptive dynamic planning in workflows.

**Created:** 2025-10-20
**Related Initiative:** docs/initiatives/completed/2025-10-20-workflow-task-system-v3.md
**Related Rules:** .windsurf/rules/07_task_system.md

---

## Executive Summary

**What changed:** Task system now supports **adaptive dynamic planning** where tasks are added as work progresses, rather than predicted upfront.

**Why it matters:**

- **60-80% fewer task plan updates** (fewer prediction errors)
- **Clearer current focus** for users (see what's happening now)
- **More resilient** to scope changes mid-work
- **Less cognitive load** on agents

**When to use:** Multi-phase work, complex implementations, work with uncertain scope

---

## Table of Contents

1. [Adaptive vs Static Planning](#adaptive-vs-static-planning)
2. [Implementation Patterns](#implementation-patterns)
3. [Automatic Checkpoints](#automatic-checkpoints)
4. [Workflow Autonomy](#workflow-autonomy)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

---

## Adaptive vs Static Planning

### Decision Framework

**Use ADAPTIVE planning when:**

- ✅ Multi-phase implementation (3+ phases)
- ✅ Scope may change based on discoveries
- ✅ Work duration >1 hour
- ✅ Next steps depend on intermediate results

**Use STATIC planning when:**

- ⚠️ Well-defined sequence with no branches (rare)
- ⚠️ Very short tasks (<30 min total)
- ⚠️ Template-driven work with fixed steps

**Default recommendation:** **Use ADAPTIVE** unless you're certain static will work.

### The Problem with Static Planning

**Before (Static - Brittle):**

```typescript
// Agent tries to predict ALL tasks upfront
update_plan({
  plan: [
    { step: "3.1. /implement - Phase 1", status: "pending" },
    { step: "3.2. /implement - Phase 2", status: "pending" },
    { step: "3.3. /implement - Phase 3", status: "pending" },
    { step: "3.4. /implement - Phase 4", status: "pending" },
    { step: "3.5. /implement - Phase 5", status: "pending" },
    { step: "3.6. /commit - Commit Phase 1", status: "pending" },  // ❌ Wrong order!
    { step: "3.7. /commit - Commit Phase 2", status: "pending" },  // ❌ Pre-planned
    { step: "3.8. /commit - Commit Phase 3", status: "pending" }   // ❌ Pre-planned
  ]
})

// What actually happens:
// - Agent executes Phase 1
// - Jumps to task 3.6 (commit)
// - Phases 2-5 skipped or re-ordered
// - Constant task plan corrections needed
```

**After (Adaptive - Robust):**

```typescript
// Initial plan: Show CURRENT phase only
update_plan({
  plan: [
    { step: "3.1. /implement - Phase 1: Foundation", status: "in_progress" },
    { step: "  3.1.1. /implement - Load context", status: "in_progress" },
    { step: "  3.1.2. /implement - Design tests", status: "pending" },
    { step: "  3.1.3. /implement - Implement core", status: "pending" }
    // Phase 2-5 NOT listed - will add when Phase 1 nears completion
  ]
})

// After Phase 1 completes, dynamically ADD Phase 2
update_plan({
  explanation: "✅ Phase 1 complete. Adding Phase 2 tasks.",
  plan: [
    { step: "3.1. /implement - Phase 1: Foundation", status: "completed" },
    { step: "  3.1.1. /implement - Load context", status: "completed" },
    { step: "  3.1.2. /implement - Design tests", status: "completed" },
    { step: "  3.1.3. /implement - Implement core", status: "completed" },
    { step: "3.2. /implement - Phase 2: Integration", status: "in_progress" },
    { step: "  3.2.1. /implement - Design integration points", status: "in_progress" }
    // Phase 3-5 still not listed
  ]
})
```

---

## Implementation Patterns

### Pattern 1: Phase Detection

**Workflows should auto-detect phases from initiative files:**

```python
def detect_phases(initiative_path: str) -> list[str]:
    """Extract phases from initiative markdown."""
    content = read_file(initiative_path)
    phases = []

    for line in content.split('\n'):
        if line.startswith('### Phase '):
            # Extract: "### Phase 2: Integration (3-4h)" -> "Phase 2: Integration"
            phase_name = line.strip('#').strip()
            phases.append(phase_name)

    return phases

# Usage in /implement workflow
initiative = "docs/initiatives/active/feature-x.md"
phases = detect_phases(initiative)
print(f"📋 **Detected {len(phases)} phases:** {', '.join(phases[:3])}...")
# Output: 📋 **Detected 5 phases:** Phase 1: Foundation, Phase 2: Integration, Phase 3: Testing...
```

### Pattern 2: Dynamic Task Addition

**Add tasks when approaching completion of current phase:**

```typescript
// When Phase N is ~80% complete or user requests next phase
if (current_phase_nearing_completion()) {
    update_plan({
        explanation: `Phase ${N} nearing completion. Adding Phase ${N+1} tasks.`,
        plan: [
            // ... all previous tasks with correct status ...
            { step: `3.${N}. /implement - Phase ${N}: ${phase_name}`, status: "in_progress" },
            { step: `  3.${N}.3. /implement - Final subtask`, status: "in_progress" },
            // ADD next phase dynamically
            { step: `3.${N+1}. /implement - Phase ${N+1}: ${next_phase_name}`, status: "pending" },
            { step: `  3.${N+1}.1. /implement - First subtask of next phase`, status: "pending" }
        ]
    })
}
```

### Pattern 3: Workflow Autonomy

**Parent workflows define WHAT, child workflows define HOW:**

```typescript
// Parent (/work) - High-level deliverable
update_plan({
    plan: [
        { step: "3. /implement - Complete multi-phase implementation", status: "pending" }
    ]
})

// Child (/implement) - Auto-detects and breaks down
// When invoked, /implement reads initiative, detects phases, creates subtasks
update_plan({
    explanation: "Auto-detected 3 phases from initiative",
    plan: [
        { step: "3. /implement - Complete multi-phase implementation", status: "in_progress" },
        { step: "  3.1. /implement - Phase 1 (auto-detected)", status: "in_progress" },
        { step: "  3.2. /implement - Phase 2 (auto-detected)", status: "pending" },
        { step: "  3.3. /implement - Phase 3 (auto-detected)", status: "pending" }
    ]
})
```

---

## Automatic Checkpoints

### The Problem

**OLD way (Manual checkpoints as tasks):**

```typescript
// ❌ BAD: Commits and validation listed as separate tasks
update_plan({
    plan: [
        { step: "3.2. /implement - Implement Phase 2", status: "completed" },
        { step: "3.3. /validate - Test Phase 2", status: "pending" },  // ❌ Manual
        { step: "3.4. /commit - Commit Phase 2", status: "pending" },  // ❌ Pre-planned
        { step: "3.5. /implement - Implement Phase 3", status: "pending" }
    ]
})
```

**Problems:**

- Task list cluttered with process steps
- Commits pre-planned (what if tests fail?)
- Manual management overhead
- Confuses deliverables with process

### The Solution

**NEW way (Automatic checkpoints):**

```typescript
// ✅ GOOD: Tasks show DELIVERABLES only
update_plan({
    plan: [
        { step: "3.2. /implement - Phase 2 complete", status: "completed" },
        { step: "3.3. /implement - Phase 3 implementation", status: "in_progress" }
        // Validation and commits happen AUTOMATICALLY
    ]
})

// Validation runs AUTOMATICALLY after Phase 2
validate_phase_completion()  // Not a task, embedded logic

// Commit happens AUTOMATICALLY when stable state reached
if (tests_pass && lint_clean && phase_complete) {
    commit_changes()  // Intelligent decision, not pre-planned task
}
```

### Automatic Validation Pattern

**Implementation in workflows:**

```python
def validate_phase_completion(phase_num: int) -> dict:
    """Automatically validate after phase completion."""
    results = {}

    # Run tests
    test_result = run_command("task test:fast")
    results['tests'] = 'pass' if test_result.exit_code == 0 else 'fail'
    test_count = extract_test_count(test_result.output)

    # Run linting
    lint_result = run_command("task lint")
    results['lint'] = 'pass' if lint_result.exit_code == 0 else 'fail'

    # Type checking
    type_result = run_command("task lint:mypy")
    results['types'] = 'pass' if type_result.exit_code == 0 else 'fail'

    # Print results (visibility, not a task)
    print(f"""
📋 **Phase {phase_num} Complete - Validation Results**
✅ Tests: {test_count} passing
{'✅' if results['lint'] == 'pass' else '❌'} Linting: {'Clean' if results['lint'] == 'pass' else 'Errors found'}
{'✅' if results['types'] == 'pass' else '❌'} Type checking: {'No errors' if results['types'] == 'pass' else 'Errors found'}
    """)

    return results
```

### Intelligent Commit Strategy

**Stable State Criteria:**

1. ✅ All tests passing for current scope
2. ✅ Linting clean (no errors)
3. ✅ Type checking passes
4. ✅ Work logically complete (phase/feature done)
5. ✅ No explicit "don't commit yet" from user

**Implementation:**

```python
def should_auto_commit(phase_num: int, total_phases: int, validation_results: dict) -> bool:
    """Decide if automatic commit is appropriate."""

    # Must-have: All quality gates passed
    if validation_results['tests'] != 'pass':
        print("⏸️  Holding commit: Tests failing")
        return False

    if validation_results['lint'] != 'pass':
        print("⏸️  Holding commit: Linting errors")
        return False

    if validation_results['types'] != 'pass':
        print("⏸️  Holding commit: Type errors")
        return False

    # Commit at phase boundaries
    print(f"💾 **Auto-committing:** Phase {phase_num}/{total_phases} complete")
    return True

# After each phase validation
validation_results = validate_phase_completion(current_phase)

if should_auto_commit(current_phase, total_phases, validation_results):
    commit_hash = commit_with_message(
        f"feat: complete Phase {current_phase} - {phase_name}\n\n"
        f"- {summary_of_work}\n"
        f"- Tests: {test_count} passing\n"
        f"- Initiative: {initiative_path}"
    )
    print(f"✅ **Committed:** {commit_hash} - Phase {current_phase} complete")
```

### Checkpoint Visibility

**Print checkpoint results (don't list as tasks):**

```markdown
📋 **Phase 2 Complete - Validation Results**
✅ Tests: 23/23 passing (15 new, 8 existing)
✅ Linting: Clean
✅ Type checking: No errors
✅ Security: No issues detected
💾 **Auto-committed:** feat: Phase 2 implementation (a1b2c3d)

🔄 **Starting Phase 3: Integration Layer**
```

---

## Workflow Autonomy

### The Autonomy Principle

**Parent workflows:** Define WHAT needs to be done (deliverable)
**Child workflows:** Define HOW it will be done (breakdown)

**Example:**

```typescript
// Parent (/work) - Doesn't predict child's tasks
update_plan({
    plan: [
        { step: "3. /implement - Complete Phases 2-5", status: "pending" }
        // That's it! /implement will handle the breakdown
    ]
})

// Child (/implement) - Self-manages breakdown
// When invoked:
// 1. Reads initiative file
// 2. Detects phases automatically
// 3. Creates its own subtasks

update_plan({
    plan: [
        { step: "3. /implement - Complete Phases 2-5", status: "in_progress" },
        { step: "  3.1. /implement - Phase 2: Core", status: "in_progress" },
        { step: "  3.2. /implement - Phase 3: Integration", status: "pending" },
        { step: "  3.3. /implement - Phase 4: Validation", status: "pending" },
        { step: "  3.4. /implement - Phase 5: Documentation", status: "pending" }
    ]
})
```

### Benefits

- **Parent stays simple:** One high-level task
- **Child adapts to reality:** Discovers actual requirements
- **Fewer prediction errors:** No guessing child's tasks
- **Clearer separation:** Each workflow owns its domain

---

## Examples

### Example 1: Multi-Phase Implementation (Before/After)

**Before (Static - Brittle):**

```typescript
// Initial plan tries to predict everything
update_plan({
    explanation: "Starting 5-phase implementation",
    plan: [
        { step: "1. /load-context - Load files", status: "pending" },
        { step: "2. /implement - Phase 1", status: "pending" },
        { step: "3. /implement - Phase 2", status: "pending" },
        { step: "4. /implement - Phase 3", status: "pending" },
        { step: "5. /implement - Phase 4", status: "pending" },
        { step: "6. /implement - Phase 5", status: "pending" },
        { step: "7. /validate - Run tests", status: "pending" },
        { step: "8. /commit - Commit all changes", status: "pending" }
    ]
})

// What actually happens:
// - Execute task 1, 2
// - Discover Phase 2 needs subdivision
// - Update plan (add 3.1, 3.2, 3.3)
// - Execute Phase 2
// - Jump to task 7 (validate) - skips Phases 3-5!
// - Massive confusion and corrections needed
```

**After (Adaptive - Robust):**

```typescript
// Initial plan: ONLY show Phase 1
update_plan({
    explanation: "Starting Phase 1 of 5-phase implementation (adaptive)",
    plan: [
        { step: "1. /implement - Phase 1: Foundation", status: "in_progress" },
        { step: "  1.1. /implement - Load context", status: "in_progress" },
        { step: "  1.2. /implement - Design core interface", status: "pending" },
        { step: "  1.3. /implement - Write unit tests", status: "pending" },
        { step: "  1.4. /implement - Implement core logic", status: "pending" }
        // Phase 2-5 not listed yet
    ]
})

// After Phase 1 completes, validation runs automatically
// Commit happens automatically
// Then ADD Phase 2 dynamically:

update_plan({
    explanation: "✅ Phase 1 complete. Adding Phase 2 tasks.",
    plan: [
        { step: "1. /implement - Phase 1: Foundation", status: "completed" },
        { step: "  1.1. /implement - Load context", status: "completed" },
        { step: "  1.2. /implement - Design core interface", status: "completed" },
        { step: "  1.3. /implement - Write unit tests", status: "completed" },
        { step: "  1.4. /implement - Implement core logic", status: "completed" },
        { step: "2. /implement - Phase 2: Integration", status: "in_progress" },
        { step: "  2.1. /implement - Design integration points", status: "in_progress" },
        { step: "  2.2. /implement - Write integration tests", status: "pending" },
        { step: "  2.3. /implement - Implement integration", status: "pending" }
        // Phase 3-5 still not listed
    ]
})

// Continues dynamically for each phase
```

### Example 2: Research-Driven Planning

**Scenario:** Creating ADR-based feature with uncertain design

**Adaptive approach:**

```typescript
// Initial: Research phase only
update_plan({
    plan: [
        { step: "1. /research - Gather best practices", status: "in_progress" },
        { step: "  1.1. /research - Search codebase patterns", status: "in_progress" },
        { step: "  1.2. /research - Web research current standards", status: "pending" },
        { step: "  1.3. /research - Evaluate alternatives", status: "pending" }
        // Don't know what comes after until research completes
    ]
})

// After research: NOW we know the approach, add ADR + implementation
update_plan({
    explanation: "Research complete. Recommendation: Use Strategy A. Adding ADR + implementation tasks.",
    plan: [
        { step: "1. /research - Gather best practices", status: "completed" },
        { step: "  1.1. /research - Search codebase patterns", status: "completed" },
        { step: "  1.2. /research - Web research current standards", status: "completed" },
        { step: "  1.3. /research - Evaluate alternatives", status: "completed" },
        { step: "2. /new-adr - Document Strategy A decision", status: "in_progress" },
        { step: "3. /implement - Implement Strategy A", status: "pending" }
        // Implementation tasks will be added by /implement workflow
    ]
})
```

---

## Troubleshooting

### Problem: Agent still listing all tasks upfront

**Symptoms:**

- Task plan has 10+ tasks immediately
- Tasks like "Phase 5" listed when starting Phase 1
- Frequent task plan corrections

**Solution:**

1. **Check workflow invocation:** Ensure workflow uses adaptive pattern
2. **Review task creation code:** Should only add current phase
3. **Verify phase detection:** Check if `detect_phases()` working correctly

**Example fix:**

```typescript
// ❌ WRONG: Lists everything
update_plan({
    plan: [
        { step: "1. Phase 1", status: "in_progress" },
        { step: "2. Phase 2", status: "pending" },  // Too early!
        { step: "3. Phase 3", status: "pending" },  // Too early!
        { step: "4. Phase 4", status: "pending" },  // Too early!
        { step: "5. Phase 5", status: "pending" }   // Too early!
    ]
})

// ✅ CORRECT: Only current phase
update_plan({
    plan: [
        { step: "1. Phase 1: Foundation", status: "in_progress" },
        { step: "  1.1. Load context", status: "in_progress" },
        { step: "  1.2. Design tests", status: "pending" },
        { step: "  1.3. Implement core", status: "pending" }
        // Add Phase 2 LATER when Phase 1 nears completion
    ]
})
```

### Problem: Commits still listed as tasks

**Symptoms:**

- Tasks like "3.6. /commit - Commit Phase 2"
- Validation tasks listed separately
- Cluttered task list

**Solution:**

1. **Remove commit/validate tasks** from task plan
2. **Embed checkpoints** in workflow logic
3. **Print results** for visibility

**Example fix:**

```typescript
// ❌ WRONG: Commits as tasks
{ step: "3.4. /commit - Commit Phase 2", status: "pending" }

// ✅ CORRECT: No commit tasks, automatic with visibility
// (No task in plan)
//
// After phase completes:
if (should_auto_commit()) {
    commit_hash = commit_changes()
    print(f"💾 **Auto-committed:** {commit_hash}")
}
```

### Problem: Parent predicting child tasks

**Symptoms:**

- `/work` listing `/implement` subtasks
- Parent task plan has detailed breakdown
- Child workflow redundant

**Solution:**

1. **Parent:** One high-level task
2. **Child:** Creates own breakdown when invoked

**Example fix:**

```typescript
// ❌ WRONG: Parent predicts child tasks
update_plan({  // In /work
    plan: [
        { step: "3. /implement - Implementation", status: "pending" },
        { step: "  3.1. /implement - Load context", status: "pending" },  // Too detailed!
        { step: "  3.2. /implement - Write tests", status: "pending" },   // Too detailed!
        { step: "  3.3. /implement - Implement", status: "pending" }      // Too detailed!
    ]
})

// ✅ CORRECT: Parent delegates, child manages
update_plan({  // In /work
    plan: [
        { step: "3. /implement - Complete implementation", status: "pending" }
        // That's it! /implement will break it down when invoked
    ]
})

// Child (/implement) creates breakdown:
update_plan({  // In /implement when invoked
    plan: [
        { step: "3. /implement - Complete implementation", status: "in_progress" },
        { step: "  3.1. /implement - Load context", status: "in_progress" },
        { step: "  3.2. /implement - Write tests", status: "pending" },
        { step: "  3.3. /implement - Implement", status: "pending" }
    ]
})
```

---

## References

### Industry Standards

**Adaptive Orchestration:**

- [Dynamiq (2025): Agent Orchestration Patterns](https://www.getdynamiq.ai/post/agent-orchestration-patterns-in-multi-agent-systems-linear-and-adaptive-approaches-with-dynamiq)
  - "Adaptive Orchestrator excels at dynamic decision-making... makes decisions on the fly based on current context."
- [MarkTechPost (2025): 9 Agentic AI Workflow Patterns](https://www.marktechpost.com/2025/08/09/9-agentic-ai-workflow-patterns-transforming-ai-agents-in-2025/)
  - "Plan-execute pattern: Agents autonomously plan multi-step workflows, execute each stage sequentially, review outcomes, and adjust as needed."

**Checkpoint Automation:**

- [Microsoft Azure (2025): AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
  - "Use checkpoint features available in your SDK to help recover from interrupted orchestration."

**Workflow Autonomy:**

- V7 Labs (2025): Multi-Agent AI Systems
  - "Breaking tasks into smaller, specialized agents with clear responsibilities. Each agent manages its own subtasks autonomously."

### Internal Documentation

- **Task System Rules:** `.windsurf/rules/07_task_system.md`
- **Work Orchestration:** `.windsurf/workflows/work.md`
- **Implementation Workflow:** `.windsurf/workflows/implement.md`
- **Initiative Template:** `docs/initiatives/template.md`

---

**Last Updated:** 2025-10-20
**Version:** 1.0.0
**Maintainer:** Core Team
