---
title: "Cursor & Windsurf Dual Compatibility Research"
type: "research"
status: "Active"
description: "Comprehensive research on Cursor and Windsurf architectures, rules/commands systems, and migration strategy"
tags: ["research", "cursor", "windsurf", "ide-compatibility", "architecture"]
related:
  - "/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility/initiative.md"
audience: "ai-agent"
token_budget: "high"
complexity: "complex"
created: "2025-10-22"
updated: "2025-10-22"
---

# Cursor & Windsurf Dual Compatibility Research

## Cursor IDE Rules System

### Format & Location

- **Format:** `.mdc` (Markdown Components) with YAML frontmatter
- **Location:** `.cursor/rules/` (project) or `~/.cursor/rules/` (user)
- **Frontmatter Fields:**
  - `description` (required): Brief description of rule purpose
  - `globs` (optional): File patterns for auto-attachment (e.g., `"*.py"`, `["*.py", "*.pyi"]`)
  - `alwaysApply` (optional, default: false): If true, apply to all chats

### Rule Type Inference

1. **Always:** `alwaysApply: true` - Applied to every chat
2. **Auto-Attached:** `globs: ["*.py"]` - Applied when editing matching files
3. **Manual:** No globs/alwaysApply - User must invoke manually
4. **Relevant:** Agent-decided based on description

### Key Findings

- Frontmatter is strict (only description, globs, alwaysApply parsed)
- Everything after frontmatter is passed to LLM as-is
- Globs use standard glob patterns: `*.py`, `**/*.py`, `src/**/*.ts`
- Multiple globs: `["*.py", "*.pyi"]` or `"*.py, *.pyi"`
- Nested directories supported: `.cursor/rules/python/`, `.cursor/rules/frontend/`

## Cursor IDE Commands System

### Format & Location

- **Format:** Markdown files (no special extension)
- **Location:** `.cursor/commands/` (project) or `~/.cursor/commands/` (user)
- **File Naming:** Kebab-case (my-command.md → /my-command)

### Markdown Structure

Convention-based (not enforced):

- Title (H1): Command name
- Description (paragraph): One-liner summary
- Objective (H2): Detailed task description
- Requirements (H2): Prerequisites and context
- Steps (H2): Implementation steps
- Expected Output (H2): Success criteria

### Key Characteristics

- No frontmatter required (unlike rules)
- Markdown structure is flexible (conventions, not enforced)
- Context must be embedded (no memory system)
- No multi-stage orchestration
- Agent can invoke based on relevance

## Windsurf IDE Rules System

### Format & Location

- **Format:** Markdown with YAML frontmatter
- **Location:** `.windsurf/rules/` (project) or `~/.windsurf/rules/` (global)
- **Frontmatter Fields:**
  - `trigger` (required): always_on, glob, model_decision, manual
  - `description` (required): Rule purpose (used for model_decision)
  - `globs` (optional): File patterns for glob trigger

### Trigger Modes

1. **always_on:** Applied to every Cascade action (≈ Cursor `alwaysApply: true`)
2. **glob:** Triggered when file path matches pattern (≈ Cursor `globs`)
3. **model_decision:** Cascade reads description and decides relevance (NO Cursor equivalent)
4. **manual:** User must @mention rule (≈ Cursor manual)

### Hybrid Loading

Can @mention rules in chat: `@rule-name` - Combines with automatic loading

## Windsurf IDE Workflows System

### Format & Location

- **Format:** Markdown with complex YAML frontmatter
- **Location:** `.windsurf/workflows/`
- **Invocation:** `/workflow-name` (slash command)

### Workflow Capabilities

- Multi-stage orchestration with state tracking
- Context loading via `/load-context` workflow
- Task planning via `/plan` workflow
- Validation via `/validate` workflow
- Automation via `task` commands
- Persistent memory across stages

### Current Project

21 workflows including: /work, /implement, /plan, /validate, /commit, /archive-initiative, /meta-analysis, etc.

## Trigger Mode Mapping

### Windsurf → Cursor

| Windsurf | Cursor | Type |
|----------|--------|------|
| `always_on` | `alwaysApply: true` | 1:1 |
| `glob` | `globs: [...]` | 1:1 |
| `model_decision` | `globs` (best-effort) or manual | LOSSY |
| `manual` | No globs/alwaysApply | 1:1 |

### Cursor → Windsurf

| Cursor | Windsurf | Type |
|--------|----------|------|
| `alwaysApply: true` | `always_on` | 1:1 |
| `globs: [...]` | `glob` | 1:1 |
| No globs/alwaysApply | `manual` | 1:1 |
| N/A | `model_decision` | No equivalent |

