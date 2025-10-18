# Phase 5: YAML Frontmatter

**Status:** ⏳ Planned
**Priority:** MEDIUM
**Duration:** 4-6 hours
**Owner:** AI Agent

---

## Objective

Add structured YAML frontmatter metadata to all workflows and rules for improved AI context loading and documentation generation.

**Target:** 100% frontmatter coverage (22 files: 17 workflows + 5 rules)

---

## Background

**Industry Best Practice:** YAML frontmatter provides structured metadata that:

- Improves AI context loading efficiency
- Enables automated documentation generation
- Supports workflow dependency analysis
- Facilitates validation and monitoring

**Research Finding:** YAML 66% more efficient than JSON for LLM context (Decoding AI, 2025)

---

## Tasks

### Task 5.1: Define Frontmatter Schema

**Purpose:** Establish standard schema for all workflow and rule files

**Schema Design:**

```yaml
---
# Core metadata (required for all files)
created: YYYY-MM-DD          # Creation date
updated: YYYY-MM-DD          # Last update date
category: string             # File category
description: string          # One-sentence summary
tokens: number               # Estimated token count

# Workflow-specific (optional)
complexity: number           # Complexity score 0-100
dependencies: [string]       # Required workflows
status: string               # active|deprecated|experimental

# Rule-specific (optional)
applyTo: [string]            # When to apply this rule
priority: string             # high|medium|low
---
```

**Category Values:**

- **Workflows:** orchestrator, planning, implementation, validation, automation, analysis, documentation
- **Rules:** core, testing, language, documentation, security, operations

**Implementation:**

1. Document schema in `docs/DOCUMENTATION_STRUCTURE.md`
2. Create JSON Schema for validation: `.windsurf/schemas/frontmatter-schema.json`
3. Add schema documentation with examples

**Effort:** 1 hour

---

### Task 5.2: Add Frontmatter to All Workflows

**Purpose:** Add metadata to 17 workflow files

**Workflow Frontmatter Template:**

```yaml
---
created: 2025-10-XX
updated: 2025-10-XX
category: [orchestrator|planning|implementation|etc]
complexity: [score 0-100]
description: One-sentence summary
tokens: [estimated count]
dependencies:
  - workflow-name-1
  - workflow-name-2
status: active
---
```

**Target Files (17):**

1. `work.md` - orchestrator
2. `detect-context.md` - orchestrator
3. `plan.md` - planning
4. `research.md` - planning
5. `generate-plan.md` - planning
6. `implement.md` - implementation
7. `validate.md` - validation
8. `commit.md` - validation
9. `bump-version.md` - automation
10. `update-docs.md` - automation
11. `meta-analysis.md` - analysis
12. `extract-session.md` - analysis
13. `summarize-session.md` - analysis
14. `consolidate-summaries.md` - analysis
15. `archive-initiative.md` - documentation
16. `new-adr.md` - documentation
17. `load-context.md` - operations

**Process per File:**

1. Calculate current token count
2. Determine complexity score
3. Identify dependencies
4. Add frontmatter at top of file
5. Update "updated" date

**Example - work.md:**

```yaml
---
created: 2025-10-17
updated: 2025-10-18
category: orchestrator
complexity: 82
description: Central orchestration workflow with intelligent context detection and routing
tokens: 2629
dependencies:
  - detect-context
  - implement
  - plan
  - validate
  - commit
status: active
---
```

**Effort:** 2-3 hours (10-15 min per file)

---

### Task 5.3: Add Frontmatter to All Rules

**Purpose:** Add metadata to 5 rule files

**Rule Frontmatter Template:**

```yaml
---
created: 2025-10-XX
updated: 2025-10-XX
category: [core|testing|language|documentation|security|operations]
description: One-sentence summary
tokens: [estimated count]
applyTo:
  - context-type-1
  - context-type-2
priority: [high|medium|low]
status: active
---
```

**Target Files (5):**

1. `00_agent_directives.md` - core
2. `01_testing_and_tooling.md` - testing
3. `02_python_standards.md` - language
4. `03_documentation_lifecycle.md` - documentation
5. `04_security.md` - security

**Example - 00_agent_directives.md:**

```yaml
---
created: 2025-10-15
updated: 2025-10-18
category: core
description: Core agent persona, principles, and operational mandate
tokens: 5387
applyTo:
  - all
priority: high
status: active
---
```

**Example - 01_testing_and_tooling.md:**

```yaml
---
created: 2025-10-15
updated: 2025-10-18
category: testing
description: Test-driven development practices and quality tooling standards
tokens: 1428
applyTo:
  - testing
  - implementation
priority: high
status: active
---
```

**Effort:** 1 hour

---

### Task 5.4: Create Validation Script

**Purpose:** Automated validation of frontmatter schema compliance

**Script:** `scripts/validate_frontmatter.py`

**Features:**

1. **Schema Validation:**
   - Check all required fields present
   - Verify data types correct
   - Validate enum values (category, status, priority)

2. **Token Count Verification:**
   - Calculate actual token count
   - Compare to frontmatter value
   - Warn if difference >5%

