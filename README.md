# mcp-web

## MCP Server for Intelligent Web Summarization

A powerful Model Context Protocol (MCP) server that provides intelligent URL summarization with content extraction, smart chunking, and LLM-based summarization.

## Features

- 🚀 **Fast & Robust Fetching**: httpx primary with Playwright fallback for JS-heavy sites
- 📁 **File System Support**: Summarize local files (markdown, code, docs) alongside web URLs
- 🎯 **Intelligent Content Extraction**: trafilatura-powered main content extraction
- 📊 **Smart Chunking**: Hierarchical and semantic text splitting with configurable overlap
- 🤖 **LLM Summarization**: Map-reduce strategy for long documents with streaming output
- 🏠 **Local LLM Support**: Ollama, LM Studio, LocalAI, or cloud providers (OpenAI, Anthropic)
- 💾 **Persistent Caching**: Disk-based cache with TTL and LRU eviction
- 🔒 **Security First**: Path validation, directory whitelisting, and OWASP LLM Top 10 compliance
- 📈 **Metrics & Logging**: Comprehensive observability with structured logging
- 🔗 **Link Following**: Optional recursive link following for deeper context
- 📝 **Markdown Output**: Well-formatted summaries with citations and metadata
- 🧪 **Comprehensive Testing**: Unit, integration, security, golden, and benchmark tests

**Status:** Active Development | **Version:** 0.1.0 | **Test Coverage:** ~85% | **License:** MIT

## Real-World Example

**Input:** Summarize Python's asyncio documentation

```python
result = await summarize_urls(
    urls=["https://docs.python.org/3/library/asyncio.html"],
    query="How do I create and manage concurrent async tasks?"
)
```

**Output:**

> ## Summary: Python asyncio - Concurrent Task Management
>
> **Source:** https://docs.python.org/3/library/asyncio.html
>
> ### Key Points
>
> **Creating Tasks:**
>
> - Use `asyncio.create_task()` to schedule coroutines concurrently
> - Tasks are wrappers around coroutines that run them concurrently
> - `asyncio.gather()` runs multiple awaitables concurrently and collects results
>
> **Managing Tasks:**
>
> - `asyncio.wait()` for fine-grained control over task completion
> - `asyncio.TaskGroup()` (Python 3.11+) for structured concurrency
> - Tasks can be cancelled with `.cancel()` and checked with `.done()`
>
> **Best Practices:**
>
> - Always await tasks or they'll be garbage collected
> - Use timeouts with `asyncio.wait_for()` to prevent hanging
> - Handle exceptions with `try/except` or check `.exception()`
>
> **Performance:**
>
> - Tasks enable true concurrency for I/O-bound operations
> - Use semaphores to limit concurrent operations
> - Prefer `gather()` for simple parallel execution
>
> _Summary generated with llama3.2:3b via Ollama | Extraction: trafilatura | Chunking: adaptive (512 tokens)_

**Why this matters:** Instead of reading 15,000+ words of documentation, you get focused, actionable answers in seconds.

### File System Support Example

**Input:** Summarize local project documentation

```python
result = await summarize_urls(
    urls=[
        "file:///home/user/project/README.md",
        "/home/user/project/docs/ARCHITECTURE.md",
        "/home/user/project/CONTRIBUTING.md"
    ],
    query="How do I contribute to this project?"
)
```

**Output:**

> ## Summary: Project Contribution Guide
>
> **Sources:** README.md, ARCHITECTURE.md, CONTRIBUTING.md
>
> ### Getting Started
>
> - Fork the repository and clone locally
> - Install dependencies with `uv sync` (Python 3.10+)
> - Use dev containers for consistent environment
>
> ### Development Workflow
>
> - Follow conventional commits format
> - Run `task test` before submitting PR
> - Ensure linting passes with `task lint`
> - Add tests for new features (≥85% coverage required)
>
> ### Architecture Overview
>
> - Modular pipeline: Fetcher → Extractor → Chunker → Summarizer
> - Security-first design with path validation and whitelisting
> - Supports local LLMs (Ollama) and cloud providers
>
> _Summary generated from local files | Same quality as web URLs_

**Why this matters:** Quickly understand project structure, contribution guidelines, and architecture from local documentation without manual reading.

---

## Quick Start

### Option 1: Development Containers (Recommended)

The easiest way to get started is using VS Code Dev Containers with Docker:

```bash
# Prerequisites: Docker and VS Code with Dev Containers extension
# 1. Clone the repository
git clone https://github.com/geehexx/mcp-web.git
cd mcp-web

# 2. Open in VS Code
code .

# 3. When prompted, click "Reopen in Container"
# Or: Press F1 → "Dev Containers: Reopen in Container"
```

