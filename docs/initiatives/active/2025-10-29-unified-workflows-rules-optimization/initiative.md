---
Status: "In Progress"
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
  - "/docs/initiatives/deferred/2025-10-29-pull-request-workflow-automation/initiative.md"
---
# Initiative: Unified Workflows & Rules System Optimization

## Objective

Reduce `.unified/` workflow and rule token footprint by ≥15% while enforcing a minimal,
structured frontmatter schema that keeps Windsurf and Cursor outputs correct, deterministic,
and maintainable. Encode verbose contextual data (execution notes, long-form guidance,
legacy metadata) into discrete frontmatter fields so adapters can hide sections such as
`Command Metadata` and boilerplate context without losing institutional knowledge.

---

## Success Criteria

- [ ] Total `.unified/` token count reduced by ≥15% (≈11.6k token savings target)
- [ ] All 32 unified YAML files adhere to the minimal schema (description + IDE-specific required fields)
- [ ] Windsurf workflows include `auto_execution_mode` and correct activation metadata
- [ ] Cursor rule transformations emit raw (unquoted) glob strings when present
- [ ] Metadata sections (`## Command Metadata`, `## Rule Metadata`, boilerplate context loading) removed from all rendered content
- [ ] Verbose contextual data captured via structured frontmatter fields (e.g., `ide.hidden_sections`, `ide.metadata`, token metrics, execution notes) so generated `.cursor/` & `.windsurf/` artifacts stay lean and whitespace-correct
- [ ] Adapters honor `ide.hidden_sections` and other structured metadata when generating IDE outputs (verified via golden tests)
- [ ] Updated adapters, validators, and CI checks prevent schema drift (≥90% coverage in affected modules)
- [ ] Documentation refreshed to reflect new schema and authoring guidance
- [ ] Regression suite (lint, mypy, pytest, bandit, semgrep) passes with regenerated `.cursor/` & `.windsurf/` artifacts
- [ ] Feature branch + PR workflow formalised (new unified workflow, rules updates, ADR, constitution revisions) and adopted during execution

---

## Motivation

### Problem

1. **Token bloat from redundant metadata** – Command metadata blocks repeat frontmatter details, adding 100–300 tokens per file without value.
2. **Frontmatter field sprawl** – Fields like `tags`, `related`, `type`, and Windsurf-specific mirrors (`windsurf.type`, `windsurf.dependencies`) are unused by either IDE yet inflate every file.
3. **Hidden knowledge trapped in body content** – Long-form execution guidance, attribution notes, and legacy caveats live in sections that need to disappear from generated artifacts. Without a structured frontmatter home, adapters strip the context entirely.
4. **Missing Windsurf execution fields** – `auto_execution_mode` omission risks workflow failures despite historical documentation requiring modes 1–3.
5. **Glob formatting inconsistencies** – Cursor adapters emit list-form globs instead of raw comma-separated strings, diverging from best practices derived from community guidance.
6. **Verbose boilerplate** – Repeated context loading, integration summaries, and anti-pattern sections dilute signal-to-noise across 21 workflows.

### Impact

- Increased prompt/token costs for Cascade and Cursor agents
- Higher maintenance burden with larger diffs and redundant metadata
- Risk of Windsurf workflows failing due to missing required fields
- Potential Cursor rule misapplication due to glob formatting drift
- Loss of institutional knowledge when verbose sections are dropped from IDE outputs
- Slower comprehension for contributors due to repetitive boilerplate

### Value

- Leaner `.unified/` sources that regenerate faster and fit tighter context windows
- Deterministic adapters that keep IDE artifacts aligned without manual fixes
- Stronger validation gates that block schema rot before it lands in `main`
- Clear authoring guidance with concise, high-signal workflows and rules
- Persistent institutional knowledge captured as machine-readable metadata that IDEs
  can selectively expose

---

## Scope

### In Scope

