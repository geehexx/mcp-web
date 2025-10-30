# Phase 1: Inventory & Measurement

**Status:** Completed
**Owner:** Core Team
**Duration:** ~2 hours
**Priority:** P0 (Critical)

---

## Objective

Quantify the current `.unified/` footprint, identify high-bloat targets, and catalogue existing frontmatter and metadata usage to guide later optimization.

---

## Key Tasks

- [x] Enumerate all `.unified/**/*.yaml` files and record counts by type (rules vs workflows)
- [x] Measure current file sizes (chars/tokens) and list top 10 heaviest files
- [x] Detect redundant sections (`## Command Metadata`, `## Rule Metadata`, boilerplate context sections)
- [x] Catalog frontmatter fields in use across files (populate `artifacts/frontmatter-field-matrix.md`)
- [x] Document metadata removal candidates in `artifacts/metadata-removal-playbook.md`
- [x] Summarize findings with recommended focus order for subsequent phases

---

## Checkpoints & Cadence

| ID | Trigger | Required Actions |
|----|---------|------------------|
| C1.1 | Inventory scripts executed, raw metrics captured | Commit measurement tooling (`scripts/analysis/*`) and raw outputs in `artifacts/token-inventory.md`; update this phase log with methodology; push branch |
| C1.2 | High-bloat targets identified | Commit prioritized list + notes in `artifacts/metadata-removal-playbook.md`; update initiative "Updates" with focus order; run `/commit` workflow |
| C1.3 | Stakeholder sign-off on focus order | Record approval comments in phase file; create TODOs/backlog issues if adjustments needed; push branch with sign-off summary |

Proceed to Phase 2 only after C1.3 is completed, committed, and pushed.

---

## Deliverables

- Updated token inventory with per-file metrics
- Frontmatter field usage matrix
- Metadata removal playbook with prioritized sections and rationale

---

## Entry Criteria

- Phase 0 baseline artifacts complete
- Access to repo and ability to run measurement scripts or commands
- Agreement on token estimation methodology (chars/4 approximation acceptable initially)

---

## Exit Criteria

- Baseline metrics documented in artifacts directory
- High-bloat targets identified and ranked
- Metadata removal candidates approved for Phase 4 execution

---

## Notes

- Automate measurement where possible (Python script, Taskfile). Manual collection should be temporary
- Consider capturing histogram or summary statistics to highlight long-tail outliers
- Coordinate with Testing Excellence initiative to align measurement techniques if new tooling is introduced
- When committing outputs, keep raw data under `artifacts/` and include command snippets in commit messages for reproducibility