**What you get:**

- ✅ Python 3.10, uv, and all dependencies pre-installed
- ✅ Playwright browsers ready to use
- ✅ Pre-commit hooks configured
- ✅ VS Code extensions (Python, Ruff, Mypy, Task) installed
- ✅ Consistent environment across all developers

The container automatically runs setup on first launch. See [Development Containers](#development-containers) for details.

### Option 2: Manual Installation

```bash
# Clone the repository
git clone https://github.com/geehexx/mcp-web.git
cd mcp-web

# Install uv (modern Python package manager)
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install Taskfile (recommended)
# macOS: brew install go-task/tap/go-task
# Linux: snap install task --classic
# Or see: https://taskfile.dev/installation/

# Setup complete environment (recommended)
task dev:setup

# Or manual installation with uv
uv sync --all-extras
uv run playwright install chromium
```

### Configuration

#### Default Local LLM (Ollama)

```bash
# Install Ollama: https://ollama.com
# Start: ollama serve
# Pull model: ollama pull llama3.2:3b

export MCP_WEB_SUMMARIZER_PROVIDER=ollama
export MCP_WEB_SUMMARIZER_MODEL=llama3.2:3b

# Or use task commands
task llm:ollama:pull # Pull recommended models
task llm:ollama:start # Start Ollama server
```

See [docs/LOCAL_LLM_GUIDE.md](docs/LOCAL_LLM_GUIDE.md) for complete local LLM setup.

#### Cloud LLM (OpenAI)

```bash
export OPENAI_API_KEY="sk-..."
export MCP_WEB_SUMMARIZER_PROVIDER=openai
export MCP_WEB_SUMMARIZER_MODEL=gpt-4o-mini
```

Set these only if you need hosted OpenAI quality/latency characteristics.

#### Other Settings

```bash
# Cache settings
export MCP_WEB_CACHE_DIR="~/.cache/mcp-web"
export MCP_WEB_CACHE_TTL=604800 # 7 days

# Fetcher settings
export MCP_WEB_FETCHER_TIMEOUT=30
export MCP_WEB_FETCHER_MAX_CONCURRENT=5

# Summarizer settings
export MCP_WEB_SUMMARIZER_TEMPERATURE=0.3
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

```text
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

See [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) for full design documentation.

## Project Structure

```text
mcp-web/
├── src/mcp_web/
│ ├── mcp_server.py # MCP tool entry point & orchestration
│ ├── fetcher.py # URL fetching (httpx + Playwright)
│ ├── extractor.py # Content extraction (trafilatura)
│ ├── chunker.py # Text chunking strategies
│ ├── summarizer.py # LLM summarization (map-reduce)
│ ├── cache.py # Disk cache manager
│ ├── metrics.py # Logging & metrics collection
│ ├── config.py # Configuration management
│ └── utils.py # Token counting, formatting
├── tests/ # Unit & integration tests
├── docs/ # Architecture & API documentation
├── examples/ # Example usage scripts
└── pyproject.toml # Dependencies & project metadata
```

## Development Containers

This project includes a complete VS Code Development Container configuration for consistent, reproducible development environments.

### Quick Start with Dev Containers

1. **Install Prerequisites:**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - [VS Code](https://code.visualstudio.com/)
   - [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. **Open in Container:**

   ```bash
   git clone https://github.com/geehexx/mcp-web.git
   cd mcp-web
   code .
   # Press F1 → "Dev Containers: Reopen in Container"
   ```

3. **Wait for Setup:**
   - Container builds (~2-5 minutes first time)
   - Dependencies install automatically via `post-create.sh`
   - Playwright browsers download
   - Pre-commit hooks configure

4. **Start Developing:**

   ```bash
   task test:fast    # Run tests
   task lint         # Check code quality
   task --list       # See all commands
   ```

### What's Included

**Base Environment:**

- Debian 12 base image
- Python 3.10 (via uv)
- Node.js (for documentation tooling)
- Git, curl, build-essential

**Python Tools:**

- uv (fast package manager)
- pytest with xdist (parallel testing)
- ruff (linting & formatting)
- mypy (type checking)
- bandit, semgrep (security)

**VS Code Integration:**

- Python extension with Pylance
- Ruff extension (format on save)
- Mypy type checker
- Task runner integration
- Markdown linting
- Git integration (GitLens)
- Docker extension

**Playwright:**

- Chromium browser pre-installed
- All system dependencies configured
- Ready for integration tests

### Configuration Files

- `.devcontainer/Dockerfile` - Container image definition
- `.devcontainer/devcontainer.json` - VS Code settings and extensions
- `.devcontainer/post-create.sh` - Automated setup script

### Customization

**Add VS Code Extensions:**

Edit `.devcontainer/devcontainer.json`:

```json
"extensions": [
  "ms-python.python",
  "your-extension-id"
]
```

**Modify Python Version:**

Edit `.devcontainer/devcontainer.json`:

```json
"args": {
  "PYTHON_VERSION": "3.11"
}
```

**Add System Dependencies:**

Edit `.devcontainer/Dockerfile`:

```dockerfile
RUN apt-get update && apt-get install -y \
    your-package-here
```

### Troubleshooting

**Container Won't Build:**

- Check Docker is running: `docker ps`
- Clear Docker cache: `docker system prune -a`
- Rebuild without cache: F1 → "Dev Containers: Rebuild Container"

**Extensions Not Working:**

- Reload window: F1 → "Developer: Reload Window"
- Reinstall extensions: F1 → "Dev Containers: Rebuild Container"

**Performance Issues:**

- Allocate more resources in Docker Desktop settings
- Use WSL 2 backend on Windows
- Enable BuildKit: `export DOCKER_BUILDKIT=1`

See [VS Code Dev Containers docs](https://code.visualstudio.com/docs/devcontainers/containers) for more details.

## Development

### Using Taskfile (Recommended)

```bash
# Show all available tasks
task --list

# Complete setup
task dev:setup

# Run tests
task test # All tests except live
task test:fast # Unit + security + golden
task test:coverage # With coverage report
task test:parallel # Parallel execution

# Code quality
task lint # All linting
task format # Auto-format code
task security # Security scans
task analyze # Complete analysis

# CI simulation
task ci # Full CI pipeline
task ci:fast # Quick check
```

See [TASKFILE_GUIDE.md](TASKFILE_GUIDE.md) for complete task reference.

### Running Tests

```bash
# With Taskfile
task test # Recommended
task test:unit
task test:security
task test:golden # With local/cloud LLM

# Or with pytest directly
pytest -m "not live"
pytest -m unit
pytest -m golden
```

### Code Quality

```bash
# With Taskfile (recommended)
task lint
task format
task security

# Or directly
ruff check src/ tests/
ruff format src/ tests/
mypy src/
bandit -r src/
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

See [docs/architecture/ARCHITECTURE.md#configuration-strategy](docs/architecture/ARCHITECTURE.md#configuration-strategy) for complete configuration options.

### Key Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `FETCHER_TIMEOUT` | 30 | HTTP request timeout (seconds) |
| `FETCHER_MAX_CONCURRENT` | 5 | Max parallel fetches |
| `CHUNKER_CHUNK_SIZE` | 512 | Target tokens per chunk |
| `CHUNKER_OVERLAP` | 50 | Overlap between chunks (tokens) |
| `SUMMARIZER_MODEL` | llama3.2:3b | LLM model to use |
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
3. Use `llama3.2:3b` for cost-effective summaries (default)
4. Limit `max_depth` for link following
5. Prune cache periodically

## Troubleshooting

### Common Issues

### "No module named 'playwright'"

- Run `pip install playwright && playwright install chromium`

### "OPENAI_API_KEY not set"

- Export your API key: `export OPENAI_API_KEY="sk-..."`

### "Cache permission denied"

- Check `~/.cache/mcp-web` permissions or set custom `CACHE_DIR`

### "Extraction returned empty content"

- Site might be JS-heavy; fetcher will auto-fallback to Playwright
- Some sites block scrapers; check `robots.txt`

### Debug Mode

Enable debug logging:

```bash
export MCP_WEB_METRICS_LOG_LEVEL="DEBUG"
python -m mcp_web.mcp_server
```

## Roadmap

### v0.2.0 (Current)

- [x] Local LLM support (Ollama, LM Studio, LocalAI)
- [x] Comprehensive testing infrastructure
- [x] Security testing (OWASP LLM Top 10)
- [x] Taskfile for better tooling
- [x] Golden tests with deterministic verification

### v0.3.0

- [ ] PDF OCR support for scanned documents
- [ ] Multi-language translation
- [ ] Anthropic Claude integration
- [ ] Vector embeddings for semantic search

### v0.4.0

- [ ] Per-domain extraction rules
- [ ] Image/diagram extraction
- [ ] Incremental summarization
- [ ] Prometheus metrics export

See [docs/architecture/ARCHITECTURE.md#future-enhancements](docs/architecture/ARCHITECTURE.md#future-enhancements) for full roadmap.

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
