# Environment Variables Reference

**Version:** 0.1.0
**Last Updated:** 2025-10-16

---

## Overview

mcp-web uses environment variables for configuration. All variables are prefixed with `MCP_WEB_` followed by the component name.

**Configuration Hierarchy:**

1. Environment variables (highest priority)
2. `.env` file
3. Default values (lowest priority)

---

## Quick Start

### Minimal Setup (Default Local LLM)

```bash
export MCP_WEB_SUMMARIZER_PROVIDER="ollama"
export MCP_WEB_SUMMARIZER_MODEL="llama3.2:3b"
```

### Minimal Setup (Cloud LLM)

```bash
export OPENAI_API_KEY="sk-..."
export MCP_WEB_SUMMARIZER_PROVIDER="openai"
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"
```

---

## Fetcher Settings

**Prefix:** `MCP_WEB_FETCHER_`

### MCP_WEB_FETCHER_TIMEOUT

**Type:** Integer
**Default:** `30`
**Description:** HTTP request timeout in seconds

```bash
export MCP_WEB_FETCHER_TIMEOUT=60
```

### MCP_WEB_FETCHER_PLAYWRIGHT_TIMEOUT

**Type:** Integer
**Default:** `60`
**Description:** Playwright browser timeout in seconds (should be longer than httpx timeout)

```bash
export MCP_WEB_FETCHER_PLAYWRIGHT_TIMEOUT=90
```

### MCP_WEB_FETCHER_MAX_CONCURRENT

**Type:** Integer
**Default:** `5`
**Description:** Maximum concurrent fetch operations

```bash
export MCP_WEB_FETCHER_MAX_CONCURRENT=10
```

### MCP_WEB_FETCHER_ENABLE_FALLBACK

**Type:** Boolean
**Default:** `true`
**Description:** Enable Playwright fallback for JavaScript-heavy sites

```bash
export MCP_WEB_FETCHER_ENABLE_FALLBACK=false  # Disable fallback (faster, less robust)
```

### MCP_WEB_FETCHER_USER_AGENT

**Type:** String
**Default:** `"mcp-web/0.1.0 (compatible; AI assistant)"`
**Description:** User-Agent header for HTTP requests

```bash
export MCP_WEB_FETCHER_USER_AGENT="MyBot/1.0"
```

### MCP_WEB_FETCHER_RESPECT_ROBOTS_TXT

**Type:** Boolean
**Default:** `true`
**Description:** Honor robots.txt rules

```bash
export MCP_WEB_FETCHER_RESPECT_ROBOTS_TXT=false  # Ignore robots.txt (not recommended)
```

### MCP_WEB_FETCHER_CRAWL_DELAY_OVERRIDE

**Type:** Float (optional)
**Default:** `null`
**Description:** Override crawl-delay from robots.txt (seconds)

```bash
export MCP_WEB_FETCHER_CRAWL_DELAY_OVERRIDE=2.0
```

### MCP_WEB_FETCHER_MAX_RETRIES

**Type:** Integer
**Default:** `3`
**Description:** Maximum retry attempts for failed requests

```bash
export MCP_WEB_FETCHER_MAX_RETRIES=5
```

### MCP_WEB_FETCHER_RETRY_DELAY

**Type:** Float
**Default:** `1.0`
**Description:** Delay between retries in seconds

```bash
export MCP_WEB_FETCHER_RETRY_DELAY=2.0
```

---

## Extractor Settings

**Prefix:** `MCP_WEB_EXTRACTOR_`

### MCP_WEB_EXTRACTOR_FAVOR_RECALL

**Type:** Boolean
**Default:** `true`
**Description:** Maximize content extraction (favor recall over precision)

```bash
export MCP_WEB_EXTRACTOR_FAVOR_RECALL=false
```

### MCP_WEB_EXTRACTOR_INCLUDE_COMMENTS

**Type:** Boolean
**Default:** `true`
**Description:** Extract comment sections from articles

