"""Golden tests for content extraction with static HTML.

These tests use predetermined HTML samples with expected extraction results
to ensure consistent extraction behavior across changes.
"""

import pytest

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


class TestGoldenExtraction:
    """Test extraction against golden HTML samples."""

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_simple_article_extraction(self, test_config):
        """Test extraction of simple article matches expectations."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/simple-article",
            content=SIMPLE_ARTICLE_HTML.encode("utf-8"),
            content_type="text/html; charset=utf-8",
            headers={"content-type": "text/html"},
            status_code=200,
            fetch_method="test",
        )
        
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        # Verify title
        assert SIMPLE_ARTICLE_EXPECTED["title"] in extracted.title
        
        # Verify content contains expected keywords
        content_lower = extracted.content.lower()
        for keyword in SIMPLE_ARTICLE_EXPECTED["content_keywords"]:
            assert keyword.lower() in content_lower, f"Missing keyword: {keyword}"
        
        # Verify sections are present
        for section in SIMPLE_ARTICLE_EXPECTED["sections"]:
            assert section in extracted.content, f"Missing section: {section}"
        
        # Verify code blocks
        code_block_count = extracted.content.count("```")
        assert code_block_count >= SIMPLE_ARTICLE_EXPECTED["code_blocks"] * 2  # Opening and closing
        
        # Verify links
        assert len(extracted.links) >= len(SIMPLE_ARTICLE_EXPECTED["links"])
        for expected_link in SIMPLE_ARTICLE_EXPECTED["links"]:
            assert expected_link in extracted.links
        
        # Verify content length
        assert len(extracted.content) >= SIMPLE_ARTICLE_EXPECTED["min_content_length"]

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_technical_doc_extraction(self, test_config):
        """Test extraction of technical documentation."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/api-docs",
            content=TECHNICAL_DOC_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        # Verify title
        assert TECHNICAL_DOC_EXPECTED["title"] in extracted.title
        
        # Verify keywords
        content_lower = extracted.content.lower()
        for keyword in TECHNICAL_DOC_EXPECTED["content_keywords"]:
            assert keyword.lower() in content_lower, f"Missing keyword: {keyword}"
        
        # Verify sections
        for section in TECHNICAL_DOC_EXPECTED["sections"]:
            assert section in extracted.content, f"Missing section: {section}"
        
        # Verify code blocks (technical docs have many)
        code_block_count = extracted.content.count("```")
        assert code_block_count >= TECHNICAL_DOC_EXPECTED["code_blocks_min"] * 2
        
        # Verify JSON examples if expected
        if TECHNICAL_DOC_EXPECTED["has_json_examples"]:
            assert "json" in extracted.content.lower()
            assert "{" in extracted.content
        
        # Verify content length
        assert len(extracted.content) >= TECHNICAL_DOC_EXPECTED["min_content_length"]

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_news_article_extraction(self, test_config):
        """Test extraction of news article with quotes."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/news",
            content=NEWS_ARTICLE_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        # Verify title
        assert NEWS_ARTICLE_EXPECTED["title"] in extracted.title
        
        # Verify metadata
        if extracted.metadata.get("author"):
            assert NEWS_ARTICLE_EXPECTED["author"] in extracted.metadata.get("author", "")
        
        # Verify keywords
        content_lower = extracted.content.lower()
        for keyword in NEWS_ARTICLE_EXPECTED["content_keywords"]:
            assert keyword.lower() in content_lower, f"Missing keyword: {keyword}"
        
        # Verify quotes are preserved
        if NEWS_ARTICLE_EXPECTED["has_quotes"]:
            # Should contain quote markers or blockquote content
            assert '"' in extracted.content or '>' in extracted.content
        
        # Verify sections
        for section in NEWS_ARTICLE_EXPECTED["sections"]:
            assert section in extracted.content, f"Missing section: {section}"
        
        # Verify links
        for expected_link in NEWS_ARTICLE_EXPECTED["links"]:
            assert expected_link in extracted.links
        
        # Verify content length
        assert len(extracted.content) >= NEWS_ARTICLE_EXPECTED["min_content_length"]

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_blog_post_extraction(self, test_config):
        """Test extraction of blog post with multiple links."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/blog",
            content=BLOG_POST_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        # Verify title
        assert BLOG_POST_EXPECTED["title"] in extracted.title
        
        # Verify keywords
        content_lower = extracted.content.lower()
        for keyword in BLOG_POST_EXPECTED["content_keywords"]:
            assert keyword.lower() in content_lower, f"Missing keyword: {keyword}"
        
        # Verify all numbered sections
        section_count = sum(1 for i in range(1, 11) if f"{i}." in extracted.content)
        assert section_count >= BLOG_POST_EXPECTED["sections"]
        
        # Verify links
        assert len(extracted.links) >= BLOG_POST_EXPECTED["links_min"]
        
        # Verify content length
        assert len(extracted.content) >= BLOG_POST_EXPECTED["min_content_length"]

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_extraction_consistency(self, test_config):
        """Test that extraction is consistent across multiple runs."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/consistent",
            content=SIMPLE_ARTICLE_HTML.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        # Extract multiple times
        results = []
        for _ in range(3):
            extracted = await extractor.extract(fetch_result, use_cache=False)
            results.append({
                "title": extracted.title,
                "content": extracted.content,
                "links": sorted(extracted.links),
            })
        
        # All results should be identical
        for i in range(1, len(results)):
            assert results[i]["title"] == results[0]["title"]
            assert results[i]["content"] == results[0]["content"]
            assert results[i]["links"] == results[0]["links"]

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_code_block_preservation(self, test_config):
        """Test that code blocks are preserved correctly."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        html_with_code = """
        <html>
        <body>
            <article>
                <h1>Code Example</h1>
                <pre><code class="language-python">
