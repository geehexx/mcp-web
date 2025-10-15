"""URL fetching with httpx and Playwright fallback.

Implements fetch strategy:
1. Primary: httpx async GET (fast)
2. Fallback: Playwright headless browser (JS-heavy sites)
3. Caching: ETag/Last-Modified headers

Design Decision DD-001: httpx primary, Playwright fallback.
"""

import asyncio
from dataclasses import dataclass

import httpx
import structlog
from playwright.async_api import async_playwright

from mcp_web.cache import CacheKeyBuilder, CacheManager
from mcp_web.config import FetcherSettings
from mcp_web.metrics import get_metrics_collector

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


@dataclass
class FetchResult:
    """Result of URL fetch operation."""

    url: str
    content: bytes
    content_type: str
    headers: dict[str, str]
    status_code: int
    fetch_method: str  # 'httpx', 'playwright', or 'cache'
    from_cache: bool = False


class URLFetcher:
    """URL fetcher with automatic fallback strategy.

    Example:
        >>> fetcher = URLFetcher(config)
        >>> result = await fetcher.fetch("https://example.com")
        >>> print(result.content_type)
        'text/html'
    """

    def __init__(
        self,
        config: FetcherSettings,
        cache: CacheManager | None = None,
    ):
        """Initialize URL fetcher.

        Args:
            config: Fetcher configuration
            cache: Optional cache manager
        """
        self.config = config
        self.cache = cache
        self.metrics = get_metrics_collector()

        # HTTP client
        self.http_client = httpx.AsyncClient(
            timeout=config.timeout,
            follow_redirects=True,
            headers={"User-Agent": config.user_agent},
        )

    async def fetch(
        self,
        url: str,
        force_playwright: bool = False,
        use_cache: bool = True,
    ) -> FetchResult:
        """Fetch URL with automatic fallback.

        Args:
            url: URL to fetch
            force_playwright: Skip httpx, use Playwright directly
            use_cache: Use cached result if available

        Returns:
            FetchResult with content and metadata

        Raises:
            Exception: If all fetch methods fail
        """
        _get_logger().info("fetch_start", url=url, force_playwright=force_playwright)

        # Check cache first
        if use_cache and self.cache:
            cache_key = CacheKeyBuilder.fetch_key(url)
            cached = await self.cache.get(cache_key)
            if cached:
                _get_logger().info("fetch_cache_hit", url=url)
                return FetchResult(
                    url=url,
                    content=cached["content"],
                    content_type=cached["content_type"],
                    headers=cached["headers"],
                    status_code=cached["status_code"],
                    fetch_method="cache",
                    from_cache=True,
                )

        # Try httpx first (unless forced to use Playwright)
        if not force_playwright:
            try:
                result = await self._fetch_httpx(url)

                # Cache successful fetch
                if use_cache and self.cache and result.status_code == 200:
                    await self._cache_result(url, result)

                return result

            except Exception as e:
                _get_logger().warning(
                    "httpx_failed",
                    url=url,
                    error=str(e),
                    fallback="playwright",
                )

                # Only fallback if enabled
                if not self.config.use_playwright_fallback:
                    raise

        # Fallback to Playwright
        try:
            result = await self._fetch_playwright(url)

            # Cache successful fetch
            if use_cache and self.cache and result.status_code == 200:
                await self._cache_result(url, result)

            return result

        except Exception as e:
            _get_logger().error("fetch_failed", url=url, error=str(e))
            self.metrics.record_error("fetcher", e, {"url": url})
            raise Exception(f"Failed to fetch {url}: {str(e)}") from e

    async def _fetch_httpx(self, url: str) -> FetchResult:
        """Fetch using httpx.

        Args:
            url: URL to fetch

        Returns:
            FetchResult

        Raises:
            Exception: On fetch failure
        """
        import time

        start_time = time.perf_counter()

        try:
            response = await self.http_client.get(url)
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Check for problematic responses that might need Playwright
            if response.status_code in [403, 429] or len(response.content) < 100:
                raise Exception(
                    f"Suspicious response: status={response.status_code}, "
                    f"size={len(response.content)}"
                )

            result = FetchResult(
                url=str(response.url),
                content=response.content,
                content_type=response.headers.get("content-type", "text/html"),
                headers=dict(response.headers),
                status_code=response.status_code,
                fetch_method="httpx",
            )

            self.metrics.record_fetch(
                url=url,
                method="httpx",
                duration_ms=duration_ms,
                status_code=response.status_code,
                content_size=len(response.content),
                success=True,
            )

            _get_logger().info(
                "httpx_success",
                url=url,
                status=response.status_code,
                size=len(response.content),
                duration_ms=round(duration_ms, 2),
            )

            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.record_fetch(
                url=url,
                method="httpx",
                duration_ms=duration_ms,
                status_code=0,
                content_size=0,
                success=False,
                error=str(e),
            )
            raise

    async def _fetch_playwright(self, url: str) -> FetchResult:
        """Fetch using Playwright headless browser.

        Args:
            url: URL to fetch

        Returns:
            FetchResult

        Raises:
            Exception: On fetch failure
        """
        import time

        start_time = time.perf_counter()

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=self.config.user_agent,
                    viewport={"width": 1920, "height": 1080},
                )
                page = await context.new_page()

                # Navigate with timeout
                response = await page.goto(
                    url,
                    wait_until="networkidle",
                    timeout=self.config.timeout * 1000,
                )

                if response is None:
                    raise Exception("No response from page")

                # Get page content
                content = await page.content()
                headers = response.headers

                await browser.close()

                duration_ms = (time.perf_counter() - start_time) * 1000

                result = FetchResult(
                    url=page.url,
                    content=content.encode("utf-8"),
                    content_type=headers.get("content-type", "text/html"),
                    headers=headers,
                    status_code=response.status,
                    fetch_method="playwright",
                )

                self.metrics.record_fetch(
                    url=url,
                    method="playwright",
                    duration_ms=duration_ms,
                    status_code=response.status,
                    content_size=len(content),
                    success=True,
                )

                _get_logger().info(
                    "playwright_success",
                    url=url,
                    status=response.status,
                    size=len(content),
                    duration_ms=round(duration_ms, 2),
                )

                return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.record_fetch(
                url=url,
                method="playwright",
                duration_ms=duration_ms,
                status_code=0,
                content_size=0,
                success=False,
                error=str(e),
            )
            raise

    async def _cache_result(self, url: str, result: FetchResult) -> None:
        """Cache fetch result.

        Args:
            url: Original URL
            result: FetchResult to cache
        """
        if not self.cache:
            return

        cache_key = CacheKeyBuilder.fetch_key(url)
        cache_value = {
            "content": result.content,
            "content_type": result.content_type,
            "headers": result.headers,
            "status_code": result.status_code,
        }

        await self.cache.set(
            cache_key,
            cache_value,
            etag=result.headers.get("etag"),
            last_modified=result.headers.get("last-modified"),
        )

    async def fetch_multiple(
        self,
        urls: list[str],
        max_concurrent: int | None = None,
    ) -> dict[str, FetchResult]:
        """Fetch multiple URLs concurrently.

        Args:
            urls: List of URLs to fetch
            max_concurrent: Max concurrent requests (defaults to config)

        Returns:
            Dict mapping URL to FetchResult
        """
        max_concurrent = max_concurrent or self.config.max_concurrent
        semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch_with_semaphore(url: str) -> tuple[str, FetchResult | None]:
            async with semaphore:
                try:
                    result = await self.fetch(url)
                    return url, result
                except Exception as e:
                    _get_logger().error("fetch_multiple_error", url=url, error=str(e))
                    return url, None

        tasks = [fetch_with_semaphore(url) for url in urls]
        results = await asyncio.gather(*tasks)

        return {url: result for url, result in results if result is not None}

    async def close(self) -> None:
        """Close HTTP client and cleanup resources."""
        await self.http_client.aclose()
        _get_logger().info("fetcher_closed")
