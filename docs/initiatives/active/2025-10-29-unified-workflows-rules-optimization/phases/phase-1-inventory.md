# Phase 1: Inventory & Measurement

**Status:** Planned
**Owner:** Core Team
**Duration:** ~2 hours
**Priority:** P0 (Critical)

---

## Objective

Quantify the current `.unified/` footprint, identify high-bloat targets, and catalogue existing frontmatter and metadata usage to guide later optimization.

---

## Key Tasks

- [ ] Enumerate all `.unified/**/*.yaml` files and record counts by type (rules vs workflows)
- [ ] Measure current file sizes (chars/tokens) and list top 10 heaviest files
- [ ] Detect redundant sections (`## Command Metadata`, `## Rule Metadata`, boilerplate context sections)
- [ ] Catalog frontmatter fields in use across files (populate `artifacts/frontmatter-field-matrix.md`)
- [ ] Document metadata removal candidates in `artifacts/metadata-removal-playbook.md`
- [ ] Summarize findings with recommended focus order for subsequent phases

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
