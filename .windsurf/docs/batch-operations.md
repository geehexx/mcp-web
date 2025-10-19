---
type: machine-readable-reference
category: pattern-library
purpose: Optimization strategies for batch and parallel operations
token_budget: medium
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "2025-10-20"
tags: ["batch-operations", "performance", "optimization", "parallelization"]
---

# Batch Operations

**Purpose:** Quick-reference patterns for optimizing batch and parallel operations.

---

## When to Batch

| Scenario | Batch? | Reason |
|----------|--------|--------|
| 3+ independent items | ✅ Yes | 3-10x faster |
| I/O-bound operations | ✅ Yes | Parallelism wins |
| Items depend on previous | ❌ No | Sequential required |
| CPU-bound tasks | ⚠️ Maybe | Use different parallelization |
| Memory constrained | ❌ No | Stream instead |

---

## Optimal Batch Sizes

| Operation | Batch Size | Reason |
|-----------|------------|--------|
| Local file reads | 10-15 | Balance parallelism vs overhead |
| Network file reads | 5-10 | Network latency dominates |
| URL fetches | 3-5 | Rate limiting, politeness |
| LLM API calls | 1-3 | API rate limits |
| Database queries | 50-100 | Connection pooling |

---

## Pattern 1: Parallel File Reading

**Use:** Read multiple files simultaneously

```python
# ✅ Batch (3-10x faster)
mcp0_read_multiple_files([
    "/path/file1.md",
    "/path/file2.md",
    "/path/file3.md"
])

# ❌ Sequential (slow)
for file in files:
    read_file(file)
```

**Optimal:** 10-15 files per batch

---

## Pattern 2: Chunked Processing

**Use:** Process large datasets without memory issues

```python
def process_in_chunks(items, chunk_size=10):
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        results = mcp0_read_multiple_files(chunk)
        yield results

# Process 50 files in chunks of 10
for chunk_result in process_in_chunks(all_files, 10):
    analyze(chunk_result)
```

**Benefits:** Constant memory, progress tracking, error isolation

---

## Pattern 3: Rate Limiting

**Use:** Respect external API limits

```python
import time

def batch_with_rate_limit(items, batch_size=5, delay=1.0):
    for i in range(0, len(items), batch_size):
        chunk = items[i:i + batch_size]
        process_batch(chunk)
        if i + batch_size < len(items):
            time.sleep(delay)
```

**Common Limits:**

| Service | Limit | Strategy |
|---------|-------|----------|
| GitHub API | 5000/hour | Batch 10, delay 1s |
| OpenAI | 3500/min | Batch 3, delay 1s |
| Generic REST | Varies | Start conservative |

---

## Pattern 4: Error Handling

**Use:** Graceful degradation in batch operations

```python
def batch_with_fallback(items, batch_size=10):
    results = []
    for i in range(0, len(items), batch_size):
        chunk = items[i:i + batch_size]
        try:
            batch_results = process_batch(chunk)
            results.extend(batch_results)
        except Exception as e:
            # Fallback: process individually
            for item in chunk:
                try:
                    results.append(process_single(item))
                except Exception:
                    results.append(None)  # Mark failure
    return results
```

---

## Pattern 5: Progress Tracking

**Use:** Long-running batch operations

```python
from tqdm import tqdm

def batch_with_progress(items, batch_size=10):
    results = []
    for i in tqdm(range(0, len(items), batch_size)):
        chunk = items[i:i + batch_size]
        results.extend(process_batch(chunk))
    return results
```

---

## MCP Tool Batching

### File Operations

```python
# ✅ Batch read
mcp0_read_multiple_files([file1, file2, file3])

# ✅ Batch search
grep_search(query, includes=["*.py", "*.md"])

# ❌ No batch write (use loop)
for file, content in files_to_write:
    mcp0_write_file(file, content)
```

### Context Loading

```python
# ✅ Load initiative context (batch)
files = [
    "docs/initiatives/active/feature-x/initiative.md",
    "docs/initiatives/active/feature-x/plan.md",
    "src/feature_x.py",
    "tests/test_feature_x.py"
]
mcp0_read_multiple_files(files)
```

---

## Anti-Patterns

### ❌ Over-Batching

```python
# Bad: 100 files at once
mcp0_read_multiple_files(all_100_files)  # Memory issues, no progress

# Good: Chunked
for chunk in chunks(all_100_files, 15):
    process(mcp0_read_multiple_files(chunk))
```

### ❌ Ignoring Rate Limits

```python
# Bad: Hammer API
for url in urls:
    fetch(url)  # Gets banned

# Good: Rate limited batches
batch_with_rate_limit(urls, batch_size=5, delay=1.0)
```

### ❌ Batching Dependent Operations

```python
# Bad: Results depend on previous
for item in items:
    result = process(item, previous_result)  # Can't batch

# Good: Separate independent from dependent
independent = [item for item in items if not depends_on_previous(item)]
batch_process(independent)
```

---

## Performance Guidelines

| Files | Method | Expected Speedup |
|-------|--------|------------------|
| 1-2 | Sequential | Baseline |
| 3-5 | Batch | 3-5x faster |
| 6-15 | Batch | 5-10x faster |
| 16-50 | Chunked batch | 8-12x faster |
| 50+ | Chunked + streaming | 10-15x faster |

---

## Quick Decision Matrix

```text
Need to process multiple items?
├─ Items independent? ──────────────────┐
│  ├─ Yes: Batch them                   │
│  └─ No: Sequential required           │
│                                        │
├─ How many items?                       │
│  ├─ <10: Single batch                 │
│  ├─ 10-50: Chunked batching           │
│  └─ >50: Chunked + progress tracking  │
│                                        │
├─ External API?                         │
│  ├─ Yes: Add rate limiting            │
│  └─ No: Full speed ahead              │
│                                        │
└─ Memory concerns?                      │
   ├─ Yes: Use chunking                  │
   └─ No: Batch all at once              │
```

---

## References

- [context-loading-patterns.md](./context-loading-patterns.md) - Context loading strategies
- [common-patterns.md](./common-patterns.md) - Code examples
- [tool-patterns.md](./tool-patterns.md) - MCP tool usage

---

**Version:** 2.0.0 (Compressed for conciseness)
**Maintained by:** mcp-web core team
