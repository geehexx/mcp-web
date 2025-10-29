---
Status: "Proposed"
Created: "2025-10-29"
Updated: "2025-10-30"
Owner: "Core Team"
Priority: "High"
Estimated Duration: "8-12 hours"
Target Completion: "2025-11-01"
Tags:
  - "workflows"
  - "rules"
  - "token-optimization"
  - "cursor"
  - "windsurf"
Related:
  - "/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/initiative.md"
  - "/docs/initiatives/active/2025-10-22-testing-excellence/initiative.md"
  - "/.unified/README.md"
  - "/scripts/adapters/"
  - "https://docs.windsurf.com/windsurf/cascade/workflows"
  - "https://gist.github.com/bossjones/1fd99aea0e46d427f671f853900a0f2a"
---
# Initiative: Unified Workflows & Rules System Optimization

## Objective

Reduce `.unified/` workflow and rule token footprint by ≥15% while enforcing a minimal frontmatter schema that keeps Windsurf and Cursor outputs correct, deterministic, and maintainable.

---

## Success Criteria

- [ ] Total `.unified/` token count reduced by ≥15% (≈11.6k token savings target)
- [ ] All 32 unified YAML files adhere to the minimal schema (description + IDE-specific required fields)
- [ ] Windsurf workflows include `auto_execution_mode` and correct activation metadata
- [ ] Cursor rule transformations emit raw (unquoted) glob strings when present
- [ ] Metadata sections (`## Command Metadata`, `## Rule Metadata`, boilerplate context loading) removed from all rendered content
- [ ] Updated adapters, validators, and CI checks prevent schema drift (≥90% coverage in affected modules)
- [ ] Documentation refreshed to reflect new schema and authoring guidance
- [ ] Regression suite (lint, mypy, pytest, bandit, semgrep) passes with regenerated `.cursor/` & `.windsurf/` artifacts

---

## Motivation

### Problem

1. **Token bloat from redundant metadata** – Command metadata blocks repeat frontmatter details, adding 100–300 tokens per file without value.
2. **Frontmatter field sprawl** – Fields like `tags`, `related`, `type`, and Windsurf-specific mirrors (`windsurf.type`, `windsurf.dependencies`) are unused by either IDE yet inflate every file.
3. **Missing Windsurf execution fields** – `auto_execution_mode` omission risks workflow failures despite historical documentation requiring modes 1–3.
4. **Glob formatting inconsistencies** – Cursor adapters emit list-form globs instead of raw comma-separated strings, diverging from best practices derived from community guidance.
5. **Verbose boilerplate** – Repeated context loading, integration summaries, and anti-pattern sections dilute signal-to-noise across 21 workflows.

### Impact

- Increased prompt/token costs for Cascade and Cursor agents
- Higher maintenance burden with larger diffs and redundant metadata
- Risk of Windsurf workflows failing due to missing required fields
- Potential Cursor rule misapplication due to glob formatting drift
- Slower comprehension for contributors due to repetitive boilerplate

### Value

- Leaner `.unified/` sources that regenerate faster and fit tighter context windows
- Deterministic adapters that keep IDE artifacts aligned without manual fixes
- Stronger validation gates that block schema rot before it lands in `main`
- Clear authoring guidance with concise, high-signal workflows and rules

---

## Scope

### In Scope

- Refactoring `.unified/**/*.yaml` frontmatter to the minimal schema
- Removing redundant metadata sections and boilerplate from workflow/rule bodies
- Updating Cursor and Windsurf adapters for new schema behaviour
- Enhancing validation scripts, pre-commit hooks, and tests that guard the pipeline
- Refreshing contributor documentation tied to unified workflows/rules
- Capturing baseline and post-optimization token metrics

### Out of Scope

- Non-unified documentation or rule/workflow authoring unrelated to IDE parity
- IDE-specific feature enhancements beyond schema alignment
- Rewriting existing workflow logic/tasks beyond structural optimization

---

## Phases

- **[Phase 0: Kickoff & Baseline Capture](phases/phase-0-kickoff.md)** – establish backups, gather token baselines, and validate current build outputs.
- **[Phase 1: Inventory & Measurement](phases/phase-1-inventory.md)** – quantify token costs, catalogue metadata sections, and prioritize high-bloat files.
- **[Phase 2: IDE Requirements Analysis](phases/phase-2-ide-requirements.md)** – confirm minimal field requirements via docs and adapters; finalize schema JSON.
- **[Phase 3: Frontmatter Optimization](phases/phase-3-frontmatter.md)** – roll out minimal schema across `.unified/`, add missing Windsurf metadata, normalise globs.
- **[Phase 4: Content Optimization](phases/phase-4-content.md)** – excise redundant sections, consolidate context guidance, ensure succinct narratives.
- **[Phase 5: Tooling & Validation Hardening](phases/phase-5-tooling.md)** – update adapters, validators, tests, and CI hooks for new schema rules.
- **[Phase 6: Documentation & Rollout](phases/phase-6-rollout.md)** – refresh guides, run regression suites, document outcomes, and complete rollout checklist.
- **[Phase 7: Monitoring & Continuous Improvement](phases/phase-7-monitoring.md)** – gather feedback, track drift, and queue follow-up enhancements after rollout.

Each phase file captures objectives, tasks, entry/exit criteria, success metrics, and dependencies.

---

## Dependencies

### Prerequisites