def hello_world():
    print("Hello, World!")
    return True
                </code></pre>
            </article>
        </body>
        </html>
        """
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/code",
            content=html_with_code.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        # Code should be in extracted content
        assert "def hello_world" in extracted.content
        assert "print" in extracted.content
        
        # Code blocks should be marked
        assert "```" in extracted.content or "def hello_world" in extracted.content

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_metadata_extraction(self, test_config):
        """Test metadata extraction from HTML."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        html_with_metadata = """
        <html>
        <head>
            <title>Test Article</title>
            <meta name="author" content="John Doe">
            <meta name="description" content="Test description">
            <meta property="article:published_time" content="2024-10-15T10:00:00Z">
            <meta property="og:title" content="Open Graph Title">
        </head>
        <body>
            <article>
                <h1>Article Title</h1>
                <p>Article content here.</p>
            </article>
        </body>
        </html>
        """
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/metadata",
            content=html_with_metadata.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        # Should extract title
        assert extracted.title
        assert "Test Article" in extracted.title or "Article Title" in extracted.title
        
        # Should extract metadata if configured
        if test_config.extractor.extract_metadata:
            assert extracted.metadata is not None

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_empty_content_handling(self, test_config):
        """Test handling of pages with no meaningful content."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        empty_html = """
        <html>
        <head><title>Empty Page</title></head>
        <body>
            <nav>Navigation</nav>
            <footer>Footer</footer>
        </body>
        </html>
        """
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/empty",
            content=empty_html.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        # Should not crash on empty content
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        # Should return something, even if minimal
        assert extracted is not None
        assert extracted.url == "https://test.com/empty"

    @pytest.mark.golden
    @pytest.mark.asyncio
    async def test_malformed_html_handling(self, test_config):
        """Test handling of malformed HTML."""
        from mcp_web.extractor import ContentExtractor
        from mcp_web.fetcher import FetchResult
        
        malformed_html = """
        <html>
        <body>
            <article>
                <h1>Title
                <p>Unclosed paragraph
                <div>Unclosed div
                <p>Some content here</p>
            </article>
        </body>
        """
        
        extractor = ContentExtractor(test_config.extractor, cache=None)
        
        fetch_result = FetchResult(
            url="https://test.com/malformed",
            content=malformed_html.encode("utf-8"),
            content_type="text/html",
            headers={},
            status_code=200,
            fetch_method="test",
        )
        
        # Should handle malformed HTML gracefully
        extracted = await extractor.extract(fetch_result, use_cache=False)
        
        assert extracted is not None
        # Should still extract some content
        assert "content" in extracted.content.lower()
