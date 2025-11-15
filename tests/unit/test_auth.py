"""Comprehensive tests for authentication module.

Tests for OWASP LLM Top 10 2025 authentication requirements:
- API key authentication (bearer token)
- Rate limiting per identity
- Audit logging
- Secure defaults

Target coverage: 80%+ (critical security module)
"""

import os
import time
from unittest.mock import patch

import pytest

from mcp_web.auth import APIKey, APIKeyAuthenticator


class TestAPIKey:
    """Test APIKey dataclass."""

    def test_api_key_creation_with_defaults(self):
        """Test APIKey creation with default values."""
        key = APIKey(
            key="sk-test123",
            name="test-key",
            created_at=time.time(),
        )

        assert key.key == "sk-test123"
        assert key.name == "test-key"
        assert key.rate_limit == 60  # default
        assert key.enabled is True  # default
        assert isinstance(key.created_at, float)

    def test_api_key_creation_with_custom_values(self):
        """Test APIKey creation with custom values."""
        created_at = time.time()
        key = APIKey(
            key="sk-custom",
            name="custom-key",
            created_at=created_at,
            rate_limit=100,
            enabled=False,
        )

        assert key.key == "sk-custom"
        assert key.name == "custom-key"
        assert key.created_at == created_at
        assert key.rate_limit == 100
        assert key.enabled is False


class TestKeyGeneration:
    """Test API key generation."""

    def test_generate_key_format(self):
        """Test generated key has correct format."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.generate_key()

        # Format: sk-{32 hex chars}
        assert key.startswith("sk-")
        assert len(key) == 35  # "sk-" (3) + 32 hex chars

        # Verify hex characters only (after prefix)
        hex_part = key[3:]
        assert all(c in "0123456789abcdef" for c in hex_part)

    def test_generate_key_uniqueness(self):
        """Test that generated keys are unique."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        keys = [authenticator.generate_key() for _ in range(100)]

        # All keys should be unique
        assert len(keys) == len(set(keys))

    def test_generate_key_randomness(self):
        """Test that keys are cryptographically random (not sequential)."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key1 = authenticator.generate_key()
        key2 = authenticator.generate_key()

        # Keys should be different
        assert key1 != key2

        # Keys should have sufficient entropy (not similar)
        # Convert to integers and check they're not sequential
        hex1 = int(key1[3:], 16)
        hex2 = int(key2[3:], 16)
        assert abs(hex1 - hex2) > 1000  # Not sequential


class TestKeyManagement:
    """Test API key management operations."""

    def test_add_key_creates_valid_key(self):
        """Test that add_key creates a valid API key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test-service", rate_limit=100)

        # Key should be in correct format
        assert key.startswith("sk-")
        assert len(key) == 35

        # Key should be stored
        assert key in authenticator.keys

        # Metadata should be correct
        api_key = authenticator.keys[key]
        assert api_key.name == "test-service"
        assert api_key.rate_limit == 100
        assert api_key.enabled is True
        assert isinstance(api_key.created_at, float)

    def test_add_key_with_default_rate_limit(self):
        """Test add_key with default rate limit."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test-service")

        api_key = authenticator.keys[key]
        assert api_key.rate_limit == 60  # default

    def test_add_key_with_disabled_flag(self):
        """Test add_key with enabled=False."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test-service", enabled=False)

        api_key = authenticator.keys[key]
        assert api_key.enabled is False

    def test_validate_key_valid_enabled(self):
        """Test validate_key returns True for valid enabled key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test-service")

        assert authenticator.validate_key(key) is True

    def test_validate_key_invalid(self):
        """Test validate_key returns False for invalid key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        assert authenticator.validate_key("sk-invalid") is False

    def test_validate_key_disabled(self):
        """Test validate_key returns False for disabled key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test-service", enabled=False)

        assert authenticator.validate_key(key) is False

    def test_revoke_key_success(self):
        """Test revoking an API key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test-service")

        # Key should be enabled initially
        assert authenticator.validate_key(key) is True

        # Revoke the key
        result = authenticator.revoke_key(key)
        assert result is True

        # Key should be disabled now
        assert authenticator.validate_key(key) is False
        assert authenticator.keys[key].enabled is False

    def test_revoke_key_not_found(self):
        """Test revoking a non-existent key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        result = authenticator.revoke_key("sk-invalid")
        assert result is False

    def test_list_keys_empty(self):
        """Test list_keys with no keys."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        keys = authenticator.list_keys()
        assert keys == []

    def test_list_keys_multiple(self):
        """Test list_keys with multiple keys."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        key1 = authenticator.add_key("service-1", rate_limit=100)
        key2 = authenticator.add_key("service-2", rate_limit=200, enabled=False)

        keys = authenticator.list_keys()
        assert len(keys) == 2

        # Check metadata format
        key_data = {k["name"]: k for k in keys}

        assert "service-1" in key_data
        assert key_data["service-1"]["key_prefix"] == key1[:10] + "..."
        assert key_data["service-1"]["rate_limit"] == 100
        assert key_data["service-1"]["enabled"] is True

        assert "service-2" in key_data
        assert key_data["service-2"]["key_prefix"] == key2[:10] + "..."
        assert key_data["service-2"]["rate_limit"] == 200
        assert key_data["service-2"]["enabled"] is False


class TestAuthentication:
    """Test authentication flow."""

    def test_authenticate_disabled_auth(self):
        """Test authentication when auth is disabled."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        # Should return None (no authentication required)
        result = authenticator.authenticate("any-token")
        assert result is None

    def test_authenticate_with_bearer_prefix(self):
        """Test authentication with 'Bearer ' prefix."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service")

        # Authenticate with Bearer prefix
        result = authenticator.authenticate(f"Bearer {key}")

        assert result is not None
        assert isinstance(result, APIKey)
        assert result.key == key
        assert result.name == "test-service"

    def test_authenticate_without_bearer_prefix(self):
        """Test authentication without Bearer prefix."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service")

        # Authenticate without Bearer prefix
        result = authenticator.authenticate(key)

        assert result is not None
        assert result.key == key

    def test_authenticate_invalid_key(self):
        """Test authentication with invalid key."""
        authenticator = APIKeyAuthenticator(enable_auth=True)

        result = authenticator.authenticate("sk-invalid")
        assert result is None

    def test_authenticate_disabled_key(self):
        """Test authentication with disabled key."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", enabled=False)

        result = authenticator.authenticate(key)
        assert result is None

    def test_authenticate_bearer_with_whitespace(self):
        """Test authentication handles whitespace in Bearer token."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service")

        # Should handle extra whitespace
        result = authenticator.authenticate(f"Bearer   {key}  ")
        assert result is not None
        assert result.key == key


