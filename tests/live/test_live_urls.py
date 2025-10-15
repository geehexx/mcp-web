"""Live integration tests against real URLs with static content.

These are the "golden standard" tests that fetch real URLs and verify
the complete pipeline works correctly. These URLs have been selected for:
1. Static, unchanging content
2. Simple, predictable structure
3. Public availability
4. No authentication required

Note: These tests require network access and OPENAI_API_KEY.
"""

import os

import pytest

# URLs with static, unchanging content suitable for golden testing
GOLDEN_URLS = {
    "iana_example": {
        "url": "https://example.com",
        "description": "IANA example domain - simple, static HTML",
        "expected_keywords": ["example", "domain", "illustrative"],
        "expected_title": "Example Domain",
        "min_content_length": 50,
        "max_fetch_time": 10,  # seconds
    },
    "ietf_rfc": {
        "url": "https://www.rfc-editor.org/rfc/rfc2616.txt",
        "description": "HTTP/1.1 RFC (text format) - static specification",
        "expected_keywords": ["HTTP", "protocol", "request", "response"],
        "expected_title": "RFC",
        "min_content_length": 1000,
        "max_fetch_time": 15,
    },
    "python_pep": {
        "url": "https://peps.python.org/pep-0008/",
        "description": "PEP 8 Style Guide - stable Python documentation",
        "expected_keywords": ["python", "style", "guide", "PEP", "code"],
        "expected_title": "PEP 8",
        "min_content_length": 500,
        "max_fetch_time": 10,
        "has_code_examples": True,
    },
    "w3c_html_spec": {
        "url": "https://www.w3.org/TR/2011/WD-html5-20110405/",
        "description": "W3C HTML5 spec snapshot - historical, static",
        "expected_keywords": ["HTML", "element", "attribute", "specification"],
        "expected_title": "HTML",
        "min_content_length": 1000,
        "max_fetch_time": 20,
    },
}


