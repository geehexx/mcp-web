# Documentation Structure

**Version:** 1.1.0
**Last Updated:** 2025-10-18

This document defines the organization and lifecycle of all documentation in the mcp-web project.

**Related:** [ADR-0018: Workflow Architecture V3](adr/0018-workflow-architecture-v3.md) - Workflow taxonomy and guides vs workflows distinction

---

## Directory Structure

```text
docs/
├── README.md                      # Index and navigation
├── DOCUMENTATION_STRUCTURE.md     # This file
├── CONSTITUTION.md                # Project principles and AI guidelines
├── AGENTS.md                      # Agent catalog and machine-readable specs
│
├── adr/                           # Architecture Decision Records
│   ├── README.md
│   ├── 0001-use-httpx-playwright-fallback.md
│   ├── 0002-adopt-windsurf-workflow-system.md
│   ├── 0018-workflow-architecture-v3.md
│   ├── ... (17 ADRs total)
│   └── template.md
│
├── initiatives/                   # Strategic projects and roadmap
│   ├── README.md
│   ├── template.md                # Legacy flat-file template
│   ├── template/                  # Folder-based template (recommended)
│   │   ├── initiative.md
│   │   ├── phases/
│   │   │   └── phase-example.md
│   │   └── artifacts/
│   │       └── README.md
│   ├── active/                    # Current initiatives (Q4 2025)
│   │   ├── 2025-10-15-quality-foundation/  # Folder-based (large, multi-phase)
│   │   │   ├── initiative.md
│   │   │   └── phases/
│   │   │       ├── phase-1-documentation-structure.md
│   │   │       ├── phase-2-documentation-linting.md
│   │   │       └── ... (6 phases total)
│   │   ├── 2025-10-15-performance-optimization-pipeline/  # Folder-based
│   │   │   ├── initiative.md
│   │   │   ├── phases/
│   │   │   └── artifacts/
│   │   │       └── research-summary.md
│   │   ├── 2025-10-17-windsurf-workflows-v2-optimization/  # Folder-based
│   │   │   ├── initiative.md
│   │   │   └── phases/
│   │   └── 2025-10-18-workflow-architecture/  # Folder-based
│   │       ├── initiative.md
│   │       ├── phases/
│   │       └── artifacts/
│   │           └── workflow-audit.md
│   └── completed/                 # Finished initiatives
│       ├── 2025-10-16-convert-decisions-to-adrs.md
│       ├── 2025-10-16-fix-security-unit-tests.md
│       └── 2025-10-16-windsurf-workflow-rules-improvements.md
│
├── AGENTS.md                      # Agent catalog and machine-readable specs
│
├── guides/                        # Reference guides (NOT workflows)
│   ├── README.md
│   ├── TESTING_REFERENCE.md       # Test command reference
│   ├── TESTING_GUIDE.md           # Comprehensive testing practices
│   ├── LOCAL_LLM_GUIDE.md         # Local LLM provider setup
│   ├── TASKFILE_GUIDE.md          # Task automation reference
│   ├── PERFORMANCE_GUIDE.md       # Performance optimization
│   ├── DEPLOYMENT_GUIDE.md        # Deployment instructions
│   ├── COMMIT_STYLE_GUIDE.md      # Conventional commits
│   ├── DOCUMENTATION_STANDARDS.md # Documentation best practices
│   ├── SUMMARY_STANDARDS.md       # Session summary standards
│   ├── META_ANALYSIS_TRACKING.md  # Meta-analysis workflow
│   └── QUICK_START_WORKFLOWS.md   # Quick start guide
│
├── api/                           # API documentation
│   └── API.md                     # Complete API reference
│
├── architecture/                  # Architecture documentation
│   ├── ARCHITECTURE.md            # System architecture
│   ├── SECURITY_ARCHITECTURE.md   # Security patterns
│   └── diagrams/                  # Architecture diagrams
│
├── reference/                     # Configuration and lookup
│   ├── ENVIRONMENT_VARIABLES.md
│   ├── CONFIGURATION.md
│   ├── ERROR_CODES.md
│   └── CHANGELOG.md
│
└── archive/                       # Historical documents
    ├── README.md
    ├── DECISIONS.md               # Legacy decision log (superseded by ADRs)
    ├── ARCHITECTURE_INITIAL_DESIGN.md  # Initial architecture (superseded)
    └── session-summaries/         # Session summaries (meta-analysis output)
        └── YYYY-MM-DD-*.md

.windsurf/                         # Windsurf AI configuration
├── workflows/                     # Executable workflows (19 workflows)
│   ├── work.md                    # Orchestrator: Master workflow
│   ├── plan.md                    # Orchestrator: Planning
│   ├── implement.md               # Orchestrator: Implementation
│   ├── meta-analysis.md           # Orchestrator: Session end
│   ├── validate.md                # Specialized Operation: Quality gate
│   ├── commit.md                  # Specialized Operation: Git operations
│   ├── detect-context.md          # Context Handler: Project state analysis
│   ├── load-context.md            # Context Handler: Batch loading
│   ├── generate-plan.md           # Artifact Generator: Initiative docs
│   ├── summarize-session.md       # Artifact Generator: Session summaries
│   ├── archive-initiative.md      # Specialized Operation: Archive
│   ├── bump-version.md            # Specialized Operation: Versioning
│   ├── consolidate-summaries.md   # Artifact Generator: Consolidation
│   ├── extract-session.md         # Context Handler: Session extraction
│   ├── new-adr.md                 # Artifact Generator: ADR creation
│   ├── research.md                # Context Handler: Research
│   ├── update-docs.md             # Specialized Operation: Doc updates
│   ├── work-routing.md            # Sub-workflow: Routing logic
│   └── work-session-protocol.md   # Sub-workflow: Session end protocol
│
├── rules/                         # Agent behavior rules (7 rules)
│   ├── 00_agent_directives.md     # Core principles and persona
│   ├── 01_testing_and_tooling.md  # Testing standards
│   ├── 02_python_standards.md     # Code standards
│   ├── 03_documentation_lifecycle.md  # Documentation rules
│   ├── 04_security.md             # Security patterns
│   ├── 05_operational_protocols.md    # Session end, progress communication
│   └── 06_context_engineering.md  # File ops, git ops, context management
│
├── docs/                          # Machine-readable quick-reference documentation
│   ├── README.md                  # Index and guide for machine-readable docs
│   ├── context-loading-patterns.md # Context loading strategies
│   ├── batch-operations.md        # Batch operation optimization
│   ├── common-patterns.md         # Shared code examples and templates
│   ├── tool-patterns.md           # MCP tool usage patterns
│   ├── task-system-reference.md   # Task format specification
│   ├── workflow-routing-matrix.md # Routing decision matrix
│   ├── directory-structure.md     # Directory structure enforcement
│   ├── workflow-index.md          # Auto-generated workflow index
│   ├── rules-index.md             # Auto-generated rule index
│   └── workflow-dependencies.md   # Auto-generated dependency graph
│
├── schemas/                       # Validation schemas
│   └── frontmatter-schema.json    # YAML frontmatter schema
│
└── templates/                     # Code/document templates
```

