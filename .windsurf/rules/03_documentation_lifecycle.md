---
created: "2025-10-15"
updated: "2025-10-18"
trigger: glob
description: Governs documentation creation, maintenance, and archival. Meta-rule about the development process.
globs:
  - docs/**/*.md
  - "*.md"
category: documentation
tokens: 1313
applyTo:
  - documentation
  - adr
  - initiatives
priority: medium
status: active
---

# Rule: Documentation Lifecycle & Management

## 3.1 Documentation Structure

**Reference:** `docs/DOCUMENTATION_STRUCTURE.md`

Follow the established directory structure:

```text
docs/
├── CONSTITUTION.md                 # Project principles
├── DOCUMENTATION_STRUCTURE.md      # This structure (meta)
├── adr/                            # Architecture Decision Records
│   ├── README.md                   # ADR index
│   ├── template.md                 # ADR template
│   └── NNNN-decision-title.md      # Individual ADRs
├── initiatives/                    # Strategic work tracking
│   ├── active/                     # Current initiatives
│   └── completed/                  # Archived initiatives
├── guides/                         # How-to documentation
├── api/                            # API reference
├── architecture/                   # System design docs
├── reference/                      # Quick reference
└── archive/                        # Historical documents
```text

## 3.2 Document Types

### Architecture Decision Records (ADRs)

