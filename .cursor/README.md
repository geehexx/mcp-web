# Cursor IDE Configuration

This directory contains Cursor IDE-specific configuration files generated from the unified source in `.unified/`.

## Overview

The Cursor configuration provides equivalent agent capabilities to Windsurf IDE through:

- **Rules**: `.mdc` files in `rules/` directory
- **Commands**: `.md` files in `commands/` directory

## Rules

Rules are automatically applied based on their configuration:

### Always Applied Rules

Rules with `alwaysApply: true` are automatically loaded in every session:

- `00_core_directives.mdc` - Core agent directives and principles

### File-Based Rules

Rules with `globs` patterns are automatically attached when editing matching files:

- `01_python_code.mdc` - Applied when editing `.py` files
- `02_testing.mdc` - Applied when editing test files

### Manual Rules

Rules without `alwaysApply` or `globs` must be manually referenced using `@rule-name`.

## Commands

Commands are available via the command palette or can be invoked directly:

### Available Commands

- `/validate` - Quality validation workflow

### Using Commands

1. **Command Palette**: Open command palette and search for command name
2. **Direct Invocation**: Type `/command-name` in chat
3. **Context Menu**: Right-click and select command

## Limitations vs Windsurf

Due to architectural differences, some Windsurf features have limitations in Cursor:

### Rules

- **No `model_decision` trigger**: Cursor doesn't have equivalent to Windsurf's model_decision trigger
- **Simpler glob patterns**: Cursor uses array format vs Windsurf's comma-separated strings
- **No conditional loading**: All rules are either always-on or file-based

### Commands/Workflows

- **No multi-stage orchestration**: Cursor commands are single-purpose vs Windsurf's multi-stage workflows
- **No memory system**: Context must be embedded in commands
- **No automatic chaining**: Commands don't automatically chain to other workflows

## Troubleshooting

### Rules Not Loading

1. Check file format (must be `.mdc` with valid frontmatter)
2. Verify glob patterns are correct
3. Ensure file is in `rules/` directory

### Commands Not Working

1. Check command exists in `commands/` directory
2. Verify command format (must be `.md` with valid frontmatter)
3. Try using command palette instead of direct invocation

### Content Issues

1. Check if content is identical to Windsurf version
2. Verify transformations are correct
3. Rebuild configurations if needed

## Rebuilding Configuration

To regenerate Cursor configuration from unified source:

```bash
# Rebuild all configurations
python scripts/build_ide_configs.py

# Rebuild only Cursor configuration
python scripts/build_ide_configs.py --cursor-only

# Verbose output
python scripts/build_ide_configs.py --verbose
```

## File Structure

```
.cursor/
├── README.md              # This file
├── rules/                 # Rule definitions
│   ├── 00_core_directives.mdc
│   ├── 01_python_code.mdc
│   └── 02_testing.mdc
└── commands/              # Command definitions
    └── validate.md
```

## Integration

This configuration integrates with:

- **Unified System**: Generated from `.unified/` source
- **Build Script**: `scripts/build_ide_configs.py`
- **Validation**: Automated validation of transformations
- **CI/CD**: Automated building in pipelines

## Maintenance

- **Adding Rules**: Add to `.unified/rules/` and rebuild
- **Adding Commands**: Add to `.unified/commands/` and rebuild
- **Modifying**: Edit unified source and rebuild
- **Removing**: Delete from unified source and rebuild

## Support

For issues with Cursor configuration:

1. Check this README for troubleshooting steps
2. Verify unified source is correct
3. Rebuild configurations
4. Check IDE compatibility documentation

---

**Generated:** 2025-10-22
**Source:** Unified system in `.unified/`
**Maintainer:** mcp-web core team
