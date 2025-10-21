# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in mcp-web, please report it responsibly by emailing the maintainers. **Do not create public GitHub issues for security vulnerabilities.**

**Reporting Process:**

1. **Email:** Send details to [security email - to be configured]
2. **Include:** Description, steps to reproduce, potential impact, affected versions
3. **Response Time:** We aim to respond within 48 hours
4. **Disclosure:** We will coordinate public disclosure after a fix is available

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.3.x   | :white_check_mark: |
| < 0.3.0 | :x:                |

## Security Features

### OWASP LLM Top 10 2025 Compliance

mcp-web implements defenses against the OWASP LLM Top 10 vulnerabilities:

#### LLM01: Prompt Injection

- **Pattern-based detection**: 50+ dangerous instruction patterns (English + multilingual)
- **Typoglycemia detection**: Catches scrambled keyword attacks
- **Unicode normalization**: Prevents lookalike character obfuscation
- **HTML sanitization**: Removes script tags and event handlers
- **Structured prompts**: Clear separation between system instructions and user data
- **Confidence scoring**: 0.0-1.0 scale for detection certainty

**Configuration:**

```python
from mcp_web.security import PromptInjectionFilter

filter = PromptInjectionFilter()
is_dangerous, confidence, patterns = filter.detect_injection(user_input)

if is_dangerous:
    sanitized = filter.sanitize(user_input)
```

#### LLM02: Sensitive Information Disclosure

- **API key masking**: Never log full API keys (prefix only)
- **Structured logging**: Context-aware logging without sensitive data
- **Output filtering**: Removes API keys, tokens, and credentials from responses

#### LLM05: Improper Output Handling

- **Output validation**: Scans for system prompt leakage, API key exposure
- **Length limits**: Enforces maximum output size (10,000 chars default)
- **Safe filtering**: Replaces unsafe outputs with secure error messages

**Configuration:**

```python
from mcp_web.security import OutputValidator

validator = OutputValidator(max_output_length=10000)
if validator.validate(llm_output):
    return llm_output
else:
    return validator.filter_response(llm_output)
```

#### LLM07: System Prompt Leakage

- **Prompt boundary enforcement**: Clear delimiters (`---`) separate system/user data
- **Security rules**: Explicit instructions to never reveal system prompt
- **Output scanning**: Detects leaked instructions, internal reasoning

#### LLM10: Unbounded Consumption

- **Rate limiting**: Token bucket algorithm, 60 requests/minute default
- **Concurrent limits**: Semaphore-based (10 concurrent requests default)
- **Timeouts**: 120-second operation timeout
- **Token limits**: 10,000 tokens per request default

**Configuration:**

```python
from mcp_web.security import ConsumptionLimits

async with ConsumptionLimits(
    max_tokens=10000,
    max_concurrent=10,
    max_requests_per_minute=60,
    timeout_seconds=120
):
    result = await operation()
```

### Authentication & Authorization

#### API Key Authentication (v0.3.0)

- **Bearer token**: `Authorization: Bearer sk-...` header support
- **Rate limiting per key**: Independent limits for each API key
- **Key management**: Generate, validate, revoke API keys
- **Audit logging**: All authentication events logged

**Setup:**

```bash
# Single API key
export MCP_WEB_API_KEY=sk-your-secret-key

# Multiple API keys (comma-separated)
export MCP_WEB_API_KEYS=sk-key1,sk-key2,sk-key3

# Disable authentication (default: enabled)
export MCP_WEB_AUTH_ENABLED=false
```

**Usage:**

```python
from mcp_web.auth import APIKeyAuthenticator

authenticator = APIKeyAuthenticator(enable_auth=True)

# Generate new key
key = authenticator.add_key("my-app", rate_limit=100)

# Authenticate request
api_key = authenticator.authenticate(f"Bearer {key}")
if api_key:
    print(f"Authenticated as {api_key.name}")
```

#### OAuth 2.1 Support (Planned for v0.4.0)

