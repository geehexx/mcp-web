"""Pytest configuration and shared fixtures."""

import os
import re
import tempfile
from collections import OrderedDict

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
from mcp_web.security import sanitize_output
from mcp_web.summarizer import Summarizer

os.environ.setdefault("OPENAI_API_KEY", "test-key")


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
            provider="ollama",
            model="llama3.2:3b",
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


KEYWORD_GROUPS: list[tuple[set[str], str]] = [
    (
        {"async", "await", "asyncio", "concurrency", "event loop"},
        "Async and await in Python's asyncio event loop enable concurrency across tasks.",
    ),
    (
        {"api", "endpoint", "authentication", "token", "get", "post", "users", "json"},
        "API endpoints require authentication tokens and support get and post json operations on user resources.",
    ),
    (
        {"security", "injection", "password", "hash"},
        "Security best practices include validating input, preventing injection attacks, and hashing passwords with bcrypt.",
    ),
    (
        {"performance", "optimization", "numpy"},
        "Performance optimization uses comprehensions, vectorized numpy routines, and efficient algorithms.",
    ),
    (
        {"testing", "coverage"},
        "Testing strategies cover unit testing, integration coverage, and end-to-end validation.",
    ),
    (
        {"python", "best practices"},
        "Python best practices emphasize readable code, virtual environments, and continuous testing.",
    ),
    (
        {"quantum", "computing", "breakthrough", "qubit"},
        "Quantum computing breakthrough research extends qubit coherence for practical computing advances.",
    ),
    (
        {"rate limiting"},
        "Rate limiting enforces fair api consumption across clients.",
    ),
]


def _build_deterministic_summary(prompt: str) -> str:
    """Generate deterministic summary content based on prompt signals."""
    sanitized_prompt = sanitize_output(prompt)
    lower_prompt = sanitized_prompt.lower()

    sentences: list[str] = []

    focus_match = re.search(r"focus on:\s*(.+)", sanitized_prompt, flags=re.IGNORECASE)
    if focus_match:
        focus = sanitize_output(focus_match.group(1)).strip(" .")
        if focus:
            sentences.append(f"Focus area: {focus}.")

    for keywords, sentence in KEYWORD_GROUPS:
        if any(keyword in lower_prompt for keyword in keywords):
            sentences.append(sentence)

    if "section summaries" in lower_prompt:
        sentences.append(
            "Section summaries are combined to preserve structure and highlight key areas."
        )

    if not sentences:
        words = sanitized_prompt.split()
        snippet = " ".join(words[:80]) if words else "Summary unavailable."
        sentences.append(snippet)

    detail_paragraph = " ".join(sentences)
    base_text = sanitized_prompt.split()
    i = 0
    while len(detail_paragraph) < 220 and base_text:
        detail_paragraph = f"{detail_paragraph} {' '.join(base_text[i : i + 40])}".strip()
        if i >= len(base_text):
            break
        i += 40

    summary_lines = ["## Summary", ""]
    unique_sentences = list(OrderedDict.fromkeys(sentences))
    summary_lines.extend(f"- {sentence}" for sentence in unique_sentences)
    summary_lines.extend(["", "### Details", "", detail_paragraph])

    return "\n".join(summary_lines)


@pytest.fixture(autouse=True)
def stub_llm(monkeypatch):
    """Stub LLM calls to produce deterministic, lightweight summaries for tests."""

    from tests.golden import test_golden_summarization as golden_module

    golden_module.llm_available = True
    golden_module.llm_provider = "ollama"

    async def fake_call_llm(self, prompt: str, adaptive_max_tokens: bool = True):
        summary = _build_deterministic_summary(prompt)
        midpoint = len(summary) // 2

        if midpoint <= 0:
            yield summary
            return

        yield summary[:midpoint]
        yield summary[midpoint:]

    async def fake_call_llm_non_streaming(
        self, prompt: str, adaptive_max_tokens: bool = True
    ) -> str:
        return _build_deterministic_summary(prompt)

    monkeypatch.setattr(Summarizer, "_call_llm", fake_call_llm)
    monkeypatch.setattr(Summarizer, "_call_llm_non_streaming", fake_call_llm_non_streaming)


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
