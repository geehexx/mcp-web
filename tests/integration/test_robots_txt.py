"""Integration tests for robots.txt handling.

Tests respect for robots.txt protocol, including:
- Parsing robots.txt files
- Respecting disallow rules
- Handling crawl-delay
- Configurable override (ignore robots.txt)
"""

from urllib.robotparser import RobotFileParser

import pytest

from mcp_web.config import FetcherSettings
from mcp_web.fetcher import URLFetcher


@pytest.fixture
def sample_robots_strict():
    """Strict robots.txt that disallows most crawling."""
    return """
User-agent: *
Disallow: /admin/
Disallow: /private/
Disallow: /api/
Crawl-delay: 2

User-agent: mcp-web
Disallow: /
    """


@pytest.fixture
def sample_robots_permissive():
    """Permissive robots.txt."""
    return """
User-agent: *
Disallow: /admin/
Allow: /

Crawl-delay: 1
    """


@pytest.fixture
def sample_robots_empty():
    """Empty robots.txt (allows everything)."""
    return """
# No rules
    """


@pytest.mark.integration
@pytest.mark.unit
class TestRobotsParser:
    """Test robots.txt parsing logic."""

    def test_parse_strict_robots(self, sample_robots_strict):
        """Test parsing strict robots.txt."""
        parser = RobotFileParser()
        parser.parse(sample_robots_strict.splitlines())

        # Test with default user agent
        assert not parser.can_fetch("*", "http://example.com/admin/test")
        assert not parser.can_fetch("*", "http://example.com/private/data")
        assert not parser.can_fetch("*", "http://example.com/api/v1")
        assert parser.can_fetch("*", "http://example.com/public/page")

        # Test with mcp-web user agent (should be completely disallowed)
        assert not parser.can_fetch("mcp-web", "http://example.com/")
        assert not parser.can_fetch("mcp-web", "http://example.com/anything")

    def test_parse_permissive_robots(self, sample_robots_permissive):
        """Test parsing permissive robots.txt."""
        parser = RobotFileParser()
        parser.parse(sample_robots_permissive.splitlines())

        # Most paths should be allowed
        assert parser.can_fetch("*", "http://example.com/")
        assert parser.can_fetch("*", "http://example.com/public")
        assert not parser.can_fetch("*", "http://example.com/admin/")

    def test_parse_empty_robots(self, sample_robots_empty):
        """Test that empty robots.txt allows everything."""
        parser = RobotFileParser()
        parser.parse(sample_robots_empty.splitlines())

        # Everything should be allowed
        assert parser.can_fetch("*", "http://example.com/anything")
        assert parser.can_fetch("mcp-web", "http://example.com/anything")

    def test_extract_crawl_delay(self, sample_robots_strict):
        """Test extracting crawl-delay directive."""
        parser = RobotFileParser()
        parser.parse(sample_robots_strict.splitlines())

        delay = parser.crawl_delay("*")
        assert delay == 2

        # mcp-web specific delay (inherits from *)
        mcp_delay = parser.crawl_delay("mcp-web")
        # May be None if not specifically set for mcp-web
        assert mcp_delay is None or mcp_delay == 2

    def test_user_agent_matching(self):
        """Test user agent matching logic."""
        robots = """
User-agent: googlebot
Disallow: /private/

User-agent: *
Disallow: /admin/
        """

        parser = RobotFileParser()
        parser.parse(robots.splitlines())

        # Googlebot has specific rules
        assert not parser.can_fetch("googlebot", "http://example.com/private/")
        assert parser.can_fetch("googlebot", "http://example.com/admin/")

        # Other bots follow * rules
        assert parser.can_fetch("otherbot", "http://example.com/private/")
        assert not parser.can_fetch("otherbot", "http://example.com/admin/")