Future versions will support OAuth 2.1 with PKCE for production deployments. See [MCP Authorization Specification](https://modelcontextprotocol.io/specification/draft/basic/authorization).

### Additional Security Measures

#### URL Validation (SSRF Prevention)

- **Protocol whitelist**: Only `http://` and `https://` allowed
- **Localhost blocking**: Prevents access to `127.0.0.1`, `localhost`, `::1`
- **Private IP blocking**: Blocks `10.x`, `192.168.x`, `172.x` ranges

#### Content Sanitization

- **HTML stripping**: Removes `<script>`, `<style>`, event handlers
- **JavaScript removal**: Filters `javascript:` links
- **Character repetition limiting**: Prevents DoS via repeated characters
- **Length enforcement**: Maximum input length (10,000 chars default)

## Security Testing

### Test Suite

- **Unit tests**: 50+ security-specific tests
- **OWASP coverage**: Comprehensive tests for LLM01, LLM02, LLM05, LLM07, LLM10
- **Attack scenarios**: Multilingual, Unicode, XSS, typoglycemia attacks

**Run security tests:**

```bash
# All security tests
uv run pytest tests/security/ -m security

# Specific OWASP tests
uv run pytest tests/security/test_owasp_llm_top10.py -v

# Authentication tests
uv run pytest tests/security/test_auth.py -v
```

### Static Analysis

```bash
# Bandit (security vulnerability scanner)
uv run bandit -r src/ -ll

# Semgrep (pattern-based security rules)
uv run semgrep --config=auto src/
```

### Garak Integration (Planned)

Future versions will integrate [Garak](https://github.com/NVIDIA/garak), an LLM vulnerability scanner, for comprehensive adversarial testing.

## Security Best Practices

### For Developers

1. **Never hardcode secrets**: Use environment variables or secure vaults
2. **Validate all inputs**: User data, URLs, file paths must be validated
3. **Use structured prompts**: Separate system instructions from user data
4. **Log securely**: Never log API keys, passwords, or PII
5. **Test security**: Write tests for injection, XSS, SSRF scenarios
6. **Review dependencies**: Regularly update and audit dependencies

### For Users/Deployers

1. **Enable authentication**: Set `MCP_WEB_API_KEY` in production
2. **Use HTTPS**: Always use encrypted transport
3. **Rate limit**: Configure appropriate rate limits for your use case
4. **Monitor logs**: Watch for authentication failures and suspicious patterns
5. **Update regularly**: Keep mcp-web updated for security fixes
6. **Principle of least privilege**: Grant minimum necessary permissions

## Known Limitations

1. **Prompt injection is an arms race**: No defense is 100% effective
2. **Pattern-based detection**: ~90% effective but can be bypassed with novel techniques
3. **Local deployment focus**: OAuth 2.1 deferred to v0.4.0
4. **No ML-based detection**: Future enhancement for higher accuracy

## Security Roadmap

### v0.3.0 (Current)

- [x] Prompt injection detection (pattern-based)
- [x] API key authentication
- [x] Rate limiting
- [x] Output validation
- [x] OWASP LLM Top 10 test coverage

### v0.4.0 (Planned)

- [ ] OAuth 2.1 + PKCE support
- [ ] ML-based prompt injection detection (95%+ accuracy)
- [ ] Garak vulnerability scanner integration
- [ ] Advanced sandboxing (containers, seccomp)
- [ ] Security monitoring and alerting

## References

- [OWASP LLM Top 10 2025](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices)
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Adversa AI MCP Security Top 25](https://adversa.ai/mcp-security-top-25-mcp-vulnerabilities/)
- [OWASP LLM01: Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)

## Changelog

### 2025-10-21: Phase 0 Security Hardening Complete

- Implemented prompt injection detection and sanitization
- Added API key authentication with rate limiting
- Created comprehensive OWASP LLM Top 10 test suite
- Documented security architecture and best practices
- Achieved 90%+ security test coverage

---

**Last Updated:** 2025-10-21
**Version:** 0.3.0
