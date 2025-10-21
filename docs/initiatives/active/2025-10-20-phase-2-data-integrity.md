---
Status: Active
Created: 2025-10-20
Owner: Core Team
Priority: High
Estimated Duration: 1.5 weeks (60-70 hours)
Target Completion: 2025-11-24
Updated: 2025-10-20
Tags: data-integrity, P1, quality, tokenization, caching
---

# Initiative: Phase 2 - Data Integrity & Output Validation

## Quality Assurance - Ensure Output Correctness

## Objective

Eliminate silent data corruption by fixing token counting mismatches across LLM providers and implementing cache coherency guarantees for MCP protocol compliance.

## Success Criteria

- [ ] Token count variance <2% across all supported providers
- [ ] Zero context overflow errors (1000+ doc corpus)
- [ ] Chunk boundary overlap: 100% verification
- [ ] Content preservation >99% at boundaries
- [ ] Cache consistency: 100% (no partial responses)
- [ ] MCP idempotency validated (100 retries)
- [ ] Provider-specific tokenizers implemented

---

## Motivation

**Problem:**

1. **Token Mismatch**: tiktoken for all providers causes 10-20% errors with non-OpenAI models, leading to content loss
2. **Cache Coherency**: Partial streaming responses cached as complete, violating MCP idempotency

**Impact:**

- Python asyncio docs example: 12.5% content loss (2,500 tokens missing)
- Non-deterministic results on retry (cached partial response)

**Value:**

- Accurate chunking eliminates content loss
- MCP protocol compliance ensures consistency

---

## Scope

### In Scope

- Provider-specific tokenizer (OpenAI: tiktoken, Ollama: SentencePiece, etc.)
- Two-phase cache (temp memory → permanent disk on completion)
- Quality validation framework (boundary audit, preservation metrics)
- Comprehensive test suites

### Out of Scope

- Runtime validation with retry (too complex)
- Distributed caching (Redis) - future

---

## Tasks

### Phase 1: Token Analysis (16h)

- [ ] Benchmark variance across providers (100+ samples)
- [ ] Test Python asyncio docs (reference case)
- [ ] Audit current token counting logic
- [ ] Design TokenCounter architecture
- [ ] Create ADR

### Phase 2: Tokenizer Implementation (24h)

- [ ] TokenCounter class with lazy loading
- [ ] OpenAI tokenizer (tiktoken)
- [ ] Ollama tokenizer (transformers/SentencePiece)
- [ ] LM Studio / LocalAI tokenizers
- [ ] Integrate into chunking pipeline
- [ ] Tests: 50+ cases, variance <2%

### Phase 3: Cache Coherency (24h)

- [ ] TwoPhaseCache class (temp + permanent)
- [ ] Stream and accumulate pattern
- [ ] Completion markers
- [ ] Partial response cleanup
- [ ] Interruption tests (25%, 50%, 75%)
- [ ] MCP idempotency validation (1000 retries)

### Phase 4: Quality Framework (16h)

- [ ] Chunk boundary audit tool
- [ ] Content preservation metrics
- [ ] Tokenizer benchmark suite
- [ ] Cache consistency tests
- [ ] Golden regression tests

---

## Timeline

- Days 1-2: Token analysis (16h)
- Days 3-5: Tokenizer implementation (24h)
- Days 6-8: Cache coherency (24h)
- Days 9-10: Quality validation (16h)

**Total:** 68 hours (1.5 weeks, 2 people)

---

## Dependencies

**Blocks:** Phase 1 (Resource Stability) must complete first

**Libraries:** transformers, sentencepiece

---

## References

- [tiktoken](https://github.com/openai/tiktoken)
- [HuggingFace Tokenizers](https://huggingface.co/docs/tokenizers/)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26/core/tools)
- [Token Counting Guide](https://winder.ai/calculating-token-counts-llm-context-windows-practical-guide/)

---

## Updates

### 2025-10-20

Initiative created. Key decisions:

1. **Provider-Specific**: Use correct tokenizer per provider (no universal solution)
2. **Two-Phase Cache**: Memory accumulation → disk commit on completion
3. **Quality First**: Comprehensive testing before optimization

**Research:**

- Token variance: 5-20% depending on content type
- Cache coherency: Two-phase pattern ensures MCP compliance
- Performance: <5% overhead target for tokenization

---

**Last Updated:** 2025-10-20
**Status:** Active (Blocked by Phase 1 completion)
