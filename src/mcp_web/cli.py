"""Command-line interface for testing mcp-web functionality.

This module provides CLI commands for manual testing and verification
of URL summarization with various configurations.

Usage:
    python -m mcp_web.cli test-summarize <url> [options]
    task test:manual URL=<url> QUERY=<query>
"""

import asyncio
import sys
import time

import click
import structlog

from mcp_web.cache import CacheManager
from mcp_web.chunker import TextChunker
from mcp_web.config import Config
from mcp_web.extractor import ContentExtractor
from mcp_web.fetcher import URLFetcher
from mcp_web.summarizer import Summarizer

logger = structlog.get_logger()


@click.group()
def cli() -> None:
    """MCP-Web CLI for testing and verification."""
    pass


@cli.command("test-summarize")
@click.argument("urls", nargs=-1, required=True)
@click.option(
    "--query",
    "-q",
    default=None,
    help="Query to focus the summary on",
)
@click.option(
    "--provider",
    default="openai",
    type=click.Choice(["openai", "ollama", "lmstudio", "localai"]),
    help="LLM provider to use",
)
@click.option(
    "--model",
    default=None,
    help="LLM model to use (default: provider-specific)",
)
@click.option(
    "--output",
    "-o",
    default=None,
    type=click.Path(),
    help="Save output to file",
)
@click.option(
    "--show-metrics/--no-metrics",
    default=True,
    help="Show performance metrics",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Verbose output (show chunks, extraction details)",
)
def test_summarize(
    urls: tuple[str, ...],
    query: str | None,
    provider: str,
    model: str | None,
    output: str | None,
    show_metrics: bool,
    verbose: bool,
) -> None:
    """Test URL summarization with optional query focus.

    Examples:
        # Simple summarization
        mcp-web test-summarize https://example.com

        # Query-focused summarization
        mcp-web test-summarize https://example.com --query "security best practices"

        # Use local LLM
        mcp-web test-summarize https://example.com --provider ollama --model llama3.2

        # Multiple URLs
        mcp-web test-summarize https://url1.com https://url2.com --query "comparison"

        # Save output
        mcp-web test-summarize https://example.com -o summary.md
    """
    asyncio.run(
        _test_summarize_async(list(urls), query, provider, model, output, show_metrics, verbose)
    )


async def _test_summarize_async(
    urls: list[str],
    query: str | None,
    provider: str,
    model: str | None,
    output: str | None,
    show_metrics: bool,
    verbose: bool,
) -> None:
    """Async implementation of test-summarize."""
    click.echo(click.style("=== MCP-Web Test Summarizer ===\n", fg="cyan", bold=True))

    # Configuration
    config = Config()
    config.summarizer.provider = provider
    if model:
        config.summarizer.model = model
    
    # Initialize cache manager
    cache_manager = CacheManager(
        cache_dir=config.cache.cache_dir,
        ttl=config.cache.ttl,
        max_size=config.cache.max_size,
    ) if config.cache.enabled else None

    if verbose:
        click.echo(f"Provider: {config.summarizer.provider}")
        click.echo(f"Model: {config.summarizer.model}")
        click.echo(f"API Base: {config.summarizer.get_api_base()}")
        if query:
            click.echo(f"Query: {query}")
        click.echo()

    # Initialize components
    fetcher = URLFetcher(config.fetcher, cache_manager)
    extractor = ContentExtractor(config.extractor)
    chunker = TextChunker(config.chunker)
    summarizer = Summarizer(config.summarizer)

    overall_start = time.perf_counter()
    metrics = {
        "fetch_time": 0.0,
        "extract_time": 0.0,
        "chunk_time": 0.0,
        "summarize_time": 0.0,
        "total_tokens": 0,
        "fetch_method": [],
        "chunk_count": 0,
    }

    try:
        # Process each URL
        all_summaries = []

        for url in urls:
            click.echo(click.style(f"Processing: {url}", fg="yellow"))

            # Fetch
            fetch_start = time.perf_counter()
            fetch_result = await fetcher.fetch(url)
            fetch_time = time.perf_counter() - fetch_start
            metrics["fetch_time"] += fetch_time
            metrics["fetch_method"].append(fetch_result.fetch_method)

            if verbose:
                click.echo(f"  Fetch: {fetch_result.fetch_method} ({fetch_time:.2f}s)")
                click.echo(f"  Status: {fetch_result.status_code}")
                click.echo(f"  Content-Type: {fetch_result.content_type}")
                click.echo(f"  Size: {len(fetch_result.content):,} bytes")

            # Extract
            extract_start = time.perf_counter()
            extraction = await extractor.extract(fetch_result.content.decode("utf-8"))
            extract_time = time.perf_counter() - extract_start
            metrics["extract_time"] += extract_time

            if verbose:
                click.echo(f"  Extract: {len(extraction.text):,} chars ({extract_time:.2f}s)")
                click.echo(f"  Title: {extraction.title}")
                if extraction.metadata:
                    click.echo(f"  Metadata: {len(extraction.metadata)} fields")

            # Chunk
            chunk_start = time.perf_counter()
            chunks = chunker.chunk_text(extraction.text)
            chunk_time = time.perf_counter() - chunk_start
            metrics["chunk_time"] += chunk_time
            metrics["chunk_count"] += len(chunks)

            if verbose:
                click.echo(f"  Chunk: {len(chunks)} chunks ({chunk_time:.2f}s)")
                for i, chunk in enumerate(chunks[:3]):  # Show first 3
                    click.echo(f"    Chunk {i + 1}: {chunk.token_count} tokens")
                if len(chunks) > 3:
                    click.echo(f"    ... and {len(chunks) - 3} more")

            # Summarize
            click.echo(click.style("  Summarizing...", fg="cyan"))
            summarize_start = time.perf_counter()

            summary_parts = []
            async for chunk in summarizer.summarize(
                chunks=chunks,
                query=query,
                sources=[url],
            ):
                if not verbose:
                    # Show streaming progress
                    click.echo(chunk, nl=False)
                summary_parts.append(chunk)

            summary = "".join(summary_parts)
            summarize_time = time.perf_counter() - summarize_start
            metrics["summarize_time"] += summarize_time

            if verbose:
                click.echo(f"\n  Summarize: {summarize_time:.2f}s")
                click.echo(f"  Summary length: {len(summary):,} chars")
                click.echo("\n" + "=" * 80)
                click.echo(summary)
                click.echo("=" * 80 + "\n")

            all_summaries.append(
                {
                    "url": url,
                    "summary": summary,
                }
            )

        overall_time = time.perf_counter() - overall_start

        # Display metrics
        if show_metrics:
            click.echo("\n" + click.style("=== Metrics ===", fg="green", bold=True))
            click.echo(f"URLs processed: {len(urls)}")
            click.echo(f"Total time: {overall_time:.2f}s")
            click.echo(f"  Fetch: {metrics['fetch_time']:.2f}s")
            click.echo(f"  Extract: {metrics['extract_time']:.2f}s")
            click.echo(f"  Chunk: {metrics['chunk_time']:.2f}s")
            click.echo(f"  Summarize: {metrics['summarize_time']:.2f}s")
            click.echo(f"Chunks created: {metrics['chunk_count']}")
            click.echo(f"Fetch methods: {', '.join(set(metrics['fetch_method']))}")

        # Save output
        if output:
            with open(output, "w") as f:
                for item in all_summaries:
                    f.write(f"# {item['url']}\n\n")
                    f.write(item["summary"])
                    f.write("\n\n---\n\n")
            click.echo(click.style(f"\n✓ Output saved to {output}", fg="green"))

    except KeyboardInterrupt:
        click.echo(click.style("\n\n⚠ Interrupted by user", fg="yellow"))
        sys.exit(130)
    except Exception as e:
        click.echo(click.style(f"\n✗ Error: {e}", fg="red", bold=True))
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)
    finally:
        await fetcher.close()
        await summarizer.close()


