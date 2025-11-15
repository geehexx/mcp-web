"""Tests for custom exception hierarchy.

Tests all custom exceptions and their attributes, ensuring proper
inheritance and error formatting.

Coverage target: 100% (foundational module)
"""

import pytest

from mcp_web.exceptions import (
    BrowserError,
    CacheError,
    ConfigurationError,
    ExtractionError,
    FetchError,
    HTTPError,
    MCPWebError,
    NetworkError,
    ParseError,
    PromptInjectionError,
    ProviderError,
    SecurityError,
    SummarizationError,
    TimeoutError,
    TokenLimitError,
    ValidationError,
    format_exception_chain,
)


class TestBaseException:
    """Test MCPWebError base exception."""

    def test_base_exception_creation(self):
        """Test creating base exception."""
        exc = MCPWebError("Test error")
        assert str(exc) == "Test error"
        assert isinstance(exc, Exception)

    def test_base_exception_inheritance(self):
        """Test that all custom exceptions inherit from MCPWebError."""
        exceptions = [
            FetchError("test"),
            ExtractionError("test"),
            SummarizationError("test"),
            SecurityError("test"),
            CacheError("test"),
            ConfigurationError("test"),
            BrowserError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, MCPWebError)
            assert isinstance(exc, Exception)

    def test_catch_all_mcp_errors(self):
        """Test catching all MCP errors with base exception."""
        try:
            raise FetchError("Network issue")
        except MCPWebError as e:
            assert str(e) == "Network issue"


class TestFetchErrors:
    """Test fetch-related exceptions."""

    def test_fetch_error_basic(self):
        """Test basic FetchError."""
        exc = FetchError("Failed to fetch")
        assert str(exc) == "Failed to fetch"

    def test_fetch_error_with_url(self):
        """Test FetchError with URL."""
        exc = FetchError("Failed", url="https://example.com")
        assert "Failed" in str(exc)
        assert "https://example.com" in str(exc)
        assert exc.url == "https://example.com"

    def test_fetch_error_with_status_code(self):
        """Test FetchError with status code."""
        exc = FetchError("Failed", status_code=404)
        assert "Failed" in str(exc)
        assert "404" in str(exc)
        assert exc.status_code == 404

    def test_fetch_error_with_all_fields(self):
        """Test FetchError with all fields."""
        exc = FetchError(
            "Failed",
            url="https://example.com",
            status_code=500,
        )
        assert "Failed" in str(exc)
        assert "https://example.com" in str(exc)
        assert "500" in str(exc)

    def test_network_error(self):
        """Test NetworkError."""
        exc = NetworkError("Connection refused", url="https://unreachable.local")
        assert isinstance(exc, FetchError)
        assert "Connection refused" in str(exc)
        assert "unreachable.local" in str(exc)

    def test_timeout_error_basic(self):
        """Test TimeoutError without timeout value."""
        exc = TimeoutError("Request timed out")
        assert isinstance(exc, FetchError)
        assert "Request timed out" in str(exc)

    def test_timeout_error_with_timeout(self):
        """Test TimeoutError with timeout value."""
        exc = TimeoutError(
            "Request timed out",
            url="https://slow.com",
            timeout=30.0,
        )
        assert "Request timed out" in str(exc)
        assert "slow.com" in str(exc)
        assert "30" in str(exc)
        assert exc.timeout == 30.0

    def test_http_error(self):
        """Test HTTPError."""
        exc = HTTPError(
            "Not found",
            url="https://example.com/missing",
            status_code=404,
        )
        assert isinstance(exc, FetchError)
        assert "Not found" in str(exc)
        assert "404" in str(exc)


class TestExtractionErrors:
    """Test extraction-related exceptions."""

    def test_extraction_error_basic(self):
        """Test basic ExtractionError."""
        exc = ExtractionError("Failed to extract")
        assert str(exc) == "Failed to extract"
        assert exc.content_preview is None

    def test_extraction_error_with_preview(self):
        """Test ExtractionError with content preview."""
        exc = ExtractionError(
            "Failed to parse",
            content_preview="<div>broken...",
        )
        assert "Failed to parse" in str(exc)
        assert exc.content_preview == "<div>broken..."

    def test_parse_error(self):
        """Test ParseError."""
        exc = ParseError("Invalid HTML", content_preview="<html><div>")
        assert isinstance(exc, ExtractionError)
        assert "Invalid HTML" in str(exc)
        assert exc.content_preview == "<html><div>"


