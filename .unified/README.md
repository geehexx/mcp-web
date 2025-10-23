# Unified IDE Configuration System

This directory contains the unified source-of-truth configuration for both Cursor IDE and Windsurf IDE compatibility.

## Structure

```yaml
.unified/
├── README.md          # This file
├── rules/             # Unified rule definitions
└── commands/          # Unified command/workflow definitions
```

## Purpose

The unified system enables:

1. **Single Source of Truth**: Define rules and commands once
2. **IDE-Specific Generation**: Generate `.cursor/` and `.windsurf/` configs via adapters
3. **Consistency**: Ensure both IDEs have equivalent capabilities
4. **Maintenance**: Add new rules/commands in one place

## Unified Format

### Rules (`.unified/rules/rule-name.yaml`)

```yaml
---
title: "Rule Title"
description: "Brief description"
type: "rule"
status: "active"

# Windsurf-specific configuration
windsurf:
  trigger: "always_on"  # always_on, glob, model_decision, manual
  globs: "*.py, **/*.py"

# Cursor-specific configuration
cursor:
  alwaysApply: true  # true/false
  globs: ["*.py", "**/*.py"]

tags: ["tag1", "tag2"]
related: []

---

# Rule Content

Everything after the frontmatter is the actual rule content.
This is passed to both IDEs as-is.

## Section 1
Content...
```

### Commands (`.unified/commands/command-name.yaml`)

```yaml
---
title: "Command Title"
description: "Brief description"
type: "command"
status: "active"

# Windsurf workflow metadata
windsurf:
  type: "workflow"
  category: "category"
  complexity: "simple|moderate|complex"
  dependencies: []

# Cursor command metadata
cursor:
  pass_through: true

tags: ["tag1"]
related: []

---

# Command/Workflow Content

## Objective
What this command/workflow accomplishes.

## Requirements
Prerequisites and context needed.

## Steps
1. Step 1
2. Step 2
3. Step 3

## Expected Output
What should be produced.
```

## Building IDE Configs

Use the build script to generate IDE-specific configurations:

```bash
# Generate both IDE configs from unified source
python scripts/build_ide_configs.py

# Generate only Cursor configs
python scripts/build_ide_configs.py --cursor-only

# Generate only Windsurf configs
python scripts/build_ide_configs.py --windsurf-only
```

## Transformation Rules

### Rule Transformation

| Windsurf Trigger | Cursor Equivalent |
|------------------|-------------------|
| `always_on` | `alwaysApply: true` |
| `glob` | `alwaysApply: false` + `globs: "pattern"` |
| `model_decision` | `alwaysApply: false` (no globs, intelligent application via description) |
| `manual` | `alwaysApply: false` (no globs, manual reference) |

**Cursor Rule Application Logic:**

1. **Always Applied**: `alwaysApply: true` - Rule is always loaded
2. **File-Based**: `globs: "pattern"` - Rule applied when editing matching files
3. **Intelligent Application**: When `alwaysApply: false` and no `globs` present, Cursor uses the rule's description to intelligently determine when to apply the rule

### Command Transformation

- **Simple workflows**: 1:1 mapping to Cursor commands
- **Complex workflows**: Composite commands with embedded context
- **Multi-stage workflows**: Simplified for Cursor's single-stage model

## Adding New Rules/Commands

1. Create unified file in appropriate directory
2. Follow the unified format specification
3. Run build script to generate IDE configs
4. Test in both IDEs
5. Commit changes

## Validation

The build script includes validation to ensure:

- Unified format compliance
- Generated configs are valid
- Content consistency across IDEs
- Required fields are present

## Maintenance

- **Adding rules**: Create in `.unified/rules/`
- **Adding commands**: Create in `.unified/commands/`
- **Modifying existing**: Edit unified file, rebuild
- **Removing**: Delete unified file, rebuild

This system ensures both Cursor and Windsurf users have equivalent agent capabilities while maintaining a single source of truth for maintenance.
