---
Status: Active
Created: 2025-10-20
Owner: Core Team
Priority: Medium
Estimated Duration: 2 weeks (80-90 hours)
Target Completion: 2025-12-08
Updated: 2025-10-20
Tags: performance, P2, optimization, cost-reduction
---

# Initiative: Phase 3 - Performance Optimization

**User Experience - Reduce Latency & Operational Costs**

---

## Objective

Improve user experience and reduce operational costs through linear-time chunking algorithms, cache deduplication, and extraction optimization. Target 30%+ P95 latency improvement and 10%+ cost reduction.

## Success Criteria

- [ ] Large doc (20k+ tokens) processing <10s (current: 30-60s)
- [ ] Duplicate fetch rate <1% (current: 5-10%)
- [ ] Extraction time <1s for 80% of pages
- [ ] P95 latency improvement >30%
- [ ] Cloud LLM cost reduction >10% (measurable)
- [ ] Chunking quality degradation <10% vs semantic
- [ ] Memory usage <500MB for 50k token document

---

## Motivation

**Problem:**

1. **Chunking O(n²)**: Semantic chunking takes 15-25s for 20k token docs (Python asyncio), blocking pipeline
2. **Cache Races**: Concurrent requests to same URL waste 5-10% resources (duplicate fetches, LLM calls)
3. **Extraction Latency**: trafilatura `favor_recall=True` takes 1-3s per page (20-40% of pipeline time)

**Impact:**

```
Current Performance:
- 5k tokens: 1.2s chunking
- 10k tokens: 4.8s chunking
- 20k tokens: 18.5s chunking (9.3x slower than linear)
- 50k tokens: 180s (3min) - timeout territory

Cost Impact (cache races):
- 1000 requests/day, 5% races = 50 duplicates
- Time waste: 250 seconds/day
- Cost waste: $0.50/day = $182.50/year
- At scale (10k req/day): $1,825/year
```

**Value:**

- User experience: Faster responses, no timeouts
- Cost efficiency: Reduce cloud LLM API usage
- Scalability: Handle larger documents

---

## Scope

### In Scope

**P2-PERFORMANCE-001: Linear-Time Chunking**

- Adaptive chunking strategy (simple for large docs, semantic for small)
- Dynamic programming algorithm for optimal chunking
- Streaming chunker (minimal buffering)
- Configurable thresholds (large doc, deep nesting)

**P2-PERFORMANCE-002: Cache Deduplication**

- In-memory deduplication (same-process requests)
- URL normalization (redirects, trailing slashes)
- In-flight request tracking (wait for existing fetch)
- Metrics: dedup.hits, dedup.misses, duplicate.rate

**P2-PERFORMANCE-003: Extraction Optimization**

- Extraction result caching (separate from summary cache)
- Adaptive extraction strategy (simple pages vs complex)
- trafilatura configuration tuning (favor_precision for simple pages)
- Benchmark alternative extractors (readability, boilerpy3)

**Performance Testing Framework**

- Benchmark suite (chunking, extraction, end-to-end)
- Load testing (100+ concurrent requests)
- Cost measurement (LLM API usage tracking)
- Performance regression detection (CI integration)

### Out of Scope

- Advanced algorithmic research (TextTiling, TopicTiling) - future
- Distributed caching (Redis) - operational concern
- Circuit breakers / advanced retry - future
- Auto-scaling - operational concern

---

## Tasks

### Phase 1: Chunking Optimization (Days 1-4) - 32h

#### Performance Analysis

- [ ] Profile current semantic chunking (cProfile)
- [ ] Measure tree depth distribution (real web pages)
- [ ] Test quality vs speed trade-off
- [ ] Document performance bottlenecks

#### Adaptive Strategy Implementation

- [ ] Implement adaptive chunking (detect large docs)
- [ ] Threshold: 10k tokens → switch to simple chunking
- [ ] Threshold: 8+ nesting levels → simple chunking
- [ ] Configure thresholds (CHUNKER_LARGE_DOC_THRESHOLD)
- [ ] Tests: 20+ cases

#### Dynamic Programming Algorithm

- [ ] Research DP-based text segmentation
- [ ] Implement O(n) chunking algorithm
- [ ] Preserve semantic boundaries where possible
- [ ] Tests: 15+ cases
- [ ] Quality comparison (semantic vs DP)

#### Validation

- [ ] Benchmark: 5k, 10k, 20k, 50k token docs
- [ ] Quality metrics: boundary precision, coherence
- [ ] Performance: <5s for 20k tokens (current: 15-25s)
- [ ] Memory: <500MB for 50k tokens

