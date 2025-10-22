---
title: "Cursor Agent Handoff: Dual IDE Compatibility Initiative"
type: "handoff"
status: "active"
description: "Comprehensive context and instructions for Cursor agent to implement Cursor/Windsurf dual compatibility"
tags: ["handoff", "cursor", "windsurf", "implementation", "context"]
related:
  - "/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility.md"
  - "/docs/research/2025-10-22-cursor-windsurf-research.md"
  - "/AGENTS.md"
audience: "ai-agent"
token_budget: "high"
complexity: "complex"
created: "2025-10-22"
---

# Cursor Agent Handoff: Dual IDE Compatibility Initiative

## Mission

You are implementing a **unified rules/commands system** that enables the mcp-web project to work seamlessly with both **Cursor IDE** and **Windsurf IDE**. This is a **complex infrastructure project** requiring deep understanding of both IDE architectures and careful implementation.

## What You're Building

A **unified source-of-truth system** that:

1. Stores all rules and commands in a single `.unified/` format
2. Generates IDE-specific configurations via adapters
3. Maintains consistency across both IDEs
4. Simplifies maintenance (add rule once, generates for both IDEs)
5. Enables both IDE agents to work with equivalent capabilities

## Current State

### Windsurf (Existing - Reference)

**Rules:** 16 markdown files in `.windsurf/rules/`

- Trigger modes: `always_on`, `glob`, `model_decision`, `manual`
- Example: `00_core_directives.md` (always_on), `01_python_code.md` (glob: *.py)

**Workflows:** 21 markdown files in `.windsurf/workflows/`

- Multi-stage orchestration with context loading
- Examples: `/work`, `/implement`, `/validate`, `/commit`, `/archive-initiative`

**Automation:** Python scripts + Taskfile

- File operations, validation, scaffolding
- Integrated with workflows

### Cursor (Target - What You're Building)

**Rules:** `.mdc` files in `.cursor/rules/` (to be created)

- Trigger modes: `alwaysApply`, `globs`, manual, relevant
- Simpler than Windsurf (no `model_decision` equivalent)

**Commands:** Markdown files in `.cursor/commands/` (to be created)

- Simpler than Windsurf workflows (no multi-stage orchestration)
- Context must be embedded (no memory system)

## Critical Architectural Differences

### Rules

| Aspect | Cursor | Windsurf |
|--------|--------|----------|
| Format | `.mdc` with YAML | `.md` with YAML |
| Trigger: Always | `alwaysApply: true` | `always_on` |
| Trigger: File-based | `globs: ["*.py"]` | `glob` with `globs: "*.py"` |
| Trigger: Conditional | None (agent-decided) | `model_decision` (Cascade-decided) |
| Trigger: Manual | No globs/alwaysApply | `manual` |

**Key Constraint:** Cursor has NO equivalent to Windsurf's `model_decision` trigger. Solution: Use `globs` as best-effort, document limitation.

### Commands/Workflows

| Aspect | Cursor | Windsurf |
|--------|--------|----------|
| Format | Simple markdown | Complex markdown with frontmatter |
| Stages | Single-purpose | Multi-stage orchestration |
| Context | Embedded in command | Loaded via `/load-context` |
| Memory | None (per-session) | Persistent across stages |
| Automation | Manual or rules | Integrated via `task` commands |

**Key Constraint:** Cursor commands are simpler. Complex Windsurf workflows need composite commands with embedded context.

## Implementation Roadmap

### Phase 1: Adapter System (This Session)

**Deliverables:**

- `.unified/` directory structure
- `scripts/adapters/` module (unified_parser, cursor_adapter, windsurf_adapter, validator)
- `scripts/build_ide_configs.py` (main build script)
- Validation infrastructure

**Key Files to Create:**

```text
.unified/
  ├── README.md
  ├── rules/
  └── commands/

scripts/adapters/
  ├── __init__.py
  ├── unified_parser.py
  ├── cursor_adapter.py
  ├── windsurf_adapter.py
  └── validator.py

scripts/build_ide_configs.py
```

### Phase 2: Rules Migration

**Deliverables:**

- All 16 Windsurf rules converted to `.unified/rules/` format
- Generated `.cursor/rules/` directory (16 .mdc files)
- Validation report
- Testing in both IDEs

**Process:**

1. Analyze each Windsurf rule (trigger mode, globs, content)
2. Create unified version
3. Run adapter to generate Cursor .mdc
4. Validate both versions
5. Test in both IDEs

### Phase 3: Commands/Workflows Migration

**Deliverables:**

- All 21 Windsurf workflows converted to `.unified/commands/` format
- Generated `.cursor/commands/` directory (21 markdown files)
- Equivalence documentation
- Testing in both IDEs

