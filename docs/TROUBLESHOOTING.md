# MCP-Web Troubleshooting Guide

**Last Updated:** 2025-11-15
**Version:** mcp-web 0.2.0

This guide helps you diagnose and resolve common issues with MCP-Web.

---

## Table of Contents

- [Quick Diagnostics](#quick-diagnostics)
- [Installation Issues](#installation-issues)
- [Configuration Problems](#configuration-problems)
- [Network & Connection Errors](#network--connection-errors)
- [LLM Provider Issues](#llm-provider-issues)
- [Performance Problems](#performance-problems)
- [Cache Issues](#cache-issues)
- [Security & Validation Errors](#security--validation-errors)
- [Debugging Procedures](#debugging-procedures)

---

## Quick Diagnostics

### Run Health Check

```bash
# Check if MCP-Web is properly installed
python -c "from mcp_web import __version__, Config; print(f'Version: {__version__}'); Config()"
```

**Expected output:**
```
Version: 0.2.0
```

**If this fails, see [Installation Issues](#installation-issues)**.

---

### Check LLM Provider Connectivity

```python
import asyncio
from mcp_web import Config
from mcp_web.summarizer import Summarizer

async def test_llm():
    config = Config()
    summarizer = Summarizer(config)

    # Test with simple text
    from mcp_web.chunker import Chunk
    chunks = [Chunk(text="Hello, world!", tokens=3, start_pos=0, end_pos=13)]

    async for part in summarizer.summarize_chunks(chunks):
        print(f"LLM response: {part}")

asyncio.run(test_llm())
```

**If this hangs or fails, see [LLM Provider Issues](#llm-provider-issues)**.

---

## Installation Issues

### Problem: `ModuleNotFoundError: No module named 'mcp_web'`

**Cause:** MCP-Web not installed or not in Python path.

**Solution:**

```bash
# Verify Python version (must be 3.10+)
python --version

# Install MCP-Web
pip install mcp-web

# Or if using uv
uv pip install mcp-web

# Verify installation
python -c "import mcp_web; print(mcp_web.__version__)"
```

---

### Problem: `ImportError: cannot import name 'create_server'`

**Cause:** Partial installation or version mismatch.

**Solution:**

```bash
# Uninstall completely
pip uninstall -y mcp-web

# Clear pip cache
pip cache purge

# Reinstall
pip install --no-cache-dir mcp-web

# Verify
python -c "from mcp_web import create_server; print('OK')"
```

---

### Problem: Playwright installation fails

**Symptoms:**
```
ERROR: Could not install packages due to an OSError:
playwright: command not found
```

**Solution for Linux (Ubuntu/Debian):**
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    libglib2.0-0 libnss3 libnspr4 libdbus-1-3 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libasound2

# Install Playwright
pip install playwright
playwright install chromium
```

**Solution for macOS:**
```bash
# Playwright usually works out-of-box on macOS
brew install python@3.11  # If needed
pip install playwright
playwright install chromium
```

**Solution for Windows:**
```powershell
# Run as Administrator
pip install playwright
playwright install chromium
```

**Alternative: Disable Playwright**
```python
config = Config()
config.fetcher.enable_fallback = False  # Use httpx only
```

---

### Problem: Permission denied errors during installation

**Cause:** Installing to system Python without sudo.

**Solution:**

```bash
# Option 1: Use --user flag
pip install --user mcp-web

# Option 2: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install mcp-web

# Option 3: Use uv (recommended)
uv venv
source .venv/bin/activate
uv pip install mcp-web
```

---

## Configuration Problems

### Problem: `ValidationError: 1 validation error for Config`

**Symptoms:**
```python
pydantic.error_wrappers.ValidationError: 1 validation error for Config
fetcher -> timeout
  value is not a valid integer (type=type_error.integer)
```

**Cause:** Invalid configuration value.

**Solution:**

```python
# Check your configuration
from mcp_web import Config

try:
    config = Config()
except Exception as e:
    print(f"Config error: {e}")

# Fix: Ensure correct types
config.fetcher.timeout = 30  # int, not string
config.cache.enabled = True  # bool, not string
```

**For environment variables:**
```bash
# Wrong
export MCP_WEB_FETCHER_TIMEOUT="thirty"  # ❌ String

# Correct
export MCP_WEB_FETCHER_TIMEOUT=30  # ✓ Integer
```

---

### Problem: Environment variables not being read

**Symptoms:** Configuration uses defaults despite setting env vars.

**Debugging:**
```bash
# Check if variable is set
echo $MCP_WEB_FETCHER_TIMEOUT

# Check all MCP_WEB variables
env | grep MCP_WEB
```

**Common issues:**

**1. Wrong prefix:**
```bash
# Wrong
export FETCHER_TIMEOUT=30  # ❌ Missing prefix

# Correct
export MCP_WEB_FETCHER_TIMEOUT=30  # ✓ With prefix
```

**2. Nested settings:**
```bash
# For nested settings, use double underscore
export MCP_WEB_FETCHER__HEADERS='{"User-Agent":"MyBot"}'
```

**3. Variable not exported:**
```bash
# Wrong
MCP_WEB_FETCHER_TIMEOUT=30  # ❌ Not exported
python script.py

# Correct
export MCP_WEB_FETCHER_TIMEOUT=30  # ✓ Exported
python script.py
```

---

### Problem: Configuration file not found (v0.3.0+)

**Note:** YAML configuration support planned for v0.3.0.

**Current workaround:**
```python
# Use Python-based configuration
from mcp_web import Config
from mcp_web.config import FetcherSettings

config = Config()
config.fetcher = FetcherSettings(
    timeout=60,
    max_concurrent=10,
)
```

---

## Network & Connection Errors

### Problem: `ConnectionError: Failed to fetch <url>`

**Causes:**
1. Network connectivity
2. Firewall blocking
3. Invalid URL
4. Rate limiting
5. Server down

**Diagnostic steps:**

```bash
# Test basic connectivity
curl -I https://example.com

# Test from Python
python -c "import httpx; print(httpx.get('https://example.com').status_code)"
```

**Solution 1: Check network**
```bash
# Ping test
ping example.com

# DNS test
nslookup example.com

# Check proxy settings
echo $HTTP_PROXY
echo $HTTPS_PROXY
```

**Solution 2: Configure proxy**
```python
config.fetcher.proxy = "http://proxy.company.com:8080"

# Or via environment
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
```

**Solution 3: Increase timeout**
```python
config.fetcher.timeout = 60  # Default: 30
```

---

### Problem: `TimeoutError: Request timed out after 30 seconds`

**Cause:** Slow server or network.

**Solution:**

```python
# Increase timeout
config.fetcher.timeout = 120  # 2 minutes

# Or via environment
export MCP_WEB_FETCHER_TIMEOUT=120
```

**For Playwright (JavaScript-heavy sites):**
```python
config.browser.page_timeout = 60000  # 60 seconds in milliseconds
```

---

### Problem: `SSL: CERTIFICATE_VERIFY_FAILED`

**Cause:** SSL certificate issues.

**Solution 1: Update CA certificates (recommended)**
```bash
# macOS
brew install ca-certificates

# Ubuntu/Debian
sudo apt-get install ca-certificates
sudo update-ca-certificates
```

**Solution 2: Disable SSL verification (NOT RECOMMENDED)**
```python
# Only for development/testing!
config.fetcher.verify_ssl = False
```

---

### Problem: `403 Forbidden` or `429 Too Many Requests`

**Cause:** Rate limiting or blocked user agent.

**Solution 1: Custom User-Agent**
```python
config.fetcher.headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
}
```

**Solution 2: Add delays**
```python
import asyncio

urls = [...]
for url in urls:
    result = await pipeline.summarize_urls([url])
    await asyncio.sleep(2)  # 2 second delay
```

**Solution 3: Use Playwright (appears more human-like)**
```python
config.fetcher.force_playwright = True  # Always use browser
```

---

## LLM Provider Issues

### Problem: `openai.AuthenticationError: Incorrect API key`

**Cause:** Missing or invalid OpenAI API key.

**Solution:**

```bash
# Set API key
export OPENAI_API_KEY=sk-your-actual-key-here

# Verify it's set
echo $OPENAI_API_KEY

# Test directly with OpenAI
python -c "from openai import OpenAI; client = OpenAI(); print(client.models.list())"
```

**Check key validity:**
- Visit https://platform.openai.com/api-keys
- Verify key is active
- Check billing status

---

### Problem: `Connection refused` with Ollama

**Symptoms:**
```
httpx.ConnectError: [Errno 61] Connection refused
```

**Solution:**

```bash
# Check if Ollama is running
curl http://localhost:11434/api/version

# If not running, start it
ollama serve

# In another terminal, pull a model
ollama pull llama3.2

# Test
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello"
}'
```

**Common ports:**
- Ollama: `http://localhost:11434`
- LM Studio: `http://localhost:1234`
- LocalAI: `http://localhost:8080`

---

### Problem: `ModelNotFoundError: model 'gpt-4' does not exist`

**Cause:** Typo in model name or model not available.

**Solution:**

```python
# Check available models
from openai import OpenAI
client = OpenAI()
models = client.models.list()
for model in models:
    print(model.id)

# Use correct model name
config.summarizer.model = "gpt-4o-mini"  # Not "gpt-4-mini"
```

**Common model names:**
- OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`
- Ollama: `llama3.2`, `mistral`, `mixtral`

---

### Problem: Slow LLM responses

**Symptoms:** Summarization takes >60 seconds per page.

**Causes:**
1. Large chunks
2. Slow model
3. Network latency (cloud LLM)
4. Token limits

**Solutions:**

**1. Reduce chunk size:**
```python
config.chunker.chunk_size = 4000  # Default: 8000
```

**2. Use faster model:**
```python
# Instead of gpt-4
config.summarizer.model = "gpt-4o-mini"  # Much faster, cheaper

# Or use local LLM
config.summarizer.provider = "ollama"
config.summarizer.model = "llama3.2"  # Very fast locally
```

**3. Enable streaming:**
```python
# Streaming is enabled by default
async for chunk in summarizer.summarize_chunks(chunks):
    print(chunk, end="", flush=True)  # Print as it arrives
```

---

### Problem: `RateLimitError: Rate limit exceeded`

**Cause:** Too many API requests.

**Solution:**

**1. Add delays:**
```python
import asyncio
await asyncio.sleep(1)  # 1 second between requests
```

**2. Reduce concurrency:**
```python
config.fetcher.max_concurrent = 1  # Process one at a time
```

**3. Use caching:**
```python
config.cache.enabled = True  # Default, but verify
```

**4. Upgrade API tier** (OpenAI/Anthropic):
- Check usage limits
- Consider paid tier

---

## Performance Problems

### Problem: Slow summarization (>60 seconds per page)

**Diagnostic:**
```python
# Enable profiling
from mcp_web.metrics import MetricsCollector

metrics = MetricsCollector(config.metrics)

# Check where time is spent
stats = metrics.get_statistics()
print(stats)
```

**Optimization checklist:**

- [ ] **Enable caching** (fastest: cache hits in <100ms)
- [ ] **Use local LLM** (Ollama: no network latency)
- [ ] **Reduce chunk size** (fewer tokens = faster LLM)
- [ ] **Disable Playwright** (if site doesn't need JS)
- [ ] **Increase concurrency** (parallel requests)

```python
# Optimized configuration
config.cache.enabled = True
config.fetcher.enable_fallback = False  # httpx only
config.fetcher.max_concurrent = 10
config.chunker.chunk_size = 4000
config.summarizer.provider = "ollama"  # Local
```

---

### Problem: High memory usage

**Symptoms:** Python process using >2GB RAM.

**Causes:**
1. Large cache
2. Browser instances not closed
3. Too many concurrent requests
4. Large documents

**Solutions:**

**1. Limit cache size:**
```python
config.cache.max_size = 100 * 1024 * 1024  # 100MB
```

**2. Close resources properly:**
```python
async with URLFetcher(config) as fetcher:
    # Use fetcher
    pass  # Automatically closed
```

**3. Reduce concurrency:**
```python
config.fetcher.max_concurrent = 3  # Default: 5
```

**4. Use browser pool limits:**
```python
config.browser.max_browsers = 2  # Default: 5
```

---

### Problem: Browser pool exhaustion

**Symptoms:**
```
BrowserPool: All browsers busy, waiting...
```

**Cause:** More concurrent requests than available browsers.

**Solution:**

```python
# Increase browser pool
config.browser.max_browsers = 10  # Default: 5

# Or reduce concurrency
config.fetcher.max_concurrent = 3
```

**Monitor browser usage:**
```python
from mcp_web.browser_pool import BrowserPool

pool = BrowserPool(config.browser)
stats = await pool.get_stats()
print(f"Active browsers: {stats['active']}")
print(f"Available: {stats['available']}")
```

---

## Cache Issues

### Problem: Cache not working (always fetching)

**Diagnostic:**
```python
# Check if caching is enabled
print(config.cache.enabled)

# Check cache hits
from mcp_web.metrics import MetricsCollector
metrics = MetricsCollector(config.metrics)
stats = metrics.get_statistics()
print(f"Cache hit rate: {stats.get('cache_hits', 0)}")
```

**Solutions:**

**1. Verify cache is enabled:**
```python
config.cache.enabled = True
```

**2. Check cache directory permissions:**
```bash
ls -la ~/.cache/mcp-web/
# Should be writable by current user
chmod -R u+w ~/.cache/mcp-web/
```

**3. Check disk space:**
```bash
df -h ~/.cache/mcp-web/
```

---

### Problem: Stale cached data

**Symptoms:** Seeing old content despite page updates.

**Solution:**

**1. Clear cache:**
```python
from mcp_web.cache import CacheManager

cache = CacheManager(config.cache)
await cache.clear()
```

**2. Reduce TTL:**
```python
config.cache.ttl = 3600  # 1 hour instead of 7 days
```

**3. Disable caching for specific request:**
```python
result = await fetcher.fetch(url, use_cache=False)
```

---

### Problem: Cache directory filling up disk

**Cause:** No automatic pruning.

**Solution:**

**1. Clear cache:**
```bash
rm -rf ~/.cache/mcp-web/
```

**2. Set size limit:**
```python
config.cache.max_size = 500 * 1024 * 1024  # 500MB
```

**3. Manual pruning:**
```python
from mcp_web.cache import CacheManager

cache = CacheManager(config.cache)
await cache.prune()  # Remove old entries
```

---

## Security & Validation Errors

### Problem: `SecurityError: Prompt injection detected`

**Cause:** Input contains suspicious patterns.

**Symptoms:**
```
SecurityError: Potential prompt injection detected: "ignore previous instructions"
```

**This is working as designed!** The security filter is protecting you.

**If you want to allow it (NOT RECOMMENDED):**
```python
config.security.enable_prompt_filter = False  # Dangerous!
```

**Better: Sanitize input:**
```python
from mcp_web.security import PromptInjectionFilter

filter = PromptInjectionFilter()
safe_query = filter.sanitize(user_query)  # Removes dangerous content
```

---

### Problem: `ValueError: Path outside allowed directories`

**Cause:** File system access to unauthorized path.

**Solution:**

**Add directory to whitelist:**
```python
config.fetcher.enabled_file_system = True
config.fetcher.allowed_directories = [
    "/home/user/documents",
    "/home/user/downloads",
]
```

**Check resolved path:**
```python
from pathlib import Path
path = Path("/home/user/docs/report.pdf").resolve()
print(path)  # Shows actual path after symlink resolution
```

---

### Problem: `URLValidationError: URL not allowed`

**Cause:** URL fails validation (localhost, private IP, etc.).

**Examples of blocked URLs:**
- `http://localhost:8000` (localhost)
- `http://192.168.1.1` (private IP)
- `file:///etc/passwd` (outside whitelist)
- `ftp://example.com` (unsupported protocol)

**Solution:**

**For development, allow localhost:**
```python
# Note: May require modifying security.py
# Not recommended for production

# Alternative: Use ngrok or similar
ngrok http 8000  # Gives public URL
```

---

## Debugging Procedures

### Enable Debug Logging

```bash
export MCP_WEB_LOG_LEVEL=DEBUG
python your_script.py 2>&1 | tee debug.log
```

**What you'll see:**
- HTTP requests and responses
- Cache hits/misses
- Token counts
- LLM API calls
- Performance timings

---

### Capture Full Stack Trace

```python
import traceback
import sys

try:
    # Your code
    result = await pipeline.summarize_urls(urls)
except Exception as e:
    traceback.print_exc(file=sys.stderr)
    # Full stack trace printed
```

---

### Test Individual Components

```python
# Test fetcher only
from mcp_web.fetcher import URLFetcher

async def test_fetch():
    fetcher = URLFetcher(config)
    result = await fetcher.fetch("https://example.com")
    print(f"Status: {result.status_code}")
    print(f"Content length: {len(result.content)}")

# Test extractor only
from mcp_web.extractor import ContentExtractor

async def test_extract():
    extractor = ContentExtractor(config)
    content = await extractor.extract(fetch_result)
    print(f"Title: {content.title}")
    print(f"Content length: {len(content.content)}")
```

---

### Check Resource Cleanup

```python
# Ensure proper cleanup
import asyncio
import gc

async def test_cleanup():
    async with URLFetcher(config) as fetcher:
        result = await fetcher.fetch(url)
        # Fetcher closed automatically

    gc.collect()  # Force garbage collection
    await asyncio.sleep(1)  # Allow cleanup

    # Check for leaks
    import psutil
    process = psutil.Process()
    print(f"Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB")
    print(f"Open files: {len(process.open_files())}")
```

---

### Profiling Performance

```python
from mcp_web.profiler import profile

@profile("my_function")
async def my_function():
    # Your code
    pass

# Get results
from mcp_web.profiler import PerformanceCollector

collector = PerformanceCollector.get_instance()
stats = collector.get_statistics()

for name, metrics in stats.items():
    print(f"{name}:")
    print(f"  Count: {metrics['count']}")
    print(f"  Mean: {metrics['mean_ms']:.2f}ms")
    print(f"  Min: {metrics['min_ms']:.2f}ms")
    print(f"  Max: {metrics['max_ms']:.2f}ms")
```

---

## Getting Additional Help

### Still having issues?

**1. Check documentation:**
- [FAQ](FAQ.md)
- [API Reference](api/API.md)
- [Guides](guides/)

**2. Search existing issues:**
- GitHub Issues: https://github.com/yourusername/mcp-web/issues

**3. Ask in discussions:**
- GitHub Discussions: https://github.com/yourusername/mcp-web/discussions

**4. Report a bug:**

Include:
- MCP-Web version (`python -c "from mcp_web import __version__; print(__version__)"`)
- Python version (`python --version`)
- Operating system
- Full error message
- Debug logs
- Minimal reproduction code

---

## Common Error Messages Reference

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| `ModuleNotFoundError: No module named 'mcp_web'` | Not installed | `pip install mcp-web` |
| `AuthenticationError: Incorrect API key` | Invalid OpenAI key | Check `OPENAI_API_KEY` |
| `ConnectionRefusedError` | Ollama not running | `ollama serve` |
| `TimeoutError: Request timed out` | Slow server | Increase `timeout` |
| `ValidationError: 1 validation error` | Invalid config | Check config types |
| `SecurityError: Prompt injection detected` | Suspicious input | Working as designed |
| `BrowserPool: All browsers busy` | Pool exhausted | Increase `max_browsers` |
| `ValueError: Path outside allowed directories` | Unauthorized path | Add to `allowed_directories` |

---

**Last Updated:** 2025-11-15
**Need more help?** Open a [GitHub Issue](https://github.com/yourusername/mcp-web/issues)
