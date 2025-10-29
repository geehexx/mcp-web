# Validation Checklist

Use this checklist to ensure schema, adapter, and content changes meet quality gates before merging.

---

## Pre-Optimization Baseline (Phase 0)

- [ ] `python scripts/validate_workflows.py`
- [ ] `python scripts/build_ide_configs.py`
- [ ] Capture outputs and diff status (no unexpected changes)
- [ ] Record baseline coverage metrics (if available)

---

## Schema & Frontmatter (Phase 3)

- [ ] `.unified/schemas/frontmatter-minimal.json` validated (JSON schema lint)
- [ ] All `.unified/**/*.yaml` files conform to schema
- [ ] No forbidden fields present (validated via script)
- [ ] Windsurf workflows include `auto_execution_mode`
- [ ] Cursor globs formatted as raw strings

---

## Content Optimization (Phase 4)

- [ ] Metadata sections removed (grep for `## Command Metadata` / `## Rule Metadata` returns empty)
- [ ] Context-loading boilerplate replaced with concise guidance
- [ ] Token savings recorded in `artifacts/token-inventory.md`
- [ ] Peer/self review confirms clarity maintained

---

## Tooling & Validation (Phase 5)

- [ ] Adapters updated (`cursor_adapter.py`, `windsurf_adapter.py`) and tests added
- [ ] Validation script enhanced with schema + forbidden field checks
- [ ] Pre-commit hook updated to run validation script
- [ ] Test coverage ≥90% for updated modules
- [ ] Security scans (bandit, semgrep) executed

---

## Rollout (Phase 6)

- [ ] `.unified/README.md` updated with minimal schema guidance
- [ ] Related guides/docs refreshed
- [ ] Full regression suite executed: `task lint`, `uv run mypy`, `uv run pytest -n auto`, `uv run bandit`, `uv run semgrep`
- [ ] `.cursor/` and `.windsurf/` regenerated with zero diffs on rerun
- [ ] Initiative update posted summarizing outcomes
- [ ] Stakeholders notified; follow-up tasks logged

---

## Post-Merge Monitoring

- [ ] Monitor IDE usage feedback (Cursor & Windsurf)
- [ ] Track token metrics for future additions (ensure new files follow schema)
- [ ] Re-run validation checklist if significant changes occur
