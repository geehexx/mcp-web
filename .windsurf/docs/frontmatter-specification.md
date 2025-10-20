---
token_budget: low
category: reference
updated: 2025-10-20
---

# Windsurf Frontmatter Specification

**Purpose:** Authoritative specification for YAML frontmatter in `.windsurf/` files based on official Windsurf documentation (October 2025).

**Source:** https://docs.windsurf.com/windsurf/cascade/workflows and https://docs.windsurf.com/windsurf/cascade/memories

---

## Official Windsurf Format

**CRITICAL:** Windsurf recognizes ONLY minimal frontmatter. Excessive custom fields cause parsing failures.

### Workflows (`.windsurf/workflows/*.md`)

**Required Fields:**

```yaml
---
description: Brief workflow summary without apostrophes or quotes
---
```

**Format Rules:**

- `description`: Single line, plain text, NO apostrophes, NO quotes in value
- Maximum: 200 characters
- Must not contain: `'`, `"`, special YAML characters
- Example: `description: Intelligent work orchestration and routing`

**Forbidden:** All other fields are custom metadata not recognized by Windsurf

### Rules (`.windsurf/rules/*.md`)

**Required Fields:**

```yaml
---
description: Brief rule summary without apostrophes or quotes
---
```

**Format Rules:**

- Same as workflows
- Activation modes are set via Windsurf UI, not frontmatter
- Globs are set via Windsurf UI, not frontmatter

---

## Deprecated Custom Fields

**These fields were in our custom schema but are NOT recognized by Windsurf:**

❌ Removed (workflows):

- `created`, `updated`, `auto_execution_mode`, `category`, `complexity`, `tokens`, `dependencies`, `status`

❌ Removed (rules):

- `created`, `updated`, `trigger`, `category`, `tokens`, `applyTo`, `priority`, `status`, `globs`

**Reason:** Official Windsurf documentation does not specify these fields. They caused parsing failures.

---

## Migration from Custom Schema

**Old Format (BROKEN):**

```yaml
---
created: "2025-10-15"
updated: "2025-10-20"
trigger: always_on
description: Core agent persona, guiding principles, operational mandate, and high-level directives. Highest-level rule applying globally.
category: core
tokens: 1200
applyTo:
  - all
priority: high
status: active
---
```

**New Format (WORKING):**

```yaml
---
description: Core agent persona guiding principles operational mandate and high-level directives
---
```

**Changes:**

1. Remove ALL custom fields
2. Keep ONLY `description`
3. Remove apostrophes from description
4. Simplify description (no complex punctuation)

---

## Common Issues

### Issue: Apostrophes in Descriptions

❌ **BROKEN:**

```yaml
description: Provide transparent progress tracking for all non-trivial work via Windsurf's Planning Mode
```

✅ **FIXED:**

```yaml
description: Provide transparent progress tracking for all non-trivial work via Windsurf Planning Mode
```

### Issue: Complex YAML Values

❌ **BROKEN:**

```yaml
description: Apply when using update_plan tool, creating task lists, orchestrating workflows, or managing multi-step work. Essential for /work, /plan, /implement orchestration.
```

✅ **FIXED:**

```yaml
description: Apply when using update_plan tool creating task lists orchestrating workflows or managing multi-step work
```

### Issue: Too Many Fields

❌ **BROKEN:** 10+ fields in frontmatter
✅ **FIXED:** ONLY `description` field

---

## Validation Rules

1. **ONLY `description` field** in frontmatter
2. **No apostrophes** in description value
3. **No quotes** around description value (unless required by YAML parser)
4. **Plain text** description (no markdown, no special chars)
5. **Maximum 200 characters** for description

---

## Schema File Status

**Old schema:** `.windsurf/schemas/frontmatter-schema.json` - DEPRECATED (too complex, not Windsurf-compatible)

**New spec:** This file - AUTHORITATIVE

---

## References

- [Windsurf Workflows Docs](https://docs.windsurf.com/windsurf/cascade/workflows)
- [Windsurf Rules Docs](https://docs.windsurf.com/windsurf/cascade/memories)
- [GitHub Issue #157](https://github.com/Exafunction/codeium/issues/157) - Rules not loading bug

---

**Version:** 1.0.0 (Reset to minimal Windsurf-compatible format)
**Last Updated:** 2025-10-20
