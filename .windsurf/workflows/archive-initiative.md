---
created: "2025-10-17"
updated: "2025-10-21"
description: Archive completed initiative or handle superseded initiatives
auto_execution_mode: 3
category: Documentation
complexity: 50
tokens: 1100
dependencies: ["scripts/validate_archival.py"]
status: active
version: "2.0-intelligent-semantic-preservation"
---

# Archive Initiative Workflow

Archive completed initiatives with validation and automation.

---

## Stage 1: Task Plan

```typescript
update_plan({
  explanation: "📦 /archive-initiative",
  plan: [
    { step: "1. Validate gates", status: "in_progress" },
    { step: "2. Execute archival", status: "pending" },
    { step: "3. Commit", status: "pending" }
  ]
})
```

---

## Stage 2: Validation (MANDATORY)

```bash
python scripts/validate_archival.py docs/initiatives/active/[name]/initiative.md
```

**Gates:** Status=Completed, Success Criteria all checked, No blockers, No dependents, Completion entry

**Exit:** 0=Pass, 1=Fail

**CRITICAL failures:** Fix, re-run (cannot bypass)
**WARNING failures:** Fix or force:

```bash
python scripts/validate_archival.py \
  docs/initiatives/active/[name]/initiative.md \
  --force --reason "[justification]"
```

---

## Stage 3: Automated Archival

```bash
task archive:initiative NAME=[folder-name]

# Preview: DRY_RUN=true
# Date: COMPLETED_ON=YYYY-MM-DD
```

**Auto:** Adds notice, moves active/→completed/, updates refs, regenerates index

**Performance:** 90x faster (15min→10sec)

**Manual fallback:** Add archived notice, move to completed/, run `task update:index`

---

## Superseded Initiatives

**Completed:** → `completed/`
**Superseded:** → superseding initiative's `artifacts/`

```bash
mkdir -p docs/initiatives/active/[superseding]/artifacts
mv docs/initiatives/active/[superseded] \
   docs/initiatives/active/[superseding]/artifacts/[name]
```

Create `artifacts/[name]/README.md` with superseding links, update cross-references.

---

## Stage 4: Commit

```bash
task docs:lint && task test:fast
git diff && git add docs/initiatives/completed/[name].md docs/initiatives/README.md
git commit -m "chore(docs): archive initiative [name]

- Completed: YYYY-MM-DD
- All criteria met
- Related: ADR-XXXX"
```

---

## References

- ADR-0013, DOCUMENTATION_STRUCTURE.md, 14_automation_scripts.md
