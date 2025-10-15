# Initiative: Quality Foundation & Testing Excellence

**Status:** Active
**Created:** 2025-10-15
**Owner:** Core Team
**Priority:** High
**Estimated Duration:** 4 weeks
**Target Completion:** 2025-11-15

---

## Objective

Establish world-class quality standards for the mcp-web project through:
1. Comprehensive testing coverage (85%+)
2. Documentation linting and quality enforcement
3. Missing test scenarios (query-aware, Playwright, robots.txt)
4. CLI testing endpoint for manual verification
5. Improved static analysis (mypy configuration)
6. Clean documentation structure with ADRs and archiving

---

## Success Criteria

- [ ] Test coverage ≥85% across all modules
- [ ] All documentation passes markdownlint + Vale
- [ ] Zero double-spaces or LLM artifacts in docs
- [ ] Markdown/prose linting in CI/CD
- [ ] CLI endpoint for URL summarization testing
- [ ] Query-aware summarization tests (10+ scenarios)
- [ ] Playwright fallback tests (5+ scenarios)
- [ ] robots.txt tests (handling + ignoring)
- [ ] mypy strict mode enabled with no errors
- [ ] Documentation restructured per DOCUMENTATION_STRUCTURE.md
- [ ] All decisions converted to ADR format
- [ ] Improvement docs archived appropriately

---

## Motivation

The project has grown rapidly but needs stronger quality foundations:

**Current State:**
- ~85% test coverage but gaps in critical areas
- No query-aware summarization tests
- No Playwright fallback testing
- No robots.txt testing
- Documentation has LLM artifacts and redundancy
- No prose quality checking
- Decisions in single file (not sustainable long-term)
- No clear place for initiatives/roadmap
- No archiving strategy for historical docs

**Desired State:**
- Comprehensive test coverage of all features
- Clean, linted documentation
- Sustainable documentation structure
- Clear separation of active vs archived docs
- Automated quality enforcement
- Easy manual testing via CLI
- Production-ready quality standards

---

## Tasks

### Phase 1: Documentation Structure (✓ Completed 2025-10-15)

- [x] Create DOCUMENTATION_STRUCTURE.md
- [x] Create directory structure (adr/, initiatives/, guides/, etc.)
- [x] Create CONSTITUTION.md
- [x] Create ADR template
- [x] Create ADR README with index
- [ ] Convert DD-001 to DD-010 to ADR format
- [ ] Archive IMPROVEMENTS_V1.md and IMPROVEMENTS_V2.md
- [ ] Move guides to docs/guides/
- [ ] Create initiatives/README.md

### Phase 2: Documentation Linting (In Progress)

- [ ] Install markdownlint-cli2
- [ ] Create .markdownlint.json config
- [ ] Install Vale
- [ ] Create .vale.ini config
- [ ] Create custom Vale styles for mcp-web
- [ ] Add docs:lint task to Taskfile
- [ ] Add docs:fix task for auto-fixes
- [ ] Clean all markdown files (remove double-spaces, artifacts)
- [ ] Add pre-commit hook for docs linting
- [ ] Add CI check for documentation quality

### Phase 3: Missing Tests

- [ ] **Query-Aware Tests** (10+ scenarios)
  - [ ] Simple query matching
  - [ ] Complex multi-term queries
  - [ ] Query with no matches
  - [ ] Query-focused chunk selection
  - [ ] Query in map-reduce context

- [ ] **Playwright Fallback Tests** (5+ scenarios)
  - [ ] Detect JS-rendered content
  - [ ] Fallback on httpx failure
  - [ ] Wait for network idle
  - [ ] Extract from SPA
  - [ ] Handle Playwright errors gracefully

- [ ] **robots.txt Tests** (5+ scenarios)
  - [ ] Respect robots.txt by default
  - [ ] Parse and check disallow rules
  - [ ] Handle crawl-delay
  - [ ] Ignore robots.txt when configured
  - [ ] Handle missing robots.txt

- [ ] **Edge Case Tests**
  - [ ] Very long documents (>100k tokens)
  - [ ] Binary content (images, PDFs)
  - [ ] Malformed HTML
  - [ ] Timeout handling
  - [ ] Network errors

### Phase 4: CLI Testing Endpoint

- [ ] Create `mcp_web.cli` module
- [ ] Add `test-summarize` command
  - [ ] Accept URL or multiple URLs
  - [ ] Accept query parameter
  - [ ] Show streaming output
  - [ ] Display metrics (tokens, time, method used)
  - [ ] Save output to file (optional)
