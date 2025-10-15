# mcp-web

**MCP Server for Intelligent Web Summarization**

A powerful Model Context Protocol (MCP) server that provides intelligent URL summarization with content extraction, smart chunking, and LLM-based summarization.

## Features

- 🚀 **Fast & Robust Fetching**: httpx primary with Playwright fallback for JS-heavy sites
- 🎯 **Intelligent Content Extraction**: trafilatura-powered main content extraction
- 📊 **Smart Chunking**: Hierarchical and semantic text splitting with configurable overlap
- 🤖 **LLM Summarization**: Map-reduce strategy for long documents with streaming output
- 💾 **Persistent Caching**: Disk-based cache with TTL and LRU eviction
- 📈 **Metrics & Logging**: Comprehensive observability with structured logging
- 🔗 **Link Following**: Optional recursive link following for deeper context
- 📝 **Markdown Output**: Well-formatted summaries with citations and metadata

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/geehexx/mcp-web.git
cd mcp-web

# Install dependencies
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"

# Install Playwright browsers (required for fallback)
playwright install chromium
```

### Configuration

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="sk-..."
```

Optional configuration via environment variables:

```bash
# Cache settings
export MCP_WEB_CACHE_DIR="~/.cache/mcp-web"
export MCP_WEB_CACHE_TTL=604800  # 7 days

# Fetcher settings
export MCP_WEB_FETCHER_TIMEOUT=30
export MCP_WEB_FETCHER_MAX_CONCURRENT=5

# Summarizer settings
export MCP_WEB_SUMMARIZER_MODEL="gpt-4o-mini"
export MCP_WEB_SUMMARIZER_MAX_TOKENS=2048
```

### Usage

#### As an MCP Server

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "mcp-web": {
      "command": "python",
      "args": ["-m", "mcp_web.mcp_server"]
    }
  }
}
```

#### Programmatic Usage

```python
from mcp_web import create_server, load_config

# Create server
config = load_config()
mcp = create_server(config)

# Use the pipeline directly
from mcp_web.mcp_server import WebSummarizationPipeline

pipeline = WebSummarizationPipeline(config)

# Summarize URLs
async for chunk in pipeline.summarize_urls(
    urls=["https://example.com"],
    query="What are the key features?",
):
    print(chunk, end="")
```

## Tools

### `summarize_urls`

Summarize content from one or more URLs with optional query focus.

**Parameters:**
- `urls` (List[str], required): URLs to summarize
- `query` (str, optional): Question or topic to focus the summary on
- `follow_links` (bool, default=False): Follow relevant outbound links
- `max_depth` (int, default=1): Maximum link following depth

**Example:**
```python
result = await summarize_urls(
    urls=["https://docs.python.org/3/library/asyncio.html"],
    query="How do I create async tasks?",
    follow_links=True
)
```

### `get_cache_stats`

Get cache and metrics statistics.

**Returns:** Dictionary with cache size, hit rates, and processing metrics

### `clear_cache`

Clear the entire cache.

### `prune_cache`

Remove expired cache entries.

## Architecture

### Pipeline Flow

```
URLs → Fetch (httpx/Playwright) → Extract (trafilatura) → 
Chunk (hierarchical/semantic) → Summarize (LLM map-reduce) → 
Markdown Output (streaming)
```

### Key Design Decisions

1. **DD-001**: httpx primary, Playwright fallback for robustness
2. **DD-002**: Trafilatura with `favor_recall=True` for maximum content extraction
3. **DD-003**: Hierarchical + semantic chunking preserves document structure
4. **DD-004**: 512-token chunks with 50-token overlap balances context
5. **DD-006**: Map-reduce summarization handles arbitrarily long documents
6. **DD-007**: 7-day disk cache with LRU eviction
7. **DD-008**: OpenAI GPT-4o-mini default (configurable)
8. **DD-009**: Streaming output for better UX

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for full design documentation.

## Project Structure

```
mcp-web/
├── src/mcp_web/
│   ├── mcp_server.py       # MCP tool entry point & orchestration
│   ├── fetcher.py          # URL fetching (httpx + Playwright)
│   ├── extractor.py        # Content extraction (trafilatura)
│   ├── chunker.py          # Text chunking strategies
│   ├── summarizer.py       # LLM summarization (map-reduce)
│   ├── cache.py            # Disk cache manager
│   ├── metrics.py          # Logging & metrics collection
│   ├── config.py           # Configuration management
│   └── utils.py            # Token counting, formatting
├── tests/                  # Unit & integration tests
├── docs/                   # Architecture & API documentation
├── examples/               # Example usage scripts
└── pyproject.toml          # Dependencies & project metadata
```

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=mcp_web --cov-report=html

# Run specific test categories
pytest -m unit
pytest -m integration
```

