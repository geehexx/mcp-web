# Phase 7: Monitoring & Continuous Improvement

**Status:** Planned
**Owner:** Core Team
**Duration:** ~1 hour (initial rollout) + ongoing monitoring
**Priority:** P2 (Medium)

---

## Objective

Establish feedback loops, monitor unified workflow/rule health post-merge, and queue follow-up refinements based on real-world usage.

---

## Key Tasks

- [ ] Collect Windsurf and Cursor usage feedback from contributors (surveys, issue tracker, direct reports)
- [ ] Monitor regenerated `.cursor/` and `.windsurf/` artifacts for drift (weekly automated check)
- [ ] Track token budget as new workflows/rules are added (update `artifacts/token-inventory.md` quarterly)
- [ ] Review validation logs for schema violations or regressions (tie into CI alerts)
- [ ] Identify opportunities for further automation (e.g., token measurement script, lint rule)
- [ ] Document lessons learned and potential ADR needs for future improvements

---

## Checkpoints & Cadence

| ID | Trigger | Required Actions |
|----|---------|------------------|
| C7.1 | First monitoring cycle completed | Commit monitoring log updates, note feedback, and capture token drift metrics |
| C7.2 | Follow-up backlog created | File issues or TODOs for identified improvements; update initiative "Updates" with owners |
| C7.3 | Initiative transition formalised | Document handoff summary, assign ongoing maintenance owners, archive initiative when ready |

Close initiative and archive artifacts once C7.3 is captured and communicated to stakeholders.

---

## Deliverables

- Monitoring log capturing feedback, drift checks, and follow-up tasks
- Quarterly token budget updates
- Backlog items or ADR proposals when structural changes are warranted

---

## Entry Criteria

- Phase 6 rollout completed with documentation updates merged
- Validation checklist green with CI hooks active
- Stakeholders notified of changes

---

## Exit Criteria

- Initial monitoring plan executed (feedback channel open, first drift check completed)
- Follow-up tasks prioritized and assigned
- Initiative transitioned to maintenance mode with clear owners

---

## Notes

- Integrate with existing initiative/session logs if available to avoid duplicate reporting
- Use Testing Excellence dashboards or metrics pipelines when they cover relevant data (e.g., coverage, flakiness)
- Consider automation to fail fast on schema regressions (e.g., GitHub Actions, Taskfile job)
- Share monitoring results during weekly syncs and ensure backlog tickets reference specific metrics or failures observed
