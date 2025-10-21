# Windsurf Rules System Design

**Date:** 2025-10-21
**Purpose:** Complete redesign specification

---

## Phase 2: Design New Structure

### 2.1 Optimal Trigger Assignment Strategy

Based on verified Windsurf specification and usage analysis:

#### Always-On Triggers (1 rule, <3KB)

**Purpose:** Core directives that apply to ALL work

| Rule | Content | Rationale |
|------|---------|-----------|
| `00_core_directives.md` | Agent persona, guiding principles, tool selection, operational mandate (trimmed) | Must be loaded always; keep minimal |

**Token budget:** ~3,000 tokens max (always loaded)

#### Model Decision Triggers (8 rules, ~16KB)

**Purpose:** Specialized knowledge loaded when semantically relevant

| Rule | Description | Topics | Estimated Tokens |
|------|-------------|--------|------------------|
| `05_security_practices.md` | Apply when dealing with security-sensitive code including API calls, user input, LLM interactions, authentication | OWASP LLM Top 10, input validation, auth patterns | ~2,500 |
| `06_context_optimization.md` | Apply for context loading, batch operations, or performance optimization work | Batch ops, context patterns, parallelization | ~2,500 |
| `07_file_operations.md` | Apply when moving, archiving, or reorganizing files and updating cross-references | File moves, initiative archival, ref updates | ~2,000 |
| `08_git_workflows.md` | Apply for git operations, commits, branching, or version control work | Git best practices, conventional commits, branching | ~1,800 |
| `09_session_protocols.md` | Apply at session end, when completing work, or managing work transitions | Session end protocol, progress communication | ~2,000 |
| `10_error_handling.md` | Apply when handling errors, implementing error recovery, or debugging failures | Error patterns, recovery strategies, debugging | ~2,200 |
| `11_task_orchestration.md` | Apply when using update_plan, creating task lists, or orchestrating multi-step workflows | update_plan usage, task attribution, hierarchical tasks | ~3,000 |
| `12_workflow_routing.md` | Apply when routing work, making workflow decisions, or detecting project context | Routing matrix, signal detection, confidence levels | ~1,800 |

**Total:** ~17,800 tokens

#### Glob Triggers (5 rules, ~8KB)

**Purpose:** File-type specific rules, automatically loaded

| Rule | Globs | Topics | Estimated Tokens |
|------|-------|--------|------------------|
| `01_python_code.md` | _.py, **/_.py | Python style, type hints, async/await, best practices | ~2,200 |
| `02_testing.md` | tests/**/_.py, test__.py, *_test.py, conftest.py | Testing standards, pytest, fixtures, TDD | ~1,800 |
| `03_documentation.md` | docs/**/_.md,_.md, README.md | Documentation standards, markdown, ADRs, initiatives | ~2,000 |
| `04_config_files.md` | _.toml,_.ini, _.yml,_.yaml, Taskfile.yml, .pre-commit-config.yaml | Config best practices, TOML/YAML syntax, Taskfile patterns | ~1,500 |
| `13_windsurf_structure.md` | .windsurf/**/*.md, .windsurf/**/*.json | `.windsurf/` directory structure, workflow/rule format, frontmatter | ~1,200 |

**Total:** ~8,700 tokens

#### Manual Triggers (4 rules, ~14KB)

**Purpose:** Reference material, loaded only when explicitly mentioned

| Rule | Content | Estimated Tokens |
|------|---------|------------------|
| `14_automation_reference.md` | Automation scripts, Taskfile commands, scaffolding, batch operations | ~3,500 |
| `15_tool_usage_patterns.md` | Tool calling patterns, MCP usage, grep/read/edit best practices | ~3,800 |
| `16_task_system_reference.md` | Detailed task system reference, format specifications, examples | ~3,500 |
| `17_batch_optimization.md` | Performance patterns, chunking strategies, rate limiting | ~3,200 |

**Total:** ~14,000 tokens

---

### 2.2 Content Reorganization Plan

#### New Rule: 00_core_directives.md (always_on, ~3KB)

**Trim from current `00_agent_directives.md` (12.9KB → 3KB):**

**KEEP:**

