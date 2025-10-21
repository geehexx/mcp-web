---
created: "2025-10-17"
updated: "2025-10-21"
description: Archive completed initiative or handle superseded initiatives
auto_execution_mode: 3
category: Documentation
complexity: 50
tokens: 1500
dependencies: ["scripts/validate_archival.py"]
status: active
version: 1.3.0
---

# Archive Initiative Workflow

**Purpose:** Properly archive completed initiatives with validation and automation.

---

## Stage 1: Create Task Plan

```typescript
update_plan({
  explanation: "📦 Starting /archive-initiative workflow",
  plan: [
    { step: "1. /archive-initiative - Run validation gates", status: "in_progress" },
    { step: "2. /archive-initiative - Execute automated archival", status: "pending" },
    { step: "3. /archive-initiative - Validate and commit", status: "pending" }
  ]
})
```

---

## Stage 2: Validation Gates (MANDATORY)

### Run Archival Validator

```bash
python scripts/validate_archival.py docs/initiatives/active/[name]/initiative.md
```

### Validation Gates

| Gate | Check | Severity | Bypass |
|------|-------|----------|--------|
| **Status** | "Completed" or "✅" | CRITICAL | No |
| **Success Criteria** | All `[x]` checked | CRITICAL | No |
| **Blockers** | All resolved | WARNING | Yes (--force) |
| **Dependencies** | No dependents | CRITICAL | Waiver |
| **Documentation** | Completion entry exists | WARNING | Yes (--force) |

### Interpret Results

**Exit codes:**
- `0` = Pass (or forced)
- `1` = Fail (blocked)

**Example output:**

```text
✅ [CRITICAL]  Status: Completed
✅ [CRITICAL]  Success Criteria: 5/5 met
✅ [WARNING]   Blockers: None active
✅ [CRITICAL]  Dependencies: No dependents
⚠️  [WARNING]   Documentation: No completion entry
   └─ Add completion entry to Updates

Passed: 4/5, Critical: 0, Warnings: 1
✅ ARCHIVAL ALLOWED
```

### Handle Failures

**CRITICAL failures:** Fix issues, re-run (cannot bypass)

**WARNING failures:**

**Option A:** Fix warnings (recommended)

**Option B:** Force bypass with justification:

```bash
python scripts/validate_archival.py \
  docs/initiatives/active/[name]/initiative.md \
  --force \
  --reason "Superseded by initiative X"
```

### Waiver Framework

| Decision | Criteria | Action |
|----------|----------|--------|
| **Go** | All passed | Proceed to archival |
| **Waiver** | Minor warnings | Document, proceed with --force |
| **Waiver+Review** | Multiple warnings | Document, archive, review in 30d |
| **Kill/Recycle** | Critical fails | Fix, return to active |

---

## Stage 3: Automated Archival

**Use automation script (90x faster):**

```bash
# Archive initiative
task archive:initiative NAME=[folder-name]

# Preview first (optional)
task archive:initiative NAME=[folder-name] DRY_RUN=true

# Specify completion date (optional)
task archive:initiative NAME=[folder-name] COMPLETED_ON=YYYY-MM-DD
```

**Script automatically:**
1. ✅ Adds archived notice
2. ✅ Moves active/ → completed/
3. ✅ Updates ALL cross-references
4. ✅ Regenerates initiative index

**Performance:** 90x faster (15min → 10sec), 100% token savings

**See:** [14_automation_scripts.md](../rules/14_automation_scripts.md)

### Manual Fallback (If Script Fails)

**Only if automation fails:**

1. **Add notice:** At top of initiative.md:

   ```markdown
   > **⚠️ ARCHIVED:** Completed on YYYY-MM-DD.
   > See [related ADRs / outcomes].
   ```

2. **Move:** `active/` → `completed/`

3. **Update index:** `task update:index`

4. **Update refs:** `task move:file` or manual search/replace

---

## Special Case: Superseded Initiatives

**When:** Initiative not completed but replaced/split.

### Difference

- **Completed:** Finished → move to `completed/`
- **Superseded:** Replaced → move to superseding initiative as artifact

### Process

1. **Identify superseding initiative(s):**
   - Split: Choose primary/NOW initiative
   - Replaced: Use replacement

2. **Move as artifact:**

   ```bash
   mkdir -p docs/initiatives/active/[superseding]/artifacts
   mv docs/initiatives/active/[superseded] \
      docs/initiatives/active/[superseding]/artifacts/[name]
   ```

3. **Create README:** `artifacts/[name]/README.md`:

   ```markdown
   # Superseded Initiative
   
   **Status:** Superseded by pragmatic split
   **Date:** YYYY-MM-DD
   
   ## What Replaced It
   - Initiative A (link) - NOW work
   - Initiative B (link) - Future work
   
   ## What Was Preserved
   Original research in artifacts/...
   ```

4. **Update superseding initiative:**

   ```markdown
   ### YYYY-MM-DD (Supersedes Previous Plan)
   
   This supersedes [original-name].
   Original research in artifacts/[name]/.
   ```

5. **Update cross-references:** Point to new initiatives

---

## Stage 4: Validation

```bash
# Lint docs
task docs:lint

# Check links
# Verify no broken links

# Run tests
task test:fast
```

---

## Stage 5: Commit

```bash
# Review
git diff

# Stage
git add docs/initiatives/completed/[name].md
git add docs/initiatives/README.md
git add [other-files]

# Review staged
git diff --staged

# Commit
git commit -m "chore(docs): archive initiative [name]

- Completed: YYYY-MM-DD
- All success criteria met
- Related ADRs: ADR-XXXX"
```

---

## Example

```bash
# Initiative: Q4 2024 Quality Foundation
# ADRs: 0001-0010, Tests: 37+, All criteria met

# Validate
python scripts/validate_archival.py docs/initiatives/active/quality-foundation/initiative.md

# Archive (automated)
task archive:initiative NAME=quality-foundation

# Commit
git commit -m "chore(docs): archive Q4 2024 quality foundation"
```

---

## References

- [ADR-0013: Initiative Standards](../../docs/adr/0013-initiative-documentation-standards.md)
- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md)
- [14_automation_scripts.md](../rules/14_automation_scripts.md)

---

**Version:** 1.3.0
**Last Updated:** 2025-10-21