- Refactoring `.unified/**/*.yaml` frontmatter to the minimal schema
- Defining structured metadata fields (`ide.hidden_sections`, `ide.metadata`, execution logs) that preserve guidance removed from rendered markdown
- Removing redundant metadata sections and boilerplate from workflow/rule bodies
- Updating Cursor and Windsurf adapters for new schema behaviour, including hidden-section suppression
- Enhancing validation scripts, pre-commit hooks, and tests that guard the pipeline
- Refreshing contributor documentation tied to unified workflows/rules
- Capturing baseline and post-optimization token metrics
- Defining and codifying the feature-branch + PR workflow (workflows, rules, ADR, constitution update)
- Changing all `.unified/**/*.yaml` files to `.unified/**/*.md` to enable proper linting and reflect their true content (markdown + frontmatter), and updating the associated tooling (`unified_parser.py`).
- Introducing Jinja2 macros for common, repeated patterns in `.unified/**/*.md` files to improve maintainability and reduce token usage.
- Fixing the whitespace stripping bug in `scripts/adapters/unified_parser.py` to prevent unintended markdown rendering issues.

### Out of Scope

- Non-unified documentation or rule/workflow authoring unrelated to IDE parity
- IDE-specific feature enhancements beyond schema alignment
- Rewriting existing workflow logic/tasks beyond structural optimization

---

## Phases

- **[Phase 0: Kickoff & Baseline Capture](phases/phase-0-kickoff.md)** – **Completed**
- **[Phase 1: Inventory & Measurement](phases/phase-1-inventory.md)** – **Completed**
- **[Phase 2: IDE Requirements Analysis](phases/phase-2-ide-requirements.md)** – **Completed**
- **[Phase 3: Frontmatter Optimization](phases/phase-3-frontmatter.md)** – **In Progress**
- **[Phase 4: Content Optimization](phases/phase-4-content.md)** – Not Started
- **[Phase 5: Tooling & Validation Hardening](phases/phase-5-tooling.md)** – update adapters, validators, tests, and CI hooks for new schema rules.
- **[Phase 6: Documentation & Rollout](phases/phase-6-rollout.md)** – refresh guides, run regression suites, document outcomes, and complete rollout checklist.
- **[Phase 7: Monitoring & Continuous Improvement](phases/phase-7-monitoring.md)** – gather feedback, track drift, and queue follow-up enhancements after rollout.

Each phase file captures objectives, tasks, entry/exit criteria, success metrics, and dependencies.

- **Phase 2 Addition:** Define a formal JSON Schema for frontmatter in `.unified/schemas/` to make the new structure explicit and enforceable.
- **Phase 5 Addition:** Harden the validation script (`validator.py`) to use the new JSON Schema.

---

## Dependencies

### Prerequisites

- Access to existing initiatives for dual IDE compatibility and testing excellence (for alignment on validation and doc standards)
- Ability to run `scripts/build_ide_configs.py`, `scripts/validate_workflows.py`, and Taskfile commands locally
- Reference documentation for Windsurf workflows and Cursor rules (community notes and official docs) to confirm required fields

### Linked Work

- **[Cursor & Windsurf Dual Compatibility](../2025-10-22-cursor-windsurf-dual-compatibility/initiative.md)** – provides adapter architecture and transformation rules
- **[Testing Excellence & Automation Hardening](../2025-10-22-testing-excellence/initiative.md)** – establishes validation rigor and coverage targets reused here
- **[Workflow Optimization Phase 2](../2025-10-20-phase-3-performance-optimization.md)** – documents prior content trimming, informing hidden-section mappings

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
| Metadata drift between frontmatter and body | Medium | Medium | Automate schema checks that ensure `ide.hidden_sections` mirrors removed headings; add docs on encoding guidance |

---

## Rollback Strategy

If a critical issue is discovered post-merge, the following steps will be taken to revert the changes:

1. **Revert the merge commit:** A `git revert -m 1 <merge-commit-sha>` will be executed and pushed to `main`. The `-m 1` flag is required to specify the parent commit to revert to (in this case, the `main` branch). **Note:** This action can complicate re-merging the original branch later. If the branch needs to be merged again after fixes, you may need to revert the revert commit first.
2. **Communicate the rollback:** An update will be posted in the project's communication channels to inform stakeholders of the rollback and the reasons for it.
3. **Create a new initiative for the fix:** A new initiative will be created to address the critical issue, and the original initiative will be linked to it.

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
- **Metadata Utilisation** – % of workflows/rules using new structured frontmatter fields for
  hidden sections (target 100%)
- **Final Token Savings:** Measure and document the final token savings in `artifacts/token-inventory.md`.

---

## Artifacts

