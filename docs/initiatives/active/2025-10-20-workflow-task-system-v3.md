---
Status: In Progress (Phases 1, 2, 4, 5 Complete)
Created: 2025-10-20
Owner: AI Agent
Priority: High
Estimated Duration: 12-16 hours
Target Completion: 2025-11-01
Updated: 2025-10-20
Progress: 4/7 phases complete (57%)
---

# Initiative: Workflow & Task System V3 - Dynamic Planning and Intelligent Checkpoints

---

## Executive Summary

Fix critical workflow/task system brittleness by transitioning from static upfront planning to **adaptive dynamic planning** with **automatic validation checkpoints** and **intelligent commit strategies**. Address 5 major issues from Quality Automation session and industry research.

**Expected Impact:**

- **60-80% reduction** in task plan updates (fewer manual corrections)
- **Zero pre-planned commit/validate tasks** (automatic checkpoints)
- **100% correct task attribution** (orchestrator vs executor clarity)
- **Workflow autonomy** (self-managing sub-workflows)
- **Better UX** (clearer progress, fewer confusing updates)

---

## Problem Statement

### Current Pain Points

Based on **Quality Automation session (2025-10-20)** and **industry best practices research**:

#### Issue #1: Static Task Planning (Brittle)

**Problem:**

Current system requires listing ALL tasks upfront:

```typescript
// BRITTLE: Must predict entire workflow
update_plan({
  plan: [
    { step: "3.1. /load-context", status: "pending" },
    { step: "3.2. /implement - Phase 2", status: "pending" },
    { step: "3.3. /implement - Phase 3", status: "pending" },
    { step: "3.4. /implement - Phase 4", status: "pending" },
    { step: "3.5. /implement - Phase 5", status: "pending" },
    { step: "3.6. /commit - Phase 2", status: "pending" },  // Wrong!
    { step: "3.7. /commit - Phase 3", status: "pending" },  // Wrong!
    { step: "3.8. /commit - Phase 4", status: "pending" },  // Wrong!
  ]
})
```

**What Happened:**

- Agent executed 3.2 (Phase 2)
- Then jumped to 3.6 (commit)
- Skipped 3.3-3.5 entirely
- Tasks were listed but in wrong sequence

**Root Cause:** Static planning can't adapt to dynamic work

**Industry Standard:**

> "Adaptive Orchestrator excels at dynamic decision-making... makes decisions on the fly based on current context. Ideal for tasks requiring adaptive paths that alter execution during runtime."
>
> — Dynamiq (2025), _Agent Orchestration Patterns_

#### Issue #2: Manual Checkpoints (Should Be Automatic)

**Problem:**

Commits and validation listed as separate tasks:

```typescript
{ step: "3.6. /commit - Commit Phase 2 changes", status: "pending" }
{ step: "3.7. /validate - Test Phase 3", status: "pending" }
```

**What Should Happen:**

- Validation runs **automatically** after each phase
- Commits happen **intelligently** (not pre-planned)
- Checkpoints embedded in workflow logic, not task list

**Industry Standard:**

> "Use checkpoint features available in your SDK to help recover from interrupted orchestration... Implement timeout and retry mechanisms."
> — Microsoft Azure (2025), _AI Agent Orchestration Patterns_
> "A workflow chains multiple operations together... with checkpoints at each stage. Progress saved automatically."
> — Patronus AI (2025), _Agentic Workflows_

#### Issue #3: Task Attribution Confusion

**Problem:**

Confusion about which workflow **executes** vs **orchestrates**:

**From session:**

```text
3. /implement - Execute Phase 2-5     # WRONG: /work orchestrates, /implement executes
3.1. /load-context - Load files       # Correct: /load-context executes
3.2. /implement - Phase 2              # Correct: /implement executes
```

**Should Be:**

```text
3. /work - Execute implementation      # /work orchestrates
  3.1. /implement - Load context       # /implement executes (as /work's subtask)
  3.2. /implement - Phase 2            # /implement executes
```

**Rule Violated:**

> "Attribute tasks to workflow that EXECUTES them."
>
> — `07_task_system.md` Section 1.2

