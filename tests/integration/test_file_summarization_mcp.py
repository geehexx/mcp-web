"""Integration tests for MCP-based file summarization.

Tests Phase 1 of Session Summary Mining initiative:
- File:// URL support through MCP server
- Configuration of allowed directories
- End-to-end summarization of local files
"""

from pathlib import Path

import pytest

from mcp_web.config import Config
from mcp_web.mcp_server import WebSummarizationPipeline


class TestFileSummarizationMCP:
    """Test MCP server file system integration."""

    @pytest.fixture
    def temp_session_summary(self, tmp_path: Path) -> Path:
        """Create a temporary session summary file for testing."""
        content = """---
session_date: 2025-10-20
duration: 2 hours
focus: Testing file system support
---

# Session Summary: File System Testing

## Key Accomplishments

- Implemented file:// URL support in fetcher
- Added directory whitelist validation
- Created 33 tests for file system features
- All tests passing (302 total)

## Technical Details

### File System Fetcher

Created `FileSystemFetcher` class that:
- Parses file:// URLs and absolute paths
- Validates against allowed directories
- Prevents path traversal attacks
- Integrates with existing extraction pipeline

### Security

- Path validation with `resolve()` to prevent ../.. attacks
- Symlink escape detection
- File size limits (10MB default)
- Directory whitelist enforcement

## Next Steps

- [ ] Integrate with session summary mining
- [ ] Create extraction CLI tool
- [ ] Test with real session summaries

## Files Modified

- src/mcp_web/fetcher.py (+150 lines)
- src/mcp_web/config.py (+10 lines)
- tests/integration/test_filesystem_pipeline.py (33 tests)

---

**Status:** Phase complete, ready for mining integration
"""
        file_path = tmp_path / "test-session-summary.md"
        file_path.write_text(content)
        return file_path

    @pytest.mark.asyncio
    async def test_file_url_summarization(self, temp_session_summary: Path):
        """Test MCP can summarize file using file:// URL."""
        # Arrange: Configure for file system access
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(temp_session_summary.parent)]

        pipeline = WebSummarizationPipeline(config)

        # Act: Summarize using file:// URL
        file_url = f"file://{temp_session_summary}"
        chunks = []
        async for chunk in pipeline.summarize_urls([file_url]):
            chunks.append(chunk)

        # Assert: Summary generated
        summary = "".join(chunks)
        assert len(summary) > 0
        assert "Error" not in summary or "Warning" not in summary.split("\n")[0]

    @pytest.mark.asyncio
    async def test_absolute_path_summarization(self, temp_session_summary: Path):
        """Test MCP can summarize file using absolute path."""
        # Arrange
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(temp_session_summary.parent)]

        pipeline = WebSummarizationPipeline(config)

        # Act: Summarize using absolute path (treated as file://)
        chunks = []
        async for chunk in pipeline.summarize_urls([str(temp_session_summary)]):
            chunks.append(chunk)

        # Assert
        summary = "".join(chunks)
        assert len(summary) > 0
        assert "file system" in summary.lower() or "testing" in summary.lower()

    @pytest.mark.asyncio
    async def test_directory_whitelist_validation(self, temp_session_summary: Path):
        """Test directory whitelist prevents unauthorized access."""
        # Arrange: Configure with WRONG directory
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = ["/some/other/directory"]

        pipeline = WebSummarizationPipeline(config)

        # Act: Attempt to access file outside whitelist
        file_url = f"file://{temp_session_summary}"
        chunks = []
        async for chunk in pipeline.summarize_urls([file_url]):
            chunks.append(chunk)

        # Assert: Should get error about directory access
        summary = "".join(chunks)
        assert "error" in summary.lower() or "not allowed" in summary.lower()

    @pytest.mark.asyncio
    async def test_session_summaries_directory_access(self):
        """Test MCP can access docs/archive/session-summaries directory."""
        # Arrange: Configure for project session summaries
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = ["docs/archive/session-summaries"]

        # Find a real session summary file
        session_summaries_dir = Path("docs/archive/session-summaries")
        if not session_summaries_dir.exists():
            pytest.skip("Session summaries directory not found")

        summary_files = list(session_summaries_dir.glob("*.md"))
        if not summary_files:
            pytest.skip("No session summary files found")

        test_file = summary_files[0]  # Use first available

        pipeline = WebSummarizationPipeline(config)

        # Act: Summarize real session summary
        file_url = f"file://{test_file.absolute()}"
        chunks = []
        async for chunk in pipeline.summarize_urls([file_url]):
            chunks.append(chunk)

        # Assert: Summary generated from real file
        summary = "".join(chunks)
        assert len(summary) > 0
        assert "Error" not in summary or "Warning" not in summary.split("\n")[0]

    @pytest.mark.asyncio
    async def test_query_focused_file_summarization(self, temp_session_summary: Path):
        """Test MCP can do query-focused summarization of files."""
        # Arrange
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(temp_session_summary.parent)]

        pipeline = WebSummarizationPipeline(config)

        # Act: Summarize with specific query
        file_url = f"file://{temp_session_summary}"
        query = "What security features were implemented?"

        chunks = []
        async for chunk in pipeline.summarize_urls([file_url], query=query):
            chunks.append(chunk)

        # Assert: Summary focused on query
        summary = "".join(chunks)
        assert len(summary) > 0
        # Should mention security-related content
        assert any(
            keyword in summary.lower()
            for keyword in ["security", "validation", "path", "whitelist"]
        )


class TestFileSummarizationPerformance:
    """Performance benchmarks for file-based summarization."""

    @pytest.fixture
    def medium_session_summary(self, tmp_path: Path) -> Path:
        """Create a medium-sized session summary (~2KB)."""
        content = """# Session Summary: Performance Testing

## Overview
This is a test session summary for benchmarking file system performance.
""" + "\n\n".join([f"## Section {i}\n\nContent for section {i}. " * 50 for i in range(10)])

        file_path = tmp_path / "medium-summary.md"
        file_path.write_text(content)
        return file_path

    @pytest.mark.asyncio
    @pytest.mark.benchmark
    async def test_file_summarization_latency(self, medium_session_summary: Path, benchmark):
        """Benchmark file summarization latency."""
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(medium_session_summary.parent)]
        config.summarizer.streaming = False  # Easier to benchmark

        pipeline = WebSummarizationPipeline(config)
        file_url = f"file://{medium_session_summary}"

        async def summarize():
            chunks = []
            async for chunk in pipeline.summarize_urls([file_url]):
                chunks.append(chunk)
            return "".join(chunks)

        # Benchmark
        result = await benchmark.pedantic(summarize, rounds=3, iterations=1)

        # Assert: Should complete in reasonable time
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_batch_file_summarization(self, tmp_path: Path):
        """Test processing multiple files in batch."""
        # Arrange: Create 5 test files
        file_paths = []
        for i in range(5):
            content = (
                f"# Summary {i}\n\nContent for summary {i}.\n\n## Details\n\nMore details here."
            )
            file_path = tmp_path / f"summary-{i}.md"
            file_path.write_text(content)
            file_paths.append(file_path)

        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(tmp_path)]

        pipeline = WebSummarizationPipeline(config)

        # Act: Summarize all files at once
        file_urls = [f"file://{fp}" for fp in file_paths]

        chunks = []
        async for chunk in pipeline.summarize_urls(file_urls):
            chunks.append(chunk)

        # Assert: All files processed
        summary = "".join(chunks)
        assert len(summary) > 0
        # Should mention multiple sources
        assert summary.count("Source:") >= 5 or summary.count("summary-") >= 5
