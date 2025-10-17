# ADR-0003: Documentation Standards and Structure

**Status:** Implemented
**Date:** 2025-10-15
**Deciders:** Core Team
**Related:** DOCUMENTATION_STRUCTURE.md, CONSTITUTION.md

---

## Context

The mcp-web project accumulated documentation organically, resulting in:

- **Inconsistent structure:** Documents placed ad-hoc without clear organization
- **No lifecycle management:** No clear process for archiving historical docs
- **Poor discoverability:** Hard to find relevant information
- **Quality variance:** No standards for formatting, style, or completeness
- **AI-unfriendly:** Lacked structure for efficient AI agent consumption
- **Missing decision records:** Architectural decisions not systematically documented

**Specific Problems:**

- Session summaries in root directory (polluting workspace)
- Improvement documents with no clear archival strategy
- Decisions in single `DECISIONS.md` file (not scalable)
- No clear distinction between active vs historical documentation
- Double-spaces and LLM artifacts in documentation
- No prose quality checking

**Key Requirements:**

- Clear organizational hierarchy
- Sustainable documentation lifecycle
- AI-optimized structure and formatting
- Automated quality enforcement
- Support for multiple document types (ADRs, initiatives, guides, etc.)

---

## Decision

We will adopt a hierarchical, lifecycle-managed documentation structure based on industry best practices (Divio Documentation System, Docs as Code, ADR methodology):

### Directory Structure

```text
docs/
├── standards/ # Documentation standards and style guides
│ ├── DOCUMENTATION_STANDARDS.md
│ ├── COMMIT_STYLE_GUIDE.md
│ ├── SUMMARY_STANDARDS.md
│ └── META_ANALYSIS_TRACKING.md
├── adr/ # Architecture Decision Records (immutable)
│ ├── README.md
│ ├── template.md
│ └── NNNN-verb-noun-phrase.md
├── initiatives/ # Project initiatives
│ ├── active/ # Current work
│ └── completed/ # Archived initiatives
├── guides/ # How-to guides
│ ├── QUICK_START_WORKFLOWS.md
│ └── [topic]-GUIDE.md
├── api/ # API documentation
├── architecture/ # Architecture docs & diagrams
├── reference/ # Reference documentation
├── archive/ # Historical documentation
│ └── session-summaries/ # AI agent session summaries
├── ARCHITECTURE.md # System architecture overview
├── API.md # API documentation
├── TESTING.md # Testing strategy
├── PROJECT_SUMMARY.md # High-level project summary
├── DOCUMENTATION_STRUCTURE.md
└── CONSTITUTION.md # Project principles
```

### Document Types and Standards

1. **Architecture Decision Records (ADRs)**

- Template-based (Status, Context, Decision, Alternatives, Consequences)
- Numbered sequentially (0001, 0002, ...)
- Immutable once accepted
- Clear lifecycle: Proposed → Accepted → Implemented

1. **Initiatives**

- Track multi-session projects
- Clear success criteria
- Active vs completed separation
- Regular updates with timestamps

1. **Session Summaries**

- Location: `docs/archive/session-summaries/`
- Naming: `YYYY-MM-DD-descriptive-name.md`
- Standard structure (objectives, accomplishments, commits, next steps)

1. **Standards/Guides**

- Location: `docs/standards/` or `docs/guides/`
- SCREAMING_SNAKE_CASE naming
- Comprehensive, actionable content

### Quality Standards

**Automated Enforcement:**

- Markdown linting (markdownlint-cli2)
- Documentation linting (markdownlint + Microsoft Writing Style Guide)
- Pre-commit hooks
- CI/CD validation

**Manual Standards:**

- No double-spaces
- No LLM artifacts
- External references with URLs
- Last updated dates
- Clear headings hierarchy

### Lifecycle Management

**Archival Triggers:**

- Initiative completed (→ `initiatives/completed/`)
- Document superseded (→ `docs/archive/`)
- Session summary (→ `docs/archive/session-summaries/`)
- Historical reference (→ `docs/archive/`)

**Update Triggers:**

| Trigger | Update | Frequency |
|---------|--------|-----------|
| New feature | ADR, API docs, guides | Per feature |
| Config change | Reference docs | Immediately |
| Architecture change | Architecture docs, ADR | Per change |
| Quarterly review | All active docs | Quarterly |

---

## Alternatives Considered

### Alternative 1: Flat Structure

**Approach:** All docs in `docs/` with prefixes (ADR-, GUIDE-, etc.)

**Pros:**

- Simple
- No subdirectories
- Easy to browse

**Cons:**

- **❌ Poor scalability:** Becomes cluttered with many docs
- **❌ No semantic separation:** Active vs archived mixed
- **❌ Hard to discover:** No clear categorization
- **❌ Lifecycle unclear:** No obvious archival location

**Rejected because:** Not scalable, poor organization

### Alternative 2: Wiki/External System

**Approach:** Use GitHub Wiki, Confluence, Notion, etc.

