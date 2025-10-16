# Configuration Guide

**Version:** 0.1.0
**Last Updated:** 2025-10-16

---

## Overview

This guide provides practical configuration examples for common use cases. For a complete reference of all environment variables, see [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md).

---

## Quick Start

### 1. Default Local LLM (Ollama)

**Setup:**

```bash
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"
```

**MCP Client Config** (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "mcp-web": {
      "command": "python",
      "args": ["-m", "mcp_web.mcp_server"],
      "env": {
        "MCP_WEB_SUMMARIZER_PROVIDER": "ollama",
        "MCP_WEB_SUMMARIZER_MODEL": "llama3.2:3b"
      }
    }
  }
}
```

### 2. Cloud LLM (OpenAI)

**Prerequisites:**

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start server
ollama serve

# Pull model
ollama pull llama3.2:3b
```

**Setup:**

```bash
export OPENAI_API_KEY="sk-..."
export MCP_WEB_SUMMARIZER_PROVIDER="openai"
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"
```

**MCP Client Config:**

```json
{
  "mcpServers": {
    "mcp-web": {
      "command": "python",
      "args": ["-m", "mcp_web.mcp_server"],
      "env": {
        "OPENAI_API_KEY": "sk-...",
        "MCP_WEB_SUMMARIZER_PROVIDER": "openai",
        "MCP_WEB_SUMMARIZER_MODEL": "gpt-4o-mini"
      }
    }
  }
}
```

---

## Use Case Configurations

### High-Speed (Cloud LLM, Aggressive Caching)

**Goal:** Minimize latency, maximize cache hits

```bash
# Fast model
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.0  # Deterministic

# Aggressive parallel
export MCP_WEB_FETCHER_MAX_CONCURRENT=20
export MCP_WEB_SUMMARIZER_PARALLEL_MAP=true

# Large cache
export MCP_WEB_CACHE_TTL=2592000  # 30 days
export MCP_WEB_CACHE_MAX_SIZE=$((5 * 1024 * 1024 * 1024))  # 5 GB

# Disable Playwright for speed
export MCP_WEB_FETCHER_ENABLE_FALLBACK=false
```

**Tradeoffs:**

- ✅ Fastest performance
- ⚠️ May fail on JS-heavy sites (no Playwright fallback)
- ⚠️ Large disk usage

---

### High-Quality (GPT-4, Conservative)

**Goal:** Best summary quality, robustness

```bash
# Best model
export MCP_WEB_SUMMARIZER_MODEL="gpt-4-turbo"
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3

# Conservative chunk size
export MCP_WEB_CHUNKER_CHUNK_SIZE=1024
export MCP_WEB_CHUNKER_CHUNK_OVERLAP=100

# Enable all extraction
export MCP_WEB_EXTRACTOR_INCLUDE_COMMENTS=true
export MCP_WEB_EXTRACTOR_INCLUDE_TABLES=true

# Enable Playwright fallback
export MCP_WEB_FETCHER_ENABLE_FALLBACK=true

# Longer timeouts
export MCP_WEB_FETCHER_TIMEOUT=60
export MCP_WEB_SUMMARIZER_TIMEOUT=300
```

**Tradeoffs:**

- ✅ Best quality summaries
- ⚠️ Slower (GPT-4 is slower than GPT-4o-mini)
- ⚠️ Higher cost

---

### Cost-Optimized (Local LLM)

**Goal:** Zero API costs, privacy

```bash
# Local LLM
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"

# Longer timeout (local LLMs slower)
export MCP_WEB_SUMMARIZER_TIMEOUT=300

# Smaller chunks (local LLMs have smaller context)
export MCP_WEB_CHUNKER_CHUNK_SIZE=512

# Aggressive cache (LLM is slow)
export MCP_WEB_CACHE_TTL=2592000  # 30 days
```

**Tradeoffs:**

- ✅ No API costs
- ✅ Complete privacy (no cloud calls)
- ⚠️ Slower than cloud LLMs
- ⚠️ Lower quality (depends on model)

---

### Privacy-First (Local Everything)

**Goal:** No external network calls

```bash
# Local LLM
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"

# Disable external fetching (local files only)
# Not implemented yet - use with caution

# Aggressive caching
export MCP_WEB_CACHE_ENABLED=true
export MCP_WEB_CACHE_TTL=2592000

# Disable metrics export
export MCP_WEB_METRICS_METRICS_EXPORT_PATH=""
```

---

### Development/Testing

**Goal:** Fast iteration, verbose logging

```bash
# Local LLM for speed
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"

# Verbose logging
export MCP_WEB_METRICS_LOG_LEVEL="DEBUG"

# Short cache (fresh data)
export MCP_WEB_CACHE_TTL=3600  # 1 hour

# Fast timeouts
export MCP_WEB_FETCHER_TIMEOUT=30
export MCP_WEB_SUMMARIZER_TIMEOUT=120
```

---

## Performance Tuning

### Maximize Throughput (Multiple URLs)

```bash
# High concurrency
export MCP_WEB_FETCHER_MAX_CONCURRENT=20

# Parallel map-reduce
export MCP_WEB_SUMMARIZER_PARALLEL_MAP=true

# Streaming map for progress updates
export MCP_WEB_SUMMARIZER_STREAMING_MAP=true
```

**Measured Impact:**

- 20 concurrent fetches: ~5x faster than sequential
- Parallel map-reduce: 1.17x faster than sequential

---

### Minimize Latency (Single URL)

