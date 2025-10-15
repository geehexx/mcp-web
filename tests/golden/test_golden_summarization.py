"""Golden tests for summarization with deterministic verification.

These tests verify actual LLM summarization output using:
1. Deterministic models (temperature=0)
2. Golden HTML samples with expected characteristics
3. Content verification (must/should contain keywords)
4. Map-reduce strategy testing

For CI/CD:
- Tests use local LLM if available (Ollama preferred)
- Falls back to OpenAI with temperature=0 for determinism
- Can be skipped if no LLM available
"""

import os

import pytest

try:
    import httpx
except ImportError:  # pragma: no cover - optional dependency for tests only
    httpx = None  # type: ignore[assignment]

from mcp_web.chunker import TextChunker
from mcp_web.config import ChunkerSettings, SummarizerSettings
from mcp_web.extractor import ContentExtractor, FetchResult
from mcp_web.summarizer import Summarizer
from tests.fixtures.golden_data import (
    BLOG_POST_EXPECTED,
    BLOG_POST_HTML,
    NEWS_ARTICLE_EXPECTED,
    NEWS_ARTICLE_HTML,
    SIMPLE_ARTICLE_EXPECTED,
    SIMPLE_ARTICLE_HTML,
    TECHNICAL_DOC_EXPECTED,
    TECHNICAL_DOC_HTML,
)


def check_llm_available() -> tuple[bool, str]:
    """Check if any LLM is available for testing.

    Returns:
        (available, provider_name)
    """
    # Check Ollama
    if httpx is not None:
        try:
            response = httpx.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                return True, "ollama"
        except (httpx.HTTPError, httpx.TimeoutException, OSError):
            pass

    # Check OpenAI
    if os.getenv("OPENAI_API_KEY"):
        return True, "openai"

    # Check LM Studio
    if httpx is not None:
        try:
            response = httpx.get("http://localhost:1234/v1/models", timeout=2)
            if response.status_code == 200:
                return True, "lmstudio"
        except (httpx.HTTPError, httpx.TimeoutException, OSError):
            pass

    return False, "none"


# Skip all tests if no LLM available
llm_available, llm_provider = check_llm_available()
pytestmark = pytest.mark.skipif(
    not llm_available, reason="No LLM available for testing (checked: Ollama, OpenAI, LM Studio)"
)


@pytest.fixture
def summarizer_config():
    """Get summarizer config for deterministic testing."""
    if llm_provider == "ollama":
        return SummarizerSettings(
            provider="ollama",
            model="llama3.2:3b",  # Fast, small model for testing
            temperature=0.0,  # Deterministic
            max_tokens=1024,
            streaming=False,
        )
    elif llm_provider == "lmstudio":
        return SummarizerSettings(
            provider="lmstudio",
            model="local-model",
            temperature=0.0,
            max_tokens=1024,
            streaming=False,
        )
    else:  # OpenAI
        return SummarizerSettings(
            provider="openai",
            model="gpt-4o-mini",
            temperature=0.0,  # Deterministic
            max_tokens=1024,
            streaming=False,
        )


@pytest.fixture
def chunker_config():
    """Get chunker config."""
    return ChunkerSettings(
        strategy="hierarchical",
        chunk_size=512,
        chunk_overlap=50,
    )


@pytest.fixture
async def summarizer(summarizer_config):
    """Create summarizer instance."""
    s = Summarizer(summarizer_config)
    yield s
    await s.close()


@pytest.fixture
def chunker(chunker_config):
    """Create chunker instance."""
    return TextChunker(chunker_config)


@pytest.fixture
def extractor():
    """Create extractor instance."""
    from mcp_web.config import ExtractorSettings

    return ContentExtractor(ExtractorSettings(), cache=None)


def verify_summary(summary: str, expected: dict) -> tuple[bool, list[str]]:
    """Verify summary meets expectations.

    Args:
        summary: Generated summary
        expected: Expected characteristics dict

    Returns:
        (passed, list of failures)
    """
    failures = []
    summary_lower = summary.lower()

    # Check length
    if len(summary) < expected.get("summary_min_length", 0):
        failures.append(f"Summary too short: {len(summary)} < {expected['summary_min_length']}")

    if len(summary) > expected.get("summary_max_length", 100000):
        failures.append(f"Summary too long: {len(summary)} > {expected['summary_max_length']}")

    # Check must-contain keywords
    for keyword in expected.get("summary_must_contain", []):
        if keyword.lower() not in summary_lower:
            failures.append(f"Missing required keyword: '{keyword}'")

    # Check should-contain keywords (warn but don't fail)
    missing_should = []
    for keyword in expected.get("summary_should_contain", []):
        if keyword.lower() not in summary_lower:
            missing_should.append(keyword)

    if missing_should:
        # Don't fail, but log warning
        print(f"Warning: Missing suggested keywords: {missing_should}")

    return len(failures) == 0, failures


