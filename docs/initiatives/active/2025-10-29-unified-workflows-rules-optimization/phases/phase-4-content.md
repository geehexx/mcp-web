# Phase 4: Content Optimization

**Status:** Planned
**Owner:** Core Team
**Duration:** ~1.5 hours
**Priority:** P1 (High)

---

## Objective

Streamline workflow and rule bodies by removing redundant sections, consolidating boilerplate context, and ensuring each document delivers high-value guidance with minimal tokens.

---

## Key Tasks

- [ ] Remove `## Command Metadata` / `## Rule Metadata` sections and similar redundant blocks identified in Phase 1
- [ ] Replace repetitive context-loading paragraphs with concise references to `/rules/` directory guidance
- [ ] Consolidate or relocate low-value sections (e.g., generic integration or anti-patterns) into centralized documentation where appropriate
- [ ] Ensure remaining sections follow consistent, concise structure (Objective, Prerequisites, Steps, Validation, etc.)
- [ ] Record token savings per file and aggregate results in `artifacts/token-inventory.md`
- [ ] Update `artifacts/metadata-removal-playbook.md` with actual removals and lessons learned

---

## Checkpoints & Cadence

| ID | Trigger | Required Actions |
|----|---------|------------------|
| C4.1 | First batch of content refactors landed | Commit scoped changes (≤5 files) with before/after notes in this phase file; update token deltas in artifacts |
| C4.2 | Boilerplate removal playbook executed | Commit consolidated guidance, update initiative "Updates" with lessons learned, run `/commit` workflow |
| C4.3 | Peer/self review documented | Record review notes, link to diff annotations, ensure clarity preserved; push branch |

Advance to Phase 5 only after C4.3 confirms clarity maintained and metrics recorded.

---

## Deliverables

- Updated `.unified/` content with redundant sections removed
- Token savings report reflecting content optimizations
- Playbook documenting adjustments and reusable patterns
- Updated `artifacts/hidden-section-map.md` showing mappings between removed sections and
  frontmatter entries (`ide.hidden_sections`, `ide.metadata`)

---

## Entry Criteria

- Phase 3 frontmatter optimization complete
- Metadata removal candidates validated and approved
- Baseline content snapshots captured for comparison

---

## Exit Criteria

- All targeted sections removed or refactored without losing essential guidance
- Token savings documented and ≥50% of total target achieved through content work
- No workflows/rules regress in clarity; peer review or self-audit recorded in artifacts

---

## Notes

- Maintain security-first language; do not remove warnings or safeguards that enforce OWASP LLM Top 10 principles
- Use initiative artifact structure to store before/after excerpts if helpful for future audits
- Coordinate with documentation maintainers to centralize repeated guidance where applicable
- Capture representative before/after samples in `artifacts/metadata-removal-playbook.md` and attach commit SHAs for future audits
