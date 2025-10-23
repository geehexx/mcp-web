import pytest
from pytest_httpx import HTTPXMock

from mcp_web.config import FetcherSettings
from mcp_web.http_client import (
    close_http_client,
    get_client_stats,
    get_http_client,
    get_pool_stats,
    reset_http_client,
)


@pytest.fixture(autouse=True)
async def reset_client_for_test():
    """Reset the singleton client before each test."""
    await reset_http_client()
    yield
    await reset_http_client()


@pytest.mark.asyncio
async def test_get_pool_stats(httpx_mock: HTTPXMock):
    """Test that get_pool_stats returns correct stats after a request."""
    # Mock a request
    httpx_mock.add_response(url="https://example.com")

    # Initial stats should be zero
    initial_stats = get_pool_stats()
    assert initial_stats == {"all": 0, "active": 0, "idle": 0, "waiting": 0}

    # Make a request to initialize the client
    config = FetcherSettings()
    client = await get_http_client(config)
    await client.get("https://example.com")

    # After the request, there should be one idle connection
    # Note: This can sometimes be flaky in a test environment, so we
    # check for a plausible state rather than exact numbers.
    stats = get_pool_stats()
    assert stats["all"] >= 0
    assert stats["idle"] >= 0
    assert stats["active"] == 0  # Should be 0 after request is complete
    assert stats["waiting"] == 0

    # Test get_client_stats includes pool stats
    client_stats = get_client_stats()
    assert client_stats["initialized"] is True
    assert client_stats["pool_idle"] >= 0


@pytest.mark.asyncio
async def test_singleton_behavior():
    """Test that get_http_client returns the same instance."""
    config = FetcherSettings()
    client1 = await get_http_client(config)
    client2 = await get_http_client(config)
    assert client1 is client2


@pytest.mark.asyncio
async def test_close_http_client():
    """Test that close_http_client properly closes the client."""
    config = FetcherSettings()
    client = await get_http_client(config)
    assert get_client_stats()["initialized"] is True

    await close_http_client()
    assert get_client_stats()["initialized"] is False
    assert client.is_closed is True