**Pros:**

- Rich formatting
- Search functionality
- Collaboration features
- Version history

**Cons:**

- **❌ External dependency:** Not in repository
- **❌ Context loss:** AI agents can't easily access
- **❌ Synchronization issues:** Code and docs separate
- **❌ Review process:** Not part of PR workflow

**Rejected because:** Docs must be in repository for AI agent access

### Alternative 3: Generated Documentation Only

**Approach:** Auto-generate all docs from code (Sphinx, MkDocs, etc.)

**Pros:**

- Always in sync with code
- Automated updates
- Consistent format

**Cons:**

- **❌ Limited to code structure:** Can't document decisions, processes
- **❌ No ADRs:** Decisions not captured
- **❌ No initiatives:** Project planning not covered
- **❌ No prose:** Guides and explanations limited

**Rejected because:** Need mix of generated and manual documentation

---

## Consequences

### Positive

✅ **Clear organization:** Everyone knows where documents belong
✅ **Sustainable lifecycle:** Clear archival and update processes
✅ **Quality assurance:** Automated linting and validation
✅ **AI-optimized:** Structure designed for efficient agent consumption
✅ **Discoverability:** Hierarchical structure aids navigation
✅ **Immutable decisions:** ADRs provide stable architectural record
✅ **Scalability:** Structure supports project growth
✅ **Best practices:** Based on industry standards (Divio, ADR, Docs as Code)

### Negative

⚠️ **Initial migration effort:** Moving existing docs to new structure
⚠️ **Tool setup:** Need to install markdownlint-cli2
⚠️ **Learning curve:** Team must learn new structure and standards
⚠️ **Maintenance overhead:** More files to maintain than flat structure
⚠️ **CI integration:** Need to add documentation checks to pipeline

### Neutral

🔸 **Opinionated:** Imposes specific structure (but based on proven patterns)
🔸 **Markdown-centric:** All docs in Markdown (industry standard)
🔸 **File-based:** No database or external system (simplicity trade-off)

---

## Implementation

### Phase 1: Directory Structure (Completed 2025-10-15)

✅ Created directory structure:

```text
docs/
├── standards/
├── adr/
├── initiatives/active/
├── initiatives/completed/
├── guides/
├── archive/session-summaries/
└── [other directories]
```

### Phase 2: Standard Documents (Completed 2025-10-15)

✅ Created foundational documents:

- `DOCUMENTATION_STRUCTURE.md` - Structure definition
- `CONSTITUTION.md` - Project principles
- `docs/standards/DOCUMENTATION_STANDARDS.md` - AI-friendly docs
- `docs/standards/SUMMARY_STANDARDS.md` - Session summary format
- `docs/standards/COMMIT_STYLE_GUIDE.md` - Commit conventions
- `docs/standards/META_ANALYSIS_TRACKING.md` - Artifact tracking
- `docs/adr/template.md` - ADR template
- `docs/adr/README.md` - ADR index

### Phase 3: Linting Tools (Completed 2025-10-15)

✅ Configured quality tools:

- `.markdownlint.json` - Markdown structure rules
- `.vale.ini` - Prose quality rules
- `.pre-commit-config.yaml` - Git hooks
- Taskfile commands: `task docs:lint`, `task docs:fix`

### Phase 4: Migration (Completed 2025-10-15)

✅ Moved documents to proper locations:

- Session summaries → `docs/archive/session-summaries/`
- Standards → `docs/standards/`
- Guides → `docs/guides/`
- First ADR created: `0001-use-httpx-playwright-fallback.md`

### Phase 5: Conversion (In Progress)

⏳ Convert legacy documents:

- [ ] Convert DD-002 through DD-010 to ADR format
- [ ] Archive IMPROVEMENTS_V1/V2
- [ ] Consolidate redundant documentation

---

## Validation

### Success Criteria

✅ **All new docs follow structure:** New documents in correct locations
✅ **Linting passes:** `task docs:lint` succeeds
✅ **No double-spaces:** Automated removal
✅ **ADRs created:** Major decisions documented
✅ **Initiatives tracked:** Active work visible

### Monitoring

- Weekly review of documentation additions
- Monthly audit of archive vs active docs
- Quarterly review of ADRs and initiatives
- CI/CD enforcement of quality standards

---

## References

### External Standards

- [Divio Documentation System](https://documentation.divio.com/) - 4 types of documentation
- [ADR GitHub](https://adr.github.io/) - ADR best practices
- [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/) - Documentation methodology
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- [Google Developer Documentation Style Guide](https://developers.google.com/style/)

### Tools

- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) - Markdown linting
- [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) - Documentation linting
- Pre-commit framework

---

## Related ADRs

- **ADR-0002:** Windsurf workflow system
- **ADR-0001:** httpx/Playwright fallback strategy (technical)

---

**Last Updated:** 2025-10-15
**Supersedes:** Informal documentation practices
**Superseded By:** None
