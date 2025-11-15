"""Unit tests for extractor module.

Tests content extraction from HTML, PDF, and text files with mocked dependencies.
Covers trafilatura, pypdf, metadata extraction, caching, and error handling.
"""

import io
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from mcp_web.config import ExtractorSettings
from mcp_web.extractor import CodeSnippet, ContentExtractor, ExtractedContent
from mcp_web.fetcher import FetchResult


@pytest.mark.unit
class TestCodeSnippet:
    """Tests for CodeSnippet dataclass."""

    def test_code_snippet_creation(self):
        """Test creating a code snippet."""
        snippet = CodeSnippet(
            language="python",
            code='print("hello")',
            line_number=42,
        )

        assert snippet.language == "python"
        assert snippet.code == 'print("hello")'
        assert snippet.line_number == 42

    def test_code_snippet_without_line_number(self):
        """Test code snippet without line number."""
        snippet = CodeSnippet(language="javascript", code="console.log('test')")
        assert snippet.line_number is None


@pytest.mark.unit
class TestExtractedContent:
    """Tests for ExtractedContent dataclass."""

    def test_extracted_content_creation(self):
        """Test creating extracted content."""
        content = ExtractedContent(
            url="https://example.com",
            title="Test Page",
            content="# Test\n\nThis is content.",
            metadata={"author": "John Doe"},
            links=["https://example.org"],
            code_snippets=[CodeSnippet("python", "print('hi')")],
        )

        assert content.url == "https://example.com"
        assert content.title == "Test Page"
        assert "Test" in content.content
        assert content.metadata["author"] == "John Doe"
        assert len(content.links) == 1
        assert len(content.code_snippets) == 1

    def test_to_dict(self):
        """Test serialization to dictionary."""
        content = ExtractedContent(
            url="https://example.com",
            title="Test",
            content="Content",
            code_snippets=[CodeSnippet("python", "x = 1", 10)],
        )

        data = content.to_dict()

        assert data["url"] == "https://example.com"
        assert data["title"] == "Test"
        assert data["content"] == "Content"
        assert len(data["code_snippets"]) == 1
        assert data["code_snippets"][0]["language"] == "python"
        assert data["code_snippets"][0]["code"] == "x = 1"
        assert data["code_snippets"][0]["line_number"] == 10
        assert "timestamp" in data

    def test_from_dict(self):
        """Test deserialization from dictionary."""
        timestamp = datetime.now()
        data = {
            "url": "https://example.com",
            "title": "Test",
            "content": "Content",
            "metadata": {"key": "value"},
            "links": ["https://link.com"],
            "code_snippets": [{"language": "python", "code": "x = 1", "line_number": 5}],
            "timestamp": timestamp.isoformat(),
        }

        content = ExtractedContent.from_dict(data)

        assert content.url == "https://example.com"
        assert content.title == "Test"
        assert content.content == "Content"
        assert content.metadata == {"key": "value"}
        assert content.links == ["https://link.com"]
        assert len(content.code_snippets) == 1
        assert content.code_snippets[0].language == "python"
        assert content.timestamp.isoformat() == timestamp.isoformat()


