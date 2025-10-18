# API Documentation

**mcp-web** - Module & Function Reference

---

## Table of Contents

1. [MCP Server](#mcp-server)
2. [Fetcher](#fetcher)
3. [Extractor](#extractor)
4. [Chunker](#chunker)
5. [Summarizer](#summarizer)
6. [Cache](#cache)
7. [Configuration](#configuration)
8. [Utils](#utils)
9. [Metrics](#metrics)

---

## MCP Server

### `create_server(config: Optional[Config] = None) -> FastMCP`

Create MCP server with summarization tools.

**Parameters:**

- `config` (Config, optional): Configuration object (loads defaults if not provided)

**Returns:**

- `FastMCP`: Configured MCP server instance

**Example:**

```python
from mcp_web import create_server, load_config

config = load_config()
mcp = create_server(config)
```

---

### MCP Tool: `summarize_urls`

**Signature:**

```python
async def summarize_urls(
 urls: List[str],
 query: Optional[str] = None,
 follow_links: bool = False,
 max_depth: int = 1,
) -> str
```

**Description:**
Summarize content from one or more URLs with optional query focus and link following.

**Parameters:**

- `urls` (List[str], required): List of URLs to fetch and summarize
- `query` (str, optional): Question or topic to focus the summary on
- `follow_links` (bool, default=False): Whether to follow relevant outbound links
- `max_depth` (int, default=1): Maximum link following depth

**Returns:**

- `str`: Markdown-formatted summary with sources and metadata

**Example:**

```python
result = await summarize_urls(
 urls=["https://docs.python.org/3/library/asyncio.html"],
 query="How do I create async tasks?",
 follow_links=True,
 max_depth=1
)
```

---

### `WebSummarizationPipeline`

Main orchestration class for the summarization pipeline.

#### Constructor

```python
def __init__(self, config: Config)
```

**Parameters:**

- `config` (Config): Application configuration

---

#### `summarize_urls()`

```python
async def summarize_urls(
 urls: List[str],
 query: Optional[str] = None,
 follow_links: bool = False,
 max_depth: int = 1,
) -> AsyncIterator[str]
```

**Description:**
Summarize content from URLs with streaming output.

**Yields:**

- `str`: Summary text chunks (streaming)

**Example:**

```python
pipeline = WebSummarizationPipeline(config)

async for chunk in pipeline.summarize_urls(["https://example.com"]):
 print(chunk, end="")
```

---

## Fetcher

### `URLFetcher`

Fetches URLs with automatic fallback from httpx to Playwright.

#### Constructor

```python
def __init__(
 config: FetcherSettings,
 cache: Optional[CacheManager] = None,
)
```

---

#### `fetch()`

```python
async def fetch(
 url: str,
 force_playwright: bool = False,
 use_cache: bool = True,
) -> FetchResult
```

**Description:**
Fetch URL with automatic fallback strategy.

**Parameters:**

- `url` (str): URL to fetch
- `force_playwright` (bool, default=False): Skip httpx, use Playwright directly
- `use_cache` (bool, default=True): Use cached result if available

**Returns:**

- `FetchResult`: Result with content, headers, and metadata

**Raises:**

- `Exception`: If all fetch methods fail

---

#### `fetch_multiple()`

```python
async def fetch_multiple(
 urls: List[str],
 max_concurrent: Optional[int] = None,
) -> Dict[str, FetchResult]
```

**Description:**
Fetch multiple URLs concurrently with rate limiting.

**Parameters:**

- `urls` (List[str]): URLs to fetch
- `max_concurrent` (int, optional): Max concurrent requests (defaults to config)

**Returns:**

- `Dict[str, FetchResult]`: Mapping of URL to FetchResult

---

### `FetchResult`

Dataclass representing fetch result.

**Attributes:**

- `url` (str): Final URL (after redirects)
- `content` (bytes): Response content
- `content_type` (str): Content-Type header value
- `headers` (Dict[str, str]): Response headers
- `status_code` (int): HTTP status code
- `fetch_method` (str): Method used ('httpx', 'playwright', or 'cache')
- `from_cache` (bool): Whether result was from cache

---

## Extractor

### `ContentExtractor`

Extracts main content from HTML and PDF.

#### Constructor

```python
def __init__(
 config: ExtractorSettings,
 cache: Optional[CacheManager] = None,
)
```

---

#### `extract()`

```python
async def extract(
 fetch_result: FetchResult,
 use_cache: bool = True,
) -> ExtractedContent
```

**Description:**
Extract content from fetch result.

**Parameters:**

- `fetch_result` (FetchResult): Result from URLFetcher
- `use_cache` (bool, default=True): Use cached extraction if available

**Returns:**

- `ExtractedContent`: Extracted content with metadata

**Raises:**

- `Exception`: If extraction fails

---

### `ExtractedContent`

Dataclass representing extracted content.

**Attributes:**

- `url` (str): Source URL
- `title` (str): Page title
- `content` (str): Main content (Markdown formatted)
- `metadata` (dict): Page metadata (author, date, etc.)
- `links` (List[str]): Extracted links
- `code_snippets` (List[CodeSnippet]): Extracted code blocks
- `timestamp` (datetime): Extraction timestamp

**Methods:**

- `to_dict() -> dict`: Convert to dictionary for serialization
- `from_dict(data: dict) -> ExtractedContent`: Create from dictionary

---

## Chunker

### `TextChunker`

Intelligent text chunking with multiple strategies.

#### Constructor

```python
def __init__(self, config: ChunkerSettings)
```

---

#### `chunk_text()`

```python
def chunk_text(
 text: str,
 metadata: Optional[dict] = None,
) -> List[Chunk]
```

**Description:**
Chunk text using configured strategy.

**Parameters:**

- `text` (str): Input text to chunk
- `metadata` (dict, optional): Metadata to attach to chunks

**Returns:**

- `List[Chunk]`: List of text chunks

**Strategies:**

- `hierarchical`: Respects document structure (headings, sections)
- `semantic`: Splits at paragraph/sentence boundaries
- `fixed`: Fixed-size chunks with overlap

---

### `Chunk`

Dataclass representing a text chunk.

**Attributes:**

- `text` (str): Chunk text
- `tokens` (int): Token count
- `start_pos` (int): Start position in original text
- `end_pos` (int): End position in original text
- `metadata` (dict): Chunk metadata (heading, section, etc.)

**Methods:**

- `to_dict() -> dict`: Convert to dictionary

---

## Summarizer

### `Summarizer`

LLM-based content summarization with map-reduce.

#### Constructor

```python
def __init__(self, config: SummarizerSettings)
```

---

#### `summarize_chunks()`

```python
async def summarize_chunks(
 chunks: List[Chunk],
 query: Optional[str] = None,
 sources: Optional[List[str]] = None,
) -> AsyncIterator[str]
```

**Description:**
Summarize chunks with streaming output.

**Parameters:**

- `chunks` (List[Chunk]): Text chunks to summarize
- `query` (str, optional): Query for focused summary
- `sources` (List[str], optional): Source URLs for citations

**Yields:**

- `str`: Summary text chunks (streaming)

**Strategy:**

- If total tokens ≤ `map_reduce_threshold`: Direct summarization (single LLM call)
- If total tokens > `map_reduce_threshold`: Map-reduce (summarize chunks → combine)

---

## Cache

### `CacheManager`

Disk-based cache with TTL and size limits.

#### Constructor

```python
def __init__(
 cache_dir: str,
 ttl: int = 7 * 24 * 3600,
 max_size: int = 1024 * 1024 * 1024,
 eviction_policy: str = "lru",
)
```

**Parameters:**

- `cache_dir` (str): Directory for cache storage
- `ttl` (int, default=7 days): Default time-to-live (seconds)
- `max_size` (int, default=1GB): Maximum cache size (bytes)
- `eviction_policy` (str, default='lru'): Eviction policy

---

#### `get()`

```python
async def get(key: str) -> Optional[Any]
```

Retrieve cached value if valid.

---

#### `set()`

```python
async def set(
 key: str,
 value: Any,
 ttl: Optional[int] = None,
 etag: Optional[str] = None,
 last_modified: Optional[str] = None,
) -> bool
```

Store value in cache with TTL.

---

#### `delete()`

```python
async def delete(key: str) -> bool
```

Delete cached value.

---

#### `prune()`

```python
async def prune() -> int
```

Remove expired entries. Returns number of entries pruned.

---

#### `clear()`

```python
async def clear() -> None
```

Clear entire cache.

---

#### `get_stats()`

```python
def get_stats() -> Dict[str, Any]
```

Get cache statistics (size, usage, entry count).

---

### `CacheKeyBuilder`

Helper for building consistent cache keys.

**Methods:**

- `fetch_key(url: str, params: Optional[Dict] = None) -> str`
- `extract_key(url: str, config: Optional[Dict] = None) -> str`
- `summary_key(url: str, query: Optional[str] = None, config: Optional[Dict] = None) -> str`

---

## Configuration

### `Config`

Root configuration class with nested settings.

**Attributes:**

- `fetcher` (FetcherSettings): Fetcher configuration
- `extractor` (ExtractorSettings): Extractor configuration
- `chunker` (ChunkerSettings): Chunker configuration
- `summarizer` (SummarizerSettings): Summarizer configuration
- `cache` (CacheSettings): Cache configuration
- `metrics` (MetricsSettings): Metrics configuration

---

### `load_config()`

```python
def load_config(
 config_file: Optional[Path] = None,
 overrides: Optional[Dict[str, Any]] = None,
) -> Config
```

Load configuration from environment variables and optional overrides.

**Parameters:**

- `config_file` (Path, optional): Path to YAML config file (not yet implemented)
- `overrides` (dict, optional): Runtime override values

**Returns:**

- `Config`: Loaded configuration

**Environment Variables:**

- `MCP_WEB_FETCHER_TIMEOUT`: HTTP timeout (default: 30)
- `MCP_WEB_CHUNKER_CHUNK_SIZE`: Chunk size in tokens (default: 512)
- `MCP_WEB_SUMMARIZER_MODEL`: LLM model (default: 'gpt-4o-mini')
- `MCP_WEB_CACHE_DIR`: Cache directory (default: '~/.cache/mcp-web')
- See [ARCHITECTURE.md](ARCHITECTURE.md#configuration-strategy) for full list

---

## Utils

### `TokenCounter`

Token counting using tiktoken.

#### Constructor

```python
def __init__(self, encoding_name: str = "cl100k_base")
```

---

#### `count_tokens()`

```python
def count_tokens(text: str) -> int
```

Count tokens in text.

---

#### `truncate_to_tokens()`

```python
def truncate_to_tokens(text: str, max_tokens: int) -> str
```

Truncate text to maximum token count.

---

### Utility Functions

#### `validate_url(url: str) -> bool`

Validate URL format (http/https schemes only).

#### `normalize_url(url: str) -> str`

Normalize URL (remove fragments, sort query params).

#### `format_markdown_summary(summary: str, sources: List[str], metadata: Optional[dict] = None) -> str`

Format summary with citations and metadata.

#### `extract_code_blocks(text: str) -> List[tuple[str, str]]`

Extract code blocks from Markdown text. Returns list of (language, code) tuples.

#### `sanitize_filename(filename: str) -> str`

Sanitize string for use as filename.

---

## Metrics

### `MetricsCollector`

Centralized metrics collection and export.

#### Constructor

```python
def __init__(
 enabled: bool = True,
 export_path: Optional[Path] = None,
)
```

---

#### Recording Methods

```python
def record_fetch(url: str, method: str, duration_ms: float, status_code: int, content_size: int, success: bool, error: Optional[str] = None) -> None

def record_extraction(url: str, content_length: int, extracted_length: int, duration_ms: float, success: bool, error: Optional[str] = None) -> None

def record_chunking(content_length: int, num_chunks: int, avg_chunk_size: float, duration_ms: float) -> None

def record_summarization(input_tokens: int, output_tokens: int, model: str, duration_ms: float, success: bool, error: Optional[str] = None) -> None

def record_cache_operation(operation: str, key: str, size_bytes: Optional[int] = None) -> None

def record_error(module: str, error: Exception, context: Optional[Dict] = None) -> None
```

---

#### `export_metrics()`

```python
def export_metrics() -> Dict[str, Any]
```

Export all metrics as dictionary with aggregated statistics.

**Returns:**

- `dict`: Contains summary, counters, avg_durations_ms, errors

---

#### `timer()`

```python
@contextmanager
def timer(operation: str) -> Iterator[None]
```

Context manager for timing operations.

**Example:**

```python
metrics = MetricsCollector()
with metrics.timer("fetch"):
 # operation
 pass
```

---

### `get_metrics_collector()`

```python
def get_metrics_collector() -> MetricsCollector
```

Get or create global metrics collector instance.

---

### `configure_logging()`

```python
def configure_logging(level: str = "INFO", structured: bool = True) -> None
```

Configure structlog logging.

**Parameters:**

- `level` (str): Log level (DEBUG, INFO, WARNING, ERROR)
- `structured` (bool): Use structured JSON output

---

## Type Definitions

### Enums & Literals

```python
# Chunking strategies
ChunkStrategy = Literal["hierarchical", "semantic", "fixed"]

# Cache eviction policies
EvictionPolicy = Literal["lru", "lfu"]

# Log levels
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR"]
```

---

## Error Handling

All async functions may raise exceptions. Common exceptions:

- `httpx.HTTPError`: Network/HTTP errors
- `playwright.async_api.Error`: Browser automation errors
- `openai.OpenAIError`: LLM API errors
- `Exception`: Generic errors with descriptive messages

Always use try-except blocks and check logs for detailed error information.

---

## Best Practices

1. **Resource Cleanup**: Always call `close()` on pipeline/fetcher/summarizer
2. **Configuration**: Use environment variables for deployment, overrides for testing
3. **Caching**: Enable for production, disable for testing
4. **Error Handling**: Handle exceptions gracefully, check metrics for patterns
5. **Token Limits**: Monitor `max_context_tokens` to avoid API errors
6. **Rate Limiting**: Use `max_concurrent` to avoid overwhelming target servers

---

## Examples

See [examples/](../examples/) directory for complete usage examples.

---

**Last Updated:** 2025-10-15
**Version:** 0.1.0
