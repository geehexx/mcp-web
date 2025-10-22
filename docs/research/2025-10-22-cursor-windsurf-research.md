---
title: "Cursor & Windsurf Dual Compatibility Research"
type: "research"
status: "active"
description: "Comprehensive research on Cursor and Windsurf architectures, rules/commands systems, and migration strategy"
tags: ["research", "cursor", "windsurf", "ide-compatibility", "architecture"]
related:
  - "/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility.md"
audience: "ai-agent"
token_budget: "high"
complexity: "complex"
created: "2025-10-22"
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
- `src/**/*.ts` - TypeScript files in src/
- Multiple patterns: Cursor uses array `["*.py", "*.pyi"]`, Windsurf uses comma-separated `"*.py, *.pyi"`

**Transformation:**

- Cursor array → Windsurf comma-separated: `["*.py", "*.pyi"]` → `"*.py, *.pyi"`
- Windsurf comma-separated → Cursor array: `"*.py, *.pyi"` → `["*.py", "*.pyi"]`

## Unified Format Specification

### Unified Rule File (.unified/rules/rule-name.yaml)

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

## Section 1
Content...
```

### Unified Command File (.unified/commands/command-name.yaml)

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

## Objective
What this command/workflow does.

## Requirements
Prerequisites.

## Steps
1. Step 1
2. Step 2

## Expected Output
What should be produced.
```

## Directory Structure (Post-Migration)

```
.cursor/rules/                    # Generated from .unified/
.cursor/commands/                 # Generated from .unified/
.windsurf/rules/                  # Generated from .unified/
.windsurf/workflows/              # Generated from .unified/
.unified/                         # Source of truth
  ├── rules/
  ├── commands/
  └── README.md
scripts/adapters/                 # Transformation logic
  ├── unified_parser.py
  ├── cursor_adapter.py
  ├── windsurf_adapter.py
  └── validator.py
scripts/build_ide_configs.py      # Main build script
```

## Implementation Phases

### Phase 1: Architecture & Planning (Week 1)

- Create ADR for dual compatibility approach
- Design unified format specification
- Document transformation rules
- Create Cursor agent handoff document

### Phase 2: Adapter System (Week 2)

- Build Python adapter module (`scripts/adapters/`)
- Implement build process (`scripts/build_ide_configs.py`)
- Create validation infrastructure
- Integrate into CI/CD

### Phase 3: Rules Migration (Week 3)

- Convert 16 Windsurf rules to unified format
- Generate Cursor `.mdc` rules
- Validate transformations
- Test in both IDEs

### Phase 4: Commands/Workflows (Week 4)

- Convert 21 Windsurf workflows to unified format
- Generate Cursor commands
- Document equivalence and limitations
- Test in both IDEs

### Phase 5: Automation & Scripts (Week 5)

- Create IDE detection system
- Update Taskfile for both IDEs
- Build IDE-specific wrappers
- Document IDE-specific usage

### Phase 6: Documentation & Testing (Week 6)

- Create comprehensive Cursor agent documentation
- Update Windsurf documentation
- Create user guides for both IDEs
- Complete testing matrix

### Phase 7: Integration & Deployment (Week 7-8)

- CI/CD integration
- Deployment and release
- Maintenance documentation

## Critical Success Factors

1. **Unified format must be superset** of both IDE capabilities
2. **Adapters must be deterministic** (same input → same output)
3. **Validation must be comprehensive** (catch all errors)
4. **Documentation must be explicit** (no assumptions about IDE knowledge)
5. **Testing must cover both IDEs** (not just one)
6. **Maintenance process must be clear** (how to add new rules/commands)

## Risks & Mitigation

| Risk | Mitigation |
|------|-----------|
| Cursor `model_decision` equivalent missing | Use globs as best-effort, document limitation |
| Cursor commands too simple for complex workflows | Create composite commands, embed context |
| Adapter bugs cause inconsistency | Comprehensive validation, automated testing |
| Cursor agent lacks context | Comprehensive handoff document with all context |

## Key Resources for Implementation

1. **Windsurf Rules:** 16 files in `.windsurf/rules/` with trigger modes
2. **Windsurf Workflows:** 21 files in `.windsurf/workflows/` with multi-stage orchestration
3. **Existing Scripts:** `scripts/` directory with automation and validation
4. **Documentation Standards:** `docs/CONSTITUTION.md`, `docs/DOCUMENTATION_STRUCTURE.md`
5. **Repository Context:** `AGENTS.md`, project structure

## Next Steps for Cursor Agent

1. Review this research document thoroughly
2. Create `.unified/` directory structure
3. Build adapter system (`scripts/adapters/`)
4. Implement build process (`scripts/build_ide_configs.py`)
5. Migrate all 16 Windsurf rules to unified format
6. Generate Cursor `.mdc` rules and validate
7. Migrate all 21 Windsurf workflows to unified format
8. Generate Cursor commands and validate
9. Integrate automation and IDE detection
10. Complete documentation and testing
11. Deploy and release

---

**See:** `/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility.md` for initiative overview and timeline.
