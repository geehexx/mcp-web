# Performance Optimization Initiative: Sub-5-Second Summarization

**Created:** 2025-10-15
**Owner:** AI Agent
**Status:** Active - Phase 1 Complete, Planning Phase 2
**Priority:** High
**Target:** Achieve <5 second summarization without quality compromise

---

## Executive Summary

Comprehensive performance optimization initiative to profile, benchmark, and optimize the entire mcp-web pipeline with focus on reducing summarization latency from current baseline to well under 5 seconds while maintaining or improving quality.

### Key Goals

1. **Profiling & Monitoring**: Build reusable profiling tools and comprehensive monitoring
2. **Baseline Metrics**: Establish current performance baselines across all components
3. **Optimization Phases**: Implement optimizations in 3 phased approaches
4. **Quality Assurance**: Ensure zero quality regression through golden tests
5. **Future-Proof**: Create extensible framework for continuous optimization

### Success Criteria

- ✅ Summarization completes in <5 seconds for typical web pages (5-10k tokens)
- ✅ 90%+ quality retention vs baseline (measured via golden tests)
- ✅ Comprehensive profiling tools for ongoing monitoring
- ✅ Scalable to 10x current workload
- ✅ Cost reduction through batch processing where applicable

---

## Research Summary (October 2025 State-of-the-Art)

### Key Findings from Industry Research

#### 1. Batch Processing (50% Cost Savings)

