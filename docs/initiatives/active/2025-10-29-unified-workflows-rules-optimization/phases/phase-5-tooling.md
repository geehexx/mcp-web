# Phase 5: Tooling & Validation Hardening

**Status:** Planned
**Owner:** Core Team
**Duration:** ~1.5 hours
**Priority:** P1 (High)

---

## Objective

Update adapters, validators, and CI hooks to enforce the minimal schema and prevent regressions in generated Windsurf and Cursor artifacts.

---

## Key Tasks

- [ ] Update `scripts/adapters/cursor_adapter.py` to emit minimal frontmatter and raw glob strings
- [ ] Update `scripts/adapters/windsurf_adapter.py` to require `auto_execution_mode` and trimmed metadata
- [ ] Enhance `scripts/validate_workflows.py` (or successor) with schema checks, forbidden field detection, and metadata section scans
- [ ] Add/extend pre-commit hook entry for unified validation (`.pre-commit-config.yaml`)
- [ ] Create/expand unit tests covering adapters, validators, and schema (target ≥90% statement coverage)
- [ ] Run regression suite (`task lint`, `uv run mypy`, `uv run pytest -n auto`, security scans) to confirm stability

---

## Checkpoints & Cadence

| ID | Trigger | Required Actions |
|----|---------|------------------|
| C5.1 | Adapters updated with schema changes | Commit adapter updates + targeted tests; document rationale in this phase file; push branch |
| C5.2 | Validation scripts hardened | Commit validator enhancements + coverage metrics in `artifacts/validation-checklist.md`; run `/commit` workflow |
| C5.3 | Regression suite + coverage targets achieved | Attach test logs, coverage reports, and security scan summaries; update initiative "Updates" with outcomes; push branch |

Advance to Phase 6 only when C5.3 evidence is logged and shared.

---

## Deliverables

- Updated adapters and validation scripts in `scripts/`
- Test suite additions with coverage report meeting target thresholds
- Pre-commit configuration enforcing unified validation
- Validation checklist updated with new gates

---

## Entry Criteria

- Frontmatter and content optimizations (Phases 3–4) merged in feature branch
- Minimal schema finalized and stored in repository
- Baseline tests currently green (from Phase 0/1 validation)

---

## Exit Criteria

- All validation scripts pass against updated `.unified/` files
- Adapters regenerate `.cursor/` and `.windsurf/` artifacts without drift
- Test coverage metric achieved (documented in `artifacts/validation-checklist.md`)
- CI/Pre-commit safeguards enabled and documented

---

## Notes

- Leverage Testing Excellence initiative patterns for high-coverage adapter testing
- If new scripts are introduced, ensure they follow security practices (input validation, safe file IO)
- Capture any discovered issues or follow-up tasks in initiative updates or TODO tracker
- Include coverage summaries and command transcripts in `artifacts/validation-checklist.md` to support PR validation narrative
