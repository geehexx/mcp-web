"""Unit tests for summarizer caching functionality.

Tests verify that summarization results are cached based on content hash + query,
reducing redundant API calls and improving performance.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from mcp_web.cache import CacheKeyBuilder, CacheManager
from mcp_web.chunker import Chunk
from mcp_web.summarizer import Summarizer


@pytest.fixture
def test_cache(tmp_path):
    """Create a test cache manager."""
    cache_dir = tmp_path / "test_cache"
    return CacheManager(str(cache_dir), ttl=3600)


@pytest.fixture
def sample_chunks():
    """Sample text chunks for testing."""
    return [
        Chunk(
            text="Section 1: This is the first section with important content.",
            tokens=50,
            start_pos=0,
            end_pos=50,
            metadata={},
        ),
        Chunk(
            text="Section 2: This is the second section with more content.",
            tokens=50,
            start_pos=50,
            end_pos=100,
            metadata={},
        ),
    ]


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client that returns deterministic responses."""
    with patch("mcp_web.summarizer.AsyncOpenAI") as mock_class:
        mock_client = AsyncMock()

        # Mock streaming response
        async def mock_stream_generator():
            """Generate mock streaming chunks."""
            chunks = ["This ", "is ", "a ", "test ", "summary."]
            for chunk_text in chunks:
                chunk = MagicMock()
                chunk.choices = [MagicMock()]
                chunk.choices[0].delta = MagicMock()
                chunk.choices[0].delta.content = chunk_text
                chunk.choices[0].finish_reason = None
                yield chunk

        # Mock non-streaming response
        def mock_non_stream_response():
            response = MagicMock()
            response.choices = [MagicMock()]
            response.choices[0].message = MagicMock()
            response.choices[0].message.content = "This is a test summary."
            return response

        async def create_completion(**kwargs):
            if kwargs.get("stream", False):
                return mock_stream_generator()
            else:
                return mock_non_stream_response()

        mock_client.chat.completions.create = create_completion
        mock_class.return_value = mock_client

        yield mock_client


@pytest.mark.unit
@pytest.mark.asyncio
class TestSummarizerCaching:
    """Test summarization caching functionality."""

    async def test_summarizer_accepts_cache(self, test_config, test_cache):
        """Test that Summarizer can be initialized with cache."""
        summarizer = Summarizer(test_config.summarizer, cache=test_cache)
        assert summarizer.cache == test_cache

    async def test_summarizer_without_cache(self, test_config):
        """Test that Summarizer works without cache (backward compatibility)."""
        summarizer = Summarizer(test_config.summarizer, cache=None)
        assert summarizer.cache is None

    async def test_summarize_with_cache_hit(self, test_config, test_cache, sample_chunks):
        """Test summarization with cache hit returns cached result without LLM call."""
        summarizer = Summarizer(test_config.summarizer, cache=test_cache)

        # Pre-populate cache
        content_hash = summarizer._compute_content_hash(sample_chunks)
        cache_key = CacheKeyBuilder.summary_key(
            content_hash=content_hash,
            query="test query",
            model=test_config.summarizer.model,
        )
        cached_summary = "This is a cached summary from previous run."
        await test_cache.set(cache_key, cached_summary)

        # Call summarize - should return cached result
        result = []
        async for chunk in summarizer.summarize_chunks(
            sample_chunks,
            query="test query",
            sources=["https://test.com"],
            use_cache=True,
        ):
            result.append(chunk)

        summary = "".join(result)
        assert summary == cached_summary

    async def test_cache_key_includes_content_hash(self, test_config, sample_chunks):
        """Test cache key is based on content hash, not URL."""
        summarizer = Summarizer(test_config.summarizer, cache=None)

        content_hash = summarizer._compute_content_hash(sample_chunks)

        # Hash should be deterministic and based on content
        assert len(content_hash) == 64  # SHA-256 hash length
        assert content_hash == summarizer._compute_content_hash(sample_chunks)

    async def test_cache_key_varies_with_query(self, test_config, test_cache, sample_chunks):
        """Test different queries produce different cache keys."""
        summarizer = Summarizer(test_config.summarizer, cache=test_cache)

        content_hash = summarizer._compute_content_hash(sample_chunks)

        key1 = CacheKeyBuilder.summary_key(
            content_hash=content_hash,
            query="query1",
            model=test_config.summarizer.model,
        )

        key2 = CacheKeyBuilder.summary_key(
            content_hash=content_hash,
            query="query2",
            model=test_config.summarizer.model,
        )

        assert key1 != key2

    async def test_cache_key_varies_with_content(self, test_config, test_cache):
        """Test different content produces different cache keys."""
        summarizer = Summarizer(test_config.summarizer, cache=test_cache)

        chunks1 = [Chunk(text="Content A", tokens=10, start_pos=0, end_pos=10, metadata={})]
        chunks2 = [Chunk(text="Content B", tokens=10, start_pos=0, end_pos=10, metadata={})]

        hash1 = summarizer._compute_content_hash(chunks1)
        hash2 = summarizer._compute_content_hash(chunks2)

        assert hash1 != hash2

    async def test_cache_with_model_parameter(self):
        """Test cache key includes model to avoid cross-model collisions."""
        content_hash = "test_hash"

        key1 = CacheKeyBuilder.summary_key(content_hash=content_hash, query="test", model="gpt-4")

        key2 = CacheKeyBuilder.summary_key(
            content_hash=content_hash, query="test", model="claude-3"
        )

        assert key1 != key2