class TestSummarizationErrors:
    """Test LLM summarization exceptions."""

    def test_summarization_error_basic(self):
        """Test basic SummarizationError."""
        exc = SummarizationError("Generation failed")
        assert str(exc) == "Generation failed"
        assert exc.provider is None
        assert exc.model is None

    def test_summarization_error_with_provider(self):
        """Test SummarizationError with provider."""
        exc = SummarizationError(
            "API error",
            provider="openai",
        )
        assert "API error" in str(exc)
        assert "openai" in str(exc)
        assert exc.provider == "openai"

    def test_summarization_error_with_model(self):
        """Test SummarizationError with model."""
        exc = SummarizationError(
            "Model error",
            provider="openai",
            model="gpt-4",
        )
        assert "Model error" in str(exc)
        assert "openai" in str(exc)
        assert "gpt-4" in str(exc)

    def test_provider_error(self):
        """Test ProviderError."""
        exc = ProviderError(
            "Rate limit exceeded",
            provider="openai",
        )
        assert isinstance(exc, SummarizationError)
        assert "Rate limit" in str(exc)
        assert "openai" in str(exc)

    def test_token_limit_error_basic(self):
        """Test TokenLimitError without counts."""
        exc = TokenLimitError("Content too long")
        assert isinstance(exc, SummarizationError)
        assert "Content too long" in str(exc)

    def test_token_limit_error_with_counts(self):
        """Test TokenLimitError with token counts."""
        exc = TokenLimitError(
            "Exceeded limit",
            token_count=10000,
            token_limit=8000,
            provider="openai",
            model="gpt-4",
        )
        assert "Exceeded limit" in str(exc)
        assert "10000" in str(exc)
        assert "8000" in str(exc)
        assert "openai" in str(exc)
        assert "gpt-4" in str(exc)
        assert exc.token_count == 10000
        assert exc.token_limit == 8000


class TestSecurityErrors:
    """Test security-related exceptions."""

    def test_security_error(self):
        """Test basic SecurityError."""
        exc = SecurityError("SSRF attempt detected")
        assert str(exc) == "SSRF attempt detected"

    def test_validation_error_basic(self):
        """Test basic ValidationError."""
        exc = ValidationError("Invalid input")
        assert isinstance(exc, SecurityError)
        assert str(exc) == "Invalid input"

    def test_validation_error_with_field(self):
        """Test ValidationError with field."""
        exc = ValidationError(
            "Invalid URL",
            field="url",
        )
        assert "Invalid URL" in str(exc)
        assert exc.field == "url"

    def test_validation_error_with_value_preview(self):
        """Test ValidationError with value preview."""
        exc = ValidationError(
            "Malicious URL",
            field="url",
            value_preview="javascript:alert()",
        )
        assert "Malicious URL" in str(exc)
        assert exc.field == "url"
        assert exc.value_preview == "javascript:alert()"

    def test_prompt_injection_error_basic(self):
        """Test basic PromptInjectionError."""
        exc = PromptInjectionError("Injection detected")
        assert isinstance(exc, SecurityError)
        assert "Injection detected" in str(exc)
        assert exc.patterns == []

    def test_prompt_injection_error_with_confidence(self):
        """Test PromptInjectionError with confidence."""
        exc = PromptInjectionError(
            "Attack detected",
            confidence=0.95,
        )
        assert "Attack detected" in str(exc)
        assert exc.confidence == 0.95

    def test_prompt_injection_error_with_patterns(self):
        """Test PromptInjectionError with matched patterns."""
        patterns = ["ignore previous", "reveal system prompt"]
        exc = PromptInjectionError(
            "Attack detected",
            confidence=0.98,
            patterns=patterns,
        )
        assert exc.confidence == 0.98
        assert exc.patterns == patterns


class TestCacheError:
    """Test cache exceptions."""

    def test_cache_error(self):
        """Test CacheError."""
        exc = CacheError("Failed to write cache")
        assert isinstance(exc, MCPWebError)
        assert str(exc) == "Failed to write cache"