**Reference:** [ADR GitHub](https://adr.github.io/) (October 2025)

- **Purpose:** Document significant architectural decisions
- **Format:** Use `docs/adr/template.md`
- **Naming:** `NNNN-verb-noun-phrase.md` (e.g., `0001-use-httpx-playwright-fallback.md`)
- **Lifecycle:** Proposed → Accepted → Implemented (immutable once accepted)
- **When to create:**
  - New dependencies
  - Major algorithm changes
  - Security-related decisions
  - Performance-critical changes
  - API design decisions

### Initiatives

- **Location:** `docs/initiatives/active/` or `docs/initiatives/completed/`
- **Purpose:** Track strategic projects and features
- **Format:**

  ```markdown
  # Initiative: [Name]

  **Status:** Active | Completed | On Hold
  **Start Date:** YYYY-MM-DD
  **Target Completion:** YYYY-MM-DD

  ## Objective
  [What we're trying to achieve]

  ## Success Criteria
  - [ ] Criterion 1
  - [ ] Criterion 2

  ## Tasks
  - [ ] Task 1
  - [ ] Task 2

  ## Related ADRs
  - ADR-0001: Decision title

  ## Updates
  ### YYYY-MM-DD
  Progress update...
  ```text

### Guides

- **Location:** `docs/guides/`
- **Types:** User guides, developer guides, operational guides
- **Format:** Step-by-step instructions with code examples
- **Required sections:** Prerequisites, Steps, Troubleshooting, Related docs

## 3.3 Documentation Standards

### Markdown Quality

- **Linting:** All markdown must pass markdownlint-cli2
- **Command:** `task docs:lint:markdown`
- **Auto-fix:** `task docs:fix`
- **Common issues:**
  - No double-spaces between words
  - No trailing whitespace
  - Consistent heading levels
  - No bare URLs (use markdown links)

### Prose Quality

- **Linting:** Use markdownlint-cli2 with project style guide
- **Command:** `task docs:lint:prose`
- **Style:**
  - Active voice
  - Present tense
  - Be concise
  - Use inclusive language
  - Define jargon on first use

### External References

- **Always link first mentions:**

  ```markdown
  We use [uv](https://docs.astral.sh/uv/) as our package manager.
  ```text

- **Prefer official documentation:**
  - Python: https://docs.python.org/3/
  - pytest: https://docs.pytest.org/
  - OWASP: https://owasp.org/
- **Include current date context:** "As of October 2025, uv is the recommended..."

### Code Examples

```markdown
**Good example with syntax highlighting:**

\```python
async def fetch_url(url: str) -> bytes:
    """Fetch URL asynchronously."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.content
\```

**Command examples:**

\```bash
# Install dependencies
task install

# Run tests
task test:parallel
\```
```text

## 3.4 Update Triggers

| Trigger | Action | Responsible |
|---------|--------|-------------|
| New feature | Create/update ADR, guides, API docs | Developer |
| API change | Update API docs immediately | Developer |
| Config change | Update reference docs | Developer |
| Bug fix | Update guides if user-facing | Developer |
| Quarterly | Review all active docs | Team |
| Release | Update CHANGELOG | Release manager |

## 3.5 Archival Process

### When to Archive

- Document superseded by newer version
- Initiative completed (after 6 months in completed/)
- Temporary documents no longer relevant
- Old roadmaps/plans

### How to Archive

1. Add archived notice at top:

   ```markdown
   > **⚠️ ARCHIVED:** This document was archived on YYYY-MM-DD.
   > Reason: [superseded by / no longer relevant / initiative completed]
   > See [replacement.md] for current information.
   ```text

2. Move to `docs/archive/`
3. Update any referring documents
4. Add entry to `docs/archive/README.md`

## 3.6 Windsurf Artifacts

**Location:** `.windsurf/rules/` and `.windsurf/workflows/`

### Rules

- **Format:** YAML frontmatter + Markdown content
- **Naming:** `NN_descriptive_name.md` (numbered for priority)
- **Metadata:**

  ```yaml
  ---
  trigger: always_on | glob | model_decision
  description: Brief description without apostrophes
  globs: ["**/*.py"]  # Optional, for glob trigger
  ---
  ```text

- **Content:** Clear, actionable instructions
- **Validation:** After changes, verify Windsurf IDE loads artifact correctly

### Workflows

- **Format:** YAML frontmatter + Markdown steps
- **Naming:** `descriptive-name.md` (kebab-case)
- **Metadata:**

  ```yaml
  ---
  description: Brief workflow description
  auto_execution_mode: 3  # Checkpoints at key steps
  ---
  ```text

- **Content:** Numbered steps with clear instructions
- **Invocation:** `/workflow-name` in Cascade

## 3.7 Documentation Maintenance

### Regular Reviews

- **Weekly:** Active initiatives
- **Monthly:** Guides and API docs
- **Quarterly:** ADRs (ensure still valid), architecture docs

### Quality Checks

Before committing documentation:

```bash
# Run all documentation linters
task docs:lint

# Fix auto-fixable issues
task docs:fix

# Clean double-spaces and artifacts
task docs:clean
```text

### Cross-References

- **Internal links:** Use relative paths: `[ADR-0001](../adr/0001-decision.md)`
- **External links:** Full URLs with context
- **Code references:** Use backticks: `config.py`, `MCPWebConfig`
- **Check links:** Use automated link checker in CI

## 3.8 Living Documentation

**Principle:** Documentation must stay synchronized with code

- **Update docs with code changes** (not after)
- **Tests verify docs** (especially code examples)
- **CI enforces:** Documentation linting and link checking
- **README as entry point:** Always keep README.md current

## 3.9 Version Control

### Commit Messages for Docs

```bash
docs(adr): add ADR-0011 for caching strategy
docs(guides): update testing guide with parallel examples
docs(api): document new summarize_with_query endpoint
docs: fix typos in README and CONTRIBUTING
```text

### PR Requirements

Documentation PRs must:

- [ ] Pass `task docs:lint`
- [ ] Have no broken links
- [ ] Update related documents
- [ ] Include "Last Updated" date
- [ ] Be reviewed for clarity

## 3.10 Documentation Checklist

When creating/updating documentation:

- ✅ Use appropriate document type (ADR, guide, reference, etc.)
- ✅ Follow markdown and prose linting standards
- ✅ Link to external authoritative sources
- ✅ Include code examples with syntax highlighting
- ✅ Add "Last Updated" date
- ✅ Cross-reference related documents
- ✅ Run `task docs:lint` before committing
- ✅ Review for clarity and accuracy
