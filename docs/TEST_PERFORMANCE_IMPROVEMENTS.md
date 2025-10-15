# Test & Benchmark Performance Improvements

**Date:** 2025-10-15
**Status:** In Progress
**Related:** [Performance Optimization Initiative](initiatives/active/performance-optimization-pipeline.md)

---

## Overview

This document tracks improvements to test and benchmark performance, enabling faster development cycles and more efficient CI/CD pipelines.

## Current State (After Improvements)

### Test Performance

| Category | Before | After | Improvement | Notes |
|----------|--------|-------|-------------|-------|
| Rate limiting test | 500ms | 50ms | 10x faster | Fixed concurrent tracking logic |
| URL validation tests | ~500ms (loop) | 50ms (parametrize) | 10x faster | Parametrized tests |
| Fast test suite | ~70s | ~10s (est) | 7x faster | Excluding slow tests |
| Security test suite | N/A | 1.3s | New metric | Parallel execution |

### Benchmark Performance

| Improvement | Impact | Status |
|-------------|--------|--------|
| Parallel benchmark execution | Pending validation | Implemented |
| xdist_group markers | Prevents resource contention | Implemented |
| Test duration tracking | Enables smart scheduling | Implemented |
| io_bound markers | Better worker distribution | Implemented |

---

## Improvements Implemented

### 1. Test Infrastructure

✅ **Parallel Execution**
- Added `pytest-xdist` with `--numprocesses=auto`
- Added `sitecustomize.py` for coverage in parallel mode
- Reference: [PyPI 81% faster (Trail of Bits, May 2025)](https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/)

✅ **Time Manipulation**
- Added `freezegun` for testing time-dependent code
- Optimized rate limiting tests to avoid real-time waits
- Realistic timing test moved to `@pytest.mark.slow`

✅ **Better Test Output**
- Added `pytest-sugar` for clean, organized results
- Added `--durations=10` to identify slow tests
- Added `--store-durations` for test scheduling

✅ **Test Duration Tracking**
- Added `pytest-split` for duration-based scheduling
- Stores durations in `.test_durations` file
- Enables running slowest tests first for optimal parallelism

### 2. Test Organization

✅ **Markers Added**
```python
@pytest.mark.io_bound  # Suitable for high concurrency
@pytest.mark.slow      # Tests >1s, excluded from fast runs
@pytest.mark.xdist_group(name="cache")  # Prevent resource contention
```

✅ **Task Commands**
```bash
task test:fast              # Exclude slow tests (10s vs 70s)
task test:bench             # Parallel benchmarks
task test:bench:single      # Single process for accurate timing
task test:bench:save        # Save results for comparison
```

### 3. Test Optimizations

✅ **Rate Limiting Test**
- **Before**: Sequential 15 requests, 500ms wait
- **After**: Concurrent validation, 50ms
- **Technique**: Test concurrent limits, not time-based delays

✅ **URL Validation Tests**
- **Before**: Loop-based tests (slow, poor failure reporting)
- **After**: Parametrized tests (fast, clear failures)
- **Benefit**: 10x faster, better pytest output

✅ **Benchmark Grouping**
```python
@pytest.mark.xdist_group(name="cache")
class TestCachePerformance:
    # Prevents multiple workers from hitting same cache
```

---

## Remaining Optimizations

### High Priority

🔴 **Benchmark Timeout Issues**
- **Problem**: Benchmarks timeout after 4 tests
- **Root cause**: Summarization still too slow (waiting for LLM)
- **Solution**: Mock LLM responses for benchmarks
- **Impact**: Critical - blocks benchmark baseline

🔴 **Parallel Map-Reduce Not Validated**
- **Problem**: Can't run benchmarks to measure speedup
- **Solution**: Fix timeout issue first
- **Expected**: 10x speedup for large documents

### Medium Priority

🟡 **Pipeline Streaming**
- **Concept**: Start chunking while extraction is ongoing
- **Benefit**: Reduce idle time between pipeline stages
- **Complexity**: Medium - requires streaming APIs
- **Impact**: 15-25% estimated improvement

🟡 **Memory Optimization**
- **Current**: All chunks loaded in memory
- **Issue**: Memory pressure with large documents
- **Solution**: Streaming chunk processing
- **Priority**: Medium (not blocking current work)

🟡 **Adaptive Benchmarking**
- **Concept**: Run benchmarks in parallel, measure CPU time
- **Reference**: `traffic-simulator` project (Bazel-based)
- **Benefit**: Accurate timing despite parallel execution
- **Complexity**: High - requires CPU time measurement

### Low Priority

⚪ **Green Threads / Cooperative Concurrency**
- **Concept**: Use libevent/gevent for high-concurrency IO
- **Benefit**: Lower overhead than asyncio for many connections
- **Complexity**: High - requires rewrite
- **Priority**: Low - asyncio is sufficient for current scale

