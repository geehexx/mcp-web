# Design Decisions Log

**Project:** mcp-web summarization tool
**Purpose:** Track architectural choices, tradeoffs, and rationale

---

## Decision Format

Each decision includes:
- **ID:** Unique identifier (DD-XXX)
- **Date:** When decided
- **Status:** Proposed | Accepted | Deprecated | Superseded
- **Context:** Problem statement
- **Decision:** What we chose
- **Rationale:** Why we chose it
- **Alternatives:** What we considered but rejected
- **Consequences:** Implications (positive/negative)
- **References:** Links, papers, benchmarks

---

## Active Decisions

### DD-001: httpx Primary, Playwright Fallback
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need to fetch HTML from diverse websites, some with JavaScript rendering
**Decision:** Use `httpx` async client as primary method, fall back to Playwright headless browser on failure
**Rationale:**
- httpx is 10-100x faster than Playwright for static sites
- Playwright handles JS-heavy sites (SPAs, dynamic content)
- Fallback provides robustness without sacrificing performance
**Alternatives:**
- Playwright-only: Too slow for simple pages
- httpx-only: Fails on JS-rendered content
- requests library: Not async, slower
**Consequences:**
- (+) Fast happy path, robust fallback
- (-) Additional dependency (Playwright + browsers)
- (-) Complexity in deciding when to fallback
**References:**
- httpx benchmarks: https://www.python-httpx.org/
- Playwright async guide: https://playwright.dev/python/

---

### DD-002: Trafilatura for Content Extraction
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need to extract main content from arbitrary HTML (remove boilerplate, ads, navigation)
**Decision:** Use `trafilatura` library with `favor_recall=True`
**Rationale:**
- Best accuracy in HTML content extraction benchmarks
- Handles diverse page structures
- Preserves formatting (code blocks, lists, tables)
- Extracts metadata (title, author, date)
**Alternatives:**
- BeautifulSoup + heuristics: Requires manual rules per site
- newspaper3k: Less maintained, lower accuracy
- Readability (Mozilla): Good but Python port is dated
**Consequences:**
- (+) High extraction quality
- (+) Handles edge cases well
- (-) Slightly slower than simpler parsers
**References:**
- Trafilatura benchmark: https://github.com/adbar/trafilatura#evaluation
- Web scraping comparison: [to search]

---

### DD-003: Hierarchical + Semantic Chunking
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need to split long documents for LLM processing while preserving context
**Decision:** Implement hierarchical chunking (respect headings/sections) + semantic boundaries (sentences, paragraphs)
**Rationale:**
- Maintains document structure for better summarization
- Semantic boundaries prevent mid-sentence splits
- Configurable chunk size adapts to different LLM contexts
**Alternatives:**
- Fixed-size windows: Breaks context arbitrarily
- Recursive character splitting: Simpler but less intelligent
- Embedding-based clustering: Overkill for MVP, requires embeddings
**Consequences:**
- (+) Better summary quality (coherent chunks)
- (+) Flexible for different document types
- (-) More complex implementation
- (-) Slightly slower than naive splitting
**References:**
- LangChain text splitters: [to search]
- Semantic chunking research: [to search]

---

### DD-004: 512-Token Chunks with 50-Token Overlap
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need to determine optimal chunk size and overlap
**Decision:** Default to 512 tokens per chunk, 50 tokens overlap
**Rationale:**
- 512 tokens = ~1-2 paragraphs (good context unit)
- 50-token overlap prevents context loss at boundaries
- Fits within 8k context window with room for prompts
- Configurable for different use cases
**Alternatives:**
- 256 tokens: Too granular, loses context
- 1024 tokens: Too large, less precise summaries
- No overlap: Risks losing cross-boundary info
**Consequences:**
- (+) Balances granularity and context
- (+) Works well with most LLMs
- (-) May need tuning for specific content types
**References:**
- GPT token limits: https://platform.openai.com/docs/models
- Chunking best practices: [to search]

---

### DD-005: tiktoken for Token Counting
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need accurate token counting for chunk sizing and context limits
**Decision:** Use `tiktoken` library with cl100k_base encoding (GPT-4/GPT-3.5-turbo)
**Rationale:**
- Official OpenAI tokenizer (exact counting)
- Fast C implementation
- Supports multiple encodings
**Alternatives:**
- HuggingFace tokenizers: Less accurate for OpenAI models
- Character-based estimation: Too inaccurate (±30%)
- Word-based heuristics: Fails on non-English text
**Consequences:**
- (+) Exact token counts, no surprises
- (+) Fast performance
- (-) OpenAI-specific (but can add other encodings)
**References:**
- tiktoken docs: https://github.com/openai/tiktoken

---

### DD-006: Map-Reduce Summarization Strategy
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need to summarize documents that exceed LLM context window
**Decision:** Use map-reduce pattern: summarize chunks individually (map) → combine summaries (reduce)
**Rationale:**
- Scales to arbitrarily long documents
- Parallelizable (faster)
- Well-established pattern for LLMs
- Better than truncation (no info loss)
**Alternatives:**
- Truncate to context limit: Loses information
- Refine iteratively: Slower, less parallelizable
- Stuff all chunks: Fails on long docs
**Consequences:**
- (+) Handles long documents
- (+) Can parallelize map phase
- (-) May lose some cross-chunk context
- (-) Reduction step can be tricky
**References:**
- LangChain summarization: https://python.langchain.com/docs/use_cases/summarization
- Map-reduce prompting: [to search]