class TestConfigurationError:
    """Test configuration exceptions."""

    def test_configuration_error_basic(self):
        """Test basic ConfigurationError."""
        exc = ConfigurationError("Missing configuration")
        assert isinstance(exc, MCPWebError)
        assert str(exc) == "Missing configuration"
        assert exc.config_key is None

    def test_configuration_error_with_key(self):
        """Test ConfigurationError with config key."""
        exc = ConfigurationError(
            "Missing API key",
            config_key="OPENAI_API_KEY",
        )
        assert "Missing API key" in str(exc)
        assert "OPENAI_API_KEY" in str(exc)
        assert exc.config_key == "OPENAI_API_KEY"


class TestBrowserError:
    """Test browser exceptions."""

    def test_browser_error(self):
        """Test BrowserError."""
        exc = BrowserError("Browser launch failed")
        assert isinstance(exc, MCPWebError)
        assert str(exc) == "Browser launch failed"


class TestExceptionRaising:
    """Test that exceptions can be raised and caught properly."""

    def test_raise_and_catch_specific(self):
        """Test raising and catching specific exception."""
        with pytest.raises(NetworkError) as exc_info:
            raise NetworkError("Connection failed", url="https://test.com")

        assert "Connection failed" in str(exc_info.value)
        assert exc_info.value.url == "https://test.com"

    def test_raise_and_catch_parent(self):
        """Test catching child exception with parent class."""
        try:
            raise HTTPError("Not found", status_code=404)
        except FetchError as e:
            assert isinstance(e, HTTPError)
            assert e.status_code == 404

    def test_raise_and_catch_base(self):
        """Test catching any exception with base class."""
        try:
            raise TokenLimitError("Too long", token_count=10000)
        except MCPWebError as e:
            assert isinstance(e, TokenLimitError)
            assert e.token_count == 10000


class TestExceptionChaining:
    """Test exception chaining and cause tracking."""

    def test_exception_with_cause(self):
        """Test exception chaining with __cause__."""
        try:
            try:
                raise ValueError("Original error")
            except ValueError as e:
                raise FetchError("Wrapped error") from e
        except FetchError as e:
            assert e.__cause__ is not None
            assert isinstance(e.__cause__, ValueError)
            assert "Original error" in str(e.__cause__)

    def test_format_exception_chain_single(self):
        """Test formatting single exception."""
        exc = FetchError("Simple error")
        formatted = format_exception_chain(exc)

        assert "FetchError" in formatted
        assert "Simple error" in formatted

    def test_format_exception_chain_multiple(self):
        """Test formatting exception chain."""
        try:
            try:
                raise NetworkError("Connection failed")
            except NetworkError as e:
                raise FetchError("Fetch failed") from e
        except FetchError as e:
            formatted = format_exception_chain(e)

            assert "FetchError" in formatted
            assert "NetworkError" in formatted
            assert "Caused by" in formatted


class TestExceptionInheritanceHierarchy:
    """Test exception inheritance relationships."""

    def test_fetch_error_hierarchy(self):
        """Test FetchError inheritance hierarchy."""
        assert issubclass(NetworkError, FetchError)
        assert issubclass(TimeoutError, FetchError)
        assert issubclass(HTTPError, FetchError)
        assert issubclass(FetchError, MCPWebError)

    def test_extraction_error_hierarchy(self):
        """Test ExtractionError inheritance hierarchy."""
        assert issubclass(ParseError, ExtractionError)
        assert issubclass(ExtractionError, MCPWebError)

    def test_summarization_error_hierarchy(self):
        """Test SummarizationError inheritance hierarchy."""
        assert issubclass(ProviderError, SummarizationError)
        assert issubclass(TokenLimitError, SummarizationError)
        assert issubclass(SummarizationError, MCPWebError)

    def test_security_error_hierarchy(self):
        """Test SecurityError inheritance hierarchy."""
        assert issubclass(ValidationError, SecurityError)
        assert issubclass(PromptInjectionError, SecurityError)
        assert issubclass(SecurityError, MCPWebError)

    def test_all_inherit_from_base(self):
        """Test that all exceptions inherit from MCPWebError."""
        exception_classes = [
            FetchError,
            NetworkError,
            TimeoutError,
            HTTPError,
            ExtractionError,
            ParseError,
            SummarizationError,
            ProviderError,
            TokenLimitError,
            SecurityError,
            ValidationError,
            PromptInjectionError,
            CacheError,
            ConfigurationError,
            BrowserError,
        ]

        for exc_class in exception_classes:
            assert issubclass(exc_class, MCPWebError)
            assert issubclass(exc_class, Exception)