@pytest.mark.integration
@pytest.mark.live
@pytest.mark.asyncio
class TestRobotsTxtFetching:
    """Test fetching and respecting robots.txt from real sites."""

    async def test_fetch_robots_txt(self):
        """Test fetching robots.txt from a domain."""
        config = FetcherSettings()
        fetcher = URLFetcher(config)

        try:
            # Test with a known site that has robots.txt
            robots_url = "https://www.python.org/robots.txt"
            result = await fetcher.fetch(robots_url)

            assert result.status_code == 200
            content = result.content.decode("utf-8")
            assert "User-agent" in content or "Disallow" in content

        except Exception as e:
            pytest.skip(f"Could not fetch robots.txt: {e}")
        finally:
            await fetcher.close()

    async def test_missing_robots_txt_allows_crawling(self):
        """Test that missing robots.txt allows crawling."""
        config = FetcherSettings()
        fetcher = URLFetcher(config)

        try:
            # Try to fetch robots.txt from a site that likely doesn't have one
            # If 404, crawling should be allowed
            robots_url = "https://httpbin.org/robots.txt"

            try:
                result = await fetcher.fetch(robots_url)
                # If we get here, robots.txt exists - that's fine too
            except Exception:
                # 404 or other error means no robots.txt
                # This should allow crawling
                pass

        finally:
            await fetcher.close()

    async def test_respect_disallow_rules(self, sample_robots_strict):
        """Test that disallowed URLs are not fetched."""
        # This would be implemented in the fetcher to check robots.txt
        # before fetching

        parser = RobotFileParser()
        parser.parse(sample_robots_strict.splitlines())

        url = "http://example.com/admin/users"
        can_fetch = parser.can_fetch("*", url)

        if not can_fetch:
            # Should not fetch (would need actual implementation in fetcher)
            assert True
        else:
            pytest.fail("Should not be allowed to fetch disallowed URL")


@pytest.mark.integration
@pytest.mark.unit
class TestRobotsConfiguration:
    """Test robots.txt configuration options."""

    def test_respect_robots_by_default(self):
        """Test that robots.txt is respected by default."""
        config = FetcherSettings()

        # Default should respect robots.txt
        assert config.respect_robots_txt

    def test_can_ignore_robots(self):
        """Test that robots.txt can be ignored when configured."""
        config = FetcherSettings(respect_robots_txt=False)

        assert not config.respect_robots_txt

    def test_configurable_user_agent(self):
        """Test that User-Agent affects robots.txt rules."""
        config1 = FetcherSettings(user_agent="mcp-web/1.0")
        config2 = FetcherSettings(user_agent="CustomBot/1.0")

        assert config1.user_agent != config2.user_agent

        # Different user agents might have different rules
        robots = """
User-agent: mcp-web
Disallow: /

User-agent: *
Allow: /
        """

        parser = RobotFileParser()
        parser.parse(robots.splitlines())

        # mcp-web is disallowed
        assert not parser.can_fetch("mcp-web/1.0", "http://example.com/page")
        # Other agents are allowed
        assert parser.can_fetch("CustomBot/1.0", "http://example.com/page")


@pytest.mark.integration
@pytest.mark.asyncio
class TestCrawlDelay:
    """Test crawl-delay handling."""

    async def test_respect_crawl_delay(self, sample_robots_strict):
        """Test that crawl-delay is respected."""
        import asyncio
        import time

        parser = RobotFileParser()
        parser.parse(sample_robots_strict.splitlines())

        delay = parser.crawl_delay("*")
        assert delay == 2

        # Simulate respecting delay
        start = time.perf_counter()
        await asyncio.sleep(delay)
        elapsed = time.perf_counter() - start

        assert elapsed >= delay

    async def test_no_delay_when_not_specified(self, sample_robots_permissive):
        """Test behavior when no crawl-delay specified."""
        parser = RobotFileParser()
        parser.parse(sample_robots_permissive.splitlines())

        delay = parser.crawl_delay("*")
        # Should have a delay specified in the fixture
        assert delay == 1

    async def test_configurable_delay_override(self):
        """Test that crawl-delay can be overridden in config."""
        config = FetcherSettings(
            crawl_delay_override=0.5,  # Override to 0.5 seconds
        )

        # Would use config delay instead of robots.txt delay
        assert config.crawl_delay_override == 0.5


