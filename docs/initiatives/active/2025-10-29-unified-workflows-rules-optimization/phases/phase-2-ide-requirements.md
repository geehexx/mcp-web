# Phase 2: IDE Requirements Analysis

**Status:** Planned
**Owner:** Core Team
**Duration:** ~1 hour
**Priority:** P0 (Critical)

---

## Objective

Validate the minimal schema required by Windsurf and Cursor, document mandatory vs optional fields,
define structured metadata fields that preserve hidden sections (e.g., `ide.hidden_sections`,
`ide.metadata`), and confirm adapter expectations prior to frontmatter refactors.

---

## Key Tasks

- [ ] Review Windsurf workflow documentation for `auto_execution_mode`, trigger types, and frontmatter expectations
- [ ] Collect Cursor rule behaviour references (community notes, existing adapters) to confirm `alwaysApply`, `globs`, and description-driven triggers
- [ ] Map required/optional fields into the JSON schema (`.unified/schemas/frontmatter-minimal.json`)
- [ ] Identify deprecated/unused fields to remove in Phase 3
- [ ] Define structured metadata fields for hidden sections (e.g., `ide.hidden_sections`,
  `ide.metadata`) and draft migration guidance
- [ ] Document compatibility notes for adapters (`scripts/adapters/cursor_adapter.py`, `scripts/adapters/windsurf_adapter.py`)
- [ ] Capture research findings in `research/external-sources.md`

---

## Checkpoints & Cadence

| ID | Trigger | Required Actions |
|----|---------|------------------|
| C2.1 | Research notes captured | Commit references and summaries to `research/external-sources.md`; annotate this phase with methodology; push branch |
| C2.2 | Minimal schema drafted | Commit `.unified/schemas/frontmatter-minimal.json` (draft) with validation stub; request async review |
| C2.3 | Adapter impact assessed | Update phase notes with adapter expectations; log follow-ups in `artifacts/metadata-removal-playbook.md`; run `/commit` workflow before advancing |

Advance to Phase 3 only when C2.3 is complete and approvals recorded.

---

## Deliverables

- Draft minimal frontmatter JSON schema
- Field usage matrix updated with required/optional/forbidden indicators
- Research notes citing Windsurf docs and Cursor community references

---

## Entry Criteria

- Phase 1 inventory results available for reference
- Access to Windsurf and Cursor documentation (mirrors or cached copies)
- Agreement on target schema expectations with stakeholders

---

## Exit Criteria

- Minimal schema drafted and reviewed
- List of fields to remove/add approved for Phase 3
- Adapters impact assessment documented

---

## Notes

- Preserve security-first posture: verify that no sensitive metadata is lost that might affect guardrails
- Capture fallback references if official docs are inaccessible (e.g., gist mirrors)
- Coordinate with Validation tooling maintainers before finalising schema to ensure enforcement alignment
- Include citation links or archived copies of external docs within the commit description for traceability