- Section 1: Persona (200 words)
- Section 2: Guiding Principles (400 words - top 5 only)
- Section 3: Operational Mandate (300 words)
- Section 4: Tool Selection (200 words - top 5 tools)
- Quick navigation to specialized rules

**MOVE TO MANUAL RULE:**

- Section 5: Research Standards → `15_tool_usage_patterns.md`
- Section 6: File Operations → `07_file_operations.md`
- Section 7: Git Operations → `08_git_workflows.md`
- Section 8: Session End Protocol → `09_session_protocols.md`
- Section 9: Progress Communication → `09_session_protocols.md`
- Section 10: Operational Efficiency → `06_context_optimization.md`
- Section 11: Task System → `11_task_orchestration.md`

**Result:** Core directives only, <3KB

#### Consolidated Rule: 06_context_optimization.md (model_decision, ~2.5KB)

**Merge content from:**

- `batch-operations.md` (6.3KB) - Optimization patterns
- `context-loading-patterns.md` (7.0KB) - Loading strategies
- Parts of `tool-patterns.md` - Context-related tool usage
- Parts of `06_context_engineering.md` - Context optimization

**Focus:**

- When to batch (3+ items)
- Optimal batch sizes (10-15 files)
- Pattern examples (parallel reads, chunking, rate limiting)
- MCP tool batching

**Drop:**

- Detailed code examples (keep in manual reference)
- Edge cases (move to `17_batch_optimization.md`)

#### Consolidated Rule: 07_file_operations.md (model_decision, ~2KB)

**Merge content from:**

- Parts of `06_context_engineering.md` - File operations section
- `automation-scripts.md` - File operations commands
- `directory-structure.md` - Directory structure rules

**Focus:**

- File move + ref update patterns
- Initiative archival process
- Index regeneration
- Directory structure enforcement

#### Consolidated Rule: 11_task_orchestration.md (model_decision, ~3KB)

**Trim from `07_task_system.md` (29.1KB → 3KB):**

**KEEP:**

- Purpose and tool (`update_plan`)
- When required (3+ steps, >5 min)
- Required format (`/<workflow> - <description>`)
- Core rules (attribution, one active, preserve history)
- 3-5 key examples

**MOVE TO `16_task_system_reference.md` (manual):**

- Detailed format specification
- Complete examples library
- Edge cases
- Troubleshooting
- Anti-patterns (keep 2-3 top ones)

#### New Rule: 12_workflow_routing.md (model_decision, ~1.8KB)

**Merge content from:**

- `workflow-routing-matrix.md` - Routing decisions
- Parts of workflows (routing logic)

**Focus:**

- Confidence levels (High 80%+, Medium 30-79%, Low <30%)
- Signal priority matrix (5-8 key scenarios)
- Decision tree (simplified)
- Quick reference table

#### Split Python Rules

**Current:** `02_python_standards.md` (10.1KB, glob: **/*.py)

**Split into:**

1. `01_python_code.md` (glob: **/*.py, ~2.2KB) - Code style, type hints, async
2. `02_testing.md` (glob: tests/**/*.py, ~1.8KB) - Testing standards

**Rationale:** Testing is frequent enough to warrant separate glob

#### New Config Rule

**Current:** Config standards scattered across multiple rules

**Create:** `04_config_files.md` (glob: _.toml,_.ini, _.yml,_.yaml)

**Content:**

- TOML best practices (pyproject.toml)
- YAML pitfalls
- Taskfile patterns
- Pre-commit config

#### Elevate Windsurf Structure

**Current:** `directory-structure.md` (5.7KB doc)

**Create:** `13_windsurf_structure.md` (glob: .windsurf/**/*.md)

**Content:**

- `.windsurf/` directory structure
- Workflow frontmatter format
- Rule frontmatter format
- Forbidden files/locations

**Rationale:** Enforces structure when editing Windsurf files

---

### 2.3 Metadata Preservation Format

**Windsurf frontmatter (top):**

```yaml
---
trigger: model_decision
description: Apply when dealing with security-sensitive code including API calls user input LLM interactions and authentication
---
```

**Post-matter (bottom, after main content):**

