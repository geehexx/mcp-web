# Error Codes and Handling

**Version:** 0.1.0
**Last Updated:** 2025-10-16

---

## Overview

mcp-web uses structured error handling with clear error messages. Most errors are standard Python exceptions with descriptive messages logged via `structlog`.

---

## Error Categories

### 1. Configuration Errors

**Type:** `pydantic.ValidationError`
**Cause:** Invalid configuration values

#### CONFIG_001: Invalid Environment Variable Type

**Message:** `validation error for <SettingClass>`

**Cause:**

- Environment variable has wrong type
- Example: `MCP_WEB_FETCHER_TIMEOUT=abc` (should be integer)

**Solution:**

```bash
# Check type requirements in ENVIRONMENT_VARIABLES.md
export MCP_WEB_FETCHER_TIMEOUT=30  # Integer, not string
```

#### CONFIG_002: Missing Required Configuration

**Message:** `field required`

**Cause:**

- Required API key not set (for cloud providers)

**Solution:**

```bash
# For OpenAI
export OPENAI_API_KEY="sk-..."

# Or use local LLM
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
```

#### CONFIG_003: Out of Range Value

**Message:** `ensure this value is greater than <min>` or `ensure this value is less than <max>`

**Cause:**

- Configuration value outside allowed range
- Example: `MCP_WEB_SUMMARIZER_TEMPERATURE=3.0` (max is 2.0)

**Solution:**

```bash
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3  # Valid range: 0.0-2.0
```

---

### 2. Fetch Errors

**Type:** `httpx.HTTPError`, `playwright.Error`

#### FETCH_001: HTTP Request Failed

**Log Message:** `fetch_failed`

**Cause:**

- Network error
- DNS resolution failure
- Connection timeout

**Logged Fields:**

- `url`: The URL that failed
- `error`: Error description
- `method`: httpx or Playwright

**Solution:**

- Check network connectivity
- Verify URL is valid
- Increase timeout: `export MCP_WEB_FETCHER_TIMEOUT=60`

#### FETCH_002: HTTP Error Status

**Log Message:** `http_error_status`

**Cause:**

- 4xx: Client error (404 Not Found, 403 Forbidden)
- 5xx: Server error (500 Internal Server Error)

**Logged Fields:**

- `url`: The URL
- `status_code`: HTTP status code
- `fallback`: Whether Playwright fallback triggered

**Solution:**

- 404: Check URL is correct
- 403: Site may block scrapers, enable Playwright
- 5xx: Try again later, site may be down

#### FETCH_003: Playwright Timeout

**Log Message:** `playwright_timeout`

**Cause:**

- Page took too long to load
- Network idle condition not met

**Solution:**

```bash
export MCP_WEB_FETCHER_PLAYWRIGHT_TIMEOUT=120  # Increase from 60s
```

#### FETCH_004: robots.txt Disallowed

**Log Message:** `robots_txt_disallowed`

**Cause:**

- URL blocked by robots.txt rules
- `respect_robots_txt=true` (default)

**Solution:**

```bash
# Option 1: Respect robots.txt (recommended)
# Don't fetch from this URL

# Option 2: Override (not recommended)
export MCP_WEB_FETCHER_RESPECT_ROBOTS_TXT=false
```

---

### 3. Extraction Errors

**Type:** `ValueError`, `Exception`

#### EXTRACT_001: Empty Content

**Log Message:** `extraction_empty_content`

**Cause:**

- No main content found by trafilatura
- Page may be JavaScript-rendered (if Playwright disabled)
- Page structure not recognized

**Logged Fields:**

- `url`: The URL
- `html_length`: Length of HTML received

**Solution:**

- Enable Playwright fallback: `export MCP_WEB_FETCHER_ENABLE_FALLBACK=true`
- Check if URL requires authentication
- Some pages genuinely have no extractable content

#### EXTRACT_002: Malformed HTML

**Log Message:** `extraction_failed`

**Cause:**

- Invalid HTML structure
- Encoding issues

**Solution:**

- Usually recoverable, extraction will return partial content
- Check logs for specific error details

---

### 4. Chunking Errors

**Type:** `ValueError`

#### CHUNK_001: Invalid Chunk Size

**Log Message:** `invalid_chunk_size`

**Cause:**

- `chunk_size` too small (<10 tokens) or too large (>context window)

**Solution:**

```bash
export MCP_WEB_CHUNKER_CHUNK_SIZE=512  # Recommended: 256-1024
```

#### CHUNK_002: Document Too Large

**Log Message:** `document_too_large`

