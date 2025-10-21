# Rules Update Required

**Date:** 2025-10-21
**Issue:** Incomplete implementation from windsurf-rules-revamp initiative

---

## Problem

Rules files contain outdated references to `.windsurf/docs/` directory which was removed during the windsurf-rules-revamp initiative (2025-10-21).

### Affected Files

1. **`.windsurf/rules/03_documentation.md`**
   - Section 3.10: "Machine-Readable Documentation Lifecycle"
   - References `.windsurf/docs/` for pattern libraries
   - References auto-generated files that should use different mechanism

2. **`.windsurf/rules/05_windsurf_structure.md`**
   - Section describing `.windsurf/docs/` directory
   - Lists it as "Approved Directory" (should be removed)

### Current Reality

- `.windsurf/docs/` directory does NOT exist
- Machine-readable docs are in `.windsurf/rules/` (16 rule files)
- Pattern documentation should be in initiative `artifacts/` or embedded in workflows

---

## Root Cause

The windsurf-rules-revamp initiative completed Phase 1-4 but Phase 5 (Cutover) was incomplete:

- ✅ Removed `.windsurf/docs/` directory
- ❌ Did NOT update rules that reference it
- ❌ Did NOT update documentation standards

---

## Required Actions

### 1. Update `03_documentation.md`

**Remove Section 3.10** entirely or replace with:

```markdown
## 3.10 Windsurf Artifacts

**Location:** `.windsurf/rules/` and `.windsurf/workflows/`

Machine-readable documentation is embedded in:
- **Rules:** 16 rule files with model_decision/glob triggers
- **Workflows:** 21 workflow files with executable steps
- **Hybrid Loading:** Rules can be automatically loaded OR explicitly @mentioned

**No separate documentation directory needed** - All context is in rules/workflows themselves.
```

### 2. Update `05_windsurf_structure.md`

**Remove** `.windsurf/docs/` from "Approved Directories" list.

**Update** "Directory Rules" section to only list:

1. `workflows/` - Executable workflows
2. `rules/` - Agent rules
3. `schemas/` - JSON schemas

### 3. Update Related Documentation

- `docs/DOCUMENTATION_STRUCTURE.md` - Remove any `.windsurf/docs/` references
- `docs/CONSTITUTION.md` - Verify no references
- Any ADRs mentioning machine-readable docs

---

## Workaround for Current Session

**For this initiative:** Pattern documentation not needed because:

1. Optimization techniques are self-evident in optimized workflows
2. Session summary will document techniques used
3. Future optimizations can reference this initiative's artifacts

**Pattern documentation location:** If ever needed, use `docs/guides/` or initiative `artifacts/`, NOT `.windsurf/docs/`

---

## Prevention

**Pre-commit validation** should flag:

- References to non-existent directories
- Outdated documentation cross-references
- Inconsistencies between rules and reality

**Suggestion:** Add link checker that validates all internal references in rules/workflows.

---

**Priority:** Medium (does not block current work, but creates confusion)
**Owner:** Future session or manual review
**Estimated Effort:** 30-60 minutes
