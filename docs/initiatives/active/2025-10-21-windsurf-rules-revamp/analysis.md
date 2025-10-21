# Windsurf Rules System Analysis

**Date:** 2025-10-21  
**Purpose:** Complete inventory for comprehensive revamp

---

## Current Rules Inventory (8 files, 101KB)

| File | Size | Trigger | Globs | Tokens | Topics | Issues |
|------|------|---------|-------|--------|--------|--------|
| `00_agent_directives.md` | 12.9KB | `always_on` | - | 3175 | Persona, principles, mandate, tool selection | ⚠️ Excessive custom frontmatter fields |
| `01_testing_and_tooling.md` | 5.8KB | `glob` | `tests/**/*.py, src/**/*.py, *.toml, *.ini, Taskfile.yml` | 1394 | Testing standards, tooling | ⚠️ Globs in quotes (wrong format) |
| `02_python_standards.md` | 10.1KB | `glob` | `**/*.py` | 2463 | Python style, type hints, async | ⚠️ Globs in quotes, excessive metadata |
| `03_documentation_lifecycle.md` | 10.7KB | `glob` | `docs/**/*.md, *.md` | 2643 | Doc creation, maintenance, archival | ⚠️ Globs in quotes, excessive metadata |
| `04_security.md` | 11.1KB | `model_decision` | `**/*.py, **/*.ini, **/*.yml, **/*.yaml` | 2712 | OWASP LLM Top 10, security practices | ⚠️ Has globs (should not for model_decision), quotes on globs |
| `05_operational_protocols.md` | 10.2KB | `model_decision` | - | 2503 | Session end, progress communication | ⚠️ Excessive metadata |
| `06_context_engineering.md` | 11.8KB | `model_decision` | - | 2802 | File ops, git, context loading | ⚠️ Excessive metadata |
| `07_task_system.md` | 29.1KB | `manual` | - | 7176 | Task system, update_plan usage | ⚠️ Excessive metadata, very large (24% of total) |

**Total:** 101.7KB, 24,868 tokens

**Critical Issues:**
1. All rules have excessive frontmatter: `created`, `updated`, `category`, `tokens`, `applyTo`, `priority`, `status`
2. `globs` fields are quoted strings instead of comma-separated unquoted values
3. `04_security.md` has `model_decision` trigger but also has `globs` field (mutually exclusive)
4. `07_task_system.md` is massive (29KB, 7176 tokens) - should be split or made `model_decision`

---

## Current Docs Inventory (15 files, 79KB)

| File | Size | Purpose | Should Elevate? | Rationale |
|------|------|---------|-----------------|-----------|
| `automation-scripts.md` | 5.5KB | Quick ref for `task` commands | **YES** | Frequently needed, actionable |
| `batch-operations.md` | 6.3KB | Optimization patterns | **YES** | Core performance guidance |
| `common-patterns.md` | 4.1KB | General patterns | **MAYBE** | Merge into other rules? |
| `context-loading-patterns.md` | 7.0KB | Context loading strategies | **YES** | Critical for efficiency |
| `directory-structure.md` | 5.7KB | `.windsurf/` structure | **YES** | Structural enforcement |
| `error-handling-patterns.md` | 9.8KB | Error handling strategies | **YES** | Important for robustness |
| `frontmatter-specification.md` | 0 | Empty (leftover from revert) | **DELETE** | - |
| `FRONTMATTER_MIGRATION_2025-10-20.md` | 0 | Empty (leftover from revert) | **DELETE** | - |
| `index.md` | 6.7KB | Master index | **REGENERATE** | Auto-generated |
| `rules-index.md` | 1.5KB | Rules index | **REGENERATE** | Auto-generated |
| `task-system-reference.md` | 6.8KB | Task system quick ref | **MERGE** | Into `07_task_system.md` |
| `tool-patterns.md` | 9.5KB | Tool usage patterns | **YES** | Critical for tool usage |
| `workflow-dependencies.md` | 3.0KB | Workflow deps | **REGENERATE** | Auto-generated |
| `workflow-index.md` | 3.2KB | Workflow index | **REGENERATE** | Auto-generated |
| `workflow-routing-matrix.md` | 7.8KB | Routing decisions | **YES** | Critical for `/work` |

**Elevation candidates (9 docs → rules):**
1. `automation-scripts.md` → Rule (manual or model_decision)
2. `batch-operations.md` → Merge into `06_context_engineering.md`
3. `context-loading-patterns.md` → Merge into `06_context_engineering.md`
4. `directory-structure.md` → Merge into `06_context_engineering.md`
5. `error-handling-patterns.md` → New rule or merge
6. `task-system-reference.md` → Merge into `07_task_system.md`
7. `tool-patterns.md` → New rule or merge into `06_context_engineering.md`
8. `workflow-routing-matrix.md` → Merge into `/work` workflow or new rule

