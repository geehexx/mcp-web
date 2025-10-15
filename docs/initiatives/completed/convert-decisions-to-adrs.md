# Initiative: Convert Legacy Decisions to ADR Format

**Status:** Complete
**Created:** 2025-10-15
**Completed:** 2025-10-15
**Priority:** High
**Owner:** AI Agent
**Completed:** 2025-10-15
**Actual Duration:** 1.5 hours

---

## Objective

Convert DD-002 through DD-010 from `DECISIONS.md` to proper ADR format in `docs/adr/`, following the established template and best practices.

---

## Success Criteria

- [x] ADR-0001 exists (httpx/Playwright - already done)
- [x] ADR-0002 exists (Windsurf workflows - already done)
- [x] ADR-0003 exists (Documentation standards - already done)
- [x] ADR-0004: Trafilatura for content extraction (DD-002)
- [x] ADR-0005: Hierarchical + semantic chunking (DD-003)
- [x] ADR-0006: 512-token chunks with 50-token overlap (DD-004)
- [x] ADR-0007: tiktoken for token counting (DD-005)
- [x] ADR-0008: Map-reduce summarization strategy (DD-006)
- [x] ADR-0009: Disk cache with 7-day TTL (DD-007)
- [x] ADR-0010: OpenAI GPT-4 as default LLM (DD-008)
- [x] ADR-0011: Streaming output (DD-009)
- [x] ADR-0012: Monolithic tool design (DD-010)
- [x] Archive DECISIONS.md to docs/archive/

---

## Implementation Strategy

### Commit Strategy (Intelligent Commits)

**Principle:** Commit after each logical unit of work, not just at the end.

**Pattern:**

- **Per ADR:** Commit each ADR individually (allows easy revert if needed)
- **Grouping:** Can group 2-3 related ADRs if they're small
- **Archival:** Separate commit for archiving DECISIONS.md

**Benefits:**

- Clear history (one ADR per commit)
- Easy rollback (can revert specific ADR)
- Better code review (smaller diffs)
- Continuous integration (tests after each commit)

### Phase 1: Content Extraction (ADR-0004)

**Input:** DD-002 from DECISIONS.md
**Output:** docs/adr/0004-trafilatura-content-extraction.md
**Commit:** `docs(adr): add ADR-0004 trafilatura content extraction`

### Phase 2: Chunking Strategy (ADR-0005, ADR-0006)

**Input:** DD-003, DD-004 from DECISIONS.md
**Output:**

- docs/adr/0005-hierarchical-semantic-chunking.md
- docs/adr/0006-chunk-size-and-overlap.md
**Commit:** `docs(adr): add ADR-0005 and ADR-0006 chunking strategy`
**Rationale:** These two are closely related (chunking approach + parameters)

### Phase 3: Token Counting (ADR-0007)

**Input:** DD-005 from DECISIONS.md
**Output:** docs/adr/0007-tiktoken-token-counting.md
**Commit:** `docs(adr): add ADR-0007 tiktoken token counting`

### Phase 4: Summarization (ADR-0008)

**Input:** DD-006 from DECISIONS.md
**Output:** docs/adr/0008-map-reduce-summarization.md
**Commit:** `docs(adr): add ADR-0008 map-reduce summarization strategy`

### Phase 5: Caching (ADR-0009)

**Input:** DD-007 from DECISIONS.md
**Output:** docs/adr/0009-disk-cache-ttl.md
**Commit:** `docs(adr): add ADR-0009 disk caching strategy`

### Phase 6: LLM Selection (ADR-0010, ADR-0011)

**Input:** DD-008, DD-009 from DECISIONS.md
**Output:**

- docs/adr/0010-openai-gpt4-default-llm.md
- docs/adr/0011-streaming-output.md
**Commit:** `docs(adr): add ADR-0010 and ADR-0011 LLM and streaming`
**Rationale:** LLM choice and streaming are related UX decisions

### Phase 7: Architecture (ADR-0012)

**Input:** DD-010 from DECISIONS.md
**Output:** docs/adr/0012-monolithic-tool-design.md
**Commit:** `docs(adr): add ADR-0012 monolithic tool design`

### Phase 8: Cleanup

**Actions:**

- Update ADR README with all new ADRs
- Archive DECISIONS.md to docs/archive/
**Commit:** `docs(adr): update index and archive legacy DECISIONS.md`

---

## Medium-Term Documentation Items

### ADRs to Create (Future)

Based on previous session decisions:

1. **ADR-0013: uv Package Manager Adoption** (from comprehensive-overhaul)
 - Context: Replaced pip with uv for 10x speed improvement
 - Decision: Use uv for all package operations
 - Rationale: Performance, reproducibility, better dependency resolution

2. **ADR-0014: pytest-xdist Parallelization** (from comprehensive-overhaul)
 - Context: Tests were slow (225s sequential)
 - Decision: Use pytest-xdist with IO-optimized worker count (16)
 - Rationale: 7.5x speedup for IO-bound tests

3. **ADR-0015: Pre-commit Hooks** (from comprehensive-overhaul)
 - Context: Need automated quality enforcement
 - Decision: Use pre-commit framework with ruff, vale, markdownlint
 - Rationale: Catch issues before commit, consistent formatting

4. **ADR-0016: Windsurf Rules Structure** (from comprehensive-overhaul)
 - Context: Need AI agent guidance system
 - Decision: Numbered priority system (00-04) with trigger types
 - Rationale: Clear precedence, intelligent rule application

5. **ADR-0017: Documentation Linting** (from quality foundation)
 - Context: Documentation quality inconsistent
 - Decision: markdownlint-cli2 + Vale with Microsoft style
 - Rationale: Automated quality, AI-friendly docs

### Guides to Create

1. **docs/guides/TESTING_GUIDE.md**
 - How to run tests
 - Test markers and categories
 - Parallel testing with pytest-xdist
 - Writing new tests

2. **docs/guides/CONTRIBUTING_GUIDE.md** (expand existing CONTRIBUTING.md)
 - Development setup with uv
 - Workflow usage
 - ADR creation process
 - Commit conventions

3. **docs/guides/DEPLOYMENT_GUIDE.md** (expand existing DEPLOYMENT.md)
 - Production deployment
 - Configuration management
 - Monitoring and logging
 - Troubleshooting

---

## Timeline

**Estimated total:** 2-3 hours

- Phase 1-8 ADR creation: 2 hours (15-20 min per ADR)
- Cleanup and validation: 30 minutes
- Medium-term documentation: Deferred to future initiatives

---

## References

- ADR template: docs/adr/template.md
- Existing ADRs: docs/adr/0001-_.md, 0002-_.md, 0003-*.md
- Legacy decisions: docs/DECISIONS.md
- ADR best practices: https://adr.github.io/

---

**Last Updated:** 2025-10-15
**Status:** Complete - All success criteria met
