"""Authentication and authorization for MCP server.

Implements OWASP LLM Top 10 2025 authentication requirements:
- API key authentication (bearer token)
- Rate limiting per identity
- Audit logging
- Secure defaults

References:
    - https://modelcontextprotocol.io/specification/draft/basic/authorization
    - https://owasp.org/www-project-top-10-for-large-language-model-applications/
"""

import os
import secrets
import time
from collections import deque
from dataclasses import dataclass

import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger()


@dataclass
class APIKey:
    """API key with metadata."""

    key: str
    name: str
    created_at: float
    rate_limit: int = 60  # requests per minute
    enabled: bool = True


class APIKeyAuthenticator:
    """API key authentication for MCP server.

    Implements bearer token authentication with:
    - API key validation
    - Rate limiting per key
    - Audit logging
    - Key management utilities

    Example:
        >>> authenticator = APIKeyAuthenticator()
        >>> authenticator.add_key("my-service", rate_limit=100)
        'sk-abc123...'
        >>> authenticator.authenticate("sk-abc123...")
        APIKey(key='sk-abc123...', name='my-service', ...)
    """

    def __init__(self, enable_auth: bool = True):
        """Initialize authenticator.

        Args:
            enable_auth: Enable authentication (default: True)
        """
        self.enable_auth = enable_auth
        self.keys: dict[str, APIKey] = {}
        self.rate_limiters: dict[str, deque[float]] = {}

        # Load API keys from environment
        self._load_keys_from_env()

        if self.enable_auth and not self.keys:
            logger.warning(
                "authentication_enabled_no_keys",
                message="Authentication enabled but no API keys configured",
            )

    def _load_keys_from_env(self) -> None:
        """Load API keys from environment variables."""
        # Single key: MCP_WEB_API_KEY
        single_key = os.getenv("MCP_WEB_API_KEY")
        if single_key:
            self.keys[single_key] = APIKey(
                key=single_key,
                name="default",
                created_at=time.time(),
                rate_limit=60,
                enabled=True,
            )
            logger.info("api_key_loaded", source="MCP_WEB_API_KEY")

        # Multiple keys: MCP_WEB_API_KEYS (comma-separated)
        multi_keys = os.getenv("MCP_WEB_API_KEYS")
        if multi_keys:
            for idx, key in enumerate(multi_keys.split(",")):
                key = key.strip()
                if key and key not in self.keys:
                    self.keys[key] = APIKey(
                        key=key,
                        name=f"key-{idx}",
                        created_at=time.time(),
                        rate_limit=60,
                        enabled=True,
                    )
            logger.info("api_keys_loaded", source="MCP_WEB_API_KEYS", count=len(self.keys))

    def generate_key(self) -> str:
        """Generate a cryptographically secure API key.

        Returns:
            API key in format sk-{32 hex chars}

        Example:
            >>> key = authenticator.generate_key()
            >>> key.startswith('sk-')
            True
            >>> len(key)
            35
        """
        # Generate 16 bytes (128 bits) of random data
        random_bytes = secrets.token_bytes(16)
        # Convert to hex string
        hex_string = random_bytes.hex()
        return f"sk-{hex_string}"

    def add_key(self, name: str, rate_limit: int = 60, enabled: bool = True) -> str:
        """Add a new API key.

        Args:
            name: Human-readable name for the key
            rate_limit: Requests per minute allowed (default: 60)
            enabled: Enable the key (default: True)

        Returns:
            Generated API key

        Example:
            >>> key = authenticator.add_key("my-app", rate_limit=100)
            >>> authenticator.validate_key(key)
            True
        """
        key = self.generate_key()
        self.keys[key] = APIKey(
            key=key,
            name=name,
            created_at=time.time(),
            rate_limit=rate_limit,
            enabled=enabled,
        )
        logger.info("api_key_created", name=name, rate_limit=rate_limit)
        return key

    def validate_key(self, key: str) -> bool:
        """Validate API key exists and is enabled.

        Args:
            key: API key to validate

        Returns:
            True if valid and enabled

        Example:
            >>> authenticator.validate_key("sk-invalid")
            False
        """
        api_key = self.keys.get(key)
        return api_key is not None and api_key.enabled

    def authenticate(self, bearer_token: str) -> APIKey | None:
        """Authenticate request with bearer token.

        Args:
            bearer_token: Bearer token from Authorization header

        Returns:
            APIKey if authentication successful, None otherwise

        Raises:
            ValueError: If rate limit exceeded

        Example:
            >>> api_key = authenticator.authenticate("sk-abc123...")
            >>> if api_key:
            ...     print(f"Authenticated as {api_key.name}")
        """
        if not self.enable_auth:
            # Authentication disabled - allow all requests
            return None

        # Extract key from "Bearer sk-..." format
        if bearer_token.startswith("Bearer "):
            key = bearer_token[7:].strip()
        else:
            key = bearer_token.strip()

        # Validate key exists and is enabled
        api_key = self.keys.get(key)
        if not api_key or not api_key.enabled:
            logger.warning(
                "authentication_failed",
                reason="invalid_key",
                key_prefix=key[:10] if key else None,
            )
            return None

        # Check rate limit
        if not self._check_rate_limit(key, api_key.rate_limit):
            logger.warning(
                "rate_limit_exceeded",
                key_name=api_key.name,
                rate_limit=api_key.rate_limit,
            )
            raise ValueError(f"Rate limit exceeded for key '{api_key.name}'")

        # Log successful authentication
        logger.info("authentication_success", key_name=api_key.name)

        return api_key

    def _check_rate_limit(self, key: str, limit: int) -> bool:
        """Check if request is within rate limit.

        Args:
            key: API key
            limit: Requests per minute allowed

        Returns:
            True if within limit, False if exceeded
        """
        now = time.time()
        window = 60.0  # 1 minute window

        # Initialize rate limiter for this key if needed
        if key not in self.rate_limiters:
            self.rate_limiters[key] = deque()

        requests = self.rate_limiters[key]

        # Remove requests outside the time window
        while requests and requests[0] < now - window:
            requests.popleft()

        # Check if limit exceeded
        if len(requests) >= limit:
            return False

        # Record this request
        requests.append(now)
        return True

    def get_rate_limit_stats(self, key: str) -> dict[str, int | float | str]:
        """Get rate limit statistics for a key.

        Args:
            key: API key

        Returns:
            Dictionary with current_requests, max_requests, time_until_reset
        """
        api_key = self.keys.get(key)
        if not api_key:
            return {
                "current_requests": 0,
                "max_requests": 0,
                "time_until_reset": 0.0,
            }

        now = time.time()
        window = 60.0

        if key not in self.rate_limiters:
            return {
                "current_requests": 0,
                "max_requests": api_key.rate_limit,
                "time_until_reset": 0.0,
            }

        requests = self.rate_limiters[key]

        # Remove old requests
        while requests and requests[0] < now - window:
            requests.popleft()

        time_until_reset = 0.0
        if requests:
            time_until_reset = max(0, window - (now - requests[0]))

        return {
            "current_requests": len(requests),
            "max_requests": api_key.rate_limit,
            "time_until_reset": time_until_reset,
        }

    def revoke_key(self, key: str) -> bool:
        """Revoke (disable) an API key.

        Args:
            key: API key to revoke

        Returns:
            True if revoked, False if key not found

        Example:
            >>> authenticator.revoke_key("sk-abc123...")
            True
        """
        api_key = self.keys.get(key)
        if not api_key:
            return False

        api_key.enabled = False
        logger.info("api_key_revoked", key_name=api_key.name)
        return True

    def list_keys(self) -> list[dict[str, str | int | bool | float]]:
        """List all API keys with metadata.

        Returns:
            List of key metadata dictionaries

        Example:
            >>> keys = authenticator.list_keys()
            >>> for key in keys:
            ...     print(f"{key['name']}: {key['key_prefix']}")
        """
        return [
            {
                "key_prefix": key[:10] + "...",
                "name": api_key.name,
                "rate_limit": api_key.rate_limit,
                "enabled": api_key.enabled,
                "created_at": api_key.created_at,
            }
            for key, api_key in self.keys.items()
        ]
