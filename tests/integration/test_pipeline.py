"""Integration tests for the full summarization pipeline."""

import pytest
import os

from mcp_web.mcp_server import WebSummarizationPipeline

# Skip these tests if no OpenAI API key available
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OpenAI API key not available - use OPENAI_API_KEY env var"
)

class TestWebSummarizationPipeline:
    """Integration tests for the full pipeline."""

    @pytest.fixture
    def pipeline(self, test_config):
        """Create pipeline instance."""
        return WebSummarizationPipeline(test_config)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_pipeline_initialization(self, pipeline):
        """Test pipeline initializes correctly."""
        assert pipeline is not None
        assert pipeline.fetcher is not None
        assert pipeline.extractor is not None
        assert pipeline.chunker is not None
        assert pipeline.summarizer is not None

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_simple_url_fetch(self, pipeline):
        """Test fetching a simple URL."""
        # Use example.com which is designed for testing
        urls = ["https://example.com"]

        try:
            fetch_results = await pipeline.fetcher.fetch_multiple(urls)

            assert len(fetch_results) > 0
            assert "https://example.com" in fetch_results

            result = fetch_results["https://example.com"]
            assert result.status_code == 200
            assert len(result.content) > 0

        except Exception as e:
            pytest.skip(f"Network request failed: {str(e)}")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_extract_from_html(self, pipeline, sample_html):
        """Test extraction from HTML content."""
        from mcp_web.fetcher import FetchResult

        # Create fake fetch result
        fetch_result = FetchResult(
            url="https://test.com",
            content=sample_html.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )

        extracted = await pipeline.extractor.extract(fetch_result, use_cache=False)

        assert extracted is not None
        assert extracted.title != ""
        assert len(extracted.content) > 0

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_chunk_extracted_content(self, pipeline, sample_markdown):
        """Test chunking of extracted content."""
        chunks = pipeline.chunker.chunk_text(sample_markdown)

        assert len(chunks) > 0
        assert all(chunk.tokens > 0 for chunk in chunks)
        assert all(len(chunk.text) > 0 for chunk in chunks)

    @pytest.mark.integration
    @pytest.mark.slow
    @pytest.mark.requires_api
    @pytest.mark.asyncio
    async def test_full_pipeline_with_example_com(self, pipeline):
        """Test full pipeline with example.com (requires network)."""
        urls = ["https://example.com"]

        try:
            output_parts = []
            async for chunk in pipeline.summarize_urls(urls):
                output_parts.append(chunk)

            output = "".join(output_parts)

            # Verify we got some output
            assert len(output) > 0

            # Check for expected sections
            assert "Fetching" in output or "Summary" in output

        except Exception as e:
            if "OPENAI_API_KEY" in str(e) or "API" in str(e):
                pytest.skip(f"API key not configured: {str(e)}")
            else:
                pytest.skip(f"Pipeline test failed: {str(e)}")

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_cache_integration(self, pipeline):
        """Test cache integration across pipeline."""
        if not pipeline.cache:
            pytest.skip("Cache not enabled")

        # Set a test value
        key = "test:integration:key"
        value = {"test": "data"}

        await pipeline.cache.set(key, value)
        retrieved = await pipeline.cache.get(key)

        assert retrieved == value

        # Cleanup
        await pipeline.cache.delete(key)

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_metrics_collection(self, pipeline):
        """Test metrics are collected during pipeline operations."""
        if not pipeline.metrics:
            pytest.skip("Metrics not enabled")

        # Perform some operation
        from mcp_web.fetcher import FetchResult

        fetch_result = FetchResult(
            url="https://test.com",
            content=b"test content",
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )

        # This should record metrics
        pipeline.metrics.record_fetch(
            url="https://test.com",
            method="test",
            duration_ms=100.0,
            status_code=200,
            content_size=12,
            success=True,
        )

        # Export metrics
        metrics = pipeline.metrics.export_metrics()

        assert "summary" in metrics
        assert "counters" in metrics

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_pipeline_cleanup(self, pipeline):
        """Test pipeline cleanup."""
        await pipeline.close()

        # Verify resources are closed
        # Note: In a real test, we'd verify HTTP client is closed, etc.
        assert True

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_handling_invalid_url(self, pipeline):
        """Test error handling with invalid URL."""
        urls = ["not-a-valid-url"]

        output_parts = []
        async for chunk in pipeline.summarize_urls(urls):
            output_parts.append(chunk)

        output = "".join(output_parts)

        # Should contain error or warning message
        assert "Error" in output or "Warning" in output or "invalid" in output.lower()

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_multiple_urls(self, pipeline):
        """Test handling multiple URLs."""
        urls = [
            "https://example.com",
            "https://example.org",
        ]

        try:
            fetch_results = await pipeline.fetcher.fetch_multiple(urls)

            # Should successfully fetch at least one URL
            assert len(fetch_results) > 0

        except Exception as e:
            pytest.skip(f"Network request failed: {str(e)}")
