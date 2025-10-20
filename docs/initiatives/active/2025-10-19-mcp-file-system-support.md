---
Status: Active
Created: 2025-10-19
Owner: AI Agent
Priority: Medium
Estimated Duration: 6-8 hours
Target Completion: 2025-11-10
Updated: 2025-10-20
---

# Initiative: MCP Server File System Support

---

## Objective

Extend MCP server to support local file system paths (file:// URLs and direct file paths) in addition to HTTP/HTTPS URLs, enabling internal use of summarization capabilities for session summaries, documentation, and other local files.

## Success Criteria

- [x] MCP server accepts `file://` URLs for summarization
- [x] MCP server accepts absolute file paths directly
- [x] File content extraction working (markdown, text, code files)
- [x] Same summarization quality as URL-based content
- [x] Security: Path traversal prevention, allowed directories only
- [x] Tests: Unit + integration tests for file-based summarization
- [ ] Documentation: API examples for file system usage
- [x] Backward compatible: Existing URL functionality unchanged

---

## Motivation

**Problem:**

- MCP server currently only supports HTTP/HTTPS URLs
- Cannot leverage internal summarization for local files (session summaries, docs, code)
- Would need to duplicate summarization logic for file-based workflows
- Missing opportunity to dogfood our own tools

**Impact:**

- **Without this:** Separate LLM extraction pipelines needed for local files (code duplication)
- **With this:** Single summarization system for URLs + files (DRY principle)
- **Unblocks:** Advanced session summary mining automation (blocked initiative)

**Value:**

- **Code reuse:** Leverage existing summarization pipeline for local files
- **Consistency:** Same quality/approach for remote + local content
- **Foundation:** Enables future file-based workflows (code summarization, doc generation)
- **Dogfooding:** Use our tools internally, improve through real use

---

## Scope

### In Scope

- Accept `file://` URLs in `summarize_urls` tool
- Accept absolute file paths (e.g., `/home/user/file.md`)
- Support common text formats: markdown, text, code files
- Security: Whitelist allowed directories (project root, docs/, etc.)
- Error handling: File not found, permission denied, unsupported format
- Tests for file-based summarization
- Documentation and examples

### Out of Scope

- Binary file support (PDF, DOCX, images) - future enhancement
- Recursive directory summarization - future enhancement
- Watch mode / file change monitoring - future enhancement
- glob patterns (`*.md`) - can be handled by caller
- Relative paths (require absolute or file:// only)

---

## Tasks

### Phase 1: Research & Design (1 hour) ✅ COMPLETE

- [x] Research Python file:// URL handling (urllib.parse)
- [x] Design allowed directory whitelist (config-based)
- [x] Design path traversal prevention (pathlib.resolve + validation)
- [x] Review httpx integration points for file fetching
- [x] Design error handling for file operations

### Phase 2: Implementation (3-4 hours) ✅ COMPLETE

- [x] Create `FileSystemFetcher` class (parallel to httpx/Playwright)
- [x] Implement file:// URL parsing
- [x] Implement absolute path handling
- [x] Add allowed directory validation
- [x] Integrate with existing content extraction pipeline
- [x] Handle text encoding detection
- [x] Error handling (file not found, permissions, encoding)

### Phase 3: Testing (2 hours) ✅ COMPLETE

- [x] Unit tests: URL parsing, path validation, whitelist
- [x] Integration tests: End-to-end file summarization
- [x] Security tests: Path traversal attempts, unauthorized access
- [x] Edge cases: Symlinks, special characters, large files

### Phase 4: Documentation (0.5-1 hour)

- [ ] Update API.md with file system examples
- [ ] Update MCP tool documentation
- [ ] Add security considerations section
- [ ] Create usage examples (session summaries, docs)

---

## Blockers

**Current Blockers:**

- None (can start immediately)

**Resolved Blockers:**

- None

---

## Dependencies

**Internal Dependencies:**

- **MCP Server Core** (Code)
  - Status: Active, stable
  - Critical Path: Yes (must not break existing URL functionality)
  - Notes: Ensure backward compatibility

**External Dependencies:**

- **Python pathlib** - Built-in, no additional dependency
- **Python urllib.parse** - Built-in, for file:// URL handling

**Prerequisite Initiatives:**

- None

**Blocks These Initiatives:**

- [Session Summary Mining - Advanced Automation](../2025-10-19-session-summary-mining-advanced/initiative.md) - Waiting for file system support to use MCP internally

---

## Related Initiatives

**Synergistic:**

- [Session Summary Mining - Advanced](../2025-10-19-session-summary-mining-advanced/initiative.md) - Primary use case for file system support
- [MCP Server Core](../2025-10-15-performance-optimization-pipeline/initiative.md) - Extends existing summarization capabilities

**Sequential Work:**

- This initiative → [Session Summary Mining - Advanced](../2025-10-19-session-summary-mining-advanced/initiative.md)

---

## Risks and Mitigation

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Security: path traversal | High | Low | Strict whitelist validation, pathlib.resolve() |
| Breaking URL functionality | High | Low | Comprehensive backward compatibility tests |
| File encoding issues | Medium | Medium | Detect encoding (chardet), fallback to UTF-8 |
| Large file performance | Low | Medium | Add file size limits (config), streaming for large files |
| Permission errors | Low | High | Clear error messages, document allowed directories |

---

## Timeline

- **Week 1 (1h):** Research & design
- **Week 2 (3-4h):** Implementation
- **Week 3 (2h):** Testing
- **Week 3 (0.5-1h):** Documentation

**Total:** 6.5-8 hours across 3 weeks

---

## Related Documentation

- [MCP Server Architecture](../../architecture/ARCHITECTURE.md)
- [API Documentation](../../api/API.md)
- [Security Architecture](../../architecture/SECURITY_ARCHITECTURE.md)
- [ADR-0001: httpx/Playwright Fallback](../../adr/0001-use-httpx-playwright-fallback.md) - Related fetching strategy

---

## Updates

### 2025-10-19 (Creation)

Initiative created to unblock advanced session summary mining automation.

**Key Decisions:**

- Start with text formats only (markdown, code, text)
- Whitelist allowed directories for security
- Keep simple: absolute paths or file:// URLs (no relative paths)
- Defer binary formats (PDF, DOCX) to future enhancement

**Motivation:**

- Enable dogfooding: use MCP summarization internally for local files
- Unblock advanced automation: LLM-based extraction can leverage MCP server
- Avoid duplication: single summarization system for URLs + files

**Next:** Phase 1 research and design

### 2025-10-20 (Implementation Complete)

Phases 1-3 completed in single session (~4 hours).

**Implementation:**

- Added file system support to `URLFetcher` with `_fetch_file()` method
- Added text extraction to `ContentExtractor` with `_extract_text()` method
- Configuration: `allowed_directories`, `max_file_size`, `enable_file_system` settings
- Security: Path validation via `_validate_file_path()`, whitelist enforcement, symlink resolution
- Helper functions: `_parse_file_url()` for URL/path parsing

**Testing:**

- 22 unit tests covering parsing, validation, fetching, security
- 11 integration tests covering pipeline, extraction, mixed URL/file usage
- All 302 tests passing (including 33 new file system tests)
- Security validated: path traversal blocked, symlink escape prevented

**Achievements:**

- ✅ Core functionality complete (Phases 1-3)
- ✅ All success criteria met except documentation
- ✅ Backward compatible (existing tests unchanged)
- ✅ Unblocks session summary mining automation

**Remaining:**

- Phase 4: Documentation (API examples, usage guide)

**Next:** Add API documentation and usage examples

---

**Last Updated:** 2025-10-20
**Status:** Active (Phase 4 - Documentation)
