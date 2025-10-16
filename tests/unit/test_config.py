"""Unit tests for config module."""

from mcp_web.config import (
    CacheSettings,
    ChunkerSettings,
    Config,
    ExtractorSettings,
    FetcherSettings,
    SummarizerSettings,
    get_default_config,
    load_config,
)


class TestFetcherSettings:
    """Tests for FetcherSettings."""

    def test_default_values(self):
        """Test default configuration values."""
        settings = FetcherSettings()

        assert settings.timeout == 30
        assert settings.max_concurrent == 5
        assert settings.use_playwright_fallback is True
        assert settings.max_retries == 3


class TestExtractorSettings:
    """Tests for ExtractorSettings."""

    def test_default_values(self):
        """Test default configuration values."""
        settings = ExtractorSettings()

        assert settings.favor_recall is True
        assert settings.include_comments is True
        assert settings.include_tables is True
        assert settings.extract_metadata is True


class TestChunkerSettings:
    """Tests for ChunkerSettings."""

    def test_default_values(self):
        """Test default configuration values."""
        settings = ChunkerSettings()

        assert settings.strategy == "hierarchical"
        assert settings.chunk_size == 512
        assert settings.chunk_overlap == 50
        assert settings.preserve_code_blocks is True
        assert settings.adaptive_chunking is True
        assert settings.code_chunk_size == 1024
        assert settings.dense_chunk_size == 768
        assert settings.code_block_threshold == 0.1
        assert settings.dense_sentence_threshold == 24


class TestSummarizerSettings:
    """Tests for SummarizerSettings."""

    def test_default_values(self):
        """Test default configuration values."""
        settings = SummarizerSettings()

        assert settings.model == "llama3.2:3b"
        assert settings.temperature == 0.3
        assert settings.max_tokens == 2048
        assert settings.streaming is True
        assert settings.map_reduce_threshold == 8000


class TestCacheSettings:
    """Tests for CacheSettings."""

    def test_default_values(self):
        """Test default configuration values."""
        settings = CacheSettings()

        assert settings.enabled is True
        assert settings.ttl == 7 * 24 * 3600  # 7 days
        assert settings.max_size == 1024 * 1024 * 1024  # 1GB
        assert settings.eviction_policy == "lru"


class TestConfig:
    """Tests for root Config."""

    def test_default_config(self):
        """Test default configuration."""
        config = Config()

        assert isinstance(config.fetcher, FetcherSettings)
        assert isinstance(config.extractor, ExtractorSettings)
        assert isinstance(config.chunker, ChunkerSettings)
        assert isinstance(config.summarizer, SummarizerSettings)
        assert isinstance(config.cache, CacheSettings)

    def test_load_config(self):
        """Test loading configuration."""
        config = load_config()

        assert config is not None
        assert config.fetcher.timeout > 0
        assert config.chunker.chunk_size > 0

    def test_get_default_config(self):
        """Test getting default configuration."""
        config = get_default_config()

        assert config is not None
        assert config.cache.enabled is True
