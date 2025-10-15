# ADR-0009: Use Disk Cache with 7-Day TTL

**Status:** Implemented

**Date:** 2025-10-15

**Deciders:** Core team

**Tags:** architecture, performance, caching

---

## Context

The mcp-web tool performs expensive operations that should be cached:

1. **URL fetching:** HTTP requests (50-500ms)
2. **Content extraction:** HTML parsing and cleaning (50-200ms)
3. **LLM summarization:** API calls ($0.001-0.01 per summary, 2-10s latency)

Without caching:

- Repeated queries to same URL = redundant work
- High API costs for frequently accessed content
- Poor user experience (waiting for repeated processing)

Caching challenges:

- **Freshness:** Content may change over time
- **Storage:** Cache size must be bounded
- **Persistence:** Cache should survive process restarts
- **Invalidation:** Need strategy for stale content

Our requirements:

1. Persist cache across sessions (not just in-memory)
2. Reasonable freshness guarantees (content not too stale)
3. Automatic eviction to prevent unbounded growth
4. Fast cache lookups (<1ms)
5. Transparent to application logic (minimal code impact)

## Decision

We will use **disk-based caching** with **7-day TTL** using the `diskcache` library:

### Cache Strategy

1. **Storage location:** `~/.cache/mcp-web/` (XDG cache directory)
2. **Time-to-live (TTL):** 7 days for all cached entries
3. **Eviction policy:** LRU (Least Recently Used) when size limit reached
4. **Size limit:** 1GB maximum cache size
5. **Cache levels:**

- **L1:** Fetched HTML (raw, before extraction)
- **L2:** Extracted content (after trafilatura)
- **L3:** Summaries (final output)

### HTTP Cache Validation

- Use ETags and Last-Modified headers when available
- Conditional requests (If-None-Match, If-Modified-Since)
- Server returns 304 Not Modified → use cached version
- Cache hit even if content unchanged upstream

### Cache Key Design

```python
# HTML fetch cache
key = f"fetch:{url_hash}:{method}"

# Extraction cache
key = f"extract:{content_hash}:{extractor_config_hash}"

# Summary cache
key = f"summary:{content_hash}:{query_hash}:{model}:{prompt_hash}"
```

## Alternatives Considered

### Alternative 1: In-Memory Cache Only

**Description:** Use Python dictionary or `functools.lru_cache` for caching

**Pros:**

- Fastest access (no disk I/O)
- Simplest implementation
- No external dependencies

**Cons:**

- **Lost on restart:** Cache cleared every session
- **Memory limited:** Cannot cache large corpus
- **No persistence:** Poor for long-running agents
- **Single process:** Cannot share between instances

**Reason for rejection:** Persistence requirement not met

### Alternative 2: Redis or External Cache

**Description:** Use Redis, Memcached, or similar for caching

**Pros:**

- Very fast (network overhead minimal on localhost)
- Shared between processes
- Rich eviction policies
- Production-ready

**Cons:**

- **Operational overhead:** Requires running Redis server
- **Overkill:** Single-user tool doesn't need distributed cache
- **Complexity:** Connection management, error handling
- **Dependencies:** External service requirement

**Reason for rejection:** Too complex for single-user tool

### Alternative 3: Longer TTL (30 days)

**Description:** Use same disk cache but with 30-day TTL

**Pros:**

- Fewer cache misses
- Lower API costs
- Better performance

**Cons:**

- **Stale content:** News articles, documentation updates missed
- **Storage growth:** More entries retained
- **Staleness risk:** Content may be significantly outdated

**Reason for rejection:** 7 days better balances freshness and efficiency

### Alternative 4: No TTL (Manual Invalidation)

**Description:** Cache indefinitely, require explicit invalidation

**Pros:**

- Maximum cache hit rate
- Lowest API costs
- Simplest logic (no expiration checking)

**Cons:**

- **Unbounded staleness:** Content could be years old
- **User burden:** Must remember to invalidate
- **Poor UX:** Unexpected stale results
- **Storage growth:** No automatic cleanup

**Reason for rejection:** Automatic freshness required

## Consequences

### Positive Consequences

- **Fast repeated queries:** Cache hits ~1-5ms (vs 2-10s API call)
- **Cost reduction:** 50-80% fewer API calls for typical usage
- **Persistence:** Cache survives restarts, benefits multi-session work
- **HTTP efficiency:** Proper use of ETags/Last-Modified headers
- **Bounded storage:** LRU eviction prevents unbounded growth

### Negative Consequences

- **Disk usage:** Up to 1GB cache directory
- **Stale content:** May serve 7-day-old content (usually acceptable)
- **Cold start:** First query always slow (cache miss)
- **Invalidation complexity:** No automatic detection of content changes

### Neutral Consequences

- **Cache tuning:** TTL and size limits should be configurable
- **Monitoring:** Should expose cache hit/miss ratio
- **Cleanup:** Users can manually clear cache if needed
- **Debugging:** Cache can hide upstream changes during development

## Implementation

**Key files:**

- `src/mcp_web/cache.py` - Cache management and operations
- `src/mcp_web/config.py` - Cache configuration settings

**Dependencies:**

- `diskcache >= 5.6.0` - Disk-based cache library

**Configuration:**

```python
CacheSettings(
 dir: str = "~/.cache/mcp-web", # Cache directory
 ttl: int = 604800, # 7 days in seconds
 size_limit: int = 1073741824, # 1GB in bytes
 eviction_policy: str = "least-recently-used",
 enabled: bool = True, # Can disable for debugging
)
```

**Cache management tools:**

```python
# Get cache statistics
stats = get_cache_stats()
# {'size': '234 MB', 'entries': 1523, 'hit_rate': 0.73}

# Clear all cache
clear_cache()

# Clear specific cache level
clear_cache(level="summaries")

# Prune expired entries
prune_cache()
```

**HTTP cache validation:**

```python
# Fetch with cache validation
cached_html, headers = fetch_from_cache(url)
if cached_html:
 response = httpx.get(url, headers={
 'If-None-Match': headers.get('etag'),
 'If-Modified-Since': headers.get('last-modified')
 })
 if response.status_code == 304:
 return cached_html # Content unchanged
```

## References

- [HTTP Caching (MDN)](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [diskcache Documentation](http://www.grantjenks.com/docs/diskcache/)
- [XDG Base Directory Specification](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [Cache Eviction Policies](https://en.wikipedia.org/wiki/Cache_replacement_policies)
- Related ADR: [0001-use-httpx-playwright-fallback.md](0001-use-httpx-playwright-fallback.md)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-10-15 | Initial proposal and acceptance | Cascade |
| 2025-10-15 | Implemented in v0.1.0 | Cascade |