```bash
export MCP_WEB_EXTRACTOR_INCLUDE_COMMENTS=false
```

### MCP_WEB_EXTRACTOR_INCLUDE_TABLES

**Type:** Boolean
**Default:** `true`
**Description:** Extract table content

```bash
export MCP_WEB_EXTRACTOR_INCLUDE_TABLES=false
```

### MCP_WEB_EXTRACTOR_INCLUDE_LINKS

**Type:** Boolean
**Default:** `true`
**Description:** Extract link targets

```bash
export MCP_WEB_EXTRACTOR_INCLUDE_LINKS=false
```

### MCP_WEB_EXTRACTOR_INCLUDE_IMAGES

**Type:** Boolean
**Default:** `true`
**Description:** Extract image metadata (alt text, captions)

```bash
export MCP_WEB_EXTRACTOR_INCLUDE_IMAGES=false
```

### MCP_WEB_EXTRACTOR_EXTRACT_METADATA

**Type:** Boolean
**Default:** `true`
**Description:** Extract page metadata (title, author, date, description)

```bash
export MCP_WEB_EXTRACTOR_EXTRACT_METADATA=false
```

---

## Chunker Settings

**Prefix:** `MCP_WEB_CHUNKER_`

### MCP_WEB_CHUNKER_STRATEGY

**Type:** Enum (`hierarchical`, `semantic`, `fixed`)
**Default:** `"hierarchical"`
**Description:** Chunking strategy to use

```bash
export MCP_WEB_CHUNKER_STRATEGY=semantic
```

### MCP_WEB_CHUNKER_CHUNK_SIZE

**Type:** Integer
**Default:** `512`
**Description:** Target tokens per chunk

```bash
export MCP_WEB_CHUNKER_CHUNK_SIZE=1024
```

### MCP_WEB_CHUNKER_CHUNK_OVERLAP

**Type:** Integer
**Default:** `50`
**Description:** Overlap between chunks in tokens

```bash
export MCP_WEB_CHUNKER_CHUNK_OVERLAP=100
```

### MCP_WEB_CHUNKER_MIN_CHUNK_SIZE

**Type:** Integer
**Default:** `100`
**Description:** Minimum chunk size in tokens

```bash
export MCP_WEB_CHUNKER_MIN_CHUNK_SIZE=200
```

### MCP_WEB_CHUNKER_MAX_CHUNK_SIZE

**Type:** Integer
**Default:** `1024`
**Description:** Maximum chunk size in tokens

```bash
export MCP_WEB_CHUNKER_MAX_CHUNK_SIZE=2048
```

### MCP_WEB_CHUNKER_PRESERVE_CODE_BLOCKS

**Type:** Boolean
**Default:** `true`
**Description:** Keep code blocks intact when possible

```bash
export MCP_WEB_CHUNKER_PRESERVE_CODE_BLOCKS=false
```

### MCP_WEB_CHUNKER_ADAPTIVE_CHUNKING

**Type:** Boolean
**Default:** `true`
**Description:** Dynamically adjust chunk size based on document characteristics

```bash
export MCP_WEB_CHUNKER_ADAPTIVE_CHUNKING=false
```

### MCP_WEB_CHUNKER_CODE_CHUNK_SIZE

**Type:** Integer
**Default:** `1024`
**Description:** Chunk size for code-heavy documents

```bash
export MCP_WEB_CHUNKER_CODE_CHUNK_SIZE=2048
```

### MCP_WEB_CHUNKER_DENSE_CHUNK_SIZE

**Type:** Integer
**Default:** `768`
**Description:** Chunk size for dense prose

```bash
export MCP_WEB_CHUNKER_DENSE_CHUNK_SIZE=512
```

### MCP_WEB_CHUNKER_CODE_BLOCK_THRESHOLD

**Type:** Float (0.0-1.0)
**Default:** `0.1`
**Description:** Minimum proportion of code blocks to trigger code chunk sizing

