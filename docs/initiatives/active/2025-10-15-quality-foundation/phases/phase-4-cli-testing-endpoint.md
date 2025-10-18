# Phase 4: CLI Testing Endpoint

**Status:** ✓ Completed 2025-10-15 (95% complete)
**Duration:** 1 day
**Owner:** Core Team

---

## Objective

Create CLI commands for manual testing and verification of summarization and robots.txt handling.

---

## Tasks

- [x] Create `mcp_web.cli` module
- [x] Add `test-summarize` command
- [x] Accept URL or multiple URLs
- [x] Accept query parameter
- [x] Show streaming output
- [x] Display metrics (tokens, time, method used)
- [x] Save output to file (optional)
- [x] Add to Taskfile: `task test:manual URL=...`
- [x] Add `test-robots` command for robots.txt testing
- [ ] Add examples to TESTING_GUIDE.md (deferred)

---

## CLI Commands Created

### `mcp-web test-summarize`

```bash
mcp-web test-summarize https://example.com [--query "search term"] [--output file.txt]
```

Features:

- Fetch and summarize URLs
- Optional query for focused summarization
- Show streaming progress
- Display metrics (tokens, timing, fetch method)
- Save to file

### `mcp-web test-robots`

```bash
mcp-web test-robots https://example.com
```

Features:

- Fetch and parse robots.txt
- Check if URL is allowed
- Display crawl-delay if specified
- Show disallowed patterns

---

## Deliverables

- ✅ `src/mcp_web/cli.py` - CLI module with test commands
- ✅ `Taskfile.yml` - task test:manual command added
- ✅ `pyproject.toml` - CLI entry points configured

---

## Usage Examples

```bash
# Test summarization
mcp-web test-summarize https://python.org

# Query-focused test
mcp-web test-summarize https://docs.python.org --query "decorators"

# Check robots.txt
mcp-web test-robots https://example.com

# Via Taskfile
task test:manual URL=https://example.com
```

---

## Completion Notes

CLI testing endpoints fully functional. Fixed import errors for TextChunker, Config, and CacheManager. Both commands working as expected. Documentation examples deferred to future update.
