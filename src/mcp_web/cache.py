"""Disk-based caching for mcp-web.

Provides persistent caching with:
- TTL expiration
- LRU eviction
- Size limits
- ETag/Last-Modified support

Design Decision DD-007: Disk cache with 7-day TTL.
Design Decision DD-015: Cache layers for fetch, extract, summarize.
"""

import base64
import hashlib
import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import diskcache
import structlog

from mcp_web.metrics import get_metrics_collector

logger: structlog.stdlib.BoundLogger | None = None  # Will be initialized on first use


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization to avoid circular imports."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


@dataclass
class CacheEntry:
    """Cache entry with metadata."""

    value: Any
    created_at: float
    ttl: int
    etag: str | None = None
    last_modified: str | None = None


class CacheManager:
    """Disk-based cache manager with TTL and size limits.

    Example:
        >>> cache = CacheManager("/tmp/cache")
        >>> await cache.set("key", "value", ttl=3600)
        >>> result = await cache.get("key")
        'value'
    """

    def __init__(
        self,
        cache_dir: str,
        ttl: int = 7 * 24 * 3600,
        max_size: int = 1024 * 1024 * 1024,
        eviction_policy: str = "lru",
    ):
        """Initialize cache manager.

        Args:
            cache_dir: Directory for cache storage
            ttl: Default time-to-live in seconds (default: 7 days)
            max_size: Maximum cache size in bytes (default: 1GB)
            eviction_policy: Eviction policy ('lru' or 'lfu')
        """
        self.cache_dir = Path(cache_dir).expanduser().resolve()
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.default_ttl = ttl
        self.max_size = max_size

        # Map short policy names to diskcache full names
        policy_map = {
            "lru": "least-recently-used",
            "lfu": "least-frequently-used",
        }
        full_policy = policy_map.get(eviction_policy, eviction_policy)

        # Initialize diskcache
        self.cache = diskcache.Cache(
            str(self.cache_dir),
            size_limit=max_size,
            eviction_policy=full_policy,
        )

        self.metrics = get_metrics_collector()

        _get_logger().info(
            "cache_initialized",
            cache_dir=str(self.cache_dir),
            max_size_mb=max_size / (1024 * 1024),
        )

    async def get(self, key: str) -> Any | None:
        """Retrieve cached value if valid.

        Args:
            key: Cache key

        Returns:
            Cached value or None if expired/missing
        """
        cache_key = self._hash_key(key)

        try:
            entry_data = self.cache.get(cache_key)
            if entry_data is None:
                self.metrics.record_cache_operation("miss", key)
                return None

            entry = self._deserialize_entry(entry_data)

            # Check TTL expiration
            if self._is_expired(entry):
                await self.delete(key)
                self.metrics.record_cache_operation("miss", key)
                return None

            self.metrics.record_cache_operation("hit", key)
            _get_logger().debug("cache_hit", key=key[:50])
            return entry.value

        except Exception as e:
            _get_logger().warning("cache_get_error", key=key[:50], error=str(e))
            return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
        etag: str | None = None,
        last_modified: str | None = None,
    ) -> bool:
        """Store value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds (defaults to self.default_ttl)
            etag: Optional ETag for HTTP cache validation
            last_modified: Optional Last-Modified header

        Returns:
            True if stored successfully
        """
        cache_key = self._hash_key(key)
        ttl = ttl or self.default_ttl

        try:
            entry = CacheEntry(
                value=value,
                created_at=time.time(),
                ttl=ttl,
                etag=etag,
                last_modified=last_modified,
            )

            serialized = self._serialize_entry(entry)
            size_bytes = len(serialized) if isinstance(serialized, bytes) else 0

            self.cache.set(cache_key, serialized, expire=ttl)
            self.metrics.record_cache_operation("set", key, size_bytes=size_bytes)

            _get_logger().debug("cache_set", key=key[:50], ttl=ttl, size_bytes=size_bytes)
            return True

        except Exception as e:
            _get_logger().error("cache_set_error", key=key[:50], error=str(e))
            return False

    async def delete(self, key: str) -> bool:
        """Delete cached value.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        cache_key = self._hash_key(key)

        try:
            deleted = self.cache.delete(cache_key)
            if deleted:
                self.metrics.record_cache_operation("delete", key)
            return deleted
        except Exception as e:
            _get_logger().error("cache_delete_error", key=key[:50], error=str(e))
            return False

    async def prune(self) -> int:
        """Remove expired entries.

        Returns:
            Number of entries pruned
        """
        pruned_count = 0

        try:
            # Iterate through all keys and check expiration
            for cache_key in list(self.cache.iterkeys()):
                entry_data = self.cache.get(cache_key)
                if entry_data:
                    entry = self._deserialize_entry(entry_data)
                    if self._is_expired(entry):
                        self.cache.delete(cache_key)
                        pruned_count += 1
                        self.metrics.record_cache_operation("evict", str(cache_key))

            _get_logger().info("cache_pruned", pruned_count=pruned_count)
            return pruned_count

        except Exception as e:
            _get_logger().error("cache_prune_error", error=str(e))
            return pruned_count

    async def clear(self) -> None:
        """Clear entire cache."""
        try:
            self.cache.clear()
            _get_logger().info("cache_cleared")
        except Exception as e:
            _get_logger().error("cache_clear_error", error=str(e))

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics.

        Returns:
            Dict with cache stats
        """
        try:
            volume = self.cache.volume()
            return {
                "size_bytes": volume,
                "size_mb": round(volume / (1024 * 1024), 2),
                "max_size_mb": round(self.max_size / (1024 * 1024), 2),
                "usage_percent": round((volume / self.max_size) * 100, 2),
                "entry_count": len(self.cache),
            }
        except Exception:
            return {}

    def _hash_key(self, key: str) -> str:
        """Generate cache key hash.

        Args:
            key: Original key

        Returns:
            SHA256 hash
        """
        return hashlib.sha256(key.encode()).hexdigest()

    def _serialize_entry(self, entry: CacheEntry) -> str:
        """Serialize cache entry to JSON with bytes support.

        Handles bytes by base64 encoding (for FetchResult.content).

        Args:
            entry: CacheEntry to serialize

        Returns:
            JSON string
        """
        data = asdict(entry)
        # Recursively encode bytes to base64
        data = self._encode_bytes(data)
        return json.dumps(data)

    def _deserialize_entry(self, data: str) -> CacheEntry:
        """Deserialize cache entry from JSON with bytes support.

        Handles base64-encoded bytes (for FetchResult.content).

        Args:
            data: JSON string

        Returns:
            CacheEntry instance
        """
        entry_dict = json.loads(data)
        # Recursively decode base64 to bytes
        entry_dict = self._decode_bytes(entry_dict)
        return CacheEntry(**entry_dict)

    def _encode_bytes(self, obj: Any) -> Any:
        """Recursively encode bytes to base64 strings for JSON serialization.

        Args:
            obj: Object to encode (dict, list, bytes, or primitive)

        Returns:
            Object with bytes converted to base64 strings
        """
        if isinstance(obj, bytes):
            return {"__bytes__": base64.b64encode(obj).decode("ascii")}
        elif isinstance(obj, dict):
            return {k: self._encode_bytes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._encode_bytes(item) for item in obj]
        else:
            return obj

    def _decode_bytes(self, obj: Any) -> Any:
        """Recursively decode base64 strings back to bytes.

        Args:
            obj: Object to decode (dict, list, or primitive)

        Returns:
            Object with base64 strings converted back to bytes
        """
        if isinstance(obj, dict):
            if "__bytes__" in obj and len(obj) == 1:
                # This is a base64-encoded bytes object
                return base64.b64decode(obj["__bytes__"])
            return {k: self._decode_bytes(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._decode_bytes(item) for item in obj]
        else:
            return obj

    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired.

        Args:
            entry: CacheEntry to check

        Returns:
            True if expired
        """
        age = time.time() - entry.created_at
        return age > entry.ttl


class CacheKeyBuilder:
    """Helper for building consistent cache keys.

    Example:
        >>> builder = CacheKeyBuilder()
        >>> key = builder.fetch_key("https://example.com", {"timeout": 30})
        'fetch:https://example.com:timeout=30'
    """

    @staticmethod
    def fetch_key(url: str, params: dict[str, Any] | None = None) -> str:
        """Build cache key for fetch operation.

        Args:
            url: Target URL
            params: Fetch parameters

        Returns:
            Cache key string
        """
        parts = ["fetch", url]
        if params:
            param_str = ":".join(f"{k}={v}" for k, v in sorted(params.items()))
            parts.append(param_str)
        return ":".join(parts)

    @staticmethod
    def extract_key(url: str, config: dict[str, Any] | None = None) -> str:
        """Build cache key for extraction.

        Args:
            url: Source URL
            config: Extraction config

        Returns:
            Cache key string
        """
        parts = ["extract", url]
        if config:
            config_str = ":".join(f"{k}={v}" for k, v in sorted(config.items()))
            parts.append(config_str)
        return ":".join(parts)

    @staticmethod
    def summary_key(
        url: str,
        query: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> str:
        """Build cache key for summary.

        Args:
            url: Source URL
            query: Query string
            config: Summarization config

        Returns:
            Cache key string
        """
        parts = ["summary", url]
        if query:
            parts.append(f"query={query}")
        if config:
            config_str = ":".join(f"{k}={v}" for k, v in sorted(config.items()))
            parts.append(config_str)
        return ":".join(parts)