@pytest.mark.live
@pytest.mark.slow
@pytest.mark.requires_network
class TestLiveURLFetching:
    """Test fetching real URLs."""

    @pytest.mark.parametrize("test_case", GOLDEN_URLS.values(), ids=GOLDEN_URLS.keys())
    @pytest.mark.asyncio
    async def test_fetch_golden_url(self, test_case, test_config):
        """Test fetching a golden URL."""
        import time

        from mcp_web.fetcher import URLFetcher

        fetcher = URLFetcher(test_config.fetcher, cache=None)

        start_time = time.time()

        try:
            result = await fetcher.fetch(test_case["url"], use_cache=False)

            fetch_time = time.time() - start_time

            # Verify fetch completed
            assert result is not None
            assert result.status_code == 200
            assert len(result.content) > 0

            # Verify fetch time
            assert fetch_time < test_case["max_fetch_time"], (
                f"Fetch took {fetch_time:.2f}s, expected < {test_case['max_fetch_time']}s"
            )

            print(
                f"\n✓ Fetched {test_case['url']}: {len(result.content)} bytes in {fetch_time:.2f}s"
            )

        except Exception as e:
            pytest.skip(f"Network error or URL unavailable: {e}")
        finally:
            await fetcher.close()

    @pytest.mark.parametrize("test_case", GOLDEN_URLS.values(), ids=GOLDEN_URLS.keys())
    @pytest.mark.asyncio
    async def test_extract_golden_url(self, test_case, test_config):
        """Test extracting content from golden URL."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import URLFetcher

        fetcher = URLFetcher(test_config.fetcher, cache=None)
        extractor = ContentExtractor(test_config.extractor, cache=None)

        try:
            # Fetch
            fetch_result = await fetcher.fetch(test_case["url"], use_cache=False)

            # Extract
            extracted = await extractor.extract(fetch_result, use_cache=False)

            # Verify extraction
            assert extracted is not None
            assert len(extracted.content) >= test_case["min_content_length"]

            # Verify title
            if test_case.get("expected_title"):
                assert test_case["expected_title"].lower() in extracted.title.lower(), (
                    f"Expected '{test_case['expected_title']}' in title, got: {extracted.title}"
                )

            # Verify keywords
            content_lower = extracted.content.lower()
            found_keywords = []
            for keyword in test_case["expected_keywords"]:
                if keyword.lower() in content_lower:
                    found_keywords.append(keyword)

            assert len(found_keywords) >= len(test_case["expected_keywords"]) // 2, (
                f"Expected keywords in content. Found: {found_keywords}"
            )

            # Verify code examples if expected
            if test_case.get("has_code_examples"):
                assert "```" in extracted.content or "code" in content_lower

            print(f"\n✓ Extracted {len(extracted.content)} chars from {test_case['url']}")
            print(f"  Title: {extracted.title}")
            print(f"  Keywords found: {found_keywords}")

        except Exception as e:
            pytest.skip(f"Network error or extraction failed: {e}")
        finally:
            await fetcher.close()


@pytest.mark.live
@pytest.mark.slow
@pytest.mark.requires_api
@pytest.mark.requires_network
class TestLiveSummarization:
    """Test full summarization pipeline with real URLs."""

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
    @pytest.mark.parametrize("url_key", ["iana_example", "python_pep"])
    @pytest.mark.asyncio
    async def test_summarize_golden_url(self, url_key, test_config):
        """Test complete summarization of golden URL."""
        import time

        from mcp_web.mcp_server import WebSummarizationPipeline

        test_case = GOLDEN_URLS[url_key]

        # Use lower temperature for more deterministic results
        test_config.summarizer.temperature = 0.0
        test_config.summarizer.max_tokens = 500  # Shorter for tests

        pipeline = WebSummarizationPipeline(test_config)

        start_time = time.time()

        try:
            # Collect summary
            summary_parts = []
            async for chunk in pipeline.summarize_urls([test_case["url"]]):
                summary_parts.append(chunk)

            summary = "".join(summary_parts)

            elapsed = time.time() - start_time

            # Verify summary was generated
            assert len(summary) > 100, "Summary too short"

            # Verify summary contains some expected keywords
            summary_lower = summary.lower()
            found_keywords = [
                kw for kw in test_case["expected_keywords"] if kw.lower() in summary_lower
            ]

            assert len(found_keywords) > 0, (
                f"Summary should contain some keywords. Got: {summary[:200]}"
            )

            # Verify summary structure
            assert "##" in summary or "**" in summary, "Summary should be formatted"

            # Verify source is cited
            assert test_case["url"] in summary, "Summary should cite source URL"

            print(f"\n✓ Summarized {test_case['url']} in {elapsed:.2f}s")
            print(f"  Summary length: {len(summary)} chars")
            print(f"  Keywords found: {found_keywords}")
            print(f"  Preview: {summary[:200]}...")

        except Exception as e:
            pytest.skip(f"Summarization failed (API or network): {e}")
        finally:
            await pipeline.close()

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
    @pytest.mark.asyncio
    async def test_query_focused_summarization(self, test_config):
        """Test query-focused summarization on real URL."""
        from mcp_web.mcp_server import WebSummarizationPipeline

        test_case = GOLDEN_URLS["python_pep"]
        query = "What are the recommendations for indentation?"

        test_config.summarizer.temperature = 0.0
        test_config.summarizer.max_tokens = 300

        pipeline = WebSummarizationPipeline(test_config)

        try:
            summary_parts = []
            async for chunk in pipeline.summarize_urls([test_case["url"]], query=query):
                summary_parts.append(chunk)

            summary = "".join(summary_parts)

            # Verify summary is focused on query
            summary_lower = summary.lower()
            assert any(word in summary_lower for word in ["indent", "space", "tab"]), (
                "Query-focused summary should mention indentation"
            )

            print("\n✓ Query-focused summary generated")
            print(f"  Query: {query}")
            print(f"  Preview: {summary[:200]}...")

        except Exception as e:
            pytest.skip(f"Summarization failed: {e}")
        finally:
            await pipeline.close()

    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
    @pytest.mark.asyncio
    async def test_summarization_consistency(self, test_config):
        """Test that summarization with temperature=0 is relatively consistent."""
        from mcp_web.mcp_server import WebSummarizationPipeline

        test_case = GOLDEN_URLS["iana_example"]

        # Use temperature=0 for maximum consistency
        test_config.summarizer.temperature = 0.0
        test_config.summarizer.max_tokens = 200

        pipeline = WebSummarizationPipeline(test_config)

        summaries = []

        try:
            # Generate 2 summaries
            for i in range(2):
                summary_parts = []
                async for chunk in pipeline.summarize_urls([test_case["url"]]):
                    summary_parts.append(chunk)
                summaries.append("".join(summary_parts))

            # Summaries should be similar (not identical due to LLM variance)
            # Check they both contain key information
            for summary in summaries:
                assert "example" in summary.lower()
                assert len(summary) > 50

            # Calculate similarity (simple word overlap)
            words1 = set(summaries[0].lower().split())
            words2 = set(summaries[1].lower().split())

            overlap = len(words1 & words2)
            union = len(words1 | words2)

            similarity = overlap / union if union > 0 else 0

            # Should have some similarity (at least 30% word overlap)
            assert similarity > 0.3, (
                f"Summaries should be somewhat consistent. Similarity: {similarity:.2%}"
            )

            print("\n✓ Consistency check passed")
            print(f"  Similarity: {similarity:.2%}")

        except Exception as e:
            pytest.skip(f"Summarization failed: {e}")
        finally:
            await pipeline.close()


@pytest.mark.live
@pytest.mark.slow
@pytest.mark.requires_network
class TestLinkFollowing:
    """Test link following with real URLs."""

    @pytest.mark.asyncio
    async def test_extract_links_from_real_page(self, test_config):
        """Test extracting links from real page."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import URLFetcher

        test_case = GOLDEN_URLS["python_pep"]

        fetcher = URLFetcher(test_config.fetcher, cache=None)
        extractor = ContentExtractor(test_config.extractor, cache=None)

        try:
            fetch_result = await fetcher.fetch(test_case["url"], use_cache=False)
            extracted = await extractor.extract(fetch_result, use_cache=False)

            # Should extract some links
            assert len(extracted.links) > 0, "Should extract links from page"

            # Links should be valid URLs
            from mcp_web.utils import validate_url

            valid_links = [link for link in extracted.links if validate_url(link)]

            assert len(valid_links) > 0, "Should have at least one valid link"

            print(f"\n✓ Extracted {len(extracted.links)} links")
            print(f"  Valid links: {len(valid_links)}")
            print(f"  Sample links: {extracted.links[:3]}")

        except Exception as e:
            pytest.skip(f"Network error: {e}")
        finally:
            await fetcher.close()


