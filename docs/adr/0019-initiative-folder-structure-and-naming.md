# ADR-0019: Initiative Folder Structure and Date-Based Naming

**Status:** Implemented
**Date:** 2025-10-18
**Deciders:** @agent
**Tags:** documentation, governance, workflows

---

## Context

The initiative documentation set had grown rapidly, and three active initiatives (`2025-q4-quality-foundation.md`, `2025-q4-performance-optimization-pipeline.md`, `2025-q4-windsurf-workflows-v2-optimization.md`) exceeded 400–800 lines each. This caused multiple pain points:

- **Navigation overhead:** Monolithic files forced contributors to scroll through lengthy documents to locate relevant phases or artifacts.
- **Inconsistent naming:** Quarterly file names (`YYYY-qN-*`) were imprecise, made chronological ordering ambiguous, and diverged from ISO 8601 standards.
- **Artifact misclassification:** Supporting research (e.g., `workflow-audit.md`) lived beside initiatives instead of within artifacts collections, increasing confusion during cross-referencing.
- **Documentation gaps:** The structure in `DOCUMENTATION_STRUCTURE.md` and `initiatives/README.md` did not fully explain when to choose flat files vs. folder-based approaches.

Research into industry best practices (Carnegie Mellon University and Boston University data management guidelines)
recommends using `YYYY-MM-DD` prefixes for deterministic sorting.
These sources also advocate for hierarchical folder structures for complex projects.
The refactor work performed on 2025-10-18 converted initiatives accordingly and established supporting rules (`.ls-lint.yml`) and documentation updates.

## Decision

We standardize initiative documentation as follows:

1. **Naming convention:** All initiatives must use ISO 8601 date-based prefixes in the form `YYYY-MM-DD-initiative-name`. Quarterly prefixes (`YYYY-qN`) are no longer permitted.
2. **Structure policy:** Initiatives exceeding 1,000 words, containing multiple phases, or requiring supporting artifacts MUST use the folder template:

```text
docs/initiatives/active/YYYY-MM-DD-initiative-name/
├── initiative.md
├── phases/
│   └── phase-*.md
└── artifacts/
    └── *.md
```

Smaller, single-phase initiatives MAY remain flat files but must still follow the date-based naming convention.
3. **Enforcement:** `.ls-lint.yml` enforces the naming rules. `initiatives/README.md`
documents decision criteria and templates. `.windsurf/workflows/archive-initiative.md`
references the new structure to prevent regressions.

## Alternatives Considered

### Alternative 1: Continue Quarterly Naming with Flat Files

- **Description:** Retain existing `YYYY-qN` naming and single-file initiatives, possibly tightening documentation guidance.
- **Pros:** No migration cost; preserves existing contributor habits.
- **Cons:** Imprecise chronology, monolithic documents, continued confusion around artifacts.
- **Reason for rejection:** Fails to address navigation, accuracy, and maintainability issues highlighted by recent sessions.

### Alternative 2: Allow Optional Formats (Quarterly or Date-Based)

- **Description:** Permit both quarterly and date formats, documenting trade-offs, leaving structure optional per initiative.
- **Pros:** Flexibility; reduced immediate change impact.
- **Cons:** Inconsistent tooling enforcement, higher cognitive load, recurring formatting debates.
- **Reason for rejection:** Inconsistency undermines automation (ls-lint) and clear contributor expectations.

## Consequences

### Positive Consequences

- All initiatives sort chronologically by exact creation date, improving discovery and historical analysis.
- Folder-based structure enables modular documentation (`initiative.md`, `phases/`, `artifacts/`), reducing file size and improving readability.
- Automated enforcement via `.ls-lint.yml` prevents format drift and reduces manual review overhead.

### Negative Consequences

- Existing initiatives required migration work (17 new files, 3 deletions), consuming ~3 hours and adding short-term risk.
- Contributors must learn and apply the folder template for larger initiatives, increasing initial onboarding effort.

### Neutral Consequences

- Flat-file initiatives remain supported for simple cases, so lightweight documentation patterns are unchanged.
- Session summaries and ADRs referencing initiatives now point to directories instead of single files; tooling already handles both.

## Implementation

Key changes shipped on 2025-10-18:

- Converted three active initiatives to folder structure (`docs/initiatives/active/2025-10-15-quality-foundation/`, `2025-10-15-performance-optimization-pipeline/`, `2025-10-17-windsurf-workflows-v2-optimization/`).
- Updated `.ls-lint.yml` to require `YYYY-MM-DD` prefixes for files and directories under `docs/initiatives/`.
- Revised `docs/DOCUMENTATION_STRUCTURE.md`, `docs/initiatives/README.md`, and `.windsurf/workflows/archive-initiative.md` with new guidance and examples.
- Validated the workspace via `npx @ls-lint/ls-lint` and `task test:fast` to confirm compliance and regression-free migration.

## References

- [Session Summary: Initiative Naming & Structure Refactor (2025-10-18)](../archive/session-summaries/2025-10-18-initiative-naming-refactor.md)
- [CMU Data Management – File Naming Conventions](https://guides.library.cmu.edu/researchdatamanagement/filenaming)
- [Boston University – Designing a Naming Convention](https://www.bu.edu/data/manage/naming-convention/)
- [Initiative Template – Folder-Based](../initiatives/template/)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-10-18 | Initial proposal & implementation | @agent |
