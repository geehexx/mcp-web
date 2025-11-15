"""Unit tests for CLI module.

Tests command-line interface commands with mocked async operations,
URL summarization, robots.txt checking, output formatting, and error handling.
"""

import asyncio
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import nest_asyncio
import pytest
from click.testing import CliRunner

from mcp_web.chunker import Chunk
from mcp_web.cli import cli, test_robots, test_summarize
from mcp_web.extractor import ExtractedContent
from mcp_web.fetcher import FetchResult

# Apply nest_asyncio to allow asyncio.run() in CLI commands during testing
nest_asyncio.apply()


@pytest.mark.unit
class TestCLICommands:
    """Tests for CLI command structure."""

    @pytest.fixture
    def runner(self):
        """Create Click test runner."""
        return CliRunner()

    def test_cli_group_exists(self, runner):
        """Test that CLI group is defined."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "MCP-Web CLI" in result.output

    def test_test_summarize_command_exists(self, runner):
        """Test that test-summarize command exists."""
        result = runner.invoke(cli, ["test-summarize", "--help"])
        assert result.exit_code == 0
        assert "Test URL summarization" in result.output

    def test_test_robots_command_exists(self, runner):
        """Test that test-robots command exists."""
        result = runner.invoke(cli, ["test-robots", "--help"])
        assert result.exit_code == 0
        assert "Test robots.txt" in result.output


@pytest.mark.unit
class TestSummarizeCommand:
    """Tests for test-summarize command."""

    @pytest.fixture
    def runner(self):
        """Create Click test runner."""
        return CliRunner()

    @pytest.fixture
    def mock_fetch_result(self):
        """Create mock fetch result."""
        return FetchResult(
            url="https://example.com",
            content=b"<html><body><h1>Test</h1><p>Content</p></body></html>",
            content_type="text/html",
            headers={"content-type": "text/html"},
            status_code=200,
            fetch_method="httpx",
        )

    @pytest.fixture
    def mock_extracted_content(self):
        """Create mock extracted content."""
        return ExtractedContent(
            url="https://example.com",
            title="Test Page",
            content="# Test\n\nThis is test content.",
            metadata={"author": "Test Author"},
            links=["https://example.org"],
            code_snippets=[],
        )

    @pytest.fixture
    def mock_chunks(self):
        """Create mock chunks."""
        return [
            Chunk(
                text="First chunk of text",
                tokens=50,
                start_pos=0,
                end_pos=20,
                metadata={},
            ),
            Chunk(
                text="Second chunk of text",
                tokens=50,
                start_pos=20,
                end_pos=40,
                metadata={},
            ),
        ]

    def test_basic_summarize(self, runner, mock_fetch_result, mock_extracted_content, mock_chunks):
        """Test basic URL summarization."""
        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.ContentExtractor") as mock_extractor_class, \
             patch("mcp_web.cli.TextChunker") as mock_chunker_class, \
             patch("mcp_web.cli.Summarizer") as mock_summarizer_class:

            # Setup mocks
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.return_value = mock_fetch_result
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = mock_extracted_content
            mock_extractor_class.return_value = mock_extractor

            mock_chunker = Mock()
            mock_chunker.chunk_text.return_value = mock_chunks
            mock_chunker_class.return_value = mock_chunker

            # Create a proper mock class that returns async generator
            class MockSummarizer:
                async def summarize_chunks(self, *args, **kwargs):
                    yield "Test summary "
                    yield "content here."

                async def close(self):
                    pass

            mock_summarizer = MockSummarizer()
            mock_summarizer_class.return_value = mock_summarizer

            # Run command
            result = runner.invoke(
                cli,
                ["test-summarize", "https://example.com", "--no-metrics"],
                catch_exceptions=False,
            )

            if result.exit_code != 0:
                print(f"CLI Output:\n{result.output}")
                print(f"Exception: {result.exception}")
            assert result.exit_code == 0

    def test_summarize_with_query(self, runner):
        """Test summarization with query parameter."""
        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.ContentExtractor") as mock_extractor_class, \
             patch("mcp_web.cli.TextChunker") as mock_chunker_class, \
             patch("mcp_web.cli.Summarizer") as mock_summarizer_class:

            # Setup minimal mocks
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.return_value = FetchResult(
                url="https://example.com",
                content=b"content",
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="httpx",
            )
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = ExtractedContent(
                url="https://example.com",
                title="Test",
                content="Test content",
            )
            mock_extractor_class.return_value = mock_extractor

            mock_chunker = Mock()
            mock_chunker.chunk_text.return_value = [
                Chunk(text="chunk", tokens=10, start_pos=0, end_pos=5)
            ]
            mock_chunker_class.return_value = mock_chunker

            # Create a proper mock class that returns async generator
            class MockSummarizer:
                async def summarize_chunks(self, *args, **kwargs):
                    # Verify query was passed
                    assert kwargs.get("query") == "test query"
                    yield "Summary"

                async def close(self):
                    pass

            mock_summarizer = MockSummarizer()
            mock_summarizer_class.return_value = mock_summarizer

            result = runner.invoke(
                cli,
                [
                    "test-summarize",
                    "https://example.com",
                    "--query",
                    "test query",
                    "--no-metrics",
                ],
                catch_exceptions=False,
            )

            assert result.exit_code == 0

    def test_summarize_with_provider(self, runner):
        """Test summarization with different provider."""
        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.ContentExtractor") as mock_extractor_class, \
             patch("mcp_web.cli.TextChunker") as mock_chunker_class, \
             patch("mcp_web.cli.Summarizer") as mock_summarizer_class:

            # Setup mocks
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.return_value = FetchResult(
                url="https://example.com",
                content=b"content",
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="httpx",
            )
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = ExtractedContent(
                url="https://example.com",
                title="Test",
                content="Content",
            )
            mock_extractor_class.return_value = mock_extractor

            mock_chunker = Mock()
            mock_chunker.chunk_text.return_value = [
                Chunk(text="chunk", tokens=10, start_pos=0, end_pos=5)
            ]
            mock_chunker_class.return_value = mock_chunker

            # Create a proper mock class that returns async generator
            class MockSummarizer:
                async def summarize_chunks(self, *args, **kwargs):
                    yield "Summary"

                async def close(self):
                    pass

            mock_summarizer = MockSummarizer()
            mock_summarizer_class.return_value = mock_summarizer

            result = runner.invoke(
                cli,
                [
                    "test-summarize",
                    "https://example.com",
                    "--provider",
                    "ollama",
                    "--model",
                    "llama3.2",
                    "--no-metrics",
                ],
                catch_exceptions=False,
            )

            assert result.exit_code == 0

    def test_summarize_multiple_urls(self, runner):
        """Test summarization of multiple URLs."""
        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.ContentExtractor") as mock_extractor_class, \
             patch("mcp_web.cli.TextChunker") as mock_chunker_class, \
             patch("mcp_web.cli.Summarizer") as mock_summarizer_class:

            # Setup mocks
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.return_value = FetchResult(
                url="https://example.com",
                content=b"content",
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="httpx",
            )
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = ExtractedContent(
                url="https://example.com",
                title="Test",
                content="Content",
            )
            mock_extractor_class.return_value = mock_extractor

            mock_chunker = Mock()
            mock_chunker.chunk_text.return_value = [
                Chunk(text="chunk", tokens=10, start_pos=0, end_pos=5)
            ]
            mock_chunker_class.return_value = mock_chunker

            # Create a proper mock class that returns async generator
            class MockSummarizer:
                async def summarize_chunks(self, *args, **kwargs):
                    yield "Summary"

                async def close(self):
                    pass

            mock_summarizer = MockSummarizer()
            mock_summarizer_class.return_value = mock_summarizer

            result = runner.invoke(
                cli,
                [
                    "test-summarize",
                    "https://example.com",
                    "https://example.org",
                    "--no-metrics",
                ],
                catch_exceptions=False,
            )

            assert result.exit_code == 0

    def test_summarize_with_output_file(self, runner, tmp_path):
        """Test saving summary to file."""
        output_file = tmp_path / "summary.md"

        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.ContentExtractor") as mock_extractor_class, \
             patch("mcp_web.cli.TextChunker") as mock_chunker_class, \
             patch("mcp_web.cli.Summarizer") as mock_summarizer_class:

            # Setup mocks
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.return_value = FetchResult(
                url="https://example.com",
                content=b"content",
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="httpx",
            )
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = ExtractedContent(
                url="https://example.com",
                title="Test",
                content="Content",
            )
            mock_extractor_class.return_value = mock_extractor

            mock_chunker = Mock()
            mock_chunker.chunk_text.return_value = [
                Chunk(text="chunk", tokens=10, start_pos=0, end_pos=5)
            ]
            mock_chunker_class.return_value = mock_chunker

            # Create a proper mock class that returns async generator
            class MockSummarizer:
                async def summarize_chunks(self, *args, **kwargs):
                    yield "Test summary content"

                async def close(self):
                    pass

            mock_summarizer = MockSummarizer()
            mock_summarizer_class.return_value = mock_summarizer

            result = runner.invoke(
                cli,
                [
                    "test-summarize",
                    "https://example.com",
                    "--output",
                    str(output_file),
                    "--no-metrics",
                ],
                catch_exceptions=False,
            )

            assert result.exit_code == 0
            assert output_file.exists()
            content = output_file.read_text()
            assert "https://example.com" in content
            assert "Test summary content" in content

    def test_summarize_verbose_mode(self, runner):
        """Test verbose output mode."""
        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.ContentExtractor") as mock_extractor_class, \
             patch("mcp_web.cli.TextChunker") as mock_chunker_class, \
             patch("mcp_web.cli.Summarizer") as mock_summarizer_class:

            # Setup mocks
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.return_value = FetchResult(
                url="https://example.com",
                content=b"content",
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="httpx",
            )
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = ExtractedContent(
                url="https://example.com",
                title="Test Page",
                content="Content",
                metadata={"author": "Test"},
            )
            mock_extractor_class.return_value = mock_extractor

            mock_chunker = Mock()
            mock_chunker.chunk_text.return_value = [
                Chunk(text="chunk", tokens=10, start_pos=0, end_pos=5)
            ]
            mock_chunker_class.return_value = mock_chunker

            # Create a proper mock class that returns async generator
            class MockSummarizer:
                async def summarize_chunks(self, *args, **kwargs):
                    yield "Summary"

                async def close(self):
                    pass

            mock_summarizer = MockSummarizer()
            mock_summarizer_class.return_value = mock_summarizer

            result = runner.invoke(
                cli,
                [
                    "test-summarize",
                    "https://example.com",
                    "--verbose",
                    "--no-metrics",
                ],
                catch_exceptions=False,
            )

            assert result.exit_code == 0
            # Verbose mode should show additional details
            assert "Provider:" in result.output or "Title:" in result.output

    def test_summarize_error_handling(self, runner):
        """Test error handling in summarization."""
        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class:
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.side_effect = Exception("Network error")
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            result = runner.invoke(
                cli,
                ["test-summarize", "https://example.com"],
                catch_exceptions=False,
            )

            # Should handle error gracefully
            assert result.exit_code == 1
            assert "Error" in result.output or "error" in result.output.lower()


@pytest.mark.unit
class TestRobotsCommand:
    """Tests for test-robots command."""

    @pytest.fixture
    def runner(self):
        """Create Click test runner."""
        return CliRunner()

    def test_robots_txt_found(self, runner):
        """Test robots.txt found and parsed."""
        robots_content = b"""