```bash
export MCP_WEB_CHUNKER_CODE_BLOCK_THRESHOLD=0.2
```

### MCP_WEB_CHUNKER_DENSE_SENTENCE_THRESHOLD

**Type:** Integer
**Default:** `24`
**Description:** Average words per sentence to treat prose as dense

```bash
export MCP_WEB_CHUNKER_DENSE_SENTENCE_THRESHOLD=30
```

---

## Summarizer Settings

**Prefix:** `MCP_WEB_SUMMARIZER_`

### MCP_WEB_SUMMARIZER_PROVIDER

**Type:** Enum (`openai`, `ollama`, `lmstudio`, `localai`, `custom`)
**Default:** `"ollama"`
**Description:** LLM provider type

```bash
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
```

### MCP_WEB_SUMMARIZER_MODEL

**Type:** String
**Default:** `"llama3.2:3b"`
**Description:** LLM model to use

**Examples:**

```bash
# OpenAI
export MCP_WEB_SUMMARIZER_MODEL=gpt-4o-mini
export MCP_WEB_SUMMARIZER_MODEL=gpt-4-turbo

# Ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b
export MCP_WEB_SUMMARIZER_MODEL=mistral:7b

# LM Studio / LocalAI
export MCP_WEB_SUMMARIZER_MODEL=local-model
```

### MCP_WEB_SUMMARIZER_TEMPERATURE

**Type:** Float (0.0-2.0)
**Default:** `0.3`
**Description:** LLM temperature (0=deterministic, 2=creative)

```bash
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.0  # Maximum determinism
export MCP_WEB_SUMMARIZER_TEMPERATURE=1.0  # More creative
```

### MCP_WEB_SUMMARIZER_MAX_TOKENS

**Type:** Integer
**Default:** `2048`
**Description:** Maximum tokens in summary

```bash
export MCP_WEB_SUMMARIZER_MAX_TOKENS=4096
```

### MCP_WEB_SUMMARIZER_STREAMING

**Type:** Boolean
**Default:** `true`
**Description:** Enable streaming output

```bash
export MCP_WEB_SUMMARIZER_STREAMING=false
```

### MCP_WEB_SUMMARIZER_STOP_SEQUENCES

**Type:** JSON Array of Strings
**Default:** `[]`
**Description:** Stop sequences to prevent over-generation

```bash
export MCP_WEB_SUMMARIZER_STOP_SEQUENCES='["\n\n\n", "---"]'
```

### MCP_WEB_SUMMARIZER_ADAPTIVE_MAX_TOKENS

**Type:** Boolean
**Default:** `false`
**Description:** Automatically adjust max_tokens based on input size

```bash
export MCP_WEB_SUMMARIZER_ADAPTIVE_MAX_TOKENS=true
```

### MCP_WEB_SUMMARIZER_MAX_TOKENS_RATIO

**Type:** Float (0.1-1.0)
**Default:** `0.5`
**Description:** Ratio of input tokens to max output tokens (for adaptive mode)

```bash
export MCP_WEB_SUMMARIZER_MAX_TOKENS_RATIO=0.3
```

### MCP_WEB_SUMMARIZER_MAP_REDUCE_THRESHOLD

**Type:** Integer
**Default:** `8000`
**Description:** Token threshold for switching to map-reduce strategy

```bash
export MCP_WEB_SUMMARIZER_MAP_REDUCE_THRESHOLD=10000
```

### MCP_WEB_SUMMARIZER_PARALLEL_MAP

**Type:** Boolean
**Default:** `true`
**Description:** Use parallel map phase for better performance

```bash
export MCP_WEB_SUMMARIZER_PARALLEL_MAP=false
```

### MCP_WEB_SUMMARIZER_STREAMING_MAP

**Type:** Boolean
**Default:** `false`
**Description:** Stream map progress updates (better UX, slightly slower)