#### Issue #4: Missing Sub-Workflow Autonomy

**Problem:**

Workflows can't manage their own sub-tasks well. When `/implement` is called for "Phase 2-5", it should:

1. **Auto-detect** phases
2. **Create tasks** for each phase dynamically
3. **Insert validation** checkpoints automatically
4. **Commit intelligently** when stable

**Current:** Parent must predict all sub-workflow tasks

**Industry Standard:**

> "Breaking tasks into smaller, specialized agents with clear responsibilities. Each agent manages its own subtasks autonomously."
>
> — V7 Labs (2025), _Multi-Agent AI Systems_

#### Issue #5: Archive Script Error (Undocumented)

**Problem:**

```bash
task archive:initiative NAME=2025-10-19-quality-automation-and-monitoring
# Error: FileNotFoundError: /home/gxx/projects/mcp-web/2025-10-19-quality...
```

**Root Cause:**

Script expects **name only**, constructs path incorrectly:

```python
# In file_ops.py:234
src = resolve_repo_path(initiative_path, root=base)
# initiative_path = "2025-10-19-quality..." (no docs/initiatives/active prefix)
```

**Impact:** Common error, no documentation/guidance in error message

---

## Solution Overview

### Key Strategies

#### 1. Adaptive Task Planning (Dynamic)

- Workflows add tasks **as they discover work**
- Initial plan shows **current phase only**
- Next phases added **when approaching**

#### 2. Automatic Checkpoints

- Validation runs **after every deliverable**
- Commits happen **when stable** (tests pass, quality gates met)
- No pre-planned checkpoint tasks

#### 3. Clear Task Attribution

- Orchestrator shows **what it orchestrates**
- Executor shows **what it executes**
- Sub-workflows manage own tasks

#### 4. Workflow Autonomy

- `/implement` detects phases automatically
- Creates subtasks dynamically
- Inserts checkpoints intelligently

#### 5. Better Error Handling

- Archive script validates paths
- Helpful error messages
- Common pitfalls documented

---

## Phases

### Phase 1: Research & Design (2-3 hours) ✅ COMPLETE

**Completed 2025-10-20:**

- [x] Analyze Quality Automation session
- [x] Review linked conversations for patterns
- [x] Research industry best practices (Dynamiq, Microsoft, GitHub)
- [x] Design solution architecture
- [x] Create initiative

**Research Sources:**

- Dynamiq: _Agent Orchestration Patterns_ (Linear vs Adaptive)
- Microsoft Azure: _AI Agent Orchestration Patterns_ (Checkpoints, Reliability)
- GitHub: _Agentic Primitives and Context Engineering_
- V7 Labs: _Multi-Agent AI Systems_
- Patronus AI: _Agentic Workflows_

### Phase 2: Core Task System Improvements (4-5 hours) ✅ COMPLETE

**Goal:** Implement adaptive dynamic planning

**Completed 2025-10-20:**

- [x] Update `07_task_system.md` with adaptive planning rules (+338 lines)
- [x] Add "Dynamic Task Addition" section (Section 1.0)
- [x] Define "Checkpoint Embedding" pattern (Section 8.0-8.3)
- [x] Create task attribution decision tree (decision tree in 1.0)
- [x] Add examples: adaptive vs static (comprehensive examples throughout)
- [x] Add workflow autonomy principles (Section 9.0-9.2)
- [x] Include intelligent commit strategy (Section 8.2)
- [x] Reference 5 industry sources (Dynamiq, Microsoft, MarkTechPost, V7, Patronus)

**Deliverables:**

- ✅ Updated task system rules (.windsurf/rules/07_task_system.md v2.0.0)
- ✅ Clear adaptive planning guidelines with decision framework
- ✅ Decision tree for when to add tasks dynamically
- ✅ Industry-backed patterns and references

**Success Criteria:**

- ✅ Rules support dynamic task addition
- ✅ Checkpoints defined as embedded, not listed
- ✅ Task attribution unambiguous
- ✅ Token count: 7227 (was 2800, +158% for comprehensive coverage)

### Phase 3: Workflow Enhancements (3-4 hours)

