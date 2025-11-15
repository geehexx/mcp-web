"""Custom exception hierarchy for mcp-web.

Provides specific exception types for better error handling and debugging.
Replaces generic Exception usage with typed exceptions following Python best practices.

Exception Hierarchy:
    MCPWebError (base)
    ├── FetchError (URL fetching)
    │   ├── NetworkError (connection issues)
    │   ├── TimeoutError (timeout exceeded)
    │   └── HTTPError (HTTP status errors)
    ├── ExtractionError (content extraction)
    │   └── ParseError (HTML/content parsing)
    ├── SummarizationError (LLM summarization)
    │   ├── ProviderError (LLM provider issues)
    │   └── TokenLimitError (token count exceeded)
    ├── SecurityError (security violations)
    │   ├── ValidationError (input validation)
    │   └── PromptInjectionError (detected attack)
    ├── CacheError (caching operations)
    ├── ConfigurationError (configuration issues)
    └── BrowserError (browser pool/Playwright)

References:
    - PEP 3151: Exception hierarchy design
    - MODERNIZATION_ROADMAP.md Phase 2.4
"""

from __future__ import annotations


class MCPWebError(Exception):
    """Base exception for all mcp-web errors.

    All custom exceptions inherit from this base class, allowing
    consumers to catch all mcp-web errors with a single except clause.

    Example:
        >>> try:
        ...     # mcp-web operations
        ...     pass
        ... except MCPWebError as e:
        ...     print(f"MCP-Web error: {e}")
    """

    pass


# ============================================================================
# Fetch Errors
# ============================================================================


class FetchError(MCPWebError):
    """Base class for URL fetching errors.

    Raised when URL fetching fails for any reason (network, HTTP, timeout).

    Attributes:
        url: The URL that failed to fetch
        status_code: HTTP status code (if applicable)

    Example:
        >>> raise FetchError("Failed to fetch", url="https://example.com")
    """

    def __init__(
        self,
        message: str,
        url: str | None = None,
        status_code: int | None = None,
    ):
        """Initialize fetch error.

        Args:
            message: Error description
            url: URL that failed (optional)
            status_code: HTTP status code (optional)
        """
        super().__init__(message)
        self.url = url
        self.status_code = status_code

    def __str__(self) -> str:
        """Format error message with context."""
        parts = [super().__str__()]
        if self.url:
            parts.append(f"URL: {self.url}")
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        return " | ".join(parts)


class NetworkError(FetchError):
    """Network connectivity error.

    Raised when network connection fails (DNS, connection refused, etc.).

    Example:
        >>> raise NetworkError("Connection refused", url="https://unreachable.local")
    """

    pass


class TimeoutError(FetchError):
    """Request timeout error.

    Raised when HTTP request or browser navigation exceeds timeout.

    Attributes:
        timeout: Timeout value in seconds

    Example:
        >>> raise TimeoutError("Request timed out", url="https://slow.com", timeout=30)
    """

    def __init__(
        self,
        message: str,
        url: str | None = None,
        timeout: float | None = None,
    ):
        """Initialize timeout error.

        Args:
            message: Error description
            url: URL that timed out (optional)
            timeout: Timeout value in seconds (optional)
        """
        super().__init__(message, url=url)
        self.timeout = timeout

    def __str__(self) -> str:
        """Format error message with timeout."""
        base = super().__str__()
        if self.timeout:
            return f"{base} | Timeout: {self.timeout}s"
        return base


class HTTPError(FetchError):
    """HTTP protocol error.

    Raised for HTTP status code errors (4xx, 5xx).

    Example:
        >>> raise HTTPError("Not found", url="https://example.com/missing", status_code=404)
    """

    pass


# ============================================================================
# Extraction Errors
# ============================================================================


class ExtractionError(MCPWebError):
    """Content extraction error.

    Raised when content extraction or parsing fails.

    Attributes:
        content_preview: Preview of content that failed (optional)

    Example:
        >>> raise ExtractionError("Failed to parse HTML")
    """

    def __init__(self, message: str, content_preview: str | None = None):
        """Initialize extraction error.

        Args:
            message: Error description
            content_preview: Preview of problematic content (optional)
        """
        super().__init__(message)
        self.content_preview = content_preview


class ParseError(ExtractionError):
    """HTML/content parsing error.

    Raised when HTML or content parsing fails.

    Example:
        >>> raise ParseError("Invalid HTML structure", content_preview="<div>broken...")
    """

    pass


# ============================================================================
# LLM/Summarization Errors
# ============================================================================


class SummarizationError(MCPWebError):
    """LLM summarization error.

    Raised when LLM summarization fails.

    Attributes:
        provider: LLM provider name (optional)
        model: Model name (optional)

    Example:
        >>> raise SummarizationError("Generation failed", provider="openai", model="gpt-4")
    """

    def __init__(
        self,
        message: str,
        provider: str | None = None,
        model: str | None = None,
    ):
        """Initialize summarization error.

        Args:
            message: Error description
            provider: LLM provider name (optional)
            model: Model name (optional)
        """
        super().__init__(message)
        self.provider = provider
        self.model = model

    def __str__(self) -> str:
        """Format error with provider/model context."""
        parts = [super().__str__()]
        if self.provider:
            parts.append(f"Provider: {self.provider}")
        if self.model:
            parts.append(f"Model: {self.model}")
        return " | ".join(parts)