- [ ] Add to Taskfile: `task test:manual URL=...`
- [ ] Add examples to TESTING_GUIDE.md

### Phase 5: mypy Improvements

- [ ] Review current mypy configuration
- [ ] Enable strict mode where feasible
- [ ] Fix all type errors
- [ ] Add missing type hints
- [ ] Add py.typed marker
- [ ] Document type checking standards

### Phase 6: Windsurf Rules Enhancement

- [ ] Add more external references to python.md
- [ ] Add code examples to security.md
- [ ] Link to ADRs from rules
- [ ] Link to CONSTITUTION.md from rules
- [ ] Add testing best practices section
- [ ] Add async patterns section with examples

---

## Timeline

### Week 1 (2025-10-15 to 2025-10-22)
- ✓ Document structure and constitution
- Documentation linting setup
- Begin missing tests

### Week 2 (2025-10-22 to 2025-10-29)
- Complete missing tests
- CLI testing endpoint
- mypy improvements

### Week 3 (2025-10-29 to 2025-11-05)
- Documentation cleanup
- Windsurf rules enhancement
- Integration and verification

### Week 4 (2025-11-05 to 2025-11-15)
- Final polish
- Documentation review
- Release v0.3.0

---

## Risks and Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Scope creep | Schedule slip | Fixed scope, defer non-critical items |
| Test complexity | Time overrun | Prioritize critical scenarios |
| Vale configuration | Quality blocker | Start with permissive config, tighten gradually |
| Breaking changes | User impact | Maintain backward compatibility |

---

## Dependencies

**Tools required:**
- markdownlint-cli2 (npm package)
- Vale (Go binary)
- pytest-asyncio (Python package)
- Additional pytest plugins

**External dependencies:**
- None (all self-contained)

---

## Metrics

**Current metrics (baseline):**
- Test coverage: ~85%
- Documentation quality: Unknown (no linting)
- Type coverage: ~70% (estimated)
- Double-spaces in docs: ~50 instances

**Target metrics:**
- Test coverage: ≥85%
- Documentation quality: 100% passing (markdownlint + Vale)
- Type coverage: ≥90%
- Double-spaces in docs: 0

---

## Related ADRs

- ADR-0001 through ADR-0010: Core architecture decisions
- Future ADRs for any new architectural choices during implementation

---

## Related Documentation

- [DOCUMENTATION_STRUCTURE.md](../DOCUMENTATION_STRUCTURE.md)
- [CONSTITUTION.md](../CONSTITUTION.md)
- [adr/README.md](../adr/README.md)
- [TESTING_GUIDE.md](../guides/TESTING_GUIDE.md) (to be created)

---

## Updates

### 2025-10-15 (Update 2)

**Completed:**
- ✓ Created comprehensive documentation structure
- ✓ Established project constitution with AI agent guidelines
- ✓ Set up ADR framework with template and README
- ✓ Created first ADR (0001-httpx-playwright-fallback)
- ✓ Created initiative structure and this document
- ✓ Set up markdown linting (.markdownlint.json)
- ✓ Set up prose linting (.vale.ini)
- ✓ Added docs:lint tasks to Taskfile
- ✓ Fixed Taskfile YAML syntax error
- ✓ Fixed benchmark test failure
- ✓ Created CLI module (test-summarize, test-robots commands)
- ✓ Added CLI test tasks to Taskfile
- ✓ Created query-aware summarization tests (12 scenarios)
- ✓ Created Playwright fallback tests (10+ test cases)
- ✓ Created robots.txt handling tests (15+ test cases)
- ✓ Improved mypy configuration
- ✓ Added click dependency
- ✓ Added robots.txt config fields to FetcherSettings

**In Progress:**
- Converting remaining decisions to ADR format
- Running full test suite
- Cleaning documentation of LLM artifacts

**Blockers:**
- None

**Next steps:**
- Convert DD-002 through DD-010 to ADR format
- Run full test suite and fix any failures
- Clean all markdown files (remove double-spaces)
- Archive IMPROVEMENTS_V1 and V2
- Move existing guides to docs/guides/
- Run documentation linters
- Commit progress

---

**Last Updated:** 2025-10-15
**Status:** Active - On Track

---

## Completion and Archival

When this initiative is complete, the `/archive-initiative` workflow will automatically move it to `completed/` directory during session end protocol. Do not manually move this file.
