# Local LLM Support Guide

**Project:** mcp-web  
**Version:** 0.2.0  
**Last Updated:** 2025-10-15

---

## Overview

mcp-web now supports multiple LLM providers, including local models for:
- **Privacy:** Keep data on your machine
- **Cost:** No API costs
- **Speed:** Lower latency for local inference
- **Offline:** Work without internet connection

### Supported Providers

| Provider | URL | Default Port | Notes |
|----------|-----|--------------|-------|
| **OpenAI** | api.openai.com | 443 | Cloud-based (default) |
| **Ollama** | localhost | 11434 | Local, easy setup |
| **LM Studio** | localhost | 1234 | Local, GUI-based |
| **LocalAI** | localhost | 8080 | Local, OpenAI-compatible |
| **Custom** | configurable | any | Any OpenAI-compatible API |

---

## Quick Start

### Using Ollama (Recommended)

Ollama is the easiest local option with excellent model selection.

#### 1. Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

#### 2. Start Ollama

```bash
ollama serve
```

#### 3. Pull a Model

```bash
# Recommended for testing (fast, small)
ollama pull llama3.2:3b

# More capable models
ollama pull llama3.2:8b
ollama pull mistral:7b
ollama pull phi3:mini
```

#### 4. Configure mcp-web

```bash
# Environment variables
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b

# Or in Python
from mcp_web.config import SummarizerSettings

config = SummarizerSettings(
    provider="ollama",
    model="llama3.2:3b",
    temperature=0.3,
)
```

#### 5. Run Tests

```bash
# Test with local LLM
task llm:test:local

# Or with pytest
pytest -m golden -v
```

---

## Provider Details

### Ollama

**Best for:** General use, easy setup, good model selection

**Setup:**
```bash
# Install
brew install ollama  # macOS
# or
curl -fsSL https://ollama.com/install.sh | sh  # Linux

# Start server
ollama serve

# Pull models
ollama pull llama3.2:3b    # Fast, 3B params
ollama pull llama3.2:8b    # Better, 8B params  
ollama pull mistral:7b     # Alternative
ollama pull phi3:mini      # Microsoft's small model
```

**Configuration:**
```python
SummarizerSettings(
    provider="ollama",
    model="llama3.2:3b",  # or any pulled model
    api_base="http://localhost:11434/v1",  # auto-detected
    api_key="not-needed",  # auto-set
)
```

**Environment Variables:**
```bash
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b
# api_base and api_key auto-detected
```

**Recommended Models:**

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama3.2:3b | 3B | Fast | Good | Development, testing |
| llama3.2:8b | 8B | Medium | Better | Production |
| mistral:7b | 7B | Medium | Good | General purpose |
| phi3:mini | 3.8B | Fast | Good | Resource-constrained |

### LM Studio

**Best for:** GUI users, model experimentation

**Setup:**
1. Download LM Studio: https://lmstudio.ai
2. Install and launch
3. Download models from the UI
4. Start local server (Server tab, port 1234)

**Configuration:**
```python
SummarizerSettings(
    provider="lmstudio",
    model="local-model",  # Model loaded in LM Studio
    api_base="http://localhost:1234/v1",
)
```

**Environment Variables:**
```bash
export MCP_WEB_SUMMARIZER_PROVIDER=lmstudio
export MCP_WEB_SUMMARIZER_MODEL=local-model
```

### LocalAI

**Best for:** Docker deployments, production

**Setup:**
```bash
# Docker
docker run -p 8080:8080 \
  -v $PWD/models:/models \
  quay.io/go-skynet/local-ai:latest

# Or docker-compose
docker-compose up -d
```

**Configuration:**
```python
SummarizerSettings(
    provider="localai",
    model="gpt-3.5-turbo",  # Model name in LocalAI
    api_base="http://localhost:8080/v1",
)
```

### Custom Provider

**Best for:** Custom OpenAI-compatible APIs

```python
SummarizerSettings(
    provider="custom",
    model="your-model-name",
    api_base="https://your-api.com/v1",
    api_key="your-api-key",
)
```

---

## Configuration Reference

### Python Configuration

```python
from mcp_web.config import Config, SummarizerSettings

# Ollama
config = Config(
    summarizer=SummarizerSettings(
        provider="ollama",
        model="llama3.2:3b",
        temperature=0.3,  # 0.0 = deterministic, 2.0 = creative
        max_tokens=2048,
        map_reduce_threshold=8000,  # Use map-reduce for docs > 8k tokens
    )
)

# LM Studio
config = Config(
    summarizer=SummarizerSettings(
        provider="lmstudio",
        model="local-model",
        temperature=0.5,
    )
)

# OpenAI (cloud)
config = Config(
    summarizer=SummarizerSettings(
        provider="openai",
        model="gpt-4o-mini",
        api_key="sk-...",  # or from env
    )
)
```

### Environment Variables

All configuration can be done via environment variables:

