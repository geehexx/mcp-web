# Idempotency Framework Integration

**Date:** 2025-10-21  
**Purpose:** Integrate idempotency verification into workflow optimization process  
**Status:** Implementation Ready

---

## Overview

Combines research from `idempotency-research.md` with intelligent compression methodology to ensure optimizations are truly idempotent and semantically preserving.

**Goal:** `optimize(optimize(workflow)) === optimize(workflow)` with >92% semantic similarity

---

## Integration Architecture

### Stage 0: Pre-Optimization Hash

```python
def create_optimization_hash(content: str, config: OptimizationConfig) -> str:
    """Create deterministic hash for caching."""
    payload = {
        "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
        "methodology_version": "v2.0",
        "compression_techniques": config.enabled_techniques,
        "preservation_thresholds": config.thresholds,
        "model": "gpt-4",
        "temperature": 0.0,
        "seed": 42
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
```

### Stage 1: Cache Check

```python
cache_file = ".windsurf/.optimization-cache.json"

def check_cache(file_path: str, content: str) -> Optional[str]:
    """Check if already optimized."""
    opt_hash = create_optimization_hash(content, current_config)
    
    if opt_hash in cache:
        print(f"✅ CACHE HIT: {file_path} already optimized")
        return cache[opt_hash]["optimized_content"]
    
    return None  # Cache miss, proceed with optimization
```

### Stage 2: Semantic Analysis (Layer 1)

```python
def analyze_semantic_profile(content: str) -> SemanticProfile:
    """Extract semantic structure before compression."""
    return {
        "decision_points": extract_decisions(content),
        "entities": extract_entities_ner(content),  # spaCy NER
        "task_structures": extract_update_plan_calls(content),
        "examples": identify_examples(content),
        "relationships": build_dependency_graph(content),
        "anchors": extract_contextual_anchors(content)
    }
```

### Stage 3: Intelligent Compression (Layers 2-3)

```python
def compress_with_preservation(
    content: str,
    semantic_profile: SemanticProfile,
    config: OptimizationConfig
) -> str:
    """Apply 5-layer methodology."""
    
    # Layer 2: Coarse-grained (section-level)
    compressed = apply_budget_controller(content, semantic_profile)
    
    # Layer 3: Fine-grained (token-level)
    compressed = apply_contextual_anchors(compressed, semantic_profile.anchors)
    
    return compressed
```

### Stage 4: Semantic Validation (Layer 4)

```python
def validate_semantic_preservation(
    original: str,
    compressed: str,
    semantic_profile: SemanticProfile
) -> ValidationResult:
    """Multi-dimensional quality check."""
    
    scores = {
        "entity_preservation": measure_entity_overlap(
            semantic_profile.entities,
            extract_entities_ner(compressed)
        ),
        "decision_logic_intact": verify_all_present(
            semantic_profile.decision_points,
            compressed
        ),
        "task_syntax_valid": validate_update_plan_syntax(compressed),
        "relationship_preserved": check_dependency_preservation(
            semantic_profile.relationships,
            compressed
        ),
        "anchor_retention": measure_anchor_overlap(
            semantic_profile.anchors,
            compressed
        )
    }
    
    # Weighted score
    total_score = (
        scores["entity_preservation"] * 0.30 +
        scores["decision_logic_intact"] * 0.25 +
        scores["task_syntax_valid"] * 0.20 +
        scores["relationship_preserved"] * 0.15 +
        scores["anchor_retention"] * 0.10
    )
    
    return ValidationResult(
        passed=total_score >= 0.92,
        score=total_score,
        details=scores
    )
```

### Stage 5: Idempotency Testing (Layer 5)

```python
def test_idempotency(
    original: str,
    compressed: str,
    config: OptimizationConfig
) -> IdempotencyResult:
    """Verify re-optimization produces no changes."""
    
    # Test 1: Hash-based exact match
    re_compressed = compress_with_preservation(
        compressed,
        analyze_semantic_profile(compressed),
        config
    )
    
    hash_original_compressed = hashlib.sha256(compressed.encode()).hexdigest()
    hash_re_compressed = hashlib.sha256(re_compressed.encode()).hexdigest()
    
    exact_match = (hash_original_compressed == hash_re_compressed)
    
    # Test 2: Semantic similarity (allow minor variations)
    similarity = semantic_similarity_score(compressed, re_compressed)
    
    # Test 3: Token drift check
    token_count_compressed = count_tokens(compressed)
    token_count_re_compressed = count_tokens(re_compressed)
    token_drift = abs(token_count_compressed - token_count_re_compressed)
    
    return IdempotencyResult(
        exact_match=exact_match,
        semantic_similarity=similarity,
        token_drift=token_drift,
        passed=(exact_match or (similarity >= 0.98 and token_drift <= 10))
    )
```

### Stage 6: Cache Update

