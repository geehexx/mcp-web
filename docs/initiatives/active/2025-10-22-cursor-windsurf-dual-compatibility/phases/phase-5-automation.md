# Phase 5: Automation & IDE Detection ⚙️

**Status:** Planned
**Owner:** DevOps Automation Team
**Duration:** 1 week
**Priority:** P1 (High)

## Objective

Integrate the adapter pipeline into CI/CD, implement IDE detection hooks for local scripts, and enforce zero-drift guarantees across developer workflows.

## Key Tasks

- [ ] Add `scripts/build_ide_configs.py` to Taskfile (`task ide:build`)
- [ ] Implement IDE detection helper (`scripts/lib/ide_context.py`) with overrides
- [ ] Update automation scripts to branch on detected IDE (Cursor vs Windsurf)
- [ ] Add CI job ensuring regenerated artifacts match committed versions
- [ ] Integrate markdown linting/validation for Cursor `.mdc` outputs
- [ ] Document local development workflow (`task ide:dev`) for both IDEs
- [ ] Establish cache/locking strategy to avoid race conditions in CI runs

## Deliverables

- Updated Taskfile entries and supporting scripts
- CI pipeline configuration enforcing regeneration and lint checks
- Developer guide snippet embedded in Phase 6 docs

## Exit Criteria

- CI fails if generated artifacts differ from committed state
- Local automation detects IDE accurately with documented overrides
- Developers have a reproducible command set for both IDE workflows
