---
Status: Active
Created: 2025-10-19
Owner: AI Agent
Priority: Medium
Estimated Duration: 12-15 hours
Target Completion: 2025-12-01
Updated: 2025-10-19
---

# Initiative: Session Summary Mining - Advanced Automation

---

## Objective

Implement advanced LLM-based automation for session summary mining using MCP server's file system support, enabling scalable extraction, deduplication, and initiative mapping with minimal manual effort.

## Success Criteria

- [ ] LLM-based extraction pipeline using MCP server internally
- [ ] Pydantic schemas for structured action item extraction
- [ ] Multi-level deduplication (text + semantic + contextual)
- [ ] Automated initiative mapping and creation
- [ ] Processing 100+ summaries in <10 minutes
- [ ] ≥85% extraction accuracy (precision & recall)
- [ ] SQLite logging for quality tracking
- [ ] Integration with `/consolidate-summaries` workflow

---

## Motivation

**Problem:**

- Manual extraction works for 21 summaries but doesn't scale to 100+
- Deduplication requires tedious manual comparison
- Initiative mapping is time-consuming and error-prone
- Need automation for ongoing summary mining (weekly/monthly)

**Impact:**

- **Without this:** Hours of manual work per analysis cycle
- **With this:** Automated mining runs in minutes, scalable to any volume
- **Quality:** Consistent extraction using validated LLM patterns

**Value:**

- **Scalability:** Handle 100+ summaries with one command
- **Consistency:** Pydantic schemas ensure structured, validated output
- **Intelligence:** LLM understands context better than regex patterns
- **Foundation:** Research (Phase 1) already complete, ready to implement

---

## Scope

### In Scope

- LLM extraction pipeline (from Phase 2 research)
- Pydantic `ActionItem` schema with validation
- MCP server integration for file-based summarization
- Multi-level deduplication algorithm
- Automated initiative mapping logic
- SQLite logging for extraction tracking
- YAML output format (30% token efficiency)
- Enhanced `/consolidate-summaries` workflow
- Tests (unit + integration + golden)

### Out of Scope

- Real-time monitoring / alerting - future enhancement
- Web UI for extraction review - future enhancement
- Non-session-summary files (code, docs) - separate use case
- Multi-language support - English only for now

---

## Tasks

### Phase 1: MCP Integration (2 hours) ✅ COMPLETE

- [x] Update extraction script to use MCP `summarize_urls` with file:// URLs
- [x] Configure allowed directories for file system access
- [x] Test file-based summarization end-to-end
- [x] Benchmark MCP vs direct LLM API (expect similar performance)

### Phase 2: Extraction Pipeline (4 hours)

(Already designed in original initiative artifacts)

- [ ] Implement `ActionItem` Pydantic schema
- [ ] Create extraction prompts (system + user templates)
- [ ] Implement section-based extraction
- [ ] Add validation and error handling
- [ ] Create SQLite logging infrastructure

### Phase 3: Deduplication (3 hours)

- [ ] Implement Level 1: Text similarity (TF-IDF + cosine)
- [ ] Implement Level 2: Semantic similarity (LLM embeddings)
- [ ] Implement Level 3: Contextual comparison (same initiative/files)
- [ ] Create deduplication pipeline (Level 1 → 2 → 3)
- [ ] Add human review export for borderline cases (60-85% similarity)

### Phase 4: Initiative Mapping (2 hours)

- [ ] Implement initiative cross-reference algorithm
- [ ] Load active + completed initiatives
- [ ] Semantic matching (description similarity)
- [ ] File overlap analysis (related_files)
- [ ] Auto-create initiative logic (impact=high AND confidence=high)

### Phase 5: Integration & Testing (3 hours)

- [ ] Integrate with `/consolidate-summaries` workflow
- [ ] Create CLI: `task mine:summaries --date-range 2025-10-15:2025-10-19`
- [ ] Write tests (unit + integration + golden)
- [ ] Dry-run validation on test summaries
- [ ] Performance benchmarking

---

## Blockers

**Current Blockers:**

- **MCP File System Support** (External)
  - Type: Feature dependency
  - Impact: HIGH - Cannot use MCP for local files without this
  - Resolution: Wait for [MCP File System Support](../2025-10-19-mcp-file-system-support/initiative.md) to complete
  - ETA: 2025-11-10

**Resolved Blockers:**

- None

---

## Dependencies

**Internal Dependencies:**

