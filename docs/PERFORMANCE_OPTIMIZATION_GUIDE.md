# Performance Optimization Guide

**Last Updated:** 2025-10-15
**Version:** 0.2.0

---

## Overview

This guide documents the performance optimization work for mcp-web, including implemented optimizations, profiling tools, and best practices for achieving sub-5-second summarization.

### Quick Summary

✅ **Phase 1 Complete**: Parallel map-reduce optimization

- **Implementation**: `asyncio.gather()` for concurrent chunk summarization
- **Expected Improvement**: 10x+ speedup for large documents (30+ chunks)
- **Configuration**: Enabled by default via `parallel_map=True`
- **Backward Compatible**: Can disable and use sequential mode

---

## Table of Contents

1. [Optimization History](#optimization-history)
2. [Profiling Tools](#profiling-tools)
3. [Configuration](#configuration)
4. [Benchmarking](#benchmarking)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Optimization History

### Phase 1: Parallel Map-Reduce (October 2025)

**Problem**: Sequential chunk summarization was the primary bottleneck

- 10 chunks × 3s/chunk = 30 seconds (just for map phase)

**Solution**: Parallel map phase using `asyncio.gather()`

- All chunks summarized concurrently
- Expected: 10x+ speedup for documents with many chunks

**Implementation**: Three map-reduce strategies:

1. **Parallel (default)**: `asyncio.gather()` - fastest
2. **Streaming**: `asyncio.as_completed()` - better UX
3. **Sequential**: Original implementation - fallback

**References**:

- [ADR 0016: Parallel Map-Reduce](adr/0016-parallel-map-reduce-optimization.md)
- [Performance Initiative](initiatives/active/performance-optimization-pipeline.md)

---

## Profiling Tools

### 1. Profiler Module (`src/mcp_web/profiler.py`)

Comprehensive profiling utilities:

```python
from mcp_web.profiler import profile, ProfilerContext, PerformanceCollector

# Decorator profiling
@profile
async def my_function():
    await do_work()

# Context manager profiling
with ProfilerContext("database_query") as ctx:
    result = execute_query()
print(f"Took {ctx.duration_ms:.2f}ms")

# Collect all results
collector = PerformanceCollector.get_instance()
stats = collector.get_statistics()
collector.export_json("/tmp/mcp-web-performance.json")
```

### 2. Benchmark Pipeline Script (`scripts/benchmark_pipeline.py`)

End-to-end pipeline benchmarking:

```bash
# Single URL benchmark
python scripts/benchmark_pipeline.py --url https://python.org

# With profiling
python scripts/benchmark_pipeline.py --url https://python.org --profile

# Export results to temp location
python scripts/benchmark_pipeline.py --url https://python.org --export /tmp/mcp-web-benchmark.json

# Load test
python scripts/benchmark_pipeline.py --load-test --concurrent 10 --requests 100
```

### 3. Component Timer

Track timing for individual components:

```python
from mcp_web.profiler import ComponentTimer

timer = ComponentTimer()

with timer.time("fetch"):
    await fetch_url()

with timer.time("summarize"):
    await summarize()

summary = timer.get_summary()
# {
#   "fetch": {"count": 1, "mean_ms": 1500, ...},
#   "summarize": {"count": 1, "mean_ms": 3000, ...}
# }
```

### 4. cProfile Integration

For detailed Python-level profiling:

```python
from mcp_web.profiler import cprofile_context

with cprofile_context("profile.stats", top_n=50):
    expensive_function()

# Analyze with:
# python -m pstats profile.stats
```

---

## Configuration

### Map-Reduce Strategy

Control how map-reduce summarization is performed:

```bash
# Environment variables
export MCP_WEB_SUMMARIZER_PARALLEL_MAP=true      # Parallel (default, fastest)
export MCP_WEB_SUMMARIZER_STREAMING_MAP=false    # Streaming (better UX)

# If both false: falls back to sequential (slowest)
```

```python
# Python code
from mcp_web.config import load_config

config = load_config()
config.summarizer.parallel_map = True      # Parallel mode (recommended)
config.summarizer.streaming_map = False    # Set True for progress updates
```

### Choosing the Right Strategy

| Strategy | Best For | Speed | UX | Trade-offs |
|----------|----------|-------|-----|------------|
| **Parallel** | Production, performance | ⚡⚡⚡ | ⭐⭐ | Fastest, no progress updates |
| **Streaming** | Interactive, long docs | ⚡⚡ | ⭐⭐⭐ | Progress updates, slightly slower |
| **Sequential** | Debugging, fallback | ⚡ | ⭐ | Slowest, most predictable |

**Recommendation**: Use Parallel (default) for best performance.

### Map-Reduce Threshold

Control when to use map-reduce vs direct summarization:

```bash
export MCP_WEB_SUMMARIZER_MAP_REDUCE_THRESHOLD=8000  # tokens
```

- **< threshold**: Direct summarization (single LLM call)
- **≥ threshold**: Map-reduce (parallel chunk summarization)

**Tuning**:

- Lower threshold → More use of map-reduce → Better for very long docs
- Higher threshold → More direct summarization → Better for shorter docs

---

## Benchmarking

### Running Benchmarks

```bash
# Quick benchmark (uses pytest-benchmark)
task test:bench

# Full pipeline benchmark
python scripts/benchmark_pipeline.py --url https://example.com

# Compare different strategies
MCP_WEB_SUMMARIZER_PARALLEL_MAP=true python scripts/benchmark_pipeline.py --url URL
MCP_WEB_SUMMARIZER_PARALLEL_MAP=false python scripts/benchmark_pipeline.py --url URL
```

### Benchmark Expectations

| Document Size | Chunks | Sequential | Parallel | Expected Speedup |
|---------------|--------|------------|----------|------------------|
| 5k tokens     | 2-3    | ~8s        | ~4s      | 2x               |
| 10k tokens    | 5-6    | ~18s       | ~4s      | 4-5x             |
| 30k tokens    | 12-15  | ~45s       | ~5s      | 8-10x            |
| 100k tokens   | 40-50  | ~2min      | ~10s     | 12x+             |

**Assumptions:** 3s average LLM call latency, ~1s reduce phase

### Interpreting Results

Look for:

1. **Component breakdown**: Which stage is slowest?
2. **Map phase time**: Should be ~3-5s regardless of chunk count (with parallel)
3. **Reduce phase time**: Should be 1-2s
4. **Cache hit rate**: Higher = better performance

Example output:

```text
================================================================================
Benchmarking: https://python.org
Cache: Enabled
================================================================================

✓ Fetch: 1.2s (text/html)
✓ Extract: 450ms (8,234 tokens)
✓ Chunk: 85ms (12 chunks, 8,156 tokens)
✓ Summarize: 4.1s (1,234 tokens)

================================================================================
Total: 5.84s
================================================================================

Component Breakdown:
  Fetch:        1.20s (20.5%)
  Extract:      450ms  (7.7%)
  Chunk:         85ms  (1.5%)
  Summarize:    4.10s (70.3%)  ← Primary bottleneck
```

---

## Best Practices

### 1. Enable Caching

Caching provides massive performance gains for repeated requests:

```python
# Default: cache enabled with 7-day TTL
config.cache.enabled = True
config.cache.ttl = 7 * 24 * 3600  # 7 days
```

**Impact**: Cache hits return in ~50ms vs 5+ seconds

### 2. Use Parallel Map-Reduce

Always use parallel mode unless you have a specific reason not to:

```bash
export MCP_WEB_SUMMARIZER_PARALLEL_MAP=true  # Default, recommended
```

### 3. Tune Chunk Size

Larger chunks = fewer LLM calls = faster (but may reduce quality):

```bash
export MCP_WEB_CHUNKER_CHUNK_SIZE=768  # Default: 512
```

**Tuning guidance**:

- 512: Best quality, slower
- 768: Good balance (recommended for performance)
- 1024: Fastest, may reduce quality

### 4. Optimize Concurrency

For fetching multiple URLs:

```bash
export MCP_WEB_FETCHER_MAX_CONCURRENT=10  # Default: 5
```

**Warning**: Too high may hit rate limits

### 5. Monitor Performance

Use profiling in development:

```python
from mcp_web.profiler import PerformanceCollector

collector = PerformanceCollector.get_instance()

# ... run your code ...

stats = collector.get_statistics()
print(f"Average summarization: {stats['summarize_chunks']['mean_ms']:.2f}ms")
```

### 6. Handle Rate Limits

If you hit API rate limits with parallel map:

```python
# Add semaphore rate limiting (future enhancement)
# For now: reduce chunk size to create fewer chunks
config.chunker.chunk_size = 1024  # Larger chunks = fewer API calls
```

---

## Troubleshooting

### Problem: Slow summarization despite parallel mode

**Check**:

1. Is parallel mode actually enabled?

   ```bash
   uv run python -c "from mcp_web.config import load_config; c=load_config(); print(f'Parallel: {c.summarizer.parallel_map}')"
   ```

2. Are you hitting map-reduce threshold?
   - Documents < 8000 tokens use direct summarization (no parallelization)

3. Network latency?
   - Run with profiling to see actual LLM call times

   ```bash
   python scripts/benchmark_pipeline.py --url URL --profile
   ```

### Problem: API rate limit errors

**Solutions**:

1. Reduce concurrent operations:

   ```bash
   export MCP_WEB_FETCHER_MAX_CONCURRENT=3
   ```

2. Use larger chunks (fewer API calls):

   ```bash
   export MCP_WEB_CHUNKER_CHUNK_SIZE=1024
   ```

3. Add delays between requests (future: semaphore rate limiting)

### Problem: Quality degradation

**Check**:

1. Chunk size not too large:

   ```bash
   export MCP_WEB_CHUNKER_CHUNK_SIZE=512  # Don't exceed 1024
   ```

2. Run golden tests to validate:

   ```bash
   task test:golden
   ```

3. Compare with sequential mode:

   ```bash
   MCP_WEB_SUMMARIZER_PARALLEL_MAP=false task test:manual URL=your_url
   ```

### Problem: Memory usage

**Solutions**:

1. Reduce max chunk size:

   ```bash
   export MCP_WEB_CHUNKER_MAX_CHUNK_SIZE=1024
   ```

2. Clear cache periodically:

   ```bash
   task dev:clean:cache
   ```

---

## Future Optimizations

### Phase 2 (Planned)

- **Batch API integration** (50% cost savings for offline processing)
- **Adaptive chunking** (adjust size based on document characteristics)
- **Chunk-level caching** (cache summaries of common chunks)
- **Concurrency tuning** (automatic rate limit detection)

### Phase 3 (Future)

- **Multi-model strategy** (fast model for map, quality model for reduce)
- **Speculative summarization** (pipeline parallelism)
- **GPU-accelerated chunking** (for massive documents)

---

## References

- [Performance Initiative](initiatives/active/performance-optimization-pipeline.md)
- [ADR 0016: Parallel Map-Reduce](adr/0016-parallel-map-reduce-optimization.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [API Reference](API.md)

### External Resources

- [Mastering Python asyncio.gather](https://python.useinstructor.com/blog/2023/11/13/learn-async/)
- [Optimizing OpenAI API Performance](https://signoz.io/guides/open-ai-api-latency/)
- [AI Batch Processing 2025](https://adhavpavan.medium.com/ai-batch-processing-openai-claude-and-gemini-2025-94107c024a10)

---

## Support

For questions or issues:

1. Check [Troubleshooting](#troubleshooting) section
2. Review [Performance Initiative](initiatives/active/performance-optimization-pipeline.md)
3. Run benchmarks to gather data
4. Open an issue with benchmark results