## Transformation Logic

### Rule Transformation (Windsurf → Cursor)

```python
def windsurf_to_cursor(windsurf_data: dict) -> dict:
    cursor_frontmatter = {"description": windsurf_data["description"]}

    trigger = windsurf_data.get("trigger", "manual")
    if trigger == "always_on":
        cursor_frontmatter["alwaysApply"] = True
    elif trigger == "glob":
        cursor_frontmatter["globs"] = windsurf_data.get("globs", "")
    elif trigger == "model_decision":
        if "globs" in windsurf_data:
            cursor_frontmatter["globs"] = windsurf_data["globs"]
        # else: manual (no globs/alwaysApply)
    # else: manual - no globs/alwaysApply

    return cursor_frontmatter
```

### Rule Transformation (Cursor → Windsurf)

```python
def cursor_to_windsurf(cursor_data: dict) -> dict:
    windsurf_frontmatter = {"description": cursor_data["description"]}

    if cursor_data.get("alwaysApply"):
        windsurf_frontmatter["trigger"] = "always_on"
    elif "globs" in cursor_data:
        windsurf_frontmatter["trigger"] = "glob"
        windsurf_frontmatter["globs"] = cursor_data["globs"]
    else:
        windsurf_frontmatter["trigger"] = "manual"

    return windsurf_frontmatter
```

### Glob Pattern Compatibility

Both IDEs use standard glob patterns:

- `*.py` - All Python files
- `**/*.py` - Python files in any directory
- `src/**/*.ts` - TypeScript files in `src/`
- Multiple patterns: Cursor uses array `["*.py", "*.pyi"]`, Windsurf uses comma-separated `"*.py, *.pyi"`

**Transformation:**

- Cursor array → Windsurf comma-separated: `["*.py", "*.pyi"]` → "`*.py, *.pyi"`
- Windsurf comma-separated → Cursor array: "`*.py, *.pyi"` → `["*.py", "*.pyi"]`

## Unified Format Specification

### Unified Rule File (`.unified/rules/rule-name.yaml`)

```yaml
---
title: "Rule Title"
description: "Brief description"
type: "rule"
status: "active"
windsurf:
  trigger: "always_on"
  globs: "*.py, **/*.py"
cursor:
  alwaysApply: true
  globs: ["*.py", "**/*.py"]
tags: ["tag1", "tag2"]
related:
  - "/docs/adr/0001-decision.md"
---

# Rule Content
```

### Unified Command File (`.unified/commands/command-name.yaml`)

```yaml
---
title: "Command Title"
description: "Brief description"
type: "command"
status: "active"
windsurf:
  type: "workflow"
  category: "category"
  complexity: "simple|moderate|complex"
  dependencies: []
cursor:
  pass_through: true
tags: ["tag1"]
related: []
---

# Command/Workflow Content
```

## Directory Structure (Post-Migration)

```text
.cursor/rules/
.cursor/commands/
.windsurf/rules/
.windsurf/workflows/
.unified/
  ├── rules/
  ├── commands/
  └── README.md
scripts/adapters/
  ├── unified_parser.py
  ├── cursor_adapter.py
  ├── windsurf_adapter.py
  └── validator.py
scripts/build_ide_configs.py
```

## Implementation Phases

1. **Phase 1:** Architecture & Planning
2. **Phase 2:** Adapter System
3. **Phase 3:** Rules Migration
4. **Phase 4:** Commands/Workflows
5. **Phase 5:** Automation & Scripts
6. **Phase 6:** Documentation & Testing
7. **Phase 7:** Integration & Deployment

## Critical Success Factors

1. Unified format must be a superset of both IDE capabilities.
2. Adapters must be deterministic.
3. Validation must be comprehensive.
4. Documentation must be explicit.
5. Testing must cover both IDEs.

## Risks & Mitigation

| Risk | Mitigation |
|------|-----------|
| Cursor `model_decision` equivalent missing | Use globs as best-effort, document limitation |
| Cursor commands too simple for complex workflows | Create composite commands, embed context |
| Adapter bugs cause inconsistency | Comprehensive validation, automated testing |
| Cursor agent lacks context | Comprehensive handoff document with all context |

## Next Steps for Cursor Agent

1. Review research document thoroughly.
2. Create `.unified/` directory structure.
3. Build adapter system (`scripts/adapters/`).
4. Implement build process (`scripts/build_ide_configs.py`).
5. Migrate rules and commands/workflows.
6. Integrate automation and IDE detection.
7. Complete documentation and testing.
8. Deploy and release.
