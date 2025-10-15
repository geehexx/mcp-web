"""LLM-based summarization with map-reduce strategy.

Implements:
- Map-reduce summarization for long documents
- Query-aware abstractive summaries
- Streaming output
- Multiple LLM provider support (OpenAI, Anthropic)

Design Decision DD-006: Map-reduce summarization.
Design Decision DD-008: OpenAI GPT-4 default.
Design Decision DD-009: Streaming output.
"""

from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from mcp_web.chunker import Chunk
from mcp_web.config import SummarizerSettings
from mcp_web.metrics import get_metrics_collector
from mcp_web.security import (
    OutputValidator,
    PromptInjectionFilter,
    create_structured_prompt,
)
from mcp_web.utils import TokenCounter

import structlog

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

    def __init__(self, config: SummarizerSettings):
        """Initialize summarizer.

        Args:
            config: Summarizer configuration
        """
        self.config = config
        self.token_counter = TokenCounter()
        self.metrics = get_metrics_collector()

        # Security components (OWASP LLM Top 10)
        self.injection_filter = PromptInjectionFilter()
        self.output_validator = OutputValidator(max_output_length=config.max_summary_length)

        # Initialize OpenAI-compatible client
        api_key = config.get_api_key()
        api_base = config.get_api_base()

        if config.provider == "openai" and not api_key:
            _get_logger().warning(
                "no_openai_api_key", msg="OPENAI_API_KEY not set for OpenAI provider"
            )

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
    ) -> AsyncIterator[str]:
        """Summarize chunks with streaming output.

        Args:
            chunks: List of text chunks
            query: Optional query for focused summary
            sources: Optional list of source URLs

        Yields:
            Summary text chunks (streaming)
        """
        import time

        _get_logger().info(
            "summarization_start",
            num_chunks=len(chunks),
            query=query[:50] if query else None,
        )

        start_time = time.perf_counter()

        try:
            # Calculate total tokens
            total_tokens = sum(c.tokens for c in chunks)

            # Decide strategy: direct or map-reduce
            if total_tokens <= self.config.map_reduce_threshold:
                # Direct summarization
                async for chunk in self._summarize_direct(chunks, query, sources):
                    yield chunk
            else:
                # Map-reduce for large documents
                async for chunk in self._summarize_map_reduce(chunks, query, sources):
                    yield chunk

            duration_ms = (time.perf_counter() - start_time) * 1000

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
        async for chunk in self._call_llm(prompt):
            yield chunk

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
        """
        _get_logger().info("map_reduce_start", num_chunks=len(chunks))

        # Step 1: Map - Summarize each chunk
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
        async for chunk in self._call_llm(reduce_prompt):
            yield chunk

    async def _call_llm(self, prompt: str) -> AsyncIterator[str]:
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

        try:
            stream = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
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
                        if not self.output_validator.validate(full_output):
                            _get_logger().error(
                                "output_validation_failed_streaming", output_length=len(full_output)
                            )
                            # Stop streaming if validation fails
                            break

                    yield content

            # Final validation
            full_output = "".join(accumulated_output)
            if not self.output_validator.validate(full_output):
                _get_logger().error(
                    "output_validation_failed_final", output_length=len(full_output)
                )
                raise ValueError("Output validation failed: potentially unsafe content detected")

            duration_ms = (time.perf_counter() - start_time) * 1000

            # Record metrics
            self.metrics.record_summarization(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                model=self.config.model,
                duration_ms=duration_ms,
                success=True,
            )

        except Exception as e:
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

    async def _call_llm_non_streaming(self, prompt: str) -> str:
        """Call LLM without streaming (for map phase).

        Args:
            prompt: Prompt text

        Returns:
            Complete response
        """
        import time

        start_time = time.perf_counter()
        input_tokens = self.token_counter.count_tokens(prompt)

        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
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

            return content

        except Exception as e:
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

        # Build system instructions
        system_instructions = [
            "You are an expert at analyzing and summarizing web content.",
            "Your task is to create a comprehensive, well-structured summary.",
        ]

        if query:
            system_instructions.append(
                f"Focus your summary on this specific question or topic: {query}"
            )

        system_instructions.extend(
            [
                "",
                "Instructions:",
                "1. Create a clear, coherent summary in Markdown format",
                "2. Highlight key points, insights, and important details",
                "3. Preserve any code examples, technical details, or data",
                "4. Use proper Markdown formatting (headings, lists, code blocks)",
                "5. If the content is technical, maintain technical accuracy",
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
        """Build prompt for map phase.

        Args:
            chunk: Text chunk to summarize
            query: Optional query

        Returns:
            Prompt string
        """
        parts = [
            "Summarize the following section concisely, focusing on key information.",
        ]

        if query:
            parts.append(f"Pay special attention to content related to: {query}")

        parts.extend(
            [
                "",
                "Section:",
                "---",
                chunk,
                "---",
                "",
                "Concise summary:",
            ]
        )

        return "\n".join(parts)

    def _build_reduce_prompt(
        self,
        summaries: str,
        query: str | None = None,
        sources: list[str] | None = None,
    ) -> str:
        """Build prompt for reduce phase.

        Args:
            summaries: Combined chunk summaries
            query: Optional query
            sources: Optional sources

        Returns:
            Prompt string
        """
        parts = [
            "You are synthesizing multiple section summaries into a final, cohesive summary.",
            "",
        ]

        if query:
            parts.extend(
                [
                    f"Focus on this question/topic: {query}",
                    "",
                ]
            )

        parts.extend(
            [
                "Instructions:",
                "1. Combine the section summaries into a unified, well-structured summary",
                "2. Eliminate redundancy while preserving all important information",
                "3. Organize the content logically with clear headings",
                "4. Use Markdown formatting",
                "5. Maintain technical accuracy and detail",
                "",
            ]
        )

        if sources:
            parts.extend(
                [
                    "Sources:",
                    *[f"- {url}" for url in sources],
                    "",
                ]
            )

        parts.extend(
            [
                "Section summaries:",
                "---",
                summaries,
                "---",
                "",
                "Final synthesized summary:",
            ]
        )

        return "\n".join(parts)

    async def close(self) -> None:
        """Close LLM client."""
        await self.client.close()
        _get_logger().info("summarizer_closed")