```markdown
---

## Rule Metadata

**File:** `04_security.md`
**Category:** Security
**Trigger:** model_decision
**Estimated Tokens:** ~2,500
**Last Updated:** 2025-10-21
**Status:** Active

**Topics Covered:**
- OWASP LLM Top 10 (2025)
- Input validation and sanitization
- Authentication and authorization patterns
- Secure API design
- LLM interaction security

**Dependencies:**
- Referenced by workflows: `/implement`, `/validate`, `/plan`, `/research`
- References: OWASP documentation, security best practices

**Changelog:**
- 2025-10-21: Restructured frontmatter for Windsurf compatibility
- 2025-10-19: Added OWASP LLM Top 10 examples
- 2025-10-15: Initial creation

**Maintenance Notes:**
- Update when OWASP LLM Top 10 changes
- Review quarterly for new security patterns
- Keep examples current with project code
```

**Benefits:**

- ✅ Windsurf frontmatter clean and compliant
- ✅ All tracking metadata preserved
- ✅ Human-readable
- ✅ Won't interfere with Windsurf parser
- ✅ Easy to update

---

### 2.4 Renumbering Scheme

**New numbering (18 rules):**

```
00-00: always_on (1)
├─ 00_core_directives.md

01-04: glob (5)
├─ 01_python_code.md (glob: *.py)
├─ 02_testing.md (glob: tests/**/*.py)
├─ 03_documentation.md (glob: docs/**/*.md, *.md)
├─ 04_config_files.md (glob: *.toml, *.ini, *.yml)
└─ 13_windsurf_structure.md (glob: .windsurf/**/*.md)

05-12: model_decision (8)
├─ 05_security_practices.md
├─ 06_context_optimization.md
├─ 07_file_operations.md
├─ 08_git_workflows.md
├─ 09_session_protocols.md
├─ 10_error_handling.md
├─ 11_task_orchestration.md
└─ 12_workflow_routing.md

14-17: manual (4)
├─ 14_automation_reference.md
├─ 15_tool_usage_patterns.md
├─ 16_task_system_reference.md
└─ 17_batch_optimization.md
```

**Note:** `13_windsurf_structure.md` is out of sequence (glob trigger) for logical grouping

---

### 2.5 Glob Format Examples

**Correct format (unquoted, comma-separated):**

```yaml
---
trigger: glob
globs: *.py, **/*.py, src/**/*.py
---
```

**Multiple file types:**

```yaml
---
trigger: glob
globs: *.toml, *.ini, *.yml, *.yaml, Taskfile.yml
---
```

**Test files:**

```yaml
---
trigger: glob
globs: tests/**/*.py, test_*.py, *_test.py, conftest.py
---
```

**Documentation:**

```yaml
---
trigger: glob
globs: docs/**/*.md, *.md, README.md
---
```

---

### 2.6 Model Decision Descriptions

**Best practices for descriptions:**

1. **Start with "Apply when"** - Makes semantic matching easier
2. **Include key trigger words** - Security, testing, context, git, etc.
3. **Be specific but not too narrow** - Balance precision with coverage
4. **No apostrophes** - Windsurf parsing issue
5. **Max 200 characters** - Brevity helps model decision

**Examples:**

✅ **Good:**

```yaml
description: Apply when dealing with security-sensitive code including API calls user input LLM interactions and authentication
```

✅ **Good:**

```yaml
description: Apply for context loading batch operations or performance optimization work
```

❌ **Bad (too vague):**

```yaml
description: Security stuff
```

❌ **Bad (has apostrophe):**

```yaml
description: Apply when working with the project's security features
```

---

## Phase 2 Summary

**New structure:**

- 18 rules total (down from 8 rules + 15 docs)
- 1 always_on (~3KB)
- 5 glob triggers (~9KB)
- 8 model_decision (~18KB)
- 4 manual (~14KB)
- **Total: ~44KB, ~30,000 tokens** (down from ~56KB, 40,000 tokens)

**Key improvements:**

1. ✅ All frontmatter Windsurf-compliant
2. ✅ Globs correctly formatted (unquoted)
3. ✅ No excessive metadata in frontmatter
4. ✅ All rules <12KB (within Windsurf limit)
5. ✅ Metadata preserved in post-matter
6. ✅ Logical trigger assignments
7. ✅ Optimized token usage

**Next:** Phase 3 - Implementation Plan
