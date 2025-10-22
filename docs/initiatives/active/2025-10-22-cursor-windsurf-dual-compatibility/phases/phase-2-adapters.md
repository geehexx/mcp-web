# Phase 2: Adapter Tooling Implementation 🛠️

**Status:** Planned
**Owner:** Automation Team
**Duration:** 1 week
**Priority:** P0 (Critical)

## Objective

Build the tooling that converts unified definitions into IDE-specific artifacts and ensure outputs are deterministic, validated, and testable.

## Key Tasks

- [ ] Scaffold `.unified/` directory with sample rule and command entries
- [ ] Implement `scripts/adapters/unified_parser.py` (frontmatter + content parsing)
- [ ] Implement `scripts/adapters/cursor_adapter.py` and `windsurf_adapter.py`
- [ ] Implement `scripts/adapters/validator.py` for schema enforcement
- [ ] Create `scripts/build_ide_configs.py` CLI (generate, clean, diff detection)
- [ ] Add unit tests covering parsing and transformations (≥90% coverage goal)
- [ ] Prototype Cursor/Windsurf validation commands (linting, schema checks)

## Deliverables

- Adapter module (`scripts/adapters/` with tests)
- Build script (`scripts/build_ide_configs.py`)
- Initial `.unified/` samples validated against both IDEs

## Exit Criteria

- Build script generates artifacts with no manual edits required
- Unit tests for adapters achieve ≥90% coverage
- Validation steps documented for CI integration
