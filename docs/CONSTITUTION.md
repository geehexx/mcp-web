# mcp-web Project Constitution

**Version:** 1.0.0
**Effective Date:** 2025-10-15
**Status:** Active

This document establishes the principles, standards, and processes that govern the mcp-web project. It serves as the foundational reference for all contributors, especially AI agents working on the codebase.

---

## Core Principles

### 1. Quality Over Speed

**We prioritize correctness, security, and maintainability over rapid feature delivery.**

- Every feature must have tests (unit + integration)
- Security is not optional
- Code must pass all linting and type checking
- Documentation is part of the deliverable, not an afterthought

### 2. Transparency Through Documentation

**Every significant decision must be documented with rationale.**

- Architectural decisions → ADRs (`docs/adr/`)
- Features and improvements → Initiatives (`docs/initiatives/`)
- API changes → API docs (`docs/api/`)
- User-facing changes → Guides (`docs/guides/`)

### 3. Security by Default

**Security features are enabled by default and require explicit opt-out.**

- OWASP LLM Top 10 compliance is mandatory
- Prompt injection prevention on all LLM inputs
- Output validation on all LLM responses
- Rate limiting and resource controls enabled

### 4. Evidence-Based Decisions

**Decisions are based on research, benchmarks, and external references.**

- Include references to external documentation
- Link to research papers, blog posts, and standards
- Benchmark alternatives before choosing
- Document why alternatives were rejected

### 5. Sustainability

**The project must be maintainable by humans and AI agents long-term.**

- Clear documentation structure
- Consistent coding standards
- Automated quality checks
- Regular review and refactoring

---

## Documentation Standards

### 1. Documentation is Code

**All documentation follows the same quality standards as code:**

- Must pass markdown linting (markdownlint)
- Must pass documentation linting (markdownlint)
- Must be free of double-spaces and LLM artifacts
- Must be reviewed and approved

### 2. Documentation Structure

**Follow the structure defined in** [DOCUMENTATION_STRUCTURE.md](DOCUMENTATION_STRUCTURE.md):

- ADRs for architectural decisions
- Initiatives for strategic work
- Guides for how-to content
- API docs for technical reference
- Archive for historical documents

### 3. Documentation Maintenance

**Documentation must be kept up-to-date:**

| Trigger | Action | Responsible |
|---------|--------|-------------|
| New feature | Create/update ADR, guides, API docs | Developer |
| API change | Update API docs immediately | Developer |
| Config change | Update reference docs | Developer |
| Quarterly | Review all active docs | Team |
| Release | Update CHANGELOG | Release manager |
| **Any change** | **Update PROJECT_SUMMARY.md** | **Developer (Continuous)** |

#### 3.1 PROJECT_SUMMARY.md: Living Status Document

**CRITICAL REQUIREMENT:** `PROJECT_SUMMARY.md` in the project root MUST be maintained continuously as a living snapshot of project status.

**Scope:** This requirement supersedes workflow boundaries and applies to ALL work sessions.

**Update Triggers:**

- Major feature completion
- Initiative status changes
- Metrics changes (test coverage, type coverage, etc.)
- Roadmap updates
- Architecture decision implementations
- Any significant project milestone

**Required Sections:**

- Current version and status
- Key metrics (test coverage, quality indicators)
- Active initiatives with progress
- Recent accomplishments
- Roadmap (current and planned versions)
- Technical debt status
- Links to key documentation

**Maintenance Responsibility:**

- All contributors (human and AI)
- Reviewed in quarterly documentation reviews
- Updated before every release
- Serves as single source of truth for project overview

### 4. External References

**Always cite external sources:**

- Include URLs to documentation, papers, standards
- Reference specific sections when possible
- Check links in CI (use automated link checker)
- Prefer stable URLs (avoid blog posts that may disappear)

**Preferred sources:**

- Official documentation (Python, OpenAI, OWASP, etc.)
- Established standards (RFCs, OWASP, ISO, etc.)
- Academic papers (arXiv, ACM, IEEE)
- Well-maintained open source projects
- Reputable technical blogs (Real Python, Martin Fowler, etc.)

---

## Code Standards

### 1. Python Code Style

**Follow PEP 8 and our extended standards:**

- **Type hints:** Required on all functions (PEP 484)
- **Docstrings:** Google style, required on all public APIs
- **Line length:** 100 characters maximum
- **Import order:** Standard library → third-party → local
- **String quotes:** Double quotes for strings, single for keys