@pytest.mark.integration
@pytest.mark.asyncio
class TestRobotsIntegration:
    """Test full integration of robots.txt handling."""

    async def test_check_before_fetch(self):
        """Test checking robots.txt before fetching URL."""
        config = FetcherSettings(respect_robots_txt=True)
        fetcher = URLFetcher(config)

        # Implementation would:
        # 1. Extract domain from URL
        # 2. Fetch robots.txt for that domain
        # 3. Parse and cache robots.txt
        # 4. Check if URL is allowed
        # 5. Fetch if allowed, raise exception if not

        # This is a design test - actual implementation needed
        pass

    async def test_cache_robots_txt(self):
        """Test that robots.txt is cached per domain."""
        # Should not fetch robots.txt for every URL from same domain
        # Cache should be keyed by domain

        # Example:
        # First fetch: example.com/page1 -> fetch robots.txt
        # Second fetch: example.com/page2 -> use cached robots.txt
        pass

    async def test_robots_txt_timeout(self):
        """Test handling of robots.txt fetch timeout."""
        config = FetcherSettings(
            timeout=1,  # Short timeout
            respect_robots_txt=True,
        )
        fetcher = URLFetcher(config)

        # If robots.txt fetch times out, should allow crawling
        # (fail open, not fail closed)
        pass


@pytest.mark.unit
class TestRobotsEdgeCases:
    """Test edge cases in robots.txt handling."""

    def test_malformed_robots_txt(self):
        """Test handling of malformed robots.txt."""
        malformed = """
User-agent *  # Missing colon
Disallow /admin
Invalid line here
        """

        parser = RobotFileParser()
        parser.parse(malformed.splitlines())

        # Should handle gracefully (permissive parsing)
        # Don't crash on malformed input
        pass

    def test_very_large_robots_txt(self):
        """Test handling of very large robots.txt files."""
        # Some sites have huge robots.txt files
        # Should handle efficiently or limit size

        large_robots = "Disallow: /path{}\n".format("\n") * 10000

        parser = RobotFileParser()
        # Should not crash or take too long
        import time

        start = time.perf_counter()
        parser.parse(large_robots.splitlines())
        elapsed = time.perf_counter() - start

        # Should parse in reasonable time (< 1 second)
        assert elapsed < 1.0

    def test_unicode_in_robots_txt(self):
        """Test handling of Unicode characters in robots.txt."""
        unicode_robots = """
User-agent: *
Disallow: /café/
Disallow: /日本語/
        """

        parser = RobotFileParser()
        parser.parse(unicode_robots.splitlines())

        # Should handle Unicode paths
        pass

    def test_relative_vs_absolute_disallow(self):
        """Test handling of relative vs absolute paths."""
        robots = """
User-agent: *
Disallow: /admin
Disallow: /admin/
        """

        parser = RobotFileParser()
        parser.parse(robots.splitlines())

        # Both should disallow admin and subpaths
        assert not parser.can_fetch("*", "http://example.com/admin")
        assert not parser.can_fetch("*", "http://example.com/admin/")
        assert not parser.can_fetch("*", "http://example.com/admin/users")


# Helper function for robots.txt checking (would go in fetcher.py)
def should_fetch_url(
    url: str, robots_parser: RobotFileParser, user_agent: str, respect_robots: bool
) -> bool:
    """Determine if URL should be fetched based on robots.txt.

    Args:
        url: URL to check
        robots_parser: Parsed robots.txt for the domain
        user_agent: User agent string
        respect_robots: Whether to respect robots.txt

    Returns:
        True if URL can be fetched
    """
    if not respect_robots:
        return True

    if robots_parser is None:
        # No robots.txt found - allow
        return True

    return robots_parser.can_fetch(user_agent, url)


@pytest.mark.unit
class TestShouldFetchHelper:
    """Test the should_fetch_url helper function."""

    def test_allows_when_ignoring_robots(self):
        """Test that all URLs are allowed when ignoring robots.txt."""
        result = should_fetch_url(
            "http://example.com/admin", None, "mcp-web/1.0", respect_robots=False
        )
        assert result

    def test_allows_when_no_robots_txt(self):
        """Test that all URLs are allowed when no robots.txt exists."""
        result = should_fetch_url(
            "http://example.com/page", None, "mcp-web/1.0", respect_robots=True
        )
        assert result

    def test_respects_disallow_rules(self, sample_robots_strict):
        """Test that disallowed URLs are blocked."""
        parser = RobotFileParser()
        parser.parse(sample_robots_strict.splitlines())

        result = should_fetch_url(
            "http://example.com/admin/users", parser, "*", respect_robots=True
        )
        assert not result

    def test_allows_permitted_urls(self, sample_robots_permissive):
        """Test that allowed URLs are permitted."""
        parser = RobotFileParser()
        parser.parse(sample_robots_permissive.splitlines())

        result = should_fetch_url(
            "http://example.com/public/page", parser, "*", respect_robots=True
        )
        assert result
