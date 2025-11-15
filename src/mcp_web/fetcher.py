"""URL fetching with httpx and Playwright fallback.

Implements fetch strategy:
1. Primary: httpx async GET (fast)
2. Fallback: Playwright headless browser (JS-heavy sites)
3. File system: Local file:// URLs
4. Caching: ETag/Last-Modified headers

Design Decision DD-001: httpx primary, Playwright fallback.
"""

import asyncio
import mimetypes
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

import structlog

from mcp_web.browser_pool import BrowserPool
from mcp_web.cache import CacheKeyBuilder, CacheManager
from mcp_web.config import FetcherSettings
from mcp_web.exceptions import (
    BrowserError,
    ConfigurationError,
    FetchError,
    HTTPError,
    NetworkError,
    TimeoutError,
    ValidationError,
)
from mcp_web.http_client import close_http_client, get_http_client
from mcp_web.metrics import get_metrics_collector

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


def _parse_file_url(url: str) -> Path:
    """Parse file:// URL or absolute path to Path object.

    Args:
        url: file:// URL or absolute path

    Returns:
        Path object

    Example:
        >>> _parse_file_url("file:///home/user/file.txt")
        Path('/home/user/file.txt')
        >>> _parse_file_url("/home/user/file.txt")
        Path('/home/user/file.txt')
    """
    if url.startswith("file://"):
        parsed = urlparse(url)
        # Unquote to handle URL-encoded characters
        return Path(unquote(parsed.path))
    else:
        return Path(url)


def _validate_file_path(path: Path, allowed_dirs: list[Path]) -> tuple[bool, str]:
    """Validate file path against allowed directories whitelist.

    Args:
        path: File path to validate
        allowed_dirs: List of allowed directory paths (resolved)

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> _validate_file_path(Path("/home/user/doc.txt"), [Path("/home/user")])
        (True, "")
        >>> _validate_file_path(Path("/etc/passwd"), [Path("/home/user")])
        (False, "Path outside allowed directories")
    """
    try:
        # Resolve to absolute path (follows symlinks, resolves ..)
        resolved = path.resolve()
    except (OSError, RuntimeError) as e:
        return False, f"Cannot resolve path: {e}"

    # Check if path is within any allowed directory
    for allowed_dir in allowed_dirs:
        try:
            resolved.relative_to(allowed_dir)
            return True, ""  # Path is within allowed directory
        except ValueError:
            continue  # Not in this directory

    return False, f"Path outside allowed directories: {resolved}"


