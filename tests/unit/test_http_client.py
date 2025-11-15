"""Tests for httpx singleton lifecycle and cancellation safeguards."""

import asyncio
from unittest.mock import AsyncMock

import pytest

from mcp_web.config import FetcherSettings
from mcp_web.fetcher import URLFetcher
from mcp_web.http_client import get_http_client, reset_http_client


@pytest.mark.asyncio
async def test_get_http_client_returns_singleton(monkeypatch):
    """get_http_client should reuse the same AsyncClient until reset."""

    await reset_http_client()

    instances: list[object] = []

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            self.closed = False
            instances.append(self)

        async def aclose(self) -> None:
            self.closed = True

    monkeypatch.setattr("mcp_web.http_client.httpx.AsyncClient", DummyAsyncClient)

    config = FetcherSettings(timeout=1)

    client_one = await get_http_client(config)
    client_two = await get_http_client(config)

    assert client_one is client_two
    assert len(instances) == 1

    await reset_http_client()
    client_three = await get_http_client(config)

    assert client_three is not client_one
    assert len(instances) == 2

    await reset_http_client()


@pytest.mark.asyncio
async def test_fetch_httpx_cancellation_closes_singleton(monkeypatch):
    """Cancelled httpx fetches must trigger singleton cleanup to avoid leaks."""

    await reset_http_client()

    config = FetcherSettings(timeout=1, enable_fallback=False)
    fetcher = URLFetcher(config)

    client_mock = AsyncMock()
    client_mock.get.side_effect = asyncio.CancelledError()

    get_client_mock = AsyncMock(return_value=client_mock)
    close_client_mock = AsyncMock()

    monkeypatch.setattr("mcp_web.fetcher.get_http_client", get_client_mock)
    monkeypatch.setattr("mcp_web.fetcher.close_http_client", close_client_mock)

    with pytest.raises(asyncio.CancelledError):
        await fetcher.fetch("https://example.com")

    get_client_mock.assert_awaited_once()
    close_client_mock.assert_awaited_once()

    await fetcher.close()
    await reset_http_client()