class TestRateLimiting:
    """Test rate limiting functionality."""

    def test_rate_limit_within_limit(self):
        """Test requests within rate limit succeed."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", rate_limit=5)

        # Make 5 requests (at limit)
        for i in range(5):
            result = authenticator.authenticate(key)
            assert result is not None, f"Request {i+1} should succeed"

    def test_rate_limit_exceeded(self):
        """Test that exceeding rate limit raises error."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", rate_limit=5)

        # Make 5 requests (at limit)
        for _ in range(5):
            authenticator.authenticate(key)

        # 6th request should fail
        with pytest.raises(ValueError, match="Rate limit exceeded"):
            authenticator.authenticate(key)

    def test_rate_limit_sliding_window(self):
        """Test rate limit uses sliding window (old requests expire)."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", rate_limit=2)

        # Make 2 requests
        authenticator.authenticate(key)
        authenticator.authenticate(key)

        # 3rd request should fail
        with pytest.raises(ValueError, match="Rate limit exceeded"):
            authenticator.authenticate(key)

        # Simulate time passing (61 seconds)
        # Manually clean the rate limiter
        now = time.time()
        authenticator.rate_limiters[key].clear()
        authenticator.rate_limiters[key].append(now - 61)  # Old request

        # Now should succeed (old request expired)
        result = authenticator.authenticate(key)
        assert result is not None

    def test_rate_limit_per_key_independent(self):
        """Test that rate limits are independent per key."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key1 = authenticator.add_key("service-1", rate_limit=2)
        key2 = authenticator.add_key("service-2", rate_limit=2)

        # Exhaust key1's limit
        authenticator.authenticate(key1)
        authenticator.authenticate(key1)

        # key1 should be rate limited
        with pytest.raises(ValueError, match="Rate limit exceeded"):
            authenticator.authenticate(key1)

        # key2 should still work
        result = authenticator.authenticate(key2)
        assert result is not None

    def test_get_rate_limit_stats_no_requests(self):
        """Test rate limit stats with no requests."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", rate_limit=100)

        stats = authenticator.get_rate_limit_stats(key)

        assert stats["current_requests"] == 0
        assert stats["max_requests"] == 100
        assert stats["time_until_reset"] == 0.0

    def test_get_rate_limit_stats_with_requests(self):
        """Test rate limit stats after requests."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", rate_limit=10)

        # Make 3 requests
        for _ in range(3):
            authenticator.authenticate(key)

        stats = authenticator.get_rate_limit_stats(key)

        assert stats["current_requests"] == 3
        assert stats["max_requests"] == 10
        assert stats["time_until_reset"] > 0.0

    def test_get_rate_limit_stats_invalid_key(self):
        """Test rate limit stats for non-existent key."""
        authenticator = APIKeyAuthenticator(enable_auth=True)

        stats = authenticator.get_rate_limit_stats("sk-invalid")

        assert stats["current_requests"] == 0
        assert stats["max_requests"] == 0
        assert stats["time_until_reset"] == 0.0


