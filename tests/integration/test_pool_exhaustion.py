import asyncio
import logging

import pytest
import httpx
from pytest_httpx import HTTPXMock

from mcp_web.config import FetcherSettings
from mcp_web.fetcher import URLFetcher
from mcp_web.http_client import get_http_client, reset_http_client
from mcp_web.metrics import configure_logging


@pytest.fixture(autouse=True)
async def reset_client_for_test():
    """Reset the singleton client before each test."""
    await reset_http_client()
    yield
    await reset_http_client()


@pytest.mark.asyncio
async def test_pool_exhaustion_logs_warning(httpx_mock: HTTPXMock, caplog):
    """Verify that a PoolTimeout logs a warning."""
    # Mock a response that will cause a PoolTimeout
    httpx_mock.add_exception(httpx.PoolTimeout("Pool timeout"), url="https://example.com")

    config = FetcherSettings()
    fetcher = URLFetcher(config)

    # Ensure client is initialized
    await get_http_client(config)

    with caplog.at_level(logging.WARNING):
        try:
            await fetcher.fetch("https://example.com")
        except Exception:
            pass  # We expect an exception, but we're interested in the log

    assert "httpx_pool_timeout" in caplog.text
    assert "HTTPX connection pool exhausted" in caplog.text
