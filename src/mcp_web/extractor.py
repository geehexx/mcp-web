"""Content extraction from HTML and PDF.

Uses:
- HTML: trafilatura (main content extraction)
- PDF: pypdf + pdfplumber (text extraction)

Design Decision DD-002: Trafilatura with favor_recall=True.
Design Decision DD-005: Preserve code blocks and tables in Markdown.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import structlog
import trafilatura
from pypdf import PdfReader

from mcp_web.cache import CacheKeyBuilder, CacheManager
from mcp_web.config import ExtractorSettings
from mcp_web.fetcher import FetchResult
from mcp_web.metrics import get_metrics_collector

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


@dataclass
class CodeSnippet:
    """Extracted code snippet."""

    language: str
    code: str
    line_number: int | None = None


@dataclass
class ExtractedContent:
    """Extracted content with metadata."""

    url: str
    title: str
    content: str  # Markdown formatted
    metadata: dict[str, Any] = field(default_factory=dict)
    links: list[str] = field(default_factory=list)
    code_snippets: list[CodeSnippet] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "metadata": self.metadata,
            "links": self.links,
            "code_snippets": [
                {"language": cs.language, "code": cs.code, "line_number": cs.line_number}
                for cs in self.code_snippets
            ],
            "timestamp": self.timestamp.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExtractedContent":
        """Create from dictionary."""
        code_snippets = [CodeSnippet(**cs) for cs in data.get("code_snippets", [])]
        return cls(
            url=data["url"],
            title=data["title"],
            content=data["content"],
            metadata=data.get("metadata", {}),
            links=data.get("links", []),
            code_snippets=code_snippets,
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )


class ContentExtractor:
    """Extract main content from HTML and PDF.

    Example:
        >>> extractor = ContentExtractor(config)
        >>> result = await extractor.extract(fetch_result)
        >>> print(result.title)
        'Example Page'
    """

    def __init__(
        self,
        config: ExtractorSettings,
        cache: CacheManager | None = None,
    ):
        """Initialize content extractor.

        Args:
            config: Extractor configuration
            cache: Optional cache manager
        """
        self.config = config
        self.cache = cache
        self.metrics = get_metrics_collector()

    async def extract(
        self,
        fetch_result: FetchResult,
        use_cache: bool = True,
    ) -> ExtractedContent:
        """Extract content from fetch result.

        Args:
            fetch_result: Result from URLFetcher
            use_cache: Use cached extraction if available

        Returns:
            ExtractedContent with main content and metadata

        Raises:
            Exception: If extraction fails
        """
        import time

        url = fetch_result.url
        _get_logger().info("extract_start", url=url)

        # Check cache
        if use_cache and self.cache:
            cache_key = CacheKeyBuilder.extract_key(url)
            cached = await self.cache.get(cache_key)
            if cached:
                _get_logger().info("extract_cache_hit", url=url)
                return ExtractedContent.from_dict(cached)

        start_time = time.perf_counter()

        try:
            # Determine content type
            content_type = fetch_result.content_type.lower()

            if "pdf" in content_type or fetch_result.url.endswith(".pdf"):
                result = await self._extract_pdf(fetch_result)
            else:
                result = await self._extract_html(fetch_result)

            duration_ms = (time.perf_counter() - start_time) * 1000

            self.metrics.record_extraction(
                url=url,
                content_length=len(fetch_result.content),
                extracted_length=len(result.content),
                duration_ms=duration_ms,
                success=True,
            )

            # Cache result
            if use_cache and self.cache:
                cache_key = CacheKeyBuilder.extract_key(url)
                await self.cache.set(cache_key, result.to_dict())

            _get_logger().info(
                "extract_success",
                url=url,
                title=result.title,
                content_length=len(result.content),
                duration_ms=round(duration_ms, 2),
            )

            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.record_extraction(
                url=url,
                content_length=len(fetch_result.content),
                extracted_length=0,
                duration_ms=duration_ms,
                success=False,
                error=str(e),
            )
            _get_logger().error("extract_failed", url=url, error=str(e))
            self.metrics.record_error("extractor", e, {"url": url})
            raise

    async def _extract_html(self, fetch_result: FetchResult) -> ExtractedContent:
        """Extract content from HTML using trafilatura.

        Args:
            fetch_result: Fetch result with HTML content

        Returns:
            ExtractedContent
        """
        html = fetch_result.content.decode("utf-8", errors="ignore")
        url = fetch_result.url

        # Extract with trafilatura
        extracted = trafilatura.extract(
            html,
            url=url,
            include_comments=self.config.include_comments,
            include_tables=self.config.include_tables,
            include_links=self.config.include_links,
            include_images=self.config.include_images,
            output_format="markdown",
            favor_recall=self.config.favor_recall,
            with_metadata=self.config.extract_metadata,
        )

        if not extracted:
            # Fallback to html2txt
            extracted = trafilatura.html2txt(html)
            _get_logger().warning("trafilatura_fallback", url=url)

        # Extract metadata
        metadata = {}
        if self.config.extract_metadata:
            metadata_obj = trafilatura.extract_metadata(html, default_url=url)
            if metadata_obj:
                metadata = {
                    "author": metadata_obj.author,
                    "date": metadata_obj.date,
                    "description": metadata_obj.description,
                    "sitename": metadata_obj.sitename,
                    "tags": metadata_obj.tags,
                }

        # Extract title
        title = self._extract_title(html, metadata.get("title"))

        # Extract links
        links = []
        if self.config.include_links:
            links = self._extract_links(html, url)

        # Extract code snippets
        code_snippets = self._extract_code_snippets(extracted or "")

        return ExtractedContent(
            url=url,
            title=title,
            content=extracted or "",
            metadata=metadata,
            links=links,
            code_snippets=code_snippets,
        )

    async def _extract_pdf(self, fetch_result: FetchResult) -> ExtractedContent:
        """Extract content from PDF.

        Args:
            fetch_result: Fetch result with PDF content

        Returns:
            ExtractedContent
        """
        import io

        url = fetch_result.url
        pdf_bytes = io.BytesIO(fetch_result.content)

        try:
            reader = PdfReader(pdf_bytes)

            # Extract text from all pages
            text_parts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)

            content = "\n\n".join(text_parts)

            # Extract metadata
            metadata = {}
            if reader.metadata:
                metadata = {
                    "title": reader.metadata.get("/Title", ""),
                    "author": reader.metadata.get("/Author", ""),
                    "subject": reader.metadata.get("/Subject", ""),
                    "creator": reader.metadata.get("/Creator", ""),
                }

            title = metadata.get("title") or self._extract_title_from_url(url)

            return ExtractedContent(
                url=url,
                title=title,
                content=content,
                metadata=metadata,
                links=[],
                code_snippets=self._extract_code_snippets(content),
            )

        except Exception as e:
            _get_logger().error("pdf_extraction_failed", url=url, error=str(e))
            # Return minimal content on failure
            return ExtractedContent(
                url=url,
                title=self._extract_title_from_url(url),
                content="",
                metadata={"error": str(e)},
            )

    def _extract_title(self, html: str, fallback: str | None = None) -> str:
        """Extract page title from HTML.

        Args:
            html: HTML content
            fallback: Fallback title

        Returns:
            Extracted title
        """
        # Try <title> tag
        title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
        if title_match:
            return title_match.group(1).strip()

        # Try <h1> tag
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
        if h1_match:
            return re.sub(r"<[^>]+>", "", h1_match.group(1)).strip()

        return fallback or "Untitled"

    def _extract_title_from_url(self, url: str) -> str:
        """Extract title from URL path.

        Args:
            url: URL string

        Returns:
            Title derived from URL
        """
        from urllib.parse import urlparse

        parsed = urlparse(url)
        path = parsed.path.rstrip("/")

        if path:
            # Get last path segment
            title = path.split("/")[-1]
            # Remove file extension
            title = re.sub(r"\.\w+$", "", title)
            # Replace separators with spaces
            title = re.sub(r"[-_]", " ", title)
            return title.title()

        return parsed.netloc or "Untitled"

    def _extract_links(self, html: str, base_url: str) -> list[str]:
        """Extract links from HTML.

        Args:
            html: HTML content
            base_url: Base URL for resolving relative links

        Returns:
            List of absolute URLs
        """
        from urllib.parse import urljoin, urlparse

        link_pattern = r'<a[^>]+href=["\'](.*?)["\']'
        matches = re.findall(link_pattern, html, re.IGNORECASE)

        links = []
        for link in matches:
            # Skip anchors and javascript
            if link.startswith("#") or link.startswith("javascript:"):
                continue

            # Resolve to absolute URL
            absolute_url = urljoin(base_url, link)

            # Validate
            parsed = urlparse(absolute_url)
            if parsed.scheme in ("http", "https"):
                links.append(absolute_url)

        # Deduplicate while preserving order
        seen = set()
        return [url for url in links if not (url in seen or seen.add(url))]

    def _extract_code_snippets(self, markdown: str) -> list[CodeSnippet]:
        """Extract code blocks from Markdown.

        Args:
            markdown: Markdown content

        Returns:
            List of CodeSnippet objects
        """
        pattern = r"```(\w+)?\n(.*?)```"
        matches = re.findall(pattern, markdown, re.DOTALL)

        snippets = []
        for language, code in matches:
            snippets.append(
                CodeSnippet(
                    language=language or "text",
                    code=code.strip(),
                )
            )

        return snippets
