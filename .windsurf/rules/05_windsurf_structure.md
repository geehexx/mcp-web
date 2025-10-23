---
trigger: manual
description: Windsurf-specific structure and workflow system documentation
title: Windsurf Structure
---

related:

- "/docs/IDE_COMPATIBILITY.md"

# Windsurf Structure

## Directory Structure

```yaml
.windsurf/
├── rules/                   # Rule definitions
│   ├── 00_core_directives.md
│   ├── 01_python_code.md
│   └── ...
├── workflows/               # Workflow definitions
│   ├── work.md
│   ├── implement.md
│   └── ...
├── schemas/                 # Schema definitions
└── workflow-improvement-analysis.json
```

## Rule System

### Trigger Modes

- **always_on**: Rule is automatically loaded in every session
- **glob**: Rule is applied when editing files matching glob patterns
- **model_decision**: Cascade AI determines when to apply the rule based on context
- **manual**: Rule is only applied when manually referenced

### Rule Format

```yaml
---
trigger: always_on
description: "Rule description"
globs: "*.py, **/*.py"  # For glob trigger
---
```

## Workflow System

### Workflow Types

- **Orchestrator**: Central workflows that coordinate other workflows
- **Implementation**: Workflows for implementing features
- **Validation**: Workflows for quality assurance
- **Documentation**: Workflows for documentation tasks

### Workflow Format

```yaml
---
created: "2025-10-17"
updated: "2025-10-21"
description: "Workflow description"
auto_execution_mode: 3
category: "Implementation"
complexity: 75
dependencies: []
status: active
---
```

### Workflow Execution

- **Multi-stage**: Workflows can have multiple stages
- **Context Loading**: Workflows can load additional context
- **Memory System**: Workflows can maintain state across stages
- **Automation**: Workflows can trigger automated actions

## Integration with Cursor

### Transformation

Windsurf workflows are transformed to Cursor commands:

- **Simple Workflows**: 1:1 mapping to Cursor commands
- **Complex Workflows**: Composite commands with embedded context
- **Multi-stage**: Simplified to single-stage commands

### Context Handling

- **Embedded Context**: All necessary context must be embedded in Cursor commands
- **No Memory System**: Cursor commands cannot maintain state across sessions
- **Simplified Structure**: Cursor commands are simpler than Windsurf workflows

## Rule Metadata

**File:** `05_windsurf_structure.yaml`
**Trigger:** manual (Windsurf) / alwaysApply: false (Cursor)
**Estimated Tokens:** ~800
**Last Updated:** 2025-10-22
**Status:** Active

**Topics Covered:**

- Windsurf directory structure
- Rule system
- Workflow system
- Integration with Cursor

**Workflow References:**

- All workflows (for understanding structure)

**Dependencies:**

- Source: 05_windsurf_structure.md