class ProviderError(SummarizationError):
    """LLM provider error.

    Raised when LLM provider API fails (authentication, rate limit, etc.).

    Example:
        >>> raise ProviderError("Rate limit exceeded", provider="openai")
    """

    pass


class TokenLimitError(SummarizationError):
    """Token count limit exceeded.

    Raised when content exceeds model's token limit.

    Attributes:
        token_count: Actual token count
        token_limit: Maximum allowed tokens

    Example:
        >>> raise TokenLimitError("Content too long", token_count=10000, token_limit=8000)
    """

    def __init__(
        self,
        message: str,
        token_count: int | None = None,
        token_limit: int | None = None,
        **kwargs,
    ):
        """Initialize token limit error.

        Args:
            message: Error description
            token_count: Actual token count (optional)
            token_limit: Maximum allowed tokens (optional)
            **kwargs: Additional arguments for SummarizationError
        """
        super().__init__(message, **kwargs)
        self.token_count = token_count
        self.token_limit = token_limit

    def __str__(self) -> str:
        """Format error with token counts."""
        base = super().__str__()
        if self.token_count and self.token_limit:
            return f"{base} | Tokens: {self.token_count}/{self.token_limit}"
        return base


# ============================================================================
# Security Errors
# ============================================================================


class SecurityError(MCPWebError):
    """Security violation error.

    Raised when security validation fails.

    Example:
        >>> raise SecurityError("SSRF attempt detected")
    """

    pass


class ValidationError(SecurityError):
    """Input validation error.

    Raised when input validation fails (URL validation, path validation, etc.).

    Attributes:
        field: Field that failed validation (optional)
        value_preview: Preview of invalid value (optional)

    Example:
        >>> raise ValidationError("Invalid URL", field="url", value_preview="javascript:alert()")
    """

    def __init__(
        self,
        message: str,
        field: str | None = None,
        value_preview: str | None = None,
    ):
        """Initialize validation error.

        Args:
            message: Error description
            field: Field that failed validation (optional)
            value_preview: Preview of invalid value (optional)
        """
        super().__init__(message)
        self.field = field
        self.value_preview = value_preview


class PromptInjectionError(SecurityError):
    """Prompt injection attack detected.

    Raised when prompt injection is detected in user input or web content.

    Attributes:
        confidence: Detection confidence score (0.0-1.0)
        patterns: Matched attack patterns

    Example:
        >>> raise PromptInjectionError(
        ...     "Injection detected",
        ...     confidence=0.95,
        ...     patterns=["ignore previous", "reveal system prompt"]
        ... )
    """

    def __init__(
        self,
        message: str,
        confidence: float | None = None,
        patterns: list[str] | None = None,
    ):
        """Initialize prompt injection error.

        Args:
            message: Error description
            confidence: Detection confidence (0.0-1.0)
            patterns: Matched attack patterns
        """
        super().__init__(message)
        self.confidence = confidence
        self.patterns = patterns or []


# ============================================================================
# Cache Errors
# ============================================================================


class CacheError(MCPWebError):
    """Cache operation error.

    Raised when cache operations fail (read, write, cleanup).

    Example:
        >>> raise CacheError("Failed to write cache entry")
    """

    pass


# ============================================================================
# Configuration Errors
# ============================================================================


class ConfigurationError(MCPWebError):
    """Configuration error.

    Raised when configuration is invalid or missing.

    Attributes:
        config_key: Configuration key that is invalid (optional)

    Example:
        >>> raise ConfigurationError("Missing API key", config_key="OPENAI_API_KEY")
    """

    def __init__(self, message: str, config_key: str | None = None):
        """Initialize configuration error.

        Args:
            message: Error description
            config_key: Configuration key that is invalid (optional)
        """
        super().__init__(message)
        self.config_key = config_key

    def __str__(self) -> str:
        """Format error with config key."""
        base = super().__str__()
        if self.config_key:
            return f"{base} | Config: {self.config_key}"
        return base


# ============================================================================
# Browser/Playwright Errors
# ============================================================================


class BrowserError(MCPWebError):
    """Browser pool or Playwright error.

    Raised when browser operations fail.

    Example:
        >>> raise BrowserError("Browser launch failed")
    """

    pass


# ============================================================================
# Utility Functions
# ============================================================================


def format_exception_chain(exc: Exception) -> str:
    """Format exception chain for logging.

    Creates a human-readable string showing the full exception chain.

    Args:
        exc: Exception to format

    Returns:
        Formatted exception chain string

    Example:
        >>> try:
        ...     raise NetworkError("Connection failed", url="https://example.com")
        ... except NetworkError as e:
        ...     print(format_exception_chain(e))
        NetworkError: Connection failed | URL: https://example.com
    """
    chain = []
    current = exc

    while current is not None:
        chain.append(f"{current.__class__.__name__}: {current}")
        current = current.__cause__

    return "\n  Caused by: ".join(chain)
