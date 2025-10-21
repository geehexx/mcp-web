"""Singleton HTTP client for shared connection pooling.

Implements P1-STABILITY-002 fix: Shared httpx AsyncClient to prevent
connection pool accumulation from multiple URLFetcher instances.

Design:
- Module-level singleton AsyncClient
- Lazy initialization with async lock
- Shared connection pool across all fetchers
- Proper lifecycle management (cleanup on shutdown)

References:
    - Initiative: Phase 1 - Resource Stability & Leak Prevention
    - Issue: P1-STABILITY-002 (httpx connection pool accumulation)
    - httpx docs: https://www.python-httpx.org/advanced/#connection-pooling
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import httpx
import structlog

if TYPE_CHECKING:
    from mcp_web.config import FetcherSettings

logger: structlog.stdlib.BoundLogger | None = None

# Module-level singleton state
_client: httpx.AsyncClient | None = None
_lock: asyncio.Lock = asyncio.Lock()
_initialized: bool = False


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


async def get_http_client(config: FetcherSettings) -> httpx.AsyncClient:
    """Get or create singleton HTTP client.

    Returns shared AsyncClient instance with connection pooling.
    Thread-safe lazy initialization with async lock.

    Args:
        config: Fetcher settings for client configuration

    Returns:
        Shared httpx.AsyncClient instance

    Example:
        >>> from mcp_web.config import FetcherSettings
        >>> config = FetcherSettings()
        >>> client = await get_http_client(config)
        >>> response = await client.get("https://example.com")
    """
    global _client, _initialized

    # Fast path: client already initialized
    if _client is not None and _initialized:
        return _client

    # Slow path: initialize with lock
    async with _lock:
        # Double-check after acquiring lock
        if _client is not None and _initialized:
            return _client

        # Create new client with optimized connection pool settings
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                timeout=config.timeout,
                connect=10.0,  # Connection timeout
                read=config.timeout,  # Read timeout
                write=10.0,  # Write timeout
                pool=5.0,  # Pool acquisition timeout
            ),
            limits=httpx.Limits(
                max_keepalive_connections=20,  # Keep 20 connections alive
                max_connections=100,  # Max 100 total connections
                keepalive_expiry=30.0,  # Keep connections alive for 30s
            ),
            follow_redirects=True,
            headers={"User-Agent": config.user_agent},
            # Enable HTTP/2 for better performance
            http2=True,
        )

        _initialized = True

        _get_logger().info(
            "http_client_initialized",
            max_connections=100,
            max_keepalive=20,
            keepalive_expiry=30.0,
        )

        return _client


async def close_http_client() -> None:
    """Close singleton HTTP client and cleanup resources.

    Should be called on application shutdown to properly close
    all connections and release resources.

    Example:
        >>> await close_http_client()
    """
    global _client, _initialized

    async with _lock:
        if _client is not None:
            try:
                await _client.aclose()
                _get_logger().info("http_client_closed")
            except Exception as e:
                _get_logger().warning("http_client_close_error", error=str(e))
            finally:
                _client = None
                _initialized = False


def get_client_stats() -> dict[str, int | bool]:
    """Get HTTP client statistics.

    Returns:
        Dict with client stats (initialized, connection info)

    Example:
        >>> stats = get_client_stats()
        >>> print(stats["initialized"])
        True
    """
    return {
        "initialized": _initialized,
        "client_exists": _client is not None,
    }


async def reset_http_client() -> None:
    """Reset HTTP client (for testing purposes).

    Closes existing client and resets state.
    Should only be used in tests.
    """
    await close_http_client()
