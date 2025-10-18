# Manual Fixes Plan

**Generated:** 2025-10-18
**Total Violations:** 37 manual fixes required

## Summary by Type

| Type | Count | Description | Priority |
|------|-------|-------------|----------|
| MD040 | 21 | Code fence missing language | High |
| MD036 | 8 | Emphasis used as heading | Medium |
| MD025 | 4 | Multiple H1 headings | Medium |
| MD059 | 3 | Non-descriptive link text | Low |
| MD024 | 1 | Duplicate heading | Low |

---

## MD040: Code Fence Language Specifiers (21 violations)

### Workflow Files (.windsurf/workflows/)

**bump-version.md** (4 violations):

- Line 285: Add `markdown` (example section)
- Line 309: Add `markdown` (example section)
- Line 331: Add `markdown` (example section)
- Line 351: Add `markdown` (example section)

**research.md** (6 violations):

- Line 88: Add `markdown` (output example)
- Line 95: Add `markdown` (output example)
- Line 102: Add `markdown` (output example)
- Line 109: Add `markdown` (output example)
- Line 116: Add `markdown` (output example)
- Line 292: Add `markdown` (output example)

**plan.md** (1 violation):

- Line 199: Add `markdown` (example section)

**detect-context.md** (0 MD040, but 5 MD036)

### Documentation Files (docs/)

**adr/0018-workflow-architecture-v3.md** (1 violation):

- Line 197: Add `text` (log output)

**initiatives/active/2025-10-15-performance-optimization-pipeline/phases/phase-1-foundation-quick-wins.md** (1 violation):

- Line 67: Add `text` (placeholder)

**initiatives/active/2025-10-18-markdown-quality-comprehensive-fix/artifacts/research-summary.md** (3 violations):

- Line 214: Add `yaml` (pre-commit config)
- Line 259: Add `python` (test code)
- Line 467: Add `text` (directory tree)

**initiatives/active/2025-10-18-workflow-architecture/artifacts/workflow-audit.md** (3 violations):

- Line 172: Add `text` (output)
- Line 481: Add `text` (output)
- Line 496: Add `text` (output)

**initiatives/active/PROPOSAL-folder-based-structure.md** (6 violations):

- Line 20: Add `text` (directory tree)
- Line 88: Add `text` (directory tree)
- Line 115: Add `text` (comparison)
- Line 122: Add `bash` (command)
- Line 200: Add `text` (directory tree)
- Line 215: Add `bash` (command)

---

## MD036: Emphasis Used As Heading (8 violations)

**All in .windsurf/workflows/detect-context.md:**

- Line 68: Change `**Priority 1: Session Summary Si...**` to `### Priority 1: Session Summary Signals`
- Line 80: Change `**Priority 2: Active Initiative ...**` to `### Priority 2: Active Initiative Signals`
- Line 95: Change `**Priority 3: Git Signals**` to `### Priority 3: Git Signals`
- Line 108: Change `**Priority 4: Test Signals**` to `### Priority 4: Test Signals`
- Line 119: Change `**Priority 5: Documentation TODO...**` to `### Priority 5: Documentation Signals`

**Initiative files:**

- docs/initiatives/active/2025-10-15-performance-optimization-pipeline/initiative.md:106
- docs/initiatives/active/2025-10-15-quality-foundation/initiative.md:172
- docs/initiatives/active/2025-10-17-windsurf-workflows-v2-optimization/initiative.md:148

---

## MD025: Multiple H1 Headings (4 violations)

**All in artifacts/research-summary.md** (lines 439, 446, 452, 459):

- These are inside a code fence showing markdown examples
- Change from `# Command output` to `## Command output` (make H2)
- Or change fence to have correct language and escape the hashes

---

## MD059: Non-Descriptive Link Text (3 violations)

**All in .windsurf/workflows/bump-version.md** (lines 446, 452, 458):

- Change `[link]` to descriptive text like `[bump-my-version]`, `[commitizen]`, `[semantic-release]`

---

## MD024: Duplicate Heading (1 violation)

**initiatives/active/2025-10-18-workflow-architecture/initiative.md:354:**

- Heading "Updates" appears multiple times
- Make unique: "Phase 1 Updates", "Phase 2 Updates", etc.

---

## Fix Strategy

### Batch 1: Code Fence Languages (21 fixes)

Use multi_edit to fix all code fences in each file

### Batch 2: Emphasis to Headings (8 fixes)

Fix detect-context.md and initiative files

### Batch 3: Multiple H1 (4 fixes)

Fix research-summary.md code fence examples

### Batch 4: Link Text (3 fixes)

Fix bump-version.md link descriptions

### Batch 5: Duplicate Heading (1 fix)

Fix workflow-architecture initiative

---

## Estimated Time

- Batch 1: 30 minutes
- Batch 2: 15 minutes
- Batch 3: 10 minutes
- Batch 4: 5 minutes
- Batch 5: 5 minutes
- **Total: ~65 minutes**