**Cause:**

- Document exceeds processing limits
- Very long article (>1M tokens)

**Solution:**

- Currently handled gracefully, processes first N chunks
- Future: Will support incremental processing

---

### 5. Summarization Errors

**Type:** `openai.APIError`, `httpx.HTTPError`

#### SUMM_001: API Key Invalid

**Log Message:** `llm_api_error`

**Cause:**

- Invalid or expired API key
- API key not set

**HTTP Status:** 401 Unauthorized

**Solution:**

```bash
# Verify key is correct
export OPENAI_API_KEY="sk-..."

# Or use local LLM
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
```

#### SUMM_002: Rate Limit Exceeded

**Log Message:** `rate_limit_exceeded`

**Cause:**

- Too many requests to LLM provider
- Exceeded API quota

**HTTP Status:** 429 Too Many Requests

**Solution:**

```bash
# Reduce concurrency
export MCP_WEB_FETCHER_MAX_CONCURRENT=3

# Add delays
export MCP_WEB_FETCHER_RETRY_DELAY=2.0

# Or use local LLM (no rate limits)
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
```

#### SUMM_003: Context Length Exceeded

**Log Message:** `context_length_exceeded`

**Cause:**

- Chunk too large for model's context window
- Model context: 8k, 16k, 32k, 128k tokens depending on model

**Solution:**

```bash
# Reduce chunk size
export MCP_WEB_CHUNKER_CHUNK_SIZE=512

# Or use model with larger context
export MCP_WEB_SUMMARIZER_MODEL="gpt-4-turbo"  # 128k context
```

#### SUMM_004: LLM Timeout

**Log Message:** `llm_timeout`

**Cause:**

- LLM API took too long to respond
- Network issues
- Model overloaded

**Solution:**

```bash
# Increase timeout
export MCP_WEB_SUMMARIZER_TIMEOUT=300

# Or use faster model
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"
```

#### SUMM_005: Model Not Found

**Log Message:** `model_not_found`

**Cause:**

- Model name incorrect
- Model not available for API key's tier
- Ollama: Model not pulled

**Solution:**

```bash
# For OpenAI - check model name
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"

# For Ollama - pull model first
ollama pull llama3.2:3b
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"
```

---

### 6. Cache Errors

**Type:** `OSError`, `PermissionError`

#### CACHE_001: Permission Denied

**Log Message:** `cache_permission_error`

**Cause:**

- No write permissions to cache directory
- Directory owned by different user

**Solution:**

```bash
# Change cache location
export MCP_WEB_CACHE_CACHE_DIR="$HOME/.cache/mcp-web"

# Or fix permissions
chmod 755 ~/.cache/mcp-web
```

#### CACHE_002: Disk Full

**Log Message:** `cache_disk_full`

**Cause:**

- Cache directory's disk is full
- Cache size exceeded `max_size`

**Solution:**

```bash
# Clear cache
python -m mcp_web.cli clear-cache

# Reduce max size
export MCP_WEB_CACHE_MAX_SIZE=$((500 * 1024 * 1024))  # 500 MB

# Reduce TTL
export MCP_WEB_CACHE_TTL=86400  # 1 day
```

---

### 7. Security Errors

**Type:** `SecurityError` (logged, not raised)

#### SEC_001: Prompt Injection Detected

**Log Level:** WARNING
**Log Message:** `prompt_injection_detected`

**Cause:**

- User input or fetched content contains injection patterns
- Examples: "ignore previous instructions", "you are now in developer mode"

**Logged Fields:**

- `pattern`: Matched pattern
- `text_preview`: First 100 chars of input

**Action:**

- Input sanitized automatically
- Dangerous patterns replaced with `[FILTERED]`

**User Action:**

- None required (handled automatically)
- Check summary for `[FILTERED]` markers

#### SEC_002: SSRF Attempt Detected

**Log Level:** WARNING
**Log Message:** `blocked_localhost_url` or `blocked_private_ip`

**Cause:**

- URL points to internal/private network
- Examples: `http://localhost`, `http://192.168.1.1`

**Action:**

- URL validation rejects the request
- Returns error to user

**User Action:**

- Only use public URLs
- Internal URLs are blocked for security

#### SEC_003: Output Validation Failed

**Log Level:** ERROR
**Log Message:** `unsafe_output_filtered`

**Cause:**

- LLM output contains sensitive information
- API keys, system prompts, file paths detected

**Action:**

- Output replaced with safe error message
- Original output logged for investigation

**User Response:**

- "Access denied for security reasons."

**User Action:**

