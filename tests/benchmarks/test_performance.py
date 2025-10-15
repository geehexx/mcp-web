"""Performance benchmarks for mcp-web components.

These tests measure and track performance of key operations.
"""

import asyncio

import pytest


@pytest.mark.benchmark
class TestTokenCountingPerformance:
    """Benchmark token counting operations."""

    def test_token_counting_speed(self, benchmark):
        """Benchmark token counting performance."""
        from mcp_web.utils import TokenCounter

        counter = TokenCounter()

        # Sample text of various sizes
        short_text = "Hello world! " * 10
        medium_text = "This is a test sentence. " * 100
        long_text = "Lorem ipsum dolor sit amet. " * 1000

        def count_tokens():
            c1 = counter.count_tokens(short_text)
            c2 = counter.count_tokens(medium_text)
            c3 = counter.count_tokens(long_text)
            return c1 + c2 + c3

        result = benchmark(count_tokens)

        # Should be very fast (< 10ms for all three) and return token counts
        assert result > 0

    def test_token_truncation_speed(self, benchmark):
        """Benchmark token truncation performance."""
        from mcp_web.utils import TokenCounter

        counter = TokenCounter()
        text = "This is a test word. " * 500  # ~2500 tokens

        result = benchmark(counter.truncate_to_tokens, text, 500)

        assert len(result) < len(text)


@pytest.mark.benchmark
class TestChunkingPerformance:
    """Benchmark chunking operations."""

    def test_hierarchical_chunking_speed(self, benchmark, test_config):
        """Benchmark hierarchical chunking."""
        from mcp_web.chunker import TextChunker

        test_config.chunker.strategy = "hierarchical"
        chunker = TextChunker(test_config.chunker)

        # Create realistic markdown document
        markdown_doc = "\n\n".join(
            [f"# Section {i}\n\nThis is section {i} with some content. " * 20 for i in range(10)]
        )

        result = benchmark(chunker.chunk_text, markdown_doc)

        assert len(result) > 0

    def test_semantic_chunking_speed(self, benchmark, test_config):
        """Benchmark semantic chunking."""
        from mcp_web.chunker import TextChunker

        test_config.chunker.strategy = "semantic"
        chunker = TextChunker(test_config.chunker)

        text = "This is a paragraph. " * 50 + "\n\n" + "Another paragraph here. " * 50

        result = benchmark(chunker.chunk_text, text)

        assert len(result) > 0

    def test_fixed_chunking_speed(self, benchmark, test_config):
        """Benchmark fixed-size chunking."""
        from mcp_web.chunker import TextChunker

        test_config.chunker.strategy = "fixed"
        chunker = TextChunker(test_config.chunker)

        text = "Word " * 5000  # ~5000 tokens

        result = benchmark(chunker.chunk_text, text)

        assert len(result) > 0


@pytest.mark.benchmark
class TestCachePerformance:
    """Benchmark cache operations."""

    @pytest.mark.asyncio
    async def test_cache_write_speed(self, benchmark, test_config):
        """Benchmark cache write performance."""
        from mcp_web.cache import CacheManager

        cache = CacheManager(
            cache_dir=test_config.cache.cache_dir,
            ttl=3600,
        )

        test_data = {"key": "value", "data": "x" * 1000}

        async def write_cache():
            for i in range(10):
                await cache.set(f"bench_key_{i}", test_data)

        # Benchmark async function
        result = benchmark.pedantic(
            lambda: asyncio.run(write_cache()),
            iterations=5,
            rounds=3,
        )

        # Cleanup
        for i in range(10):
            await cache.delete(f"bench_key_{i}")

    @pytest.mark.asyncio
    async def test_cache_read_speed(self, benchmark, test_config):
        """Benchmark cache read performance."""
        from mcp_web.cache import CacheManager

        cache = CacheManager(
            cache_dir=test_config.cache.cache_dir,
            ttl=3600,
        )

        # Prepare data
        test_data = {"key": "value", "data": "x" * 1000}
        await cache.set("bench_read_key", test_data)

        async def read_cache():
            for _ in range(10):
                await cache.get("bench_read_key")

        benchmark.pedantic(
            lambda: asyncio.run(read_cache()),
            iterations=5,
            rounds=3,
        )

        # Cleanup
        await cache.delete("bench_read_key")