@cli.command("test-robots")
@click.argument("url")
@click.option(
    "--ignore/--respect",
    default=False,
    help="Ignore or respect robots.txt",
)
def test_robots(url: str, ignore: bool) -> None:
    """Test robots.txt handling for a URL.

    Examples:
        mcp-web test-robots https://example.com
        mcp-web test-robots https://example.com --ignore
    """
    asyncio.run(_test_robots_async(url, ignore))


async def _test_robots_async(url: str, ignore: bool) -> None:
    """Async implementation of test-robots."""
    from urllib.parse import urlparse
    from urllib.robotparser import RobotFileParser

    click.echo(click.style("=== Robots.txt Test ===\n", fg="cyan", bold=True))
    click.echo(f"URL: {url}")
    click.echo(f"Mode: {'IGNORE' if ignore else 'RESPECT'} robots.txt\n")

    # Parse robots.txt
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    click.echo(f"Fetching: {robots_url}")

    config = Config()
    cache_manager = CacheManager(
        cache_dir=config.cache.cache_dir,
        ttl=config.cache.ttl,
        max_size=config.cache.max_size,
    ) if config.cache.enabled else None
    fetcher = URLFetcher(config.fetcher, cache_manager)

    try:
        robots_result = await fetcher.fetch(robots_url)
        click.echo(click.style("✓ robots.txt found", fg="green"))

        # Parse robots.txt
        rp = RobotFileParser()
        rp.parse(robots_result.content.decode("utf-8").splitlines())

        # Check if allowed
        user_agent = config.fetcher.user_agent
        can_fetch = rp.can_fetch(user_agent, url)

        click.echo(f"\nUser-Agent: {user_agent}")
        click.echo(f"Can fetch: {can_fetch}")

        if not can_fetch:
            click.echo(click.style("⚠ URL is disallowed by robots.txt", fg="yellow"))

        # Show crawl delay
        crawl_delay = rp.crawl_delay(user_agent)
        if crawl_delay:
            click.echo(f"Crawl-Delay: {crawl_delay}s")

        # Show relevant rules
        click.echo("\nRelevant rules:")
        for line in robots_result.content.decode("utf-8").splitlines()[:20]:
            if line.strip():
                click.echo(f"  {line}")

        # Attempt fetch if ignoring or allowed
        if ignore or can_fetch:
            click.echo(
                click.style(
                    f"\n{'Ignoring robots.txt and fetching...' if not can_fetch else 'Fetching URL...'}",
                    fg="cyan",
                )
            )
            result = await fetcher.fetch(url)
            click.echo(click.style(f"✓ Fetched successfully ({result.fetch_method})", fg="green"))
            click.echo(f"  Status: {result.status_code}")
            click.echo(f"  Size: {len(result.content):,} bytes")
        else:
            click.echo(click.style("\n✗ Would not fetch (blocked by robots.txt)", fg="red"))

    except Exception as e:
        if "404" in str(e):
            click.echo(click.style("✓ No robots.txt (fetching allowed)", fg="green"))
        else:
            click.echo(click.style(f"✗ Error: {e}", fg="red"))
    finally:
        await fetcher.close()


if __name__ == "__main__":
    cli()
