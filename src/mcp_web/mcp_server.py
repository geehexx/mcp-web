"""MCP Server for web summarization.

Implements the monolithic 'summarize_urls' tool that:
1. Fetches URLs (httpx + Playwright fallback)
2. Extracts content (trafilatura)
3. Chunks intelligently
4. Summarizes with LLM (map-reduce)
5. Streams Markdown output

Design Decision DD-010: Monolithic tool design.
"""

from collections.abc import AsyncIterator
from typing import Any

import structlog
from mcp.server.fastmcp import FastMCP

from mcp_web.cache import CacheManager
from mcp_web.chunker import TextChunker
from mcp_web.config import Config, load_config
from mcp_web.extractor import ContentExtractor
from mcp_web.fetcher import URLFetcher
from mcp_web.metrics import configure_logging, get_metrics_collector
from mcp_web.summarizer import Summarizer
from mcp_web.utils import validate_url

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


class WebSummarizationPipeline:
    """Orchestrates the full summarization pipeline.

    Example:
        >>> pipeline = WebSummarizationPipeline(config)
        >>> async for chunk in pipeline.summarize_urls(["https://example.com"]):
        ...     print(chunk)
    """

    def __init__(self, config: Config):
        """Initialize pipeline.

        Args:
            config: Application configuration
        """
        self.config = config

        # Initialize cache
        self.cache = (
            CacheManager(
                cache_dir=config.cache.cache_dir,
                ttl=config.cache.ttl,
                max_size=config.cache.max_size,
                eviction_policy=config.cache.eviction_policy,
            )
            if config.cache.enabled
            else None
        )

        # Initialize components
        self.fetcher = URLFetcher(config.fetcher, cache=self.cache)
        self.extractor = ContentExtractor(config.extractor, cache=self.cache)
        self.chunker = TextChunker(config.chunker)
        self.summarizer = Summarizer(config.summarizer)

        self.metrics = get_metrics_collector()

    async def summarize_urls(
        self,
        urls: list[str],
        query: str | None = None,
        follow_links: bool = False,
        max_depth: int = 1,
    ) -> AsyncIterator[str]:
        """Summarize content from URLs.

        Args:
            urls: List of URLs to summarize
            query: Optional query for focused summary
            follow_links: Whether to follow outbound links
            max_depth: Maximum link following depth

        Yields:
            Summary text chunks (streaming)
        """
        _get_logger().info(
            "pipeline_start",
            num_urls=len(urls),
            query=query[:50] if query else None,
            follow_links=follow_links,
        )

        try:
            # Step 1: Validate URLs
            valid_urls = [url for url in urls if validate_url(url)]
            if not valid_urls:
                yield "**Error:** No valid URLs provided.\n"
                return

            invalid_urls = set(urls) - set(valid_urls)
            if invalid_urls:
                yield f"**Warning:** Skipping invalid URLs: {', '.join(invalid_urls)}\n\n"

            # Step 2: Fetch URLs
            yield "## Fetching Content\n\n"
            fetch_results = await self.fetcher.fetch_multiple(valid_urls)

            if not fetch_results:
                yield "**Error:** Failed to fetch any URLs.\n"
                return

            yield f"✓ Fetched {len(fetch_results)} / {len(valid_urls)} URLs\n\n"

            # Step 3: Extract content
            yield "## Extracting Content\n\n"
            extracted_contents = []
            for url, fetch_result in fetch_results.items():
                try:
                    extracted = await self.extractor.extract(fetch_result)
                    extracted_contents.append(extracted)
                    yield f"✓ Extracted: {extracted.title}\n"
                except Exception as e:
                    _get_logger().error("extraction_failed", url=url, error=str(e))
                    yield f"✗ Failed to extract: {url}\n"

            if not extracted_contents:
                yield "\n**Error:** Failed to extract content from any URLs.\n"
                return

            yield "\n"

            # Step 4: Optional link following
            if follow_links and max_depth > 0:
                yield "## Following Links\n\n"
                additional_contents = await self._follow_links(
                    extracted_contents,
                    max_depth=max_depth,
                    query=query,
                )
                extracted_contents.extend(additional_contents)
                yield f"✓ Followed {len(additional_contents)} additional links\n\n"

            # Step 5: Combine and chunk content
            yield "## Processing Content\n\n"
            combined_text = self._combine_contents(extracted_contents)
            chunks = self.chunker.chunk_text(combined_text)
            yield f"✓ Created {len(chunks)} chunks (avg {sum(c.tokens for c in chunks) // len(chunks)} tokens)\n\n"

            # Step 6: Summarize
            yield "## Summary\n\n"
            sources = [ec.url for ec in extracted_contents]

            async for chunk in self.summarizer.summarize_chunks(
                chunks,
                query=query,
                sources=sources,
            ):
                yield chunk

            # Step 7: Add metadata footer
            yield "\n\n---\n\n"
            yield self._format_metadata(extracted_contents)

        except Exception as e:
            _get_logger().error("pipeline_failed", error=str(e))
            self.metrics.record_error("pipeline", e)
            yield f"\n\n**Error:** {str(e)}\n"

    async def _follow_links(
        self,
        contents: list[Any],
        max_depth: int,
        query: str | None = None,
    ) -> list[Any]:
        """Recursively follow relevant links.

        Args:
            contents: Extracted contents with links
            max_depth: Maximum recursion depth
            query: Optional query for link relevance

        Returns:
            List of additional extracted contents
        """
        if max_depth <= 0:
            return []

        # Score and filter links
        relevant_links = self._score_links(contents, query)

        # Limit to top N links
        top_links = relevant_links[:5]  # Max 5 additional links per page

        if not top_links:
            return []

        _get_logger().info("following_links", num_links=len(top_links))

        # Fetch and extract
        additional_contents = []
        fetch_results = await self.fetcher.fetch_multiple(top_links)

        for url, fetch_result in fetch_results.items():
            try:
                extracted = await self.extractor.extract(fetch_result)
                additional_contents.append(extracted)
            except Exception as e:
                _get_logger().warning("link_extraction_failed", url=url, error=str(e))

        return additional_contents

    def _score_links(
        self,
        contents: list[Any],
        query: str | None = None,
    ) -> list[str]:
        """Score and rank links by relevance.

        Args:
            contents: Extracted contents
            query: Optional query

        Returns:
            Sorted list of URLs
        """
        link_scores: dict[str, float] = {}

        for content in contents:
            for link in content.links:
                # Skip already processed URLs
                if link in [c.url for c in contents]:
                    continue

                score = 0.0

                # Prefer documentation domains
                if any(
                    domain in link.lower()
                    for domain in ["docs", "documentation", "guide", "tutorial", "wiki"]
                ):
                    score += 2.0

                # Prefer specific TLDs
                if any(tld in link for tld in [".edu", ".gov", ".org"]):
                    score += 1.0

                # Avoid social media and forums
                if any(
                    domain in link.lower()
                    for domain in ["twitter", "facebook", "reddit", "instagram"]
                ):
                    score -= 2.0

                # Query relevance
                if query:
                    query_lower = query.lower()
                    if query_lower in link.lower():
                        score += 1.5

                link_scores[link] = score

        # Sort by score
        sorted_links = sorted(link_scores.items(), key=lambda x: x[1], reverse=True)
        return [link for link, score in sorted_links if score > 0]

    def _combine_contents(self, contents: list[Any]) -> str:
        """Combine multiple extracted contents.

        Args:
            contents: List of ExtractedContent

        Returns:
            Combined Markdown text
        """
        parts = []

        for content in contents:
            parts.append(f"# {content.title}\n")
            parts.append(f"Source: {content.url}\n\n")
            parts.append(content.content)
            parts.append("\n\n---\n\n")

        return "".join(parts)

    def _format_metadata(self, contents: list[Any]) -> str:
        """Format metadata footer.

        Args:
            contents: Extracted contents

        Returns:
            Formatted metadata string
        """
        parts = ["### Metadata\n\n"]

        # Sources
        parts.append("**Sources:**\n\n")
        for i, content in enumerate(contents, 1):
            parts.append(f"{i}. [{content.title}]({content.url})\n")

        parts.append("\n")

        # Stats
        total_chars = sum(len(c.content) for c in contents)
        parts.append("**Statistics:**\n\n")
        parts.append(f"- Documents processed: {len(contents)}\n")
        parts.append(f"- Total content length: {total_chars:,} characters\n")

        # Cache stats
        if self.cache:
            cache_stats = self.cache.get_stats()
            if cache_stats:
                parts.append(f"- Cache size: {cache_stats.get('size_mb', 0):.2f} MB\n")

        return "".join(parts)

    async def close(self) -> None:
        """Close all resources."""
        await self.fetcher.close()
        await self.summarizer.close()
        _get_logger().info("pipeline_closed")


