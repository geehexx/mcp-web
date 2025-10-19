---
created: "2025-10-17"
updated: "2025-10-19"
description: Archive completed initiative or handle superseded initiatives
auto_execution_mode: 3
category: Documentation
complexity: 45
tokens: 550
dependencies: []
status: active
version: 1.1.0
---

# Archive Initiative Workflow

Use this workflow to properly archive a completed initiative.

---

## Stage 0: Create Task Plan

🔄 **Entering /archive-initiative workflow**

**Create task plan:**

```typescript
update_plan({
  explanation: "📦 Starting /archive-initiative workflow",
  plan: [
    { step: "1. /archive-initiative - Verify completion", status: "in_progress" },
    { step: "2. /archive-initiative - Add archived notice and move file", status: "pending" },
    { step: "3. /archive-initiative - Update cross-references", status: "pending" },
    { step: "4. /archive-initiative - Validate and commit", status: "pending" }
  ]
})
```

---

## Phase 1: Verification

1. **Confirm completion:** Ensure all success criteria are met and living documentation is updated.

2. **Inventory references:** Search repository for initiative ID/name to identify:
   - Links in documentation
   - References in ADRs
   - Mentions in guides
   - Task references

## Phase 1.5: Automated Validation Gates

**Run validation before archival:**

```bash
task validate:initiatives
task validate:dependencies
```

**Archival quality gates (must pass before archival):**

| Gate | Check | Severity | Bypass |
|------|-------|----------|--------|
| **Success Criteria** | All checkboxes checked (`[x]`) | CRITICAL | No |
| **Dependencies** | No initiatives depend on this one | CRITICAL | Waiver required |
| **Blockers** | All blockers resolved | WARNING | Yes |
| **Documentation** | Updates section has completion entry | WARNING | Yes |
| **Status** | Status = "Completed" or "✅ Completed" | CRITICAL | No |

**Automated gate check:**

```bash
# Validate initiative before archival
python scripts/validate_initiatives.py --file docs/initiatives/active/[initiative-name]/initiative.md
```

**Dependency check:**

```bash
# Ensure no other initiatives depend on this one
python scripts/dependency_registry.py --validate
```

**If gates fail:**

- **CRITICAL failures:** Must fix before archival
- **WARNING failures:** Document waiver reason in commit message
- **Bypass:** Use `--force-archive` flag with justification

**Waiver decisions (from Quality Gates, PMI/DTU):**

- **Go:** All gates passed, proceed to archival
- **Waiver:** Minor issues, document and proceed
- **Waiver with re-view:** Document issues, review in 30 days
- **Kill/Recycle:** Gate failures indicate incomplete work, return to active

## Phase 2: Archival Actions

1. **Add archived notice:** At top of initiative document:

   ```markdown
   > **⚠️ ARCHIVED:** This initiative was completed on YYYY-MM-DD.
   > See [related ADRs / outcomes] for implemented decisions.
   ```

2. **Move document:** Relocate from `docs/initiatives/active/` to `docs/initiatives/completed/`.

3. **Update index:** Update `docs/initiatives/README.md` or tracking documents.

4. **Update cross-references:** Adjust any documentation pointing to the initiative's old location.

## Special Case: Superseded Initiatives

**When to Use:** Initiative was not completed but replaced/split into other initiatives.

### Difference from Archival

- **Completed:** Work finished, move to `completed/`, add archived notice
- **Superseded:** Work replaced, move as artifact to superseding initiative

### Process for Superseded Initiatives

1. **Identify superseding initiative(s):**
   - If split into multiple: Choose the primary/NOW initiative
   - If replaced by one: Use that initiative

2. **Move as artifact:**

   ```bash
   # Create artifacts directory if needed
   mkdir -p docs/initiatives/active/[superseding-initiative]/artifacts

   # Move superseded initiative
   mv docs/initiatives/active/[superseded-name] \
      docs/initiatives/active/[superseding-initiative]/artifacts/[descriptive-name]
   ```

3. **Create README explaining supersession:**
   Create `artifacts/[descriptive-name]/README.md` with:
   - What happened (why superseded)
   - What replaced it (links to new initiatives)
   - What was preserved (research, analysis)
   - Lessons learned

4. **Update superseding initiative:**
   Add reference in initiative.md Updates section:

   ```markdown
   ### YYYY-MM-DD (Supersedes Previous Plan)

   This initiative supersedes [original-name].
   Original research preserved in artifacts/[name]/.
   ```

5. **Update cross-references:**
   - Update any external links to point to new initiative(s)
   - Add forwarding notice if needed

### Example

```markdown
# Superseded Initiative (in artifacts/original-plan/README.md)

**Status:** Superseded by pragmatic split
**Date:** 2025-10-19

## What Replaced It
- [Initiative A](../../initiative.md) - NOW work
- [Initiative B](../../../other-initiative/initiative.md) - Future work

## What Was Preserved
Original research in artifacts/ directory...
```

---

## Phase 3: Validation

1. **Lint documentation:** Run `task docs:lint` to ensure formatting remains valid.

2. **Check links:** Verify no broken links remain from the move.

3. **Run tests:** Execute `task test:fast` to ensure no test dependencies on initiative location.

## Phase 4: Version Control

1. **Review changes:** Review all modifications:

   ```bash
   git diff
   ```

2. **Stage archival:** Stage the moved/updated files:

   ```bash
   git add docs/initiatives/completed/[initiative-name].md
   git add docs/initiatives/README.md  # If updated
   git add [other-updated-files]
   ```

3. **Review staged:** Confirm accuracy of staged changes:

   ```bash
   git diff --staged
   ```

4. **Commit:** Use descriptive message:

   ```markdown
   chore(docs): archive initiative [name]

   - Completed on YYYY-MM-DD
   - All success criteria met
   - Related ADRs: ADR-XXXX, ADR-YYYY
   ```

5. **Follow-up:** If new work spawned from TODOs, create new initiatives.

## Example

```bash
# Initiative completed: Q4 2024 Quality Foundation
# ADRs created: 0001-0010
# Tests added: 37+ scenarios
# Status: All success criteria met

# Move to completed
mv docs/initiatives/active/2025-10-15-quality-foundation/ \
   docs/initiatives/completed/

# Update references
# ... (sed/ag commands or manual edits)

# Commit
git commit -m "chore(docs): archive Q4 2024 quality foundation initiative"
```

---

## References

- [ADR-0013: Initiative Documentation Standards](../../docs/adr/0013-initiative-documentation-standards.md)
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md)

---

**Version:** 1.1 (Added superseded initiative handling)
**Last Updated:** 2025-10-19