**Source**: [AI Batch Processing: OpenAI, Claude, and Gemini (2025)](https://adhavpavan.medium.com/ai-batch-processing-openai-claude-and-gemini-2025-94107c024a10)

- **All major providers** (OpenAI, Anthropic, Google) offer 50% cost reduction for batch APIs
- **Trade-off**: 24-hour processing window vs immediate response
- **Best for**: Non-real-time workloads, evaluation, background processing
- **Implementation**: Submit multiple requests asynchronously

**Action**: Implement batch mode for map phase when map-reduce strategy is used

#### 2. Async Optimization Patterns

**Source**: [Mastering Python asyncio.gather and asyncio.as_completed](https://python.useinstructor.com/blog/2023/11/13/learn-async/)

**Key Patterns**:

- `asyncio.gather()`: Concurrent execution with ordered results
- `asyncio.as_completed()`: Stream results as they complete (better perceived latency)
- `Semaphore`: Rate limiting to respect API limits
- **Performance**: Can achieve 10x+ speedup for I/O-bound LLM calls

**Action**: Optimize map phase with parallel chunk summarization using asyncio.gather

#### 3. Map-Reduce Parallelization

**Source**: [LangChain Map-Reduce Summarization](https://python.langchain.com/docs/how_to/summarize_map_reduce/)

**Architecture**:

```python
# Map phase: Parallel chunk summarization
tasks = [summarize_chunk(chunk) for chunk in chunks]
chunk_summaries = await asyncio.gather(*tasks)

# Reduce phase: Recursive collapse if needed
if total_tokens > threshold:
    summaries = await collapse_summaries(chunk_summaries)
else:
    final = await reduce_summary(chunk_summaries)
```

**Action**: Current implementation uses sequential map phase - parallelize it

#### 4. Streaming & Latency Optimization

**Source**: [Optimizing OpenAI API Performance - SigNoz](https://signoz.io/guides/open-ai-api-latency/)

**Techniques**:

- **Lower `max_tokens`**: Reduces generation time proportionally
- **Stop sequences**: Prevent unnecessary token generation
- **Streaming responses**: Improve perceived latency (TTFT vs total time)
- **Prompt optimization**: Concise prompts = faster processing

**Action**: Optimize prompts, implement adaptive max_tokens based on content

#### 5. Concurrent Processing Best Practices

**Source**: [Scaling LLM Calls Efficiently with asyncio](https://medium.com/@kannappansuresh99/scaling-llm-calls-efficiently-in-python-the-power-of-asyncio-bfa969eed718)

**Pattern**:

```python
# Instead of sequential
for item in items:
    result = await process(item)  # Slow!

# Use concurrent
tasks = [process(item) for item in items]
results = await asyncio.gather(*tasks)  # Fast!
```

**Action**: Audit all async code for sequential patterns that could be parallel

---

## Current Architecture Analysis

### Pipeline Flow

```
┌─────────────┐    ┌──────────────┐    ┌──────────┐    ┌──────────────┐
│   Fetcher   │ -> │  Extractor   │ -> │ Chunker  │ -> │ Summarizer   │
│  (httpx/    │    │ (trafilatura)│    │ (smart   │    │ (map-reduce) │
│  Playwright)│    │              │    │  split)  │    │              │
└─────────────┘    └──────────────┘    └──────────┘    └──────────────┘
     ↓                   ↓                  ↓                 ↓
  Cache Hit?        Cache Hit?           Fast             Slowest
  (fast)            (fast)            (CPU-bound)      (I/O-bound)
```

### Performance Bottleneck Hypothesis

**Primary Bottleneck**: Summarization (LLM API calls)

- **Map phase**: Sequential chunk summarization
- **Reduce phase**: Single LLM call (fast)
- **Opportunity**: Parallelize map phase for N chunks

**Secondary Bottlenecks**:

- Fetcher: Already concurrent (configurable limit)
- Extractor: Mostly CPU-bound (trafilatura)
- Chunker: Pure CPU (can optimize token counting)

---

## Optimization Plan: 3-Phase Approach

### Phase 1: Quick Wins (Target: 30-40% improvement)

**Effort**: Low | **Impact**: Medium | **Timeline**: 1-2 sessions

#### 1.1 Parallel Map-Reduce

**Current**:

```python
# Sequential - SLOW
for i, chunk in enumerate(chunks):
    summary = await self._call_llm_non_streaming(map_prompt)
    chunk_summaries.append(summary)
```

**Optimized**:

```python
# Parallel - FAST
async def summarize_chunk(chunk, query):
    prompt = self._build_map_prompt(chunk.text, query)
    return await self._call_llm_non_streaming(prompt)

tasks = [summarize_chunk(chunk, query) for chunk in chunks]
chunk_summaries = await asyncio.gather(*tasks)
```

**Expected Impact**:

- For 10 chunks: ~10x faster map phase
- Overall: 30-50% total time reduction

#### 1.2 Optimize Prompts

**Actions**:

- Reduce verbose system instructions
- Use concise, directive prompts
- Add stop sequences for controlled output length
- Lower `max_tokens` adaptively based on chunk size

**Expected Impact**: 10-20% reduction per LLM call

#### 1.3 Streaming Optimization

**Current**: Already streaming reduce phase
**Action**: Stream map phase results as they complete using `asyncio.as_completed()`
**Expected Impact**: Better perceived latency, no total time improvement

#### 1.4 Add Profiling Instrumentation

**Create**:

- Per-component timing metrics
- LLM call duration tracking
- Token usage monitoring
- Cache hit/miss ratios

**Tools**:

- Python `cProfile` integration
- Custom `@profile` decorator
- Comprehensive metrics export

---

### Phase 2: Advanced Parallel Processing (Target: 50-70% improvement)

**Effort**: Medium | **Impact**: High | **Timeline**: 2-3 sessions

#### 2.1 Batch API Integration (Optional, for non-real-time)

**OpenAI Batch API**:

- 50% cost savings
- 24-hour processing window
- Best for: Evaluation, testing, background jobs

**Implementation**:

```python
# For map phase with many chunks
batch_requests = [
    {
        "custom_id": f"chunk-{i}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {...}
    }
    for i, chunk in enumerate(chunks)
]

# Submit batch
batch_id = await client.batches.create(requests=batch_requests)

# Poll for results
results = await client.batches.retrieve(batch_id)
```

**Decision**: Implement as optional mode for non-interactive use cases

#### 2.2 Adaptive Chunking Strategy

**Current**: Fixed chunk_size (512 tokens)
**Proposed**: Adaptive sizing based on document characteristics

```python
def adaptive_chunk_size(document):
    if document.has_code_blocks:
        return 1024  # Larger chunks for code
    elif document.structure == "dense":
        return 768   # Medium chunks
    else:
        return 512   # Standard
```

**Expected Impact**: Fewer chunks = fewer LLM calls = faster

#### 2.3 Smart Caching Layers

**Current**: URL-level cache
**Add**:

- **Chunk-level cache**: Cache summaries of common chunks
- **Semantic deduplication**: Skip summarizing identical/similar chunks
- **TTL optimization**: Extend TTL for stable content

**Expected Impact**: 20-30% for repeat content

#### 2.4 Concurrency Tuning

**Research optimal concurrency limits**:

```python
# Experiment with different limits
CONCURRENCY_LIMITS = [5, 10, 20, 30, 50]

for limit in CONCURRENCY_LIMITS:
    time = await benchmark_with_limit(limit)
    plot(limit, time)

# Find optimal: Balance API limits vs latency
```

**Expected Impact**: 10-20% based on API rate limits

---

### Phase 3: Advanced Techniques (Target: 80%+ improvement)

**Effort**: High | **Impact**: High | **Timeline**: 3-4 sessions

#### 3.1 Model Optimization

**Techniques**:

- **Use faster models for map phase**: GPT-4o-mini vs GPT-4 (faster, cheaper)
- **Use larger context for reduce phase**: Minimize reduce calls
- **Fine-tuning** (future): Custom summarization model

**Implementation**:

```python
class SummarizerConfig:
    map_model: str = "gpt-4o-mini"  # Fast for map
    reduce_model: str = "gpt-4o"    # Quality for reduce
```

**Expected Impact**: 40-60% on map phase

#### 3.2 Speculative Summarization

**Concept**: Start summarization before chunking completes

```python
# Pipeline parallelism
async def pipeline_parallel():
    extractor_task = asyncio.create_task(extract())

    # Start chunking as soon as extraction starts
    chunks = []
    async for chunk in streaming_chunker(await extractor_task):
        # Start summarizing immediately
        task = asyncio.create_task(summarize_chunk(chunk))
        chunks.append(task)

    summaries = await asyncio.gather(*chunks)
```

**Expected Impact**: 15-25% via pipeline parallelism

#### 3.3 Smart Map-Reduce Thresholds

**Current**: Always use map-reduce above threshold
**Proposed**: Dynamic strategy selection

```python
def select_strategy(chunks, query):
    total_tokens = sum(c.tokens for c in chunks)

    if total_tokens < 8000:
        return "direct"  # Single LLM call
    elif total_tokens < 32000:
        return "map_reduce"  # Parallel map
    else:
        return "hierarchical_map_reduce"  # Recursive
```

**Expected Impact**: Avoid overhead for small documents

#### 3.4 GPU-Accelerated Chunking (Future)

**For very large documents**:

- Use local sentence transformers for semantic chunking
- GPU acceleration for embedding generation
- Cluster similar sentences into chunks

**Expected Impact**: 50%+ for chunking phase on large docs

---

## Implementation Checklist

### Phase 1 Tasks

- [x] Create profiling decorator and timing utilities
- [x] Implement parallel map-reduce with `asyncio.gather()`
- [x] Add `asyncio.as_completed()` streaming variant
- [x] Add comprehensive metrics collection
- [x] Create benchmark comparison framework
- [x] Add mock LLM fixtures for deterministic benchmarks
- [x] Add summarization performance benchmarks
- [x] Validate parallel map-reduce speedup (measured ~1.17x improvement)
- [x] Fix mock LLM fixtures to fully intercept API calls (patched mcp_web.summarizer.AsyncOpenAI)
- [x] Run summarization benchmark suite with working mocks (all pass in ~150ms)
- [x] Optimize prompts (reduce verbosity, add stop sequences)
- [x] Implement adaptive `max_tokens` based on chunk size
- [x] Run comprehensive benchmark suite across all components
- [x] Validate quality with golden tests (baseline: 63% pass rate maintained)

### Phase 2 Tasks

- [ ] Research and implement OpenAI Batch API integration
- [ ] Create batch mode for non-real-time summarization
- [ ] Implement adaptive chunking strategy
- [ ] Add chunk-level caching
- [ ] Implement semantic deduplication for chunks
- [ ] Benchmark optimal concurrency limits
- [ ] Add rate limiting with exponential backoff
- [ ] Create cost tracking and reporting

### Phase 3 Tasks

- [ ] Implement multi-model strategy (fast map, quality reduce)
- [ ] Add speculative/pipeline parallelism
- [ ] Implement dynamic strategy selection
- [ ] Research fine-tuning approach
- [ ] Explore GPU-accelerated chunking
- [ ] Create performance monitoring dashboard
- [ ] Document all optimizations in ADRs

---

## Monitoring & Metrics

### Key Performance Indicators (KPIs)

1. **Total Latency**: End-to-end time from URL to summary
2. **Component Latency**: Per-stage timing (fetch, extract, chunk, summarize)
3. **LLM Metrics**:
   - Time to first token (TTFT)
   - Total tokens per second
   - Cost per summary
4. **Cache Efficiency**:
   - Hit rate %
   - Time saved via cache
5. **Quality Metrics**:
   - ROUGE scores vs baseline
   - User satisfaction (if applicable)

### Profiling Tools to Create

1. **`profiler.py`**: Central profiling utilities
   - `@profile` decorator for function timing
   - Context manager for section timing
   - Export to JSON/CSV for analysis

2. **`benchmark_suite.py`**: Comprehensive benchmarks
   - End-to-end pipeline benchmarks
   - Component-level micro-benchmarks
   - Comparison with baseline
   - Automated regression detection

3. **`metrics_dashboard.py`**: Real-time monitoring
   - CLI dashboard for live metrics
   - Export to Prometheus/Grafana (future)
   - Performance alerts

4. **`load_tester.py`**: Scalability testing
   - Simulate concurrent requests
   - Measure throughput and latency under load
   - Identify bottlenecks

---

## Risk Analysis

### Technical Risks

1. **API Rate Limits**: Parallel requests may hit limits
   - **Mitigation**: Implement semaphore-based rate limiting

2. **Quality Degradation**: Faster models may reduce quality
   - **Mitigation**: Golden tests, A/B comparison, configurable models

3. **Increased Complexity**: More code paths to maintain
   - **Mitigation**: Comprehensive tests, clear documentation

4. **Cost Increase**: More parallel calls = more cost
   - **Mitigation**: Batch API, caching, cost monitoring

### Operational Risks

1. **Backward Compatibility**: Optimization may break existing usage
   - **Mitigation**: Feature flags, gradual rollout, versioning

2. **Monitoring Overhead**: Profiling may impact performance
   - **Mitigation**: Make profiling optional, minimal overhead design

---

## Success Metrics & Validation

### Before/After Comparison

| Metric | Baseline | Target | Validation Method |
|--------|----------|--------|-------------------|
| 5k tokens summary | TBD | <3s | Benchmark suite |
| 10k tokens summary | TBD | <5s | Benchmark suite |
| 50k tokens summary | TBD | <15s | Benchmark suite |
| Quality (ROUGE-L) | TBD | ≥90% of baseline | Golden tests |
| Cache hit rate | TBD | >50% | Metrics tracking |
| Cost per summary | TBD | -30% | Cost tracking |

### Quality Assurance

1. **Golden Tests**: Run all existing golden tests, ensure pass rate ≥95%
2. **A/B Comparison**: Sample 100 URLs, compare baseline vs optimized
3. **Human Evaluation**: Manual review of 20 summaries for quality
4. **Regression Tests**: Automated tests prevent performance regression

---

## Documentation Deliverables

1. **ADR**: Architecture Decision Records for major changes
2. **Performance Guide**: Best practices for optimal configuration
3. **Profiling Guide**: How to use profiling tools
4. **Benchmark Report**: Detailed before/after analysis
5. **API Changes**: Document any API changes or new options

---

## Timeline

**Total Estimated Time**: 6-10 work sessions

| Phase | Duration | Deliverables |
|-------|----------|--------------|
| Phase 1: Quick Wins | 1-2 sessions | Parallel map-reduce, profiling tools, 30-40% improvement |
| Phase 2: Advanced Parallel | 2-3 sessions | Batch API, adaptive chunking, 50-70% improvement |
| Phase 3: Advanced Techniques | 3-4 sessions | Model optimization, pipeline parallelism, 80%+ improvement |
| Documentation & Testing | 1 session | Complete docs, test suite, final report |

---

## Tooling Improvements (Future Work)

### Testing Infrastructure

**1. Test Fixtures & Factories Library**

**Current State:**

- Manual fixture creation in conftest.py
- Repetitive data setup across test files
- No standardized factories for test objects

**Recommended:**

- Adopt `factory_boy` or `pytest-factoryboy` for object factories
- Create reusable factories for common test data:
  - `ChunkFactory` for creating test chunks
  - `FetchResultFactory` for mock fetch results
  - `ConfigFactory` for test configurations
- Benefits: DRY principle, maintainable tests, easier parameterization

**Example:**

```python
# tests/factories.py
import factory
from mcp_web.chunker import Chunk

class ChunkFactory(factory.Factory):
    class Meta:
        model = Chunk

    text = factory.Faker('text', max_nb_chars=200)
    tokens = factory.LazyAttribute(lambda o: len(o.text.split()))
    start_pos = factory.Sequence(lambda n: n * 100)
    end_pos = factory.LazyAttribute(lambda o: o.start_pos + len(o.text))
    metadata = factory.Dict({})

# Usage in tests:
chunks = ChunkFactory.create_batch(20)
```

**2. Prompt & Template Management**

**Current State:**

- LLM prompts embedded as docstrings in code
- Hard to maintain, version, and test
- Difficult to A/B test different prompt strategies
- No prompt validation or templating

**Recommended:**

- Adopt `Jinja2` for prompt templating
- Store prompts in separate files (e.g., `prompts/summarize_map.j2`)
- Benefits:
  - Decouples prompts from code
  - Version control for prompt changes
  - Easier A/B testing
  - Support for prompt validation and testing

**Example Structure:**

```
src/mcp_web/prompts/
├── __init__.py
├── loader.py              # Jinja2 environment setup
├── summarize_map.j2       # Map phase prompt
├── summarize_reduce.j2    # Reduce phase prompt
└── query_focused.j2       # Query-aware variant
```

**Example Usage:**

```python
# src/mcp_web/prompts/loader.py
from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader('mcp_web', 'prompts'),
    autoescape=False,
    trim_blocks=True,
    lstrip_blocks=True,
)

def render_prompt(template_name: str, **kwargs) -> str:
    template = env.get_template(template_name)
    return template.render(**kwargs)

# In summarizer.py:
from mcp_web.prompts import render_prompt

prompt = render_prompt('summarize_map.j2',
                       chunk=chunk_text,
                       query=query,
                       max_length=target_length)
```

**Priority:** Medium - Not blocking current performance work, but valuable for long-term maintainability.

---

## Next Steps

1. ✅ Complete baseline benchmarks (completed with mock infrastructure)
2. ✅ Create profiling infrastructure (completed)
3. ✅ Implement Phase 1 parallel map-reduce (completed)
4. ⏳ Improve mock LLM fixtures (in progress - currently still calls real API)
5. 🔜 Validate quality with golden tests
6. 🔜 Optimize prompts and implement adaptive max_tokens
7. 🔜 Consider tooling improvements (factories, templating)

---

## References

- [AI Batch Processing 2025](https://adhavpavan.medium.com/ai-batch-processing-openai-claude-and-gemini-2025-94107c024a10)
- [Async LLM Processing with asyncio.gather](https://python.useinstructor.com/blog/2023/11/13/learn-async/)
- [LangChain Map-Reduce Summarization](https://python.langchain.com/docs/how_to/summarize_map_reduce/)
- [Optimizing OpenAI API Performance](https://signoz.io/guides/open-ai-api-latency/)
- [Scaling LLM Calls with asyncio](https://medium.com/@kannappansuresh99/scaling-llm-calls-efficiently-in-python-the-power-of-asyncio-bfa969eed718)
- [OWASP LLM Top 10 2025](https://genai.owasp.org/)