**Auto-generated (4 docs → regenerate):**
- `index.md`, `rules-index.md`, `workflow-dependencies.md`, `workflow-index.md`

---

## Frontmatter Issues Analysis

### Issue 1: Excessive Fields

**Current format (WRONG):**
```yaml
---
created: "2025-10-15"
updated: "2025-10-20"
trigger: always_on
description: Core agent persona...
category: core
tokens: 1200
applyTo:
  - all
priority: high
status: active
---
```

**Should be:**
```yaml
---
trigger: always_on
---
```

**Fields to remove:** `created`, `updated`, `description`, `category`, `tokens`, `applyTo`, `priority`, `status`

**Where to move:** Post-matter section at end of file

### Issue 2: Globs Format

**Current (WRONG):**
```yaml
globs: "**/*.py, **/*.ini, **/*.yml, **/*.yaml"
```

**Should be:**
```yaml
globs: **/*.py, **/*.ini, **/*.yml, **/*.yaml
```

**Note:** Comma-separated, NO surrounding quotes

### Issue 3: Model Decision + Globs

**Current (WRONG):**
```yaml
trigger: model_decision
description: Apply when dealing with security-sensitive code...
globs: "**/*.py, **/*.ini, **/*.yml, **/*.yaml"
```

**Should be (pick ONE):**

Option A - Model decision:
```yaml
trigger: model_decision
description: Apply when dealing with security-sensitive code including API calls, user input, LLM interactions, file operations, or authentication
---
```

Option B - Glob:
```yaml
trigger: glob
globs: **/*.py, **/*.ini, **/*.yml, **/*.yaml
---
```

**Cannot have both** `model_decision` and `globs`

---

## Workflow-Rule Dependencies

### Manual Analysis Required

Need to search workflows for:
- References to `.windsurf/rules/` files
- References to `.windsurf/docs/` files
- Implicit dependencies (topics mentioned)

**Method:**
```bash
grep -r "\.windsurf/rules/" .windsurf/workflows/
grep -r "\.windsurf/docs/" .windsurf/workflows/
```

**Result:** No direct `@mention` references found in workflows

**Implication:** Rules are loaded by trigger (always_on, glob, model_decision), not by explicit mention

---

## Size Analysis

### Rules by Size

1. `07_task_system.md` - 29.1KB (29% of total) - **TOO LARGE**
2. `00_agent_directives.md` - 12.9KB (13%)
3. `06_context_engineering.md` - 11.8KB (12%)
4. `04_security.md` - 11.1KB (11%)
5. `03_documentation_lifecycle.md` - 10.7KB (11%)
6. `02_python_standards.md` - 10.1KB (10%)
7. `05_operational_protocols.md` - 10.2KB (10%)
8. `01_testing_and_tooling.md` - 5.8KB (6%)

**Windsurf limit:** 12,000 characters per rule

**Violations:**
- `00_agent_directives.md` - 12,867 bytes (**OVER LIMIT by 867 bytes**)
- `07_task_system.md` - 29,056 bytes (**OVER LIMIT by 17,056 bytes**)

---

## Criticality Assessment

### Always-On Rules (Core)

**Current:**
- `00_agent_directives.md` (always_on) - **KEEP**, but trim to <12KB

**Candidates:**
- None currently

**Recommendation:** Keep `00_agent_directives.md` as sole `always_on`, trim to essentials

### Model Decision Rules (Conditional)

**Current:**
- `04_security.md` - Security-sensitive code
- `05_operational_protocols.md` - Session end, progress
- `06_context_engineering.md` - File/git operations

**Candidates from docs:**
- `error-handling-patterns.md` - Error handling scenarios
- `workflow-routing-matrix.md` - Routing decisions

### Glob Rules (File-Type)

**Current:**
- `01_testing_and_tooling.md` - Test/source files, configs
- `02_python_standards.md` - Python files
- `03_documentation_lifecycle.md` - Markdown docs

**Issues:** Globs formatted incorrectly (quoted)

### Manual Rules (Reference)

**Current:**
- `07_task_system.md` - Task system reference

**Candidates from docs:**
- `automation-scripts.md` - Automation reference
- `batch-operations.md` - Optimization reference
- `context-loading-patterns.md` - Loading strategies
- `tool-patterns.md` - Tool usage reference

---

## Frequency Analysis

**Estimated access frequency:**

