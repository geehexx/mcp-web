---
title: "Cursor & Windsurf Dual Compatibility Initiative"
type: "initiative"
status: "Active"
description: "Enable simultaneous compatibility with both Cursor and Windsurf IDEs by creating a unified rules/commands/workflows system that adapts to each IDE's architecture"
tags: ["infrastructure", "tooling", "automation", "cursor", "windsurf", "compatibility"]
priority: "High"
owner: "@ai-agent"
start_date: "2025-10-22"
target_date: "2025-12-15"
estimated_hours: 60
related:
  - "/docs/adr/0002-adopt-windsurf-workflow-system.md"
  - "/docs/adr/0018-workflow-architecture-v3.md"
  - "/docs/research/2025-10-22-cursor-windsurf-research.md"
  - "/AGENTS.md"
  - "/.windsurf/rules/"
  - "/.windsurf/workflows/"
audience: "ai-agent"
token_budget: "high"
complexity: "complex"
created: "2025-10-22"
---

# Cursor & Windsurf Dual Compatibility Initiative

## Executive Summary

This initiative enables the mcp-web project to operate seamlessly with both **Cursor IDE** and **Windsurf IDE** by creating a unified, adapter-based system for rules, commands, and workflows. Rather than maintaining separate implementations, we will:

1. Create a **unified rules/commands source of truth** (`.unified/` directory)
2. Build **IDE-specific adapters** that transform unified definitions into Cursor/Windsurf formats
3. Implement **dynamic routing** in scripts and automation to detect and adapt to the active IDE
4. Establish **validation and testing** to ensure consistency across both IDEs
5. Provide **comprehensive documentation** for both IDE agents to understand the system

**Key Insight:** Cursor and Windsurf have fundamentally different architectures:

- **Windsurf:** Complex multi-stage workflows with memory system and orchestration
- **Cursor:** Simpler commands with rule-based context and agent autonomy

Our solution leverages each IDE's strengths while maintaining consistency through a unified source format.

---

## Current State Analysis

### Windsurf System (Current)

- **Rules:** 16 markdown files in `.windsurf/rules/` with trigger modes (always_on, glob, model_decision, manual)
- **Workflows:** 21 markdown files in `.windsurf/workflows/` with multi-stage orchestration
- **Automation:** Python scripts + Taskfile for file operations, validation, scaffolding
- **Strengths:** Complex orchestration, memory system, context loading, task tracking

### Cursor System (Target)

- **Rules:** `.mdc` files in `.cursor/rules/` with frontmatter (description, globs, alwaysApply)
- **Commands:** Markdown files in `.cursor/commands/` (simpler than Windsurf workflows)
- **Automation:** Manual or via rules (no equivalent to Windsurf Taskfile)
- **Strengths:** Agent autonomy, sophisticated code generation, simpler mental model

### Key Architectural Differences

| Aspect | Cursor | Windsurf |
|--------|--------|----------|
| Rules Format | `.mdc` with YAML | `.md` with YAML |
| Rule Triggers | alwaysApply, globs, manual, relevant | always_on, glob, model_decision, manual |
| Commands/Workflows | Simple markdown (`.cursor/commands/`) | Complex multi-stage (`.windsurf/workflows/`) |
| Orchestration | Agent Mode (systematic) | Cascade (multi-stage with memory) |
| Context System | Rules + Commands | Rules + Workflows + Memory |
| Automation | Manual or rules-based | Scripts + Taskfile + Workflows |

**Critical Constraint:** Cursor has no equivalent to Windsurf's `model_decision` trigger or multi-stage workflow orchestration. Solution: Use globs as best-effort, embed context in commands.

---

## Migration Strategy Overview

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

---

## Technical Approach

### Unified Format

**Unified Rule (.unified/rules/rule-name.yaml):**

```yaml
---
title: "Rule Title"
description: "Brief description"
type: "rule"
windsurf:
  trigger: "always_on"  # always_on, glob, model_decision, manual
  globs: "*.py"
cursor:
  alwaysApply: true
  globs: ["*.py"]
tags: ["tag1"]
---
# Rule content here
```

