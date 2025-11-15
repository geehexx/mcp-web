"""Comprehensive tests for HTTP fetching functionality.

Tests URL fetching with httpx and Playwright fallback:
- HTTP/HTTPS fetching with httpx
- Playwright fallback for JS-heavy sites
- Caching integration
- Error handling and retries
- Metrics recording

Target: Boost fetcher.py coverage from 52% to 80%+
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import httpx
import pytest

from mcp_web.cache import CacheManager
from mcp_web.config import FetcherSettings
from mcp_web.exceptions import ConfigurationError
from mcp_web.fetcher import FetchResult, URLFetcher


@pytest.fixture
def fetcher_config():
    """Create basic fetcher configuration."""
    return FetcherSettings(
        timeout=30,
        user_agent="test-agent",
        enable_file_system=False,
        enable_fallback=True,
    )


@pytest.fixture
def mock_cache():
    """Create mock cache manager."""
    cache = AsyncMock(spec=CacheManager)
    cache.get = AsyncMock(return_value=None)  # Cache miss by default
    cache.set = AsyncMock()
    return cache


class TestHTTPXFetching:
    """Test HTTP fetching with httpx."""

    @pytest.mark.asyncio
    async def test_fetch_success_with_httpx(self, fetcher_config, mock_cache):
        """Test successful fetch using httpx."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        # Make content > 100 bytes to avoid triggering fallback
        large_content = b"<html><body>Test content " + b"x" * 100 + b"</body></html>"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = large_content
        mock_response.headers = {"content-type": "text/html"}
        mock_response.url = "https://example.com"

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            result = await fetcher.fetch("https://example.com")

            assert result.url == "https://example.com"
            assert result.content == large_content
            assert result.content_type == "text/html"
            assert result.status_code == 200
            assert result.fetch_method == "httpx"
            assert result.from_cache is False

    @pytest.mark.asyncio
    async def test_fetch_httpx_403_triggers_fallback(self, fetcher_config, mock_cache):
        """Test that 403 response triggers Playwright fallback."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        # Mock httpx to return 403
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.content = b"Forbidden"
        mock_response.headers = {"content-type": "text/html"}

        # Mock successful Playwright fallback
        mock_playwright_result = FetchResult(
            url="https://example.com",
            content=b"<html><body>Playwright content</body></html>",
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="playwright",
        )

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with patch.object(fetcher, "_fetch_playwright", return_value=mock_playwright_result):
                result = await fetcher.fetch("https://example.com")

                # Should use Playwright result
                assert result.fetch_method == "playwright"
                assert b"Playwright content" in result.content

    @pytest.mark.asyncio
    async def test_fetch_httpx_429_triggers_fallback(self, fetcher_config, mock_cache):
        """Test that 429 (rate limit) response triggers Playwright fallback."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.content = b"Rate limited"
        mock_response.headers = {"content-type": "text/html"}

        mock_playwright_result = FetchResult(
            url="https://example.com",
            content=b"<html><body>Playwright content</body></html>",
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="playwright",
        )

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with patch.object(fetcher, "_fetch_playwright", return_value=mock_playwright_result):
                result = await fetcher.fetch("https://example.com")

                assert result.fetch_method == "playwright"

    @pytest.mark.asyncio
    async def test_fetch_small_content_triggers_fallback(self, fetcher_config, mock_cache):
        """Test that suspiciously small content triggers Playwright fallback."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        # Mock httpx to return very small content (< 100 bytes)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html>x</html>"  # Only 14 bytes
        mock_response.headers = {"content-type": "text/html"}

        # Playwright returns full content (> 100 bytes)
        playwright_content = b"<html><body>Full content from Playwright" + b"x" * 100 + b"</body></html>"
        mock_playwright_result = FetchResult(
            url="https://example.com",
            content=playwright_content,
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="playwright",
        )

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with patch.object(fetcher, "_fetch_playwright", return_value=mock_playwright_result):
                result = await fetcher.fetch("https://example.com")

                assert result.fetch_method == "playwright"
                assert len(result.content) > 100

    @pytest.mark.asyncio
    async def test_fetch_httpx_network_error(self, fetcher_config, mock_cache):
        """Test httpx network error triggers Playwright fallback."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        mock_playwright_result = FetchResult(
            url="https://example.com",
            content=b"<html><body>Playwright content</body></html>",
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="playwright",
        )

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=httpx.ConnectError("Connection failed"))
            mock_get_client.return_value = mock_client

            with patch.object(fetcher, "_fetch_playwright", return_value=mock_playwright_result):
                result = await fetcher.fetch("https://example.com")

                assert result.fetch_method == "playwright"

    @pytest.mark.asyncio
    async def test_fetch_httpx_timeout_error(self, fetcher_config, mock_cache):
        """Test httpx timeout triggers Playwright fallback."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        mock_playwright_result = FetchResult(
            url="https://example.com",
            content=b"<html><body>Content</body></html>",
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="playwright",
        )

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))
            mock_get_client.return_value = mock_client

            with patch.object(fetcher, "_fetch_playwright", return_value=mock_playwright_result):
                result = await fetcher.fetch("https://example.com")

                assert result.fetch_method == "playwright"

    @pytest.mark.asyncio
    async def test_fetch_httpx_cancelled(self, fetcher_config, mock_cache):
        """Test httpx request cancellation is propagated."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=asyncio.CancelledError())
            mock_get_client.return_value = mock_client

            with patch("mcp_web.fetcher.close_http_client") as mock_close:
                with pytest.raises(asyncio.CancelledError):
                    await fetcher.fetch("https://example.com")

                # Should attempt cleanup
                mock_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_fallback_disabled_raises_error(self, mock_cache):
        """Test that with fallback disabled, httpx errors are raised."""
        config = FetcherSettings(
            timeout=30,
            user_agent="test-agent",
            enable_file_system=False,
            enable_fallback=False,  # Fallback disabled
        )
        fetcher = URLFetcher(config, cache=mock_cache)

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=httpx.ConnectError("Connection failed"))
            mock_get_client.return_value = mock_client

            with pytest.raises(httpx.ConnectError):
                await fetcher.fetch("https://example.com")