### Code Quality

```bash
# Lint with ruff
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
mypy src/
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run linting and tests
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Configuration Reference

See [docs/ARCHITECTURE.md#configuration-strategy](docs/ARCHITECTURE.md#configuration-strategy) for complete configuration options.

### Key Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `FETCHER_TIMEOUT` | 30 | HTTP request timeout (seconds) |
| `FETCHER_MAX_CONCURRENT` | 5 | Max parallel fetches |
| `CHUNKER_CHUNK_SIZE` | 512 | Target tokens per chunk |
| `CHUNKER_OVERLAP` | 50 | Overlap between chunks (tokens) |
| `SUMMARIZER_MODEL` | gpt-4o-mini | LLM model to use |
| `SUMMARIZER_TEMPERATURE` | 0.3 | LLM temperature |
| `CACHE_TTL` | 604800 | Cache TTL (7 days) |
| `CACHE_MAX_SIZE` | 1GB | Maximum cache size |

## Performance

### Benchmarks

- **Single URL**: ~5-10 seconds (with cache)
- **Multiple URLs (5)**: ~15-30 seconds (parallel fetching)
- **Large document (10k+ tokens)**: ~30-60 seconds (map-reduce)

### Optimization Tips

1. Enable caching for repeated queries
2. Adjust `chunk_size` based on content type
3. Use `gpt-4o-mini` for cost-effective summaries
4. Limit `max_depth` for link following
5. Prune cache periodically

## Troubleshooting

### Common Issues

**"No module named 'playwright'"**
- Run `pip install playwright && playwright install chromium`

**"OPENAI_API_KEY not set"**
- Export your API key: `export OPENAI_API_KEY="sk-..."`

**"Cache permission denied"**
- Check `~/.cache/mcp-web` permissions or set custom `CACHE_DIR`

**"Extraction returned empty content"**
- Site might be JS-heavy; fetcher will auto-fallback to Playwright
- Some sites block scrapers; check `robots.txt`

### Debug Mode

Enable debug logging:

```bash
export MCP_WEB_METRICS_LOG_LEVEL="DEBUG"
python -m mcp_web.mcp_server
```

## Roadmap

### v0.2.0
- [ ] PDF OCR support for scanned documents
- [ ] Multi-language translation
- [ ] Anthropic Claude integration
- [ ] Vector embeddings for semantic search

### v0.3.0
- [ ] Per-domain extraction rules
- [ ] Image/diagram extraction
- [ ] Incremental summarization
- [ ] Prometheus metrics export

See [docs/ARCHITECTURE.md#future-enhancements](docs/ARCHITECTURE.md#future-enhancements) for full roadmap.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic
- [trafilatura](https://github.com/adbar/trafilatura) for content extraction
- [httpx](https://www.python-httpx.org/) for async HTTP
- [Playwright](https://playwright.dev/) for browser automation
- [tiktoken](https://github.com/openai/tiktoken) for token counting

## Support

- 📚 [Documentation](docs/)
- 🐛 [Issue Tracker](https://github.com/geehexx/mcp-web/issues)
- 💬 [Discussions](https://github.com/geehexx/mcp-web/discussions)
