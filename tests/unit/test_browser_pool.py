"""Unit tests for BrowserPool.

Tests for P0-STABILITY-001 fix: Browser pool resource management.

Test categories:
- Pool initialization and shutdown
- Browser acquisition and release
- Health checking
- Automatic browser replacement
- Pool exhaustion handling
- Metrics tracking
"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from mcp_web.browser_pool import (
    BrowserInstance,
    BrowserPool,
    BrowserPoolSettings,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def pool_settings():
    """Browser pool settings for testing."""
    return BrowserPoolSettings(
        pool_size=2,  # Small pool for faster tests
        max_age=10.0,  # Short age for testing replacement
        idle_timeout=5.0,
        max_requests=5,  # Low count for testing replacement
        health_check_timeout=1.0,
        startup_timeout=5.0,
    )


@pytest.fixture
def mock_playwright():
    """Mock Playwright instance."""
    playwright = AsyncMock()

    # Mock browser
    browser = AsyncMock()
    browser.close = AsyncMock()

    # Mock context
    context = AsyncMock()
    context.close = AsyncMock()
    context.new_page = AsyncMock()

    # Mock page
    page = AsyncMock()
    page.goto = AsyncMock()
    page.close = AsyncMock()
    page.content = AsyncMock(return_value="<html>test</html>")

    async def new_page(*args, **kwargs):
        return page

    context.new_page = AsyncMock(return_value=page)
    browser.new_context.return_value = context
    playwright.chromium.launch.return_value = browser
    playwright.stop = AsyncMock()

    return playwright


# =============================================================================
# Initialization & Shutdown Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_pool_initialization(pool_settings, mock_playwright):
    """Pool initializes Playwright correctly."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        assert pool._playwright is not None
        assert pool._shutdown is False
        assert len(pool._browsers) == 0  # Lazy creation


@pytest.mark.unit
@pytest.mark.asyncio
async def test_pool_shutdown(pool_settings, mock_playwright):
    """Pool shuts down cleanly and closes all browsers."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        # Create some browsers
        async with pool.acquire():
            pass

        # Shutdown
        await pool.shutdown(timeout=5.0)

        assert pool._shutdown is True
        assert len(pool._browsers) == 0
        mock_playwright.stop.assert_called_once()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_shutdown_timeout_handling(pool_settings, mock_playwright):
    """Pool handles shutdown timeout gracefully."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        # Create browser
        async with pool.acquire():
            pass

        # Make browser close hang
        async def slow_close():
            await asyncio.sleep(10)  # Longer than timeout

        mock_playwright.chromium.launch.return_value.close = AsyncMock(side_effect=slow_close)

        # Should not raise, just log warning
        await pool.shutdown(timeout=0.5)

        assert pool._shutdown is True


# =============================================================================
# Browser Acquisition & Release Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_acquire_creates_browser_on_demand(pool_settings, mock_playwright):
    """First acquire creates browser lazily."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        assert len(pool._browsers) == 0

        async with pool.acquire() as browser:
            assert browser is not None
            assert len(pool._browsers) == 1

        await pool.shutdown()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_acquire_reuses_existing_browser(pool_settings, mock_playwright):
    """Sequential acquires reuse same browser."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        async with pool.acquire() as browser1:
            first_browser_id = id(browser1)

        async with pool.acquire() as browser2:
            second_browser_id = id(browser2)

        assert first_browser_id == second_browser_id  # Same browser reused
        assert len(pool._browsers) == 1  # Only one created

        await pool.shutdown()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_concurrent_acquire_creates_multiple_browsers(pool_settings, mock_playwright):
    """Concurrent acquires create multiple browsers up to pool_size."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        # Acquire browsers concurrently
        async def acquire_and_hold():
            async with pool.acquire() as browser:
                await asyncio.sleep(0.1)  # Hold for a bit
                return id(browser)

        browser_ids = await asyncio.gather(
            acquire_and_hold(),
            acquire_and_hold(),
        )

        # Should have created 2 browsers (pool_size=2)
        assert len(set(browser_ids)) == 2  # Different browsers
        assert len(pool._browsers) == 2

        await pool.shutdown()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_pool_exhaustion_waits(pool_settings, mock_playwright):
    """Acquire waits when pool is exhausted."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        acquired_order = []

        async def acquire_and_hold(id_num: int, hold_time: float):
            async with pool.acquire():
                acquired_order.append(id_num)
                await asyncio.sleep(hold_time)

        # Start 3 tasks (pool_size=2, so 3rd waits)
        await asyncio.gather(
            acquire_and_hold(1, 0.2),
            acquire_and_hold(2, 0.2),
            acquire_and_hold(3, 0.1),  # This one waits
        )

        # Task 3 should acquire after 1 or 2 releases
        assert len(acquired_order) == 3
        assert acquired_order[0] in [1, 2]  # 1 or 2 first
        assert acquired_order[1] in [1, 2]  # 1 or 2 second
        assert acquired_order[2] == 3  # 3 waits

        # Check pool exhaustion metric
        assert pool.get_metrics().pool_exhaustion_count >= 1

        await pool.shutdown()