class TestPlaywrightFetching:
    """Test Playwright browser fetching."""

    @pytest.mark.asyncio
    async def test_fetch_with_playwright_browser_pool(self, fetcher_config, mock_cache):
        """Test Playwright fetch with browser pool."""
        from mcp_web.browser_pool import BrowserPool

        # Mock browser pool
        mock_pool = AsyncMock(spec=BrowserPool)
        mock_browser = MagicMock()
        mock_page = AsyncMock()
        mock_response = AsyncMock()

        mock_response.status = 200
        mock_response.headers = {"content-type": "text/html"}
        mock_page.goto = AsyncMock(return_value=mock_response)
        mock_page.content = AsyncMock(return_value="<html><body>Playwright content</body></html>")
        mock_page.close = AsyncMock()

        mock_browser.new_page = AsyncMock(return_value=mock_page)

        # Mock the context manager
        mock_pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_browser)
        mock_pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        fetcher = URLFetcher(fetcher_config, cache=mock_cache, browser_pool=mock_pool)

        result = await fetcher._fetch_playwright("https://example.com")

        assert result.status_code == 200
        assert b"Playwright content" in result.content
        assert result.fetch_method == "playwright"
        mock_page.goto.assert_called_once()
        mock_page.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_playwright_no_browser_pool(self, fetcher_config, mock_cache):
        """Test Playwright fetch without browser pool (manual mode)."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache, browser_pool=None)

        # Mock the entire playwright async context
        mock_page = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.headers = {"content-type": "text/html"}
        mock_page.goto = AsyncMock(return_value=mock_response)
        mock_page.content = AsyncMock(return_value="<html><body>Manual browser content</body></html>")
        mock_page.close = AsyncMock()

        mock_context = AsyncMock()
        mock_context.new_page = AsyncMock(return_value=mock_page)
        mock_context.close = AsyncMock()

        mock_browser = AsyncMock()
        mock_browser.new_context = AsyncMock(return_value=mock_context)
        mock_browser.close = AsyncMock()

        mock_chromium = AsyncMock()
        mock_chromium.launch = AsyncMock(return_value=mock_browser)

        mock_playwright = AsyncMock()
        mock_playwright.chromium = mock_chromium
        mock_playwright.__aenter__ = AsyncMock(return_value=mock_playwright)
        mock_playwright.__aexit__ = AsyncMock(return_value=None)

        # Import is: from playwright.async_api import async_playwright
        with patch("playwright.async_api.async_playwright", return_value=mock_playwright):
            result = await fetcher._fetch_playwright("https://example.com")

            assert result.status_code == 200
            assert b"Manual browser content" in result.content
            assert result.fetch_method == "playwright"

    @pytest.mark.asyncio
    async def test_fetch_playwright_no_response(self, fetcher_config, mock_cache):
        """Test Playwright handling when no response is returned."""
        from mcp_web.browser_pool import BrowserPool

        mock_pool = AsyncMock(spec=BrowserPool)
        mock_browser = MagicMock()
        mock_page = AsyncMock()

        # goto returns None (page didn't load)
        mock_page.goto = AsyncMock(return_value=None)
        mock_page.close = AsyncMock()

        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_browser)
        mock_pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        fetcher = URLFetcher(fetcher_config, cache=mock_cache, browser_pool=mock_pool)

        with pytest.raises(Exception, match="No response from page"):
            await fetcher._fetch_playwright("https://example.com")

        mock_page.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_playwright_timeout(self, fetcher_config, mock_cache):
        """Test Playwright timeout handling."""
        from mcp_web.browser_pool import BrowserPool

        mock_pool = AsyncMock(spec=BrowserPool)
        mock_browser = MagicMock()
        mock_page = AsyncMock()

        # Simulate timeout
        from playwright.async_api import TimeoutError as PlaywrightTimeout

        mock_page.goto = AsyncMock(side_effect=PlaywrightTimeout("Navigation timeout"))
        mock_page.close = AsyncMock()

        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_browser)
        mock_pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        fetcher = URLFetcher(fetcher_config, cache=mock_cache, browser_pool=mock_pool)

        with pytest.raises(PlaywrightTimeout):
            await fetcher._fetch_playwright("https://example.com")

        mock_page.close.assert_called_once()


class TestCacheIntegration:
    """Test caching integration."""

    @pytest.mark.asyncio
    async def test_fetch_cache_hit(self, fetcher_config):
        """Test successful cache hit returns cached content."""
        mock_cache = AsyncMock(spec=CacheManager)
        cached_data = {
            "content": b"<html><body>Cached content</body></html>",
            "content_type": "text/html",
            "headers": {"cache-control": "max-age=3600"},
            "status_code": 200,
        }
        mock_cache.get = AsyncMock(return_value=cached_data)

        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        result = await fetcher.fetch("https://example.com")

        assert result.from_cache is True
        assert result.fetch_method == "cache"
        assert result.content == b"<html><body>Cached content</body></html>"
        assert result.status_code == 200

        # Should not fetch from network
        mock_cache.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_cache_miss_stores_result(self, fetcher_config):
        """Test cache miss fetches and stores result."""
        mock_cache = AsyncMock(spec=CacheManager)
        mock_cache.get = AsyncMock(return_value=None)  # Cache miss
        mock_cache.set = AsyncMock()

        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        # Make content > 100 bytes to avoid Playwright fallback
        large_content = b"<html><body>Fresh content " + b"x" * 100 + b"</body></html>"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = large_content
        mock_response.headers = {"content-type": "text/html"}
        mock_response.url = "https://example.com"

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            result = await fetcher.fetch("https://example.com")

            # Should fetch from network
            assert result.from_cache is False
            assert result.fetch_method == "httpx"

            # Should store in cache
            mock_cache.set.assert_called_once()

    @pytest.mark.asyncio
    async def test_fetch_with_cache_disabled(self, fetcher_config):
        """Test fetch with use_cache=False bypasses cache."""
        mock_cache = AsyncMock(spec=CacheManager)
        mock_cache.get = AsyncMock(return_value={
            "content": b"Cached",
            "content_type": "text/html",
            "headers": {},
            "status_code": 200,
        })

        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        # Make content > 100 bytes to avoid Playwright fallback
        large_content = b"<html><body>Fresh " + b"x" * 100 + b"</body></html>"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = large_content
        mock_response.headers = {"content-type": "text/html"}
        mock_response.url = "https://example.com"

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            result = await fetcher.fetch("https://example.com", use_cache=False)

            # Should fetch from network, not cache
            assert b"Fresh" in result.content
            mock_cache.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_fetch_non_200_not_cached(self, fetcher_config):
        """Test that non-200 responses trigger fallback to Playwright and 200 result is cached."""
        mock_cache = AsyncMock(spec=CacheManager)
        mock_cache.get = AsyncMock(return_value=None)
        mock_cache.set = AsyncMock()

        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        # httpx returns 403 (triggers fallback)
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.content = b"Forbidden"
        mock_response.headers = {"content-type": "text/html"}
        mock_response.url = "https://example.com"

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_get_client.return_value = mock_client

            with patch.object(fetcher, "_fetch_playwright") as mock_playwright:
                # Playwright succeeds with 200
                playwright_content = b"<html><body>OK " + b"x" * 100 + b"</body></html>"
                mock_playwright.return_value = FetchResult(
                    url="https://example.com",
                    content=playwright_content,
                    content_type="text/html",
                    headers={},
                    status_code=200,
                    fetch_method="playwright",
                )

                result = await fetcher.fetch("https://example.com")

                # Playwright succeeded with 200, should be cached
                assert result.status_code == 200
                assert mock_cache.set.called


class TestForcePlaywright:
    """Test force_playwright parameter."""

    @pytest.mark.asyncio
    async def test_force_playwright_skips_httpx(self, fetcher_config, mock_cache):
        """Test force_playwright=True skips httpx."""
        from mcp_web.browser_pool import BrowserPool

        mock_pool = AsyncMock(spec=BrowserPool)
        mock_browser = MagicMock()
        mock_page = AsyncMock()
        mock_response = AsyncMock()

        mock_response.status = 200
        mock_response.headers = {"content-type": "text/html"}
        mock_page.goto = AsyncMock(return_value=mock_response)
        mock_page.content = AsyncMock(return_value="<html><body>Playwright</body></html>")
        mock_page.close = AsyncMock()

        mock_browser.new_page = AsyncMock(return_value=mock_page)
        mock_pool.acquire.return_value.__aenter__ = AsyncMock(return_value=mock_browser)
        mock_pool.acquire.return_value.__aexit__ = AsyncMock(return_value=None)

        fetcher = URLFetcher(fetcher_config, cache=mock_cache, browser_pool=mock_pool)

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            result = await fetcher.fetch("https://example.com", force_playwright=True)

            # Should not call httpx
            mock_get_client.assert_not_called()

            # Should use Playwright
            assert result.fetch_method == "playwright"


class TestErrorHandling:
    """Test error handling and propagation."""

    @pytest.mark.asyncio
    async def test_all_methods_fail_raises_exception(self, fetcher_config, mock_cache):
        """Test that if both httpx and Playwright fail, exception is raised."""
        fetcher = URLFetcher(fetcher_config, cache=mock_cache)

        with patch("mcp_web.fetcher.get_http_client") as mock_get_client:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=httpx.ConnectError("httpx failed"))
            mock_get_client.return_value = mock_client

            with patch.object(fetcher, "_fetch_playwright", side_effect=Exception("Playwright failed")):
                with pytest.raises(Exception, match="Failed to fetch"):
                    await fetcher.fetch("https://example.com")

    @pytest.mark.asyncio
    async def test_file_url_disabled_raises_error(self, mock_cache):
        """Test that file URLs raise error when file system is disabled."""
        config = FetcherSettings(
            timeout=30,
            user_agent="test-agent",
            enable_file_system=False,  # Disabled
        )
        fetcher = URLFetcher(config, cache=mock_cache)

        with pytest.raises(ConfigurationError, match="File system access is disabled"):
            await fetcher.fetch("file:///tmp/test.txt")
