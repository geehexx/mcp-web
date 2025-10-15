"""Utility functions for mcp-web.

Provides shared helpers for:
- Token counting (tiktoken)
- URL validation
- Markdown formatting
- Text normalization
"""

import re
from typing import Any
from urllib.parse import urlparse

import tiktoken


class TokenCounter:
    """Token counting utilities using tiktoken.

    Design Decision DD-005: Use tiktoken for accurate OpenAI model token counts.
    """

    def __init__(self, encoding_name: str = "cl100k_base"):
        """Initialize token counter.

        Args:
            encoding_name: Tiktoken encoding (default: cl100k_base for GPT-4/3.5)
        """
        self.encoding = tiktoken.get_encoding(encoding_name)
        self.encoding_name = encoding_name

    def count_tokens(self, text: str) -> int:
        """Count tokens in text.

        Args:
            text: Input text

        Returns:
            Number of tokens

        Example:
            >>> counter = TokenCounter()
            >>> counter.count_tokens("Hello, world!")
            4
        """
        return len(self.encoding.encode(text))

    def truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to maximum token count.

        Args:
            text: Input text
            max_tokens: Maximum allowed tokens

        Returns:
            Truncated text

        Example:
            >>> counter = TokenCounter()
            >>> counter.truncate_to_tokens("Hello world", 2)
            'Hello'
        """
        tokens = self.encoding.encode(text)
        if len(tokens) <= max_tokens:
            return text
        return self.encoding.decode(tokens[:max_tokens])


def validate_url(url: str) -> bool:
    """Validate URL format.

    Args:
        url: URL string to validate

    Returns:
        True if valid, False otherwise

    Example:
        >>> validate_url("https://example.com")
        True
        >>> validate_url("not a url")
        False
    """
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False


def normalize_url(url: str) -> str:
    """Normalize URL (remove fragments, sort query params).

    Args:
        url: Input URL

    Returns:
        Normalized URL

    Example:
        >>> normalize_url("https://example.com/page?b=2&a=1#section")
        'https://example.com/page?a=1&b=2'
    """
    from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

    parsed = urlparse(url)

    # Sort query parameters
    query_params = parse_qs(parsed.query)
    sorted_query = urlencode(sorted(query_params.items()), doseq=True)

    # Remove fragment
    normalized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, parsed.params, sorted_query, "")
    )

    return normalized


def format_markdown_summary(
    summary: str,
    sources: list[str],
    metadata: dict[str, Any] | None = None,
) -> str:
    """Format summary with citations and metadata.

    Args:
        summary: Main summary text
        sources: List of source URLs
        metadata: Optional metadata dict

    Returns:
        Formatted Markdown string

    Example:
        >>> format_markdown_summary(
        ...     "This is a summary.",
        ...     ["https://example.com"],
        ...     {"date": "2025-10-15"}
        ... )
        '# Summary\\n\\nThis is a summary.\\n\\n## Sources\\n...'
    """
    output = ["# Summary\n", summary, "\n"]

    if sources:
        output.append("\n## Sources\n\n")
        for i, url in enumerate(sources, 1):
            output.append(f"{i}. [{url}]({url})\n")

    if metadata:
        output.append("\n## Metadata\n\n")
        for key, value in metadata.items():
            output.append(f"- **{key}**: {value}\n")

    return "".join(output)


def extract_code_blocks(text: str) -> list[tuple[str, str]]:
    """Extract code blocks from Markdown text.

    Args:
        text: Markdown text

    Returns:
        List of (language, code) tuples

    Example:
        >>> extract_code_blocks("```python\\nprint('hi')\\n```")
        [('python', "print('hi')")]
    """
    pattern = r"```(\w+)?\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [(lang or "text", code.strip()) for lang, code in matches]


def sanitize_filename(filename: str) -> str:
    """Sanitize string for use as filename.

    Args:
        filename: Input filename

    Returns:
        Sanitized filename

    Example:
        >>> sanitize_filename("hello/world?.txt")
        'hello_world_.txt'
    """
    # Remove invalid filename characters
    sanitized = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Limit length
    return sanitized[:255]


def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """Estimate reading time in minutes.

    Args:
        text: Input text
        wpm: Words per minute (default: 200)

    Returns:
        Estimated reading time in minutes

    Example:
        >>> estimate_reading_time("word " * 400)
        2
    """
    word_count = len(text.split())
    return max(1, round(word_count / wpm))
