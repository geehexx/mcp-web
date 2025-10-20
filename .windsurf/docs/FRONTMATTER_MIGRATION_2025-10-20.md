---
category: migration
urgency: high
updated: 2025-10-20
---

# Frontmatter Migration Notice (2025-10-20)

**BREAKING CHANGE:** All workflow and rule frontmatter has been migrated to minimal Windsurf-compatible format.

---

## What Changed

### Before (Complex Format - BROKEN)

```yaml
---
created: "2025-10-15"
updated: "2025-10-20"
trigger: always_on
description: Core agent persona, guiding principles...
category: core
tokens: 1200
applyTo:
  - all
priority: high
status: active
---
```

### After (Minimal Format - WORKING)

```yaml
---
description: Core agent persona guiding principles operational mandate and high-level directives
---
```

---

## Why This Change

**Root Cause:** Our custom frontmatter schema was NOT recognized by Windsurf. The extensive metadata caused:

- Rules not loading automatically
- Workflows not being discovered
- YAML parsing failures (especially with apostrophes)
- GitHub Issue: https://github.com/Exafunction/codeium/issues/157

**Official Windsurf Format:** According to docs.windsurf.com (Oct 2025), Windsurf expects:

- **ONLY** `description` field in frontmatter
- No apostrophes or quotes in description
- Maximum 200 characters
- All other fields are ignored

---

## Impact

✅ **Fixed:**

- All 27 files (8 rules + 19 workflows) migrated
- Validation script updated
- Documentation updated
- All files pass `python scripts/validate_frontmatter.py`

❌ **Removed Fields:**

- Workflows: `created`, `updated`, `auto_execution_mode`, `category`, `complexity`, `tokens`, `dependencies`, `status`
- Rules: `created`, `updated`, `trigger`, `category`, `tokens`, `applyTo`, `priority`, `status`, `globs`

---

## Migration Procedure

1. **Automated:** Ran `python scripts/fix_frontmatter.py`
2. **Validated:** All files pass validation
3. **Schema:** Deprecated `.windsurf/schemas/frontmatter-schema.json`
4. **Specification:** Created `.windsurf/docs/frontmatter-specification.md`

---

## For Future

**When creating new workflows/rules:**

```yaml
---
description: Brief summary without apostrophes
---
```

**Validation:**

```bash
python scripts/validate_frontmatter.py
```

**Reference:**

- `.windsurf/docs/frontmatter-specification.md` - Full specification
- `.windsurf/rules/03_documentation_lifecycle.md` - Updated documentation standards

---

## Rollback (If Needed)

Backup of old schema: `.windsurf/schemas/frontmatter-schema.json.backup`

**NOT RECOMMENDED:** The old format did not work with Windsurf.

---

**Migration Date:** 2025-10-20
**Files Affected:** 27 (all workflows and rules)
**Status:** ✅ Complete and validated
