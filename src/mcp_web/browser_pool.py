"""Browser pool for managing reusable Playwright browser instances.

Implements P0-STABILITY-001 fix: Browser pool with async context manager pattern
to prevent resource leaks from unclosed browsers and contexts.

Design principles:
- Async context manager guarantees cleanup
- Lazy initialization (create on demand)
- Health checking before use
- Automatic replacement of aged/failed browsers
- Graceful shutdown with timeout

References:
    - Initiative: Phase 1 - Resource Stability & Leak Prevention
    - Issue: P0-STABILITY-001 (Playwright context leak)
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field

import structlog
from playwright.async_api import Browser, BrowserContext, Page, Playwright, async_playwright

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


@dataclass
class BrowserPoolSettings:
    """Browser pool configuration.

    Attributes:
        pool_size: Number of browsers in pool (default: 3)
        max_age: Maximum browser age in seconds before replacement (default: 300s = 5min)
        idle_timeout: Maximum idle time before replacement (default: 60s)
        max_requests: Maximum requests per browser before replacement (default: 1000)
        health_check_timeout: Health check timeout in seconds (default: 5.0)
        startup_timeout: Browser launch timeout in seconds (default: 30.0)
        user_agent: User agent string for browsers
    """

    pool_size: int = 3
    max_age: float = 300.0
    idle_timeout: float = 60.0
    max_requests: int = 1000
    health_check_timeout: float = 5.0
    startup_timeout: float = 30.0
    user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"


@dataclass
class BrowserInstance:
    """Wrapper for Playwright browser with metadata.

    Attributes:
        browser: Playwright browser instance
        context: Browser context with settings
        created_at: Creation timestamp
        last_used: Last usage timestamp
        request_count: Number of requests served
        is_healthy: Health status flag
    """

    browser: Browser
    context: BrowserContext
    created_at: float = field(default_factory=time.time)
    last_used: float = field(default_factory=time.time)
    request_count: int = 0
    is_healthy: bool = True
    in_use: bool = False

    async def new_page(self) -> Page:
        """Create new page in context.

        Returns:
            New page instance

        Raises:
            Exception: If page creation fails
        """
        page = await self.context.new_page()
        self.request_count += 1
        self.last_used = time.time()
        return page

    async def close(self) -> None:
        """Close browser and context.

        Closes context first, then browser. Logs errors but doesn't raise.
        """
        try:
            await self.context.close()
        except Exception as e:
            _get_logger().warning("browser_context_close_error", error=str(e))

        try:
            await self.browser.close()
        except Exception as e:
            _get_logger().warning("browser_close_error", error=str(e))

    async def health_check(self, timeout: float = 5.0) -> bool:
        """Check if browser is responsive.

        Args:
            timeout: Health check timeout in seconds

        Returns:
            True if healthy, False otherwise
        """
        try:
            page = await self.context.new_page()
            try:
                await page.goto("about:blank", timeout=int(timeout * 1000))
                self.is_healthy = True
                return True
            finally:
                await page.close()
        except Exception as e:
            _get_logger().warning("health_check_failed", error=str(e))
            self.is_healthy = False
            return False


@dataclass
class BrowserPoolMetrics:
    """Browser pool metrics for monitoring.

    Attributes:
        active_browsers: Currently in use
        idle_browsers: Available in pool
        total_browsers: Total instances
        total_requests: Lifetime request count
        replacement_count: Browsers replaced
        health_check_failures: Failed health checks
        pool_exhaustion_count: Times pool was fully utilized
    """

    active_browsers: int = 0
    idle_browsers: int = 0
    total_browsers: int = 0
    total_requests: int = 0
    replacement_count: int = 0
    health_check_failures: int = 0
    pool_exhaustion_count: int = 0


class BrowserPool:
    """Pool of reusable Playwright browser instances.

    Manages a pool of browsers to prevent resource leaks and improve performance
    by reusing browser instances instead of creating new ones for each request.

    Example:
        >>> settings = BrowserPoolSettings(pool_size=3)
        >>> pool = BrowserPool(settings)
        >>> await pool.initialize()
        >>>
        >>> # Use with async context manager (guarantees cleanup)
        >>> async with pool.acquire() as browser:
        ...     page = await browser.new_page()
        ...     await page.goto("https://example.com")
        ...     content = await page.content()
        ...     await page.close()
        >>>
        >>> await pool.shutdown()
    """

    def __init__(self, settings: BrowserPoolSettings | None = None):
        """Initialize browser pool.

        Args:
            settings: Pool configuration (uses defaults if None)
        """
        self.settings = settings or BrowserPoolSettings()
        self._browsers: list[BrowserInstance] = []
        self._semaphore = asyncio.Semaphore(self.settings.pool_size)
        self._playwright: Playwright | None = None
        self._shutdown = False
        self._metrics = BrowserPoolMetrics()
        self._lock = asyncio.Lock()  # Protect browser list modifications

    def _needs_replacement(self, browser: BrowserInstance) -> bool:
        """Determine if browser should be replaced before reuse."""

        now = time.time()
        age = now - browser.created_at
        idle_time = now - browser.last_used

        return (
            not browser.is_healthy
            or age > self.settings.max_age
            or idle_time > self.settings.idle_timeout
            or browser.request_count >= self.settings.max_requests
        )

    async def initialize(self) -> None:
        """Initialize Playwright and pool.

        Must be called before using the pool.
        """
        self._playwright = await async_playwright().start()
        _get_logger().info(
            "browser_pool_initialized",
            pool_size=self.settings.pool_size,
            max_age=self.settings.max_age,
        )

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[BrowserInstance]:
        """Acquire browser from pool with guaranteed cleanup.

        Acquires a browser instance from the pool. If pool is exhausted,
        waits until a browser becomes available. Automatically releases
        browser back to pool even if exception occurs.

        Yields:
            BrowserInstance ready for use

        Raises:
            RuntimeError: If pool not initialized or shutdown
            Exception: If browser acquisition/health check fails

        Example:
            >>> async with pool.acquire() as browser:
            ...     page = await browser.new_page()
            ...     # ... use page ...
            ...     await page.close()
        """
        if self._shutdown:
            raise RuntimeError("Browser pool is shutdown")

        if self._playwright is None:
            raise RuntimeError("Browser pool not initialized. Call initialize() first.")

        # Track pool exhaustion
        if self._semaphore.locked():
            self._metrics.pool_exhaustion_count += 1
            _get_logger().warning("browser_pool_exhausted")

        # Acquire semaphore (wait if pool full)
        await self._semaphore.acquire()

        browser = None
        try:
            # Get or create browser
            browser = await self._get_or_create_browser()

            # Health check before use
            is_healthy = await browser.health_check(self.settings.health_check_timeout)
            if not is_healthy:
                self._metrics.health_check_failures += 1
                # Replace unhealthy browser
                await self._replace_browser(browser)
                browser = await self._get_or_create_browser()

            self._metrics.active_browsers += 1
            self._metrics.total_requests += 1

            yield browser

        finally:
            if browser:
                await self._release_browser(browser)
                self._metrics.active_browsers -= 1

            self._semaphore.release()

    async def _get_or_create_browser(self) -> BrowserInstance:
        """Get existing browser or create new one.

        Returns:
            Browser instance

        Raises:
            Exception: If browser creation fails
        """
        replacement_candidate: BrowserInstance | None = None
        create_new = False

        async with self._lock:
            # Try to reuse existing idle browser
            for browser in self._browsers:
                if browser.in_use:
                    continue

                if self._needs_replacement(browser):
                    replacement_candidate = browser
                    self._browsers.remove(browser)
                    break

                browser.in_use = True
                browser.last_used = time.time()
                return browser

            if replacement_candidate is None:
                if len(self._browsers) < self.settings.pool_size:
                    create_new = True
                else:
                    available = [b for b in self._browsers if not b.in_use]
                    if available:
                        candidate = min(available, key=lambda b: b.last_used)
                        candidate.in_use = True
                        candidate.last_used = time.time()
                        return candidate

        if replacement_candidate is not None:
            await replacement_candidate.close()
            new_browser = await self._create_browser()
            new_browser.in_use = True
            new_browser.last_used = time.time()

            async with self._lock:
                self._browsers.append(new_browser)
                self._metrics.replacement_count += 1
                self._metrics.total_browsers = len(self._browsers)

            return new_browser

        if create_new:
            new_browser = await self._create_browser()
            new_browser.in_use = True
            new_browser.last_used = time.time()

            async with self._lock:
                self._browsers.append(new_browser)
                self._metrics.total_browsers = len(self._browsers)

            return new_browser

        # If we reach here, all browsers are currently in use (should not happen due to semaphore)
        raise RuntimeError("No available browser instances")

    async def _create_browser(self) -> BrowserInstance:
        """Create new browser instance.

        Returns:
            New browser instance

        Raises:
            Exception: If browser creation fails
        """
        if self._playwright is None:
            raise RuntimeError("Playwright not initialized")

        start_time = time.time()

        try:
            browser = await asyncio.wait_for(
                self._playwright.chromium.launch(headless=True),
                timeout=self.settings.startup_timeout,
            )

            context = await browser.new_context(
                user_agent=self.settings.user_agent,
                viewport={"width": 1920, "height": 1080},
            )

            duration_ms = (time.time() - start_time) * 1000

            instance = BrowserInstance(browser=browser, context=context)

            _get_logger().info(
                "browser_created",
                duration_ms=round(duration_ms, 2),
                pool_size=len(self._browsers) + 1,
            )

            return instance

        except asyncio.TimeoutError as e:
            _get_logger().error(
                "browser_creation_timeout",
                timeout=self.settings.startup_timeout,
            )
            raise RuntimeError("Browser creation timed out") from e

    async def _release_browser(self, browser: BrowserInstance) -> None:
        """Release browser back to pool.

        Checks if browser should be replaced based on age, health, and request count.

        Args:
            browser: Browser to release
        """
        browser.last_used = time.time()
        browser.in_use = False

        if self._needs_replacement(browser):
            _get_logger().info(
                "browser_replacement",
                age=round(time.time() - browser.created_at, 2),
                requests=browser.request_count,
                healthy=browser.is_healthy,
            )
            await self._replace_browser(browser)

    async def _replace_browser(self, old_browser: BrowserInstance) -> None:
        """Replace browser with new instance.

        Args:
            old_browser: Browser to replace
        """
        async with self._lock:
            try:
                # Remove from pool
                if old_browser in self._browsers:
                    self._browsers.remove(old_browser)

                # Close old browser
                await old_browser.close()

                # Create new browser
                new_browser = await self._create_browser()
                new_browser.in_use = False
                self._browsers.append(new_browser)

                self._metrics.replacement_count += 1
                self._metrics.total_browsers = len(self._browsers)

            except Exception as e:
                _get_logger().error("browser_replacement_error", error=str(e))
                # Don't re-raise, pool can continue with remaining browsers

    async def shutdown(self, timeout: float = 10.0) -> None:
        """Shutdown pool and close all browsers.

        Args:
            timeout: Shutdown timeout in seconds
        """
        self._shutdown = True

        _get_logger().info("browser_pool_shutdown_start", timeout=timeout)

        # Close all browsers with timeout
        close_tasks = [browser.close() for browser in self._browsers]

        try:
            await asyncio.wait_for(
                asyncio.gather(*close_tasks, return_exceptions=True),
                timeout=timeout,
            )
        except asyncio.TimeoutError:
            _get_logger().warning("browser_pool_shutdown_timeout", timeout=timeout)

        # Stop Playwright
        if self._playwright:
            try:
                await self._playwright.stop()
            except Exception as e:
                _get_logger().warning("playwright_stop_error", error=str(e))

        self._browsers.clear()
        self._metrics.total_browsers = 0

        _get_logger().info("browser_pool_shutdown_complete")

    def get_metrics(self) -> BrowserPoolMetrics:
        """Get pool metrics.

        Returns:
            Current pool metrics
        """
        self._metrics.idle_browsers = len(
            [browser for browser in self._browsers if not browser.in_use]
        )
        return self._metrics
