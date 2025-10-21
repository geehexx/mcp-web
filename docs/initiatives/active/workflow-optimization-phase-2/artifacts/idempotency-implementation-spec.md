# Idempotency Implementation Specification

**Date:** 2025-10-21
**Purpose:** Technical spec for idempotent workflow optimization
**Research:** See `idempotency-research.md`

---

## Architecture

### Components

| Component | Purpose | Location |
|-----------|---------|----------|
| Optimization Cache | Hash-based LLM result storage | `.windsurf/.optimization-cache.json` |
| Golden Snapshots | Reference outputs for regression | `tests/golden/workflows/` |
| Validation Script | Test idempotency | `scripts/test_optimization_idempotency.py` |
| Cache Management | Manage cache | `scripts/manage_optimization_cache.py` |
| Golden Tests | Pytest suite | `tests/golden/test_golden_optimization.py` |

---

## Optimization Cache Structure

**File:** `.windsurf/.optimization-cache.json`

```json
{
  "version": "1.0.0",
  "cache": {
    "abc123...": {
      "file_path": ".windsurf/workflows/implement.md",
      "original_hash": "def456...",
      "optimized_content": "...",
      "metadata": {
        "model": "gpt-4",
        "temperature": 0.0,
        "seed": 42,
        "timestamp": "2025-10-21T10:00:00Z"
      }
    }
  }
}
```

---

## Golden Test Workflows

Already-optimized workflows to test (from Session 2):

1. `.windsurf/workflows/implement.md`
2. `.windsurf/workflows/detect-context.md`
3. `.windsurf/workflows/load-context.md`
4. `.windsurf/workflows/plan.md`

**Test:** Re-optimize → expect ZERO changes (character-by-character match)

---

## Implementation Checklist

### Phase 1: Core Infrastructure (1-2 hours)

- [ ] Create cache file structure
- [ ] Implement `OptimizationCache` class with put/get/invalidate
- [ ] Implement hash generation (SHA-256 of content + prompt + model)
- [ ] Test cache operations

### Phase 2: Validation Script (1 hour)

- [ ] Create `scripts/test_optimization_idempotency.py`
- [ ] Implement workflow optimization with caching
- [ ] Add CLI for testing specific workflows
- [ ] Test on sample workflow

### Phase 3: Golden Tests (1 hour)

- [ ] Create `tests/golden/workflows/` directory
- [ ] Copy Session 2 optimized workflows as golden snapshots
- [ ] Create pytest test suite
- [ ] Run tests to verify PASS

### Phase 4: Validation (30 min)

- [ ] Run validation on all golden workflows
- [ ] Verify 100% idempotent (no changes)
- [ ] Update documentation
- [ ] Commit changes

---

## Validation Protocol

**PRE-IMPLEMENTATION TEST (CRITICAL):**

Manually verify Session 2 workflows are idempotent:

```bash
# Re-optimize already-optimized workflows
# Expected: NO CHANGES detected

python scripts/test_optimization_idempotency.py \
  --workflows implement.md detect-context.md load-context.md plan.md \
  --expect-no-changes
```

**If ANY changes detected:**

- ❌ STOP Phase 2 optimizations
- Investigate root cause
- Fix optimization algorithm

**POST-IMPLEMENTATION TEST:**

```bash
# Run validation script
python scripts/test_optimization_idempotency.py --test-golden

# Run pytest
pytest tests/golden/test_golden_optimization.py -v

# Both must return 100% PASS
```

---

## Success Criteria

**MANDATORY before Phase 2:**

- [ ] All scripts implemented
- [ ] Golden snapshots created
- [ ] Validation: 100% idempotent (0 changes)
- [ ] Pytest: 100% PASS
- [ ] Cache functional
- [ ] Documentation complete

**Acceptance Test:**

```bash
# Optimize same file twice
output1=$(python scripts/test_optimization_idempotency.py --workflows implement.md)
output2=$(python scripts/test_optimization_idempotency.py --workflows implement.md)

# Verify identical
diff <(echo "$output1") <(echo "$output2")
# Expected: NO OUTPUT (identical)
```

---

## Key Functions

### Hash Generation

```python
def create_optimization_hash(file_path, content, prompt, model, temp, seed):
    content_hash = sha256(content)
    prompt_hash = sha256(prompt)
    payload = {file_path, content_hash, prompt_hash, model, temp, seed}
    return sha256(json.dumps(payload, sort_keys=True))
```

### Cache Lookup

```python
def optimize_with_cache(workflow_path):
    content = read_file(workflow_path)
    cache_key = create_hash(workflow_path, content)

    if cache_key in cache:
        return cache[cache_key]  # Cache hit

    optimized = llm_optimize(content, temp=0.0, seed=42)
    cache[cache_key] = optimized
    return optimized
```

### Golden Test

```python
def test_optimization_idempotency(workflow_path):
    original = read_file(workflow_path)
    optimized = optimize_workflow(workflow_path, use_cache=False)
    assert original == optimized, "IDEMPOTENCY VIOLATION"
```

---

## Next Steps

1. Implement core infrastructure
2. Create validation script
3. Set up golden test framework
4. Run validation suite
5. **Only proceed to Phase 2 if 100% idempotent**

---

**Status:** Ready for Implementation
**Est. Time:** 3-4 hours
**Priority:** CRITICAL (blocks Phase 2)