@pytest.mark.unit
class TestContentExtractor:
    """Tests for ContentExtractor."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return ExtractorSettings(
            favor_recall=True,
            include_comments=True,
            include_tables=True,
            include_links=True,
            include_images=True,
            extract_metadata=True,
        )

    @pytest.fixture
    def extractor(self, config):
        """Create ContentExtractor instance."""
        return ContentExtractor(config)

    @pytest.fixture
    def sample_fetch_result(self, sample_html):
        """Create sample FetchResult."""
        return FetchResult(
            url="https://example.com/test",
            content=sample_html.encode("utf-8"),
            content_type="text/html; charset=utf-8",
            headers={"content-type": "text/html"},
            status_code=200,
            fetch_method="httpx",
        )

    @pytest.mark.asyncio
    async def test_extract_html_with_trafilatura(self, extractor, sample_html):
        """Test HTML extraction using trafilatura."""
        fetch_result = FetchResult(
            url="https://example.com",
            content=sample_html.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        with patch("mcp_web.extractor.trafilatura.extract") as mock_extract:
            mock_extract.return_value = "# Main Heading\n\nThis is the main content."

            result = await extractor.extract(fetch_result, use_cache=False)

            assert result.url == "https://example.com"
            assert result.title == "Test Page"
            assert "Main Heading" in result.content
            mock_extract.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_html_with_fallback(self, extractor, sample_html):
        """Test HTML extraction with trafilatura fallback."""
        fetch_result = FetchResult(
            url="https://example.com",
            content=sample_html.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        with patch("mcp_web.extractor.trafilatura.extract") as mock_extract, patch(
            "mcp_web.extractor.trafilatura.html2txt"
        ) as mock_html2txt:
            # trafilatura.extract returns None, triggering fallback
            mock_extract.return_value = None
            mock_html2txt.return_value = "Fallback content"

            result = await extractor.extract(fetch_result, use_cache=False)

            assert "Fallback content" in result.content
            mock_html2txt.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_html_with_metadata(self, extractor, sample_html):
        """Test HTML extraction with metadata."""
        fetch_result = FetchResult(
            url="https://example.com",
            content=sample_html.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        # Create mock metadata object
        mock_metadata = MagicMock()
        mock_metadata.title = "Metadata Title"
        mock_metadata.author = "Test Author"
        mock_metadata.date = "2025-11-15"
        mock_metadata.description = "Test description"
        mock_metadata.sitename = "Example Site"
        mock_metadata.tags = ["test", "example"]

        with patch("mcp_web.extractor.trafilatura.extract") as mock_extract, patch(
            "mcp_web.extractor.trafilatura.extract_metadata"
        ) as mock_extract_metadata:
            mock_extract.return_value = "Content"
            mock_extract_metadata.return_value = mock_metadata

            result = await extractor.extract(fetch_result, use_cache=False)

            assert result.metadata["author"] == "Test Author"
            assert result.metadata["date"] == "2025-11-15"
            assert result.metadata["description"] == "Test description"
            assert result.metadata["sitename"] == "Example Site"
            assert result.metadata["tags"] == ["test", "example"]

    @pytest.mark.asyncio
    async def test_extract_pdf(self, extractor):
        """Test PDF extraction."""
        # Create minimal PDF content (mock)
        pdf_content = b"%PDF-1.4\n%test content"
        fetch_result = FetchResult(
            url="https://example.com/doc.pdf",
            content=pdf_content,
            content_type="application/pdf",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        # Mock PdfReader
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page 1 content"

        mock_reader = MagicMock()
        mock_reader.pages = [mock_page]
        mock_reader.metadata = {
            "/Title": "Test PDF",
            "/Author": "Test Author",
            "/Subject": "Testing",
            "/Creator": "Test Creator",
        }

        with patch("mcp_web.extractor.PdfReader", return_value=mock_reader):
            result = await extractor.extract(fetch_result, use_cache=False)

            assert result.title == "Test PDF"
            assert "Page 1 content" in result.content
            assert result.metadata.get("author") == "Test Author"
            assert result.metadata.get("subject") == "Testing"

    @pytest.mark.asyncio
    async def test_extract_pdf_error_handling(self, extractor):
        """Test PDF extraction error handling."""
        pdf_content = b"%PDF-1.4\n%invalid"
        fetch_result = FetchResult(
            url="https://example.com/doc.pdf",
            content=pdf_content,
            content_type="application/pdf",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        with patch("mcp_web.extractor.PdfReader", side_effect=Exception("PDF parse error")):
            result = await extractor.extract(fetch_result, use_cache=False)

            # Should return minimal content on error
            assert result.url == "https://example.com/doc.pdf"
            assert result.content == ""
            assert "error" in result.metadata
            assert "PDF parse error" in result.metadata["error"]

    @pytest.mark.asyncio
    async def test_extract_markdown(self, extractor, sample_markdown):
        """Test Markdown file extraction."""
        fetch_result = FetchResult(
            url="https://example.com/doc.md",
            content=sample_markdown.encode("utf-8"),
            content_type="text/markdown",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        result = await extractor.extract(fetch_result, use_cache=False)

        assert result.url == "https://example.com/doc.md"
        assert result.title == "Introduction"  # First heading
        assert "Background" in result.content
        assert "Methods" in result.content
        assert len(result.code_snippets) > 0
        assert result.code_snippets[0].language == "python"

    @pytest.mark.asyncio
    async def test_extract_plain_text(self, extractor):
        """Test plain text extraction."""
        text_content = "This is plain text content.\nWith multiple lines.\nAnd paragraphs."
        fetch_result = FetchResult(
            url="https://example.com/doc.txt",
            content=text_content.encode("utf-8"),
            content_type="text/plain",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        result = await extractor.extract(fetch_result, use_cache=False)

        assert result.url == "https://example.com/doc.txt"
        assert result.content == text_content
        assert "plain text" in result.content

    @pytest.mark.asyncio
    async def test_extract_json(self, extractor):
        """Test JSON file extraction."""
        json_content = '{"key": "value", "data": [1, 2, 3]}'
        fetch_result = FetchResult(
            url="https://example.com/data.json",
            content=json_content.encode("utf-8"),
            content_type="application/json",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        result = await extractor.extract(fetch_result, use_cache=False)

        assert result.url == "https://example.com/data.json"
        assert "key" in result.content
        assert "value" in result.content

    @pytest.mark.asyncio
    async def test_extract_with_cache_hit(self, extractor, sample_fetch_result):
        """Test extraction with cache hit."""
        mock_cache = AsyncMock()
        cached_data = {
            "url": "https://example.com/test",
            "title": "Cached Page",
            "content": "Cached content",
            "metadata": {},
            "links": [],
            "code_snippets": [],
            "timestamp": datetime.now().isoformat(),
        }
        mock_cache.get.return_value = cached_data

        extractor.cache = mock_cache

        result = await extractor.extract(sample_fetch_result, use_cache=True)

        assert result.title == "Cached Page"
        assert result.content == "Cached content"
        mock_cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_with_cache_miss(self, extractor, sample_fetch_result):
        """Test extraction with cache miss."""
        mock_cache = AsyncMock()
        mock_cache.get.return_value = None

        extractor.cache = mock_cache

        with patch("mcp_web.extractor.trafilatura.extract") as mock_extract:
            mock_extract.return_value = "Extracted content"

            result = await extractor.extract(sample_fetch_result, use_cache=True)

            assert "Extracted content" in result.content
            mock_cache.get.assert_called_once()
            mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_extract_without_cache(self, extractor, sample_fetch_result):
        """Test extraction without using cache."""
        with patch("mcp_web.extractor.trafilatura.extract") as mock_extract:
            mock_extract.return_value = "Fresh content"

            result = await extractor.extract(sample_fetch_result, use_cache=False)

            assert "Fresh content" in result.content

    @pytest.mark.asyncio
    async def test_extract_code_snippets(self, extractor):
        """Test code snippet extraction from Markdown."""
        markdown = """
