---
description: Optimization strategies for batch and parallel operations
category: Reference Guide
---

# Batch Operations Guide

**Purpose:** Strategies and best practices for optimizing batch and parallel operations in workflows.

**Used By:** Workflows processing multiple files, URLs, or records

---

## Overview

Batch operations can be 3-10x faster than sequential processing when done correctly. This guide covers optimization strategies for common workflow operations.

---

## Core Principles

### When to Batch

**Use batch operations when:**

- Processing 3+ independent items
- I/O-bound operations (file reads, network requests)
- No dependencies between items
- Memory permits loading all items

**Don't batch when:**

- Items depend on previous results
- CPU-bound operations (better to parallelize differently)
- Memory constraints (process streaming)
- Need incremental results

### Optimal Batch Sizes

| Operation Type | Recommended Batch Size | Reason |
|----------------|------------------------|--------|
| File reads (local) | 10-15 files | Balances parallelism vs overhead |
| File reads (network) | 5-10 files | Network latency dominates |
| URL fetches | 3-5 URLs | Rate limiting, politeness |
| LLM API calls | 1-3 calls | API rate limits |
| Database queries | 50-100 records | DB connection pooling |

---

## Pattern 1: Parallel File Reading

### Basic Parallel Read

**Purpose:** Read multiple files simultaneously

**Implementation:**

```python
# Batch read (parallel)
mcp0_read_multiple_files([
    "/home/gxx/projects/mcp-web/file1.md",
    "/home/gxx/projects/mcp-web/file2.md",
    "/home/gxx/projects/mcp-web/file3.md"
])

# vs Sequential (slow)
for file in files:
    read_file(file)  # 3x slower
```

**Performance:**

- 3-10x faster for I/O-bound operations
- Optimal batch size: 10-15 files
- Diminishing returns beyond 20 files

---

## Pattern 2: Chunked Processing

### Process Large Sets in Chunks

**Purpose:** Avoid memory issues with large datasets

**When to Use:** Processing 20+ items

**Implementation:**

```python
def process_in_chunks(items, chunk_size=10):
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        # Process chunk
        results = mcp0_read_multiple_files(chunk)
        # Yield or store results
        yield results
```

**Benefits:**

- Constant memory usage
- Progress tracking between chunks
- Graceful handling of errors per chunk

**Example:**

```python
# Process 50 files in chunks of 10
all_files = get_file_list()  # 50 files
for chunk_result in process_in_chunks(all_files, 10):
    # Process results from this chunk
    analyze(chunk_result)
```

---

## Pattern 3: Rate Limiting

### Respect External Service Limits

**Purpose:** Avoid API rate limits and bans

**When to Use:** External API calls, web scraping

**Implementation:**

```python
import time

def batch_with_rate_limit(items, batch_size=5, delay=1.0):
    for i in range(0, len(items), batch_size):
        chunk = items[i:i + batch_size]
        # Process chunk
        process_batch(chunk)
        # Wait between batches
        if i + batch_size < len(items):
            time.sleep(delay)
```

**Common Limits:**

| Service | Limit | Recommended Batch |
|---------|-------|-------------------|
| OpenAI API | 3,500 RPM | 3-5 per minute |
| Web scraping | Varies | 1-3 per second |
| GitHub API | 5,000 per hour | 10-20 per minute |

---

## Pattern 4: Error Handling in Batches

### Graceful Batch Failure

**Purpose:** Continue processing even if some items fail

**Implementation:**

```python
def batch_with_error_handling(items):
    results = []
    errors = []

    for batch in chunks(items, 10):
        try:
            batch_results = process_batch(batch)
            results.extend(batch_results)
        except Exception as e:
            # Log error, continue with next batch
            errors.append((batch, str(e)))
            continue

    return results, errors
```

**Strategies:**

- **Fail-fast:** Stop on first error (critical operations)
- **Collect-errors:** Continue, report all errors at end (best-effort)
- **Retry-failed:** Re-process failed items individually

---

## Pattern 5: Progress Tracking

### Monitor Batch Progress

**Purpose:** Provide feedback during long operations

**Implementation:**

```python
def batch_with_progress(items, batch_size=10):
    total = len(items)
    processed = 0

    for chunk in chunks(items, batch_size):
        # Process chunk
        results = process_batch(chunk)
        processed += len(chunk)

        # Report progress
        print(f"Progress: {processed}/{total} ({100*processed//total}%)")

        yield results
```

**Output Example:**

```text
Progress: 10/50 (20%)
Progress: 20/50 (40%)
Progress: 30/50 (60%)
...
```

---

## Pattern 6: Memory Management

### Streaming for Large Datasets

**Purpose:** Process datasets larger than memory

