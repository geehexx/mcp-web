# Performance Testing Guide

**Purpose:** Guide for running performance benchmarks and regression testing in mcp-web.

**Last Updated:** 2025-10-20

---

## Overview

This project uses `pytest-benchmark` for performance testing with automated regression detection in CI. Benchmarks track the performance of critical operations (chunking, extraction, summarization, caching) to catch regressions early.

---

## Quick Start

### Run All Benchmarks

```bash
# Run benchmarks (single process for accurate timing)
task test:bench:single

# Run benchmarks in parallel (faster, but less precise)
task test:bench
```

### Check for Regressions

```bash
# Compare against baseline and fail if >20% slower
task test:bench:regression
```

### Update Baseline

```bash
# After verified performance improvements, update baseline
task test:bench:baseline
```

---

## Benchmark Categories

### 1. Token Operations

- **test_token_counting_speed** - Token counting with tiktoken
- **test_token_truncation_speed** - Token truncation performance

**Optimization:** CPU-bound, benefits from efficient encoding

### 2. Text Chunking

- **test_hierarchical_chunking_speed** - Markdown-aware hierarchical chunking
- **test_semantic_chunking_speed** - Sentence-based semantic chunking
- **test_fixed_chunking_speed** - Fixed-size token chunking

**Optimization:** Memory-efficient chunking for large documents

### 3. Content Extraction

- **test_extraction_speed** - HTML content extraction with trafilatura

**Optimization:** Fast DOM parsing and text extraction

### 4. Cache Operations

- **test_cache_write_speed** - Cache write performance (10 items)
- **test_cache_read_speed** - Cache read performance (10 operations)

**Optimization:** Async I/O, filesystem-based caching

### 5. URL Processing

- **test_url_validation_speed** - URL validation (60 URLs)
- **test_url_normalization_speed** - URL normalization (60 URLs)

**Optimization:** Fast URL parsing and validation

### 6. Summarization (Mocked)

- **test_direct_summarization_speed** - Direct LLM summarization
- **test_map_reduce_summarization_speed** - Map-reduce summarization

**Note:** Uses mocked LLM responses for deterministic benchmarking

---

## CI Integration

### GitHub Actions Workflow

**File:** `.github/workflows/performance-regression.yml`

**Triggers:**

- Pull requests to `main` (compare against cached baseline)
- Pushes to `main` (update cached baseline)

**Behavior:**

- Runs all benchmarks with `--benchmark-only`
- Compares against previous results from GitHub Actions cache
- Fails PR if any test is >20% slower than baseline
- Posts comment on PR with performance summary
- Caches results for future comparisons

**Alert Threshold:** 120% (fails if >20% slower)

### Viewing Results

1. **PR Comments:** Performance summary automatically posted
2. **Artifacts:** Download `benchmark-results` artifact for full JSON
3. **Logs:** Check workflow logs for detailed timing

---

## Local Regression Testing

### Comparing Against Baseline

```bash
# Run benchmarks and compare (exit 1 if regression detected)
task test:bench:regression

# Generate new baseline after performance improvements
task test:bench:baseline
```

### Manual Comparison

```bash
# Run current benchmarks
uv run pytest -m benchmark --benchmark-only --benchmark-json=current.json -o addopts=''

# Compare against baseline
python scripts/check_performance_regression.py current.json .benchmarks/baseline.json --threshold 1.2
```

**Output:**

```text
✅ No performance regressions detected (12 tests checked)
   Threshold: 20% slower
```

Or if regressions found:

```text
❌ Performance regressions detected (2/12 tests)
   Threshold: 20% slower

Slowest Regressions:
Test                                                Baseline        Current         Change
---------------------------------------------------------------------------------------------------
test_hierarchical_chunking_speed                    11.838ms        15.200ms        +28.4%
test_cache_write_speed                              1.597ms         2.100ms         +31.5%
```

---

## Baseline Management

### When to Update Baseline

**Update baseline after:**