@pytest.mark.golden
@pytest.mark.requires_api
@pytest.mark.asyncio
class TestGoldenSummarization:
    """Test summarization with golden HTML samples."""

    async def test_simple_article_summary(self, extractor, chunker, summarizer):
        """Test summarization of simple article."""
        # Extract content
        fetch_result = FetchResult(
            url="https://test.com/article",
            content=SIMPLE_ARTICLE_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        extracted = await extractor.extract(fetch_result, use_cache=False)

        # Chunk content
        chunks = chunker.chunk_text(extracted.content)
        assert len(chunks) > 0

        # Summarize
        summary_parts = []
        async for chunk in summarizer.summarize_chunks(chunks):
            summary_parts.append(chunk)

        summary = "".join(summary_parts)

        # Verify
        passed, failures = verify_summary(summary, SIMPLE_ARTICLE_EXPECTED)

        if not passed:
            print(f"\nGenerated summary:\n{summary}\n")
            print(f"Failures: {failures}")

        assert passed, f"Summary verification failed: {failures}"

        # Additional checks
        assert len(summary) > 100, "Summary is too short"
        assert "async" in summary.lower() or "asynchronous" in summary.lower()

    async def test_technical_doc_summary(self, extractor, chunker, summarizer):
        """Test summarization of technical documentation."""
        fetch_result = FetchResult(
            url="https://test.com/docs",
            content=TECHNICAL_DOC_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        extracted = await extractor.extract(fetch_result, use_cache=False)
        chunks = chunker.chunk_text(extracted.content)

        summary_parts = []
        async for chunk in summarizer.summarize_chunks(chunks):
            summary_parts.append(chunk)

        summary = "".join(summary_parts)

        passed, failures = verify_summary(summary, TECHNICAL_DOC_EXPECTED)
        assert passed, f"Summary verification failed: {failures}"

        # Technical docs should mention API endpoints
        assert "api" in summary.lower()

    async def test_news_article_summary(self, extractor, chunker, summarizer):
        """Test summarization of news article."""
        fetch_result = FetchResult(
            url="https://test.com/news",
            content=NEWS_ARTICLE_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        extracted = await extractor.extract(fetch_result, use_cache=False)
        chunks = chunker.chunk_text(extracted.content)

        summary_parts = []
        async for chunk in summarizer.summarize_chunks(chunks):
            summary_parts.append(chunk)

        summary = "".join(summary_parts)

        passed, failures = verify_summary(summary, NEWS_ARTICLE_EXPECTED)
        assert passed, f"Summary verification failed: {failures}"

    async def test_blog_post_summary(self, extractor, chunker, summarizer):
        """Test summarization of blog post."""
        fetch_result = FetchResult(
            url="https://test.com/blog",
            content=BLOG_POST_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        extracted = await extractor.extract(fetch_result, use_cache=False)
        chunks = chunker.chunk_text(extracted.content)

        summary_parts = []
        async for chunk in summarizer.summarize_chunks(chunks):
            summary_parts.append(chunk)

        summary = "".join(summary_parts)

        passed, failures = verify_summary(summary, BLOG_POST_EXPECTED)
        assert passed, f"Summary verification failed: {failures}"


@pytest.mark.golden
@pytest.mark.requires_api
@pytest.mark.asyncio
class TestQueryFocusedSummarization:
    """Test query-focused summarization."""

    async def test_query_focused_async_article(self, extractor, chunker, summarizer):
        """Test query-focused summary on async article."""
        fetch_result = FetchResult(
            url="https://test.com/article",
            content=SIMPLE_ARTICLE_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        extracted = await extractor.extract(fetch_result, use_cache=False)
        chunks = chunker.chunk_text(extracted.content)

        # Query-focused summary
        query = "How does the event loop work?"
        summary_parts = []
        async for chunk in summarizer.summarize_chunks(chunks, query=query):
            summary_parts.append(chunk)

        summary = "".join(summary_parts)

        # Should focus on event loop
        assert "event loop" in summary.lower() or "eventloop" in summary.lower()
        assert len(summary) > 50

    async def test_query_focused_api_docs(self, extractor, chunker, summarizer):
        """Test query-focused summary on API docs."""
        fetch_result = FetchResult(
            url="https://test.com/docs",
            content=TECHNICAL_DOC_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        extracted = await extractor.extract(fetch_result, use_cache=False)
        chunks = chunker.chunk_text(extracted.content)

        query = "What are the authentication requirements?"
        summary_parts = []
        async for chunk in summarizer.summarize_chunks(chunks, query=query):
            summary_parts.append(chunk)

        summary = "".join(summary_parts)

        # Should focus on authentication
        assert "auth" in summary.lower() or "token" in summary.lower()


@pytest.mark.golden
@pytest.mark.requires_api
@pytest.mark.asyncio
@pytest.mark.slow
class TestMapReduceSummarization:
    """Test map-reduce summarization for large documents."""

    async def test_map_reduce_large_document(self, extractor, chunker, summarizer_config):
        """Test map-reduce on large document."""
        # Force map-reduce by lowering threshold
        summarizer_config.map_reduce_threshold = 1000  # Low threshold
        summarizer = Summarizer(summarizer_config)

        try:
            # Create large document (repeat article multiple times)
            large_html = SIMPLE_ARTICLE_HTML * 3  # ~3x content

            fetch_result = FetchResult(
                url="https://test.com/large",
                content=large_html.encode("utf-8"),
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="test",
            )
            extracted = await extractor.extract(fetch_result, use_cache=False)
            chunks = chunker.chunk_text(extracted.content)

            # Should have multiple chunks
            assert len(chunks) > 3, "Need multiple chunks for map-reduce test"

            # Calculate total tokens
            total_tokens = sum(c.tokens for c in chunks)
            assert total_tokens > summarizer_config.map_reduce_threshold

            # Summarize (should trigger map-reduce)
            summary_parts = []
            async for chunk in summarizer.summarize_chunks(chunks):
                summary_parts.append(chunk)

            summary = "".join(summary_parts)

            # Verify summary
            assert len(summary) > 200, "Map-reduce summary too short"
            assert "async" in summary.lower() or "asynchronous" in summary.lower()

            # Map-reduce should still capture key concepts
            for keyword in SIMPLE_ARTICLE_EXPECTED["summary_must_contain"]:
                assert keyword.lower() in summary.lower(), f"Map-reduce lost keyword: {keyword}"

        finally:
            await summarizer.close()

    async def test_map_reduce_preserves_structure(self, extractor, chunker, summarizer_config):
        """Test that map-reduce preserves document structure."""
        summarizer_config.map_reduce_threshold = 1000
        summarizer = Summarizer(summarizer_config)

        try:
            # Use technical doc (has clear structure)
            large_html = TECHNICAL_DOC_HTML * 2

            fetch_result = FetchResult(
                url="https://test.com/docs",
                content=large_html.encode("utf-8"),
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="test",
            )
            extracted = await extractor.extract(fetch_result, use_cache=False)
            chunks = chunker.chunk_text(extracted.content)

            total_tokens = sum(c.tokens for c in chunks)
            assert total_tokens > summarizer_config.map_reduce_threshold

            summary_parts = []
            async for chunk in summarizer.summarize_chunks(chunks):
                summary_parts.append(chunk)

            summary = "".join(summary_parts)

            # Should still mention key sections
            assert "api" in summary.lower()
            assert "authentication" in summary.lower() or "auth" in summary.lower()

        finally:
            await summarizer.close()


@pytest.mark.golden
@pytest.mark.requires_api
@pytest.mark.asyncio
class TestDeterminism:
    """Test summarization determinism (temperature=0)."""

    async def test_deterministic_summary(self, extractor, chunker, summarizer_config):
        """Test that temperature=0 produces consistent results."""
        # Ensure temperature=0
        summarizer_config.temperature = 0.0
        summarizer = Summarizer(summarizer_config)

        try:
            fetch_result = FetchResult(
                url="https://test.com/article",
                content=SIMPLE_ARTICLE_HTML.encode("utf-8"),
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="test",
            )
            extracted = await extractor.extract(fetch_result, use_cache=False)
            chunks = chunker.chunk_text(extracted.content)

            # Generate summary twice
            summaries = []
            for _ in range(2):
                summary_parts = []
                async for chunk in summarizer.summarize_chunks(chunks):
                    summary_parts.append(chunk)
                summaries.append("".join(summary_parts))

            # With temperature=0, summaries should be very similar
            # (Allow small differences due to LLM non-determinism edge cases)
            similarity_ratio = len(set(summaries[0].split()) & set(summaries[1].split())) / max(
                len(summaries[0].split()), len(summaries[1].split())
            )

            assert similarity_ratio > 0.7, (
                f"Summaries not similar enough ({similarity_ratio:.2f}). "
                f"Temperature=0 should be more deterministic."
            )

        finally:
            await summarizer.close()


@pytest.mark.golden
@pytest.mark.requires_api
@pytest.mark.asyncio
class TestLocalLLMSupport:
    """Test local LLM providers."""

    @pytest.mark.skipif(llm_provider != "ollama", reason="Ollama not available")
    async def test_ollama_summarization(self, extractor, chunker):
        """Test summarization with Ollama."""
        config = SummarizerSettings(
            provider="ollama",
            model="llama3.2:3b",
            temperature=0.0,
            max_tokens=512,
        )
        summarizer = Summarizer(config)

        try:
            fetch_result = FetchResult(
                url="https://test.com/article",
                content=SIMPLE_ARTICLE_HTML.encode("utf-8"),
                content_type="text/html",
                headers={},
                status_code=200,
                fetch_method="test",
            )
            extracted = await extractor.extract(fetch_result, use_cache=False)
            chunks = chunker.chunk_text(extracted.content)

            summary_parts = []
            async for chunk in summarizer.summarize_chunks(chunks):
                summary_parts.append(chunk)

            summary = "".join(summary_parts)

            assert len(summary) > 50, "Ollama summary too short"
            # Should contain some relevant content
            assert any(kw in summary.lower() for kw in ["async", "python", "code", "program"])

        finally:
            await summarizer.close()
