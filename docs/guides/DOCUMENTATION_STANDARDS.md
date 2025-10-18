# Documentation Standards for AI Agents

**Purpose:** Define clear, AI-consumable documentation standards for mcp-web project.
**Audience:** AI agents, developers, contributors
**Last Updated:** October 15, 2025

---

## Table of Contents

- [Principles](#principles)
- [Directory Structure](#directory-structure)
- [Document Types](#document-types)
- [Formatting Standards](#formatting-standards)
- [Session Summary Standards](#session-summary-standards)
- [AI Optimization Guidelines](#ai-optimization-guidelines)
- [References](#references)

---

## Principles

### 1. Clarity Over Brevity

AI agents benefit from explicit, detailed information. When in doubt, be more specific.

**DO:** "Run `task test:fast` to execute unit and security tests in parallel (excludes LLM-dependent tests)"
**DON'T:** "Run fast tests"

### 2. Hierarchical Organization

Use clear heading structures (H1 → H2 → H3). Each level should represent a meaningful subdivision.

### 3. Consistent Terminology

Use the same terms throughout. Define domain-specific terms on first use.

**Project Glossary:**

- **MCP:** Model Context Protocol
- **LLM:** Large Language Model
- **ADR:** Architecture Decision Record
- **TDD:** Test-Driven Development

### 4. Actionable Content

Every instruction should be executable. Prefer code examples over prose.

### 5. Time-Stamped References

Include dates for time-sensitive information and external references.

**Example:** "As of October 2025, pytest-xdist 3.8.0 is the stable version."

---

## Directory Structure

```text
docs/
├── standards/ # Documentation standards and style guides
│ ├── DOCUMENTATION_STANDARDS.md (this file)
│ ├── COMMIT_STYLE_GUIDE.md
│ ├── PYTHON_STYLE_GUIDE.md
│ └── SUMMARY_STANDARDS.md
├── adr/ # Architecture Decision Records
│ ├── README.md
│ ├── template.md
│ └── NNNN-verb-noun-phrase.md
├── initiatives/ # Project initiatives
│ ├── active/ # Current initiatives
│ └── archived/ # Completed initiatives
├── archive/ # Historical documentation
│ └── session-summaries/ # AI agent session summaries
├── ARCHITECTURE.md # System architecture overview
├── API.md # API documentation
├── TESTING.md # Testing strategy and guide
├── PROJECT_SUMMARY.md # High-level project summary
├── DOCUMENTATION_STRUCTURE.md # Meta-documentation guide
└── CONSTITUTION.md # Project principles and values
```

### Document Placement Rules

| Type | Location | Naming Convention |
|------|----------|-------------------|
| **Architecture Decision** | `docs/adr/` | `NNNN-verb-noun-phrase.md` |
| **Active Initiative** | `docs/initiatives/active/` | `kebab-case-name.md` |
| **Archived Initiative** | `docs/initiatives/archived/` | `YYYY-QN-kebab-case.md` |
| **Session Summary** | `docs/archive/session-summaries/` | `YYYY-MM-DD-descriptive-name.md` |
| **Standard/Guide** | `docs/standards/` | `SCREAMING_SNAKE_CASE.md` |
| **Core Documentation** | `docs/` | `SCREAMING_SNAKE_CASE.md` |

---

## Document Types

### 1. Architecture Decision Records (ADRs)

**Purpose:** Document significant architectural choices

**Template:** `docs/adr/template.md`

**Required Sections:**

1. **Title:** Number + verb-noun phrase (`0001-use-httpx-playwright-fallback.md`)
2. **Status:** Proposed → Accepted → Implemented (or Rejected/Superseded)
3. **Context:** What is the issue we're addressing?
4. **Decision:** What did we decide?
5. **Alternatives:** What other options were considered?
6. **Consequences:** What are the impacts (positive and negative)?
7. **Implementation:** How is this being/was implemented?

**When to Create:**

- Choosing between major libraries/frameworks
- Defining system boundaries
- Establishing architectural patterns
- Making technology stack decisions

**References:**

- [Michael Nygard's ADR Template](https://github.com/joelparkerhenderson/architecture-decision-record/blob/main/templates/decision-record-template-by-michael-nygard/index.md)
- [ADR Tools](https://adr.github.io/)

### 2. Initiatives

**Purpose:** Track multi-session projects

**Required Sections:**

1. **Status:** Active/Completed/Abandoned
2. **Created Date**
3. **Priority:** High/Medium/Low
4. **Owner:** Who's responsible
5. **Overview:** What is this initiative?
6. **Goals:** Specific, measurable objectives
7. **Acceptance Criteria:** Checklist of completion requirements
8. **Implementation Notes:** Technical details
9. **Timeline:** Estimates and deadlines (if applicable)

**When to Create:**

- Work that spans multiple sessions
- Complex refactoring projects
- Feature development
- Technical debt remediation

**Archive When:**

- All acceptance criteria met
- Replaced by newer approach
- Explicitly abandoned

### 3. Session Summaries

**Purpose:** Document significant AI agent work sessions

**See:** [SUMMARY_STANDARDS.md](./SUMMARY_STANDARDS.md)

### 4. Standards and Style Guides

**Purpose:** Define conventions for code, commits, documentation

**Required Sections:**

1. **Purpose:** Why this standard exists
2. **Scope:** What it covers
3. **Rules:** Specific, enumerated guidelines (MUST/SHOULD/MAY)
4. **Examples:** Good and bad examples
5. **Enforcement:** How it's checked
6. **References:** External authoritative sources

**When to Create:**

- Establishing project conventions
- Formalizing informal practices
- Preventing repeated mistakes

### 5. Core Documentation

**Types:**

- **ARCHITECTURE.md:** System design and component relationships
- **API.md:** Public API reference
- **TESTING.md:** Test strategy, markers, and practices
- **PROJECT_SUMMARY.md:** High-level project description
- **README.md:** Quick start and overview

**Update Frequency:**

- After major architectural changes
- When adding new public APIs
- Quarterly reviews

---

## Formatting Standards

### Markdown Conventions

#### Headings

- Use ATX-style headings (`#`, `##`, `###`)
- Only one H1 per document (the title)
- Don't skip heading levels
- Add blank line before and after headings

```markdown
# Document Title

## Section

### Subsection

Content here.

### Another Subsection
```

#### Lists

- Use `-` for unordered lists
- Use `1.` for ordered lists (auto-numbering)
- Indent nested lists by 2 spaces
- Add blank line before/after lists

```markdown
- Item 1
 - Nested item
 - Another nested
- Item 2

1. First step
2. Second step
 - Substep a
 - Substep b
3. Third step
```

#### Code Blocks

- Use fenced code blocks with language identifier
- Include language even for plain text (use `bash`, `text`, `python`, etc.)
- Add blank line before/after code blocks

```python
def example() -> str:
    return "hello"
```

```bash
task test:fast
```

#### Links

- Use reference-style links for repeated URLs
- Include URL in link text for external references
- Use relative paths for internal links

```text
See [Testing Guide](../TESTING.md) for details.

External: [pytest Documentation](https://docs.pytest.org/)

[pytest]: https://docs.pytest.org/
[ruff]: https://docs.astral.sh/ruff/
```

#### Emphasis

- Use `**bold**` for emphasis/importance
- Use `*italic*` for technical terms on first use
- Use `code` for inline code, commands, file names

```markdown
**Important:** Always run `task test:fast` before committing.

The *Model Context Protocol* (MCP) defines how agents communicate.

Edit the `pytest.ini` file to add markers.
```

#### Tables

- Use tables for structured data
- Align columns with pipes
- Include header separator

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1 | Cell 2 | Cell 3 |
| Cell 4 | Cell 5 | Cell 6 |
```

#### Horizontal Rules

- Use `---` on its own line
- Add blank lines before/after
- Use to separate major sections

```markdown
## Section 1

Content.

---

## Section 2
```

### Metadata

Include frontmatter for workflows:

```markdown
---
description: Brief action phrase
auto_execution_mode: 3
---

# Workflow Name
```

### File Organization

#### Document Structure

```markdown
# Title

**Purpose:** One sentence summary
**Last Updated:** YYYY-MM-DD

---

## Table of Contents (for long documents)

- [Section 1](#section-1)
- [Section 2](#section-2)

---

## Section 1

Content.

## Section 2

Content.

---

## References

- [External Link](https://example.com/)
- [Internal Link](../path/to/doc.md)
```

---

## Session Summary Standards

See [SUMMARY_STANDARDS.md](./SUMMARY_STANDARDS.md) for complete specification.

---

## AI Optimization Guidelines

### Language Clarity

#### Use Imperative Mood

**Good:** "Run `task test` to execute all tests."
**Bad:** "You should probably run tests."

#### Avoid Ambiguity

**Good:** "Set `max_length` to 10000 for production deployments."
**Bad:** "Use a reasonable value for `max_length`."

#### Define Acronyms

**First use:**

```markdown
The *Model Context Protocol* (MCP) defines...
```

**Subsequent uses:**

```markdown
MCP servers provide...
```

### Structural Clarity

#### Use Numbered Lists for Procedures

```markdown
1. Open the configuration file: `config.toml`
2. Set the `cache_ttl` parameter to `3600`
3. Save and restart the service: `task restart`
```

#### Use Bullet Lists for Properties

```markdown
The cache system supports:
- In-memory storage
- Persistent storage (SQLite)
- TTL-based expiration
- LRU eviction
```

#### Use Tables for Comparisons

```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| Speed | Fast | Slow |
| Memory | High | Low |
```

### Example-Driven

#### Include Code Examples

Don't just describe—show:

```python
# Good: Concrete example
def fetch_with_cache(url: str) -> str:
 """Fetch URL with caching.

 Example:
 >>> result = fetch_with_cache("https://example.com")
 >>> print(result[:100])
 '<!DOCTYPE html>...'
 """
 return cache.get_or_fetch(url)
```

#### Show Command Output

```bash
$ task test:fast

============================= test session starts ==============================
...
========================== 54 passed in 5.23s ===========================
```

### Context Preservation

#### Link Related Documents

```markdown
This decision relates to [ADR-0001: httpx/Playwright Fallback](../adr/0001-use-httpx-playwright-fallback.md).

See also:
- [Testing Strategy](../TESTING.md)
- [Security Guidelines](../../.windsurf/rules/04_security.md)
```

#### Include Dates for Time-Sensitive Info

```markdown
As of October 2025, the recommended Python version is 3.12.

Reference: [Python Release Schedule](https://peps.python.org/pep-0693/)
(Checked: 2025-10-15)
```

### Validation

Before publishing documentation:

- [ ] All code examples are tested and work
- [ ] All links are valid (internal and external)
- [ ] Acronyms are defined on first use
- [ ] Commands include expected output
- [ ] Dates are included for time-sensitive information
- [ ] Passes markdownlint validation
- [ ] Uses consistent terminology from glossary

---

## Tooling

### Markdown Linting

```bash
# Check markdown files
task lint:markdown

# Auto-fix issues
markdownlint-cli2 --fix "**/*.md"
```

Configuration: `.markdownlint.json`

### Link Checking

```bash
# Check for broken links (not yet implemented)
# TODO: Add markdown-link-check
```

### Documentation Generation

```bash
# Generate API docs (if applicable)
# TODO: Add sphinx/mkdocs
```

---

## References

### Standards and Specifications

- **Markdown:** [CommonMark Spec](https://commonmark.org/)
- **Frontmatter:** [YAML 1.2](https://yaml.org/spec/1.2/)
- **ADRs:** [ADR GitHub Organization](https://adr.github.io/)
- **Conventional Commits:** [conventionalcommits.org](https://www.conventionalcommits.org/)

### Style Guides

- **Google:** [Technical Writing Guide](https://developers.google.com/tech-writing)
- **Microsoft:** [Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/)
- **GitLab:** [Documentation Style Guide](https://docs.gitlab.com/ee/development/documentation/styleguide/)

### Tools

- **markdownlint:** [Rules Reference](https://github.com/DavidAnson/markdownlint/blob/main/doc/Rules.md)
- **Diátaxis:** [Documentation System](https://diataxis.fr/)

### AI-Specific

- **JetBrains:** [Coding Guidelines for AI Agents](https://blog.jetbrains.com/idea/2025/05/coding-guidelines-for-your-ai-agents/)
- **Anthropic:** [Prompt Engineering Guide](https://docs.anthropic.com/claude/docs/prompt-engineering)

---

**Last Updated:** October 15, 2025
**Version:** 1.0
**Maintained By:** mcp-web core team