**Process:**

1. Analyze each Windsurf workflow (complexity, stages, dependencies)
2. Create unified version
3. Run adapter to generate Cursor command
4. Validate both versions
5. Test in both IDEs

### Phase 4: Integration & Deployment

**Deliverables:**

- CI/CD integration (build step)
- IDE detection system
- Comprehensive documentation
- Release

## Unified Format Specification

### Unified Rule (.unified/rules/rule-name.yaml)

```yaml
---
title: "Rule Title"
description: "Brief description of what this rule does"
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

# Common metadata
tags: ["tag1", "tag2"]
related:
  - "/docs/adr/0001-decision.md"

---

# Rule Content

Everything after the frontmatter is the actual rule content.
This is passed to both IDEs as-is.

## Section 1
Content...

## Section 2
Content...
```

### Unified Command (.unified/commands/command-name.yaml)

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

# Cursor command metadata (usually just pass_through)
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

**Trigger Mode Mapping:**

- `always_on` → `alwaysApply: true`
- `glob` → `globs: [...]` (convert comma-separated to array)
- `model_decision` → Use `globs` if available, else manual (no globs/alwaysApply)
- `manual` → No globs/alwaysApply

**Glob Pattern Conversion:**

- Windsurf: `"*.py, **/*.py"` (comma-separated string)
- Cursor: `["*.py", "**/*.py"]` (array)

**Content:** Remains identical

### Command/Workflow Transformation

**Simple Workflows (1-2 stages):**

- 1:1 mapping to Cursor command
- Structure: Objective + Requirements + Steps + Expected Output

**Complex Workflows (3+ stages):**

- Composite command with embedded context
- Include note about Windsurf workflow equivalence
- Embed all necessary context (no memory system)

## Key Implementation Tasks

### Task 1: Create Unified Format Parser

**File:** `scripts/adapters/unified_parser.py`

```python
class UnifiedParser:
    """Parse unified format YAML files."""

    def parse(self, file_path: str) -> dict:
        """Parse unified file and return structured data."""
        # Read YAML frontmatter
        # Read content
        # Return dict with frontmatter and content
        pass
```

### Task 2: Create Cursor Adapter

**File:** `scripts/adapters/cursor_adapter.py`

```python
class CursorAdapter:
    """Transform unified format to Cursor format."""

    def transform_rule(self, unified: dict) -> dict:
        """Transform unified rule to Cursor .mdc format."""
        # Extract cursor-specific config
        # Transform trigger modes
        # Convert globs format
        # Return Cursor rule dict
        pass

    def transform_command(self, unified: dict) -> dict:
        """Transform unified command to Cursor markdown."""
        # Extract command content
        # Format as markdown
        # Return Cursor command dict
        pass
```

### Task 3: Create Windsurf Adapter

**File:** `scripts/adapters/windsurf_adapter.py`

```python
class WindsurfAdapter:
    """Transform unified format to Windsurf format."""

    def transform_rule(self, unified: dict) -> dict:
        """Transform unified rule to Windsurf .md format."""
        # Extract windsurf-specific config
        # Transform trigger modes
        # Convert globs format
        # Return Windsurf rule dict
        pass

    def transform_workflow(self, unified: dict) -> dict:
        """Transform unified command to Windsurf workflow."""
        # Extract workflow content
        # Add Windsurf metadata
        # Format as markdown
        # Return Windsurf workflow dict
        pass
```

### Task 4: Create Validator

**File:** `scripts/adapters/validator.py`

```python
class Validator:
    """Validate transformed rules and commands."""

    def validate_cursor_rule(self, rule: dict) -> bool:
        """Validate Cursor rule format."""
        # Check required fields (description)
        # Validate frontmatter
        # Check globs format if present
        # Return True/False
        pass

    def validate_windsurf_rule(self, rule: dict) -> bool:
        """Validate Windsurf rule format."""
        # Check required fields (trigger, description)
        # Validate trigger mode
        # Check globs format if present
        # Return True/False
        pass
```

### Task 5: Create Build Script

**File:** `scripts/build_ide_configs.py`

```python
#!/usr/bin/env python3
"""Build IDE-specific configs from unified source."""

from pathlib import Path
from adapters import UnifiedParser, CursorAdapter, WindsurfAdapter, Validator

def build_configs():
    """Main build function."""
    # Initialize adapters
    # For each rule in .unified/rules/:
    #   - Parse unified format
    #   - Generate Cursor .mdc
    #   - Generate Windsurf .md
    #   - Validate both
    # For each command in .unified/commands/:
    #   - Parse unified format
    #   - Generate Cursor markdown
    #   - Generate Windsurf workflow
    #   - Validate both
    # Report results
    pass

if __name__ == "__main__":
    build_configs()
```

