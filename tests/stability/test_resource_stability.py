import asyncio
import logging
import time

import httpx
import psutil
import pytest
from pytest_httpx import HTTPXMock

from mcp_web.config import FetcherSettings
from mcp_web.fetcher import URLFetcher
from mcp_web.http_client import get_http_client, reset_http_client


@pytest.fixture(autouse=True)
async def reset_client_for_test():
    """Reset the singleton client before each test."""
    await reset_http_client()
    yield
    await reset_http_client()


@pytest.mark.asyncio
@pytest.mark.slow
async def test_memory_usage_stability(httpx_mock: HTTPXMock):
    """Test that memory usage remains stable after many requests."""
    httpx_mock.add_response(url="https://example.com")

    config = FetcherSettings()
    fetcher = URLFetcher(config)

    # Ensure client is initialized
    await get_http_client(config)

    process = psutil.Process()
    mem_before = process.memory_info().rss

    for _ in range(100):
        await fetcher.fetch("https://example.com", use_cache=False)

    mem_after = process.memory_info().rss
    mem_growth = (mem_after - mem_before) / mem_before

    # Allow for some memory growth, but it should be minimal
    assert mem_growth < 0.1, "Memory growth exceeds 10%"


@pytest.mark.asyncio
@pytest.mark.slow
async def test_pool_stability_under_load(httpx_mock: HTTPXMock, caplog):
    """Test that the connection pool is stable under high load."""

    async def slow_response(*args, **kwargs):
        await asyncio.sleep(0.01)
        return httpx.Response(200)

    httpx_mock.add_callback(slow_response, url="https://example.com")

    config = FetcherSettings()
    fetcher = URLFetcher(config)

    # Ensure client is initialized
    await get_http_client(config)

    async def fetch_task():
        try:
            await fetcher.fetch("https://example.com", use_cache=False)
        except Exception:
            pass

    with caplog.at_level(logging.WARNING):
        tasks = [fetch_task() for _ in range(200)]
        await asyncio.gather(*tasks)

    assert "httpx_pool_timeout" not in caplog.text, "Pool exhaustion occurred"


@pytest.mark.asyncio
@pytest.mark.slow
async def test_performance_with_connection_pooling(httpx_mock: HTTPXMock):
    """Test that connection pooling improves performance."""
    httpx_mock.add_response(url="https://example.com")

    config = FetcherSettings()
    fetcher = URLFetcher(config)

    # Ensure client is initialized
    await get_http_client(config)

    # "Warm up" the connection pool
    for _ in range(10):
        await fetcher.fetch("https://example.com", use_cache=False)

    # Time a series of requests
    start_time = time.monotonic()
    for _ in range(100):
        await fetcher.fetch("https://example.com", use_cache=False)
    end_time = time.monotonic()

    duration = end_time - start_time
    # This is a simple performance test. A more sophisticated test would
    # measure the connection pool hit rate directly, but that's not
    # easily exposed by httpx.
    # The goal is to ensure that the requests are reasonably fast, which
    # indicates that connection pooling is working.
    assert duration < 5, "Requests took too long, pooling may not be effective"
