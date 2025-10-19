---
type: machine-readable-reference
category: meta
purpose: Index and guide for .windsurf/docs machine-readable documentation
token_budget: low
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "2025-10-20"
tags: ["index", "documentation", "machine-readable"]
---

# .windsurf/docs - Machine-Readable Documentation

**Purpose:** Quick-reference documentation optimized for AI agent consumption.

**Target Audience:** AI agents (not humans - see `docs/guides/` for human-readable tutorials)

---

## Philosophy

This directory contains **machine-readable** documentation that prioritizes:

1. **Speed over comprehensiveness** - Quick lookup, not tutorials
2. **Structure over prose** - Tables, lists, code snippets
3. **Minimal tokens** - Target <2000 tokens per file
4. **Self-contained** - Each file includes necessary context
5. **Auto-generated where possible** - Reduce manual maintenance

**Contrast with `docs/guides/`:**

- `docs/guides/` = Human-readable tutorials (5K-15K tokens)
- `.windsurf/docs/` = Machine-readable quick-reference (<2K tokens)

---

## Directory Contents

### Pattern Libraries (Manual Maintenance)

| File | Purpose | Token Budget | Last Updated |
|------|---------|--------------|--------------|
| [batch-operations.md](./batch-operations.md) | Batch operation optimization strategies | Medium | 2025-10-20 |
| [common-patterns.md](./common-patterns.md) | Shared code examples and command templates | Low | 2025-10-20 |
| [context-loading-patterns.md](./context-loading-patterns.md) | Efficient context loading strategies | Medium | 2025-10-20 |
| [tool-patterns.md](./tool-patterns.md) | MCP tool usage patterns and best practices | Medium | 2025-10-20 |

### Quick References (Manual Maintenance)

| File | Purpose | Token Budget | Last Updated |
|------|---------|--------------|--------------|
| [task-system-reference.md](./task-system-reference.md) | Task format specification for update_plan | Low | 2025-10-20 |
| [workflow-routing-matrix.md](./workflow-routing-matrix.md) | Decision matrix for /work routing | Low | 2025-10-20 |

### Enforcement (Manual Maintenance)

| File | Purpose | Token Budget | Last Updated |
|------|---------|--------------|--------------|
| [directory-structure.md](./directory-structure.md) | .windsurf directory structure rules | Low | 2025-10-20 |

### Auto-Generated Indexes (Automated Maintenance)

| File | Purpose | Token Budget | Generator |
|------|---------|--------------|-----------|
| [rules-index.md](./rules-index.md) | Index of all agent rules | Low | `scripts/generate_indexes.py` |
| [workflow-index.md](./workflow-index.md) | Index of all workflows | Low | `scripts/generate_indexes.py` |
| [workflow-dependencies.md](./workflow-dependencies.md) | Workflow dependency graph | Low | `scripts/generate_indexes.py` |

---

## Maintenance

### Auto-Generated Files

**Update command:**

```bash
task docs:windsurf:update
```

**Triggers:**

- Workflow frontmatter changes
- Rule frontmatter changes
- Pre-commit hook (validation only)

**Generator:** `scripts/update_windsurf_docs.py`

### Manual Files

**Update triggers:**

- New patterns discovered
- Tool usage changes
- Routing logic updates
- Task system changes

**Maintenance responsibility:** AI agents and core team

---

## YAML Frontmatter Schema

All files in this directory use standardized frontmatter:

```yaml
---
type: machine-readable-reference
category: [pattern-library|auto-generated|quick-reference|enforcement|meta]
purpose: One-sentence description
token_budget: [low|medium]  # Target: low=<1000, medium=<2000
audience: ai-agent
auto_generated: [true|false]
maintenance: [auto|manual|hybrid]
last_updated: "YYYY-MM-DD"
tags: ["tag1", "tag2", "tag3"]
---
```

---

## Token Budget Guidelines

| Budget | Target Tokens | Use Case |
|--------|---------------|----------|
| **Low** | <1000 | Quick references, indexes, decision matrices |
| **Medium** | 1000-2000 | Pattern libraries, comprehensive references |
| **High** | >2000 | **AVOID** - Move to `docs/guides/` instead |

**Rationale:** Machine-readable docs should be fast to load and parse. Large docs belong in human-readable guides.

---

## Adding New Documentation

### Checklist

- [ ] Determine if truly machine-readable (vs tutorial)
- [ ] Choose appropriate category
- [ ] Add YAML frontmatter
- [ ] Keep token count <2000
- [ ] Use tables/lists over prose
- [ ] Include code examples
- [ ] Add to this README
- [ ] Run `task docs:lint`

### Template

```markdown
---
type: machine-readable-reference
category: [category]
purpose: [one-sentence description]
token_budget: [low|medium]
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "YYYY-MM-DD"
tags: ["tag1", "tag2"]
---

# [Title]

**Purpose:** [Expanded purpose statement]

**Target Audience:** AI agents working in this repository

---

## [Section 1]

[Content in tables, lists, code blocks]

---

## References

- [Related doc 1](./related.md)
- [Related doc 2](../workflows/workflow.md)

---

**Maintained by:** mcp-web core team
**Version:** 1.0.0
```

---

## Migration Notes

### 2025-10-20: Machine-Readable Documentation Refinement

**Changes:**

- Moved `workflow-guide.md` → `docs/guides/WORKFLOW_GUIDE.md` (tutorial content)
- Moved `rules-guide.md` → `docs/guides/RULES_GUIDE.md` (tutorial content)
- Added YAML frontmatter to all remaining files
- Created new quick-reference docs:
  - `tool-patterns.md` - MCP tool usage patterns
  - `task-system-reference.md` - Task format specification
  - `workflow-routing-matrix.md` - Routing decision matrix
- Created maintenance automation: `scripts/update_windsurf_docs.py`

**Rationale:**

- Separate machine-readable (quick-reference) from human-readable (tutorials)
- Reduce token consumption for AI agents
- Improve discoverability and maintenance
- Enable automated updates for indexes

---

## References

### Internal Documentation

- [DOCUMENTATION_STRUCTURE.md](../../docs/DOCUMENTATION_STRUCTURE.md) - Overall doc organization
- [docs/guides/WORKFLOW_GUIDE.md](../../docs/guides/WORKFLOW_GUIDE.md) - Comprehensive workflow tutorial
- [docs/guides/RULES_GUIDE.md](../../docs/guides/RULES_GUIDE.md) - Comprehensive rules tutorial

### External Best Practices

- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Biel.ai: Optimizing Docs for AI Agents](https://biel.ai/blog/optimizing-docs-for-ai-agents-complete-guide)
- [YAML Front Matter Specification](https://assemble.io/docs/YAML-front-matter.html)

---

**Maintained by:** mcp-web core team
**Version:** 1.0.0