```bash
# Provider selection
export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b

# Generation parameters
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3
export MCP_WEB_SUMMARIZER_MAX_TOKENS=2048

# API configuration (optional, auto-detected)
export MCP_WEB_SUMMARIZER_API_BASE=http://localhost:11434/v1
export MCP_WEB_SUMMARIZER_API_KEY=not-needed

# Map-reduce threshold
export MCP_WEB_SUMMARIZER_MAP_REDUCE_THRESHOLD=8000
```

### Auto-Detection

The config automatically detects the correct settings:

```python
config = SummarizerSettings(provider="ollama")

# Automatically sets:
# - api_base = "http://localhost:11434/v1"
# - api_key = "not-needed"

config.get_api_base()  # "http://localhost:11434/v1"
config.get_api_key()   # "not-needed"
```

---

## Testing with Local LLMs

### Golden Tests

Golden tests now verify actual summarization output:

```bash
# Run with Ollama (if running)
task llm:test:local

# Or explicitly set provider
MCP_WEB_SUMMARIZER_PROVIDER=ollama \
MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b \
pytest -m golden -v
```

### Test Features

1. **Auto-detection:** Tests automatically detect available LLM providers
2. **Deterministic:** Uses temperature=0 for reproducible results
3. **Verification:** Checks summary contains key concepts
4. **Map-reduce:** Tests summary of summaries

### Running Specific Tests

```bash
# All golden tests with local LLM
pytest tests/golden/test_golden_summarization.py -v

# Specific test
pytest tests/golden/test_golden_summarization.py::TestGoldenSummarization::test_simple_article_summary -v

# Map-reduce tests
pytest -m "golden and slow" -v

# Ollama-specific
pytest tests/golden/test_golden_summarization.py::TestLocalLLMSupport::test_ollama_summarization -v
```

---

## Model Selection

### For Development & Testing

Use fast, small models:

```bash
# Ollama
ollama pull llama3.2:3b      # Recommended
ollama pull phi3:mini
```

Configuration:
```python
SummarizerSettings(
    provider="ollama",
    model="llama3.2:3b",
    temperature=0.0,  # Deterministic for tests
    max_tokens=1024,  # Lower for speed
)
```

### For Production

Use larger, more capable models:

```bash
# Ollama
ollama pull llama3.2:8b
ollama pull mistral:7b
ollama pull mixtral:8x7b    # Mixture of experts
```

Configuration:
```python
SummarizerSettings(
    provider="ollama",
    model="llama3.2:8b",
    temperature=0.3,  # Balanced
    max_tokens=2048,
    map_reduce_threshold=8000,
)
```

### Model Comparison

| Model | Params | RAM | Speed | Quality | Best For |
|-------|--------|-----|-------|---------|----------|
| llama3.2:3b | 3B | 4GB | Fast | Good | Testing, dev |
| phi3:mini | 3.8B | 4GB | Fast | Good | Limited resources |
| llama3.2:8b | 8B | 8GB | Medium | Better | Production |
| mistral:7b | 7B | 8GB | Medium | Good | General use |
| mixtral:8x7b | 47B | 32GB | Slow | Excellent | High quality |

---

## Performance Optimization

### Hardware Recommendations

**Minimum (Development):**
- CPU: 4 cores
- RAM: 8GB
- Models: llama3.2:3b, phi3:mini

**Recommended (Production):**
- CPU: 8+ cores (or GPU)
- RAM: 16GB+
- Models: llama3.2:8b, mistral:7b

**High Performance:**
- GPU: NVIDIA with 8GB+ VRAM
- RAM: 32GB+
- Models: mixtral:8x7b, llama3.2:70b

### Optimization Tips

#### 1. Use GPU Acceleration

Ollama automatically uses GPU if available:

```bash
# Check GPU usage
ollama ps

# Force CPU mode
OLLAMA_NUM_GPU=0 ollama serve
```

#### 2. Adjust Context Size

```python
SummarizerSettings(
    max_tokens=1024,  # Lower for speed
    map_reduce_threshold=4000,  # Lower threshold = more chunking
)
```

#### 3. Batch Processing

```python
# Process multiple chunks efficiently
chunks = chunker.chunk_text(long_document)

# Map-reduce automatically batches
async for summary_chunk in summarizer.summarize_chunks(chunks):
    print(summary_chunk)
```

#### 4. Caching

Enable caching to avoid re-summarizing:

```python
from mcp_web.cache import CacheManager

cache = CacheManager(
    cache_dir="~/.cache/mcp-web",
    ttl=7 * 24 * 3600,  # 7 days
)
```

---

## Troubleshooting

### Connection Issues

**Problem:** `Connection refused` or `Failed to connect to localhost:11434`

**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

### Model Not Found

**Problem:** `Model 'llama3.2:3b' not found`

**Solution:**
```bash
# List available models
ollama list

# Pull the model
ollama pull llama3.2:3b
```

### Out of Memory

