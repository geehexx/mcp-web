# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Adaptive chunking enabled by default with content heuristics
- Prompt optimization reducing verbosity by 45-60%
- Adaptive `max_tokens` based on input size with configurable ratio
- Stop sequences support for LLM calls
- Parallel map-reduce optimization for 1.17x speedup
- Mock LLM fixtures for deterministic benchmarks
- Comprehensive benchmark suite for performance testing
- Profiling infrastructure with timing utilities
- CLI testing endpoints (`test-summarize`, `test-robots`)
- Query-aware summarization tests (11 scenarios)
- Playwright fallback tests (18 test cases)
- robots.txt handling tests (25 test cases)
- Documentation linting infrastructure (markdownlint, Vale)
- Custom Vale styles for project-specific terminology
- Pre-commit hooks for documentation quality
- GitHub Actions workflow for CI documentation checks
- Comprehensive ADR framework (16 architecture decisions)
- Project constitution and AI agent directives
- Initiative tracking system (active/completed)
- Meta-analysis workflow for session review
- Session summary standardization
- Windsurf workflow system integration (ADR-0002)
- Documentation structure standards (ADR-0003)

### Changed

- Default chunking strategy now uses adaptive approach
- LLM prompts optimized for reduced latency
- Test performance improved with pytest-xdist parallelization
- Type coverage increased to ~90% (64 errors fixed, 96 → 32)
- Improved logger return type annotations (52 errors fixed)
- Dict type parameters added across 5 modules (12 errors fixed)

### Fixed

- Security test failures (6 tests) with async context manager protocol
- CLI import errors (TextChunker, Config, CacheManager)
- Cache eviction policy name mapping (short to full names)
- Test timeout issues and reliability improvements
- Integration test failures with chunking optimization
- Cache bytes serialization with dotenv loading
- Mock LLM fixtures now fully intercept API calls
- Docker-based markdownlint-cli2 to avoid nodeenv issues
- Workflow auto-fix diff checking to prevent uncommitted changes
- Injection pattern detection in security module

### Security

- Enhanced prompt injection detection patterns
- Implemented async context manager protocol for security validation
- Comprehensive security test coverage (OWASP LLM Top 10)
- Bandit and semgrep integration in CI pipeline

## [0.1.0] - 2025-10-15

### Added

- Initial MCP server implementation
- httpx primary with Playwright fallback for robust fetching (ADR-0001)
- trafilatura content extraction with `favor_recall=True` (ADR-0004)
- Hierarchical and semantic chunking strategies (ADR-0005)
- Map-reduce summarization for long documents (ADR-0006)
- Disk-based caching with 7-day TTL and LRU eviction (ADR-0007)
- OpenAI GPT-4o-mini as default LLM (ADR-0010)
- Local LLM support (Ollama, LM Studio, LocalAI)
- Streaming output for summaries
- MCP tools: `summarize_urls`, `get_cache_stats`, `clear_cache`, `prune_cache`
- Comprehensive test suite (unit, integration, security, golden)
- Taskfile for project automation
- Environment-based configuration
- Structured logging with metrics collection
- Token counting utilities
- Link following with configurable depth
- Markdown output formatting with citations
- Error handling and retry logic
- Rate limiting support
- Concurrent URL fetching
- Content validation and sanitization

### Changed

- Project structure reorganized for maintainability
- Configuration management via environment variables
- LLM provider abstraction for multi-provider support

### Fixed

- Various bug fixes during initial development
- Test stability improvements
- Error handling edge cases

### Security

- Input validation for all user-provided data
- Prompt injection protection
- Content sanitization
- robots.txt respect by default
- Secure credential handling

## Release Notes

### [Unreleased] - October 16, 2025

**Highlights:**

- **Performance**: 1.17x speedup with parallel map-reduce, optimized prompts
- **Quality**: 85% test coverage, comprehensive security testing
- **Documentation**: Complete ADR framework, linting infrastructure
- **Developer Experience**: Windsurf workflows, Taskfile automation

**Breaking Changes:**

- None (backward compatible)

**Migration Guide:**

- No migration required
- New adaptive chunking enabled by default (opt-out via `MCP_WEB_CHUNKER_ADAPTIVE_CHUNKING=false`)
- New configuration options available but optional

### [0.1.0] - October 15, 2025

**Highlights:**

- Initial release
- Full MCP server implementation
- Local and cloud LLM support
- Comprehensive testing infrastructure

**Breaking Changes:**

- Initial release, no breaking changes

## Development

### Commit Message Format

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions or updates
- `chore`: Maintenance tasks
- `security`: Security improvements
- `ci`: CI/CD changes

**Scopes:**

- `fetcher`: URL fetching
- `extractor`: Content extraction
- `chunker`: Text chunking
- `summarizer`: LLM summarization
- `cache`: Caching system
- `config`: Configuration
- `cli`: Command-line interface
- `security`: Security features
- `tests`: Test infrastructure
- `docs`: Documentation
- `workflows`: Windsurf workflows
- `adr`: Architecture Decision Records
- `initiative`: Initiative tracking
- `meta`: Meta-analysis and session summaries

### Changelog Maintenance

**Update triggers:**

1. Before every release (review all unreleased changes)
2. After significant features (add to Unreleased section)
3. After breaking changes (document migration path)
4. Monthly review of unreleased changes

**Process:**

1. Review commits since last release: `git log v0.1.0..HEAD --oneline`
2. Group by type (Added, Changed, Fixed, Security)
3. Add human-readable descriptions
4. Link to relevant ADRs or issues
5. Document breaking changes with migration guide

**Automation:**

```bash
# Generate changelog entries from commits
git log --format="%s" v0.1.0..HEAD | grep "^feat:" | sed 's/feat[(][^)]*[)]: /- /'
git log --format="%s" v0.1.0..HEAD | grep "^fix:" | sed 's/fix[(][^)]*[)]: /- /'
```

## Versioning Strategy

**Semantic Versioning:**

- **Major (X.0.0)**: Breaking changes, major rewrites
- **Minor (0.X.0)**: New features, backward compatible
- **Patch (0.0.X)**: Bug fixes, backward compatible

**Current Focus:**

- v0.1.0: Initial release (foundation)
- v0.2.0: Local LLM support, testing infrastructure ✅
- v0.3.0: Performance optimization, quality foundation (in progress)
- v0.4.0: Extended features (PDF, multi-language, embeddings)
- v1.0.0: Production-ready, stable API

## Links

- [GitHub Repository](https://github.com/geehexx/mcp-web)
- [Issue Tracker](https://github.com/geehexx/mcp-web/issues)
- [ADR Index](../adr/README.md)
- [Contributing Guide](../../CONTRIBUTING.md)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)

---

_Generated from git history and conventional commits. For detailed commit history, see `git log`._