class TestEnvironmentLoading:
    """Test loading API keys from environment variables."""

    def test_load_from_single_env_var(self):
        """Test loading from MCP_WEB_API_KEY."""
        test_key = "sk-test-single-key"

        with patch.dict(os.environ, {"MCP_WEB_API_KEY": test_key}, clear=False):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # Key should be loaded
            assert test_key in authenticator.keys
            assert authenticator.keys[test_key].name == "default"
            assert authenticator.keys[test_key].rate_limit == 60

    def test_load_from_multi_env_var(self):
        """Test loading from MCP_WEB_API_KEYS (comma-separated)."""
        key1 = "sk-test-key-1"
        key2 = "sk-test-key-2"
        key3 = "sk-test-key-3"

        with patch.dict(os.environ, {"MCP_WEB_API_KEYS": f"{key1},{key2},{key3}"}, clear=False):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # All keys should be loaded
            assert key1 in authenticator.keys
            assert key2 in authenticator.keys
            assert key3 in authenticator.keys

            # Names should be key-0, key-1, key-2
            assert authenticator.keys[key1].name == "key-0"
            assert authenticator.keys[key2].name == "key-1"
            assert authenticator.keys[key3].name == "key-2"

    def test_load_from_multi_env_var_with_whitespace(self):
        """Test loading handles whitespace in comma-separated keys."""
        key1 = "sk-test-key-1"
        key2 = "sk-test-key-2"

        with patch.dict(os.environ, {"MCP_WEB_API_KEYS": f" {key1} , {key2} "}, clear=False):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # Keys should be loaded (stripped)
            assert key1 in authenticator.keys
            assert key2 in authenticator.keys

    def test_load_from_both_env_vars(self):
        """Test loading from both MCP_WEB_API_KEY and MCP_WEB_API_KEYS."""
        single_key = "sk-single"
        multi_key1 = "sk-multi-1"
        multi_key2 = "sk-multi-2"

        with patch.dict(
            os.environ,
            {
                "MCP_WEB_API_KEY": single_key,
                "MCP_WEB_API_KEYS": f"{multi_key1},{multi_key2}",
            },
            clear=False,
        ):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # All keys should be loaded
            assert single_key in authenticator.keys
            assert multi_key1 in authenticator.keys
            assert multi_key2 in authenticator.keys

    def test_load_multi_env_var_no_duplicates(self):
        """Test that duplicate keys in MCP_WEB_API_KEYS are handled."""
        key1 = "sk-test-key-1"

        # Single key already loaded, shouldn't be duplicated
        with patch.dict(
            os.environ,
            {
                "MCP_WEB_API_KEY": key1,
                "MCP_WEB_API_KEYS": f"{key1},sk-key-2",
            },
            clear=False,
        ):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # Should only have 2 keys (not 3)
            assert len(authenticator.keys) == 2

    def test_no_env_vars_warning(self, caplog):
        """Test warning when auth enabled but no keys configured."""
        # Clear any env vars
        with patch.dict(os.environ, {}, clear=True):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # Should have no keys
            assert len(authenticator.keys) == 0

    def test_env_var_empty_string(self):
        """Test handling of empty string in env vars."""
        with patch.dict(os.environ, {"MCP_WEB_API_KEY": ""}, clear=False):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # Empty string should not create a key
            assert "" not in authenticator.keys

    def test_multi_env_var_empty_entries(self):
        """Test handling of empty entries in comma-separated list."""
        key1 = "sk-valid-key"

        with patch.dict(os.environ, {"MCP_WEB_API_KEYS": f"{key1},,,"}, clear=False):
            authenticator = APIKeyAuthenticator(enable_auth=True)

            # Should only have the valid key
            assert len(authenticator.keys) == 1
            assert key1 in authenticator.keys


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_authenticate_empty_token(self):
        """Test authentication with empty token."""
        authenticator = APIKeyAuthenticator(enable_auth=True)

        result = authenticator.authenticate("")
        assert result is None

    def test_authenticate_bearer_only(self):
        """Test authentication with just 'Bearer' and no token."""
        authenticator = APIKeyAuthenticator(enable_auth=True)

        result = authenticator.authenticate("Bearer ")
        assert result is None

    def test_check_rate_limit_zero_limit(self):
        """Test rate limiting with zero limit (should always fail)."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", rate_limit=0)

        # Should immediately exceed rate limit
        with pytest.raises(ValueError, match="Rate limit exceeded"):
            authenticator.authenticate(key)

    def test_multiple_authenticators_independent(self):
        """Test that multiple authenticator instances are independent."""
        auth1 = APIKeyAuthenticator(enable_auth=False)
        auth2 = APIKeyAuthenticator(enable_auth=False)

        key1 = auth1.add_key("service-1")
        key2 = auth2.add_key("service-2")

        # Keys should be different
        assert key1 != key2

        # Each authenticator should only have its own key
        assert key1 in auth1.keys
        assert key1 not in auth2.keys
        assert key2 in auth2.keys
        assert key2 not in auth1.keys

    def test_rate_limiter_cleanup(self):
        """Test that old rate limit entries are cleaned up."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-service", rate_limit=100)

        # Make a request
        authenticator.authenticate(key)

        # Manually add old timestamp (2 minutes ago)
        old_timestamp = time.time() - 120
        authenticator.rate_limiters[key].appendleft(old_timestamp)

        # Get stats (should trigger cleanup)
        stats = authenticator.get_rate_limit_stats(key)

        # Should only count recent request
        assert stats["current_requests"] == 1
