"""Pytest configuration and shared fixtures."""

import os
import tempfile

import pytest

from mcp_web.config import (
    CacheSettings,
    ChunkerSettings,
    Config,
    ExtractorSettings,
    FetcherSettings,
    MetricsSettings,
    SummarizerSettings,
)


@pytest.fixture
def temp_cache_dir():
    """Create temporary cache directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def test_config(temp_cache_dir):
    """Create test configuration."""
    return Config(
        fetcher=FetcherSettings(
            timeout=5,
            max_concurrent=2,
            use_playwright_fallback=False,  # Disable for tests
        ),
        extractor=ExtractorSettings(
            favor_recall=True,
            include_comments=True,
        ),
        chunker=ChunkerSettings(
            strategy="hierarchical",
            chunk_size=100,
            chunk_overlap=10,
        ),
        summarizer=SummarizerSettings(
            model="gpt-4o-mini",
            temperature=0.3,
            max_tokens=500,  # Lower for tests
        ),
        cache=CacheSettings(
            enabled=True,
            cache_dir=temp_cache_dir,
            ttl=3600,
            max_size=10 * 1024 * 1024,  # 10MB for tests
        ),
        metrics=MetricsSettings(
            enabled=True,
            log_level="WARNING",  # Reduce noise in tests
        ),
    )


@pytest.fixture
def sample_html():
    """Sample HTML content for testing."""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <header>
        <nav>Navigation</nav>
    </header>
    <main>
        <h1>Main Heading</h1>
        <p>This is the main content of the test page.</p>
        <p>It has multiple paragraphs for testing extraction.</p>

        <h2>Section 1</h2>
        <p>Content in section 1.</p>

        <pre><code>
def example():
    return "code example"
        </code></pre>

        <h2>Section 2</h2>
        <p>Content in section 2.</p>
    </main>
    <footer>Footer content</footer>
</body>
</html>
"""


@pytest.fixture
def sample_markdown():
    """Sample Markdown content for testing."""
    return """
# Introduction

This is the introduction section with some important content.

## Background

Some background information with **bold** and *italic* text.

## Methods

Description of methods used:

1. First method
2. Second method
3. Third method

### Code Example

```python
def hello_world():
    print("Hello, world!")
```

## Conclusion

Final thoughts and summary.
"""


@pytest.fixture
def sample_urls():
    """Sample URLs for testing."""
    return [
        "https://example.com",
        "https://example.org",
        "https://www.iana.org/domains/example",
    ]


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables for tests."""
    # Store original values
    original_env = {}
    test_env_keys = [
        "OPENAI_API_KEY",
        "MCP_WEB_CACHE_DIR",
        "MCP_WEB_LOG_LEVEL",
    ]

    for key in test_env_keys:
        if key in os.environ:
            original_env[key] = os.environ[key]

    yield

    # Restore original values
    for key in test_env_keys:
        if key in original_env:
            os.environ[key] = original_env[key]
        elif key in os.environ:
            del os.environ[key]


# Markers for test categorization
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: mark test as a unit test")
    config.addinivalue_line("markers", "integration: mark test as an integration test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "requires_api: mark test as requiring external API")