User-agent: *
Disallow: /admin/
Allow: /

Crawl-delay: 1
"""

        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class:
            mock_fetcher = AsyncMock()

            async def mock_fetch(url):
                if "robots.txt" in url:
                    return FetchResult(
                        url=url,
                        content=robots_content,
                        content_type="text/plain",
                        headers={},
                        status_code=200,
                        fetch_method="httpx",
                    )
                else:
                    return FetchResult(
                        url=url,
                        content=b"<html><body>Test</body></html>",
                        content_type="text/html",
                        headers={},
                        status_code=200,
                        fetch_method="httpx",
                    )

            mock_fetcher.fetch.side_effect = mock_fetch
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            result = runner.invoke(
                cli,
                ["test-robots", "https://example.com/test"],
                catch_exceptions=False,
            )

            assert result.exit_code == 0
            assert "robots.txt found" in result.output

    def test_robots_txt_not_found(self, runner):
        """Test when robots.txt is not found."""
        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class:
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.side_effect = Exception("404 Not Found")
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            result = runner.invoke(
                cli,
                ["test-robots", "https://example.com/test"],
                catch_exceptions=False,
            )

            # Should handle gracefully
            assert result.exit_code == 0 or "404" in result.output

    def test_robots_disallow(self, runner):
        """Test when URL is disallowed by robots.txt."""
        robots_content = b"""