```bash
# Fast model
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"

# Adaptive max_tokens
export MCP_WEB_SUMMARIZER_ADAPTIVE_MAX_TOKENS=true
export MCP_WEB_SUMMARIZER_MAX_TOKENS_RATIO=0.5

# Stop sequences
export MCP_WEB_SUMMARIZER_STOP_SEQUENCES='["\n\n\n"]'

# Disable Playwright if not needed
export MCP_WEB_FETCHER_ENABLE_FALLBACK=false
```

**Measured Impact:**

- Prompt optimization: 45-60% faster
- Adaptive max_tokens: 20-30% faster (depends on content)

---

### Minimize Cost

```bash
# Use local LLM (zero cost)
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"

# OR use smallest cloud model
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"

# Aggressive caching
export MCP_WEB_CACHE_ENABLED=true
export MCP_WEB_CACHE_TTL=2592000  # 30 days

# Smaller summaries
export MCP_WEB_SUMMARIZER_MAX_TOKENS=1024
```

**Cost Comparison** (1000 URLs, avg 5k tokens each):

| Model | Cost | Notes |
|-------|------|-------|
| Ollama (local) | $0 | Free, slower |
| gpt-4o-mini | ~$5 | Fast, good quality |
| gpt-4-turbo | ~$50 | Best quality, expensive |

---

## LLM Provider Setup

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
export MCP_WEB_SUMMARIZER_PROVIDER="openai"
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"
```

**Available Models:**

- `gpt-4o-mini` (recommended, fast & cheap)
- `gpt-4-turbo` (best quality, expensive)
- `gpt-3.5-turbo` (faster, lower quality)

---

### Ollama

**Install:**

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

**Start Server:**

```bash
ollama serve
```

**Pull Models:**

```bash
ollama pull llama3.2:3b     # Recommended, fast
ollama pull mistral:7b      # Good quality
ollama pull llama3.1:8b     # Better quality, slower
```

**Configure:**

```bash
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"
```

**Custom Port:**

```bash
export MCP_WEB_SUMMARIZER_API_BASE="http://localhost:11434/v1"
```

---

### LM Studio

**Install:** Download from [lmstudio.ai](https://lmstudio.ai/)

**Configure:**

```bash
export MCP_WEB_SUMMARIZER_PROVIDER="lmstudio"
export MCP_WEB_SUMMARIZER_MODEL="local-model"
export MCP_WEB_SUMMARIZER_API_BASE="http://localhost:1234/v1"
```

---

### Anthropic Claude (Future)

**Planned for v0.4.0:**

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export MCP_WEB_SUMMARIZER_PROVIDER="anthropic"
export MCP_WEB_SUMMARIZER_MODEL="claude-3-haiku-20240307"
```

---

## Troubleshooting

### Issue: "No module named 'playwright'"

**Solution:**

```bash
pip install playwright
playwright install chromium
```

Or disable Playwright:

```bash
export MCP_WEB_FETCHER_ENABLE_FALLBACK=false
```

---

### Issue: "OPENAI_API_KEY not set"

**Solution:**

```bash
export OPENAI_API_KEY="sk-..."
```

Or use local LLM:

```bash
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
```

---

### Issue: Summaries are too short

**Solution:**

```bash
# Increase max tokens
export MCP_WEB_SUMMARIZER_MAX_TOKENS=4096

# Or disable adaptive mode
export MCP_WEB_SUMMARIZER_ADAPTIVE_MAX_TOKENS=false
```

---

### Issue: Summaries are too slow

**Solution:**

```bash
# Use faster model
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"

# Enable adaptive max_tokens
export MCP_WEB_SUMMARIZER_ADAPTIVE_MAX_TOKENS=true

# Increase concurrency
export MCP_WEB_FETCHER_MAX_CONCURRENT=10
```

---

### Issue: Cache taking too much space

**Solution:**

```bash
# Reduce TTL
export MCP_WEB_CACHE_TTL=86400  # 1 day

# Reduce max size
export MCP_WEB_CACHE_MAX_SIZE=$((500 * 1024 * 1024))  # 500 MB

# Or clear cache
python -m mcp_web.cli clear-cache
```

---

## Advanced Configuration

### Custom API Base

For OpenAI-compatible APIs:

```bash
export MCP_WEB_SUMMARIZER_PROVIDER="custom"
export MCP_WEB_SUMMARIZER_API_BASE="https://api.example.com/v1"
export MCP_WEB_SUMMARIZER_API_KEY="custom-key"
export MCP_WEB_SUMMARIZER_MODEL="custom-model"
```

---

### Nested Configuration (Future)

Using `__` delimiter:

```bash
export MCP_WEB__SUMMARIZER__MODEL="gpt-4o-mini"
export MCP_WEB__CACHE__TTL=604800
```

---

### YAML Config (Planned)

```yaml
# mcp-web.yml
summarizer:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.3

cache:
  ttl: 604800
  max_size: 1073741824
```

Load with:

```python
from mcp_web import load_config

config = load_config(config_file="mcp-web.yml")
```

---

## References

- **Environment Variables**: [ENVIRONMENT_VARIABLES.md](ENVIRONMENT_VARIABLES.md)
- **Architecture**: [../architecture/ARCHITECTURE.md](../architecture/ARCHITECTURE.md)
- **Local LLM Guide**: [../guides/LOCAL_LLM_GUIDE.md](../guides/LOCAL_LLM_GUIDE.md)
- **Configuration Code**: [../../src/mcp_web/config.py](../../src/mcp_web/config.py)

---

**Last Updated:** 2025-10-16
**Maintained by:** mcp-web core team