@pytest.mark.benchmark
@pytest.mark.asyncio
class TestExtractionPerformance:
    """Benchmark content extraction."""

    async def test_extraction_speed(self, benchmark, test_config, sample_html):
        """Benchmark HTML extraction."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult

        extractor = ContentExtractor(test_config.extractor, cache=None)

        fetch_result = FetchResult(
            url="https://test.com",
            content=sample_html.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )

        async def extract():
            await extractor.extract(fetch_result, use_cache=False)

        # Run benchmark
        result = benchmark.pedantic(
            lambda: asyncio.run(extract()),
            iterations=10,
            rounds=3,
        )


@pytest.mark.benchmark
class TestURLValidationPerformance:
    """Benchmark URL validation."""

    def test_url_validation_speed(self, benchmark):
        """Benchmark URL validation."""
        from mcp_web.utils import validate_url

        test_urls = [
            "https://example.com",
            "http://example.org/path",
            "https://subdomain.example.com:8080/path?query=value",
            "invalid-url",
            "javascript:alert('xss')",
            "https://example.com/very/long/path/with/many/segments",
        ] * 10  # 60 URLs total

        def validate_all():
            for url in test_urls:
                validate_url(url)

        result = benchmark(validate_all)

    def test_url_normalization_speed(self, benchmark):
        """Benchmark URL normalization."""
        from mcp_web.utils import normalize_url

        test_urls = [
            "https://example.com?b=2&a=1#section",
            "https://example.com:443/path",
            "https://example.com/path/./subpath/../other",
        ] * 20

        def normalize_all():
            for url in test_urls:
                normalize_url(url)

        result = benchmark(normalize_all)


@pytest.mark.benchmark
class TestMemoryUsage:
    """Test memory usage of key operations."""

    def test_chunking_memory_usage(self, test_config):
        """Test memory usage during chunking."""
        import tracemalloc

        from mcp_web.chunker import TextChunker

        chunker = TextChunker(test_config.chunker)

        # Create large text
        large_text = "Word " * 50000  # ~50k tokens

        # Measure memory
        tracemalloc.start()

        chunks = chunker.chunk_text(large_text)

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Peak memory should be reasonable (< 100MB)
        assert peak < 100 * 1024 * 1024, f"Peak memory too high: {peak / 1024 / 1024:.2f} MB"

        print(f"\nChunking memory: {peak / 1024 / 1024:.2f} MB peak for 50k tokens")
        print(f"Chunks created: {len(chunks)}")

    @pytest.mark.asyncio
    async def test_cache_memory_usage(self, test_config):
        """Test memory usage of cache operations."""
        import tracemalloc

        from mcp_web.cache import CacheManager

        cache = CacheManager(
            cache_dir=test_config.cache.cache_dir,
            ttl=3600,
        )

        # Measure memory while writing many items
        tracemalloc.start()

        for i in range(100):
            await cache.set(f"mem_test_{i}", {"data": "x" * 1000})

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(f"\nCache memory: {peak / 1024 / 1024:.2f} MB peak for 100 items")

        # Cleanup
        await cache.clear()


@pytest.mark.benchmark
class TestConcurrency:
    """Test concurrent operation performance."""

    @pytest.mark.asyncio
    async def test_concurrent_chunking(self, test_config):
        """Test performance of concurrent chunking."""
        import time

        from mcp_web.chunker import TextChunker

        chunker = TextChunker(test_config.chunker)

        texts = ["Section content " * 500 + "\n\n" for _ in range(10)]

        # Sequential
        start = time.perf_counter()
        for text in texts:
            chunker.chunk_text(text)
        sequential_time = time.perf_counter() - start

        # Concurrent (using asyncio)
        start = time.perf_counter()

        async def chunk_async(text):
            return chunker.chunk_text(text)

        tasks = [chunk_async(text) for text in texts]
        await asyncio.gather(*tasks)

        concurrent_time = time.perf_counter() - start

        print("\nConcurrent chunking:")
        print(f"  Sequential: {sequential_time:.3f}s")
        print(f"  Concurrent: {concurrent_time:.3f}s")
        print(f"  Speedup: {sequential_time / concurrent_time:.2f}x")

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_concurrent_cache_operations(self, test_config):
        """Test concurrent cache read/write performance."""
        import time

        from mcp_web.cache import CacheManager

        cache = CacheManager(
            cache_dir=test_config.cache.cache_dir,
            ttl=3600,
        )

        # Prepare test data
        for i in range(50):
            await cache.set(f"concurrent_{i}", {"data": f"value_{i}"})

        # Concurrent reads
        start = time.perf_counter()

        tasks = [cache.get(f"concurrent_{i}") for i in range(50)]
        results = await asyncio.gather(*tasks)

        concurrent_time = time.perf_counter() - start

        assert all(r is not None for r in results)

        print(f"\nConcurrent cache reads: {concurrent_time:.3f}s for 50 operations")
        print(f"  Avg per operation: {concurrent_time / 50 * 1000:.2f}ms")

        # Cleanup
        await cache.clear()


@pytest.mark.benchmark
class TestScalability:
    """Test scalability with increasing data sizes."""

    def test_chunking_scalability(self, test_config):
        """Test chunking performance with increasing text size."""
        import time

        from mcp_web.chunker import TextChunker

        chunker = TextChunker(test_config.chunker)

        sizes = [100, 500, 1000, 5000, 10000]  # Token counts
        times = []

        for size in sizes:
            text = "Word " * size

            start = time.perf_counter()
            chunks = chunker.chunk_text(text)
            elapsed = time.perf_counter() - start

            times.append(elapsed)

            print(f"\n{size} tokens: {elapsed:.3f}s, {len(chunks)} chunks")

        # Check that time scales reasonably (should be roughly linear)
        # Time for 10000 tokens should be < 20x time for 500 tokens
        if times[1] > 0:
            ratio = times[4] / times[1]  # 10000 / 500 = 20x size
            assert ratio < 40, f"Scalability issue: {ratio:.1f}x slowdown for 20x data"
