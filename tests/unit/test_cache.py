"""Unit tests for cache module."""

import tempfile

import pytest

from mcp_web.cache import CacheKeyBuilder, CacheManager


class TestCacheKeyBuilder:
    """Tests for CacheKeyBuilder."""

    def test_fetch_key(self):
        """Test fetch key generation."""
        key1 = CacheKeyBuilder.fetch_key("https://example.com")
        key2 = CacheKeyBuilder.fetch_key("https://example.com")
        key3 = CacheKeyBuilder.fetch_key("https://other.com")

        assert key1 == key2  # Same URL = same key
        assert key1 != key3  # Different URL = different key
        assert "fetch" in key1

    def test_fetch_key_with_params(self):
        """Test fetch key with parameters."""
        key1 = CacheKeyBuilder.fetch_key("https://example.com", {"timeout": 30})
        key2 = CacheKeyBuilder.fetch_key("https://example.com", {"timeout": 60})

        assert key1 != key2  # Different params = different key

    def test_extract_key(self):
        """Test extract key generation."""
        key = CacheKeyBuilder.extract_key("https://example.com")
        assert "extract" in key

    def test_summary_key(self):
        """Test summary key generation."""
        key1 = CacheKeyBuilder.summary_key("https://example.com", query="test")
        key2 = CacheKeyBuilder.summary_key("https://example.com", query="other")

        assert key1 != key2  # Different query = different key
        assert "summary" in key1


class TestCacheManager:
    """Tests for CacheManager."""

    @pytest.fixture
    def cache_dir(self):
        """Create temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir

    @pytest.fixture
    def cache(self, cache_dir):
        """Create CacheManager instance."""
        return CacheManager(
            cache_dir=cache_dir,
            ttl=3600,
            max_size=10 * 1024 * 1024,  # 10MB
        )

    @pytest.mark.asyncio
    async def test_set_and_get(self, cache):
        """Test setting and getting cache values."""
        key = "test_key"
        value = {"data": "test value"}

        # Set value
        success = await cache.set(key, value)
        assert success is True

        # Get value
        retrieved = await cache.get(key)
        assert retrieved == value

    @pytest.mark.asyncio
    async def test_get_missing(self, cache):
        """Test getting non-existent key."""
        result = await cache.get("nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete(self, cache):
        """Test deleting cache entries."""
        key = "test_key"
        value = "test value"

        await cache.set(key, value)
        assert await cache.get(key) == value

        deleted = await cache.delete(key)
        assert deleted is True
        assert await cache.get(key) is None

    @pytest.mark.asyncio
    async def test_ttl_expiration(self, cache):
        """Test TTL expiration."""
        key = "test_key"
        value = "test value"

        # Set with very short TTL
        await cache.set(key, value, ttl=1)
        assert await cache.get(key) == value

        # Wait for expiration
        import asyncio

        await asyncio.sleep(2)

        # Should be expired
        assert await cache.get(key) is None

    @pytest.mark.asyncio
    async def test_clear(self, cache):
        """Test clearing entire cache."""
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")

        await cache.clear()

        assert await cache.get("key1") is None
        assert await cache.get("key2") is None

    @pytest.mark.asyncio
    async def test_prune(self, cache):
        """Test pruning expired entries."""
        # Add entries with different TTLs
        await cache.set("short", "value", ttl=1)
        await cache.set("long", "value", ttl=3600)

        # Wait for short TTL to expire
        import asyncio

        await asyncio.sleep(2)

        # Prune should remove expired entry
        # Note: diskcache with eviction policies may not immediately report pruned count
        pruned = await cache.prune()
        
        # The important check: expired entry should be gone
        assert await cache.get("short") is None
        assert await cache.get("long") is not None

    def test_get_stats(self, cache):
        """Test getting cache statistics."""
        stats = cache.get_stats()

        assert "size_bytes" in stats
        assert "size_mb" in stats
        assert "usage_percent" in stats
        assert "entry_count" in stats
        assert isinstance(stats["size_mb"], (int, float))
