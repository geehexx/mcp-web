"""LLM-based summarization with map-reduce strategy.

Implements:
- Map-reduce summarization for long documents
- Query-aware abstractive summaries
- Streaming output
- Multiple LLM provider support (OpenAI, Anthropic)
- Content-based caching for deduplication

Design Decision DD-006: Map-reduce summarization.
Design Decision DD-008: OpenAI GPT-4 default.
Design Decision DD-009: Streaming output.
Design Decision DD-015: Cache layers for fetch, extract, summarize.
"""

import asyncio
import hashlib
from collections.abc import AsyncIterator

import structlog
from openai import AsyncOpenAI

from mcp_web.cache import CacheKeyBuilder, CacheManager
from mcp_web.chunker import Chunk
from mcp_web.config import SummarizerSettings
from mcp_web.metrics import get_metrics_collector
from mcp_web.security import (
    OutputValidator,
    PromptInjectionFilter,
    create_structured_prompt,
)
from mcp_web.utils import TokenCounter

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


class Summarizer:
    """LLM-based content summarizer.

    Example:
        >>> summarizer = Summarizer(config)
        >>> async for chunk in summarizer.summarize_chunks(chunks, query="key points"):
        ...     print(chunk)
    """

    def __init__(self, config: SummarizerSettings, cache: CacheManager | None = None):
        """Initialize summarizer.

        Args:
            config: Summarizer configuration
            cache: Optional cache manager for result caching
        """
        self.config = config
        self.cache = cache
        self.token_counter = TokenCounter()
        self.metrics = get_metrics_collector()

        # Security components (OWASP LLM Top 10)
        self.injection_filter = PromptInjectionFilter()
        self.output_validator = OutputValidator(max_output_length=config.max_summary_length)

        # Initialize OpenAI-compatible client
        api_key = config.get_api_key()
        api_base = config.get_api_base()

        # For local providers without API keys, use placeholder
        if not api_key:
            if config.provider == "openai":
                _get_logger().warning(
                    "no_openai_api_key", msg="OPENAI_API_KEY not set for OpenAI provider"
                )
            # Local LLMs don't need real API keys
            api_key = "not-needed"

        _get_logger().info(
            "summarizer_init",
            provider=config.provider,
            model=config.model,
            api_base=api_base,
        )

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=api_base,
            timeout=config.timeout,
        )

    async def summarize_chunks(
        self,
        chunks: list[Chunk],
        query: str | None = None,
        sources: list[str] | None = None,
        use_cache: bool = True,
    ) -> AsyncIterator[str]:
        """Summarize chunks with streaming output.

        Args:
            chunks: List of text chunks
            query: Optional query for focused summary
            sources: Optional list of source URLs
            use_cache: Use cached summary if available (default: True)

        Yields:
            Summary text chunks (streaming)

        Note:
            Caching is content-based (SHA-256 hash) to deduplicate identical
            content from different sources.
        """
        import time

        _get_logger().info(
            "summarization_start",
            num_chunks=len(chunks),
            query=query[:50] if query else None,
        )

        start_time = time.perf_counter()

        # Check cache first
        if use_cache and self.cache:
            content_hash = self._compute_content_hash(chunks)
            cache_key = CacheKeyBuilder.summary_key(
                content_hash=content_hash,
                query=query,
                model=self.config.model,
            )
            cached_summary = await self.cache.get(cache_key)
            if cached_summary:
                _get_logger().info(
                    "summarization_cache_hit",
                    content_hash=content_hash[:16],
                    query=query[:50] if query else None,
                )
                # Yield cached summary as single chunk
                yield cached_summary
                return

        try:
            # Calculate total tokens
            total_tokens = sum(c.tokens for c in chunks)

            # Accumulate output for caching
            accumulated_output = []

            # Decide strategy: direct or map-reduce
            if total_tokens <= self.config.map_reduce_threshold:
                # Direct summarization
                async for response_chunk in self._summarize_direct(chunks, query, sources):
                    accumulated_output.append(response_chunk)
                    yield response_chunk
            else:
                # Map-reduce for large documents
                # Choose between parallel gather or streaming as_completed
                if self.config.streaming_map:
                    async for response_chunk in self._summarize_map_reduce_streaming(
                        chunks, query, sources
                    ):
                        accumulated_output.append(response_chunk)
                        yield response_chunk
                elif self.config.parallel_map:
                    async for response_chunk in self._summarize_map_reduce(chunks, query, sources):
                        accumulated_output.append(response_chunk)
                        yield response_chunk
                else:
                    # Sequential fallback (original implementation)
                    async for response_chunk in self._summarize_map_reduce_sequential(
                        chunks, query, sources
                    ):
                        accumulated_output.append(response_chunk)
                        yield response_chunk

            duration_ms = (time.perf_counter() - start_time) * 1000

            # Cache the result
            if use_cache and self.cache and accumulated_output:
                full_summary = "".join(accumulated_output)
                content_hash = self._compute_content_hash(chunks)
                cache_key = CacheKeyBuilder.summary_key(
                    content_hash=content_hash,
                    query=query,
                    model=self.config.model,
                )
                await self.cache.set(cache_key, full_summary)
                _get_logger().info(
                    "summarization_cached",
                    content_hash=content_hash[:16],
                    summary_length=len(full_summary),
                )

            _get_logger().info(
                "summarization_complete",
                duration_ms=round(duration_ms, 2),
            )

        except Exception as e:
            _get_logger().error("summarization_failed", error=str(e))
            self.metrics.record_error("summarizer", e)
            raise

    async def _summarize_direct(
        self,
        chunks: list[Chunk],
        query: str | None = None,
        sources: list[str] | None = None,
    ) -> AsyncIterator[str]:
        """Direct summarization (single LLM call).

        Args:
            chunks: Text chunks
            query: Optional query
            sources: Optional sources

        Yields:
            Summary chunks
        """
        # Combine chunks
        combined_text = "\n\n".join(c.text for c in chunks)

        # Build prompt
        prompt = self._build_summary_prompt(combined_text, query, sources)

        # Call LLM
        async for llm_response_chunk in self._call_llm(prompt):
            yield llm_response_chunk

    async def _summarize_map_reduce(
        self,
        chunks: list[Chunk],
        query: str | None = None,
        sources: list[str] | None = None,
    ) -> AsyncIterator[str]:
        """Map-reduce summarization for large documents.

        Args:
            chunks: Text chunks
            query: Optional query
            sources: Optional sources

        Yields:
            Summary chunks

        Note:
            Uses parallel map phase for performance (asyncio.gather).
            This can achieve 10x+ speedup for documents with many chunks.
        """
        _get_logger().info("map_reduce_start", num_chunks=len(chunks))

        # Step 1: Map - Summarize each chunk IN PARALLEL
        async def summarize_single_chunk(i: int, chunk: Chunk) -> str:
            """Summarize a single chunk."""
            _get_logger().debug("map_chunk_start", chunk_num=i + 1)
            map_prompt = self._build_map_prompt(chunk.text, query)
            summary = await self._call_llm_non_streaming(map_prompt)
            _get_logger().debug("map_chunk_complete", chunk_num=i + 1)
            return summary

        # Create tasks for all chunks and execute in parallel
        tasks = [summarize_single_chunk(i, chunk) for i, chunk in enumerate(chunks)]
        chunk_summaries = await asyncio.gather(*tasks)

        _get_logger().info("map_complete", num_summaries=len(chunk_summaries))

        # Step 2: Reduce - Combine summaries
        combined_summaries = "\n\n".join(
            f"Section {i + 1}:\n{s}" for i, s in enumerate(chunk_summaries)
        )

        reduce_prompt = self._build_reduce_prompt(combined_summaries, query, sources)

        # Stream final summary
        async for response_chunk in self._call_llm(reduce_prompt):
            yield response_chunk

    async def _summarize_map_reduce_sequential(
        self,
        chunks: list[Chunk],
        query: str | None = None,
        sources: list[str] | None = None,
    ) -> AsyncIterator[str]:
        """Sequential map-reduce (original implementation).

        Args:
            chunks: Text chunks
            query: Optional query
            sources: Optional sources

        Yields:
            Summary chunks

        Note:
            This is the original sequential implementation.
            Kept for compatibility and as a fallback option.
        """
        _get_logger().info("map_reduce_sequential_start", num_chunks=len(chunks))

        # Step 1: Map - Summarize each chunk SEQUENTIALLY
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            _get_logger().debug("map_chunk", chunk_num=i + 1)
            map_prompt = self._build_map_prompt(chunk.text, query)
            summary = await self._call_llm_non_streaming(map_prompt)
            chunk_summaries.append(summary)

        _get_logger().info("map_complete", num_summaries=len(chunk_summaries))

        # Step 2: Reduce - Combine summaries
        combined_summaries = "\n\n".join(
            f"Section {i + 1}:\n{s}" for i, s in enumerate(chunk_summaries)
        )

        reduce_prompt = self._build_reduce_prompt(combined_summaries, query, sources)

        # Stream final summary
        async for response_chunk in self._call_llm(reduce_prompt):
            yield response_chunk

    async def _summarize_map_reduce_streaming(
        self,
        chunks: list[Chunk],
        query: str | None = None,
        sources: list[str] | None = None,
    ) -> AsyncIterator[str]:
        """Map-reduce with streaming results as they complete.

        Args:
            chunks: Text chunks
            query: Optional query
            sources: Optional sources

        Yields:
            Progress updates and final summary

        Note:
            Uses asyncio.as_completed() to stream map results as they finish.
            Better perceived latency but results are out of order.
        """
        _get_logger().info("map_reduce_streaming_start", num_chunks=len(chunks))

        # Yield progress update
        yield f"Processing {len(chunks)} sections...\n\n"

        # Step 1: Map - Summarize chunks and stream progress
        async def summarize_single_chunk(i: int, chunk: Chunk) -> tuple[int, str]:
            """Summarize a single chunk, return index and summary."""
            map_prompt = self._build_map_prompt(chunk.text, query)
            summary = await self._call_llm_non_streaming(map_prompt)
            return (i, summary)

        # Create tasks
        tasks = [
            asyncio.create_task(summarize_single_chunk(i, chunk)) for i, chunk in enumerate(chunks)
        ]

        # Collect summaries as they complete
        chunk_summaries: list[str | None] = [None] * len(chunks)

        for task in asyncio.as_completed(tasks):
            idx, summary = await task
            chunk_summaries[idx] = summary

            # Stream progress
            yield f"✓ Section {idx + 1}/{len(chunks)} complete\n"

        _get_logger().info("map_complete_streaming", num_summaries=len(chunk_summaries))

        # Step 2: Reduce - Combine summaries
        yield "\nSynthesizing final summary...\n\n"

        combined_summaries = "\n\n".join(
            f"Section {i + 1}:\n{s}" for i, s in enumerate(chunk_summaries) if s
        )

        reduce_prompt = self._build_reduce_prompt(combined_summaries, query, sources)

        # Stream final summary
        async for response_chunk in self._call_llm(reduce_prompt):
            yield response_chunk

    def _calculate_max_tokens(self, input_tokens: int) -> int:
        """Calculate adaptive max_tokens based on input size.

        Args:
            input_tokens: Number of input tokens

        Returns:
            Optimized max_tokens value

        Note:
            Adaptive max_tokens reduces latency by preventing over-generation.
            Based on research: smaller max_tokens = faster response.
            Reference: https://signoz.io/guides/open-ai-api-latency/
        """
        if not self.config.adaptive_max_tokens:
            return self.config.max_tokens

        # Calculate adaptive max_tokens based on input size
        # Ratio: smaller inputs need proportionally smaller outputs
        adaptive_tokens = int(input_tokens * self.config.max_tokens_ratio)

        # Clamp to reasonable bounds
        min_tokens = 200  # Minimum useful summary
        max_tokens = self.config.max_tokens  # Never exceed configured max

        return max(min_tokens, min(adaptive_tokens, max_tokens))

    async def _call_llm(self, prompt: str, adaptive_max_tokens: bool = True) -> AsyncIterator[str]:
        """Call LLM with streaming and output validation.

        Args:
            prompt: Prompt text

        Yields:
            Validated response chunks

        Note:
            Implements output validation (OWASP LLM05:2025) to detect
            system prompt leakage and sensitive data exposure.
        """
        import time

        start_time = time.perf_counter()
        input_tokens = self.token_counter.count_tokens(prompt)
        output_tokens = 0
        accumulated_output = []

        # Calculate adaptive max_tokens if enabled
        max_tokens = (
            self._calculate_max_tokens(input_tokens)
            if adaptive_max_tokens
            else self.config.max_tokens
        )

        # Prepare stop sequences if configured
        stop = self.config.stop_sequences if self.config.stop_sequences else None

        from openai import APIError, Timeout

        try:
            # Sanitize prompt before sending to LLM
            if self.injection_filter.detect_injection(prompt):
                _get_logger().warning("prompt_injection_detected", prompt_preview=prompt[:100])
                prompt = self.injection_filter.sanitize(prompt)

            stream = await self.client.chat.completions.create(  # semgrep-ignore: llm-missing-error-handling, potential-prompt-injection-risk
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    output_tokens += self.token_counter.count_tokens(content)
                    accumulated_output.append(content)

                    # Validate accumulated output periodically (every 10 chunks)
                    if len(accumulated_output) % 10 == 0:
                        full_output = "".join(accumulated_output)
                        sanitized = self.output_validator.filter_response(full_output)
                        if sanitized != full_output:
                            accumulated_output = [sanitized]

                    yield self.output_validator.filter_response(content)

            # Final validation
            full_output = "".join(accumulated_output)
            sanitized_output = self.output_validator.filter_response(full_output)
            if sanitized_output != full_output:
                _get_logger().info(
                    "output_sanitized",
                    before_length=len(full_output),
                    after_length=len(sanitized_output),
                )
                accumulated_output = [sanitized_output]

            duration_ms = (time.perf_counter() - start_time) * 1000

            # Record metrics
            self.metrics.record_summarization(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                model=self.config.model,
                duration_ms=duration_ms,
                success=True,
            )

        except (APIError, Timeout) as e:
            _get_logger().error("llm_call_failed", error=str(e))
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.record_summarization(
                input_tokens=input_tokens,
                output_tokens=0,
                model=self.config.model,
                duration_ms=duration_ms,
                success=False,
                error=str(e),
            )
            raise

    async def _call_llm_non_streaming(self, prompt: str, adaptive_max_tokens: bool = True) -> str:
        """Call LLM without streaming (for map phase).

        Args:
            prompt: Prompt text

        Returns:
            Complete response
        """
        import time

        start_time = time.perf_counter()
        input_tokens = self.token_counter.count_tokens(prompt)

        # Calculate adaptive max_tokens if enabled
        max_tokens = (
            self._calculate_max_tokens(input_tokens)
            if adaptive_max_tokens
            else self.config.max_tokens
        )

        # Prepare stop sequences if configured
        stop = self.config.stop_sequences if self.config.stop_sequences else None

        from openai import APIError, Timeout

        try:
            # Sanitize prompt before sending to LLM
            if self.injection_filter.detect_injection(prompt):
                _get_logger().warning("prompt_injection_detected", prompt_preview=prompt[:100])
                prompt = self.injection_filter.sanitize(prompt)

            response = await self.client.chat.completions.create(  # semgrep-ignore: llm-missing-error-handling, potential-prompt-injection-risk
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=max_tokens,
                stop=stop,
                stream=False,
            )

            content = response.choices[0].message.content or ""
            output_tokens = self.token_counter.count_tokens(content)
            duration_ms = (time.perf_counter() - start_time) * 1000

            self.metrics.record_summarization(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                model=self.config.model,
                duration_ms=duration_ms,
                success=True,
            )

            return self.output_validator.filter_response(content)

        except (APIError, Timeout) as e:
            _get_logger().error("llm_call_failed_non_streaming", error=str(e))
            duration_ms = (time.perf_counter() - start_time) * 1000
            self.metrics.record_summarization(
                input_tokens=input_tokens,
                output_tokens=0,
                model=self.config.model,
                duration_ms=duration_ms,
                success=False,
                error=str(e),
            )
            raise

    def _build_summary_prompt(
        self,
        content: str,
        query: str | None = None,
        sources: list[str] | None = None,
    ) -> str:
        """Build secure prompt for direct summarization.

        Uses structured prompt pattern (OWASP LLM01:2025) to prevent
        prompt injection attacks.

        Args:
            content: Content to summarize
            query: Optional query
            sources: Optional sources

        Returns:
            Secure structured prompt string
        """
        # Check for prompt injection in query
        if query and self.injection_filter.detect_injection(query):
            _get_logger().warning("prompt_injection_in_query", query_preview=query[:100])
            # Sanitize the query
            query = self.injection_filter.sanitize(query)

        # Build optimized system instructions (balanced for performance and quality)
        # Research: Concise prompts reduce latency without sacrificing quality
        # Reference: https://signoz.io/guides/open-ai-api-latency/
        system_instructions = [
            "Create a comprehensive summary of this web content in Markdown format.",
        ]

        if query:
            system_instructions.append(f"Focus on: {query}")

        system_instructions.extend(
            [
                "",
                "Requirements:",
                "- Highlight key points and important details",
                "- Preserve technical accuracy, code examples, and data",
                "- Use proper Markdown formatting (headings, lists, code blocks)",
            ]
        )

        # Build user data section
        user_data_parts = []

        if sources:
            user_data_parts.extend(
                [
                    "Source URLs:",
                    *[f"- {url}" for url in sources],
                    "",
                ]
            )

        user_data_parts.extend(
            [
                "Content to summarize:",
                content,
            ]
        )

        # Use structured prompt pattern for security
        return create_structured_prompt(
            system_instructions="\n".join(system_instructions),
            user_data="\n".join(user_data_parts),
        )

    def _build_map_prompt(self, chunk: str, query: str | None = None) -> str:
        """Build optimized prompt for map phase.

        Args:
            chunk: Text chunk to summarize
            query: Optional query

        Returns:
            Concise prompt string

        Note:
            Optimized for performance - clear directives reduce latency.
        """
        parts = ["Summarize the key information from this section:"]

        if query:
            parts.append(f"Focus on: {query}")

        parts.extend(["", chunk, "", "Summary:"])

        return "\n".join(parts)

    def _build_reduce_prompt(
        self,
        summaries: str,
        query: str | None = None,
        sources: list[str] | None = None,
    ) -> str:
        """Build optimized prompt for reduce phase.

        Args:
            summaries: Combined chunk summaries
            query: Optional query
            sources: Optional sources

        Returns:
            Concise prompt string

        Note:
            Optimized for performance - clear directives reduce latency.
        """
        parts = [
            "Combine these section summaries into a cohesive final summary.",
            "Use Markdown formatting with clear structure.",
        ]

        if query:
            parts.append(f"Focus on: {query}")

        parts.append("")

        if sources:
            parts.extend(["Sources:", *[f"- {url}" for url in sources], ""])

        parts.extend(
            [
                "Section summaries:",
                summaries,
                "",
                "Final summary:",
            ]
        )

        return "\n".join(parts)

    def _compute_content_hash(self, chunks: list[Chunk]) -> str:
        """Compute SHA-256 hash of chunk content for cache key.

        Args:
            chunks: List of chunks to hash

        Returns:
            Hex-encoded SHA-256 hash

        Note:
            Hash is based on concatenated chunk text to identify identical
            content regardless of source URL.
        """
        content = "".join(chunk.text for chunk in chunks)
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    async def close(self) -> None:
        """Close LLM client."""
        await self.client.close()
        _get_logger().info("summarizer_closed")