- Retry with different query
- Check if URL content is malicious

---

### 8. Validation Errors

**Type:** `ValueError`

#### VAL_001: Invalid URL

**Log Message:** `invalid_url_scheme` or `invalid_url_no_domain`

**Cause:**

- URL missing http:// or https://
- URL has no domain
- Malformed URL

**Solution:**

```python
# Bad
summarize_urls(["example.com"])
summarize_urls(["file:///etc/passwd"])

# Good
summarize_urls(["https://example.com"])
```

#### VAL_002: Empty URL List

**Error Message:** "No valid URLs provided"

**Cause:**

- Empty URL list passed to `summarize_urls`
- All URLs invalid

**Solution:**

```python
# Provide at least one valid URL
summarize_urls(["https://example.com"])
```

---

## Error Handling Best Practices

### 1. Check Logs

All errors logged with structured context:

```bash
# Enable debug logging
export MCP_WEB_METRICS_LOG_LEVEL=DEBUG

# View logs
python -m mcp_web.mcp_server 2>&1 | tee mcp-web.log
```

### 2. Graceful Degradation

mcp-web handles errors gracefully:

- **Fetch fails**: Tries Playwright fallback
- **Extraction fails**: Returns partial content
- **One URL fails**: Continues with other URLs
- **LLM fails**: Returns error message, doesn't crash

### 3. Retry Logic

Built-in retries for transient errors:

```bash
export MCP_WEB_FETCHER_MAX_RETRIES=3
export MCP_WEB_FETCHER_RETRY_DELAY=2.0
```

### 4. Timeouts

All operations have timeouts:

```bash
export MCP_WEB_FETCHER_TIMEOUT=30
export MCP_WEB_FETCHER_PLAYWRIGHT_TIMEOUT=60
export MCP_WEB_SUMMARIZER_TIMEOUT=120
```

---

## Debugging

### Enable Verbose Logging

```bash
export MCP_WEB_METRICS_LOG_LEVEL=DEBUG
```

### Check Configuration

```python
from mcp_web import load_config

config = load_config()
print(config.model_dump_json(indent=2))
```

### Test Components

```bash
# Test fetch
python -m mcp_web.cli test-url https://example.com

# Test summarize (if CLI extended)
python -m mcp_web.cli test-summarize https://example.com
```

---

## Common Error Scenarios

### Scenario 1: "Everything fails"

**Symptoms:** All URLs fail to fetch

**Checklist:**

1. Network connected? `ping google.com`
2. Firewall blocking? Check firewall rules
3. Proxy required? Set `HTTP_PROXY` environment variable
4. DNS working? `nslookup example.com`

### Scenario 2: "Summaries empty or gibberish"

**Symptoms:** Summaries are very short or nonsensical

**Checklist:**

1. Check model: `echo $MCP_WEB_SUMMARIZER_MODEL`
2. Check API key valid: Test with OpenAI Playground
3. Local LLM running? `curl http://localhost:11434/api/tags`
4. Temperature too high? Try `export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3`

### Scenario 3: "Too slow"

**Symptoms:** Takes minutes per URL

**Checklist:**

1. Using cloud LLM or local? Local is slower
2. Playwright fallback triggering? Check logs
3. Large documents? Enable parallel: `export MCP_WEB_SUMMARIZER_PARALLEL_MAP=true`
4. Cache disabled? Enable: `export MCP_WEB_CACHE_ENABLED=true`

---

## Reporting Issues

### Information to Include

1. **Error message** from logs
2. **Configuration** (sanitize API keys!)
3. **URL** that failed (if applicable)
4. **Python version**: `python --version`
5. **mcp-web version**: `pip show mcp-web`
6. **OS**: macOS, Linux, Windows

### Example Issue Report

```text
**Error:** LLM timeout

**Configuration:**
- Provider: ollama
- Model: llama3.2:3b
- Timeout: 120s

**Logs:**
```

ERROR llm_timeout model=llama3.2:3b url=https://example.com

```text

**Environment:**
- Python: 3.11.5
- mcp-web: 0.1.0
- OS: macOS 14.0
```

---

## References

- **Architecture**: [../architecture/ARCHITECTURE.md](../architecture/ARCHITECTURE.md)
- **Security**: [../architecture/SECURITY_ARCHITECTURE.md](../architecture/SECURITY_ARCHITECTURE.md)
- **Configuration**: [CONFIGURATION.md](CONFIGURATION.md)
- **Environment Variables**: [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)

---

**Last Updated:** 2025-10-16
**Maintained by:** mcp-web core team
