---
description: Archive completed initiative
auto_execution_mode: 3
---

# Archive Initiative Workflow

Use this workflow to properly archive a completed initiative.

## Phase 1: Verification

1. **Confirm completion:** Ensure all success criteria are met and living documentation is updated.

2. **Inventory references:** Search repository for initiative ID/name to identify:
   - Links in documentation
   - References in ADRs
   - Mentions in guides
   - Task references

## Phase 2: Archival Actions

1. **Add archived notice:** At top of initiative document:

   ```markdown
   > **⚠️ ARCHIVED:** This initiative was completed on YYYY-MM-DD.
   > See [related ADRs / outcomes] for implemented decisions.
   ```

2. **Move document:** Relocate from `docs/initiatives/active/` to `docs/initiatives/completed/`.

3. **Update index:** Update `docs/initiatives/README.md` or tracking documents.

4. **Update cross-references:** Adjust any documentation pointing to the initiative's old location.

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
mv docs/initiatives/active/2024-q4-quality-foundation.md \
   docs/initiatives/completed/

# Update references
# ... (sed/ag commands or manual edits)

# Commit
git commit -m "chore(docs): archive Q4 2024 quality foundation initiative"
```