## Testing Strategy

### Unit Testing

1. **Parser Tests:** Verify unified format parsing
2. **Adapter Tests:** Verify transformations (Windsurf → Cursor, Cursor → Windsurf)
3. **Validator Tests:** Verify validation logic

### Integration Testing

1. **Build Process:** Verify build script generates correct files
2. **File Format:** Verify generated .mdc and .md files are valid
3. **Content:** Verify content is identical across IDEs

### IDE Testing

1. **Cursor Testing:** Load generated rules and commands in Cursor IDE
2. **Windsurf Testing:** Load generated rules and workflows in Windsurf IDE
3. **Equivalence Testing:** Verify both IDEs behave equivalently

## Documentation Requirements

### For Cursor Users

Create `.cursor/README.md`:

- Overview of rules and commands
- How to use rules (always, auto-attached, manual)
- How to use commands (/command-name)
- Troubleshooting
- Limitations vs Windsurf

### For Windsurf Users

Update `.windsurf/README.md`:

- Explain unified format
- Document adapter system
- Explain build process
- Migration guide

### For Developers

Create `docs/IDE_COMPATIBILITY.md`:

- Architecture overview
- Unified format specification
- Transformation rules
- Maintenance procedures
- How to add new rules/commands

## Success Criteria

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

## Resources Provided

### Windsurf Rules (Reference)

All 16 rules in `.windsurf/rules/`:

- `00_core_directives.md` (always_on)
- `01_python_code.md` (glob: *.py)
- `02_testing.md` (glob: *.py)
- `03_documentation.md` (glob: *.md)
- `04_config_files.md` (glob: _.yml,_.yaml, *.toml)
- `05_windsurf_structure.md` (manual)
- `06_security_practices.md` (model_decision)
- `07_context_optimization.md` (model_decision)
- `08_file_operations.md` (model_decision)
- `09_git_workflows.md` (model_decision)
- `10_session_protocols.md` (model_decision)
- `11_error_handling.md` (model_decision)
- `12_task_orchestration.md` (model_decision)
- `13_workflow_routing.md` (model_decision)
- `14_automation_scripts.md` (model_decision)
- `15_tool_patterns.md` (model_decision)

### Windsurf Workflows (Reference)

All 21 workflows in `.windsurf/workflows/`:

- `/work` - Central orchestration
- `/implement` - Feature implementation
- `/plan` - Research and planning
- `/validate` - Quality validation
- `/commit` - Git commit
- `/archive-initiative` - Archive completed work
- `/meta-analysis` - Session analysis
- And 14 more specialized workflows

### Documentation

- `/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility.md` - Initiative overview
- `/docs/research/2025-10-22-cursor-windsurf-research.md` - Comprehensive research
- `/AGENTS.md` - Agent capabilities and configuration
- `/docs/CONSTITUTION.md` - Project principles
- `/docs/DOCUMENTATION_STRUCTURE.md` - Documentation standards

## Getting Started

1. **Review Research:** Read `/docs/research/2025-10-22-cursor-windsurf-research.md` thoroughly
2. **Understand Initiative:** Review `/docs/initiatives/active/2025-10-22-cursor-windsurf-dual-compatibility.md`
3. **Create Directories:** Create `.unified/` and `scripts/adapters/`
4. **Build Adapters:** Implement the adapter system
5. **Test Build:** Verify build process works
6. **Migrate Rules:** Convert Windsurf rules to unified format
7. **Migrate Commands:** Convert Windsurf workflows to unified format
8. **Test Both IDEs:** Verify equivalence
9. **Document:** Create comprehensive documentation
10. **Deploy:** Integrate into CI/CD and release

## Questions to Consider

1. **Glob Patterns:** How to handle complex glob patterns across IDEs?
2. **model_decision Rules:** How to best represent in Cursor (globs vs manual)?
3. **Complex Workflows:** How to simplify multi-stage workflows for Cursor?
4. **Context Embedding:** What context is essential vs optional in commands?
5. **Maintenance:** How to make adding new rules/commands easy for both IDEs?

## Contact & Support

This handoff document contains all necessary context for implementation. Refer to:

- Research document for technical details
- Initiative document for timeline and milestones
- Windsurf rules/workflows for reference implementations

---

**Created:** 2025-10-22
**Status:** Ready for implementation
**Platform:** Cursor IDE
**Duration:** ~8 weeks (60 estimated hours)
**Complexity:** High (infrastructure, dual IDE support, complex transformations)

Good luck! You're building something valuable for the project. 🚀
