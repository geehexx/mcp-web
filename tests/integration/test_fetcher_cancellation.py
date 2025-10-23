import asyncio
import time

import pytest
import httpx
from pytest_httpx import HTTPXMock

from mcp_web.config import FetcherSettings
from mcp_web.fetcher import URLFetcher
from mcp_web.http_client import get_http_client, get_pool_stats, reset_http_client


async def wait_for_condition(condition_func, timeout=0.5, poll_interval=0.005):
    """Wait for a condition to become true."""
    start_time = time.monotonic()
    while time.monotonic() - start_time < timeout:
        if condition_func():
            return True
        await asyncio.sleep(poll_interval)
    return False


@pytest.fixture(autouse=True)
async def reset_client_for_test():
    """Reset the singleton client before each test."""
    await reset_http_client()
    yield
    await reset_http_client()


@pytest.mark.asyncio
async def test_fetch_cancellation_releases_connection(httpx_mock: HTTPXMock):
    """Verify that cancelling a fetch task releases the connection."""
    # Mock a slow response
    async def slow_response(*args, **kwargs):
        await asyncio.sleep(0.05)  # Shorter sleep
        return httpx.Response(200)

    httpx_mock.add_callback(slow_response, url="https://example.com")

    config = FetcherSettings()
    fetcher = URLFetcher(config)

    # Ensure client is initialized
    await get_http_client(config)

    initial_stats = get_pool_stats()
    assert initial_stats["active"] == 0

    # Start the fetch in a separate task
    fetch_task = asyncio.create_task(fetcher.fetch("https://example.com"))

    # Wait for the connection to be acquired
    assert await wait_for_condition(
        lambda: get_pool_stats()["active"] == 1
    ), "Connection was not acquired"

    # Cancel the task
    fetch_task.cancel()

    with pytest.raises(asyncio.CancelledError):
        await fetch_task

    # After cancellation, the connection should be released
    assert await wait_for_condition(
        lambda: get_pool_stats()["active"] == 0
    ), "Connection was not released"

    stats_after_cancellation = get_pool_stats()
    assert stats_after_cancellation["idle"] >= initial_stats["idle"]


@pytest.mark.asyncio
async def test_fetch_cancellation_stress_test(httpx_mock: HTTPXMock):
    """Run cancellation tests in a loop to check for resource leaks."""
    # Mock a slow response
    async def slow_response(*args, **kwargs):
        await asyncio.sleep(0.01)  # Even shorter sleep for stress test
        return httpx.Response(200)

    httpx_mock.add_callback(slow_response, url="https://example.com")

    config = FetcherSettings()
    fetcher = URLFetcher(config)

    # Ensure client is initialized
    await get_http_client(config)

    initial_stats = get_pool_stats()

    for i in range(5):  # Reduced iterations
        fetch_task = asyncio.create_task(fetcher.fetch("https://example.com"))

        # Wait for an active connection
        assert await wait_for_condition(
            lambda: get_pool_stats()["active"] >= 1
        ), f"No active connection on iteration {i}"

        fetch_task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await fetch_task

    # After all cancellations, the pool should be stable
    assert await wait_for_condition(
        lambda: get_pool_stats()["active"] == 0
    ), "Not all connections were released"

    final_stats = get_pool_stats()
    assert final_stats["idle"] >= initial_stats["idle"]