| Rule/Doc | Frequency | Reasoning |
|----------|-----------|-----------|
| `00_agent_directives.md` | Always (100%) | always_on trigger |
| `07_task_system.md` | Very High (80%) | Every workflow uses update_plan |
| `05_operational_protocols.md` | High (70%) | Session end protocol |
| `06_context_engineering.md` | High (60%) | File operations frequent |
| `04_security.md` | Medium (40%) | Security work only |
| `01_testing_and_tooling.md` | High (60%) | Glob trigger on tests/code |
| `02_python_standards.md` | High (70%) | Glob trigger on all Python |
| `03_documentation_lifecycle.md` | Medium (50%) | Glob trigger on docs |
| `automation-scripts.md` | Medium (40%) | Task automation |
| `batch-operations.md` | Medium (30%) | Performance optimization |
| `context-loading-patterns.md` | High (60%) | Context loading frequent |
| `error-handling-patterns.md` | Medium (30%) | Error scenarios |
| `tool-patterns.md` | High (50%) | Tool usage frequent |
| `workflow-routing-matrix.md` | High (70%) | /work routing |

---

## Token Budget Analysis

**Current total:** 24,868 tokens (rules) + ~15,000 tokens (docs) = ~40,000 tokens

**Target:** Optimize for ≤30,000 tokens total

**Always-loaded context:**
- `always_on` rules: ~3,175 tokens (00_agent_directives.md)
- Python glob rules when editing .py: ~4,000 tokens (01, 02)
- Doc glob rules when editing .md: ~2,600 tokens (03)

**Worst case (editing Python in docs/):** ~10,000 tokens loaded automatically

**Recommendation:** Keep individual rules <3,000 tokens ideally

---

## Consolidation Opportunities

### Opportunity 1: Context Engineering Superrule

**Merge:**
- `06_context_engineering.md` (11.8KB, 2802 tokens)
- `batch-operations.md` (6.3KB)
- `context-loading-patterns.md` (7.0KB)
- `directory-structure.md` (5.7KB)
- Parts of `tool-patterns.md` (9.5KB)

**Result:** Single `06_context_engineering.md` rule (~15-18KB) - **TOO LARGE**

**Better approach:** Split into 2-3 focused rules:
1. `06_file_operations.md` (glob: **/*.py, **/*.md, *.toml)
2. `07_context_loading.md` (model_decision: context/performance)
3. `08_git_operations.md` (model_decision: git operations)

### Opportunity 2: Task System Consolidation

**Merge:**
- `07_task_system.md` (29.1KB, 7176 tokens)
- `task-system-reference.md` (6.8KB)

**Problem:** Already over limit

**Solution:** Extract to separate rule:
- `07_task_system_core.md` (model_decision, <10KB) - Core update_plan usage
- `08_task_system_reference.md` (manual, <10KB) - Detailed reference

### Opportunity 3: Automation Reference

**Merge:**
- `automation-scripts.md` (5.5KB)
- Parts of `01_testing_and_tooling.md` (Taskfile commands)

**Result:** `09_automation_reference.md` (manual, ~8KB)

---

## Proposed New Structure (18 rules)

### Always-On (1 rule, ~3KB)

- `00_agent_directives.md` (trimmed to <12KB)

### Glob Triggers (4 rules, ~8KB)

- `01_python_standards.md` (glob: **/*.py)
- `02_testing_standards.md` (glob: tests/**/*.py, **/*test*.py)
- `03_documentation_standards.md` (glob: docs/**/*.md, *.md)
- `04_config_standards.md` (glob: *.toml, *.ini, *.yml, *.yaml, Taskfile.yml)

### Model Decision (8 rules, ~20KB)

- `05_security.md` (security-sensitive code)
- `06_context_loading.md` (context/performance optimization)
- `07_file_operations.md` (file moves, archives, indexing)
- `08_git_operations.md` (git workflows, commits)
- `09_operational_protocols.md` (session end, progress)
- `10_error_handling.md` (error scenarios)
- `11_task_system.md` (update_plan usage)
- `12_workflow_routing.md` (routing decisions)

### Manual (5 rules, ~25KB)

- `13_automation_reference.md` (automation scripts, Taskfile)
- `14_tool_patterns.md` (tool usage patterns)
- `15_task_system_reference.md` (detailed task system reference)
- `16_batch_operations.md` (optimization patterns)
- `17_directory_structure.md` (`.windsurf/` structure)

**Total:** 18 rules, ~56KB, target ~30,000 tokens

---

## Migration Risks

### Risk 1: Breaking Glob Triggers

**Mitigation:** Test each glob rule after migration

### Risk 2: Losing Metadata

**Mitigation:** Move to post-matter section

### Risk 3: Rules Not Loading

**Mitigation:** Validate frontmatter format before cutover

### Risk 4: Workflow Disruption

**Mitigation:** No workflow changes needed (no @mentions found)

---

## Next Steps

1. Design optimal trigger assignments
2. Plan content reorganization
3. Create metadata preservation format
4. Design renumbering scheme
5. Implement changes
6. Test thoroughly
7. Document migration

---

**Analysis Complete**  
**Next Phase:** Design New Structure
