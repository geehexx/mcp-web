---
title: Workflow Architecture Refactor
status: Active
created: 2025-10-18
priority: Medium
estimated_effort: 8-12 hours
tags: [workflows, architecture, optimization]
---

# Initiative: Workflow Architecture Refactor

**Status:** Active  
**Created:** 2025-10-18  
**Target Completion:** 2025-10-25  
**Owner:** @agent  
**Priority:** Medium  
**Estimated Effort:** 8-12 hours

---

## Context

During Phase 2 of workflow optimization (v2), we identified deeper architectural issues that go beyond simple decomposition:

1. **Semantic Overlap:** Multiple workflows serve similar purposes with unclear boundaries
2. **Tool Evolution:** References to deprecated tools (`mcp2_git_*`) scattered throughout
3. **Duplication:** Common patterns repeated across workflows (validation, testing, git operations)
4. **Purpose Drift:** Some workflows have grown beyond their original scope

**Source:** Feedback during windsurf-workflows-v2-optimization Phase 2 completion

**Research Reference:** [Azure AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns) - Anti-patterns section highlights:
- "Creating unnecessary coordination complexity"
- "Adding agents that don't provide meaningful specialization"

---

## Objective

Restructure workflows to eliminate semantic overlap, establish clear boundaries, and ensure each workflow provides meaningful specialization.

**Core Principle:** Each workflow should have a single, well-defined purpose that doesn't overlap with others.

---

## Success Criteria

- [ ] Clear workflow taxonomy defined (categorization by purpose)
- [ ] Zero tool reference errors (all use correct tools)
- [ ] Duplication eliminated (DRY principle applied)
- [ ] Each workflow has unique value proposition
- [ ] Integration points clearly documented
- [ ] All workflows follow consistent patterns
- [ ] Documentation reflects new architecture

**Verification:**
- Grep for deprecated tool references: `grep -r "mcp2_" .windsurf/workflows/` returns empty
- Manual review confirms no semantic overlap
- Each workflow can explain "what makes it different from X"

---

## Research Summary

### Current Issues Identified

**1. Semantic Overlap Examples:**

| Workflow | Purpose (Current) | Overlaps With | Issue |
|----------|------------------|---------------|-------|
| `/run-tests` | Test execution reference | `/validate` | Both explain pytest-xdist, test types |
| `/validate` | Quality gate (lint+test+security) | `/run-tests`, `/commit` | Testing logic duplicated |
| `/commit` | Git operations + validation | `/validate` | Validation checklist duplicated |

**2. Tool Reference Issues:**

- `/commit` references `mcp2_git_status`, `mcp2_git_diff_unstaged`, `mcp2_git_add`, `mcp2_git_commit`, `mcp2_git_log`
- These tools no longer exist (MCP git server not in use)
- Should use standard `git` commands via `run_command` tool

**3. Purpose Ambiguity:**

- Is `/run-tests` a workflow or documentation?
- Does `/validate` orchestrate or document?
- When to call `/validate` vs `/run-tests`?

### Proposed Taxonomy

**Category 1: Orchestrators** (High-level coordination)
- `/work` - Master orchestrator
- `/plan` - Planning orchestrator
- `/implement` - Implementation orchestrator

**Category 2: Specialized Operations** (Focused tasks)
- `/validate` - Quality gate (atomic operation)
- `/commit` - Git operations (atomic operation)
- `/bump-version` - Versioning (atomic operation)
- `/update-docs` - Documentation sync (atomic operation)

**Category 3: Context Handlers** (Information gathering)
- `/detect-context` - Project state analysis
- `/load-context` - Batch context loading
- `/extract-session` - Session data extraction

**Category 4: Artifact Generators** (Content creation)
- `/generate-plan` - Plan document generation
- `/summarize-session` - Session summary generation
- `/new-adr` - ADR creation

**Category 5: Reference Guides** (Documentation, not workflows)
- Move `/run-tests` to `docs/guides/testing-reference.md`
- Keep only true workflows in `.windsurf/workflows/`

---

## Implementation Plan

### Phase 1: Analysis & Design (3-4 hours)

**Tasks:**

1. **Audit all workflows** (1h)
   - List every workflow with current purpose
   - Identify all overlapping responsibilities
   - Find all deprecated tool references
   - Document integration points

2. **Design new taxonomy** (1h)
   - Categorize by true purpose
   - Define clear boundaries
   - Establish naming conventions
   - Create decision tree for "which workflow to use"

3. **Create migration plan** (1h)
   - Identify which workflows to merge
   - Identify which to split
   - Identify which to deprecate
   - Plan for backward compatibility

4. **Research best practices** (1h)
   - Web search: "workflow orchestration patterns 2025"
   - Web search: "agent coordination anti-patterns"
   - Review Azure AI orchestration patterns (already retrieved)
   - Document findings and recommendations

**Exit Criteria:** Architecture document with clear taxonomy and migration plan

**Deliverables:**
- `docs/adr/ADR-XXXX-workflow-architecture-v3.md`
- Migration checklist in this initiative