**Problem:** `Out of memory` or system freezing

**Solution:**
```bash
# Use smaller model
ollama pull llama3.2:3b  # instead of 8b

# Or limit memory
OLLAMA_MAX_LOADED_MODELS=1 ollama serve
```

### Slow Performance

**Problem:** Slow summarization

**Solutions:**
1. Use smaller model (llama3.2:3b vs 8b)
2. Reduce max_tokens
3. Enable GPU acceleration
4. Lower map_reduce_threshold for better chunking

### Tests Skipping

**Problem:** `No LLM available for testing`

**Solution:**
```bash
# Start Ollama
ollama serve

# Pull a model
ollama pull llama3.2:3b

# Or set OpenAI key
export OPENAI_API_KEY="sk-..."

# Re-run tests
pytest -m golden -v
```

---

## Task Commands

The Taskfile includes convenient commands for local LLM work:

```bash
# Start Ollama (if installed)
task llm:ollama:start

# Pull recommended models
task llm:ollama:pull

# Test with local LLM
task llm:test:local

# Check configuration
task info:env
```

---

## Comparison: Local vs Cloud

### Local LLMs (Ollama, LM Studio)

**Pros:**
- ✅ Privacy (data stays local)
- ✅ No API costs
- ✅ Lower latency (once loaded)
- ✅ Offline operation
- ✅ Unlimited requests

**Cons:**
- ❌ Requires powerful hardware
- ❌ Lower quality (vs GPT-4)
- ❌ Slower cold start
- ❌ Limited context length

### Cloud LLMs (OpenAI, Anthropic)

**Pros:**
- ✅ Higher quality
- ✅ No hardware requirements
- ✅ Fast cold start
- ✅ Larger context windows

**Cons:**
- ❌ Costs per request
- ❌ Requires internet
- ❌ Data sent to cloud
- ❌ Rate limits

### Recommendation

**Development:** Use Ollama with llama3.2:3b for fast iteration

**Testing:** Use temperature=0 with either local or cloud for determinism

**Production:** Choose based on:
- Privacy needs → Local
- Quality needs → Cloud
- Cost constraints → Local
- Scale → Cloud (with caching)

---

## Examples

### Basic Usage

```python
from mcp_web import MCPWebServer
from mcp_web.config import Config, SummarizerSettings

# Configure for Ollama
config = Config(
    summarizer=SummarizerSettings(
        provider="ollama",
        model="llama3.2:3b",
    )
)

# Use in pipeline
async def summarize_url(url: str) -> str:
    async with MCPWebServer(config) as server:
        result = await server.summarize_urls([url])
        return result
```

### With Custom Settings

```python
config = Config(
    summarizer=SummarizerSettings(
        provider="ollama",
        model="llama3.2:8b",
        temperature=0.5,  # More creative
        max_tokens=4096,  # Longer summaries
        map_reduce_threshold=16000,  # Larger docs before chunking
    )
)
```

### Multiple Providers

```python
# Switch providers dynamically
import os

provider = os.getenv("LLM_PROVIDER", "ollama")

configs = {
    "ollama": SummarizerSettings(provider="ollama", model="llama3.2:3b"),
    "openai": SummarizerSettings(provider="openai", model="gpt-4o-mini"),
    "lmstudio": SummarizerSettings(provider="lmstudio", model="local-model"),
}

config = Config(summarizer=configs[provider])
```

---

## Resources

### Ollama

- Website: https://ollama.com
- Models: https://ollama.com/library
- GitHub: https://github.com/ollama/ollama
- Discord: https://discord.gg/ollama

### LM Studio

- Website: https://lmstudio.ai
- Documentation: https://lmstudio.ai/docs

### LocalAI

- Website: https://localai.io
- GitHub: https://github.com/go-skynet/LocalAI
- Docker: https://quay.io/repository/go-skynet/local-ai

### Model Sources

- Hugging Face: https://huggingface.co/models
- Ollama Library: https://ollama.com/library
- TheBloke (GGUF): https://huggingface.co/TheBloke

---

## Security Considerations

### Local LLMs

- ✅ Data never leaves your machine
- ✅ No API key exposure risk
- ✅ Full control over model
- ⚠️ Still validate outputs (prompt injection possible)
- ⚠️ Models may have biases

### Best Practices

1. **Validate inputs** even with local LLMs
2. **Sanitize outputs** before displaying to users
3. **Keep models updated** for security patches
4. **Use content filtering** for production
5. **Monitor resource usage** to prevent DoS

---

## Future Enhancements

- [ ] Support for vLLM (high-performance serving)
- [ ] Llama.cpp integration (CPU-optimized)
- [ ] Model quantization options (4-bit, 8-bit)
- [ ] Automatic model selection based on hardware
- [ ] Fine-tuning support for domain-specific models
- [ ] Multi-model ensembles

---

**Author:** mcp-web team  
**Version:** 0.2.0  
**Status:** ✅ Local LLM support fully implemented
