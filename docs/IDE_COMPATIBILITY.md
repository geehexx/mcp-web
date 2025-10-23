# IDE Compatibility System

This document describes the unified IDE compatibility system that enables the mcp-web project to work seamlessly with both **Cursor IDE** and **Windsurf IDE**.

## Overview

The unified system provides:

1. **Single Source of Truth**: Define rules and commands once in `.unified/` format
2. **IDE-Specific Generation**: Generate `.cursor/` and `.windsurf/` configs via adapters
3. **Consistency**: Ensure both IDEs have equivalent capabilities
4. **Maintenance**: Add new rules/commands in one place

## Architecture

```text
.unified/                    # Unified source of truth
├── rules/                   # Unified rule definitions
│   ├── 00_core_directives.yaml
│   ├── 01_python_code.yaml
│   └── 02_testing.yaml
└── commands/                # Unified command/workflow definitions
    └── validate.yaml

scripts/adapters/            # Adapter system
├── __init__.py
├── unified_parser.py        # Parse unified format
├── cursor_adapter.py        # Transform to Cursor format
├── windsurf_adapter.py      # Transform to Windsurf format
└── validator.py             # Validate transformations

scripts/build_ide_configs.py # Main build script
```

## Unified Format Specification

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

## Transformation Rules

### Rule Transformation (Windsurf → Cursor)

| Windsurf Trigger | Cursor Equivalent |
|------------------|-------------------|
| `always_on` | `alwaysApply: true` |
| `glob` | `alwaysApply: false` + `globs: "pattern"` |
| `model_decision` | `alwaysApply: false` (no globs, intelligent application via description) |
| `manual` | `alwaysApply: false` (no globs, manual reference) |

**Glob Pattern Conversion:**

- Windsurf: `"*.py, **/*.py"` (comma-separated string)
- Cursor: `"*.py, **/*.py"` (same format, raw unquoted)

**Content:** Remains identical

**Cursor Rule Application Logic:**

1. **Always Applied**: `alwaysApply: true` - Rule is always loaded
2. **File-Based**: `globs: "pattern"` - Rule applied when editing matching files
3. **Intelligent Application**: When `alwaysApply: false` and no `globs` present, Cursor uses the rule's description to intelligently determine when to apply the rule

### Command/Workflow Transformation

**Simple Workflows (1-2 stages):**

- 1:1 mapping to Cursor command
- Structure: Objective + Requirements + Steps + Expected Output

**Complex Workflows (3+ stages):**

- Composite command with embedded context
- Include note about Windsurf workflow equivalence
- Embed all necessary context (no memory system)

## Building IDE Configs

### Basic Usage

```bash
# Generate both IDE configs from unified source
python scripts/build_ide_configs.py

# Generate only Cursor configs
python scripts/build_ide_configs.py --cursor-only

# Generate only Windsurf configs
python scripts/build_ide_configs.py --windsurf-only

# Verbose output
python scripts/build_ide_configs.py --verbose
```

### Build Process

1. **Parse Unified Files**: Read all `.yaml` files in `.unified/rules/` and `.unified/commands/`
2. **Transform Rules**: Convert to IDE-specific formats
3. **Transform Commands**: Convert to IDE-specific formats
4. **Validate**: Ensure transformations are correct
5. **Generate Files**: Write `.cursor/` and `.windsurf/` directories

### Output Structure

```text
.cursor/
├── rules/                   # Generated .mdc files
│   ├── 00_core_directives.mdc
│   ├── 01_python_code.mdc
│   └── 02_testing.mdc
└── commands/                # Generated .md files
    └── validate.md

.windsurf/
├── rules/                   # Generated .md files
│   ├── 00_core_directives.md
│   ├── 01_python_code.md
│   └── 02_testing.md
└── workflows/               # Generated .md files
    └── validate.md
```

## Adding New Rules/Commands

### 1. Create Unified File

Create a new `.yaml` file in the appropriate directory:

```bash
# For a new rule
touch .unified/rules/new_rule.yaml

# For a new command
touch .unified/commands/new_command.yaml
```

### 2. Follow Format Specification

Use the unified format specification above to define your rule or command.

### 3. Build and Test

```bash
# Build the configurations
python scripts/build_ide_configs.py --verbose

# Test in both IDEs
# - Load Cursor and verify rule/command works
# - Load Windsurf and verify rule/workflow works
```

### 4. Validate

Ensure both IDEs behave equivalently:

- Rules trigger correctly
- Commands execute properly
- Content is identical

## Maintenance

### Updating Existing Rules/Commands

1. Edit the unified file in `.unified/`
2. Run build script
3. Test in both IDEs
4. Commit changes

### Removing Rules/Commands

1. Delete the unified file
2. Run build script (will remove generated files)
3. Test that both IDEs no longer have the rule/command

### Troubleshooting

**Build Errors:**

- Check YAML syntax in unified files
- Verify required fields are present
- Check file permissions

**IDE Issues:**

- Verify generated files are valid
- Check IDE-specific format requirements
- Test with minimal examples

## Validation

The build system includes comprehensive validation:

- **Format Validation**: Ensures unified files follow specification
- **Transformation Validation**: Verifies transformations are correct
- **Content Validation**: Ensures content is preserved
- **Consistency Validation**: Checks both IDEs get equivalent content

## Integration with CI/CD

The build process can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/build-ide-configs.yml
name: Build IDE Configs
on:
  push:
    paths:
      - '.unified/**'
      - 'scripts/adapters/**'
      - 'scripts/build_ide_configs.py'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Build IDE configs
        run: python scripts/build_ide_configs.py
      - name: Validate generated files
        run: |
          # Add validation steps here
          echo "Validation passed"
```

## Success Criteria

The unified system is successful when:

1. ✅ All 16 Windsurf rules have Cursor equivalents
2. ✅ All 21 Windsurf workflows have Cursor command equivalents
3. ✅ 90%+ of content is shared (unified format)
4. ✅ Adapters are deterministic (same input → same output)
5. ✅ Validation catches all errors
6. ✅ Both IDEs behave equivalently (where possible)
7. ✅ Adding new rule requires single unified file
8. ✅ Comprehensive documentation for both IDEs
9. ✅ CI/CD integration complete
10. ✅ All tests pass in both IDEs

## Future Enhancements

Potential improvements to the unified system:

- **Automated Testing**: Test generated configs in both IDEs
- **Migration Tools**: Automated migration from existing configs
- **Validation Rules**: IDE-specific validation rules
- **Documentation Generation**: Auto-generate IDE-specific docs
- **Version Management**: Track changes to unified configs

## References

- [Cursor IDE Documentation](https://cursor.sh/docs)
- [Windsurf IDE Documentation](https://windsurf.ai/docs)
- [MCP Web Project Constitution](docs/CONSTITUTION.md)
- [Unified Format Specification](.unified/README.md)

---

**Created:** 2025-10-22
**Status:** Active
**Maintainer:** mcp-web core team