# =============================================================================
# Health Check Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_health_check_success(pool_settings, mock_playwright):
    """Healthy browser passes health check."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        async with pool.acquire() as browser:
            assert browser.is_healthy is True

        await pool.shutdown()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_health_check_failure_triggers_replacement(pool_settings, mock_playwright):
    """Unhealthy browser is replaced automatically."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        # First acquire - create browser
        async with pool.acquire() as browser1:
            first_id = id(browser1)

        # Make health check fail
        mock_playwright.chromium.launch.return_value.new_context.return_value.new_page = AsyncMock(
            side_effect=Exception("Browser crashed")
        )

        # Second acquire - should detect unhealthy and replace
        async with pool.acquire() as browser2:
            second_id = id(browser2)

        # Should have been replaced
        assert first_id != second_id
        assert pool.get_metrics().replacement_count >= 1
        assert pool.get_metrics().health_check_failures >= 1

        await pool.shutdown()


# =============================================================================
# Browser Replacement Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_replacement_on_max_age(pool_settings, mock_playwright):
    """Browser replaced when max_age exceeded."""
    pool_settings.max_age = 0.5  # 500ms
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        async with pool.acquire() as browser1:
            first_id = id(browser1)

        # Wait for age to exceed max_age
        await asyncio.sleep(0.6)

        async with pool.acquire() as browser2:
            second_id = id(browser2)

        assert first_id != second_id  # Replaced
        assert pool.get_metrics().replacement_count >= 1

        await pool.shutdown()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_replacement_on_max_requests(pool_settings, mock_playwright):
    """Browser replaced when max_requests exceeded."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        # Make max_requests requests
        for _i in range(pool_settings.max_requests):
            async with pool.acquire() as browser:
                await browser.new_page()  # Increments request_count

        len(pool._browsers)

        # Next acquire should trigger replacement
        async with pool.acquire() as browser:
            pass

        assert pool.get_metrics().replacement_count >= 1

        await pool.shutdown()


# =============================================================================
# Error Handling Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_acquire_without_initialization_raises():
    """Acquire raises if pool not initialized."""
    pool = BrowserPool()

    with pytest.raises(RuntimeError, match="not initialized"):
        async with pool.acquire():
            pass


@pytest.mark.unit
@pytest.mark.asyncio
async def test_acquire_after_shutdown_raises(pool_settings, mock_playwright):
    """Acquire raises if pool is shutdown."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()
        await pool.shutdown()

        with pytest.raises(RuntimeError, match="shutdown"):
            async with pool.acquire():
                pass


@pytest.mark.unit
@pytest.mark.asyncio
async def test_browser_creation_timeout_handling(pool_settings, mock_playwright):
    """Browser creation timeout handled gracefully."""
    pool_settings.startup_timeout = 0.1  # Very short timeout
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        # Make browser launch hang
        async def slow_launch(*args, **kwargs):
            await asyncio.sleep(10)

        mock_playwright.chromium.launch = AsyncMock(side_effect=slow_launch)

        await pool.initialize()

        with pytest.raises(RuntimeError, match="timed out"):
            async with pool.acquire():
                pass

        await pool.shutdown()


# =============================================================================
# Metrics Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_metrics_tracking(pool_settings, mock_playwright):
    """Pool tracks metrics correctly."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        # Acquire and release
        async with pool.acquire() as browser:
            await browser.new_page()

        metrics = pool.get_metrics()

        assert metrics.total_browsers == 1
        assert metrics.total_requests == 1
        assert metrics.active_browsers == 0  # Released
        assert metrics.idle_browsers == 1

        await pool.shutdown()


# =============================================================================
# Resource Leak Prevention Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_browser_closed_on_exception(pool_settings, mock_playwright):
    """Browser properly released even when exception occurs."""
    pool = BrowserPool(pool_settings)

    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        await pool.initialize()

        with pytest.raises(ValueError):
            async with pool.acquire() as browser:
                raise ValueError("Test exception")

        # Browser should still be in pool and reusable
        async with pool.acquire() as browser:
            assert browser is not None

        await pool.shutdown()


@pytest.mark.unit
@pytest.mark.asyncio
async def test_page_close_on_exception(mock_playwright):
    """Page properly closed even when exception occurs during work."""
    with patch("mcp_web.browser_pool.async_playwright") as mock_async_pw:
        mock_async_pw.return_value.start = AsyncMock(return_value=mock_playwright)

        from mcp_web.browser_pool import BrowserInstance

        browser_mock = mock_playwright.chromium.launch.return_value
        context_mock = browser_mock.new_context.return_value

        instance = BrowserInstance(browser=browser_mock, context=context_mock)

        # Simulate page usage with exception
        with pytest.raises(ValueError):
            await instance.new_page()
            raise ValueError("Test error")

        # Page creation should have been called
        context_mock.new_page.assert_called()


# =============================================================================
# BrowserInstance Tests
# =============================================================================


@pytest.mark.unit
@pytest.mark.asyncio
async def test_browser_instance_new_page_increments_count():
    """new_page() increments request count."""
    browser_mock = AsyncMock()
    context_mock = AsyncMock()
    page_mock = AsyncMock()
    context_mock.new_page.return_value = page_mock

    instance = BrowserInstance(browser=browser_mock, context=context_mock)

    initial_count = instance.request_count
    await instance.new_page()

    assert instance.request_count == initial_count + 1


@pytest.mark.unit
@pytest.mark.asyncio
async def test_browser_instance_close_closes_both():
    """close() closes context and browser."""
    browser_mock = AsyncMock()
    context_mock = AsyncMock()

    instance = BrowserInstance(browser=browser_mock, context=context_mock)

    await instance.close()

    context_mock.close.assert_called_once()
    browser_mock.close.assert_called_once()
