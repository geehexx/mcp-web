---
type: machine-readable-reference
category: pattern-library
purpose: Efficient context loading strategies for AI agents
token_budget: medium
audience: ai-agent
auto_generated: false
maintenance: manual
last_updated: "2025-10-20"
tags: ["context-loading", "performance", "mcp-tools", "batch-operations"]
---

# Context Loading Patterns

**Purpose:** Quick-reference patterns for efficient context loading in workflows.

---

## Loading Strategy Matrix

| Scenario | Strategy | Tools | Batch Size |
|----------|----------|-------|------------|
| Initiative work | Targeted | `mcp0_read_multiple_files` | 5-10 files |
| Full project scan | Hierarchical | `find_by_name` + batch read | 10-15 files |
| Code exploration | Search-first | `grep_search` → targeted read | 3-5 files |
| Documentation | Batch read | `mcp0_read_multiple_files` | 10-15 files |
| Large codebase | Chunked | Iterate + batch | 10 files/chunk |

---

## Pattern 1: Initiative Context

**Use:** Load all files for an active initiative

```python
# 1. Identify initiative files
initiative_dir = "docs/initiatives/active/feature-x/"
core_files = [
    f"{initiative_dir}initiative.md",
    f"{initiative_dir}plan.md",
    "src/feature_x.py",
    "tests/test_feature_x.py"
]

# 2. Batch load
mcp0_read_multiple_files(core_files)
```

**Performance:** 5-10x faster than sequential

---

## Pattern 2: Hierarchical Loading

**Use:** Load project context progressively

```python
# Phase 1: High-level overview
overview_files = [
    "README.md",
    "docs/CONSTITUTION.md",
    "docs/DOCUMENTATION_STRUCTURE.md"
]
mcp0_read_multiple_files(overview_files)

# Phase 2: Relevant subsystem (based on Phase 1)
subsystem_files = find_by_name(
    SearchDirectory="src/subsystem/",
    Pattern="*.py",
    MaxDepth=2
)
mcp0_read_multiple_files(subsystem_files[:10])

# Phase 3: Deep dive (if needed)
# Load specific files identified in Phase 2
```

**Benefits:** Minimal tokens, targeted loading, progressive refinement

---

## Pattern 3: Search-First Loading

**Use:** Find relevant code before loading

```python
# 1. Search for relevant code
results = grep_search(
    Query="authentication",
    SearchPath="src/",
    Includes=["*.py"],
    MatchPerLine=False  # Just find files
)

# 2. Extract file paths from results
relevant_files = extract_file_paths(results)

# 3. Batch load top matches
mcp0_read_multiple_files(relevant_files[:5])
```

**Performance:** Avoids loading irrelevant files

---

## Pattern 4: Chunked Loading

**Use:** Load large file sets without memory issues

```python
def load_in_chunks(file_list, chunk_size=10):
    for i in range(0, len(file_list), chunk_size):
        chunk = file_list[i:i + chunk_size]
        yield mcp0_read_multiple_files(chunk)

# Process 50 files in chunks of 10
all_files = get_all_python_files()
for chunk_data in load_in_chunks(all_files, 10):
    analyze(chunk_data)
```

---

## Pattern 5: Lazy Loading

**Use:** Load only when needed

```python
# 1. Load index/manifest first
manifest = read_file("docs/FILE_INDEX.md")

# 2. Identify required files from manifest
required_files = parse_manifest(manifest)

# 3. Load only required files
mcp0_read_multiple_files(required_files)
```

**Benefits:** Minimal initial load, on-demand expansion

---

## MCP Tool Selection

| Task | Tool | Reason |
|------|------|--------|
| Load known files | `mcp0_read_multiple_files` | Fastest for known paths |
| Find files by name | `find_by_name` | Glob patterns, filtering |
| Search file content | `grep_search` | Content-based discovery |
| List directory | `mcp0_list_directory` | Explore structure |
| Get file metadata | `mcp0_get_file_info` | Size, timestamps |

---

## Optimization Guidelines

### Batch Size Recommendations

| File Type | Optimal Batch | Reason |
|-----------|---------------|--------|
| Small (<10KB) | 15 files | Low memory impact |
| Medium (10-100KB) | 10 files | Balance speed/memory |
| Large (>100KB) | 5 files | Avoid memory issues |
| Mixed sizes | 10 files | Safe default |

### When to Use Each Pattern

```text
Do you know exact files needed?
├─ Yes: Pattern 1 (Initiative Context)
└─ No: ──────────────────────────────┐
   │                                  │
   Need full project view?            │
   ├─ Yes: Pattern 2 (Hierarchical)   │
   └─ No: ─────────────────────────┐  │
      │                             │  │
      Know what to search for?      │  │
      ├─ Yes: Pattern 3 (Search)    │  │
      └─ No: Pattern 2 (Hierarchical)│  │
                                     │  │
   Processing many files?            │  │
   └─ Yes: Pattern 4 (Chunked)       │  │
```

---

## Anti-Patterns

### ❌ Loading Everything

```python
# Bad: Load entire codebase
all_files = find_by_name(SearchDirectory=".", Pattern="*")
mcp0_read_multiple_files(all_files)  # Thousands of files!

# Good: Targeted loading
relevant_files = find_by_name(
    SearchDirectory="src/feature_x/",
    Pattern="*.py",
    MaxDepth=2
)
mcp0_read_multiple_files(relevant_files[:10])
```

### ❌ Sequential Loading

```python
# Bad: Load files one by one
for file in files:
    content = read_file(file)  # 10x slower

# Good: Batch load
contents = mcp0_read_multiple_files(files)
```

### ❌ Ignoring File Sizes

```python
# Bad: Batch large files
large_files = ["10MB_file1.json", "20MB_file2.json", ...]
mcp0_read_multiple_files(large_files)  # Memory explosion

# Good: Check sizes first
file_info = [mcp0_get_file_info(f) for f in files]
small_files = [f for f, info in zip(files, file_info)
               if info['size'] < 100_000]
mcp0_read_multiple_files(small_files)
```

---

## Performance Metrics

| Pattern | Files Loaded | Time (est) | Memory |
|---------|--------------|------------|--------|
| Sequential | 10 | 10s | Low |
| Batch (10) | 10 | 1-2s | Medium |
| Hierarchical | 5 → 10 → 5 | 3-4s | Low-Medium |
| Search-first | 3-5 | 1-2s | Low |
| Chunked (50 files) | 50 | 5-8s | Medium |

---

## Quick Reference

**Most Common Pattern:**

```python
# Initiative-focused loading
files = [
    "docs/initiatives/active/X/initiative.md",
    "src/module.py",
    "tests/test_module.py"
]
mcp0_read_multiple_files(files)
```

**Exploration Pattern:**

```python
# 1. Search
results = grep_search(Query="pattern", SearchPath="src/")

# 2. Load matches
files = extract_paths(results)[:5]
mcp0_read_multiple_files(files)
```

**Full Context Pattern:**

```python
# 1. Overview
mcp0_read_multiple_files(["README.md", "docs/CONSTITUTION.md"])

# 2. Targeted subsystem
subsystem_files = find_by_name(SearchDirectory="src/X/", Pattern="*.py")
mcp0_read_multiple_files(subsystem_files[:10])
```

---

## References

- [batch-operations.md](./batch-operations.md) - Batch operation patterns
- [tool-patterns.md](./tool-patterns.md) - MCP tool usage
- [common-patterns.md](./common-patterns.md) - Code examples

---

**Version:** 2.0.0 (Compressed for conciseness)
**Maintained by:** mcp-web core team
