# Reference Guides

**Purpose:** Quick reference documentation for commands, patterns, and tools.

**Location:** `docs/guides/`

---

## What Are Reference Guides?

Reference guides are **documentation-only** resources that provide quick command references, pattern examples, and tool usage instructions. They are **NOT executable workflows**.

**Key Characteristics:**

- ✅ Command reference and examples
- ✅ Quick lookup for syntax and options
- ✅ Pattern and best practice documentation
- ❌ **NOT** orchestration logic
- ❌ **NOT** invoked by workflows
- ❌ **NOT** located in `.windsurf/workflows/`

---

## Distinction: Guides vs Workflows

| Aspect | Reference Guide | Workflow |
|--------|----------------|----------|
| **Purpose** | Documentation | Execution |
| **Content** | Commands, examples | Orchestration logic |
| **Invocation** | Read by humans/AI | Called by workflows |
| **Location** | `docs/guides/` | `.windsurf/workflows/` |
| **Example** | "Here's how to run tests" | "Run tests, check results, route" |

**Example Decision:**

- ❓ "What test commands can I run?" → **Read** `docs/guides/TESTING_REFERENCE.md`
- ✅ "Run validation before commit" → **Call** `/validate` workflow

---

## Available Guides

### Testing Reference

**File:** [`TESTING_REFERENCE.md`](TESTING_REFERENCE.md)

**Content:**

- Quick test commands (`task test:fast`, `task test:coverage`)
- Test scopes (unit, integration, golden, live)
- Parallelization options (pytest-xdist)
- Coverage and debugging commands
- Test marker usage

**Use When:**

- Looking up test command syntax
- Finding coverage or debugging options
- Understanding test markers
- Checking parallelization strategies

**Related Workflow:** `/validate` (pre-commit quality gate)

---

## Adding New Guides

**When to create a reference guide:**

1. ✅ Command reference needed (git, pytest, docker, etc.)
2. ✅ Pattern catalog (design patterns, code templates)
3. ✅ Tool usage examples (debugging, profiling)
4. ✅ Configuration reference (environment variables, settings)

**When NOT to create a guide:**

1. ❌ Orchestration logic needed → Create workflow in `.windsurf/workflows/`
2. ❌ Decision-making needed → Create workflow or ADR
3. ❌ Multi-step process → Create workflow with stages

**Template:**

```markdown
---
title: [Guide Name]
description: [Brief description]
category: Reference Documentation
related_workflows: [list workflows that reference this]
---

# [Guide Name]

> **📖 Reference Documentation**
>
> This is a reference guide for [purpose].
> For [related workflow action], use the [workflow name] workflow.

**Purpose:** [One sentence description]

---

## Quick Commands

[Most common commands with examples]

---

## [Section 2]

[Detailed reference material]

---

## References

- [External docs URL]
- [Related workflow path]
```

---

## Integration with Workflows

**Workflows reference guides for detailed command syntax:**

**Example from `/validate`:**

```markdown
**For detailed test commands and options, see:**
[`docs/guides/TESTING_REFERENCE.md`](../../docs/guides/TESTING_REFERENCE.md)
```

**Guides do NOT call workflows** - They are passive documentation.

---

## Related Documentation

- [ADR-0018: Workflow Architecture V3](../adr/0018-workflow-architecture-v3.md) - Taxonomy decision
- [DOCUMENTATION_STRUCTURE.md](../DOCUMENTATION_STRUCTURE.md) - Overall doc structure
- [.windsurf/workflows/](../../.windsurf/workflows/) - Executable workflows

---

**Last Updated:** 2025-10-18
**Related ADR:** [ADR-0018](../adr/0018-workflow-architecture-v3.md)