- Access to existing initiatives for dual IDE compatibility and testing excellence (for alignment on validation and doc standards)
- Ability to run `scripts/build_ide_configs.py`, `scripts/validate_workflows.py`, and Taskfile commands locally
- Reference documentation for Windsurf workflows and Cursor rules (community notes and official docs) to confirm required fields

### Linked Work

- **[Cursor & Windsurf Dual Compatibility](../2025-10-22-cursor-windsurf-dual-compatibility/initiative.md)** – provides adapter architecture and transformation rules
- **[Testing Excellence & Automation Hardening](../2025-10-22-testing-excellence/initiative.md)** – establishes validation rigor and coverage targets reused here

### Blockers

- Inability to reach Cursor documentation (current restrictions) must be resolved or mirrored via offline references before Phase 2 exit
- CI capacity planning for additional validation jobs must be confirmed during Phase 5

---

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Cursor docs inaccessible due to redirect policies | Medium | High | Capture authoritative guidance via trusted mirrors/community notes; store offline references in repo research artifacts |
| Schema refactor introduces adapter regressions | High | Medium | Add golden tests, expand coverage ≥90%, and run `build_ide_configs.py` in CI with zero-diff enforcement |
| Token savings <15% | Medium | Low | Prioritise highest bloat files first, iterate with measurement checkpoints per phase |
| Windsurf workflow execution fails without `auto_execution_mode` | High | Low | Validate with Windsurf docs and add schema enforcement that blocks missing fields before merge |
| Contributor confusion during rollout | Medium | Medium | Publish migration guide, update `.unified/README.md`, and announce changes via initiative updates |

---

## Timeline & Effort

| Window | Focus | Effort |
|--------|-------|--------|
| Day 0 (2–3h) | Phase 0 – Kickoff & Baseline | 2–3h |
| Day 0 (2h) | Phase 1 – Inventory & Measurement | 2h |
| Day 0–1 (1h) | Phase 2 – IDE Requirements Analysis | 1h |
| Day 1 (2h) | Phase 3 – Frontmatter Optimization | 2h |
| Day 1 (1.5h) | Phase 4 – Content Optimization | 1.5h |
| Day 1 (1.5h) | Phase 5 – Tooling & Validation Hardening | 1.5h |
| Day 1 (1h) | Phase 6 – Documentation & Rollout | 1h |

_Total planned effort: 11–12 hours across ~1.5 working days._

---

## Metrics

- **Token Baseline vs. Post-Optimization** – tracked via `artifacts/token-inventory.md`
- **Schema Compliance** – % of files passing minimal schema validation (target 100%)
- **Adapter Test Coverage** – `scripts/adapters/*` statement coverage (target ≥90%)
- **Validation Runtime** – Additional seconds added to CI pipeline (< +120s target)
- **Documentation Accuracy** – `.unified/README.md` and guides updated, verified during Phase 6 exit

---

## Artifacts

- [`artifacts/token-inventory.md`](artifacts/token-inventory.md) – baseline vs. post-optimization metrics
- [`artifacts/frontmatter-field-matrix.md`](artifacts/frontmatter-field-matrix.md) – required vs. optional fields per IDE
- [`artifacts/metadata-removal-playbook.md`](artifacts/metadata-removal-playbook.md) – sections slated for removal with rationale
- [`artifacts/validation-checklist.md`](artifacts/validation-checklist.md) – updated validation gates and acceptance criteria
- [`artifacts/monitoring-log.md`](artifacts/monitoring-log.md) – post-rollout observations, feedback, and follow-up actions
- [`research/external-sources.md`](research/external-sources.md) – authoritative references collected for IDE behaviour

---

## Testing & Validation Strategy

1. **Pre-flight** – execute `python scripts/validate_workflows.py` and `python scripts/build_ide_configs.py` to capture baseline outputs.
2. **Per-phase checks** – rerun validation script after frontmatter and content updates; ensure no regressions in generated `.cursor/`/`.windsurf/` artifacts.
3. **Regression suite** – run `task lint`, `uv run mypy`, `uv run pytest -n auto`, `uv run bandit -r src/ scripts/`, and `uv run semgrep --config .semgrep.yml` before rollout.
4. **Token metrics** – recompute token counts post-optimization and document savings in artifacts.
5. **Manual IDE verification** – smoke test workflows in Windsurf and ensure Cursor rules attach as expected (tracked in Phase 6 exit criteria).

---

## Rollout Plan

1. Complete schema refactor and validation updates (Phases 3–5).
2. Regenerate `.cursor/` and `.windsurf/` artifacts; confirm zero diffs after rerun.
3. Update documentation and announce changes via initiative updates and `PROJECT_SUMMARY.md` entry.
4. Merge changes once validation passes; monitor initial IDE usage feedback and capture follow-up tasks if issues arise.

---

## Updates

- **2025-10-29 – Initiative Created:** Drafted optimization plan, captured baseline problems, and
  seeded artifact/phase scaffolding. External references documented for Windsurf activation modes
  and Cursor glob formatting best practices (community guidance suggests raw comma-separated
  strings for Cursor rules).

---

## References

- Windsurf workflow activation modes documentation (`auto_execution_mode`, activation types) – Windsurf Docs @ https://docs.windsurf.com/windsurf/cascade/workflows
- Cursor rule formatting best practices (`globs` raw strings, minimal metadata) – Community notes @ https://gist.github.com/bossjones/1fd99aea0e46d427f671f853900a0f2a
