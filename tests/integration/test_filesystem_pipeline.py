"""Integration tests for file system summarization pipeline."""

import pytest

from mcp_web.config import Config
from mcp_web.mcp_server import WebSummarizationPipeline


class TestFileSystemPipeline:
    """Integration tests for file:// URL summarization."""

    @pytest.fixture
    def sample_files(self, tmp_path):
        """Create sample files for testing."""
        # Create a markdown document
        markdown = tmp_path / "document.md"
        markdown.write_text("""# Sample Document

This is a sample markdown document for testing file system summarization.

## Section 1

Some content in section 1.

## Section 2

More content in section 2.

### Subsection 2.1

Additional details here.
""")

        # Create a text file
        text = tmp_path / "notes.txt"
        text.write_text("""Meeting Notes

Date: 2025-10-20
Attendees: Team

Discussion points:
- File system support implementation
- Security considerations
- Testing strategy
""")

        return {
            "dir": tmp_path,
            "markdown": markdown,
            "text": text,
        }

    @pytest.fixture
    def pipeline(self, sample_files):
        """Create pipeline with file system enabled."""
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(sample_files["dir"])]

        pipeline = WebSummarizationPipeline(config)
        yield pipeline

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_fetch_local_markdown_file(self, pipeline, sample_files):
        """Test fetching local markdown file."""
        fetch_results = await pipeline.fetcher.fetch_multiple([str(sample_files["markdown"])])

        assert len(fetch_results) == 1
        result = list(fetch_results.values())[0]

        assert result.status_code == 200
        assert result.fetch_method == "filesystem"
        assert b"Sample Document" in result.content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_extract_from_local_file(self, pipeline, sample_files):
        """Test extraction from local file."""
        # Fetch file
        fetch_result = await pipeline.fetcher.fetch(str(sample_files["markdown"]))

        # Extract content
        extracted = await pipeline.extractor.extract(fetch_result, use_cache=False)

        assert extracted is not None
        assert "Sample Document" in extracted.title or "Sample Document" in extracted.content
        assert len(extracted.content) > 0

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_chunk_local_file_content(self, pipeline, sample_files):
        """Test chunking content from local file."""
        # Fetch and extract
        fetch_result = await pipeline.fetcher.fetch(str(sample_files["markdown"]))
        extracted = await pipeline.extractor.extract(fetch_result, use_cache=False)

        # Chunk
        chunks = pipeline.chunker.chunk_text(extracted.content)

        assert len(chunks) > 0
        assert all(chunk.tokens > 0 for chunk in chunks)

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.requires_api
    @pytest.mark.asyncio
    async def test_full_pipeline_with_local_file(self, pipeline, sample_files):
        """Test full summarization pipeline with local file (requires LLM)."""
        urls = [str(sample_files["markdown"])]

        try:
            summary_parts = []
            async for chunk in pipeline.summarize_urls(urls):
                summary_parts.append(chunk)

            summary = "".join(summary_parts)

            # Verify we got output
            assert len(summary) > 0

            # Check for expected sections
            assert "Fetching" in summary or "Summary" in summary

        except Exception as e:
            # Skip if API key not configured
            if "API" in str(e) or "key" in str(e).lower():
                pytest.skip(f"API key not configured: {str(e)}")
            else:
                raise

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_mixed_url_and_file_fetching(self, pipeline, sample_files):
        """Test fetching mix of HTTP URLs and file:// URLs."""
        urls = [
            "https://example.com",
            str(sample_files["text"]),
        ]

        try:
            results = await pipeline.fetcher.fetch_multiple(urls)

            # Should have at least the local file
            assert len(results) >= 1

            # Check if local file was fetched
            local_results = [r for r in results.values() if r.fetch_method == "filesystem"]
            assert len(local_results) >= 1

        except Exception as e:
            # Network errors are acceptable for this test
            if "example.com" not in str(e).lower():
                raise

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_file_url_with_file_scheme(self, pipeline, sample_files):
        """Test file:// URL scheme."""
        file_url = f"file://{sample_files['text']}"

        result = await pipeline.fetcher.fetch(file_url)

        assert result.status_code == 200
        assert result.fetch_method == "filesystem"
        assert b"Meeting Notes" in result.content

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_handling_missing_file(self, pipeline, sample_files):
        """Test error handling for missing file."""
        missing_file = str(sample_files["dir"] / "does-not-exist.txt")

        with pytest.raises(FileNotFoundError):
            await pipeline.fetcher.fetch(missing_file)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_security_unauthorized_access(self, sample_files):
        """Test security prevents unauthorized file access."""
        # Create pipeline with restrictive allowed directories
        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = ["/tmp/nonexistent"]

        pipeline = WebSummarizationPipeline(config)

        try:
            # Attempt to access file outside allowed directory
            with pytest.raises(PermissionError):
                await pipeline.fetcher.fetch(str(sample_files["text"]))
        finally:
            await pipeline.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_multiple_file_summarization(self, pipeline, sample_files):
        """Test summarizing multiple local files."""
        urls = [
            str(sample_files["markdown"]),
            str(sample_files["text"]),
        ]

        results = await pipeline.fetcher.fetch_multiple(urls)

        assert len(results) == 2
        assert all(r.status_code == 200 for r in results.values())
        assert all(r.fetch_method == "filesystem" for r in results.values())


class TestFileSystemContentExtraction:
    """Test content extraction from various file types."""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_extract_markdown_preserves_structure(self, tmp_path):
        """Test markdown extraction preserves structure."""
        markdown_file = tmp_path / "test.md"
        markdown_file.write_text("""# Title

## Section 1

Content with **bold** and *italic*.

- List item 1
- List item 2

## Section 2

More content.
""")

        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(tmp_path)]

        pipeline = WebSummarizationPipeline(config)

        try:
            fetch_result = await pipeline.fetcher.fetch(str(markdown_file))
            extracted = await pipeline.extractor.extract(fetch_result, use_cache=False)

            # Check structure is preserved
            assert "Title" in extracted.content
            assert "Section 1" in extracted.content
            assert "Section 2" in extracted.content

        finally:
            await pipeline.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_extract_plain_text(self, tmp_path):
        """Test plain text extraction."""
        text_file = tmp_path / "plain.txt"
        text_file.write_text("Simple plain text content.\nMultiple lines.\n")

        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(tmp_path)]

        pipeline = WebSummarizationPipeline(config)

        try:
            fetch_result = await pipeline.fetcher.fetch(str(text_file))
            extracted = await pipeline.extractor.extract(fetch_result, use_cache=False)

            assert "Simple plain text content" in extracted.content
            assert "Multiple lines" in extracted.content

        finally:
            await pipeline.close()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_extract_python_code(self, tmp_path):
        """Test Python code file extraction."""
        python_file = tmp_path / "code.py"
        python_file.write_text("""#!/usr/bin/env python3
\"\"\"Module docstring.\"\"\"

def hello():
    \"\"\"Function docstring.\"\"\"
    print("Hello, world!")

if __name__ == "__main__":
    hello()
""")

        config = Config()
        config.fetcher.enable_file_system = True
        config.fetcher.allowed_directories = [str(tmp_path)]

        pipeline = WebSummarizationPipeline(config)

        try:
            fetch_result = await pipeline.fetcher.fetch(str(python_file))

            # Should fetch successfully
            assert fetch_result.status_code == 200
            assert fetch_result.content_type == "text/x-python"
            assert b"def hello():" in fetch_result.content

        finally:
            await pipeline.close()
