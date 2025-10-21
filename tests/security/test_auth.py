"""Authentication and authorization security tests.

Tests OWASP LLM Top 10 2025 authentication requirements.
"""

import pytest

from mcp_web.auth import APIKeyAuthenticator


class TestAPIKeyAuthenticator:
    """Test API key authentication."""

    @pytest.mark.security
    @pytest.mark.unit
    def test_generate_key_format(self):
        """Test API key generation format."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.generate_key()

        assert key.startswith("sk-")
        assert len(key) == 35  # sk- + 32 hex chars
        assert all(c in "0123456789abcdef-sk" for c in key)

    @pytest.mark.security
    @pytest.mark.unit
    def test_generate_key_uniqueness(self):
        """Test that generated keys are unique."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        keys = {authenticator.generate_key() for _ in range(100)}

        # All keys should be unique
        assert len(keys) == 100

    @pytest.mark.security
    @pytest.mark.unit
    def test_add_key(self):
        """Test adding API key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test-app", rate_limit=100)

        assert authenticator.validate_key(key)
        assert key in authenticator.keys
        assert authenticator.keys[key].name == "test-app"
        assert authenticator.keys[key].rate_limit == 100
        assert authenticator.keys[key].enabled is True

    @pytest.mark.security
    @pytest.mark.unit
    def test_validate_key_invalid(self):
        """Test validation of invalid key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        assert not authenticator.validate_key("sk-invalid")
        assert not authenticator.validate_key("")
        assert not authenticator.validate_key("not-a-key")

    @pytest.mark.security
    @pytest.mark.unit
    def test_authenticate_bearer_token(self):
        """Test authentication with bearer token."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-app")

        # Test with Bearer prefix
        api_key = authenticator.authenticate(f"Bearer {key}")
        assert api_key is not None
        assert api_key.name == "test-app"

        # Test without Bearer prefix
        api_key = authenticator.authenticate(key)
        assert api_key is not None

    @pytest.mark.security
    @pytest.mark.unit
    def test_authenticate_disabled(self):
        """Test authentication when disabled."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        # Should return None (authentication disabled)
        result = authenticator.authenticate("any-key")
        assert result is None

    @pytest.mark.security
    @pytest.mark.unit
    def test_authenticate_invalid_key(self):
        """Test authentication with invalid key."""
        authenticator = APIKeyAuthenticator(enable_auth=True)

        result = authenticator.authenticate("sk-invalid")
        assert result is None

    @pytest.mark.security
    @pytest.mark.unit
    def test_rate_limiting(self):
        """Test rate limiting enforcement."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-app", rate_limit=5)

        # First 5 requests should succeed
        for _ in range(5):
            api_key = authenticator.authenticate(key)
            assert api_key is not None

        # 6th request should fail
        with pytest.raises(ValueError, match="Rate limit exceeded"):
            authenticator.authenticate(key)

    @pytest.mark.security
    @pytest.mark.unit
    def test_rate_limit_window(self):
        """Test rate limit time window."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-app", rate_limit=2)

        # Use up rate limit
        authenticator.authenticate(key)
        authenticator.authenticate(key)

        # Should fail
        with pytest.raises(ValueError):
            authenticator.authenticate(key)

        # Manually clear old requests to simulate time passing
        authenticator.rate_limiters[key].clear()

        # Should succeed now
        api_key = authenticator.authenticate(key)
        assert api_key is not None

    @pytest.mark.security
    @pytest.mark.unit
    def test_rate_limit_stats(self):
        """Test rate limit statistics."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-app", rate_limit=10)

        # No requests yet
        stats = authenticator.get_rate_limit_stats(key)
        assert stats["current_requests"] == 0
        assert stats["max_requests"] == 10

        # Make some requests
        authenticator.authenticate(key)
        authenticator.authenticate(key)

        stats = authenticator.get_rate_limit_stats(key)
        assert stats["current_requests"] == 2
        assert stats["max_requests"] == 10

    @pytest.mark.security
    @pytest.mark.unit
    def test_revoke_key(self):
        """Test key revocation."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key = authenticator.add_key("test-app")

        # Key should work initially
        api_key = authenticator.authenticate(key)
        assert api_key is not None

        # Revoke key
        assert authenticator.revoke_key(key) is True

        # Key should not work after revocation
        result = authenticator.authenticate(key)
        assert result is None

    @pytest.mark.security
    @pytest.mark.unit
    def test_revoke_nonexistent_key(self):
        """Test revoking nonexistent key."""
        authenticator = APIKeyAuthenticator(enable_auth=False)

        assert authenticator.revoke_key("sk-nonexistent") is False

    @pytest.mark.security
    @pytest.mark.unit
    def test_list_keys(self):
        """Test listing API keys."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        authenticator.add_key("app1", rate_limit=50)
        authenticator.add_key("app2", rate_limit=100)

        keys = authenticator.list_keys()
        assert len(keys) == 2

        # Keys should be masked
        for key_info in keys:
            assert key_info["key_prefix"].endswith("...")
            assert len(key_info["key_prefix"]) < 35  # Full key length
            assert "name" in key_info
            assert "rate_limit" in key_info
            assert "enabled" in key_info

    @pytest.mark.security
    @pytest.mark.unit
    def test_load_from_env_single(self, monkeypatch):
        """Test loading single API key from environment."""
        test_key = "sk-test123abc"
        monkeypatch.setenv("MCP_WEB_API_KEY", test_key)

        authenticator = APIKeyAuthenticator(enable_auth=True)

        assert test_key in authenticator.keys
        assert authenticator.keys[test_key].name == "default"

    @pytest.mark.security
    @pytest.mark.unit
    def test_load_from_env_multiple(self, monkeypatch):
        """Test loading multiple API keys from environment."""
        keys = "sk-key1,sk-key2,sk-key3"
        monkeypatch.setenv("MCP_WEB_API_KEYS", keys)

        authenticator = APIKeyAuthenticator(enable_auth=True)

        assert "sk-key1" in authenticator.keys
        assert "sk-key2" in authenticator.keys
        assert "sk-key3" in authenticator.keys
        assert len(authenticator.keys) == 3

    @pytest.mark.security
    @pytest.mark.unit
    def test_concurrent_requests_per_key(self):
        """Test that different keys have independent rate limits."""
        authenticator = APIKeyAuthenticator(enable_auth=True)
        key1 = authenticator.add_key("app1", rate_limit=2)
        key2 = authenticator.add_key("app2", rate_limit=2)

        # Use up key1 limit
        authenticator.authenticate(key1)
        authenticator.authenticate(key1)

        # key1 should be rate limited
        with pytest.raises(ValueError):
            authenticator.authenticate(key1)

        # key2 should still work
        api_key = authenticator.authenticate(key2)
        assert api_key is not None
        assert api_key.name == "app2"


class TestSecurityDefaults:
    """Test secure default configurations."""

    @pytest.mark.security
    @pytest.mark.unit
    def test_auth_enabled_by_default(self):
        """Test that authentication is enabled by default."""
        authenticator = APIKeyAuthenticator()
        assert authenticator.enable_auth is True

    @pytest.mark.security
    @pytest.mark.unit
    def test_rate_limit_default(self):
        """Test default rate limit is reasonable."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test")

        api_key = authenticator.keys[key]
        assert api_key.rate_limit == 60  # 60 requests per minute

    @pytest.mark.security
    @pytest.mark.unit
    def test_key_enabled_by_default(self):
        """Test that keys are enabled by default."""
        authenticator = APIKeyAuthenticator(enable_auth=False)
        key = authenticator.add_key("test")

        assert authenticator.keys[key].enabled is True