---

### DD-007: Disk Cache with 7-Day TTL
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need to avoid redundant fetches and processing for frequently accessed URLs
**Decision:** Implement disk-based cache in `~/.cache/mcp-web/` with 7-day TTL
**Rationale:**
- Disk cache persists across sessions (unlike in-memory)
- 7 days balances freshness and efficiency
- Uses ETags for HTTP cache validation
- LRU eviction prevents unbounded growth
**Alternatives:**
- In-memory cache: Lost on restart
- Redis/external: Overkill for single-user tool
- No cache: Too slow, wasteful
- Longer TTL: Stale content risk
**Consequences:**
- (+) Fast repeated queries
- (+) Reduces API costs (LLM calls)
- (-) Disk space usage (mitigated by size limit)
- (-) Cache invalidation complexity
**References:**
- HTTP caching: https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching
- diskcache library: [to search]

---

### DD-008: OpenAI GPT-4 as Default LLM
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Need high-quality abstractive summaries
**Decision:** Default to OpenAI GPT-4, make model configurable
**Rationale:**
- GPT-4 produces best summaries (quality, coherence)
- Widely available, stable API
- Good balance of speed and quality
- Configurable for other models (Claude, local LLMs)
**Alternatives:**
- GPT-3.5: Cheaper but lower quality
- Claude: Comparable quality, different API
- Local models (Llama): Privacy but worse quality
**Consequences:**
- (+) Best summary quality
- (+) 32k context window (handles long chunks)
- (-) Cost per request (mitigated by caching)
- (-) Requires API key
**References:**
- GPT-4 benchmarks: https://openai.com/research/gpt-4

---

### DD-009: Streaming Output
**Date:** 2025-10-15
**Status:** Accepted
**Context:** Long summaries can take 10-30 seconds, need to show progress
**Decision:** Stream partial results using async generators
**Rationale:**
- Better UX (user sees progress)
- Aligns with MCP streaming capabilities
- Enables real-time monitoring
**Alternatives:**
- Batch response: Long wait times
- Progress callbacks: Less elegant than streaming
**Consequences:**
- (+) Responsive UI
- (+) Can cancel mid-stream
- (-) More complex error handling
**References:**
- MCP streaming: [to search MCP docs]
- OpenAI streaming: https://platform.openai.com/docs/api-reference/streaming

---

### DD-010: Monolithic Tool Design
**Date:** 2025-10-15
**Status:** Accepted
**Context:** MCP architecture decision: single tool vs. multiple tools
**Decision:** Implement as single `summarize_urls` tool with rich parameters
**Rationale:**
- Simpler user interface (one tool to learn)
- Easier to orchestrate internal pipeline
- Reduces inter-tool communication overhead
**Alternatives:**
- Multiple tools (fetch_url, extract_content, summarize): More modular but complex
- Separate tools per content type: Too fragmented
**Consequences:**
- (+) Simple API surface
- (+) Easier to optimize pipeline
- (-) Less composable (can't reuse fetch_url alone)
- (mitigation) Modules are still reusable programmatically
**References:**
- MCP best practices: [to search]

---

## Deprecated Decisions

### DD-XXX: Example Deprecated Decision
**Date:** 2025-XX-XX
**Status:** Superseded by DD-YYY
**Reason:** [Explanation]

---

## Pending Decisions

### PD-001: PDF Extraction Library
**Context:** Need to extract text from PDFs (research papers, documentation)
**Options:**
1. `pypdf`: Lightweight, pure Python
2. `pdfplumber`: Better layout preservation
3. `pdfminer.six`: Most accurate but slower
**Research Needed:**
- Benchmark accuracy on technical PDFs
- OCR integration for scanned docs
**Target Date:** Phase 2 (extractor implementation)

---

### PD-002: Link Scoring Algorithm
**Context:** When following links recursively, need to prioritize relevant URLs
**Options:**
1. Keyword matching (query terms in link text/URL)
2. Domain reputation (prefer .edu, .gov, known docs sites)
3. PageRank-style scoring
4. LLM-based relevance scoring (expensive)
**Research Needed:**
- Benchmark different strategies
- Cost-benefit of LLM scoring
**Target Date:** Phase 4 (integration)

---

### PD-003: Embeddings for Semantic Search
**Context:** Future enhancement to find most relevant chunks for query
**Options:**
1. OpenAI embeddings API
2. Local sentence-transformers
3. Hybrid (keyword + embeddings)
**Decision Criteria:**
- Cost (API calls vs. compute)
- Latency impact
- Quality improvement over keyword search
**Target Date:** V2 (post-MVP)

---

## Change Log

| Date | Decision | Change | Reason |
|------|----------|--------|--------|
| 2025-10-15 | DD-001 to DD-010 | Initial decisions | Project kickoff |

---

**Maintained By:** Cascade (AI Agent)
**Review Cadence:** After each milestone, before major refactors
**Format:** Inspired by Michael Nygard's Architecture Decision Records (ADR)