**Key Distinction:** Workflows (`.windsurf/workflows/`) are **executable**, Guides (`docs/guides/`) are **reference documentation**. See [ADR-0018](adr/0018-workflow-architecture-v3.md) for taxonomy.

---

## Document Types

### 1. Architecture Decision Records (ADRs)

**Purpose:** Document significant architectural decisions with context and consequences.

**Location:** `docs/adr/`

**Format:** Markdown, numbered sequentially (0001-title.md)

**Template:** See `docs/adr/template.md`

**Lifecycle:**

- **Proposed** → **Accepted** → **Implemented**
- ADRs are **immutable** once accepted
- Superseded ADRs reference the new ADR but remain in place
- Never delete ADRs

**Naming Convention:**

- `NNNN-verb-noun-phrase.md`
- Example: `0003-use-structured-prompts.md`

**References:**

- [ADR GitHub](https://adr.github.io/)
- [Joel Parker Henderson's ADR repo](https://github.com/joelparkerhenderson/architecture-decision-record)

### 2. Initiatives

**Purpose:** Track strategic projects, features, and improvements.

**Location:** `docs/initiatives/`

**Subdirectories:**

- `active/` - Current initiatives (Q4 2025, etc.)
- `completed/` - Finished initiatives (archived automatically)

**Format:**

```markdown
# Initiative: [Name]

**Status:** Active | Completed | On Hold
**Start Date:** YYYY-MM-DD
**Target Completion:** YYYY-MM-DD
**Owner:** @username

## Objective
[What we're trying to achieve]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Tasks
- [ ] Task 1
- [ ] Task 2

## Related ADRs
- ADR-0003: Use structured prompts

## Updates
### 2025-10-15
Progress update...
```

**Lifecycle:**

- Active initiatives reviewed weekly/monthly
- Completed initiatives moved to `completed/` with completion date
- On-hold initiatives documented with reason and review date

### 3. Reference Guides

**Purpose:** Quick reference documentation for commands, patterns, and tools. **NOT executable workflows.**

**Location:** `docs/guides/`

**Critical Distinction (ADR-0018):**

| Aspect | Reference Guide | Workflow |
|--------|----------------|----------|
| **Purpose** | Documentation | Execution |
| **Content** | Commands, examples | Orchestration logic |
| **Invocation** | Read by humans/AI | Called by workflows |
| **Location** | `docs/guides/` | `.windsurf/workflows/` |

**Example:**

- ❓ "What test commands can I run?" → **Read** `docs/guides/TESTING_REFERENCE.md`
- ✅ "Run validation before commit" → **Call** `/validate` workflow

**Types:**

- Command reference (git, pytest, docker)
- Pattern catalogs (design patterns, code templates)
- Tool usage examples (debugging, profiling)
- Configuration reference (environment variables, settings)

**Format:**

- YAML frontmatter with `category: Reference Documentation`
- Clear command examples with syntax
- Links to related executable workflows
- Troubleshooting sections

### 4. Workflows

**Purpose:** Executable AI agent workflows for orchestration, operations, and content generation.

**Location:** `.windsurf/workflows/`

**Decision:** [ADR-0018: Workflow Architecture V3](adr/0018-workflow-architecture-v3.md)

**5-Category Taxonomy:**

1. **Orchestrators** (4 workflows) - High-level coordination
   - `/work` - Master orchestrator (context detection + routing)
   - `/plan` - Planning orchestrator (research → generate-plan → implement)
   - `/implement` - Implementation orchestrator (test-first, incremental)
   - `/meta-analysis` - Session end orchestrator (extract → summarize → update-docs)

2. **Specialized Operations** (5 workflows) - Atomic focused tasks
   - `/validate` - Quality gate (lint + test + security)
   - `/commit` - Git operations + validation
   - `/bump-version` - Semantic versioning from conventional commits
   - `/update-docs` - Sync PROJECT_SUMMARY + CHANGELOG
   - `/archive-initiative` - Archive completed initiatives

3. **Context Handlers** (3 workflows) - Information gathering
   - `/detect-context` - Project state analysis for routing
   - `/load-context` - Batch context loading (3-10x faster)
   - `/extract-session` - Extract structured session data

4. **Artifact Generators** (4 workflows) - Content creation
   - `/generate-plan` - Transform research → initiative document
   - `/summarize-session` - Generate formatted session summary
   - `/new-adr` - ADR creation with research
   - `/consolidate-summaries` - Consolidate daily summaries

5. **Reference Guides** - NOT workflows, moved to `docs/guides/`
   - Command reference documentation only
   - Example: `docs/guides/TESTING_REFERENCE.md`

**Workflow Frontmatter:**

```yaml
---
description: Brief workflow description
auto_execution_mode: 2|3
category: Orchestrator|Specialized Operation|Context Handler|Artifact Generator
---
```

**Standard Tool Patterns:**

- Batch file reads: `mcp0_read_multiple_files([paths])` for 3+ files
- Git operations: `run_command("git [cmd]", cwd=root, blocking=true)`
- Tests: `run_command("task test:*", cwd=root, blocking=true)`

**See:** [ADR-0018](adr/0018-workflow-architecture-v3.md) for complete taxonomy, decision tree, and tool standards.

### 5. API Documentation

**Purpose:** Technical reference for modules and functions.

**Location:** `docs/api/`

**Source:** Generated from code docstrings + manual curation

**Update Trigger:** Any API change requires doc update (enforced by CI)

### 5. Architecture Documentation

**Purpose:** System design, patterns, and principles.

**Location:** `docs/architecture/`

**Contents:**

- High-level architecture diagrams
- Component interactions
- Design patterns used
- Security architecture

**Update Frequency:** Quarterly review or after major changes

### 6. Reference Documentation

**Purpose:** Quick lookup information.

**Location:** `docs/reference/`

**Contents:**

- Environment variables
- Configuration options
- Error codes and messages
- CLI commands

**Maintenance:** Keep up-to-date with code changes

### 7. Archive

**Purpose:** Historical documents no longer actively used.

**Location:** `docs/archive/`

**Triggers for Archiving:**

- Document superseded by newer version
- Initiative completed (after 6 months)
- Temporary documents no longer relevant
- Old roadmaps/plans

**Process:**

1. Add "ARCHIVED" notice at top with date and reason
2. Link to replacement document if applicable
3. Move to `docs/archive/`
4. Update any referring documents

---

## YAML Frontmatter Schema

**Purpose:** Structured metadata for AI-optimized documentation discovery and indexing.

**Applies to:** All documentation files (workflows, rules, ADRs, guides, initiatives)

### Standard Schema

**Required fields:**

```yaml
---
# Core metadata (all documents)
title: "Document Title"
type: "guide|adr|initiative|workflow|rule|api|architecture|reference"
status: "draft|active|completed|deprecated|superseded"

# Discovery metadata
description: "One-sentence description for quick context"
tags: ["tag1", "tag2", "tag3"]
---
```

**Optional fields:**

```yaml
---
# Relationships
related:
  - "/docs/path/to/related-doc.md"
  - "/docs/adr/0012-decision.md"

# Workflow-specific
auto_execution_mode: 3  # Windsurf workflow execution mode

# Context hints
audience: "developer|ai-agent|both"
token_budget: "low|medium|high"
complexity: "simple|moderate|complex"

# Timestamps (ONLY on creation, never updated)
created: "2025-10-15"

# ADR-specific
supersedes: "0012-old-decision.md"
superseded_by: "0015-new-decision.md"
decision_date: "2025-10-15"

# Initiative-specific
priority: "low|medium|high|critical"
owner: "@username"
start_date: "2025-10-15"
target_date: "2025-11-15"
estimated_hours: 20
---
```

### Field Definitions

| Field | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `title` | string | Yes | Any | Human-readable title |
| `type` | string | Yes | guide\|adr\|initiative\|workflow\|rule\|api\|architecture\|reference | Document type |
| `status` | string | Yes | draft\|active\|completed\|deprecated\|superseded | Current status |
| `description` | string | Yes | Any | One-sentence summary |
| `tags` | array | Yes | Any | Keywords for search |
| `related` | array | No | Paths | Related documents |
| `audience` | string | No | developer\|ai-agent\|both | Target audience |
| `token_budget` | string | No | low\|medium\|high | Context loading hint |
| `complexity` | string | No | simple\|moderate\|complex | Difficulty level |
| `created` | string | No | YYYY-MM-DD | Creation date (never update) |
| `priority` | string | No | low\|medium\|high\|critical | Initiative priority |
| `owner` | string | No | @username | Responsible person |

### Examples by Document Type

**Workflow:**

```yaml
---
title: "Bump Version Workflow"
type: "workflow"
status: "active"
description: "Auto-bump version based on conventional commits"
tags: ["versioning", "automation", "git"]
related:
  - "/docs/reference/CHANGELOG.md"
  - "/.windsurf/workflows/commit.md"
audience: "ai-agent"
token_budget: "medium"
complexity: "moderate"
auto_execution_mode: 3
created: "2025-10-18"
---
```

**ADR:**

```yaml
---
title: "Use Structured LLM Prompts"
type: "adr"
status: "accepted"
description: "Adopt structured prompt format for all LLM interactions"
tags: ["llm", "prompts", "security"]
related:
  - "/docs/adr/0002-adopt-windsurf-workflow-system.md"
  - "/docs/architecture/SECURITY_ARCHITECTURE.md"
audience: "both"
token_budget: "high"
complexity: "complex"
created: "2025-09-20"
decision_date: "2025-09-25"
---
```

**Initiative:**

```yaml
---
title: "Windsurf Workflows v2 Optimization"
type: "initiative"
status: "active"
description: "Optimize workflows for 30-50% token reduction"
tags: ["optimization", "workflows", "efficiency"]
priority: "high"
owner: "@ai-agent"
start_date: "2025-10-17"
target_date: "2025-11-15"
estimated_hours: 35
related:
  - "/docs/adr/0002-adopt-windsurf-workflow-system.md"
audience: "ai-agent"
token_budget: "high"
complexity: "complex"
created: "2025-10-17"
---
```

**Guide:**

```yaml
---
title: "Testing Guide"
type: "guide"
status: "active"
description: "Comprehensive guide to testing practices and tools"
tags: ["testing", "pytest", "tdd"]
related:
  - "/.windsurf/rules/01_testing_and_tooling.md"
  - "/.windsurf/workflows/run-tests.md"
audience: "developer"
token_budget: "high"
complexity: "moderate"
created: "2025-09-15"
---
```

**Rule:**

```yaml
---
title: "Testing and Tooling Standards"
type: "rule"
status: "active"
description: "Testing principles, tool selection, and TDD workflow"
tags: ["testing", "pytest", "tdd", "standards"]
related:
  - "/.windsurf/workflows/run-tests.md"
  - "/docs/guides/TESTING_GUIDE.md"
audience: "ai-agent"
token_budget: "medium"
complexity: "moderate"
created: "2025-09-10"
---
```

### Validation

**Frontmatter validation script:**

```bash
# Validate all documentation frontmatter
task docs:validate-frontmatter

# Check for required fields
# Verify valid values for enums
# Report missing frontmatter
```

**Required checks:**

- All required fields present
- Valid enum values (type, status, audience, etc.)
- Valid date format (YYYY-MM-DD)
- Related paths exist
- No duplicate tags

### Migration Strategy

**Phase 1: Add to new documents** (immediate)

- All new workflows, rules, ADRs, initiatives must include frontmatter

**Phase 2: Backfill existing documents** (Initiative Phase 5)

- Add frontmatter to all existing workflows (9 files)
- Add frontmatter to all existing rules (5 files)
- Add frontmatter to all existing ADRs (17 files)
- Add frontmatter to all guides and reference docs

**Phase 3: Validation enforcement** (Initiative Phase 6)

- Add pre-commit hook to validate frontmatter
- CI check for valid frontmatter
- Reject commits with invalid or missing frontmatter

### AI Agent Usage

**Discovery pattern:**

```markdown
AI Agent: "I need to find documentation about testing"
→ Search frontmatter: tags contains "testing"
→ Results:
  - Testing Guide (type: guide, complexity: moderate)
  - Testing Rules (type: rule, token_budget: medium)
  - Run Tests Workflow (type: workflow, complexity: simple)
→ Load by priority: Rules first (principles), then Guide (how-to), then Workflow (commands)
```

**Token budget optimization:**

```markdown
AI Agent: Limited context window
→ Filter by token_budget: "low" or "medium"
→ Load essential context only
→ Defer "high" token_budget docs until needed
```

**Relationship traversal:**

```markdown
AI Agent: Reading ADR-0013 (Testing Strategy)
→ Check frontmatter.related
→ Find: testing-guide.md, run-tests.md
→ Load related docs for complete context
```

### Benefits

**For AI Agents:**

- Structured search by type, tags, complexity
- Token budget hints for context optimization
- Relationship traversal for complete context
- Quick relevance assessment via description

**For Developers:**

- Consistent metadata across all docs
- Easy filtering and discovery
- Clear document relationships
- Status and priority visibility

**For Automation:**

- Validation and linting
- Auto-generation of doc indexes
- Dependency graph generation
- Stale document detection

---

## Documentation Maintenance

### Update Triggers

| Trigger | Documents to Update | Frequency |
|---------|-------------------|-----------|
| New feature | ADR, API docs, guides | Per feature |
| Bug fix | Guides if user-facing | As needed |
| Config change | Reference docs | Immediately |
| Architecture change | Architecture docs, ADR | Per change |
| Release | CHANGELOG, version refs | Per release |
| Quarterly review | All active docs | Quarterly |

### Quality Standards

**All documentation must:**

- Pass markdown linting (markdownlint-cli2)
- Have no double-spaces or LLM artifacts
- Include last updated date
- Link to related documentation
- Reference external sources when applicable

**Enforced by:**

- Pre-commit hooks
- CI/CD pipeline
- Documentation linter tasks

### Review Schedule

| Document Type | Review Frequency |
|--------------|-----------------|
| ADRs | Immutable (no review) |
| Active initiatives | Weekly |
| Guides | Quarterly |
| API docs | On code change |
| Architecture | Quarterly |
| Reference | On code change |

---

## Tool Integration

### Linting Tools

**Documentation Linting:**

- Tool: `markdownlint-cli2`
- Config: `.markdownlint.json`
- Rules: MD001-MD048 (standard rules)

**Python Docstrings:**

- Tool: `pydocstyle` or `darglint`
- Style: Google docstring format
- Enforced by: pre-commit and CI

### Task Commands

```bash
# Lint all documentation
task docs:lint

# Lint markdown structure
task docs:lint:markdown

# Fix auto-fixable issues
task docs:fix

# Generate API docs
task docs:generate

# Serve docs locally
task docs:serve
```

---

## Contribution Guidelines

### Creating New Documents

1. **Determine document type** (ADR, guide, reference, etc.)
2. **Use appropriate template** from `docs/templates/`
3. **Follow naming conventions** (see above)
4. **Add to index** (`docs/README.md`)
5. **Run linters** before committing
6. **Link from related documents**

### Updating Existing Documents

1. **Check if document is in archive** (if so, create new version)
2. **Update "Last Updated" date** at top
3. **Run linters** after changes
4. **Update related documents** if necessary
5. **Add changelog entry** for significant changes

### Archiving Documents

1. **Add ARCHIVED notice** at top:

 ```markdown
 > **⚠️ ARCHIVED:** This document was archived on YYYY-MM-DD.
 > Reason: [superseded by / no longer relevant / initiative completed]
 > See [replacement.md] for current information.
```

1. **Move to `docs/archive/`**
2. **Update referring documents**
3. **Add entry to archive README**

---

## Migration from Current State

### Phase 1: Restructure (Immediate)

- [x] Create directory structure
- [ ] Move existing docs to appropriate locations
- [ ] Convert DECISIONS.md to ADR format
- [ ] Create initiative for Q4 2025
- [ ] Archive old improvement docs

### Phase 2: Tooling (Week 1)

- [ ] Install markdownlint-cli2
- [ ] Install markdownlint-cli2
- [ ] Create linting configs
- [ ] Add Task commands
- [ ] Add pre-commit hooks

### Phase 3: Content (Week 2)

- [ ] Write missing API docs
- [ ] Create testing guide
- [ ] Expand architecture docs
- [ ] Clean up redundancy
- [ ] Remove LLM artifacts

### Phase 4: Automation (Week 3)

- [ ] CI/CD integration
- [ ] Auto-generate API docs
- [ ] Documentation coverage checks
- [ ] Link checking automation

---

## Best Practices

### ADR Best Practices

From [adr.github.io](https://adr.github.io/):

1. **One ADR per decision** - Keep focused
2. **Immutable** - Don't edit after acceptance
3. **Include context** - Why was this needed?
4. **List alternatives** - What else was considered?
5. **Document consequences** - What are the implications?

### Writing Style

Follow [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/):

- Use active voice
- Use present tense
- Be concise
- Use inclusive language
- Avoid jargon (or define it)

### Link Strategy

- **Internal links:** Relative paths (`../adr/0001-decision.md`)
- **External links:** Full URLs with context
- **Code references:** Use backticks (\`config.py\`)
- **Check links:** Use automated link checker in CI

---

## References

### External Standards

- [Architecture Decision Records (ADR)](https://adr.github.io/)
- [Divio Documentation System](https://documentation.divio.com/)
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style/)
- [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/)

### Tools

- [markdownlint](https://github.com/DavidAnson/markdownlint)
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)
- [MkDocs](https://www.mkdocs.org/) (potential future use)

---

## Questions and Answers

**Q: Where do TODOs go?**
A: In `docs/initiatives/active/` as tasks within an initiative.

**Q: Where do feature requests go?**
A: GitHub Issues → Initiative (if approved) → ADR (if architectural) → Implementation

**Q: How long do documents stay in archive?**
A: Indefinitely, but reviewed annually for permanent deletion candidates.

**Q: What if a document doesn't fit a category?**
A: Create `docs/misc/` temporarily, but periodically review and categorize.

**Q: How do we handle API docs from code?**
A: Generate from docstrings + manual curation in `docs/api/`.

---

**Maintained by:** mcp-web core team
**Questions:** Open GitHub issue with "docs:" prefix