User-agent: *
Disallow: /admin/
"""

        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class:
            mock_fetcher = AsyncMock()

            async def mock_fetch(url):
                if "robots.txt" in url:
                    return FetchResult(
                        url=url,
                        content=robots_content,
                        content_type="text/plain",
                        headers={},
                        status_code=200,
                        fetch_method="httpx",
                    )
                raise Exception("Should not fetch disallowed URL")

            mock_fetcher.fetch.side_effect = mock_fetch
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            result = runner.invoke(
                cli,
                ["test-robots", "https://example.com/admin/secret"],
                catch_exceptions=False,
            )

            assert result.exit_code == 0

    def test_robots_ignore_flag(self, runner):
        """Test --ignore flag to bypass robots.txt."""
        robots_content = b"""
User-agent: *
Disallow: /
"""

        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class:
            mock_fetcher = AsyncMock()

            async def mock_fetch(url):
                if "robots.txt" in url:
                    return FetchResult(
                        url=url,
                        content=robots_content,
                        content_type="text/plain",
                        headers={},
                        status_code=200,
                        fetch_method="httpx",
                    )
                else:
                    return FetchResult(
                        url=url,
                        content=b"<html><body>Test</body></html>",
                        content_type="text/html",
                        headers={},
                        status_code=200,
                        fetch_method="httpx",
                    )

            mock_fetcher.fetch.side_effect = mock_fetch
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            result = runner.invoke(
                cli,
                ["test-robots", "https://example.com/test", "--ignore"],
                catch_exceptions=False,
            )

            assert result.exit_code == 0


@pytest.mark.unit
class TestCLIHelpers:
    """Tests for CLI helper functions and edge cases."""

    @pytest.fixture
    def runner(self):
        """Create Click test runner."""
        return CliRunner()

    def test_cli_no_arguments(self, runner):
        """Test CLI with no arguments shows help."""
        result = runner.invoke(cli, [])
        # Click groups exit with code 2 when no subcommand is provided
        assert result.exit_code == 2
        assert "MCP-Web CLI" in result.output

    def test_test_summarize_requires_url(self, runner):
        """Test that test-summarize requires URL argument."""
        result = runner.invoke(cli, ["test-summarize"])
        assert result.exit_code != 0

    def test_test_robots_requires_url(self, runner):
        """Test that test-robots requires URL argument."""
        result = runner.invoke(cli, ["test-robots"])
        assert result.exit_code != 0

    def test_invalid_provider(self, runner):
        """Test invalid provider value."""
        result = runner.invoke(
            cli,
            ["test-summarize", "https://example.com", "--provider", "invalid"],
        )
        # Should show error about invalid choice
        assert result.exit_code != 0


@pytest.mark.unit
class TestAsyncImplementations:
    """Tests for async implementation details."""

    @pytest.mark.asyncio
    async def test_test_summarize_async_basic(self):
        """Test async implementation of test-summarize."""
        from mcp_web.cli import _test_summarize_async

        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.ContentExtractor") as mock_extractor_class, \
             patch("mcp_web.cli.TextChunker") as mock_chunker_class, \
             patch("mcp_web.cli.Summarizer") as mock_summarizer_class, \
             patch("mcp_web.cli.click.echo") as mock_echo:

            # Setup mocks
            mock_fetcher = AsyncMock()
            mock_fetcher.fetch.return_value = FetchResult(
                url="https://example.com",
                content=b"content",
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="httpx",
            )
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            mock_extractor = AsyncMock()
            mock_extractor.extract.return_value = ExtractedContent(
                url="https://example.com",
                title="Test",
                content="Content",
            )
            mock_extractor_class.return_value = mock_extractor

            mock_chunker = Mock()
            mock_chunker.chunk_text.return_value = [
                Chunk(text="chunk", tokens=10, start_pos=0, end_pos=5)
            ]
            mock_chunker_class.return_value = mock_chunker

            # Create a proper mock class that returns async generator
            class MockSummarizer:
                async def summarize_chunks(self, *args, **kwargs):
                    yield "Summary"

                async def close(self):
                    pass

            mock_summarizer = MockSummarizer()
            mock_summarizer_class.return_value = mock_summarizer

            # Call async function
            await _test_summarize_async(
                urls=["https://example.com"],
                query=None,
                provider="openai",
                model=None,
                output=None,
                show_metrics=False,
                verbose=False,
            )

            # Verify fetcher was used
            mock_fetcher.fetch.assert_called_once()
            mock_fetcher.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_test_robots_async_basic(self):
        """Test async implementation of test-robots."""
        from mcp_web.cli import _test_robots_async

        robots_content = b"User-agent: *\nAllow: /"

        with patch("mcp_web.cli.URLFetcher") as mock_fetcher_class, \
             patch("mcp_web.cli.click.echo"):

            mock_fetcher = AsyncMock()

            async def mock_fetch(url):
                return FetchResult(
                    url=url,
                    content=robots_content if "robots.txt" in url else b"content",
                    content_type="text/plain" if "robots.txt" in url else "text/html",
                    headers={},
                    status_code=200,
                    fetch_method="httpx",
                )

            mock_fetcher.fetch.side_effect = mock_fetch
            mock_fetcher.close = AsyncMock()
            mock_fetcher_class.return_value = mock_fetcher

            # Call async function
            await _test_robots_async("https://example.com", ignore=False)

            # Verify robots.txt was fetched
            assert any("robots.txt" in str(call) for call in mock_fetcher.fetch.call_args_list)
