"""Basic usage examples for mcp-web.

Demonstrates:
1. Simple URL summarization
2. Query-focused summarization
3. Multiple URL summarization
4. Link following
5. Cache operations
"""

import asyncio
import os

from mcp_web import load_config
from mcp_web.mcp_server import WebSummarizationPipeline


async def example_1_simple_summary():
    """Example 1: Simple URL summarization."""
    print("=" * 80)
    print("Example 1: Simple URL Summarization")
    print("=" * 80)

    config = load_config()
    pipeline = WebSummarizationPipeline(config)

    print("\nSummarizing: https://example.com\n")

    async for chunk in pipeline.summarize_urls(
        urls=["https://example.com"],
    ):
        print(chunk, end="", flush=True)

    print("\n")
    await pipeline.close()


async def example_2_query_focused():
    """Example 2: Query-focused summarization."""
    print("=" * 80)
    print("Example 2: Query-Focused Summarization")
    print("=" * 80)

    config = load_config()
    pipeline = WebSummarizationPipeline(config)

    url = "https://docs.python.org/3/library/asyncio-task.html"
    query = "How do I create and run asyncio tasks?"

    print(f"\nSummarizing: {url}")
    print(f"Query: {query}\n")

    async for chunk in pipeline.summarize_urls(
        urls=[url],
        query=query,
    ):
        print(chunk, end="", flush=True)

    print("\n")
    await pipeline.close()


async def example_3_multiple_urls():
    """Example 3: Multiple URL summarization."""
    print("=" * 80)
    print("Example 3: Multiple URL Summarization")
    print("=" * 80)

    config = load_config()
    pipeline = WebSummarizationPipeline(config)

    urls = [
        "https://example.com",
        "https://example.org",
    ]

    print(f"\nSummarizing {len(urls)} URLs:\n")
    for url in urls:
        print(f"  - {url}")
    print()

    async for chunk in pipeline.summarize_urls(urls=urls):
        print(chunk, end="", flush=True)

    print("\n")
    await pipeline.close()


async def example_4_link_following():
    """Example 4: Summarization with link following."""
    print("=" * 80)
    print("Example 4: Summarization with Link Following")
    print("=" * 80)

    config = load_config()
    pipeline = WebSummarizationPipeline(config)

    url = "https://example.com"

    print(f"\nSummarizing: {url}")
    print("Following relevant links (depth=1)\n")

    async for chunk in pipeline.summarize_urls(
        urls=[url],
        follow_links=True,
        max_depth=1,
    ):
        print(chunk, end="", flush=True)

    print("\n")
    await pipeline.close()


async def example_5_cache_operations():
    """Example 5: Cache operations."""
    print("=" * 80)
    print("Example 5: Cache Operations")
    print("=" * 80)

    config = load_config()
    pipeline = WebSummarizationPipeline(config)

    # Check cache stats
    if pipeline.cache:
        print("\nCache statistics:")
        stats = pipeline.cache.get_stats()
        print(f"  Size: {stats.get('size_mb', 0):.2f} MB")
        print(f"  Usage: {stats.get('usage_percent', 0):.1f}%")
        print(f"  Entries: {stats.get('entry_count', 0)}")

        # Prune cache
        print("\nPruning expired entries...")
        pruned = await pipeline.cache.prune()
        print(f"  Pruned {pruned} entries")

        # Clear cache (optional, commented out)
        # print("\nClearing entire cache...")
        # await pipeline.cache.clear()
        # print("  Cache cleared")
    else:
        print("\nCache is not enabled")

    await pipeline.close()


async def main():
    """Run all examples."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set")
        print("Export your API key: export OPENAI_API_KEY='sk-...'")
        return

    # Run examples (uncomment the ones you want to run)
    
    # Simple examples (fast)
    await example_1_simple_summary()
    await example_5_cache_operations()

    # More complex examples (slower, require API calls)
    # await example_2_query_focused()
    # await example_3_multiple_urls()
    # await example_4_link_following()


if __name__ == "__main__":
    asyncio.run(main())