- [`artifacts/token-inventory.md`](artifacts/token-inventory.md) – baseline vs. post-optimization metrics
- [`artifacts/frontmatter-field-matrix.md`](artifacts/frontmatter-field-matrix.md) – required vs. optional fields per IDE
- [`artifacts/metadata-removal-playbook.md`](artifacts/metadata-removal-playbook.md) – sections slated for removal with rationale
- [`artifacts/validation-checklist.md`](artifacts/validation-checklist.md) – updated validation gates and acceptance criteria
- [`artifacts/monitoring-log.md`](artifacts/monitoring-log.md) – post-rollout observations, feedback, and follow-up actions
- [`research/external-sources.md`](research/external-sources.md) – authoritative references collected for IDE behaviour
- [`artifacts/hidden-section-map.md`](artifacts/hidden-section-map.md) – mapping between removed
  headings and their corresponding frontmatter entries (`ide.hidden_sections`, `ide.metadata`)

---

## Testing & Validation Strategy

1. **Pre-flight** – execute `python scripts/validate_workflows.py` and `python scripts/build_ide_configs.py` to capture baseline outputs.
2. **Per-phase checks** – rerun validation script after frontmatter and content updates; ensure no regressions in generated `.cursor/`/`.windsurf/` artifacts.
3. **Metadata integrity** – validate that every removed section has a matching frontmatter entry
   (`ide.hidden_sections`, `ide.metadata`) and that adapters respect the metadata in generated
   artifacts.
4. **Regression suite** – run `task lint`, `uv run mypy`, `uv run pytest -n auto`, `uv run bandit -r src/ scripts/`, and `uv run semgrep --config .semgrep.yml` before rollout.
5. **Token metrics** – recompute token counts post-optimization and document savings in artifacts.
6. **Manual IDE verification** – smoke test workflows in Windsurf and ensure Cursor rules attach as expected (tracked in Phase 6 exit criteria).
7. **Golden File Testing** - Leverage the existing `pytest-golden` framework by running `task golden:update` after all content changes are made to capture the new, correct state of the generated IDE files.

---

## Feature Branch & PR Workflow

1. **Create initiative feature branch** – start work from `main` using `git checkout -b feature/unified-workflows-rules-optimization` (or equivalent). Document branch details in `initiative.md` and Phase 0 notes.
2. **Follow checkpoint cadence** – each phase contains explicit checkpoints (see below) that require:
   - Committing scoped changes with descriptive Conventional Commit messages (`feat:`, `chore:`, `refactor:`, `test:` etc.).
   - Updating relevant artifacts (`initiative.md`, phase files, `artifacts/*.md`, research notes) to reflect progress.
   - Running `/commit` workflow to ensure validation before pushing.
3. **Push and share frequently** – push the feature branch after every checkpoint so collaborators and automation can observe progress.
4. **Leverage `/implement` and related workflows** – execute the canonical workflows (e.g., `/implement`, `/validate`, `/commit`) to keep execution consistent with project standards.
5. **Prepare PR at completion** – once Phase 6 exit criteria are met, draft the PR (see "Pull Request Expectations") and collect approvals before merging.

---

## Phase Checkpoints & Commit Cadence

| Phase | Checkpoint ID | Trigger | Required Actions |
|-------|----------------|---------|------------------|
| 0 | C0.1 | Feature branch created & baseline scripts run | Commit branch bootstrap + initial validation notes; update Phase 0 log |
| 0 | C0.2 | Baseline artifacts captured | Commit token inventory, field matrix snapshots, validation results |
| 1 | C1.1 | Inventory scripts/report drafted | Commit measurement tooling/results; update `artifacts/metadata-removal-playbook.md` |
| 1 | C1.2 | Prioritised target list agreed | Commit annotated plan; update initiative "Updates" section |
| 2 | C2.1 | Schema research complete | Commit research notes + draft schema; update `research/external-sources.md` |
| 2 | C2.2 | Schema JSON ready for review | Commit `.unified/schemas/frontmatter-minimal.json` draft; request review |
| 3 | C3.x | Batches of 5–10 files optimised | Commit per batch with clear scope; update token inventory delta per batch |
| 4 | C4.1 | Metadata removal playbook executed | Commit rewritten content; capture before/after metrics |
| 5 | C5.1 | Tooling updates + tests passing | Commit adapter/validator changes with coverage evidence |
| 6 | C6.1 | Documentation + rollout checklist complete | Commit documentation updates, final metrics, communication drafts |
| 6 | C6.2 | Final validation suite green | Tag commit or push with validation logs attached |
| 7 | C7.1 | Monitoring plan activated | Commit monitoring log, backlog tickets, initiative closure notes |

