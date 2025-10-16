# Documentation Structure

**Version:** 1.0.0
**Last Updated:** 2025-10-15

This document defines the organization and lifecycle of all documentation in the mcp-web project.

---

## Directory Structure

```text
docs/
├── README.md # Index and navigation
├── DOCUMENTATION_STRUCTURE.md # This file
├── CONSTITUTION.md # Project principles and AI guidelines
│
├── adr/ # Architecture Decision Records
│ ├── README.md
│ ├── 0001-httpx-playwright-fallback.md
│ ├── 0002-trafilatura-extraction.md
│ └── template.md
│
├── initiatives/ # Active initiatives and roadmap
│ ├── README.md
│ ├── active/ # Current initiatives
│ │ └── 2025-q4-security-hardening.md
│ └── completed/ # Completed initiatives (archive)
│ └── 2025-q3-local-llm-support.md
│
├── guides/ # How-to guides
│ ├── LOCAL_LLM_GUIDE.md
│ ├── TASKFILE_GUIDE.md
│ ├── TESTING_GUIDE.md
│ └── CONTRIBUTING.md
│
├── api/ # API documentation
│ ├── README.md
│ ├── fetcher.md
│ ├── extractor.md
│ ├── chunker.md
│ ├── summarizer.md
│ └── security.md
│
├── architecture/ # Architecture documentation
│ ├── ARCHITECTURE.md # System architecture
│ ├── SECURITY_ARCHITECTURE.md
│ └── diagrams/
│
├── reference/ # Reference documentation
│ ├── ENVIRONMENT_VARIABLES.md
│ ├── CONFIGURATION.md
│ ├── ERROR_CODES.md
│ └── CHANGELOG.md
│
└── archive/ # Historical documents
 ├── README.md
 ├── IMPROVEMENTS_V1.md
 └── IMPROVEMENTS_V2.md
```

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

### 3. Guides

**Purpose:** Step-by-step instructions for specific tasks.

**Location:** `docs/guides/`

**Types:**

- User guides (installation, configuration, usage)
- Developer guides (contributing, testing, debugging)
- Operational guides (deployment, monitoring)

**Format:**

- Clear headings
- Code examples
- Troubleshooting sections
- Links to related docs

### 4. API Documentation

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

- Pass markdown linting (markdownlint)
- Pass prose linting (Vale with project style)
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

**Markdown Structure:**

- Tool: `markdownlint-cli2`
- Config: `.markdownlint.json`
- Rules: MD001-MD048 (standard rules)

**Prose Quality:**

- Tool: `Vale`
- Config: `.vale.ini`
- Styles: Microsoft, Google, custom mcp-web style

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

# Lint prose quality
task docs:lint:prose

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
- [ ] Install Vale
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
- [Vale](https://vale.sh/)
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
