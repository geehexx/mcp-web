# ADR-0001: Use httpx with Playwright Fallback

**Status:** Implemented

**Date:** 2025-10-15

**Deciders:** Core team

**Tags:** architecture, performance, fetching

---

## Context

The mcp-web tool needs to fetch HTML content from diverse websites to extract and summarize information. Websites vary significantly in their implementation:

- **Static HTML:** Traditional server-rendered pages (news sites, blogs, documentation)
- **Client-side rendered (CSR):** Single-page applications using React, Vue, Angular
- **Hybrid:** Progressive enhancement, partial server rendering

The challenge is to handle both efficiently:
- Static sites need fast fetching (minimize latency)
- CSR sites require JavaScript execution to render content
- Some sites use anti-bot measures that may block simple HTTP clients

Our requirements:
1. Fast fetching for common static sites (>80% of web pages)
2. Reliable extraction from JS-heavy sites
3. Async/await compatibility for high concurrency
4. Reasonable resource usage (memory, CPU)

## Decision

We will use **httpx** as the primary fetch method with **Playwright** as a fallback:

1. **Primary attempt:** Use `httpx.AsyncClient` to fetch HTML
   - Fast HTTP/2 client with connection pooling
   - Minimal overhead (~50-100ms per request)
   - Async-native design

2. **Fallback trigger:** If httpx fails OR content appears incomplete
   - HTTP error status (4xx, 5xx)
   - Empty or minimal body (<100 bytes)
   - Detection of JS-rendered markers (`<div id="root"></div>` with no content)

3. **Fallback method:** Launch Playwright headless browser
   - Execute JavaScript to render page
   - Wait for network idle or specific selectors
   - Extract final rendered HTML

## Alternatives Considered

### Alternative 1: Playwright Only

**Description:** Use Playwright for all requests, no httpx

**Pros:**
- Simpler code path (single method)
- Guaranteed JS execution
- Handles all anti-bot measures

**Cons:**
- 10-100x slower for static sites (~2-5s vs ~100ms)
- High memory usage (~100MB per browser instance)
- CPU intensive (Chromium process overhead)
- Browser binary dependencies (~200MB installation)

**Reason for rejection:** Performance penalty unacceptable for majority use case (static sites)

### Alternative 2: httpx Only

**Description:** Use httpx for all requests, no browser fallback

**Pros:**
- Fastest possible fetching
- Minimal dependencies
- Low resource usage

**Cons:**
- Fails on JS-rendered content (20% of modern web)
- Cannot handle SPAs, dynamic loading
- No anti-bot evasion capabilities

**Reason for rejection:** Too many sites would fail, reducing tool utility

### Alternative 3: requests Library

**Description:** Use synchronous `requests` library instead of httpx

**Pros:**
- More mature, widely used
- Extensive middleware ecosystem

**Cons:**
- Not async-native (blocks event loop or requires threads)
- Slower than httpx for concurrent requests
- HTTP/1.1 only (no HTTP/2 benefits)

**Reason for rejection:** Async requirement and performance needs favor httpx

## Consequences

### Positive Consequences

- **Fast happy path:** Static sites fetch in ~100ms (10-50x faster than browser)
- **Robust fallback:** JS-heavy sites still work (2-5s latency)
- **High concurrency:** Can fetch 10-100 URLs concurrently with httpx
- **Automatic optimization:** System learns which sites need browser over time (with caching)

### Negative Consequences

- **Complex logic:** Need to detect when fallback is necessary
- **Resource variability:** Memory usage varies (10MB httpx vs 100MB+ Playwright)
- **Dependency size:** Playwright adds ~200MB to installation
- **Browser maintenance:** Need to keep Chromium updated

### Neutral Consequences

- **Caching importance:** Cache effectiveness critical for performance
- **Monitoring needs:** Should track httpx vs Playwright usage ratio
- **Configuration options:** Users may want to prefer one method (fast-only or thorough mode)

## Implementation

**Key files:**
- `src/mcp_web/fetcher.py` - Core fetching logic with fallback
- `src/mcp_web/config.py` - Timeout and User-Agent configuration

**Dependencies:**
- `httpx >= 0.27.0` - Async HTTP client
- `playwright >= 1.41.0` - Browser automation

**Configuration:**
```python
FetcherSettings(
    timeout: int = 30,              # HTTP timeout
    user_agent: str = "mcp-web/1.0",
    playwright_timeout: int = 60,   # Browser timeout (longer)
    enable_fallback: bool = True,   # Can disable for speed
)
```

**Metrics tracked:**
- Fetch method used (httpx vs playwright)
- Fetch duration
- Success/failure rate by method

## References

- [httpx documentation](https://www.python-httpx.org/)
- [Playwright Python](https://playwright.dev/python/)
- [Async HTTP benchmarks](https://www.python-httpx.org/async/)
- Related ADR: [0002-use-trafilatura-extraction.md](0002-use-trafilatura-extraction.md)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-10-15 | Initial proposal and acceptance | Cascade |
| 2025-10-15 | Implemented in v0.1.0 | Cascade |