**Goal:** Update workflows to use adaptive planning

**Files to Update:**

- `.windsurf/workflows/implement.md`
- `.windsurf/workflows/work.md`
- `.windsurf/workflows/plan.md`

**Changes:**

1. **`/implement` Workflow:**
   - Add phase detection logic
   - Dynamic task creation pattern
   - Automatic validation checkpoints
   - Intelligent commit strategy

2. **`/work` Workflow:**
   - Clarify orchestrator role
   - Remove sub-workflow task prediction
   - Let routed workflows manage themselves

3. **`/plan` Workflow:**
   - Emphasize adaptive planning
   - Remove "list all tasks upfront" mandate

**Deliverables:**

- Updated workflow files
- Adaptive planning examples
- Checkpoint embedding examples

### Phase 4: Commit & Validation Automation (2-3 hours)

**Goal:** Make commits and validation automatic

**Tasks:**

- [ ] Define "stable state" criteria
- [ ] Create commit decision algorithm
- [ ] Document validation checkpoint pattern
- [ ] Add to `/implement` workflow
- [ ] Update `/validate` workflow

**Stable State Criteria:**

- All tests passing
- Linting clean
- Security scans pass (if relevant)
- Work logically complete (phase done)

**Commit Strategy:**

```markdown
## Intelligent Commit Pattern

**When to commit automatically:**

1. Phase complete + tests pass + linting clean
2. Logical deliverable done (feature works end-to-end)
3. Before switching contexts (Phase 2 → Phase 3)

**When to hold commit:**

1. Tests failing
2. Linting errors
3. Incomplete work (mid-phase)
4. User explicitly said "don't commit yet"
```

**Deliverables:**

- Commit automation rules
- Validation checkpoint pattern
- Updated workflows

### Phase 4: Archive Script Fix (1 hour) ✅ COMPLETE

**Goal:** Fix `scripts/file_ops.py` archive function

**Completed 2025-10-20:**

- [x] Fix path resolution in `archive_initiative()` (+71 lines)
- [x] Add better error messages with usage examples
- [x] Validate input before processing (3 resolution strategies)
- [x] Add usage examples to error output
- [x] List available initiatives in error message
- [x] Test with various input formats (tested successfully)

**Changes:**

```python
# Before
src = resolve_repo_path(initiative_path, root=base)

# After
# Try multiple path patterns
try:
    src = resolve_repo_path(
        f"docs/initiatives/active/{initiative_path}",
        root=base
    )
except FileNotFoundError:
    # Try with full path
    src = resolve_repo_path(initiative_path, root=base)
```

**Add error guidance:**

```python
if not src.exists():
    raise FileNotFoundError(
        f"Initiative not found: {initiative_path}\n\n"
        f"Usage: task archive:initiative NAME=<name>\n"
        f"  NAME should be one of:\n"
        f"    - Just the name: 2025-10-19-quality-automation\n"
        f"    - Relative path: docs/initiatives/active/2025-10-19-quality-automation.md\n"
        f"    - Absolute path: /home/user/project/docs/initiatives/active/...\n\n"
        f"Available initiatives:\n{list_active_initiatives()}"
    )
```

**Deliverables:**

- Fixed archive script
- Better error messages
- Usage documentation

### Phase 5: Documentation & Examples (2-3 hours) ✅ COMPLETE

**Goal:** Document new patterns with examples

**Completed 2025-10-20:**

- [x] Create `docs/guides/ADAPTIVE_TASK_PLANNING.md` (comprehensive 800+ line guide)
- [x] Add examples from Quality Automation session (Example 1)
- [x] Document checkpoint patterns (Section: Automatic Checkpoints)
- [x] Create troubleshooting guide (Section: Troubleshooting)
- [x] Include implementation patterns (3 patterns documented)
- [x] Add industry references (5 authoritative sources)

**Deliverables:**

- ✅ Comprehensive guide (docs/guides/ADAPTIVE_TASK_PLANNING.md)
- ✅ Real examples (before/after comparisons throughout)
- ✅ Troubleshooting section (3 common problems with solutions)
- ✅ Decision frameworks (adaptive vs static, commit strategy)