⚪ **Test Scheduling Optimization**
- **Concept**: Run slowest tests first to minimize wait time
- **Tool**: `pytest-split` with `--splits` and `--group`
- **Benefit**: 10-20% faster CI/CD
- **Priority**: Low - manually optimized for now

---

## Benchmark Mock Strategy

### Problem

Current benchmarks call real LLM APIs, causing:
- Timeouts after 4 tests (300s limit)
- Non-deterministic results
- Cost per benchmark run
- Can't establish baseline

### Solution: Mock LLM Responses

```python
# tests/benchmarks/conftest.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_llm():
    """Mock LLM responses for deterministic benchmarks."""
    with patch('openai.AsyncOpenAI') as mock:
        async_mock = AsyncMock()
        
        # Mock streaming response
        async def mock_stream():
            chunks = ["This ", "is ", "a ", "test ", "summary."]
            for chunk in chunks:
                yield AsyncMock(
                    choices=[AsyncMock(delta=AsyncMock(content=chunk))]
                )
        
        async_mock.chat.completions.create.return_value = mock_stream()
        mock.return_value = async_mock
        yield mock

@pytest.fixture
def mock_summarizer(test_config, mock_llm):
    """Summarizer with mocked LLM."""
    from mcp_web.summarizer import Summarizer
    return Summarizer(test_config.summarizer)
```

**Usage:**
```python
@pytest.mark.benchmark
def test_summarization_speed(benchmark, mock_summarizer, sample_chunks):
    result = benchmark(
        lambda: asyncio.run(
            consume_stream(mock_summarizer.summarize_chunks(sample_chunks))
        )
    )
    assert len(result) > 0
```

---

## Performance Targets

### Test Suite

| Target | Current | Goal | Strategy |
|--------|---------|------|----------|
| Fast tests | ~10s | <5s | Parallel + mocks |
| Full test suite | ~70s | <30s | Parallel + smart scheduling |
| Benchmark suite | Timeout | <60s | Mock LLM + parallel |

### Summarization

| Document Size | Current | Target | Strategy |
|---------------|---------|--------|----------|
| 5k tokens | ~8s | <3s | Parallel map-reduce |
| 10k tokens | ~18s | <5s | Parallel map-reduce |
| 30k tokens | ~45s | <10s | Parallel map-reduce |

---

## Implementation Plan

### Phase 1: Fix Blocking Issues ✅

- [x] Add parallel test execution infrastructure
- [x] Optimize slow tests (rate limiting, URL validation)
- [x] Add test duration tracking
- [x] Create fast test task
- [ ] Mock LLM responses for benchmarks (NEXT)
- [ ] Validate parallel map-reduce speedup (BLOCKED by above)

### Phase 2: Pipeline Streaming

- [ ] Add streaming API to extractor
- [ ] Add streaming API to chunker
- [ ] Connect fetcher → extractor → chunker as pipeline
- [ ] Benchmark pipeline vs sequential
- [ ] Document streaming architecture

### Phase 3: Advanced Optimizations

- [ ] Adaptive chunking based on document characteristics
- [ ] Chunk-level caching
- [ ] Smart test scheduling (slowest first)
- [ ] Memory optimization for large documents

---

## Metrics & Monitoring

### Test Duration Tracking

Pytest now tracks test durations in `.test_durations`:
```json
{
  "tests/unit/test_security.py::TestRateLimiter::test_sliding_window": 2.0,
  "tests/unit/test_security.py::TestConsumptionLimits::test_rate_limiting_realistic_timing": 60.07,
  ...
}
```

**Usage:**
```bash
# Run slowest tests first
pytest --splitting-algorithm=duration_based_chunks --splits=4 --group=1
```

### Benchmark Comparison

```bash
# Save baseline
task test:bench:save

# Compare after changes
pytest-benchmark compare
```

---

## References

### External Resources

- [PyPI 81% Faster Test Suite](https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/)
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/)
- [Freezegun Guide](https://pytest-with-eric.com/plugins/python-freezegun/)
- [pytest-benchmark Best Practices](https://pytest-benchmark.readthedocs.io/)

### Internal Documentation

- [Performance Optimization Initiative](initiatives/active/performance-optimization-pipeline.md)
- [ADR 0016: Parallel Map-Reduce](adr/0016-parallel-map-reduce-optimization.md)
- [Performance Optimization Guide](PERFORMANCE_OPTIMIZATION_GUIDE.md)

---

## Next Actions

1. 🔴 **Create mock LLM fixture for benchmarks** - Unblocks baseline measurement
2. 🔴 **Run benchmark suite successfully** - Validates parallel map-reduce
3. 🟡 **Measure actual speedup** - Compare sequential vs parallel
4. 🟡 **Implement pipeline streaming** - 15-25% additional improvement
5. 🟢 **Document findings** - Update performance guide with real metrics

---

**Last Updated:** 2025-10-15
**Status:** Test infrastructure complete, benchmarks blocked by LLM mocking