@dataclass
class FetchResult:
    """Result of URL fetch operation."""

    url: str
    content: bytes
    content_type: str
    headers: dict[str, str]
    status_code: int
    fetch_method: str  # 'httpx', 'playwright', 'filesystem', or 'cache'
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
        browser_pool: BrowserPool | None = None,
    ):
        """Initialize URL fetcher.

        Args:
            config: Fetcher configuration
            cache: Optional cache manager
            browser_pool: Optional browser pool for Playwright fetching
        """
        self.config = config
        self.cache = cache
        self.browser_pool = browser_pool
        self.metrics = get_metrics_collector()

        # Resolve allowed directories for file system access
        self.allowed_dirs: list[Path] = []
        if config.enable_file_system:
            for dir_str in config.allowed_directories:
                dir_path = Path(dir_str).expanduser()
                if not dir_path.is_absolute():
                    dir_path = Path.cwd() / dir_path
                self.allowed_dirs.append(dir_path.resolve())

    async def fetch(
        self,
        url: str,
        force_playwright: bool = False,
        use_cache: bool = True,
    ) -> FetchResult:
        """Fetch URL with automatic fallback.

        Args:
            url: URL to fetch (http://, https://, file://, or absolute path)
            force_playwright: Skip httpx, use Playwright directly
            use_cache: Use cached result if available

        Returns:
            FetchResult with content and metadata

        Raises:
            Exception: If all fetch methods fail
        """
        _get_logger().info("fetch_start", url=url, force_playwright=force_playwright)

        # Detect file:// URLs or absolute paths
        is_file_url = url.startswith("file://") or (
            Path(url).is_absolute() if not url.startswith(("http://", "https://")) else False
        )

        if is_file_url:
            if not self.config.enable_file_system:
                raise ConfigurationError(
                    "File system access is disabled. Set FETCHER_ENABLE_FILE_SYSTEM=true",
                    config_key="FETCHER_ENABLE_FILE_SYSTEM",
                )

            # File system fetch (no cache for local files)
            return await self._fetch_file(url)

        # Check cache first (for HTTP/HTTPS URLs)
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
            except asyncio.CancelledError:
                raise
            except Exception as e:
                _get_logger().warning(
                    "httpx_failed",
                    url=url,
                    error=str(e),
                    fallback="playwright",
                )

                # Only fallback if enabled
                if not self.config.enable_fallback:
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
            raise FetchError(f"Failed to fetch: {str(e)}", url=url) from e

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
            # Use singleton HTTP client
            client = await get_http_client(self.config)
            response = await client.get(url)
            duration_ms = (time.perf_counter() - start_time) * 1000

            # Check for problematic responses that might need Playwright
            if response.status_code in [403, 429] or len(response.content) < 100:
                raise HTTPError(
                    f"Suspicious response (size={len(response.content)})",
                    url=url,
                    status_code=response.status_code,
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

        except asyncio.CancelledError as cancel_error:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.record_fetch(
                url=url,
                method="httpx",
                duration_ms=duration_ms,
                status_code=0,
                content_size=0,
                success=False,
                error="cancelled",
            )

            try:
                await close_http_client()
                _get_logger().warning(
                    "httpx_request_cancelled",
                    url=url,
                    duration_ms=round(duration_ms, 2),
                )
            except Exception as cleanup_error:  # pragma: no cover - defensive logging
                _get_logger().warning(
                    "httpx_cancel_cleanup_failed",
                    url=url,
                    error=str(cleanup_error),
                )
            finally:
                raise

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
            # Use browser pool if available, fallback to manual browser
            if self.browser_pool:
                async with self.browser_pool.acquire() as browser_instance:
                    page = await browser_instance.new_page()
                    try:
                        # Navigate with timeout
                        response = await page.goto(
                            url,
                            wait_until="networkidle",
                            timeout=self.config.timeout * 1000,
                        )

                        if response is None:
                            raise BrowserError(f"Browser navigation failed for {url}: No response from page")

                        # Get page content
                        content = await page.content()
                        headers = response.headers
                        status = response.status
                    finally:
                        await page.close()
            else:
                # Fallback: manual browser (legacy mode, not recommended)
                from playwright.async_api import async_playwright

                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    context = await browser.new_context(
                        user_agent=self.config.user_agent,
                        viewport={"width": 1920, "height": 1080},
                    )
                    page = await context.new_page()

                    try:
                        # Navigate with timeout
                        response = await page.goto(
                            url,
                            wait_until="networkidle",
                            timeout=self.config.timeout * 1000,
                        )

                        if response is None:
                            raise BrowserError(f"Browser navigation failed for {url}: No response from page")

                        # Get page content
                        content = await page.content()
                        headers = response.headers
                        status = response.status
                    finally:
                        await page.close()
                        await context.close()
                        await browser.close()

            duration_ms = (time.perf_counter() - start_time) * 1000

            result = FetchResult(
                url=url,
                content=content.encode("utf-8"),
                content_type=headers.get("content-type", "text/html"),
                headers=headers,
                status_code=status,
                fetch_method="playwright",
            )

            self.metrics.record_fetch(
                url=url,
                method="playwright",
                duration_ms=duration_ms,
                status_code=status,
                content_size=len(content),
                success=True,
            )

            _get_logger().info(
                "playwright_success",
                url=url,
                status=status,
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

    async def _fetch_file(self, url: str) -> FetchResult:
        """Fetch from local file system.

        Args:
            url: file:// URL or absolute path

        Returns:
            FetchResult

        Raises:
            Exception: On fetch failure or security violation
        """
        import time

        start_time = time.perf_counter()

        try:
            # Parse URL to path
            file_path = _parse_file_url(url)

            # Validate path
            is_valid, error_msg = _validate_file_path(file_path, self.allowed_dirs)
            if not is_valid:
                duration_ms = (time.perf_counter() - start_time) * 1000
                self.metrics.record_fetch(
                    url=url,
                    method="filesystem",
                    duration_ms=duration_ms,
                    status_code=403,
                    content_size=0,
                    success=False,
                    error=error_msg,
                )
                raise ValidationError(error_msg, field="file_path", value_preview=str(file_path))

            # Check file exists
            if not file_path.exists():
                duration_ms = (time.perf_counter() - start_time) * 1000
                self.metrics.record_fetch(
                    url=url,
                    method="filesystem",
                    duration_ms=duration_ms,
                    status_code=404,
                    content_size=0,
                    success=False,
                    error="File not found",
                )
                # Keep FileNotFoundError for backward compatibility but wrap in FetchError
                raise FetchError(
                    f"File not found: {file_path}",
                    url=url,
                    status_code=404,
                ) from FileNotFoundError(str(file_path))

            # Check is file (not directory)
            if not file_path.is_file():
                duration_ms = (time.perf_counter() - start_time) * 1000
                self.metrics.record_fetch(
                    url=url,
                    method="filesystem",
                    duration_ms=duration_ms,
                    status_code=400,
                    content_size=0,
                    success=False,
                    error="Not a file",
                )
                raise ValidationError(
                    f"Not a file: {file_path}",
                    field="file_path",
                    value_preview=str(file_path),
                )

            # Check file size
            file_size = file_path.stat().st_size
            if file_size > self.config.max_file_size:
                duration_ms = (time.perf_counter() - start_time) * 1000
                self.metrics.record_fetch(
                    url=url,
                    method="filesystem",
                    duration_ms=duration_ms,
                    status_code=413,
                    content_size=file_size,
                    success=False,
                    error=f"File too large: {file_size} > {self.config.max_file_size}",
                )
                raise ValidationError(
                    f"File too large: {file_size} bytes > {self.config.max_file_size} bytes",
                    field="file_size",
                )

            # Read file
            content = file_path.read_bytes()

            # Guess content type
            content_type, _ = mimetypes.guess_type(str(file_path))
            if not content_type:
                # Default based on content
                try:
                    content.decode("utf-8")
                    content_type = "text/plain"
                except UnicodeDecodeError:
                    content_type = "application/octet-stream"

            duration_ms = (time.perf_counter() - start_time) * 1000

            result = FetchResult(
                url=url,
                content=content,
                content_type=content_type,
                headers={"content-length": str(len(content))},
                status_code=200,
                fetch_method="filesystem",
            )

            self.metrics.record_fetch(
                url=url,
                method="filesystem",
                duration_ms=duration_ms,
                status_code=200,
                content_size=len(content),
                success=True,
            )

            _get_logger().info(
                "filesystem_success",
                url=url,
                path=str(file_path),
                size=len(content),
                content_type=content_type,
                duration_ms=round(duration_ms, 2),
            )

            return result

        except Exception as e:
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.record_fetch(
                url=url,
                method="filesystem",
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
        """Close HTTP client and cleanup resources.

        Note: This now closes the singleton HTTP client and browser pool.
        Should only be called on application shutdown.
        """
        await close_http_client()
        if self.browser_pool:
            await self.browser_pool.shutdown()
        _get_logger().info("fetcher_closed")