3. **Dependency Validation:**
   - Verify all referenced workflows exist
   - Check for circular dependencies
   - Generate dependency graph

4. **Date Validation:**
   - Verify date format (YYYY-MM-DD)
   - Check updated >= created
   - Warn if updated >30 days old (stale)

**Implementation:**

```python
#!/usr/bin/env python3
"""Validate YAML frontmatter in workflow and rule files."""

import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError

def load_schema():
    """Load JSON schema for frontmatter."""
    schema_path = Path(".windsurf/schemas/frontmatter-schema.json")
    with open(schema_path) as f:
        return json.load(f)

def extract_frontmatter(file_path):
    """Extract YAML frontmatter from markdown file."""
    with open(file_path) as f:
        content = f.read()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])

def validate_file(file_path, schema):
    """Validate single file's frontmatter."""
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        return False, "No frontmatter found"

    try:
        validate(instance=frontmatter, schema=schema)
        return True, "Valid"
    except ValidationError as e:
        return False, str(e)

def main():
    schema = load_schema()
    workflow_dir = Path(".windsurf/workflows")
    rules_dir = Path(".windsurf/rules")

    errors = []
    for file_path in workflow_dir.glob("*.md"):
        valid, msg = validate_file(file_path, schema)
        if not valid:
            errors.append(f"{file_path}: {msg}")

    for file_path in rules_dir.glob("*.md"):
        valid, msg = validate_file(file_path, schema)
        if not valid:
            errors.append(f"{file_path}: {msg}")

    if errors:
        print("Validation errors:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
    else:
        print("All frontmatter valid ✅")

if __name__ == "__main__":
    main()
```

**Effort:** 1-2 hours

---

### Task 5.5: Generate Documentation Indexes

**Purpose:** Auto-generate documentation from frontmatter metadata

**Outputs:**

1. **Workflow Index** (`.windsurf/workflows/INDEX.md`)
   - Table of all workflows with metadata
   - Sorted by category
   - Includes complexity and dependencies

2. **Rule Index** (`.windsurf/rules/INDEX.md`)
   - Table of all rules with metadata
   - Sorted by priority
   - Includes applicability

3. **Dependency Graph** (`.windsurf/workflows/DEPENDENCIES.md`)
   - Visual workflow dependencies
   - Mermaid diagram
   - Circular dependency warnings

**Example - Workflow Index:**

```markdown
# Workflow Index

## Orchestrator Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| work | 82 | 2629 | detect-context, implement, plan | active |
| detect-context | 75 | 3622 | - | active |

## Planning Workflows

| Workflow | Complexity | Tokens | Dependencies | Status |
|----------|------------|--------|--------------|--------|
| plan | 65 | 2293 | research, generate-plan | active |
| research | 55 | 1842 | - | active |

[etc...]
```

**Implementation Script:** `scripts/generate_indexes.py`

**Effort:** 1-2 hours

---

## Success Criteria

### Quantitative Metrics

- ✅ 100% frontmatter coverage (22/22 files)
- ✅ 100% schema compliance (all files pass validation)
- ✅ Token counts accurate (±5% of actual)
- ✅ All indexes generated automatically

### Qualitative Metrics

- ✅ Improved documentation discoverability
- ✅ Easier workflow navigation
- ✅ Better dependency understanding
- ✅ Automated validation catches errors

---

## Validation Steps

1. **Coverage Check:**

   ```bash
   # Count files with frontmatter
   grep -l "^---$" .windsurf/**/*.md | wc -l
   # Expected: 22
   ```

2. **Schema Validation:**

   ```bash
   python scripts/validate_frontmatter.py
   # Expected: All frontmatter valid ✅
   ```

3. **Index Generation:**

   ```bash
   python scripts/generate_indexes.py
   # Expected: 3 index files created
   ```

4. **Manual Review:**
   - Check 3 workflow files for correct metadata
   - Verify dependency graph accurate
   - Confirm indexes readable

---

## Deliverables

- ✅ `.windsurf/schemas/frontmatter-schema.json` - JSON Schema definition
- ✅ All 17 workflows - Updated with frontmatter
- ✅ All 5 rules - Updated with frontmatter
- ✅ `scripts/validate_frontmatter.py` - Validation script
- ✅ `scripts/generate_indexes.py` - Index generation script
- ✅ `.windsurf/workflows/INDEX.md` - Workflow index
- ✅ `.windsurf/rules/INDEX.md` - Rule index
- ✅ `.windsurf/workflows/DEPENDENCIES.md` - Dependency graph
- ✅ Updated `docs/DOCUMENTATION_STRUCTURE.md` - Schema documentation

---

## Dependencies

**Requires:**

- Phase 3-4 complete (file structure stable)

**Enables:**

- Phase 6: Automation (workflows can parse metadata)
- Phase 8: Quality Automation (validation uses schema)

---

## Completion Notes

**Phase 5 Status:** ⏳ Planned, ready after Phase 4

**Next Phase:** Phase 6 (Automation Workflows) - Validate automation

**Estimated Timeline:** Week of 2025-10-28 (4-6 hours)
