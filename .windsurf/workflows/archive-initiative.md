---
description: Archive completed initiative or handle superseded initiatives
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

**MANDATORY:** Run archival validation before moving initiatives.

### Step 1: Run Archival Validator

```bash
# Validate initiative against all archival gates
python scripts/validate_archival.py docs/initiatives/active/[initiative-name]/initiative.md
```

**The validator checks 5 gates:**

| Gate | Check | Severity | Bypass Allowed |
|------|-------|----------|----------------|
| **Status Completion** | Status = "Completed" or "✅ Completed" | CRITICAL | No |
| **Success Criteria** | All success criteria checkboxes checked (`[x]`) | CRITICAL | No |
| **Blockers** | All current blockers resolved | WARNING | Yes (with --force) |
| **Dependencies** | No initiatives depend on this one | CRITICAL | Waiver required |
| **Documentation** | Updates section has completion entry | WARNING | Yes (with --force) |

### Step 2: Interpret Results

**Exit codes:**

- `0` = All gates passed (or force bypass used)
- `1` = Gate failures, archival blocked

**Example output:**

```text
📋 Archival Validation: initiative.md
============================================================

✅ [CRITICAL]    Status Completion    Status: Completed
✅ [CRITICAL]    Success Criteria     5/5 success criteria met
✅ [WARNING]     Blockers            No active blockers
✅ [CRITICAL]    Dependencies        No dependents
⚠️  [WARNING]     Documentation       No completion entry found
   └─ Add completion entry with date and summary to Updates section

============================================================
Passed: 4/5
Critical failures: 0
Warning failures: 1

✅ ARCHIVAL ALLOWED
```

### Step 3: Handle Gate Failures

**If CRITICAL gates fail:**

1. Fix the issues (cannot bypass)
2. Re-run validator
3. Proceed only when all critical gates pass

**If WARNING gates fail:**

**Option A:** Fix the warnings (recommended)

**Option B:** Use force bypass with justification

```bash
python scripts/validate_archival.py \
  docs/initiatives/active/[initiative-name]/initiative.md \
  --force \
  --reason "Superseded by initiative X, blockers no longer relevant"
```

### Step 4: Generate Validation Report (Optional)

```bash
# Generate detailed markdown report
python scripts/validate_archival.py \
  docs/initiatives/active/[initiative-name]/initiative.md \
  --report archival-validation-report.md
```

**Use report for:**

- Documentation of archival decision
- Waiver justification records
- Portfolio governance audits

### Waiver Decision Framework

Based on Quality Gates (PMI/DTU ProjectLab):

| Decision | Criteria | Action |
|----------|----------|--------|
| **Go** | All gates passed | Proceed to Phase 2 (archival) |
| **Waiver** | Minor warnings only | Document reason, proceed with `--force` |
| **Waiver with Review** | Multiple warnings | Document issues, archive, review in 30 days |
| **Kill/Recycle** | Critical failures | Return to active, fix issues |

**Waiver documentation must include:**

- Which gates failed
- Business justification for bypass
- Mitigation plan (if applicable)
- Approval authority (if required)

## Phase 2: Archival Actions (Automated)

**Use automation script for all archival operations:**

```bash
# Archive initiative (90x faster than manual)
task archive:initiative NAME=[initiative-folder-name]

# Optional: Preview changes first
task archive:initiative NAME=[initiative-folder-name] DRY_RUN=true

# Optional: Specify completion date
task archive:initiative NAME=[initiative-folder-name] COMPLETED_ON=YYYY-MM-DD
```

**The script automatically:**

1. ✅ Adds archived notice to initiative document
2. ✅ Moves from `docs/initiatives/active/` to `completed/`
3. ✅ Updates ALL cross-references repository-wide
4. ✅ Regenerates initiative index

**Performance:** 90x faster (15 min → 10 sec), 100% token savings

**See:** [automation-scripts.md](../docs/automation-scripts.md)

### Manual Fallback (If Script Fails)

**Only if automation script fails:**

1. **Add archived notice:** At top of initiative document:

   ```markdown
   > **⚠️ ARCHIVED:** This initiative was completed on YYYY-MM-DD.
   > See [related ADRs / outcomes] for implemented decisions.
   ```

2. **Move document:** Relocate from `docs/initiatives/active/` to `docs/initiatives/completed/`.

3. **Update index:** Run `task update:index`.

4. **Update cross-references:** Search and replace manually or use `task move:file`.

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

**Version:** 1.3.0 (Integrated automation script for archival operations)
**Last Updated:** 2025-10-20
