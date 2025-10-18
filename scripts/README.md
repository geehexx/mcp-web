# Automation Scripts

This directory contains automation scripts for the mcp-web project to reduce token expenditure on mechanical workflow tasks.

## Phase 1: Template Scaffolding (Complete)

### Quick Start

```bash
# Create a new initiative
task scaffold:initiative

# Create a new ADR
task scaffold:adr

# Create a new session summary
task scaffold:summary
```

### scaffold.py - Template Generation Tool

**Purpose:** Generate standardized documents from Jinja2 templates with interactive prompts and validation.

**Usage:**

```bash
# Interactive mode (recommended)
task scaffold:initiative
task scaffold:adr
task scaffold:summary

# With config file
python scripts/scaffold.py --type initiative --config config.yaml

# Dry-run (preview without writing)
python scripts/scaffold.py --type adr --dry-run

# Validate template only
python scripts/scaffold.py --type initiative --validate-only
```

**Templates Available:**

- `initiative-flat.md.j2` - Flat file initiative (ADR-0013 format)
- `adr.md.j2` - Architecture Decision Record
- `session-summary.md.j2` - Session summary with metrics

**Features:**

- ✅ Interactive prompts for all fields
- ✅ Config file support (YAML/JSON)
- ✅ Auto-numbering (ADRs)
- ✅ Auto-dating (all templates)
- ✅ Markdown linting validation
- ✅ Frontmatter generation
- ✅ Dry-run mode

**Token Savings:**

- Initiative creation: 1500 tokens → 50 tokens (97% reduction)
- ADR creation: 1200 tokens → 50 tokens (96% reduction)
- Session summary: 2500 tokens → 100 tokens (96% reduction)

### Template Structure

```text
scripts/templates/
├── initiative-flat.md.j2    # Initiative template
├── adr.md.j2                 # ADR template
├── session-summary.md.j2     # Session summary template
└── schemas/                  # Future: validation schemas
```

### Testing

```bash
# Run scaffold tests
uv run python -m pytest tests/test_scaffold.py -c /dev/null

# All 26 tests pass
```

### Dependencies

- `jinja2>=3.1.0` - Template rendering
- `python-frontmatter>=1.0.0` - Markdown frontmatter
- `pyyaml>=6.0.0` - YAML parsing
- `click>=8.1.0` - CLI framework

## Future Phases

### Phase 2: File Operations (Planned)

- Archive initiative script
- Move file with reference updates
- Index/README automation

### Phase 3: Frontmatter Management (Planned)

- Schema validation
- Pre-commit hook integration
- Automatic frontmatter generation

### Phase 4: Session Summary Automation (Planned)

- YAML extraction (30% more token-efficient than JSON)
- Summary consolidation
- Template-based generation

## Development

### Adding New Templates

**Steps:**

1. Create template file in `scripts/templates/`

   ```jinja2
   # my-template.md.j2
   # {{ title }}

   **Created:** {{ date }}

   {{ content }}
   ```

2. Add to `TemplateType` enum in `scaffold.py`
3. Add schema in `Scaffolder.get_schema()`
4. Add to template_files mapping in `render()` and `validate_template()`
5. Add Taskfile command
6. Write tests

### Template Guidelines

- Use Jinja2 syntax
- Support optional fields with `{% if %}` blocks
- Use `{%- -%}` to control whitespace
- Validate all generated files with markdownlint

## References

- Initiative: [2025-10-18-workflow-automation-enhancement.md](../docs/initiatives/active/2025-10-18-workflow-automation-enhancement.md)
- Technical Design: [technical-design.md](../docs/initiatives/active/2025-10-18-workflow-automation-enhancement/technical-design.md)
- ADR-0013: [Initiative Documentation Standards](../docs/adr/0013-initiative-documentation-standards.md)
