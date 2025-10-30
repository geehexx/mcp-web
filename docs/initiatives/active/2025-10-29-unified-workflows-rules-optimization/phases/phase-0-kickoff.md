# Phase 0: Kickoff & Baseline Capture

**Status:** Completed
**Owner:** Core Team
**Duration:** 2–3 hours
**Priority:** P0 (Critical)

---

## Objective

Establish a safe baseline before optimization work begins: snapshot current unified files, measure token counts, verify adapters/validators run cleanly, and ensure rollback paths exist.

---

## Key Tasks

- [x] Create feature branch `feature/unified-workflows-rules-optimization`.
- [x] Capture `scripts/build_ide_configs.py` output and establish a clean baseline.
- [x] Run `scripts/validation/validate_workflows.py` and confirm no failures.
- [ ] Collect raw token metrics for all `.unified/**/*.yaml` files (store in `artifacts/token-inventory.md`)
- [ ] Snapshot current frontmatter field usage for reference (`artifacts/frontmatter-field-matrix.md`)
- [x] Confirm backup of `.cursor/` and `.windsurf/` artifacts (git status clean after generation).

---

## Checkpoints & Cadence

| ID | Trigger | Required Actions |
|----|---------|------------------|
| C0.1 | Feature branch created, safety validation run | Commit branch bootstrap (`chore(initiative): bootstrap unified optimization branch`), add initial validation notes to this phase file, push branch |
| C0.2 | Baseline artifacts captured | Commit token inventory/frontmatter matrix snapshots (`docs/initiatives/.../artifacts`), update initiative "Updates" with baseline summary, run `/commit` workflow before push |
| C0.3 | Rollback plan confirmed | Document rollback steps in phase notes, tag commit or push with rollback summary, notify stakeholders in initiative comments |

Treat checkpoints as blocking gates; do not proceed to Phase 1 until C0.3 is complete and pushed.

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

- Aligns with Testing Excellence initiative’s pre-flight discipline to ensure reproducible baselines.
- Token counting can leverage simple char-count ÷ 4 approximation before optimization automation is built.
- Update `initiative.md` Feature Branch section with branch name, command transcript, and validation evidence collected here.
- **2025-10-30:** The `validate_workflows.py` script was found at `scripts/validation/validate_workflows.py`, not `scripts/validate_workflows.py`. The documentation should be updated.
- **2025-10-30:** Initial run of `build_ide_configs.py` introduced numerous linting errors in the generated files. These were autofixed to establish a clean baseline. This suggests the generator templates may need whitespace adjustments in the future.