### Phase 7: Validation & Testing (1-2 hours)

**Goal:** Test adaptive planning in practice

**Tasks:**

- [ ] Create test initiative (multi-phase)
- [ ] Run through `/work` with adaptive planning
- [ ] Verify dynamic task addition
- [ ] Verify automatic checkpoints
- [ ] Verify intelligent commits
- [ ] Document any issues

**Test Scenario:**

Multi-phase implementation (like Quality Automation):

1. Phase 1: Simple task
2. Phase 2: Complex task (subdivides dynamically)
3. Phase 3: Depends on Phase 2
4. Verify: Tasks added dynamically, commits automatic

**Deliverables:**

- Test results
- Validation report
- Any fixes needed

---

## Success Metrics

### Quantitative

- **Task plan updates:** -60 to -80% (fewer corrections)
- **Pre-planned checkpoint tasks:** 0 (all automatic)
- **Task attribution errors:** 0 (clear rules)
- **Archive script success rate:** 100% (better validation)
- **Dynamic task addition:** 100% of multi-phase work

### Qualitative

- Workflows feel more autonomous
- Less "fighting with task system"
- Clearer progress visibility
- Better user experience
- Commits happen at right times

---

## Dependencies

**Internal:**

- Task system (`07_task_system.md`) - Must update
- Workflows (`/implement`, `/work`, `/plan`) - Must update
- File ops script (`scripts/file_ops.py`) - Must fix

**External:**

- None

---

## Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking existing workflows | Medium | High | Gradual rollout, maintain backward compatibility |
| Confusion about new patterns | Medium | Medium | Comprehensive documentation with examples |
| Over-automation (commits too frequent) | Low | Medium | Conservative stable-state criteria |
| Under-automation (missing checkpoints) | Low | Medium | Explicit checkpoint requirements in workflows |

---

## Timeline

**Total: 15-19 hours** (within 12-16h estimate with optimization)

- Phase 1: ✅ Complete (3 hours)
- Phase 2: 4-5 hours
- Phase 3: 3-4 hours
- Phase 4: 2-3 hours
- Phase 5: 1 hour
- Phase 6: 2-3 hours
- Phase 7: 1-2 hours

**Target Completion:** 2025-11-01 (12 days)

---

## References

### Research Sources

**Industry Best Practices:**

1. **Dynamiq (2025):** _Agent Orchestration Patterns in Multi-Agent Systems_
   - Linear vs Adaptive orchestrators
   - Dynamic workflow systems
   - Context-aware processing

2. **Microsoft Azure (2025):** _AI Agent Orchestration Patterns_
   - Checkpoint features for reliability
   - Distributed systems patterns
   - Graceful degradation

3. **GitHub (2025):** _Agentic Primitives and Context Engineering_
   - Agentic workflow composition
   - Natural language as code
   - Runtime management

4. **V7 Labs (2025):** _Multi-Agent AI Systems_
   - Agent autonomy
   - Transparent checkpoints
   - Modular reasoning

5. **Patronus AI (2025):** _Agentic Workflows_
   - Workflow chaining
   - Checkpoints and recovery
   - Orchestrator patterns

### Internal References

- **Quality Automation Session:** 2025-10-20 (identified issues)
- **Workflows V2 Optimization:** (token optimization, workflow architecture)
- **Documentation Validation:** (validation patterns, consistency checks)

### Related ADRs

- None yet (may create ADR for dynamic planning if architectural)

---

## Updates

### 2025-10-20 (Creation)

**Initiative created** based on systematic analysis of workflow/task system issues.

**Evidence:**

- Quality Automation session showed brittle static planning
- Commits pre-planned but should be automatic
- Task attribution confusion (orchestrator vs executor)
- Archive script path resolution bug
- Industry research shows adaptive > static

**Research conducted:**

- 5 industry sources analyzed
- 3 conversation trajectories searched
- Best practices identified and documented

**Next:** Phase 2 - Core task system improvements

---

**Last Updated:** 2025-10-20
**Status:** Active (Phase 1 Complete, Phases 2-7 Pending)
**Next Session Priority:** Phase 2 - Update core task system rules
