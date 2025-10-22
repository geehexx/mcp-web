---
Status: "Active"
Created: "2025-10-22"
Updated: "2025-10-22"
Owner: "@ai-agent"
Priority: "High"
Estimated Duration: "8 weeks (~60 hours)"
Target Completion: "2025-12-15"
Tags:
  - "cursor"
  - "windsurf"
  - "automation"
  - "workflows"
  - "rules"
  - "tooling"
Related:
  - "/docs/adr/0002-adopt-windsurf-workflow-system.md"
  - "/docs/adr/0018-workflow-architecture-v3.md"
  - "/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/artifacts/research.md"
  - "/CURSOR_AGENT_HANDOFF.md"
  - "/.windsurf/rules/"
  - "/.windsurf/workflows/"
---
# Initiative: Cursor & Windsurf Dual Compatibility

## Objective

Establish a unified, adapter-driven rules and workflows system so `.windsurf/` and `.cursor/` artifacts remain synchronized, enabling contributors to operate the project from either IDE without duplicate maintenance or drift in standards.

## Success Criteria

- [ ] `.unified/` definitions regenerate Windsurf and Cursor artifacts deterministically (no diffs on repeated builds)
- [ ] Generated `.cursor/rules/*.mdc` files pass Cursor validation and markdown linting
- [ ] Generated `.windsurf/rules/*.md` and workflows pass Windsurf validation and existing workflow checks
- [ ] `scripts/build_ide_configs.py` runs in CI with zero-diff enforcement and failure on drift
- [ ] Adapter and validator test suite achieves ≥90% statement coverage
- [ ] Dual-IDE operations guide published covering setup, troubleshooting, and migration FAQs

## Motivation

### Problem

- Windsurf has comprehensive workflows and rules, but Cursor contributors lack equivalent automation or guardrails.
- Maintaining separate rule/workflow sets would inevitably diverge, risking conflicting security or coding standards.
- Existing automation assumes Windsurf-only execution and cannot detect or adapt to Cursor usage.

### Impact

- Cursor-focused teams are blocked from executing repository workflows, reducing contributor velocity.
- Divergent documentation increases the likelihood of inconsistent behaviour across IDEs.
- CI/CD currently lacks safeguards to ensure Cursor artifacts remain current with Windsurf updates.

### Value

- A single source of truth reduces review overhead and maintenance effort.
- Dual IDE support broadens the contributor base while preserving Windsurf’s orchestration strengths.
- Automated guardrails guarantee future rule/workflow changes propagate to both IDE ecosystems reliably.

## Scope

### In Scope

- Unified specification covering rules, commands, workflows, and metadata.
- Adapter toolchain (`scripts/adapters/`) and build automation that generate IDE-specific artifacts.
- Migration of all existing Windsurf rules/workflows and validation of the generated Cursor outputs.
- Documentation and enablement for Cursor and Windsurf usage patterns.

### Out of Scope

- IDE feature development beyond rules/workflows (e.g., Cursor tab completions, Windsurf memory changes).
- Refactors unrelated to dual IDE support unless they block adapter or validation work.
- Non-agent tooling, UI changes, or external integrations.

## Tasks

- [ ] Phase 0 – Discovery & Research (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-0-discovery.md`)
- [ ] Phase 1 – Unified Specification & ADR (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-1-specification.md`)
- [ ] Phase 2 – Adapter Tooling Implementation (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-2-adapters.md`)
- [ ] Phase 3 – Rules Migration & Validation (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-3-rules-migration.md`)
- [ ] Phase 4 – Workflow & Command Alignment (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-4-workflows-commands.md`)
- [ ] Phase 5 – Automation & IDE Detection (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-5-automation.md`)
- [ ] Phase 6 – Documentation & Enablement (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-6-docs.md`)
- [ ] Phase 7 – Integration, Rollout & Monitoring (`docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/phases/phase-7-rollout.md`)

Each phase file captures detailed task lists, checkpoints, owners, and status notes.

## Dependencies

### Prerequisites

- ADR documenting the dual-IDE architecture (Phase 1 deliverable).
- Access to authoritative Cursor documentation (`https://docs.cursor.com/context/rules`, `https://cursor.com/docs/agent/chat/commands`).
- Current Windsurf rules/workflows as baseline migration inputs.

### Blockers

- Cursor `.mdc` schema validation or linting tooling must be confirmed (Phase 2 task).
- CI capacity for additional validation jobs needs planning before Phase 5 execution.

### Downstream Impact

- After rollout, all rule/workflow updates must be authored through the unified pipeline.
- Onboarding materials and internal playbooks depend on Phase 6 documentation deliverables.

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Cursor lacks analogue for Windsurf `model_decision` trigger | High | Likely | Provide best-effort glob mapping, manual override commands, and document limitations |
| Adapter outputs drift between runs | High | Possible | Add golden snapshot tests and hash verification in CI |
| Workflow payloads exceed Cursor context window | Medium | Possible | Produce lightweight command variants and guardrails in Phase 4 |
| IDE detection misidentifies active environment | Medium | Possible | Implement environment probes with explicit override flags and regression tests |
| Migration confuses contributors | Medium | Possible | Execute Phase 7 communication plan with migration checklist and pairing sessions |

## Timeline

| Week | Milestone |
|------|-----------|
| 1 | Phase 0 complete (research, initiative, handoff) |
| 2 | Phase 1 specification and ADR finalized |
| 3 | Phase 2 adapter tooling merged |
| 4 | Phase 3 rule regeneration validated |
| 5 | Phase 4 workflow/command parity achieved |
| 6 | Phase 5 automation & CI integration delivered |
| 7 | Phase 6 documentation and enablement published |
| 8 | Phase 7 rollout and monitoring complete |

## Metrics

- Windsurf rules migrated: 16 → Cursor parity achieved (16)
- Windsurf workflows migrated: 21 → Cursor command parity achieved (≥21)
- Adapter/validator coverage: 0% → ≥90%
- CI runtime impact: ≤ +2 minutes per pipeline run
- Dual-IDE onboarding effort: 120 minutes → ≤45 minutes with new guide

## Related Documentation

- `/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/artifacts/research.md`
- `/CURSOR_AGENT_HANDOFF.md`
- `/docs/CONSTITUTION.md`
- `/docs/DOCUMENTATION_STRUCTURE.md`
- `https://docs.cursor.com/context/rules`
- `https://cursor.com/docs/agent/chat/commands`
- `https://docs.windsurf.com/windsurf/cascade/workflows`

## Updates

### 2025-10-22 — Initiative Created

- Published comprehensive research artifact detailing Cursor/Windsurf parity requirements.
- Authored Cursor agent handoff instructions for implementation.
- Established eight-phase execution plan with success criteria and risk mitigation strategies.