### Phase 2: Tool Reference Fixes (2-3 hours)

**Tasks:**

1. **Replace MCP git tool references** (1h)
   - Grep all workflows for `mcp2_git_*`
   - Replace with standard `git` commands via `run_command`
   - Test all git operations work correctly
   - Update any rules that reference MCP git tools

2. **Standardize tool invocation patterns** (1h)
   - Define standard patterns for git, pytest, ruff, etc.
   - Apply consistently across all workflows
   - Document in workflow template

3. **Validation and testing** (1h)
   - Run through each workflow manually
   - Verify tool calls work as expected
   - Fix any edge cases discovered

**Exit Criteria:** Zero references to deprecated tools, all tool calls valid

**Deliverables:**
- Updated workflow files with correct tool references
- Tool invocation standard documented

### Phase 3: Consolidation & Restructuring (3-4 hours)

**Tasks:**

1. **Merge/eliminate overlapping workflows** (2h)
   - Based on Phase 1 design
   - Preserve unique functionality
   - Add cross-references where needed
   - Update all caller references

2. **Move reference docs out of workflows/** (1h)
   - Create `docs/guides/` for reference material
   - Move `/run-tests` → `docs/guides/testing-reference.md`
   - Update cross-references
   - Add frontmatter note: "See docs/guides/ for references"

3. **Update integration points** (1h)
   - Ensure all workflow calls still work
   - Update `/work` routing logic
   - Test complete workflow chains
   - Verify no broken references

**Exit Criteria:** 
- All workflows follow new taxonomy
- No semantic overlap
- All reference docs in proper location

**Deliverables:**
- Consolidated workflow files
- Updated `docs/guides/` directory
- Integration test results

### Phase 4: Documentation & Validation (1-2 hours)

**Tasks:**

1. **Update documentation** (1h)
   - Update `docs/DOCUMENTATION_STRUCTURE.md`
   - Add workflow decision tree
   - Update all cross-references
   - Add migration notes for future reference

2. **Final validation** (1h)
   - Run through all workflows
   - Verify each has unique purpose
   - Check all tool references work
   - Confirm no duplication remains

**Exit Criteria:** Documentation complete, all workflows validated

**Deliverables:**
- Updated documentation
- Workflow decision tree/diagram
- Validation report

---

## Dependencies

**Prerequisites:**
- windsurf-workflows-v2-optimization Phase 1 ✅ (Complete)
- windsurf-workflows-v2-optimization Phase 2 ✅ (Complete)

**Blockers:**
- None (can start immediately)

---

## Risks & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Breaking existing workflow chains | Medium | High | Test all integration points, add deprecation warnings before removal |
| User confusion during transition | Low | Medium | Document changes clearly, provide migration guide |
| Scope creep (too many changes) | High | Medium | Strict adherence to taxonomy, defer non-critical changes |
| Missing edge cases in tool references | Medium | Medium | Comprehensive grep + manual review + testing |

**Out of Scope:**
- New workflow features (focus on restructuring only)
- Performance optimization (separate initiative)
- AI model improvements (separate concern)

---

## ADRs

- [ ] ADR-XXXX: Workflow Architecture V3 - Taxonomy and Principles

**ADR Required:** Yes - Significant architectural change affecting all workflows

---

## Related Documentation

- `docs/initiatives/active/windsurf-workflows-v2-optimization.md` - Parent initiative
- `docs/DOCUMENTATION_STRUCTURE.md` - Will be updated
- `.windsurf/workflows/*.md` - All workflow files affected
- `.windsurf/rules/00_agent_directives.md` - May need updates for tool patterns

---

## Updates

### 2025-10-18 (Creation)
Initiative created based on feedback during Phase 2 of workflow optimization. Identified need for deeper architectural refactor beyond simple decomposition.

**Trigger:** User feedback: "There's very heavy overlap and redundancy between workflows... we might want to re-think at a higher level the purpose of the workflows"

**Decision:** Create separate initiative to avoid scope creep in v2-optimization. This allows focused work on architecture without derailing token optimization.

---

## Success Metrics

**Quantitative:**
- Deprecated tool references: 0 (currently: ~10)
- Workflow semantic overlap: 0 (currently: 3 pairs identified)
- Reference docs in workflows/: 0 (move to docs/guides/)

**Qualitative:**
- Each workflow can articulate unique value in 1 sentence
- Clear decision tree for "which workflow to call when"
- Consistent tool invocation patterns across all workflows

**Time:**
- Estimated: 8-12 hours across 2-3 sessions
- Target completion: 1 week from start

---

## Future Considerations

**Post-refactor opportunities:**
- Workflow versioning system
- Automated workflow testing framework
- Workflow performance profiling
- AI-generated workflow suggestions based on context

**Dependencies on this initiative:**
- Token optimization (Phase 3) should wait for architecture stabilization
- Any new workflow creation should follow new taxonomy
- Documentation updates should reflect new structure