```bash
export MCP_WEB_SUMMARIZER_STREAMING_MAP=true
```

### MCP_WEB_SUMMARIZER_API_KEY

**Type:** String (optional)
**Default:** `null` (reads from `OPENAI_API_KEY`)
**Description:** API key for cloud providers

```bash
export MCP_WEB_SUMMARIZER_API_KEY="sk-..."
# Or use standard variable:
export OPENAI_API_KEY="sk-..."
```

### MCP_WEB_SUMMARIZER_API_BASE

**Type:** String (optional)
**Default:** Auto-detected by provider
**Description:** Custom API base URL

```bash
export MCP_WEB_SUMMARIZER_API_BASE="https://api.openai.com/v1"
export MCP_WEB_SUMMARIZER_API_BASE="http://localhost:11434/v1"
```

**Auto-detected values:**

- `openai`: `https://api.openai.com/v1`
- `ollama`: `http://localhost:11434/v1`
- `lmstudio`: `http://localhost:1234/v1`
- `localai`: `http://localhost:8080/v1`

### MCP_WEB_SUMMARIZER_TIMEOUT

**Type:** Integer
**Default:** `120`
**Description:** API request timeout in seconds

```bash
export MCP_WEB_SUMMARIZER_TIMEOUT=300
```

### MCP_WEB_SUMMARIZER_MAX_SUMMARY_LENGTH

**Type:** Integer
**Default:** `10000`
**Description:** Maximum summary length (safety limit)

```bash
export MCP_WEB_SUMMARIZER_MAX_SUMMARY_LENGTH=20000
```

### MCP_WEB_SUMMARIZER_CONTENT_FILTERING

**Type:** Boolean
**Default:** `true`
**Description:** Enable content filtering for safety

```bash
export MCP_WEB_SUMMARIZER_CONTENT_FILTERING=false  # Not recommended
```

---

## Cache Settings

**Prefix:** `MCP_WEB_CACHE_`

### MCP_WEB_CACHE_ENABLED

**Type:** Boolean
**Default:** `true`
**Description:** Enable caching

```bash
export MCP_WEB_CACHE_ENABLED=false
```

### MCP_WEB_CACHE_CACHE_DIR

**Type:** String (path)
**Default:** `"~/.cache/mcp-web"`
**Description:** Cache directory path

```bash
export MCP_WEB_CACHE_CACHE_DIR="/var/cache/mcp-web"
```

### MCP_WEB_CACHE_TTL

**Type:** Integer
**Default:** `604800` (7 days)
**Description:** Cache time-to-live in seconds

```bash
export MCP_WEB_CACHE_TTL=86400  # 1 day
export MCP_WEB_CACHE_TTL=2592000  # 30 days
```

### MCP_WEB_CACHE_MAX_SIZE

**Type:** Integer
**Default:** `1073741824` (1 GB)
**Description:** Maximum cache size in bytes

```bash
export MCP_WEB_CACHE_MAX_SIZE=$((2 * 1024 * 1024 * 1024))  # 2 GB
```

### MCP_WEB_CACHE_EVICTION_POLICY

**Type:** Enum (`lru`, `lfu`)
**Default:** `"lru"`
**Description:** Cache eviction policy

- `lru`: Least Recently Used
- `lfu`: Least Frequently Used

```bash
export MCP_WEB_CACHE_EVICTION_POLICY=lfu
```

---

## Metrics Settings

**Prefix:** `MCP_WEB_METRICS_`

### MCP_WEB_METRICS_ENABLED

**Type:** Boolean
**Default:** `true`
**Description:** Enable metrics collection

```bash
export MCP_WEB_METRICS_ENABLED=false
```

### MCP_WEB_METRICS_LOG_LEVEL

**Type:** Enum (`DEBUG`, `INFO`, `WARNING`, `ERROR`)
**Default:** `"INFO"`
**Description:** Logging level

```bash
export MCP_WEB_METRICS_LOG_LEVEL=DEBUG
```

