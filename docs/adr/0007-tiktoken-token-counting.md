# ADR-0007: Use tiktoken for Token Counting

**Status:** Implemented

**Date:** 2025-10-15

**Deciders:** Core team

**Tags:** architecture, performance, llm

---

## Context

The mcp-web tool needs accurate token counting for several purposes:

1. **Chunk sizing:** Ensure document chunks fit within LLM context windows
2. **Cost estimation:** Calculate API costs before making requests
3. **Context management:** Track cumulative token usage across conversations
4. **Validation:** Prevent exceeding model token limits

Token counting accuracy is critical because:
- **Underestimation** leads to API errors (exceeding context window)
- **Overestimation** wastes context capacity and increases costs
- Different tokenizers produce different counts for the same text

Our requirements:
1. Accurate token counts for OpenAI models (GPT-4, GPT-3.5-turbo)
2. Fast performance (minimal overhead in chunk processing)
3. Support for multiple encodings if needed
4. Reliable across different text types (code, prose, multilingual)

## Decision

We will use **tiktoken** library with the `cl100k_base` encoding (GPT-4/GPT-3.5-turbo tokenizer):

1. **Primary encoding:** `cl100k_base` for GPT-4, GPT-4-turbo, GPT-3.5-turbo
2. **Alternative encodings:** Support for `p50k_base` (older models) and `o200k_base` (GPT-4o)
3. **Implementation:** Centralized token counting in `utils.py`
4. **Caching:** Encoding objects are cached (not created per-call)

```python
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")
token_count = len(encoding.encode(text))
```

## Alternatives Considered

### Alternative 1: HuggingFace Tokenizers

**Description:** Use HuggingFace `tokenizers` library with GPT-2 tokenizer

**Pros:**
- Supports many model types
- Well-maintained library
- Good for non-OpenAI models

**Cons:**
- Not exact match for OpenAI tokenizers (±5-10% variance)
- Slower than tiktoken for OpenAI models
- Requires loading model files

**Reason for rejection:** Accuracy is critical; variance leads to context overflow errors

### Alternative 2: Character-based Estimation

**Description:** Estimate tokens using character count heuristics (e.g., 1 token ≈ 4 characters)

**Pros:**
- Extremely fast (no tokenization needed)
- No external dependencies
- Simple implementation

**Cons:**
- Very inaccurate (±20-30% variance)
- Fails on non-English text (CJK characters ≈ 1-2 chars per token)
- Fails on code (more tokens per character)
- Cannot be trusted for production use

**Reason for rejection:** Too inaccurate for reliable operation

### Alternative 3: Word-based Heuristics

**Description:** Estimate tokens using word count (e.g., 1 token ≈ 0.75 words)

**Pros:**
- Faster than full tokenization
- Better than character-based estimation
- Works reasonably for English prose

**Cons:**
- Still inaccurate (±15-20% variance)
- Fails on compound words, punctuation
- Fails on non-English text
- Fails on code and technical content

**Reason for rejection:** Insufficient accuracy for context management

## Consequences

### Positive Consequences

- **Exact token counts:** No surprises, no API errors from context overflow
- **Fast performance:** tiktoken uses C implementation (~1-5ms per document)
- **Multi-encoding support:** Can add support for other models easily
- **Cost accuracy:** Precise cost estimation before API calls
- **Confidence:** Can safely chunk documents to context limits

### Negative Consequences

- **OpenAI-specific:** Optimized for OpenAI models (but can add others)
- **Dependency:** Additional package dependency (~5MB)
- **Encoding assumptions:** Must update encodings as OpenAI releases new models

### Neutral Consequences

- **Caching importance:** Encoding objects should be cached (minor implementation detail)
- **Async considerations:** tiktoken is CPU-bound but fast enough for async usage
- **Fallback strategy:** Could add character-based estimate as ultra-fast fallback (not currently needed)

## Implementation

**Key files:**
- `src/mcp_web/utils.py` - Token counting functions
- `src/mcp_web/chunker.py` - Uses token counts for chunk sizing
- `src/mcp_web/summarizer.py` - Uses token counts for context management

**Dependencies:**
- `tiktoken >= 0.7.0` - OpenAI token counting library

**Configuration:**
```python
# Encoding selection based on model
ENCODINGS = {
    "gpt-4": "cl100k_base",
    "gpt-4-turbo": "cl100k_base",
    "gpt-3.5-turbo": "cl100k_base",
    "gpt-4o": "o200k_base",
    "text-davinci-003": "p50k_base",
}
```

**Usage pattern:**
```python
from mcp_web.utils import count_tokens

# Count tokens in text
token_count = count_tokens(text)

# Count tokens for specific model
token_count = count_tokens(text, model="gpt-4")

# Chunk text to token limit
chunks = chunk_to_token_limit(text, max_tokens=4000)
```

## References

- [tiktoken GitHub](https://github.com/openai/tiktoken)
- [OpenAI Tokenizer Documentation](https://platform.openai.com/docs/guides/embeddings/what-are-embeddings)
- [OpenAI Model Token Limits](https://platform.openai.com/docs/models)
- Related ADR: [0006-chunk-size-and-overlap.md](0006-chunk-size-and-overlap.md)
- Related ADR: [0008-map-reduce-summarization.md](0008-map-reduce-summarization.md)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2025-10-15 | Initial proposal and acceptance | Cascade |
| 2025-10-15 | Implemented in v0.1.0 | Cascade |
