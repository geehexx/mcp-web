"""Unit tests for utils module."""

import pytest

from mcp_web.utils import (
    TokenCounter,
    average_sentence_word_count,
    calculate_code_block_ratio,
    estimate_reading_time,
    extract_code_blocks,
    format_markdown_summary,
    normalize_url,
    sanitize_filename,
    validate_url,
)


@pytest.mark.unit
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

    def test_encoding_name(self):
        """Test encoding name is set correctly."""
        counter = TokenCounter("cl100k_base")
        assert counter.encoding_name == "cl100k_base"

    def test_different_encoding(self):
        """Test with different encoding."""
        counter = TokenCounter("p50k_base")
        assert counter.encoding_name == "p50k_base"


@pytest.mark.unit
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

    def test_validate_url_edge_cases(self):
        """Test edge cases for URL validation."""
        assert not validate_url("//example.com")  # No scheme
        assert not validate_url("https://")  # No netloc
        assert not validate_url("file:///path/to/file")  # file scheme

    def test_normalize_url(self):
        """Test URL normalization."""
        # Remove fragment
        assert normalize_url("https://example.com#section") == "https://example.com"

        # Sort query params
        normalized = normalize_url("https://example.com?b=2&a=1")
        assert "a=1" in normalized
        assert normalized.index("a=1") < normalized.index("b=2")

    def test_normalize_url_complex(self):
        """Test complex URL normalization."""
        url = "https://example.com/path?z=3&y=2&x=1#fragment"
        normalized = normalize_url(url)

        assert "#" not in normalized  # Fragment removed
        assert "x=1" in normalized
        assert "y=2" in normalized
        assert "z=3" in normalized


@pytest.mark.unit
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

    def test_format_markdown_summary_multiple_sources(self):
        """Test formatting with multiple sources."""
        summary = format_markdown_summary(
            "Summary",
            sources=["https://example.com", "https://test.com"],
        )

        assert "1. [https://example.com]" in summary
        assert "2. [https://test.com]" in summary

    def test_format_markdown_summary_no_metadata(self):
        """Test formatting without metadata."""
        summary = format_markdown_summary("Summary", sources=[], metadata=None)
        assert "## Metadata" not in summary


@pytest.mark.unit
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

    def test_extract_code_blocks_empty(self):
        """Test extraction with no code blocks."""
        markdown = "Just plain text"
        blocks = extract_code_blocks(markdown)
        assert len(blocks) == 0


@pytest.mark.unit
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

    def test_sanitize_filename_special_chars(self):
        """Test sanitization of special characters."""
        # Seven special chars: < > : " | ? *
        assert sanitize_filename('file<>:"|?*.txt') == "file_______.txt"


@pytest.mark.unit
class TestReadingTime:
    """Tests for reading time estimation."""

    def test_estimate_reading_time(self):
        """Test reading time estimation."""
        # 200 words at 200 wpm = 1 minute
        text = " ".join(["word"] * 200)
        assert estimate_reading_time(text) == 1

        # 400 words at 200 wpm = 2 minutes
        text = " ".join(["word"] * 400)
        assert estimate_reading_time(text) == 2

    def test_estimate_reading_time_custom_wpm(self):
        """Test reading time with custom WPM."""
        text = " ".join(["word"] * 100)
        # 100 words at 100 wpm = 1 minute
        assert estimate_reading_time(text, wpm=100) == 1

    def test_estimate_reading_time_minimum(self):
        """Test minimum reading time of 1 minute."""
        text = "Just a few words"
        assert estimate_reading_time(text) >= 1


@pytest.mark.unit
class TestCodeBlockRatio:
    """Tests for code block ratio calculation."""

    def test_calculate_code_block_ratio_no_code(self):
        """Test ratio with no code blocks."""
        text = "Just plain text with no code"
        assert calculate_code_block_ratio(text) == 0.0

    def test_calculate_code_block_ratio_all_code(self):
        """Test ratio with all content in code blocks."""
        text = "```\ncode\n```"
        ratio = calculate_code_block_ratio(text)
        assert ratio > 0.8  # Most of the content is code

    def test_calculate_code_block_ratio_mixed(self):
        """Test ratio with mixed content."""
        text = """Some text before

```python
def hello():
    print("world")
```

Some text after
"""
        ratio = calculate_code_block_ratio(text)
        assert 0 < ratio < 1  # Between 0 and 1

    def test_calculate_code_block_ratio_empty(self):
        """Test ratio with empty text."""
        assert calculate_code_block_ratio("") == 0.0


@pytest.mark.unit
class TestSentenceWordCount:
    """Tests for average sentence word count."""

    def test_average_sentence_word_count_single(self):
        """Test with single sentence."""
        text = "This is a simple sentence."
        avg = average_sentence_word_count(text)
        assert avg == 5.0

    def test_average_sentence_word_count_multiple(self):
        """Test with multiple sentences."""
        text = "Short. This is a longer sentence. Tiny."
        avg = average_sentence_word_count(text)
        assert 1 < avg < 10  # Average should be reasonable

    def test_average_sentence_word_count_empty(self):
        """Test with empty text."""
        assert average_sentence_word_count("") == 0.0

    def test_average_sentence_word_count_whitespace(self):
        """Test with only whitespace."""
        assert average_sentence_word_count("   ") == 0.0

    def test_average_sentence_word_count_punctuation(self):
        """Test with different punctuation."""
        text = "One! Two? Three."
        avg = average_sentence_word_count(text)
        assert avg == 1.0
