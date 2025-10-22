#!/usr/bin/env python3
"""Comprehensive pipeline benchmarking script.

Profiles the entire summarization pipeline and generates detailed reports.

Usage:
    python scripts/benchmark_pipeline.py --url https://example.com
    python scripts/benchmark_pipeline.py --url https://example.com --profile --export /tmp/mcp-web-benchmark.json
    python scripts/benchmark_pipeline.py --load-test --concurrent 10 --requests 100
"""

import argparse
import asyncio
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mcp_web.cache import CacheManager
from mcp_web.chunker import TextChunker
from mcp_web.config import Config, load_config
from mcp_web.extractor import ContentExtractor
from mcp_web.fetcher import URLFetcher
from mcp_web.profiler import (
    ComponentTimer,
    PerformanceCollector,
    cprofile_context,
    format_duration,
)
from mcp_web.summarizer import Summarizer
from mcp_web.utils import TokenCounter


class PipelineBenchmark:
    """Benchmark the full summarization pipeline."""

    def __init__(self, config: Config):
        """Initialize benchmark.

        Args:
            config: Application configuration
        """
        self.config = config
        self.timer = ComponentTimer()
        self.token_counter = TokenCounter()

        # Initialize components
        self.cache = (
            CacheManager(
                cache_dir=config.cache.cache_dir,
                ttl=config.cache.ttl,
            )
            if config.cache.enabled
            else None
        )
        self.fetcher = URLFetcher(config.fetcher, cache=self.cache)
        self.extractor = ContentExtractor(config.extractor, cache=self.cache)
        self.chunker = TextChunker(config.chunker)
        self.summarizer = Summarizer(config.summarizer)

    async def benchmark_full_pipeline(
        self,
        url: str,
        query: str | None = None,
        use_cache: bool = True,
    ) -> dict[str, Any]:
        """Benchmark the full pipeline.

        Args:
            url: URL to summarize
            query: Optional query
            use_cache: Whether to use cache

        Returns:
            Benchmark results
        """
        print(f"\n{'=' * 80}")
        print(f"Benchmarking: {url}")
        print(f"Query: {query or 'None'}")
        print(f"Cache: {'Enabled' if use_cache else 'Disabled'}")
        print(f"{'=' * 80}\n")

        overall_start = time.perf_counter()

        # Step 1: Fetch
        with self.timer.time("fetch"):
            fetch_result = await self.fetcher.fetch(url, use_cache=use_cache)

        print(
            f"✓ Fetch: {format_duration(self.timer.timings['fetch'][-1])} "
            f"({fetch_result.content_type})"
        )

        # Step 2: Extract
        with self.timer.time("extract"):
            extracted = await self.extractor.extract(fetch_result, use_cache=use_cache)

        content_tokens = self.token_counter.count_tokens(extracted.content)
        print(
            f"✓ Extract: {format_duration(self.timer.timings['extract'][-1])} "
            f"({content_tokens:,} tokens)"
        )

        # Step 3: Chunk
        with self.timer.time("chunk"):
            chunks = self.chunker.chunk_text(extracted.content)

        chunk_tokens = sum(c.tokens for c in chunks)
        print(
            f"✓ Chunk: {format_duration(self.timer.timings['chunk'][-1])} "
            f"({len(chunks)} chunks, {chunk_tokens:,} tokens)"
        )

        # Step 4: Summarize
        summary_parts = []
        summarize_start = time.perf_counter()

        with self.timer.time("summarize"):
            async for chunk in self.summarizer.summarize_chunks(chunks, query=query, sources=[url]):
                summary_parts.append(chunk)

        summary = "".join(summary_parts)
        summarize_duration = (time.perf_counter() - summarize_start) * 1000

        summary_tokens = self.token_counter.count_tokens(summary)
        print(f"✓ Summarize: {format_duration(summarize_duration)} ({summary_tokens:,} tokens)")

        # Overall timing
        overall_duration = (time.perf_counter() - overall_start) * 1000

        print(f"\n{'=' * 80}")
        print(f"Total: {format_duration(overall_duration)}")
        print(f"{'=' * 80}\n")

        # Calculate percentages
        fetch_pct = (self.timer.timings["fetch"][-1] / overall_duration) * 100
        extract_pct = (self.timer.timings["extract"][-1] / overall_duration) * 100
        chunk_pct = (self.timer.timings["chunk"][-1] / overall_duration) * 100
        summarize_pct = (summarize_duration / overall_duration) * 100

        # Build results
        results = {
            "url": url,
            "query": query,
            "overall_duration_ms": overall_duration,
            "components": {
                "fetch": {
                    "duration_ms": self.timer.timings["fetch"][-1],
                    "percentage": fetch_pct,
                    "method": fetch_result.fetch_method,
                },
                "extract": {
                    "duration_ms": self.timer.timings["extract"][-1],
                    "percentage": extract_pct,
                    "tokens": content_tokens,
                },
                "chunk": {
                    "duration_ms": self.timer.timings["chunk"][-1],
                    "percentage": chunk_pct,
                    "num_chunks": len(chunks),
                    "tokens": chunk_tokens,
                },
                "summarize": {
                    "duration_ms": summarize_duration,
                    "percentage": summarize_pct,
                    "tokens": summary_tokens,
                },
            },
            "summary": summary[:200] + "..." if len(summary) > 200 else summary,
        }

        # Print breakdown
        print("Component Breakdown:")
        print(
            f"  Fetch:      {format_duration(results['components']['fetch']['duration_ms']):>8} ({fetch_pct:>5.1f}%)"
        )
        print(
            f"  Extract:    {format_duration(results['components']['extract']['duration_ms']):>8} ({extract_pct:>5.1f}%)"
        )
        print(
            f"  Chunk:      {format_duration(results['components']['chunk']['duration_ms']):>8} ({chunk_pct:>5.1f}%)"
        )
        print(
            f"  Summarize:  {format_duration(results['components']['summarize']['duration_ms']):>8} ({summarize_pct:>5.1f}%)"
        )

        return results

    async def load_test(
        self,
        url: str,
        num_requests: int,
        concurrent: int,
    ) -> dict[str, Any]:
        """Load test the pipeline.

        Args:
            url: URL to test
            num_requests: Total number of requests
            concurrent: Concurrent requests

        Returns:
            Load test results
        """
        print(f"\n{'=' * 80}")
        print(f"Load Test: {num_requests} requests, {concurrent} concurrent")
        print(f"{'=' * 80}\n")

        semaphore = asyncio.Semaphore(concurrent)
        durations = []

        async def single_request(request_num: int) -> float:
            """Single request with semaphore."""
            async with semaphore:
                time.perf_counter()
                try:
                    result = await self.benchmark_full_pipeline(url, use_cache=False)
                    duration = result["overall_duration_ms"]
                    durations.append(duration)
                    print(f"Request {request_num + 1}/{num_requests}: {format_duration(duration)}")
                    return duration
                except Exception as e:
                    print(f"Request {request_num + 1} failed: {e}")
                    return 0.0

        # Run all requests
        overall_start = time.perf_counter()
        tasks = [single_request(i) for i in range(num_requests)]
        await asyncio.gather(*tasks)
        overall_duration = time.perf_counter() - overall_start

        # Calculate stats
        successful = [d for d in durations if d > 0]
        failed = num_requests - len(successful)

        if successful:
            results = {
                "total_requests": num_requests,
                "successful": len(successful),
                "failed": failed,
                "concurrent": concurrent,
                "total_time_s": overall_duration,
                "throughput_rps": len(successful) / overall_duration,
                "latency": {
                    "min_ms": min(successful),
                    "max_ms": max(successful),
                    "mean_ms": statistics.mean(successful),
                    "median_ms": statistics.median(successful),
                    "p95_ms": statistics.quantiles(successful, n=20)[18],
                    "p99_ms": statistics.quantiles(successful, n=100)[98],
                },
            }
        else:
            results = {
                "total_requests": num_requests,
                "successful": 0,
                "failed": failed,
                "error": "All requests failed",
            }

        # Print results
        print(f"\n{'=' * 80}")
        print("Load Test Results:")
        print(f"  Total Requests: {results['total_requests']}")
        print(f"  Successful:     {results.get('successful', 0)}")
        print(f"  Failed:         {results.get('failed', 0)}")
        if "throughput_rps" in results:
            print(f"  Throughput:     {results['throughput_rps']:.2f} req/s")
            print("\nLatency:")
            print(f"  Min:    {format_duration(results['latency']['min_ms'])}")
            print(f"  Mean:   {format_duration(results['latency']['mean_ms'])}")
            print(f"  Median: {format_duration(results['latency']['median_ms'])}")
            print(f"  P95:    {format_duration(results['latency']['p95_ms'])}")
            print(f"  P99:    {format_duration(results['latency']['p99_ms'])}")
            print(f"  Max:    {format_duration(results['latency']['max_ms'])}")
        print(f"{'=' * 80}\n")

        return results

    async def close(self) -> None:
        """Cleanup resources."""
        await self.fetcher.close()
        await self.summarizer.close()


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Benchmark mcp-web pipeline")
    parser.add_argument("--url", default="https://python.org", help="URL to benchmark")
    parser.add_argument("--query", help="Optional query for focused summary")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache for benchmark")
    parser.add_argument("--profile", action="store_true", help="Enable cProfile profiling")
    parser.add_argument("--export", help="Export results to JSON file")
    parser.add_argument("--load-test", action="store_true", help="Run load test instead")
    parser.add_argument(
        "--concurrent", type=int, default=5, help="Concurrent requests for load test"
    )
    parser.add_argument("--requests", type=int, default=10, help="Total requests for load test")

    args = parser.parse_args()

    # Load config
    config = load_config()

    # Initialize benchmark
    benchmark = PipelineBenchmark(config)

    try:
        if args.load_test:
            # Run load test
            if args.profile:
                with cprofile_context("load_test.stats"):
                    results = await benchmark.load_test(args.url, args.requests, args.concurrent)
            else:
                results = await benchmark.load_test(args.url, args.requests, args.concurrent)
        else:
            # Run single benchmark
            if args.profile:
                with cprofile_context("benchmark.stats"):
                    results = await benchmark.benchmark_full_pipeline(
                        args.url, args.query, use_cache=not args.no_cache
                    )
            else:
                results = await benchmark.benchmark_full_pipeline(
                    args.url, args.query, use_cache=not args.no_cache
                )

        # Export if requested
        if args.export:
            export_path = Path(args.export)
            export_path.parent.mkdir(parents=True, exist_ok=True)
            with open(export_path, "w") as f:
                json.dump(results, f, indent=2)
            print(f"\n✓ Results exported to: {export_path}")

        # Export performance collector data
        if not args.load_test:
            collector = PerformanceCollector.get_instance()
            if collector.results:
                perf_path = Path(".benchmarks") / "performance_data.json"
                collector.export_json(perf_path)
                print(f"✓ Performance data exported to: {perf_path}")

    finally:
        await benchmark.close()


if __name__ == "__main__":
    asyncio.run(main())
