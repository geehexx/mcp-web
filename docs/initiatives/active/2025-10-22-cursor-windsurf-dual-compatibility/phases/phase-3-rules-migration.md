# Phase 3: Rules Migration & Validation ✅

**Status:** Planned
**Owner:** Documentation & Tooling Team
**Duration:** 1 week
**Priority:** P0 (Critical)

## Objective

Convert all Windsurf rules into the unified format, regenerate both IDE representations, and validate behaviour across Cascades and Cursor to guarantee consistency.

## Key Tasks

- [ ] Inventory 16 Windsurf rules (triggers, tags, cross references)
- [ ] Author unified `.yaml` definitions for each rule
- [ ] Generate new `.windsurf/rules/*.md` via build script and diff against baseline
- [ ] Generate `.cursor/rules/*.mdc` files and run Cursor validation/linting
- [ ] Resolve lossy conversions (`model_decision`, manual overrides) with documented fallbacks
- [ ] Implement regression tests ensuring regenerated Windsurf rules match source content
- [ ] Update related documentation/links if file names change

## Deliverables

- `.unified/rules/*.yaml` covering all Windsurf rules
- Regenerated `.windsurf/rules/*.md` and `.cursor/rules/*.mdc`
- Validation report summarizing trigger mapping decisions

## Exit Criteria

- All rule diffs reviewed and approved by maintainers
- Cursor validation passes for entire rule set
- Golden snapshot stored to detect future drift