Treat checkpoints as hard gates: do not proceed until actions are committed, pushed, and reflected in initiative artifacts.

---

## Pull Request Expectations

- **Title:** `feat(unified-workflows): optimize schema + tooling` (adjust scope prefix if broader).
- **Description outline:**
  1. Summary of optimisation goals and outcomes (token savings, schema adoption, tooling hardening).
  2. Checklist of phases/checkpoints achieved with links to commits or docs.
  3. Testing & validation: include Taskfile/lint/mypy/pytest/bandit/semgrep outputs, coverage deltas, regenerated artifacts confirmation.
  4. Documentation updates: enumerate files touched (initiative, phase notes, `.unified/` README, ADR, constitution updates).
  5. Backward compatibility & rollout notes: highlight any follow-up items slated for Phase 7 monitoring.
- **Attachments:** link to updated artifacts (`token-inventory`, `monitoring-log`, ADR) and include screenshots or tables where relevant.
- **Review process:** request reviews from adapter maintainers, documentation maintainers, and initiative stakeholders; ensure at least two approvals.

---

---

## Rollout Plan

1. Complete schema refactor and validation updates (Phases 3–5).
2. Regenerate `.cursor/` and `.windsurf/` artifacts; confirm zero diffs after rerun.
3. Update documentation and announce changes via initiative updates and `PROJECT_SUMMARY.md` entry,
   highlighting new frontmatter fields and hidden-section handling guidance.
4. Merge changes once validation passes; monitor initial IDE usage feedback and capture follow-up tasks if issues arise.
5. Update the main Pull Request template to include a "Manual Verification Checklist" to formalize the manual testing process for reviewers.

---

## Updates

- **2025-10-29 — Initiative Created:** Drafted optimization plan, captured baseline problems, and
  seeded artifact/phase scaffolding. External references documented for Windsurf activation modes
  and Cursor glob formatting best practices (community guidance suggests raw comma-separated
  strings for Cursor rules).
- **2025-10-30 — Implementation Guidance Added:** Formalized feature-branch + PR workflow
  expectations (checkpoints, commit cadence, evidence logging). Flagged that execution must create
  a multi-template PR system under `.github/pull_request_template/` (e.g., `initiative.md`,
  `phase.md`, `rollout.md` variants). The dedicated `/pull-request` workflow to assemble
  descriptions from initiative artifacts has been de-scoped to a separate initiative. These assets
  are **not yet implemented**; they are queued for the feature branch owner to deliver during
  Phases 0–6 alongside ADR/constitution updates.
- **2025-10-30 — Structured Metadata Plan Approved:** Captured strategy for encoding verbose
  sections into `ide.hidden_sections`/`ide.metadata`, expanded success metrics, and aligned phases
  and artifacts with hidden-section validation requirements.
- **2025-10-30 — Phases 0, 1, and 2 Completed:**
  - Established a clean baseline and completed the project kickoff (Phase 0).
  - Inventoried the `.unified` directory, measured the token footprint, and cataloged the frontmatter fields (Phase 1).
  - Researched IDE requirements, defined a minimal frontmatter schema, and documented the findings (Phase 2).
- **2025-10-30 — Phase 3 In Progress:**
  - Renamed all `.unified/**/*.yaml` files to `.unified/**/*.md`.
  - Updated the `unified_parser.py` script to recognize the new file extension.
  - Began refactoring the `.unified` files to conform to the new schema. 10 files have been completed so far.

---

## References

- Windsurf workflow activation modes documentation (`auto_execution_mode`, activation types) – Windsurf Docs @ https://docs.windsurf.com/windsurf/cascade/workflows
- Cursor rule formatting best practices (`globs` raw strings, minimal metadata) – Community notes @ https://gist.github.com/bossjones/1fd99aea0e46d427f671f853900a0f2a
- Shipixen Cursor Rules deep-dive (frontmatter requirements, metadata structuring) – https://shipixen.com/boilerplate-documentation/shipixen-cursor-rules-explained
- SSW Frontmatter best practices (structured YAML, avoiding inline HTML) – https://www.ssw.com.au/rules/best-practices-for-frontmatter-in-markdown/