**Unified Command (.unified/commands/cmd-name.yaml):**

```yaml
---
title: "Command Title"
description: "Brief description"
type: "command"
windsurf:
  type: "workflow"
  complexity: "simple"
cursor:
  pass_through: true
---
# Command/Workflow content
```

### Adapter Transformation Logic

**Windsurf → Cursor:**

- `always_on` → `alwaysApply: true`
- `glob` → `globs: [...]`
- `model_decision` → `globs` (best-effort) or manual
- `manual` → no globs/alwaysApply

**Cursor → Windsurf:**

- `alwaysApply: true` → `always_on`
- `globs` → `glob`
- No globs/alwaysApply → `manual`

### Directory Structure (Post-Migration)

```
.cursor/rules/           # Generated from .unified/
.cursor/commands/        # Generated from .unified/
.windsurf/rules/         # Generated from .unified/
.windsurf/workflows/     # Generated from .unified/
.unified/                # Source of truth
  ├── rules/
  ├── commands/
  └── README.md
scripts/adapters/        # Transformation logic
  ├── unified_parser.py
  ├── cursor_adapter.py
  ├── windsurf_adapter.py
  └── validator.py
```

---

## Success Criteria

1. **Functional Equivalence:** All Windsurf rules/workflows have Cursor equivalents
2. **Code Reuse:** 90%+ of content shared (unified format)
3. **Consistency:** Rules behave identically in both IDEs (where possible)
4. **Maintainability:** Adding new rule requires single unified file
5. **Testing:** All rules/commands tested in both IDEs
6. **Documentation:** Comprehensive guides for both IDEs

---

## Risks & Mitigation

| Risk | Mitigation |
|------|-----------|
| Cursor `model_decision` equivalent missing | Use globs as best-effort, document limitation |
| Cursor commands too simple for complex workflows | Create composite commands, embed context |
| Adapter bugs cause inconsistency | Comprehensive validation, automated testing |
| Cursor agent lacks context | Comprehensive handoff document with all context |

---

## For Implementation Agent (Cursor)

**See:** `/docs/research/2025-10-22-cursor-windsurf-research.md` for comprehensive research, technical details, and implementation guide.

**Key Resources Provided:**

1. Complete Windsurf rules analysis (16 files)
2. Complete Windsurf workflows analysis (21 files)
3. Cursor IDE architecture documentation
4. Transformation specifications
5. Adapter implementation guide
6. Testing procedures
7. Documentation templates

**Implementation Sequence:**

1. Review research document thoroughly
2. Create `.unified/` directory structure
3. Build adapter system
4. Migrate rules (with validation)
5. Migrate commands/workflows
6. Integrate automation
7. Test in both IDEs
8. Document for both IDE users

**Critical Success Factors:**

- Unified format must be superset of both IDEs
- Adapters must be deterministic
- Validation must be comprehensive
- Documentation must be explicit
- Testing must cover both IDEs

---

## Timeline

| Phase | Duration | Milestone |
|-------|----------|-----------|
| 1: Architecture | 1 week | ADR + Specifications |
| 2: Adapters | 1 week | Build system ready |
| 3: Rules | 1 week | Unified rules + Cursor rules |
| 4: Commands | 1 week | Unified commands + Cursor commands |
| 5: Automation | 1 week | IDE detection + scripts |
| 6: Documentation | 1 week | All documentation complete |
| 7: Integration | 2 weeks | Deployment + release |

**Total:** 8 weeks (60 estimated hours)

---

## Next Steps

1. **Windsurf Agent (This Session):** Create this initiative ✓
2. **Cursor Agent (Next Session):** Implement using research document as comprehensive context
3. **Both Agents:** Validate and test in respective IDEs
4. **Deployment:** Integrate into CI/CD and release

---

**Created:** 2025-10-22
**Status:** Ready for implementation
**Implementation Platform:** Cursor IDE (with Windsurf reference)