**When to Use:** Processing gigabytes of data

**Implementation:**

```python
def stream_process(items):
    for item in items:
        # Process one at a time
        result = process_item(item)
        # Yield result immediately (don't accumulate)
        yield result
        # Memory freed after yield
```

**Trade-offs:**

- **Streaming:** Low memory, slower (sequential)
- **Batching:** Higher memory, faster (parallel)
- **Hybrid:** Batch within memory limits

---

## Pattern 7: Parallel Command Execution

### Run Multiple Commands Concurrently

**Purpose:** Speed up independent command operations

**Implementation:**

```bash
# Sequential (slow)
git status
task test
task lint

# Parallel (faster for independent ops)
git status & task test & task lint & wait
```

**Note:** Only parallelize truly independent operations.

---

## Performance Benchmarks

### File Reading

| Files | Sequential | Batch (10) | Speedup |
|-------|-----------|-----------|---------|
| 5 | ~5s | ~1s | 5x |
| 10 | ~10s | ~2s | 5x |
| 20 | ~20s | ~4s | 5x |
| 50 | ~50s | ~10s | 5x |

### URL Fetching

| URLs | Sequential | Batch (5) | Speedup |
|------|-----------|----------|---------|
| 3 | ~9s | ~3s | 3x |
| 5 | ~15s | ~5s | 3x |
| 10 | ~30s | ~10s | 3x |

**Assumptions:** I/O-bound operations with typical latency

---

## Anti-Patterns

### ❌ Don't: Batch Dependent Operations

**Bad:**

```python
# These depend on each other!
batch_process([
    "read config",
    "validate config",
    "apply config"
])
```

**Good:**

```python
config = read_config()
validate_config(config)
apply_config(config)
```

### ❌ Don't: Over-Batch

**Bad:**

```python
# 1000 files at once - memory explosion
mcp0_read_multiple_files(all_1000_files)
```

**Good:**

```python
# Chunk into manageable batches
for chunk in chunks(all_1000_files, 15):
    process_batch(chunk)
```

### ❌ Don't: Ignore Rate Limits

**Bad:**

```python
# Hammer API with requests
for url in urls:
    fetch(url)  # Gets banned
```

**Good:**

```python
# Respect rate limits
for batch in chunks(urls, 5):
    fetch_batch(batch)
    time.sleep(1)  # Polite delay
```

---

## Tool-Specific Guidance

### pytest-xdist (Test Parallelization)

```bash
# Auto-detect CPU count
pytest -n auto

# Explicit worker count
pytest -n 4

# Load balancing
pytest -n auto --dist loadscope
```

**Best for:** I/O-bound tests (network, file system)

### MCP Batch Tools

```python
# Batch read multiple files
mcp0_read_multiple_files(paths)

# More efficient than:
for path in paths:
    mcp0_read_text_file(path)
```

---

## Monitoring & Tuning

### Measure Performance

```python
import time

start = time.time()
results = batch_process(items)
duration = time.time() - start

print(f"Processed {len(items)} items in {duration:.2f}s")
print(f"Throughput: {len(items)/duration:.2f} items/s")
```

### Tune Batch Size

**Start conservative, measure, increase:**

1. Start with batch_size=5
2. Measure throughput
3. Double batch size
4. Repeat until performance plateaus
5. Use batch size at plateau point

---

## Common Use Cases

### Case 1: Session Summary Consolidation

```python
# Read 10 session summaries
summaries = mcp0_read_multiple_files([
    "docs/archive/session-summaries/2025-10-*-summary.md"
])

# Process in batches of 10
for chunk in chunks(summaries, 10):
    consolidate_chunk(chunk)
```

### Case 2: Initiative Context Loading

```python
# Load initiative + related files
context_files = [
    initiative_file,
    *source_files,  # 5-10 files
    *test_files,    # 5-10 files
]

# Batch load (1-2 seconds vs 10-20 sequential)
mcp0_read_multiple_files(context_files)
```

### Case 3: Validation Pipeline

```python
# Run validations in parallel
commands = [
    "task lint:ruff",
    "task lint:mypy",
    "task test:fast"
]

# Run concurrently (3x faster)
run_parallel(commands)
```

---

## References

- [Context Loading Patterns](./context-loading-patterns.md) - File loading strategies
- [load-context.md](../workflows/load-context.md) - Context loading workflow
- [pytest-xdist docs](https://pytest-xdist.readthedocs.io/) - Test parallelization
- Agent directives: [00_agent_directives.md](../rules/00_agent_directives.md) - Section 1.10

---

**Version:** 1.0.0 (Extracted from consolidate-summaries.md Phase 4 decomposition)
**Last Updated:** 2025-10-18