### Phase 2: Cache Deduplication (Days 5-7) - 24h

#### In-Memory Deduplication

- [ ] Implement DeduplicatingFetcher class
- [ ] Track in-flight requests (url → Future)
- [ ] Wait for existing fetch (no duplicate)
- [ ] Clean up on completion
- [ ] Tests: 15+ cases

#### URL Normalization

- [ ] Normalize URLs (redirects, trailing slash, case)
- [ ] Handle redirect chains
- [ ] Cache key consistency
- [ ] Tests: 10+ cases

#### Metrics & Monitoring

- [ ] Track deduplication hits/misses
- [ ] Measure duplicate fetch rate
- [ ] Cost savings calculation
- [ ] Integration tests: 10+ cases

#### Validation

- [ ] Test: 10 concurrent requests, same URL
- [ ] Verify: Only 1 fetch, others wait
- [ ] Test: Redirect chain deduplication
- [ ] Measure: Deduplication overhead (<1ms)

### Phase 3: Extraction Optimization (Days 8-10) - 24h

#### Extraction Caching

- [ ] Implement CachedExtractor class
- [ ] Cache key: URL + HTML hash
- [ ] TTL: 1 day (shorter than summary)
- [ ] Tests: 10+ cases

#### Adaptive Extraction

- [ ] Detect simple vs complex pages (heuristics)
- [ ] favor_precision for simple pages (faster)
- [ ] favor_recall for complex pages (quality)
- [ ] Tests: 15+ cases

#### Alternative Extractors (Research)

- [ ] Benchmark readability-lxml
- [ ] Benchmark newspaper3k
- [ ] Benchmark boilerpy3
- [ ] Compare: speed, coverage, structure
- [ ] Document findings (ADR)

#### Validation

- [ ] Extract 100 diverse pages
- [ ] Measure time and quality
- [ ] Cache effectiveness (40%+ hit rate)
- [ ] Quality: <5% degradation

### Phase 4: Performance Testing Framework (Days 11-14) - 30h

#### Benchmark Suite

- [ ] Chunking benchmark (algorithms, sizes)
- [ ] Extraction benchmark (strategies)
- [ ] End-to-end latency benchmark
- [ ] Concurrency benchmark (100+ requests)
- [ ] Cost benchmark (LLM API usage)

#### Load Testing

- [ ] Create load test script (realistic patterns)
- [ ] Test 100 concurrent requests
- [ ] Measure resource usage (CPU, memory, FDs)
- [ ] Measure error rate
- [ ] Generate performance report

#### Cost Measurement

- [ ] Track LLM API calls (count, tokens)
- [ ] Calculate cost per request
- [ ] Measure cache hit rate impact
- [ ] Measure deduplication savings
- [ ] Compare before/after optimization

#### CI Integration

- [ ] Add benchmarks to CI (performance-regression.yml)
- [ ] Baseline comparison (20% threshold)
- [ ] PR comments with performance impact
- [ ] Document performance testing guide

---

## Timeline

- Days 1-4: Chunking optimization (32h)
- Days 5-7: Cache deduplication (24h)
- Days 8-10: Extraction optimization (24h)
- Days 11-14: Performance testing (30h)

**Total:** 86 hours (2 weeks, 2 people)

---

## Dependencies

**Blocks:** Phase 2 (Data Integrity) must complete first

**Libraries:** None (use existing)

---

## References

- [TextTiling Algorithm](https://aclanthology.org/J97-1003.pdf)
- [httpx Connection Pooling](https://www.python-httpx.org/advanced/#connection-pooling)
- [trafilatura Performance](https://trafilatura.readthedocs.io/en/latest/corefunctions.html#options)
- [Python DP: Text Segmentation](https://en.wikipedia.org/wiki/Dynamic_programming)

---

## Updates

### 2025-10-20

Initiative created. Key decisions:

1. **Adaptive Chunking**: Simple algorithm for large/complex docs (immediate relief)
2. **In-Memory Dedup**: Simple and effective for single-process (majority case)
3. **Extraction Cache**: Separate cache layer (repeated URL queries)
4. **Quality First**: <10% degradation acceptable for 3-10x speedup

**Research:**

- Semantic chunking: O(n² log n) complexity
- Cache races: 5-10% wasted resources
- Extraction: 20-40% of pipeline time
- Cost savings: $182-$1825/year depending on scale

---

**Last Updated:** 2025-10-20
**Status:** Active (Blocked by Phase 2 completion)
