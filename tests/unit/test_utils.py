"""Unit tests for utils module."""

import pytest

from mcp_web.utils import (
    TokenCounter,
    extract_code_blocks,
    format_markdown_summary,
    normalize_url,
    sanitize_filename,
    validate_url,
)


class TestTokenCounter:
    """Tests for TokenCounter."""

    def test_count_tokens(self):
        """Test token counting."""
        counter = TokenCounter()
        
        # Simple text
        assert counter.count_tokens("Hello") > 0
        assert counter.count_tokens("Hello world") > counter.count_tokens("Hello")
        
        # Empty string
        assert counter.count_tokens("") == 0

    def test_truncate_to_tokens(self):
        """Test token truncation."""
        counter = TokenCounter()
        
        text = "Hello world, this is a test."
        tokens = counter.count_tokens(text)
        
        # Truncate to half
        truncated = counter.truncate_to_tokens(text, tokens // 2)
        assert counter.count_tokens(truncated) <= tokens // 2
        assert len(truncated) < len(text)
        
        # Truncate to more than available
        not_truncated = counter.truncate_to_tokens(text, tokens + 100)
        assert not_truncated == text


class TestURLValidation:
    """Tests for URL validation."""

    def test_validate_url_valid(self):
        """Test valid URLs."""
        assert validate_url("https://example.com")
        assert validate_url("http://example.com")
        assert validate_url("https://example.com/path")
        assert validate_url("https://example.com:8080/path?query=1")

    def test_validate_url_invalid(self):
        """Test invalid URLs."""
        assert not validate_url("not a url")
        assert not validate_url("ftp://example.com")  # Wrong scheme
        assert not validate_url("javascript:alert(1)")
        assert not validate_url("")

    def test_normalize_url(self):
        """Test URL normalization."""
        # Remove fragment
        assert normalize_url("https://example.com#section") == "https://example.com"
        
        # Sort query params
        normalized = normalize_url("https://example.com?b=2&a=1")
        assert "a=1" in normalized
        assert normalized.index("a=1") < normalized.index("b=2")


class TestMarkdownFormatting:
    """Tests for Markdown formatting."""

    def test_format_markdown_summary(self):
        """Test summary formatting."""
        summary = format_markdown_summary(
            "This is a summary.",
            sources=["https://example.com"],
            metadata={"date": "2025-10-15"},
        )
        
        assert "# Summary" in summary
        assert "This is a summary." in summary
        assert "## Sources" in summary
        assert "https://example.com" in summary
        assert "## Metadata" in summary
        assert "date" in summary

    def test_format_markdown_summary_no_sources(self):
        """Test formatting without sources."""
        summary = format_markdown_summary("Summary", sources=[])
        assert "# Summary" in summary
        assert "## Sources" not in summary


class TestCodeExtraction:
    """Tests for code extraction."""

    def test_extract_code_blocks(self):
        """Test code block extraction."""
        markdown = """
Some text

```python
print('hello')
```

More text

```javascript
console.log('world');
```
"""
        
        blocks = extract_code_blocks(markdown)
        assert len(blocks) == 2
        assert blocks[0][0] == "python"
        assert "print" in blocks[0][1]
        assert blocks[1][0] == "javascript"
        assert "console.log" in blocks[1][1]

    def test_extract_code_blocks_no_language(self):
        """Test code blocks without language specifier."""
        markdown = "```\ncode here\n```"
        blocks = extract_code_blocks(markdown)
        assert len(blocks) == 1
        assert blocks[0][0] == "text"


class TestFilenameUtils:
    """Tests for filename utilities."""

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        assert sanitize_filename("hello.txt") == "hello.txt"
        assert sanitize_filename("hello/world.txt") == "hello_world.txt"
        assert sanitize_filename("hello:world?.txt") == "hello_world_.txt"
        
        # Test length limit
        long_name = "a" * 300
        sanitized = sanitize_filename(long_name)
        assert len(sanitized) <= 255
