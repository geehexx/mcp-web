# Phase 1: Unified Specification & ADR 📘

**Status:** Planned
**Owner:** Core Architecture Group
**Duration:** 1 week
**Priority:** P0 (Critical)

## Objective

Define the canonical unified schema for rules, workflows, and commands, and capture the decision in a formal ADR so downstream implementation has a stable contract.

## Key Tasks

- [ ] Draft unified YAML schema (required/optional fields, validation rules)
- [ ] Map Windsurf and Cursor metadata to unified schema (trigger, globs, tags, etc.)
- [ ] Document lossless vs lossy conversions and required fallbacks
- [ ] Author ADR-0024 (Dual IDE Rules & Workflow Architecture)
- [ ] Review schema with Windsurf and Cursor maintainers
- [ ] Update `docs/DOCUMENTATION_STRUCTURE.md` references if new document types introduced

## Deliverables

- `docs/adr/0024-dual-ide-rules-architecture.md` (new ADR)
- `.unified/README.md` describing schema and conventions
- Schema reference tables embedded in ADR and README

## Exit Criteria

- ADR approved and merged
- Unified schema signed off by both IDE maintainers
- Validation rules documented and handed to Phase 2
