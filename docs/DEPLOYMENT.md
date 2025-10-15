# Deployment Guide

**mcp-web** - Production Deployment Instructions

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Configuration](#configuration)
4. [Running the Server](#running-the-server)
5. [Integration with MCP Clients](#integration-with-mcp-clients)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **OS:** Linux, macOS, or Windows
- **Python:** 3.10 or higher
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 2GB for dependencies + cache storage
- **Network:** Internet access for URL fetching and LLM API calls

### Required Accounts

- OpenAI API account with API key (or compatible API endpoint)
- Optional: Anthropic API for Claude integration

---

## Installation Methods

### Method 1: pip (Recommended)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

# Install from source
cd mcp-web
pip install -e .

# Install Playwright browsers
playwright install chromium
```

### Method 2: uv (Fast Alternative)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create environment and install
uv venv
source .venv/bin/activate
uv pip install -e .

# Install Playwright
playwright install chromium
```

### Method 3: Docker (Coming in v0.2)

```bash
# Build image
docker build -t mcp-web:latest .

# Run container
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY mcp-web:latest
```

---

## Configuration

### 1. API Keys

**Required:** OpenAI API key

```bash
export OPENAI_API_KEY="sk-..."
```

**Optional:** Custom API endpoint

```bash
export MCP_WEB_SUMMARIZER_API_BASE="https://api.openai.com/v1"
```

### 2. Environment Variables

Create a `.env` file or export variables:

```bash
# Core settings
export MCP_WEB_CACHE_DIR="~/.cache/mcp-web"
export MCP_WEB_METRICS_LOG_LEVEL="INFO"

# Fetcher settings
export MCP_WEB_FETCHER_TIMEOUT=30
export MCP_WEB_FETCHER_MAX_CONCURRENT=5
export MCP_WEB_FETCHER_USE_PLAYWRIGHT_FALLBACK=true

# Extractor settings
export MCP_WEB_EXTRACTOR_FAVOR_RECALL=true

# Chunker settings
export MCP_WEB_CHUNKER_STRATEGY="hierarchical"
export MCP_WEB_CHUNKER_CHUNK_SIZE=512
export MCP_WEB_CHUNKER_CHUNK_OVERLAP=50

# Summarizer settings
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3
export MCP_WEB_SUMMARIZER_MAX_TOKENS=2048

# Cache settings
export MCP_WEB_CACHE_TTL=604800 # 7 days
export MCP_WEB_CACHE_MAX_SIZE=1073741824 # 1GB
```

### 3. Directory Structure

Ensure proper permissions for:

```bash
# Cache directory
mkdir -p ~/.cache/mcp-web
chmod 755 ~/.cache/mcp-web

# Config directory (optional, for future YAML configs)
mkdir -p ~/.config/mcp-web
```

---

## Running the Server

### Method 1: Direct Python Execution

```bash
python -m mcp_web.mcp_server
```

### Method 2: As Module

```python
from mcp_web import create_server

server = create_server()
# Server is now ready for MCP client connections
```

### Method 3: Systemd Service (Linux)

Create `/etc/systemd/system/mcp-web.service`:

```ini
[Unit]
Description=MCP Web Summarization Server
After=network.target

[Service]
Type=simple
User=mcp-web
WorkingDirectory=/opt/mcp-web
Environment="OPENAI_API_KEY=sk-..."
Environment="MCP_WEB_CACHE_DIR=/var/cache/mcp-web"
ExecStart=/opt/mcp-web/venv/bin/python -m mcp_web.mcp_server
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable mcp-web
sudo systemctl start mcp-web
sudo systemctl status mcp-web
```

---

## Integration with MCP Clients

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
 "mcpServers": {
 "mcp-web": {
 "command": "python",
 "args": ["-m", "mcp_web.mcp_server"],
 "env": {
 "OPENAI_API_KEY": "sk-..."
 }
 }
 }
}
```

### Custom MCP Client

```python
import asyncio
from mcp.client import Client

async def main():
 async with Client() as client:
 # Connect to mcp-web server
 await client.connect_to_server("mcp-web")
 
 # Call summarize_urls tool
 result = await client.call_tool(
 "summarize_urls",
 urls=["https://example.com"],
 query="What is this about?"
 )
 
 print(result)

asyncio.run(main())
```

---

## Monitoring & Maintenance

### 1. Metrics Collection

Enable metrics export:

```bash
export MCP_WEB_METRICS_ENABLED=true
export MCP_WEB_METRICS_EXPORT_PATH="/var/log/mcp-web/metrics.json"
```

View metrics:

```python
from mcp_web import create_server

server = create_server()
# Access metrics through server tools
metrics = await server.call_tool("get_cache_stats")
print(metrics)
```

### 2. Log Management

Logs are written to stdout/stderr by default. Redirect for persistent logging:

```bash
python -m mcp_web.mcp_server 2>&1 | tee -a /var/log/mcp-web/server.log
```

Log rotation with logrotate (`/etc/logrotate.d/mcp-web`):

```
/var/log/mcp-web/*.log {
 daily
 rotate 7
 compress
 delaycompress
 notifempty
 create 0644 mcp-web mcp-web
}
```

### 3. Cache Maintenance

**Automatic Pruning:**

```python
# Schedule periodic pruning
from mcp_web.cache import CacheManager

cache = CacheManager(cache_dir="~/.cache/mcp-web")
pruned = await cache.prune()
print(f"Pruned {pruned} expired entries")
```

**Manual Cleanup:**

```bash
# Clear entire cache
rm -rf ~/.cache/mcp-web/*

# Or use the tool
python -c "
import asyncio
from mcp_web import create_server
server = create_server()
asyncio.run(server.call_tool('clear_cache'))
"
```

**Disk Space Monitoring:**

```bash
du -sh ~/.cache/mcp-web
```

### 4. Performance Monitoring

Key metrics to monitor:

- **Cache hit rate:** Should be >50% for repeated queries
- **Fetch duration:** httpx should be <1s, Playwright <5s
- **LLM token usage:** Track costs
- **Error rates:** Should be <5%

View metrics:

```bash
# Export metrics to file
python -c "
import asyncio
from mcp_web.metrics import get_metrics_collector
collector = get_metrics_collector()
collector.save_metrics('metrics.json')
"
```

---

## Security Considerations

### 1. API Key Protection

**Never commit API keys to version control:**

```bash
# Use environment variables
export OPENAI_API_KEY="sk-..."

# Or use secrets management
# AWS Secrets Manager, HashiCorp Vault, etc.
```

**File permissions:**

```bash
chmod 600 ~/.bashrc # If storing in shell config
```

### 2. Cache Security

Cache may contain sensitive data. Secure the cache directory:

```bash
chmod 700 ~/.cache/mcp-web
```

For multi-user systems, use per-user caches:

```bash
export MCP_WEB_CACHE_DIR="$HOME/.cache/mcp-web"
```

### 3. Network Security

**Firewall rules:**

- Allow outbound HTTPS (443) for API calls and URL fetching
- No inbound connections required (MCP uses stdio)

**Proxy configuration:**

```bash
export HTTP_PROXY="http://proxy.example.com:8080"
export HTTPS_PROXY="http://proxy.example.com:8080"
```

### 4. Content Security

Be cautious when summarizing:

- Untrusted URLs (may contain malicious content)
- Sites requiring authentication (credentials exposure)
- Internal company URLs (data leakage to LLM API)

Consider:

- URL allowlist/blocklist
- Content filtering
- Local LLM for sensitive content

### 5. Resource Limits

Prevent abuse with configuration limits:

```bash
export MCP_WEB_FETCHER_MAX_CONCURRENT=3 # Limit parallel fetches
export MCP_WEB_FETCHER_TIMEOUT=10 # Shorter timeout
export MCP_WEB_CACHE_MAX_SIZE=536870912 # 512MB cache limit
```

---

## Troubleshooting

### Issue: "No module named 'playwright'"

**Solution:**

```bash
pip install playwright
playwright install chromium
```

### Issue: "OPENAI_API_KEY not set"

**Solution:**

```bash
export OPENAI_API_KEY="sk-..."
# Add to ~/.bashrc or ~/.zshrc for persistence
```

### Issue: "Cache permission denied"

**Solution:**

```bash
mkdir -p ~/.cache/mcp-web
chmod 755 ~/.cache/mcp-web
# Or set custom cache directory
export MCP_WEB_CACHE_DIR="/tmp/mcp-web-cache"
```

### Issue: "Playwright browser not found"

**Solution:**

```bash
playwright install chromium
# Or disable Playwright fallback
export MCP_WEB_FETCHER_USE_PLAYWRIGHT_FALLBACK=false
```

### Issue: "Extraction returns empty content"

**Possible causes:**

1. Site blocks scrapers (check robots.txt)
2. JS-heavy site (enable Playwright: `force_playwright=True`)
3. Paywall or login required

**Solution:**

```python
# Force Playwright for problematic sites
result = await summarize_urls(
 urls=["https://js-heavy-site.com"],
 # Will auto-fallback to Playwright if httpx fails
)
```

### Issue: "LLM timeout or rate limit"

**Solution:**

```bash
# Increase timeout
export MCP_WEB_SUMMARIZER_TIMEOUT=120

# Use smaller chunks
export MCP_WEB_CHUNKER_CHUNK_SIZE=256

# Reduce max tokens
export MCP_WEB_SUMMARIZER_MAX_TOKENS=1024
```

### Issue: "High memory usage"

**Solution:**

```bash
# Reduce cache size
export MCP_WEB_CACHE_MAX_SIZE=268435456 # 256MB

# Reduce concurrent fetches
export MCP_WEB_FETCHER_MAX_CONCURRENT=2

# Clear cache periodically
python -c "import asyncio; from mcp_web import create_server; ..."
```

### Debug Mode

Enable verbose logging:

```bash
export MCP_WEB_METRICS_LOG_LEVEL="DEBUG"
export MCP_WEB_METRICS_STRUCTURED_LOGGING=false # Human-readable
python -m mcp_web.mcp_server
```

---

## Health Checks

### Basic Health Check

```python
import asyncio
from mcp_web import create_server, load_config

async def health_check():
 try:
 config = load_config()
 server = create_server(config)
 print("✓ Server initialized successfully")
 
 # Check cache
 if server.pipeline.cache:
 stats = server.pipeline.cache.get_stats()
 print(f"✓ Cache operational: {stats['size_mb']:.2f} MB")
 
 print("✓ Health check passed")
 return True
 except Exception as e:
 print(f"✗ Health check failed: {e}")
 return False

asyncio.run(health_check())
```

### Production Health Check Script

```bash
#!/bin/bash
# health_check.sh

# Check if server is responsive
python -c "
import asyncio
from mcp_web import create_server

async def check():
 try:
 server = create_server()
 return True
 except Exception as e:
 print(f'Error: {e}')
 return False

result = asyncio.run(check())
exit(0 if result else 1)
"

if [ $? -eq 0 ]; then
 echo "Health check: OK"
 exit 0
else
 echo "Health check: FAILED"
 exit 1
fi
```

---

## Backup & Recovery

### Backup Cache

```bash
# Backup cache directory
tar -czf mcp-web-cache-backup-$(date +%Y%m%d).tar.gz ~/.cache/mcp-web/

# Restore from backup
tar -xzf mcp-web-cache-backup-20251015.tar.gz -C ~/
```

### Backup Configuration

```bash
# Backup environment variables
env | grep MCP_WEB > mcp-web-env-backup.txt

# Restore
source mcp-web-env-backup.txt
```

---

## Production Checklist

- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`pip install -e .`)
- [ ] Playwright browsers installed (`playwright install chromium`)
- [ ] OPENAI_API_KEY configured
- [ ] Cache directory created with proper permissions
- [ ] Log directory created (if logging to file)
- [ ] Environment variables configured
- [ ] Service configured (systemd/supervisor)
- [ ] Monitoring configured
- [ ] Cache pruning scheduled (cron/systemd timer)
- [ ] Log rotation configured
- [ ] Backups configured
- [ ] Security review completed
- [ ] Health checks configured
- [ ] Documentation reviewed

---

## Support

- **Documentation:** [docs/](.)
- **Issues:** [GitHub Issues](https://github.com/geehexx/mcp-web/issues)
- **Discussions:** [GitHub Discussions](https://github.com/geehexx/mcp-web/discussions)

---

**Last Updated:** 2025-10-15
**Version:** 0.1.0