# Example

Some text.

```python
def hello():
    print("world")
```

More text.

```javascript
console.log('test');
```
"""
        snippets = extractor._extract_code_snippets(markdown)

        assert len(snippets) == 2
        assert snippets[0].language == "python"
        assert "def hello" in snippets[0].code
        assert snippets[1].language == "javascript"
        assert "console.log" in snippets[1].code

    @pytest.mark.asyncio
    async def test_extract_code_snippets_without_language(self, extractor):
        """Test code snippet extraction without language specifier."""
        markdown = """
```
generic code block
```
"""
        snippets = extractor._extract_code_snippets(markdown)

        assert len(snippets) == 1
        assert snippets[0].language == "text"
        assert "generic code block" in snippets[0].code

    def test_extract_title_from_html(self, extractor):
        """Test title extraction from HTML."""
        html = "<html><head><title>Test Title</title></head><body></body></html>"
        title = extractor._extract_title(html)
        assert title == "Test Title"

    def test_extract_title_from_h1(self, extractor):
        """Test title extraction from H1 tag."""
        html = "<html><body><h1>Main Heading</h1><p>Content</p></body></html>"
        title = extractor._extract_title(html)
        assert title == "Main Heading"

    def test_extract_title_with_fallback(self, extractor):
        """Test title extraction with fallback."""
        html = "<html><body><p>No title</p></body></html>"
        title = extractor._extract_title(html, fallback="Fallback Title")
        assert title == "Fallback Title"

    def test_extract_title_from_url(self, extractor):
        """Test title extraction from URL."""
        title = extractor._extract_title_from_url("https://example.com/my-page.html")
        assert title == "My Page"

        title = extractor._extract_title_from_url("https://example.com/docs/api-reference")
        assert title == "Api Reference"

        title = extractor._extract_title_from_url("https://example.com")
        assert title == "example.com"

    def test_extract_links(self, extractor):
        """Test link extraction from HTML."""
        html = """
        <html>
        <body>
            <a href="https://example.com/page1">Link 1</a>
            <a href="/relative/page">Link 2</a>
            <a href="#anchor">Anchor</a>
            <a href="javascript:void(0)">JS Link</a>
            <a href="https://example.org">External</a>
        </body>
        </html>
        """
        base_url = "https://example.com/base"
        links = extractor._extract_links(html, base_url)

        # Should extract absolute URLs and resolve relative ones
        assert "https://example.com/page1" in links
        assert "https://example.com/relative/page" in links
        assert "https://example.org" in links
        # Should skip anchors and javascript
        assert not any(link.startswith("#") for link in links)
        assert not any(link.startswith("javascript:") for link in links)

    def test_extract_links_deduplication(self, extractor):
        """Test that duplicate links are removed."""
        html = """
        <a href="https://example.com">Link</a>
        <a href="https://example.com">Duplicate</a>
        <a href="https://example.org">Other</a>
        """
        links = extractor._extract_links(html, "https://example.com")

        # Should have only 2 unique links
        assert len(links) == 2
        assert "https://example.com" in links
        assert "https://example.org" in links

    @pytest.mark.asyncio
    async def test_extract_error_handling(self, extractor):
        """Test extraction error handling and metrics."""
        fetch_result = FetchResult(
            url="https://example.com/error",
            content=b"content",
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="httpx",
        )

        with patch(
            "mcp_web.extractor.trafilatura.extract", side_effect=Exception("Extraction failed")
        ):
            with pytest.raises(Exception, match="Extraction failed"):
                await extractor.extract(fetch_result, use_cache=False)

    def test_extract_title_from_text(self, extractor):
        """Test title extraction from plain text content."""
        # Markdown heading
        text = "# Main Title\n\nContent here"
        title = extractor._extract_title_from_text(text, "https://example.com/doc")
        assert title == "Main Title"

        # First line
        text = "First line as title\nSecond line\nThird line"
        title = extractor._extract_title_from_text(text, "https://example.com/doc")
        assert title == "First line as title"

        # Long first line (should be truncated)
        long_line = "a" * 150
        text = f"{long_line}\nContent"
        title = extractor._extract_title_from_text(text, "https://example.com/doc")
        assert len(title) == 100

        # Empty text (should use URL)
        title = extractor._extract_title_from_text("", "https://example.com/my-doc.txt")
        assert title == "My Doc"

    @pytest.mark.asyncio
    async def test_extract_metrics_recording(self, extractor, sample_fetch_result):
        """Test that extraction metrics are recorded."""
        with patch("mcp_web.extractor.trafilatura.extract") as mock_extract:
            mock_extract.return_value = "Test content"

            # Mock metrics to verify calls
            with patch.object(extractor.metrics, "record_extraction") as mock_record:
                await extractor.extract(sample_fetch_result, use_cache=False)

                # Verify metrics were recorded
                mock_record.assert_called_once()
                call_args = mock_record.call_args
                assert call_args[1]["url"] == sample_fetch_result.url
                assert call_args[1]["success"] is True
