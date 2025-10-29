# Phase 0: Kickoff & Baseline Capture

**Status:** Planned
**Owner:** Core Team
**Duration:** 2–3 hours
**Priority:** P0 (Critical)

---

## Objective

Establish a safe baseline before optimization work begins: snapshot current unified files, measure token counts, verify adapters/validators run cleanly, and ensure rollback paths exist.

---

## Key Tasks

- [ ] Create safety branch (e.g., `git checkout -b initiative/unified-optimization-KO`)
- [ ] Capture `scripts/build_ide_configs.py` output and archive in `artifacts/token-inventory.md`
- [ ] Run `python scripts/validate_workflows.py` and document current failures (if any)
- [ ] Collect raw token metrics for all `.unified/**/*.yaml` files (store in `artifacts/token-inventory.md`)
- [ ] Snapshot current frontmatter field usage for reference (`artifacts/frontmatter-field-matrix.md`)
- [ ] Confirm backup of `.cursor/` and `.windsurf/` artifacts (git status clean)

---

## Deliverables

- Baseline token inventory (before optimization)
- Baseline frontmatter matrix (fields in use)
- Validation report noting current script/adapters status

---

## Entry Criteria

- Initiative plan approved
- Access to necessary scripts (`build_ide_configs.py`, `validate_workflows.py`)
- Ability to run Taskfile/uv commands locally

---

## Exit Criteria

- Baseline artifacts committed to initiative artifacts directory
- Validation and build scripts confirmed to run without unexpected errors
- Rollback plan documented (branch and backups ready)

---

## Notes

- Aligns with Testing Excellence initiative’s pre-flight discipline to ensure reproducible baselines
- Token counting can leverage simple char-count ÷ 4 approximation before optimization automation is built
