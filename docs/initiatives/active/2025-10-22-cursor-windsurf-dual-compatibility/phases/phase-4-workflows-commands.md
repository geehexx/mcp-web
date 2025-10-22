# Phase 4: Workflow & Command Alignment 🔄

**Status:** Planned
**Owner:** Workflow Orchestration Team
**Duration:** 1 week
**Priority:** P1 (High)

## Objective

Translate Windsurf workflows into unified definitions, generate Cursor-friendly command equivalents, and ensure task orchestration remains coherent despite IDE capability differences.

## Key Tasks

- [ ] Catalogue 21 Windsurf workflows (stages, dependencies, invocation patterns)
- [ ] Author unified command/workflow definitions capturing objectives, steps, and expected outputs
- [ ] Generate refreshed `.windsurf/workflows/*.md` and verify Cascade compatibility
- [ ] Generate `.cursor/commands/*.md` with embedded context to replace multi-stage orchestration
- [ ] Define lightweight command variants for workflows that exceed Cursor context limits
- [ ] Document manual trigger guidance for workflows lacking direct Cursor parity
- [ ] Update handoff guide with workflow/command mapping table

## Deliverables

- `.unified/commands/*.yaml` covering all workflows
- Regenerated Windsurf workflow files and Cursor command files
- Mapping matrix documenting limitations and manual procedures

## Exit Criteria

- All workflows have Cursor command counterparts or documented manual procedures
- Windsurf workflows execute without regression after regeneration
- Cursor commands reviewed and validated via smoke tests in IDE