**Enforced by:**

- `ruff` (linting and formatting)
- `mypy` (type checking)
- `pydocstyle` (docstring validation)

### 2. Async/Await Patterns

**Follow async best practices from Real Python:**

- Use `async def` only for I/O operations
- Use `await` for all async calls (no blocking in async context)
- Use `asyncio.gather()` for concurrent operations
- Use semaphores for rate limiting
- Use `async with` for resource cleanup
- Handle exceptions in async context properly

**Reference:** [Real Python - Async I/O](https://realpython.com/async-io-python/)

### 3. Security Standards

**Follow OWASP LLM Top 10 (2025):**

- **LLM01:** Prompt injection prevention (required)
- **LLM05:** Output validation (required)
- **LLM07:** System prompt leakage detection (required)
- **LLM10:** Resource consumption limits (required)

**All LLM interactions must:**

- Validate and sanitize inputs
- Use structured prompts (separate instructions from data)
- Validate outputs for security issues
- Enforce rate limits and timeouts
- Log security events

**Reference:** [OWASP LLM Top 10](https://genai.owasp.org/)

### 4. Testing Standards

**Comprehensive test coverage is mandatory:**

- **Unit tests:** All functions and classes
- **Integration tests:** Module interactions
- **Security tests:** All security features
- **Golden tests:** Output regression testing
- **Performance tests:** Benchmarks for critical paths

**Test organization:**

```text
tests/
├── unit/ # Fast, isolated tests
├── integration/ # Multi-component tests
├── security/ # Security-focused tests
├── golden/ # Regression tests
├── live/ # Network/API tests (marked)
└── benchmarks/ # Performance tests
```

**Test requirements:**

- Use AAA pattern (Arrange, Act, Assert)
- One test per scenario
- Descriptive test names
- Proper fixtures and parametrization
- Async tests properly marked
- 85%+ code coverage

---

## Change Management

### 1. Architecture Decisions

**For significant architectural changes:**

1. Create ADR using template (`docs/adr/template.md`)
2. Status: Proposed
3. Open PR for team review
4. Discuss alternatives and tradeoffs
5. Status: Accepted (after approval)
6. Implement the decision
7. Status: Implemented
8. Reference ADR in code comments where relevant

**What qualifies as "significant":**

- New dependencies
- Major algorithm changes
- Security-related changes
- Performance-critical changes
- API design changes

### 2. Feature Development

**For new features:**

1. Create initiative in `docs/initiatives/active/`
2. Define success criteria and tasks
3. Create ADRs for architectural decisions
4. Implement with tests and documentation
5. Update guides and API docs
6. Mark initiative as completed
7. Move to `docs/initiatives/completed/` after 1 month

### 3. Bug Fixes

**For bug fixes:**

1. Create regression test that reproduces bug
2. Fix the bug
3. Verify test passes
4. Update documentation if user-facing
5. Add to CHANGELOG

### 4. Documentation Changes

**For documentation updates:**

1. Run linters before committing
2. Check internal and external links
3. Update "Last Updated" date
4. Run `task docs:lint` before PR
5. Review for clarity and accuracy

---

## AI Agent Guidelines

**For AI agents (like Cascade) working on this project:**

### 1. Always Reference the Constitution

**Before making changes, consult:**

- This constitution for principles and standards
- `DOCUMENTATION_STRUCTURE.md` for documentation organization
- Windsurf rules (`.windsurf/rules/`) for detailed guidelines
- Relevant ADRs for architectural context

### 2. Documentation is Mandatory

**For every code change:**

- Update or create documentation
- Add references to external sources
- Create ADRs for architectural decisions
- Update API docs for API changes
- Keep CHANGELOG current

### 3. Quality Checks

**Before committing:**

- Run all linters (`task lint`)
- Run all tests (`task test`)
- Run security checks (`task security`)
- Run documentation linters (`task docs:lint`)
- Check type hints (`task lint:mypy`)

### 4. External Research

**When making decisions:**

- Search for best practices (use @web search)
- Reference authoritative sources
- Include URLs in documentation
- Document alternatives considered
- Explain rationale with evidence

### 5. Avoid LLM Artifacts

**Clean up all output:**

- Remove double-spaces
- Remove placeholder comments ("TODO: implement this")
- Remove overly enthusiastic language
- Remove unnecessary emoji (unless explicitly requested)
- Use professional, technical tone

### 6. Update This Constitution

**If standards evolve:**

- Propose changes via PR
- Document rationale
- Update version number
- Add to changelog at bottom
- Notify team of changes

---

## Tool and Process Standards

### 1. Task Runner

**Use Taskfile for all commands:**

```bash
# Don't use raw commands
python -m pytest

# Use Taskfile instead
task test
```

**Benefits:**

- Consistent commands across environments
- Centralized configuration
- Documentation in task descriptions

### 2. Dependency Management

**Use pip with pyproject.toml:**

- Lock dependencies for reproducibility
- Separate dev and production dependencies
- Keep dependencies up-to-date (quarterly review)
- Security scan dependencies (`task security:safety`)

### 3. Version Control

**Git commit message format:**

```text
type(scope): brief description

Detailed explanation of what and why (not how).

References: #123, ADR-0005
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `security`: Security enhancement
- `chore`: Maintenance tasks

### 4. CI/CD

**All PRs must pass:**

- Linting (`task lint`)
- Type checking (`task lint:mypy`)
- Tests with coverage (`task test:coverage:min`)
- Security checks (`task security`)
- Documentation linting (`task docs:lint`)

**On merge to main:**

- Run full test suite including live tests
- Generate API documentation
- Update CHANGELOG
- Tag release if applicable

---

## Review and Update Process

### 1. Quarterly Review

**Every quarter, review:**

- All active initiatives (move completed ones to archive)
- All active documentation (update or archive)
- Dependencies (update or replace)
- ADRs (check if still valid)
- This constitution (update if needed)

### 2. Post-Release Review

**After each release:**

- Review what went well / what didn't
- Update processes if needed
- Archive old documentation
- Plan next initiatives

### 3. Security Review

**Monthly security review:**

- Check for security vulnerabilities (`task security`)
- Review security test coverage
- Update dependencies with security fixes
- Review OWASP LLM Top 10 for new guidance

---

## Exceptions and Overrides

### When to Break the Rules

**Exceptions are allowed when:**

- Emergency security fix (skip some docs, add later)
- Prototype/spike (clearly mark as temporary)
- External constraint (dependency limitation)

**Process for exceptions:**

1. Document the exception and rationale
2. Create issue to fix properly later
3. Add TODO comment in code
4. Add to technical debt log

**Never skip:**

- Security checks
- Critical tests
- Security-related documentation

---

## Governance

### 1. Decision Authority

| Level | Who Decides | Process |
|-------|-------------|---------|
| Code style | Constitution + linters | Automated |
| Bug fixes | Developer | Review + tests |
| Features | Core team | Initiative + review |
| Architecture | Core team | ADR + consensus |
| Constitution changes | Core team | PR + discussion |

### 2. Conflict Resolution

**If standards conflict:**

1. Constitution takes precedence over Windsurf rules
2. Security takes precedence over convenience
3. Documented standards take precedence over undocumented practices
4. Recent decisions supersede old ones (with ADR)

### 3. Evolution

**This constitution evolves with the project:**

- Proposals via PR with rationale
- Discussion period (1 week minimum)
- Consensus required for major changes
- Version number updated
- Changelog maintained at bottom

---

## References

### Standards and Guidelines

- [PEP 8 - Python Style Guide](https://peps.python.org/pep-0008/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [OWASP LLM Top 10 (2025)](https://genai.owasp.org/)
- [Architecture Decision Records](https://adr.github.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)

### Tools

- [Ruff - Python Linter](https://docs.astral.sh/ruff/)
- [MyPy - Type Checker](https://mypy.readthedocs.io/)
- [pytest - Testing Framework](https://docs.pytest.org/)
- [markdownlint - Documentation Linter](https://github.com/DavidAnson/markdownlint)

### Project Documents

- [DOCUMENTATION_STRUCTURE.md](DOCUMENTATION_STRUCTURE.md) - Doc organization
- [docs/adr/](adr/) - Architecture decisions
- [.windsurf/rules/](../.windsurf/rules/) - Detailed coding guidelines

---

## Changelog

### Version 1.0.0 (2025-10-15)

**Initial constitution including:**

- Core principles established
- Documentation standards defined
- Code standards specified
- Change management process
- AI agent guidelines
- Tool and process standards
- Governance structure

**References:**

- Based on research from OWASP, ADR community, and Python best practices
- Incorporates lessons from initial project development (v0.1.0 - v0.2.1)

---

**Maintained by:** mcp-web core team
**Review frequency:** Quarterly
**Last reviewed:** 2025-10-15
**Next review:** 2026-01-15