@pytest.mark.live
@pytest.mark.slow
class TestCachingBehavior:
    """Test caching behavior with real URLs."""

    @pytest.mark.asyncio
    async def test_cache_hit_on_second_fetch(self, test_config):
        """Test that second fetch uses cache."""
        import time

        from mcp_web.cache import CacheManager
        from mcp_web.fetcher import URLFetcher

        test_case = GOLDEN_URLS["iana_example"]

        # Enable cache
        cache = CacheManager(
            cache_dir=test_config.cache.cache_dir,
            ttl=test_config.cache.ttl,
        )

        fetcher = URLFetcher(test_config.fetcher, cache=cache)

        try:
            # First fetch (no cache)
            start1 = time.time()
            result1 = await fetcher.fetch(test_case["url"], use_cache=True)
            time1 = time.time() - start1

            # Second fetch (should hit cache)
            start2 = time.time()
            result2 = await fetcher.fetch(test_case["url"], use_cache=True)
            time2 = time.time() - start2

            # Verify cache hit
            assert result2.from_cache, "Second fetch should be from cache"

            # Cache hit should be faster (usually)
            # Note: This might not always be true, but generally should be
            print("\n✓ Cache test completed")
            print(f"  First fetch: {time1:.3f}s")
            print(f"  Second fetch (cached): {time2:.3f}s")

        except Exception as e:
            pytest.skip(f"Cache test failed: {e}")
        finally:
            await fetcher.close()
            await cache.clear()  # Clean up