### MCP_WEB_METRICS_STRUCTURED_LOGGING

**Type:** Boolean
**Default:** `true`
**Description:** Use structured JSON logs

```bash
export MCP_WEB_METRICS_STRUCTURED_LOGGING=false
```

### MCP_WEB_METRICS_METRICS_EXPORT_PATH

**Type:** String (path, optional)
**Default:** `null`
**Description:** Export metrics to file

```bash
export MCP_WEB_METRICS_METRICS_EXPORT_PATH="/var/log/mcp-web/metrics.json"
```

---

## Common Configurations

### Production (Cloud LLM)

```bash
# OpenAI Configuration
export OPENAI_API_KEY="sk-..."
export MCP_WEB_SUMMARIZER_PROVIDER=openai
export MCP_WEB_SUMMARIZER_MODEL=gpt-4o-mini
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3
export MCP_WEB_SUMMARIZER_MAX_TOKENS=2048

# Performance
export MCP_WEB_FETCHER_MAX_CONCURRENT=10
export MCP_WEB_SUMMARIZER_PARALLEL_MAP=true

# Caching
export MCP_WEB_CACHE_TTL=604800  # 7 days
export MCP_WEB_CACHE_MAX_SIZE=$((2 * 1024 * 1024 * 1024))  # 2 GB

# Security
export MCP_WEB_FETCHER_RESPECT_ROBOTS_TXT=true
export MCP_WEB_SUMMARIZER_CONTENT_FILTERING=true

# Logging
export MCP_WEB_METRICS_LOG_LEVEL=INFO
```

### Development (Local LLM)

```bash
# Ollama Configuration
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3

# Performance (slower with local LLM)
export MCP_WEB_FETCHER_MAX_CONCURRENT=5
export MCP_WEB_SUMMARIZER_TIMEOUT=300

# Caching (aggressive for dev)
export MCP_WEB_CACHE_TTL=2592000  # 30 days

# Logging (verbose)
export MCP_WEB_METRICS_LOG_LEVEL=DEBUG
```

### Testing (Fast, No External Calls)

```bash
# Disable caching
export MCP_WEB_CACHE_ENABLED=false

# Disable Playwright fallback
export MCP_WEB_FETCHER_ENABLE_FALLBACK=false

# Fast timeouts
export MCP_WEB_FETCHER_TIMEOUT=10
export MCP_WEB_SUMMARIZER_TIMEOUT=30

# Minimal logging
export MCP_WEB_METRICS_LOG_LEVEL=WARNING
```

---

## .env File Example

Create `.env` in project root:

```bash
# .env.example - Copy to .env and fill in values

# LLM Provider (OpenAI)
OPENAI_API_KEY=sk-...
MCP_WEB_SUMMARIZER_MODEL=gpt-4o-mini

# OR Local LLM (Ollama)
# MCP_WEB_SUMMARIZER_PROVIDER=ollama
# MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b

# Performance Tuning
MCP_WEB_FETCHER_MAX_CONCURRENT=10
MCP_WEB_SUMMARIZER_PARALLEL_MAP=true

# Caching
MCP_WEB_CACHE_CACHE_DIR=~/.cache/mcp-web
MCP_WEB_CACHE_TTL=604800

# Logging
MCP_WEB_METRICS_LOG_LEVEL=INFO
```

---

## Validation

To see the current configuration:

```python
from mcp_web import load_config

config = load_config()
print(config.model_dump_json(indent=2))
```

Or via CLI (if implemented):

```bash
mcp-web config show
```

---

## References

- **Configuration Code**: [../../src/mcp_web/config.py](../../src/mcp_web/config.py)
- **Configuration Guide**: [CONFIGURATION.md](CONFIGURATION.md)
- **Architecture**: [../architecture/ARCHITECTURE.md](../architecture/ARCHITECTURE.md)

---

**Last Updated:** 2025-10-16
**Maintained by:** mcp-web core team
