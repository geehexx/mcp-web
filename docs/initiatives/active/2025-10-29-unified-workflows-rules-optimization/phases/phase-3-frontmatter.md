# Phase 3: Frontmatter Optimization

**Status:** Planned
**Owner:** Core Team
**Duration:** ~2 hours
**Priority:** P0 (Critical)

---

## Objective

Apply the minimal schema to every `.unified/**/*.yaml` file, remove redundant fields, and add missing Windsurf metadata so that adapters receive consistent inputs.

---

## Key Tasks

- [ ] Implement `.unified/schemas/frontmatter-minimal.json` with required/optional fields
- [ ] Update all unified files to remove deprecated fields (`title`, `type`, `tags`, `related`, `status`, `windsurf.*` bloat, `cursor.pass_through`)
- [ ] Add `windsurf.auto_execution_mode: 3` to workflows (unless analysis dictates other values)
- [ ] Normalize Cursor globs to raw comma-separated strings (no YAML lists)
- [ ] Record before/after token and schema compliance snapshots in `artifacts/token-inventory.md`
- [ ] Validate schema across repo using updated validation script

---

## Checkpoints & Cadence

| ID | Trigger | Required Actions |
|----|---------|------------------|
| C3.1 | Schema implemented in repo tooling | Commit schema enforcement updates (validators/tests) alongside documentation in this phase file; push branch |
| C3.2 | First batch (≤10 files) migrated | Commit batch with clear scope (`refactor(unified): apply minimal schema to workflows batch 1`), update token deltas in artifacts, run `/commit` workflow |
| C3.3 | All files migrated & validation green | Commit final batch, attach validation logs, update initiative "Updates" with summary and blockers |

Do not advance to Phase 4 until C3.3 confirms full compliance and artifacts are refreshed.

---

## Deliverables

- Minimal schema file committed
- All unified files compliant with new schema and recorded in checklist
- Token delta documenting field removals vs additions

---

## Entry Criteria

- Phase 2 schema decisions approved
- Baseline backups and metrics from Phases 0–1 completed
- Validation tooling updated or ready to accept new schema

---

## Exit Criteria

- Schema validation passes for all `.unified/` files
- Windsurf workflows include `auto_execution_mode`
- Cursor-specific fields formatted as required
- No deprecated fields remaining (verified via validation script)

---

## Notes

- Consider batching edits (5–10 files per commit) to simplify review if PR is large
- Coordinate with adapter maintainers so transitional builds do not break downstream consumers
- Ensure any files requiring exceptions are documented in artifacts and initiative narrative
- Tag batches in `artifacts/token-inventory.md` with commit SHAs for traceability and regression analysis