- Verified performance improvements (faster code)
- Major refactoring with acceptable perf changes
- Infrastructure changes (new Python version, dependencies)

**Never update baseline:**

- To hide regressions
- Without understanding the cause of changes
- Before investigating slowdowns

### Update Process

1. **Verify changes are intentional:**

   ```bash
   # Compare current vs baseline
   task test:bench:regression
   ```

2. **Review what changed:**

   ```bash
   # See detailed report
   python scripts/check_performance_regression.py output.json .benchmarks/baseline.json --threshold 1.0
   ```

3. **Update if justified:**

   ```bash
   task test:bench:baseline
   git add .benchmarks/baseline.json
   git commit -m "perf: update performance baseline after [reason]"
   ```

---

## Benchmark Configuration

### Thresholds

- **CI Threshold:** 120% (20% slower = fail)
- **Local Threshold:** Configurable via `--threshold` flag
- **Recommended:** 1.1-1.2 (10-20% tolerance)

### pytest-benchmark Settings

**File:** `tests/benchmarks/conftest.py`

- **Mocked LLM:** Deterministic responses, no API calls
- **Iterations:** 5 iterations per round
- **Rounds:** 3 rounds per test
- **Warmup:** Automatic calibration

### Parallel Execution

```bash
# Parallel benchmarks (less accurate, but faster)
task test:bench  # Uses pytest-xdist

# Single process (accurate timing)
task test:bench:single
```

**Note:** Some benchmarks use `@pytest.mark.xdist_group` to avoid contention

---

## Performance Optimization Tips

### 1. Profile Before Optimizing

```bash
# Profile with cProfile
task bench:profile

# View top 30 slowest functions
python -c 'import pstats; p = pstats.Stats("profile.stats"); p.sort_stats("cumulative"); p.print_stats(30)'
```

### 2. Memory Profiling

Benchmarks include memory usage tests:

```bash
# Run memory tests
uv run pytest tests/benchmarks/test_performance.py::TestMemoryUsage -v
```

### 3. Concurrency Testing

Benchmarks include concurrency tests to verify speedup:

```bash
# Test concurrent chunking speedup
uv run pytest tests/benchmarks/test_performance.py::TestConcurrency -v
```

---

## Troubleshooting

### Inconsistent Results

**Problem:** Benchmark times vary significantly between runs

**Solutions:**

- Close background applications
- Run single-process: `task test:bench:single`
- Increase rounds/iterations in test
- Use `--benchmark-disable-gc` to disable GC during tests

### CI Failures

**Problem:** Benchmarks pass locally but fail in CI

**Causes:**

- CI runners have variable performance
- Different CPU/memory than local
- Concurrent workflows

**Solutions:**

- Increase threshold slightly (1.25-1.3)
- Use cache-based comparison (already implemented)
- Run multiple times to average out noise

### Missing Baseline

**Problem:** `.benchmarks/baseline.json` not found

**Solution:**

```bash
# Generate initial baseline
task test:bench:baseline
git add .benchmarks/baseline.json
git commit -m "perf: add initial performance baseline"
```

---

## Best Practices

1. **Run benchmarks before commits:** `task test:bench:regression`
2. **Update baseline only after review:** Don't hide regressions
3. **Document perf changes:** Explain why baseline changed
4. **Use mocked data:** Keep benchmarks deterministic
5. **Monitor trends:** Watch for gradual slowdowns over time
6. **Profile first:** Don't optimize without data

---

## References

- [pytest-benchmark Documentation](https://pytest-benchmark.readthedocs.io/)
- [github-action-benchmark](https://github.com/benchmark-action/github-action-benchmark)
- [Performance Optimization Guide](https://towardsdatascience.com/benchmarking-pytest-with-cicd-using-github-action-17af32b4a30b/)

---

**Maintained By:** mcp-web core team
**Related:**

- [Testing Guide](../CONTRIBUTING.md#testing)
- [CI/CD Workflows](../../.github/workflows/)
- [Benchmark Tests](../../tests/benchmarks/)
