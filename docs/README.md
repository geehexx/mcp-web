# Documentation Index

**mcp-web** - Comprehensive documentation for the MCP Web Summarization Tool

**Last Updated:** 2025-10-18

---

## Quick Links

- [Project Summary](../PROJECT_SUMMARY.md) - High-level project overview
- [Constitution](CONSTITUTION.md) - Project principles and AI guidelines
- [Documentation Structure](DOCUMENTATION_STRUCTURE.md) - How documentation is organized
- [Contributing](../CONTRIBUTING.md) - Contribution guidelines

---

## Documentation Categories

### 📋 Architecture Decision Records (ADRs)

**Location:** [`adr/`](adr/)

Immutable records of significant architectural decisions.

**Key ADRs:**

- [ADR-0001: Use httpx with Playwright Fallback](adr/0001-use-httpx-playwright-fallback.md)
- [ADR-0002: Adopt Windsurf Workflow System](adr/0002-adopt-windsurf-workflow-system.md)
- [ADR-0018: Workflow Architecture V3](adr/0018-workflow-architecture-v3.md)

[View all ADRs →](adr/README.md)

---

### 🎯 Active Initiatives

**Location:** [`initiatives/active/`](initiatives/active/)

Current strategic projects and features in development.

**Q4 2025 Initiatives:**

- [Quality Foundation](initiatives/active/2025-q4-quality-foundation.md)
- [Performance Optimization Pipeline](initiatives/active/2025-q4-performance-optimization-pipeline.md)
- [Windsurf Workflows V2 Optimization](initiatives/active/2025-q4-windsurf-workflows-v2-optimization.md)

[View all initiatives →](initiatives/README.md)

---

### 📖 Guides & References

**Location:** [`guides/`](guides/)

Practical guides, command references, and how-to documentation.

**Available Guides:**

- [Testing Reference](guides/TESTING_REFERENCE.md) - Test commands and patterns
- [Testing Guide](guides/TESTING_GUIDE.md) - Comprehensive testing practices
- [Local LLM Guide](guides/LOCAL_LLM_GUIDE.md) - Using local LLM providers
- [Taskfile Guide](guides/TASKFILE_GUIDE.md) - Task automation reference
- [Performance Guide](guides/PERFORMANCE_GUIDE.md) - Performance optimization
- [Deployment Guide](guides/DEPLOYMENT_GUIDE.md) - Deployment instructions
- [Commit Style Guide](guides/COMMIT_STYLE_GUIDE.md) - Conventional commits
- [Documentation Standards](guides/DOCUMENTATION_STANDARDS.md) - Documentation best practices
- [Summary Standards](guides/SUMMARY_STANDARDS.md) - Session summary standards
- [Meta-Analysis Tracking](guides/META_ANALYSIS_TRACKING.md) - Meta-analysis workflow

[View all guides →](guides/README.md)

---

### 🏗️ Architecture Documentation

**Location:** [`architecture/`](architecture/)

System design, patterns, and architectural documentation.

**Key Documents:**

- [System Architecture](architecture/ARCHITECTURE.md) - Overall system design
- [Security Architecture](architecture/SECURITY_ARCHITECTURE.md) - Security patterns and practices

---

### 📚 API Documentation

**Location:** [`api/`](api/)

Technical reference for modules and functions.

**Key Documents:**

- [API Reference](api/API.md) - Complete API documentation

---

### 🔧 Reference Documentation

**Location:** [`reference/`](reference/)

Configuration, environment variables, and quick lookup information.

**Available References:**

- [Environment Variables](reference/ENVIRONMENT_VARIABLES.md)
- [Configuration](reference/CONFIGURATION.md)
- [Error Codes](reference/ERROR_CODES.md)
- [Changelog](reference/CHANGELOG.md)

---

### 📦 Archive

**Location:** [`archive/`](archive/)

Historical documents, completed initiatives, and session summaries.

**Contents:**

- [Session Summaries](archive/session-summaries/) - Historical session records
- [Completed Initiatives](initiatives/completed/) - Finished projects
- [Archived Decisions](archive/DECISIONS.md) - Legacy decision log (superseded by ADRs)

---

## Windsurf AI Configuration

**Location:** [`../.windsurf/`](../.windsurf/)

AI agent workflows and behavior rules (not strictly documentation).

### Workflows

**Location:** [`../.windsurf/workflows/`](../.windsurf/workflows/)

Executable AI agent workflows for orchestration and automation.

**Key Workflows:**

- `/work` - Master orchestration workflow
- `/plan` - Planning workflow
- `/implement` - Implementation workflow
- `/validate` - Quality gate validation
- `/commit` - Git operations

[See ADR-0018 for complete workflow taxonomy](adr/0018-workflow-architecture-v3.md)

### Rules

**Location:** [`../.windsurf/rules/`](../.windsurf/rules/)

AI agent behavior rules and standards.

**Available Rules:**

- `00_agent_directives.md` - Core principles and persona
- `01_testing_and_tooling.md` - Testing standards
- `02_python_standards.md` - Code standards
- `03_documentation_lifecycle.md` - Documentation rules
- `04_security.md` - Security patterns

---

## Documentation Standards

All documentation follows:

- **Markdown format** with linting (markdownlint-cli2)
- **Naming conventions** enforced by ls-lint
- **YAML frontmatter** for metadata (see [DOCUMENTATION_STRUCTURE.md](DOCUMENTATION_STRUCTURE.md))
- **Version control** via Git
- **Quality gates** via pre-commit hooks and CI

---

## Contributing to Documentation

1. **Follow naming conventions:**
   - ADRs: `0001-my-decision.md`
   - Initiatives: `YYYY-MM-DD-my-initiative.md` or `YYYY-qN-my-initiative.md`
   - Guides: `UPPER_CASE.md`
   - Session summaries: `YYYY-MM-DD-description.md`

2. **Use appropriate templates:**
   - ADRs: [`adr/template.md`](adr/template.md)
   - Initiatives: [`initiatives/template.md`](initiatives/template.md)

3. **Run quality checks:**

   ```bash
   task docs:lint        # Lint all documentation
   task docs:fix         # Auto-fix issues
   npx @ls-lint/ls-lint  # Validate naming conventions
   ```

4. **Update this index** when adding new major documents

---

## Questions?

- Check [DOCUMENTATION_STRUCTURE.md](DOCUMENTATION_STRUCTURE.md) for detailed organization
- Review [CONSTITUTION.md](CONSTITUTION.md) for project principles
- Open an issue with "docs:" prefix for documentation questions

---

**Maintained by:** mcp-web core team
**Structure Version:** 1.1.0
**Last Review:** 2025-10-18
