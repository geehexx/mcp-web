# Workflow Architecture Audit - 2025-10-18

**Purpose:** Comprehensive analysis of all workflows to identify deprecated tools, semantic overlap, and architectural issues.

**Initiative:** `2025-10-18-workflow-architecture-refactor.md`

---

## Executive Summary

**Total Workflows:** 18
**Total Words:** 19,464
**Deprecated Tool References:** 3 (in 1 workflow)
**Semantic Overlaps Identified:** 6 pairs
**Recommended Actions:** Consolidate, clarify boundaries, fix tool references

---

## Research Foundation

### Key Anti-Patterns (Azure AI, 2025)

1. **Creating unnecessary coordination complexity** - Using complex patterns when simple ones suffice
2. **Adding agents without meaningful specialization** - Each workflow must have unique value
3. **Over-reliance on orchestration** - Tight coupling between workflows and orchestration logic
4. **Service sprawl** - Too many workflows without clear governance

**Sources:**

- [Azure AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Microservices Anti-Patterns 2025](https://www.geeksforgeeks.org/blogs/microservice-anti-patterns/)
- [9 Agentic Workflow Patterns 2025](https://www.marktechpost.com/2025/08/09/9-agentic-ai-workflow-patterns-transforming-ai-agents-in-2025/)

### Best Practice Patterns

1. **Sequential Intelligence** - Prompt chaining, plan-execute loops
2. **Parallel Processing** - Orchestrator-worker pattern, parallelization
3. **Intelligent Routing** - Input classification to specialized handlers
4. **Self-Improving Systems** - Reflection and learning loops

---

## Workflow Inventory & Analysis

### Category 1: Orchestrators (High-Level Coordination)

| Workflow | Size | Purpose | Issues | Recommendation |
|----------|------|---------|--------|----------------|
| `/work` | 711w | Master orchestrator, context detection + routing | ✅ Well-defined, good specialization | Keep |
| `/plan` | 828w | Research → planning → implementation | ✅ Clear sequential pattern | Keep |
| `/implement` | 1,289w | Test-first implementation workflow | ✅ Unique value (TDD enforcement) | Keep |
| `/meta-analysis` | 575w | Session end protocol orchestrator | ✅ Mandatory quality gate | Keep |

**Analysis:** All orchestrators follow the **Orchestrator-Worker pattern** effectively. Each has clear unique purpose and calls specialized sub-workflows.

**Anti-Pattern Check:** ✅ No unnecessary complexity. Each orchestrator provides meaningful specialization.

---

### Category 2: Specialized Operations (Focused Tasks)

| Workflow | Size | Purpose | Issues | Recommendation |
|----------|------|---------|--------|----------------|
| `/validate` | 1,392w | Quality gate (lint+test+security) | ⚠️ Overlap with `/run-tests` | Clarify: `/validate` = pre-commit gate, `/run-tests` = reference |
| `/commit` | 623w | Git operations + validation | ⚠️ Validation logic duplicated | Remove validation details, reference `/validate` |
| `/bump-version` | 1,342w | Semver bumping from commits | ✅ Unique specialized operation | Keep |
| `/update-docs` | 1,150w | Sync PROJECT_SUMMARY + CHANGELOG | ✅ Clear atomic operation | Keep |
| `/archive-initiative` | 290w | Archive completed initiatives | ⚠️ **3 deprecated tool refs (mcp2_git_*)** | Fix tool references |

**Issues Identified:**

1. **Deprecated Tools (archive-initiative):**
   - `mcp2_git_diff_unstaged`
   - `mcp2_git_add`
   - `mcp2_git_diff_staged`
   - **Fix:** Replace with standard `git` commands via `run_command`

2. **Semantic Overlap (validate vs run-tests):**
   - Both explain pytest-xdist usage
   - Both list test types
   - **Fix:** Make `/run-tests` pure reference, `/validate` the workflow

3. **Duplication (commit validation):**
   - `/commit` duplicates validation checklist from `/validate`
   - **Fix:** Reference `/validate` instead of duplicating

---

### Category 3: Context Handlers (Information Gathering)

| Workflow | Size | Purpose | Issues | Recommendation |
|----------|------|---------|--------|----------------|
| `/detect-context` | 1,968w | Project state analysis for routing | ✅ Critical for autonomous continuation | Keep |
| `/load-context` | 1,431w | Batch context loading strategies | ✅ Performance optimization (3x faster) | Keep |
| `/extract-session` | 897w | Extract structured session data | ✅ Called by meta-analysis only | Keep |

**Analysis:** All context handlers have clear, unique purposes. No overlap.

**Anti-Pattern Check:** ✅ Meaningful specialization. Context handlers enable autonomous work continuation.

---

### Category 4: Artifact Generators (Content Creation)

| Workflow | Size | Purpose | Issues | Recommendation |
|----------|------|---------|--------|----------------|
| `/generate-plan` | 1,189w | Transform research → initiative doc | ✅ Clear artifact generation | Keep |
| `/summarize-session` | 1,073w | Generate formatted session summary | ✅ Template-based generation | Keep |
| `/new-adr` | 362w | ADR creation workflow | ✅ Simple, focused | Keep |
| `/consolidate-summaries` | 2,861w | Consolidate daily summaries | ⚠️ Largest workflow, complex | Review for simplification |

**Issues Identified:**

1. **Consolidate-summaries complexity:**
   - 2,861 words (largest workflow)
   - May be too complex for single workflow
   - **Recommendation:** Consider breaking into phases or simplifying

---

### Category 5: Reference Guides (Documentation)

| Workflow | Size | Purpose | Issues | Recommendation |
|----------|------|---------|--------|----------------|
| `/run-tests` | 508w | Test execution reference | ⚠️ **Identity crisis: workflow or reference?** | **Move to `docs/guides/testing-reference.md`** |
| `/research` | 975w | Research execution workflow | ⚠️ Borderline: could be reference | Keep as workflow (active execution) |

**Critical Issue:**

**`/run-tests` Identity Crisis:**

- Current location: `.windsurf/workflows/run-tests.md`
- Actual function: Reference documentation for test commands
- Overlap with: `/validate` (which actually runs tests)
- **Decision needed:** Is this a workflow or a reference doc?

**Analysis:**

- Content is mostly command reference (`task test:fast`, `task test:coverage`, etc.)
- No orchestration logic or tool calls
- Not invoked by other workflows
- **Verdict:** This is a **reference guide**, not a workflow

**Recommendation:**

- Move to `docs/guides/testing-reference.md`
- Keep `.windsurf/workflows/` for true executable workflows only
- Update cross-references

---

## Semantic Overlap Matrix

| Workflow A | Workflow B | Overlap | Severity | Resolution |
|------------|------------|---------|----------|------------|
| `/validate` | `/run-tests` | Test execution commands, pytest-xdist explanation | **High** | Move `/run-tests` to docs/guides/, keep `/validate` as workflow |
| `/commit` | `/validate` | Validation checklist duplicated | **Medium** | Remove duplication from `/commit`, reference `/validate` |
| `/implement` | `/validate` | Test execution (TDD) | **Low** | Acceptable - different contexts (during dev vs pre-commit) |
| `/plan` | `/research` | Research initiation | **Low** | Acceptable - `/plan` orchestrates, `/research` executes |
| `/work` | `/detect-context` | Context analysis | **Low** | Acceptable - `/work` orchestrates, `/detect-context` executes |
| `/meta-analysis` | `/extract-session` + `/summarize-session` | Session summary generation | **Low** | Acceptable - orchestrator pattern |

**Total High-Severity Overlaps:** 1 (validate vs run-tests)
**Total Medium-Severity Overlaps:** 1 (commit validation duplication)

---

## Workflow Decision Tree

**When should I call which workflow?**

```text
User request arrives
     |
     ├─> "Continue work" / no specific request
     |       └─> Call `/work` (detects context, routes to appropriate workflow)
     |
     ├─> "Create plan for [feature]"
     |       └─> Call `/plan` (research → generate-plan → ready for /implement)
     |
     ├─> "Implement [feature]" (plan exists)
     |       └─> Call `/implement` (test-first, incremental)
     |
     ├─> "Run validation / ready to commit?"
     |       └─> Call `/validate` (lint + test + security gate)
     |
     ├─> "Commit changes"
     |       └─> Call `/commit` (git operations + calls /validate)
     |
     ├─> "Create ADR for [decision]"
     |       └─> Call `/new-adr` (research + document decision)
     |
     ├─> "Archive initiative"
     |       └─> Call `/archive-initiative` (move + update refs)
     |
     ├─> "What tests can I run?"
     |       └─> **Read** `docs/guides/testing-reference.md` (NOT a workflow call)
     |
     └─> Session ending
             └─> Call `/meta-analysis` (MANDATORY, creates session summary)
```

**Key Insight:** Only 8-9 workflows should be directly user-callable. Others are sub-workflows called by orchestrators.

---

## Taxonomy Validation

### Proposed 5-Category Taxonomy (from initiative)

1. **Orchestrators** (3-4 workflows)
   - High-level coordination
   - Call multiple sub-workflows
   - Examples: `/work`, `/plan`, `/meta-analysis`, `/implement`

2. **Specialized Operations** (4-5 workflows)
   - Atomic, focused tasks
   - Examples: `/validate`, `/commit`, `/bump-version`, `/update-docs`, `/archive-initiative`

3. **Context Handlers** (3 workflows)
   - Information gathering
   - Examples: `/detect-context`, `/load-context`, `/extract-session`

4. **Artifact Generators** (4 workflows)
   - Content creation
   - Examples: `/generate-plan`, `/summarize-session`, `/new-adr`, `/consolidate-summaries`

5. **Reference Guides** (1-2 docs, NOT workflows)
   - Documentation, not executable
   - Examples: `testing-reference.md`, potentially `security-checklist.md`

**Validation Results:**

| Category | Expected | Actual | Status |
|----------|----------|--------|--------|
| Orchestrators | 3-4 | 4 | ✅ Good |
| Specialized Operations | 4-5 | 5 | ✅ Good |
| Context Handlers | 3 | 3 | ✅ Perfect |
| Artifact Generators | 4 | 4 | ✅ Perfect |
| Reference Guides | 1-2 | 1 (but misplaced) | ⚠️ Need to move `/run-tests` |

**Overall:** Taxonomy is sound and matches actual workflow distribution.

---

## Deprecated Tool References

### Complete Audit

**Tool:** `mcp2_git_*` (MCP git server - no longer available)

**Occurrences:**

1. **archive-initiative.md** (3 references)
   - Line ~65: `mcp2_git_diff_unstaged`
   - Line ~67: `mcp2_git_add`
   - Line ~69: `mcp2_git_diff_staged`

**Other Workflows:** ✅ Clean (no deprecated references)

**Replacement Strategy:**

```yaml
Old: mcp2_git_diff_unstaged
New: run_command("git diff", cwd=project_root, blocking=true)

Old: mcp2_git_add [files]
New: run_command("git add [files]", cwd=project_root, blocking=true)

Old: mcp2_git_diff_staged
New: run_command("git diff --staged", cwd=project_root, blocking=true)

Old: mcp2_git_commit -m "[message]"
New: run_command("git commit -m '[message]'", cwd=project_root, blocking=true)
```

**Verification Command:**

```bash
grep -r "mcp2_" .windsurf/workflows/
# Should return 0 results after fix
```

---

## Tool Invocation Patterns

### Current State

**File Operations:**

- ✅ Most workflows correctly use `mcp0_read_multiple_files()` for batch reads
- ✅ Edit operations use `edit()` or `multi_edit()` appropriately
- ✅ MCP tools used for `.windsurf/` protected directories

**Git Operations:**

- ⚠️ Inconsistent: some use `git` via `run_command`, one uses deprecated `mcp2_git_*`
- **Standardization needed**

**Test Execution:**

- ✅ Consistent: `task test:*` commands via `run_command`

### Proposed Standard Patterns

```yaml
# File Operations (Batch Read - Always for 3+ files)
mcp0_read_multiple_files(["/abs/path/1", "/abs/path/2", "/abs/path/3"])

# File Operations (Single Read)
read_file("/abs/path/file.py")

# File Operations (Protected .windsurf/ directory)
mcp0_read_text_file("/home/gxx/projects/mcp-web/.windsurf/rules/file.md")
mcp0_write_file("/home/gxx/projects/mcp-web/.windsurf/workflows/file.md", content)

# Git Operations (Standard Pattern)
run_command("git status", cwd=project_root, blocking=true, safe_to_auto_run=true)
run_command("git diff", cwd=project_root, blocking=true, safe_to_auto_run=true)
run_command("git add [files]", cwd=project_root, blocking=true, safe_to_auto_run=false)
run_command("git commit -m '[msg]'", cwd=project_root, blocking=true, safe_to_auto_run=false)

# Test Execution
run_command("task test:fast", cwd=project_root, blocking=true, safe_to_auto_run=true)
run_command("task test:coverage", cwd=project_root, blocking=true, safe_to_auto_run=true)

# Validation
run_command("task format:check", cwd=project_root, blocking=true, safe_to_auto_run=true)
run_command("task lint", cwd=project_root, blocking=true, safe_to_auto_run=true)
```

**Documentation:** Add to workflow template or `.windsurf/rules/` for consistency

---

## Migration Plan

### Phase 2: Tool Reference Fixes (Immediate)

**Tasks:**

1. ✅ Fix `/archive-initiative` (3 deprecated tool references)
2. ✅ Verify all other workflows clean
3. ✅ Document standard tool patterns
4. ✅ Test archive workflow with real initiative

**Estimated Time:** 1 hour

---

### Phase 3: Consolidation & Restructuring

#### 3.1 Move Reference Docs (High Priority)

**Task:** Move `/run-tests` to reference docs

**Actions:**

```bash
# Create guides directory if needed
mkdir -p docs/guides/

# Move file
mv .windsurf/workflows/run-tests.md docs/guides/testing-reference.md

# Update cross-references
# - .windsurf/workflows/validate.md (remove overlap, reference guide)
# - .windsurf/workflows/implement.md (update reference)
# - docs/DOCUMENTATION_STRUCTURE.md (document new guides/ directory)
```

**Estimated Time:** 30 minutes

#### 3.2 Remove Validation Duplication (Medium Priority)

**Task:** Simplify `/commit` to reference `/validate`

**Actions:**

- Remove duplicated validation checklist from `/commit`
- Add: "Before committing, `/commit` calls `/validate` workflow"
- Keep commit-specific git operations

**Estimated Time:** 20 minutes

#### 3.3 Clarify Semantic Boundaries (Medium Priority)

**Task:** Update workflow documentation to clarify boundaries

**Actions:**

- `/validate`: Add note "This is the pre-commit quality gate workflow"
- `docs/guides/testing-reference.md`: Add note "For test execution commands, not a workflow"
- Update decision tree in each workflow's frontmatter or description

**Estimated Time:** 30 minutes

#### 3.4 Review Consolidate-Summaries (Low Priority)

**Task:** Evaluate if largest workflow (2,861w) needs simplification

**Actions:**

- Review workflow logic
- Consider breaking into sub-workflows if too complex
- Or: Accept complexity if justified by unique purpose

**Estimated Time:** 1-2 hours (defer to separate task if needed)

---

### Phase 4: Documentation & Validation

**Tasks:**

1. ✅ Create ADR-0018: Workflow Architecture V3
2. ✅ Update `docs/DOCUMENTATION_STRUCTURE.md` with workflow taxonomy
3. ✅ Add workflow decision tree to documentation
4. ✅ Create `docs/guides/` directory structure
5. ✅ Update all cross-references
6. ✅ Final validation (grep for deprecated tools, test workflows)

**Estimated Time:** 2 hours

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking workflow chains during refactor | Medium | High | Test all integration points, maintain backward compat during transition |
| User confusion about workflow vs reference | Low | Medium | Clear documentation, update decision tree |
| Missing deprecated tool references | Low | High | Comprehensive grep, manual review of all workflows |
| Over-engineering taxonomy | Medium | Low | Stick to 5 categories, resist adding more |

---

## Success Metrics (Post-Refactor)

**Quantitative:**

- Deprecated tool references: 3 → 0 ✅
- High-severity semantic overlaps: 1 → 0 ✅
- Reference docs in workflows/: 1 → 0 ✅
- Workflows with clear unique value: 100% ✅

**Qualitative:**

- Each workflow can explain unique value in 1 sentence ✅
- Clear decision tree for "which workflow to call" ✅
- Consistent tool invocation patterns ✅
- Taxonomy documented and followed ✅

---

## Next Steps

1. **Immediate (Phase 2):**
   - Fix 3 deprecated tool references in `/archive-initiative`
   - Verify fix with grep

2. **This Session (Phase 3):**
   - Move `/run-tests` to `docs/guides/testing-reference.md`
   - Remove validation duplication from `/commit`
   - Clarify semantic boundaries in documentation

3. **Before End of Session (Phase 4):**
   - Create ADR-0018
   - Update DOCUMENTATION_STRUCTURE.md
   - Final validation

4. **Future Session (Optional):**
   - Review `/consolidate-summaries` complexity
   - Consider workflow performance profiling

---

## Appendix A: Workflow Size Distribution

```text
Small (< 500w):     3 workflows (archive-initiative, new-adr, run-tests)
Medium (500-1000w): 6 workflows (commit, work, plan, meta-analysis, extract-session, research)
Large (1000-1500w): 7 workflows (bump-version, validate, load-context, generate-plan, summarize-session, implement, detect-context)
X-Large (> 2000w):  2 workflows (consolidate-summaries, [none others])
```

**Observation:** Most workflows (13/18) are medium or large size, which is appropriate for orchestration logic. Only 2 outliers (consolidate-summaries is very large, some are very small).

---

## Appendix B: Integration Matrix

**Which workflows call which?**

```text
/work
  ├─> /detect-context
  ├─> /load-context
  ├─> /plan
  ├─> /implement
  ├─> /validate
  ├─> /commit
  ├─> /archive-initiative
  └─> /meta-analysis (MANDATORY at session end)

/plan
  ├─> /research
  ├─> /generate-plan
  ├─> /load-context
  └─> /implement

/implement
  └─> /validate

/commit
  └─> /validate
  └─> /bump-version (conditionally)

/meta-analysis
  ├─> /extract-session
  ├─> /summarize-session
  └─> /update-docs (conditionally)

/generate-plan
  └─> /new-adr (conditionally)
```

**Leaf Workflows** (called but don't call others):

- `/detect-context`, `/load-context`, `/research`, `/new-adr`
- `/extract-session`, `/summarize-session`, `/update-docs`
- `/validate`, `/bump-version`, `/archive-initiative`

**Orphan Workflows** (not called by others):

- `/consolidate-summaries` (standalone, manual invocation only)

---

**Audit Complete.**
**Ready for Phase 1.2: Design Taxonomy & Phase 1.3: Create ADR**
