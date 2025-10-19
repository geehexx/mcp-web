# Technical Design: Workflow Automation Enhancement

**Initiative:** 2025-10-18-workflow-automation-enhancement
**Author:** AI Agent (Cascade)
**Created:** 2025-10-18
**Status:** Draft

---

## Architecture Overview

### System Components

```text
Workflow Automation System
├── scaffold.py        - Template engine (Jinja2 + interactive prompts)
├── file_ops.py        - File operations (move, archive, update refs)
├── frontmatter_mgr.py - Frontmatter validation/generation
└── summarize.py       - Session summary extraction/consolidation
```

### Key Design Decisions

#### 1. Python + Jinja2 over Cookiecutter

- **Why:** Simpler for single-repo use, full control, zero extra deps
- **Trade-off:** Less feature-rich than Cookiecutter ecosystem

#### 2. Click for CLI interface

- **Why:** Already in project, clean argument parsing, testing support
- **Trade-off:** More verbose than argparse

#### 3. Taskfile as primary API

- **Why:** Consistent with project standards, hides complexity, user-friendly
- **Trade-off:** Adds indirection layer

#### 4. YAML for session summary extraction

- 30% more token-efficient than JSON (Microsoft Research 2025)
- Use YAML format (from consolidate-summaries.md)
- Validate against schema to prevent LLM hallucination
- **Trade-off:** More rigid than freeform extraction

---

## Module APIs

### 1. scaffold.py - Template Engine

```python
# Usage
task scaffold:initiative           # Interactive prompts
task scaffold:adr                  # Interactive prompts
task scaffold:summary              # Interactive prompts
python scripts/scaffold.py --type initiative --config config.yaml
```

**Key Functions:**

- `prompt_interactive()` - CLI prompts for template fields
- `render(fields)` - Jinja2 template rendering
- `validate_output(path)` - Post-generation validation
- `generate_path(fields)` - Auto-generate output path

### 2. file_ops.py - File Operations

```python
# Usage
task archive:initiative <name>
task move:file <src> <dst> --update-refs
python scripts/file_ops.py archive-initiative <name>
```

**Key Functions:**

- `archive_initiative(name)` - Move to completed/ + update refs
- `move_file(src, dst)` - Move + update all references
- `update_references(old, new)` - Grep + sed reference updates
- `update_index(dir)` - Regenerate README index

### 3. frontmatter_mgr.py - Frontmatter Management

```python
# Usage
task validate:frontmatter
task validate:frontmatter:file <path>
python scripts/frontmatter_mgr.py validate --all
```

**Key Functions:**

- `validate_file(path)` - Check schema compliance
- `generate_frontmatter(type, fields)` - Create valid YAML
- `update_frontmatter(path, updates)` - Merge new fields

### 4. summarize.py - Session Summary Tools

```python
# Usage
task summary:extract <file> -o <yaml>
task summary:consolidate <date>
python scripts/summarize.py extract <file>
```

**Key Functions:**

- `extract_file(path)` - Markdown → YAML extraction (30% more token-efficient)
- `consolidate_date(date)` - Merge summaries for date
- `apply_consolidation_rules(data)` - Deduplicate + merge

---

## Template Structure

```text
scripts/templates/
├── initiative-flat.md.j2         # Flat file initiative
├── initiative-folder/            # Folder-based initiative
│   ├── initiative.md.j2
│   ├── phases/
│   └── artifacts/
├── adr.md.j2                     # ADR template
├── session-summary.md.j2         # Session summary
├── workflow.md.j2                # Workflow with frontmatter
└── schemas/                      # Schemas for validation
    ├── frontmatter.yaml          # Frontmatter schemas
    └── session-summary.yaml      # Session summary schema
```

---

## Integration with Workflows

### Before (Manual)

```markdown
1. AI agent constructs initiative document line-by-line (1500 tokens)
2. AI manually creates directory structure
3. AI generates frontmatter with potential errors
4. AI moves files and searches for references manually
```

### After (Automated)

```markdown
1. Agent: "task scaffold:initiative" (50 tokens)
2. Script prompts for fields interactively
3. Template rendered with validation
4. Agent: "task archive:initiative X" (30 tokens)
```

---

## Testing Strategy

**Unit Tests (pytest):**

- `test_scaffold.py` - Template rendering, validation
- `test_file_ops.py` - File moves, reference updates
- `test_frontmatter.py` - Schema validation
- `test_summarize.py` - Extraction, consolidation

**Integration Tests:**

- `test_workflows.py` - End-to-end workflow invocation
- `test_generated_files.py` - Validate scaffolded files pass linting

**Fixtures:**

- `tests/fixtures/templates/` - Sample templates
- `tests/fixtures/docs/` - Sample documents for testing

---

## Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Template scaffold | <1s | Including prompts + validation |
| Archive initiative | <2s | Including reference search/update |
| Frontmatter validate | <0.5s | Per file |
| Summary extract | <1s | Per file |
| Summary consolidate | <5s | Up to 10 summaries |

---

## Security Considerations

**1. Path Traversal Prevention:**

- Validate all paths are within project root
- No symlink following for file operations

**2. Template Injection Prevention:**

- Use Jinja2 autoescape for user input in templates
- Validate field values before rendering

**3. Command Injection Prevention:**

- Use subprocess with argument lists (not shell=True)
- Sanitize all user inputs

---

## Extensibility

### Adding New Template Types

1. Create `scripts/templates/new-type.md.j2`
2. Add `TemplateType.NEW_TYPE` enum
3. Add schema in `Scaffolder.get_schema()`
4. Add Taskfile command: `task scaffold:new-type`

### Adding New File Operations

1. Implement function in `file_ops.py`
2. Add Click command decorator
3. Add Taskfile shortcut
4. Write tests

---

## References

- **Research:** Web search results on Cookiecutter, Plop, Jinja2 automation
- **Standards:** ADR-0013 (Initiative Standards), DOCUMENTATION_STRUCTURE.md
- **Examples:** `scripts/benchmark_pipeline.py` (existing automation pattern)
