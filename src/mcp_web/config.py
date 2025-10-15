"""Configuration management for MCP-Web.

Uses pydantic-settings for type-safe configuration from environment variables
and config files. Supports multiple LLM providers (OpenAI, Ollama, etc).
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file at module import (before any config instantiation)
load_dotenv()


class FetcherSettings(BaseSettings):
    """Fetcher configuration."""

    timeout: int = Field(default=30, description="HTTP request timeout in seconds")
    playwright_timeout: int = Field(
        default=60, description="Playwright browser timeout in seconds (longer than httpx)"
    )
    max_concurrent: int = Field(default=5, description="Max concurrent fetch operations")
    enable_fallback: bool = Field(
        default=True, description="Enable Playwright fallback for JS-heavy sites"
    )
    use_playwright_fallback: bool = Field(
        default=True, description="Enable Playwright fallback (deprecated, use enable_fallback)"
    )
    user_agent: str = Field(
        default="mcp-web/0.1.0 (compatible; AI assistant)",
        description="User-Agent header",
    )
    respect_robots_txt: bool = Field(default=True, description="Honor robots.txt rules")
    crawl_delay_override: float | None = Field(
        default=None, description="Override crawl-delay from robots.txt (seconds)"
    )
    max_retries: int = Field(default=3, description="Max retry attempts")
    retry_delay: float = Field(default=1.0, description="Delay between retries (seconds)")

    model_config = SettingsConfigDict(env_prefix="MCP_WEB_FETCHER_")


class ExtractorSettings(BaseSettings):
    """Content extractor configuration."""

    favor_recall: bool = Field(
        default=True, description="Maximize content extraction (vs precision)"
    )
    include_comments: bool = Field(default=True, description="Extract comment sections")
    include_tables: bool = Field(default=True, description="Extract table content")
    include_links: bool = Field(default=True, description="Extract link targets")
    include_images: bool = Field(default=True, description="Extract image metadata")
    extract_metadata: bool = Field(default=True, description="Extract page metadata")

    model_config = SettingsConfigDict(env_prefix="MCP_WEB_EXTRACTOR_")


class ChunkerSettings(BaseSettings):
    """Content chunking configuration."""

    strategy: Literal["hierarchical", "semantic", "fixed"] = Field(
        default="hierarchical", description="Chunking strategy"
    )
    chunk_size: int = Field(default=512, description="Target tokens per chunk")
    chunk_overlap: int = Field(default=50, description="Overlap between chunks (tokens)")
    min_chunk_size: int = Field(default=100, description="Minimum chunk size (tokens)")
    max_chunk_size: int = Field(default=1024, description="Maximum chunk size (tokens)")
    preserve_code_blocks: bool = Field(
        default=True, description="Keep code blocks intact when possible"
    )

    model_config = SettingsConfigDict(env_prefix="MCP_WEB_CHUNKER_")


class SummarizerSettings(BaseSettings):
    """Summarizer configuration.

    Supports multiple LLM providers:
    - OpenAI (default): api.openai.com
    - Ollama: localhost:11434
    - LM Studio: localhost:1234
    - LocalAI: localhost:8080
    - Custom: any OpenAI-compatible API
    """

    # Provider configuration
    provider: Literal["openai", "ollama", "lmstudio", "localai", "custom"] = Field(
        default="openai", description="LLM provider type"
    )
    model: str = Field(default="gpt-4o-mini", description="LLM model to use")

    # Generation parameters
    temperature: float = Field(
        default=0.3,
        ge=0.0,
        le=2.0,
        description="LLM temperature (0=deterministic, 2=creative)",
    )
    max_tokens: int = Field(default=2048, description="Max tokens in summary")
    streaming: bool = Field(default=True, description="Enable streaming output")
    stop_sequences: list[str] = Field(
        default_factory=list,
        description="Stop sequences to prevent over-generation (e.g., ['\n\n\n', '---'])",
    )
    adaptive_max_tokens: bool = Field(
        default=False,
        description="Automatically adjust max_tokens based on input size for better performance",
    )
    max_tokens_ratio: float = Field(
        default=0.5,
        ge=0.1,
        le=1.0,
        description=(
            "Ratio of input tokens to max output tokens "
            "when adaptive_max_tokens is enabled"
        ),
    )

    # Map-reduce configuration
    map_reduce_threshold: int = Field(
        default=8000, description="Token threshold for map-reduce strategy"
    )
    parallel_map: bool = Field(
        default=True,
        description="Use parallel map phase (asyncio.gather) for better performance",
    )
    streaming_map: bool = Field(
        default=False,
        description=(
            "Stream map progress updates (asyncio.as_completed) - "
            "better UX but slightly slower"
        ),
    )

    # API configuration
    api_key: str | None = Field(default=None, description="API key (if required)")
    api_base: str | None = Field(
        default=None, description="API base URL (auto-detected by provider)"
    )
    timeout: int = Field(default=120, description="API request timeout in seconds")

    # Security settings
    max_summary_length: int = Field(
        default=10000, description="Maximum summary length (safety limit)"
    )
    content_filtering: bool = Field(default=True, description="Enable content filtering for safety")

    model_config = SettingsConfigDict(env_prefix="MCP_WEB_SUMMARIZER_")

    def get_api_base(self) -> str:
        """Get API base URL based on provider.

        Returns:
            API base URL for the configured provider
        """
        if self.api_base:
            return self.api_base

        provider_urls = {
            "openai": "https://api.openai.com/v1",
            "ollama": "http://localhost:11434/v1",
            "lmstudio": "http://localhost:1234/v1",
            "localai": "http://localhost:8080/v1",
        }

        return provider_urls.get(self.provider, "https://api.openai.com/v1")

    def get_api_key(self) -> str | None:
        """Get API key based on provider.

        Local providers don't require API keys.

        Returns:
            API key or None for local providers
        """
        if self.api_key:
            return self.api_key

        # Local providers don't need API keys
        if self.provider in ("ollama", "lmstudio", "localai"):
            return "not-needed"

        # Try to get from environment
        return os.getenv("OPENAI_API_KEY")


class CacheSettings(BaseSettings):
    """Caching configuration."""

    enabled: bool = Field(default=True, description="Enable caching")
    cache_dir: str = Field(default="~/.cache/mcp-web", description="Cache directory path")
    ttl: int = Field(default=7 * 24 * 3600, description="Cache TTL (seconds)")
    max_size: int = Field(default=1024 * 1024 * 1024, description="Max cache size (bytes)")
    eviction_policy: Literal["lru", "lfu"] = Field(
        default="lru", description="Cache eviction policy"
    )

    model_config = SettingsConfigDict(env_prefix="MCP_WEB_CACHE_")


class MetricsSettings(BaseSettings):
    """Metrics and logging configuration."""

    enabled: bool = Field(default=True, description="Enable metrics collection")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO", description="Logging level"
    )
    structured_logging: bool = Field(default=True, description="Use structured JSON logs")
    metrics_export_path: str | None = Field(default=None, description="Export metrics to file")

    model_config = SettingsConfigDict(env_prefix="MCP_WEB_METRICS_")


class Config(BaseSettings):
    """Root configuration for mcp-web."""

    # Sub-configurations
    fetcher: FetcherSettings = Field(default_factory=FetcherSettings)
    extractor: ExtractorSettings = Field(default_factory=ExtractorSettings)
    chunker: ChunkerSettings = Field(default_factory=ChunkerSettings)
    summarizer: SummarizerSettings = Field(default_factory=SummarizerSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    metrics: MetricsSettings = Field(default_factory=MetricsSettings)

    model_config = SettingsConfigDict(
        env_prefix="MCP_WEB_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    def __post_init__(self) -> None:
        """Post-initialization validation."""
        # Expand cache directory path
        if self.cache.cache_dir:
            self.cache.cache_dir = str(Path(self.cache.cache_dir).expanduser().resolve())


def load_config(
    _config_file: Path | None = None,
    overrides: dict[str, Any] | None = None,
) -> Config:
    """Load configuration from file and environment.

    Args:
        config_file: Optional path to YAML config file
        overrides: Optional dict of override values

    Returns:
        Loaded and validated configuration

    Example:
        >>> config = load_config()
        >>> config.summarizer.model
        'gpt-4o-mini'
    """
    # TODO: Add YAML file loading support in future
    # For now, load from environment variables
    config = Config()

    # Apply overrides if provided
    if overrides:
        for key, value in overrides.items():
            if hasattr(config, key):
                setattr(config, key, value)

    return config


def get_default_config() -> Config:
    """Get default configuration (for testing/development).

    Returns:
        Config with all default values
    """
    return Config()