- **MCP File System Support** (Initiative) ⚠️ BLOCKING
  - Status: Active (not started)
  - Critical Path: Yes - required for file-based summarization
  - Notes: Cannot proceed until file:// URL support implemented

- **Session Summary Consolidation Workflow** (Initiative)
  - Status: Active
  - Critical Path: No - provides manual process as fallback
  - Notes: Manual workflow validates automation requirements

**External Dependencies:**

- **OpenAI/Claude API** - Available (already using for MCP server)
- **Python libraries** - instructor, pydantic, scikit-learn (need to add)

**Prerequisite Initiatives:**

- [MCP File System Support](../2025-10-19-mcp-file-system-support/initiative.md) must complete

**Blocks These Initiatives:**

- None (nice-to-have automation, not blocking other work)

---

## Related Initiatives

**Synergistic:**

- [MCP File System Support](../2025-10-19-mcp-file-system-support/initiative.md) - Required dependency
- [Session Summary Consolidation Workflow](../2025-10-19-session-summary-consolidation-workflow/initiative.md) - Manual process validates automation
- [Workflow Automation Enhancement](../2025-10-18-workflow-automation-enhancement/initiative.md) - Similar automation philosophy (Phase 2-6)

**Sequential Work:**

- [Session Summary Consolidation](../2025-10-19-session-summary-consolidation-workflow/initiative.md) → [MCP File System](../2025-10-19-mcp-file-system-support/initiative.md) → This initiative

---

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| MCP file support delayed | High | Low | Use manual workflow, defer automation |
| Extraction accuracy <85% | High | Medium | Extensive prompt engineering, golden tests, human review |
| Deduplication false positives | Medium | Medium | Human review step for borderline cases (60-85%) |
| LLM API costs high | Low | Medium | Batch processing, caching, use gpt-4o-mini for extraction |
| Performance slower than expected | Low | Low | Parallel processing, optimize prompts |

---

## Timeline

### Prerequisite: MCP File System Support (ETA: 2025-11-10)

Cannot start until prerequisite complete.

- **Week 1 (2h):** MCP integration
- **Week 2 (4h):** Extraction pipeline
- **Week 3 (3h):** Deduplication
- **Week 4 (2h):** Initiative mapping
- **Week 5 (3h):** Integration & testing

**Total:** 14 hours across 5 weeks (starts after MCP file support)

---

## Related Documentation

**From Original Research (Reusable):**

- [Research Summary](../2025-10-19-session-summary-mining-system/artifacts/research-summary.md) - Extraction best practices, Pydantic patterns
- [Summary Analysis](../2025-10-19-session-summary-mining-system/artifacts/summary-analysis.md) - 21 summaries analyzed, patterns identified
- [Phase 2 Design](../2025-10-19-session-summary-mining-system/phases/phase-2-extraction-pipeline.md) - Detailed technical design

**MCP Server:**

- [API Documentation](../../api/API.md)
- [Architecture](../../architecture/ARCHITECTURE.md)

---

## Updates

### 2025-10-19 (Creation)

Initiative created as "LATER" split from original comprehensive mining system.

**Why Deferred:**

- MCP file system support needed first (avoid reinventing wheel)
- Manual workflow sufficient for current 21 summaries
- Research complete, ready to implement when unblocked
- Pragmatic: good-enough now, advanced automation later

**Why Worth Doing Later:**

- Scalability: Manual process doesn't scale to 100+ summaries
- Reuse: Leverage MCP summarization (DRY principle)
- Quality: LLM extraction more consistent than manual
- Foundation: Research (Phase 1) complete, design validated

**Blocked By:**

- [MCP File System Support](../2025-10-19-mcp-file-system-support/initiative.md) - ETA 2025-11-10

**Next (When Unblocked):**

- Phase 1: MCP integration with file:// URLs

---

## Progress Updates

### 2025-10-20 - Phase 1 Complete ✅

**Completed:**

- Fixed MCP pipeline URL validation to accept file:// URLs and absolute paths
- Created `scripts/extract_action_items.py` with date range and batch processing
- Added 6 integration tests for file summarization (all passing)
- All 308 tests passing

**Deliverables:**

- `scripts/extract_action_items.py` - CLI tool for action item extraction
- `tests/integration/test_file_summarization_mcp.py` - 6 integration tests
- MCP pipeline now supports absolute path → file:// URL conversion

**Next:** Phase 2 - Extraction Pipeline (Pydantic schemas, prompts, validation)

---

**Last Updated:** 2025-10-20
**Status:** Active (Phase 1 complete, Phase 2 ready)