```python
def update_cache(
    file_path: str,
    original: str,
    compressed: str,
    validation: ValidationResult,
    idempotency: IdempotencyResult
):
    """Store successful optimization."""
    
    opt_hash = create_optimization_hash(original, current_config)
    
    cache[opt_hash] = {
        "file_path": file_path,
        "original_hash": hashlib.sha256(original.encode()).hexdigest(),
        "optimized_content": compressed,
        "timestamp": datetime.now().isoformat(),
        "metadata": {
            "methodology_version": "v2.0",
            "semantic_score": validation.score,
            "idempotency_verified": idempotency.passed,
            "compression_ratio": len(original) / len(compressed),
            "techniques_applied": current_config.enabled_techniques
        }
    }
    
    save_cache(cache_file, cache)
```

---

## Workflow Integration

### improve-prompt.md Enhancement

**Add to Stage 2.5 (Model Detection):**

```markdown
### 2.5.5 Idempotency Check

**Before optimization:**

1. Calculate optimization hash
2. Check cache (`.windsurf/.optimization-cache.json`)
3. If cache hit: Return cached result immediately
4. If cache miss: Proceed with optimization

**After optimization:**

1. Run idempotency test (re-optimize and compare)
2. If idempotency fails: Flag for manual review
3. If idempotency passes: Update cache
```

**Add to Stage 6 (Validate):**

```markdown
### 6.5 Idempotency Verification

**Tests:**
- ✅ Hash-based exact match OR
- ✅ Semantic similarity >= 98% AND token drift <= 10

**Output:**
- Idempotency status in results summary
- Cache entry created for future optimizations
```

### improve-workflow.md Enhancement

**Add to Stage 0 (Workflow Context Analysis):**

```markdown
### 0.3 Idempotency Pre-Check

Check if workflow already optimized:
- Method 1: Cache lookup by hash
- Method 2: Frontmatter `optimized_version` field
- Method 3: Token count vs target delta < 50

If already optimized: Skip optimization, return unchanged
```

**Add to Stage 3 (Workflow-Specific Validation):**

```markdown
### 3.4 Idempotency Testing

For workflows:
- Re-optimize optimized content
- Verify `update_plan` calls unchanged
- Check frontmatter integrity
- Validate workflow entry/exit preserved

Golden tests: 4 previously optimized workflows
```

---

## Golden Test Suite

### Test Workflows (Already Optimized)

```python
GOLDEN_WORKFLOWS = [
    ".windsurf/workflows/implement.md",
    ".windsurf/workflows/detect-context.md", 
    ".windsurf/workflows/load-context.md",
    ".windsurf/workflows/plan.md"
]

def test_golden_idempotency():
    """Verify re-optimization produces no changes."""
    for workflow_path in GOLDEN_WORKFLOWS:
        original = read_file(workflow_path)
        
        # Re-optimize
        re_optimized = optimize_workflow(
            workflow_path,
            temperature=0.0,
            seed=42
        )
        
        # Assert exact match
        assert original == re_optimized, f"Idempotency violated: {workflow_path}"
        print(f"✅ {workflow_path} passed idempotency test")
```

---

## Cache Structure

```json
{
  "optimization_cache": {
    "abc123...": {
      "file_path": ".windsurf/workflows/work.md",
      "original_hash": "def456...",
      "optimized_content": "...",
      "timestamp": "2025-10-21T10:00:00Z",
      "metadata": {
        "methodology_version": "v2.0",
        "semantic_score": 0.94,
        "idempotency_verified": true,
        "compression_ratio": 0.72,
        "techniques_applied": [
          "table_consolidation",
          "example_consolidation",
          "information_distillation"
        ]
      }
    }
  },
  "metadata": {
    "cache_version": "1.0",
    "created": "2025-10-21T10:00:00Z",
    "last_updated": "2025-10-21T12:00:00Z",
    "total_entries": 17
  }
}
```

---

## Implementation Checklist

- [ ] Create `.windsurf/.optimization-cache.json`
- [ ] Add idempotency checks to `improve-prompt.md`
- [ ] Add idempotency checks to `improve-workflow.md`
- [ ] Create golden test suite (`tests/golden/test_golden_optimization.py`)
- [ ] Add semantic preservation metrics
- [ ] Create cache management commands (clear, prune, stats)
- [ ] Update pre-commit hook to verify idempotency
- [ ] Document cache structure in README

---

## Benefits

1. **Performance:** Cache hits avoid redundant LLM calls
2. **Consistency:** Deterministic results across runs
3. **Quality:** Semantic preservation metrics guarantee no loss
4. **Safety:** Idempotency tests catch regressions early
5. **Transparency:** Cache metadata shows what changed and why

---

## References

- `idempotency-research.md` - Original research
- `intelligent-compression-v2.md` - 5-layer methodology
- LLMLingua paper - Budget controller inspiration
- Semantic preservation metrics - Entity preservation >95%

---

**Version:** 1.0  
**Status:** Ready for integration  
**Last Updated:** 2025-10-21