def create_server(config: Config | None = None) -> FastMCP:
    """Create MCP server with summarize_urls tool.

    Args:
        config: Optional configuration (loads defaults if not provided)

    Returns:
        FastMCP server instance
    """
    config = config or load_config()

    # Configure logging
    configure_logging(
        level=config.metrics.log_level,
        structured=config.metrics.structured_logging,
    )

    # Create MCP server
    mcp = FastMCP(name="mcp-web", instructions="Intelligent web summarization server")

    # Initialize pipeline
    pipeline = WebSummarizationPipeline(config)

    @mcp.tool()
    async def summarize_urls(
        urls: list[str],
        query: str | None = None,
        follow_links: bool = False,
        max_depth: int = 1,
    ) -> str:
        """Summarize content from one or more URLs.

        This tool fetches URLs, extracts main content, and generates an intelligent
        summary focused on your optional query. It can optionally follow relevant
        links for deeper context.

        Args:
            urls: List of URLs to summarize (required)
            query: Optional question or topic to focus the summary on
            follow_links: Whether to follow relevant outbound links (default: False)
            max_depth: Maximum link following depth (default: 1)

        Returns:
            Markdown-formatted summary with sources and metadata

        Examples:
            - summarize_urls(["https://example.com"])
            - summarize_urls(["https://docs.python.org"], query="async programming")
            - summarize_urls(["https://arxiv.org/paper"], follow_links=True)
        """
        # Collect streaming output
        output_parts = []
        async for chunk in pipeline.summarize_urls(
            urls=urls,
            query=query,
            follow_links=follow_links,
            max_depth=max_depth,
        ):
            output_parts.append(chunk)

        return "".join(output_parts)

    @mcp.tool()
    async def get_cache_stats() -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dictionary with cache metrics (size, hit rate, etc.)
        """
        if pipeline.cache:
            stats = pipeline.cache.get_stats()
            metrics = pipeline.metrics.export_metrics()
            return {
                "cache": stats,
                "metrics": metrics.get("summary", {}),
            }
        return {"cache": {"enabled": False}}

    @mcp.tool()
    async def clear_cache() -> str:
        """Clear the entire cache.

        Returns:
            Confirmation message
        """
        if pipeline.cache:
            await pipeline.cache.clear()
            return "✓ Cache cleared successfully"
        return "Cache is not enabled"

    @mcp.tool()
    async def prune_cache() -> str:
        """Remove expired cache entries.

        Returns:
            Number of entries pruned
        """
        if pipeline.cache:
            count = await pipeline.cache.prune()
            return f"✓ Pruned {count} expired entries"
        return "Cache is not enabled"

    _get_logger().info(
        "mcp_server_created",
        tools=["summarize_urls", "get_cache_stats", "clear_cache", "prune_cache"],
    )

    return mcp


# Entry point for running the server
def main() -> None:
    """Run the MCP server."""
    config = load_config()
    mcp = create_server(config)

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
