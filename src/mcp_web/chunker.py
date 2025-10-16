"""Intelligent text chunking for LLM processing.

Implements:
- Hierarchical chunking (respects document structure)
- Semantic chunking (sentence/paragraph boundaries)
- Fixed-size chunking with overlap

Design Decision DD-003: Hierarchical + semantic chunking.
Design Decision DD-004: 512-token chunks with 50-token overlap.
Design Decision DD-009: Keep code blocks intact.
"""

import re
from dataclasses import dataclass, field
from typing import Any

import structlog

from mcp_web.config import ChunkerSettings
from mcp_web.metrics import get_metrics_collector
from mcp_web.utils import (
    TokenCounter,
    average_sentence_word_count,
    calculate_code_block_ratio,
)

logger: structlog.stdlib.BoundLogger | None = None


def _get_logger() -> structlog.stdlib.BoundLogger:
    """Lazy logger initialization."""
    global logger
    if logger is None:
        logger = structlog.get_logger()
    return logger


@dataclass
class Chunk:
    """Text chunk with metadata."""

    text: str
    tokens: int
    start_pos: int
    end_pos: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "text": self.text,
            "tokens": self.tokens,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "metadata": self.metadata,
        }


class TextChunker:
    """Intelligent text chunking for LLM processing.

    Example:
        >>> chunker = TextChunker(config)
        >>> chunks = chunker.chunk_text(long_text)
        >>> print(len(chunks))
        10
    """

    def __init__(self, config: ChunkerSettings):
        """Initialize text chunker.

        Args:
            config: Chunker configuration
        """
        self.config = config
        self.token_counter = TokenCounter()
        self.metrics = get_metrics_collector()

    def chunk_text(self, text: str, metadata: dict[str, Any] | None = None) -> list[Chunk]:
        """Chunk text using configured strategy.

        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to chunks

        Returns:
            List of Chunk objects
        """
        import time

        start_time = time.perf_counter()

        _get_logger().info(
            "chunking_start",
            strategy=self.config.strategy,
            text_length=len(text),
        )

        effective_chunk_size = self._select_chunk_size(text)

        _get_logger().debug(
            "chunking_strategy_selected",
            requested_strategy=self.config.strategy,
            adaptive_enabled=self.config.adaptive_chunking,
            effective_chunk_size=effective_chunk_size,
        )

        if self.config.strategy == "hierarchical":
            chunks = self._chunk_hierarchical(text, metadata, effective_chunk_size)
        elif self.config.strategy == "semantic":
            chunks = self._chunk_semantic(text, metadata, effective_chunk_size)
        else:  # fixed
            chunks = self._chunk_fixed(text, metadata, effective_chunk_size)

        # Remove empty/zero-token chunks that may appear from structural splits
        chunks = [chunk for chunk in chunks if chunk.tokens > 0 and chunk.text.strip()]

        duration_ms = (time.perf_counter() - start_time) * 1000

        # Record metrics
        avg_chunk_size = sum(c.tokens for c in chunks) / len(chunks) if chunks else 0
        self.metrics.record_chunking(
            content_length=len(text),
            num_chunks=len(chunks),
            avg_chunk_size=avg_chunk_size,
            duration_ms=duration_ms,
            strategy=self.config.strategy,
            adaptive_enabled=self.config.adaptive_chunking,
            target_chunk_size=effective_chunk_size,
        )

        _get_logger().info(
            "chunking_complete",
            num_chunks=len(chunks),
            avg_tokens=round(avg_chunk_size, 1),
            duration_ms=round(duration_ms, 2),
        )

        return chunks

    def _chunk_hierarchical(
        self, text: str, metadata: dict[str, Any] | None = None, chunk_size: int | None = None
    ) -> list[Chunk]:
        """Chunk text hierarchically (headings → paragraphs → sentences).

        Args:
            text: Input text
            metadata: Optional metadata

        Returns:
            List of chunks
        """
        chunks = []
        metadata = metadata or {}

        # Split by headings (Markdown format)
        sections = self._split_by_headings(text)

        for section_heading, section_text in sections:
            section_metadata = {**metadata, "heading": section_heading}

            # Check if section fits in one chunk
            section_tokens = self.token_counter.count_tokens(section_text)

            target_size = chunk_size or self.config.chunk_size

            if section_tokens <= target_size:
                # Section fits in one chunk
                chunks.append(
                    Chunk(
                        text=section_text,
                        tokens=section_tokens,
                        start_pos=text.find(section_text),
                        end_pos=text.find(section_text) + len(section_text),
                        metadata=section_metadata,
                    )
                )
            else:
                # Section needs splitting
                section_chunks = self._split_large_section(
                    section_text, section_metadata, target_size
                )
                chunks.extend(section_chunks)

        # Handle overlap between chunks
        chunks = self._add_overlap(chunks, text)

        return chunks

    def _chunk_semantic(
        self, text: str, metadata: dict[str, Any] | None = None, chunk_size: int | None = None
    ) -> list[Chunk]:
        """Chunk text by semantic boundaries using recursive splitting.

        Based on research from Pinecone and Databricks (2024):
        - Uses hierarchical separators: paragraphs -> sentences -> words
        - Preserves logical boundaries for better context
        - Optimized for 200-500 token chunks with 10-20% overlap

        References:
        - https://www.pinecone.io/learn/chunking-strategies/
        - https://community.databricks.com/t5/technical-blog/the-ultimate-guide-to-chunking-strategies-for-rag-applications/ba-p/113089

        Args:
            text: Input text
            metadata: Optional metadata

        Returns:
            List of chunks with enhanced metadata
        """
        chunks = []
        metadata = metadata or {}

        # Recursive splitting with semantic separators (best practice from LangChain)
        # Order matters: try larger boundaries first
        separators = ["\n\n", "\n", ". ", "! ", "? ", "; ", ": ", " ", ""]

        # Split text recursively
        current_chunks = [text]

        target_size = chunk_size or self.config.chunk_size

        for separator in separators:
            new_chunks = []
            for chunk_text in current_chunks:
                # If chunk is small enough, keep it
                if self.token_counter.count_tokens(chunk_text) <= target_size:
                    new_chunks.append(chunk_text)
                else:
                    # Split by current separator
                    parts = chunk_text.split(separator)
                    combined = ""

                    for part in parts:
                        if not part.strip():
                            continue

                        test_combined = combined + separator + part if combined else part

                        if self.token_counter.count_tokens(test_combined) <= target_size:
                            combined = test_combined
                        else:
                            if combined:
                                new_chunks.append(combined)
                            combined = part

                    if combined:
                        new_chunks.append(combined)

            current_chunks = new_chunks

            # If all chunks are within size, we're done
            if all(self.token_counter.count_tokens(c) <= target_size for c in current_chunks):
                break

        # Convert to Chunk objects with metadata
        start_pos = 0
        for i, chunk_text in enumerate(current_chunks):
            if not chunk_text.strip():
                continue

            tokens = self.token_counter.count_tokens(chunk_text)
            chunk_metadata = metadata.copy()
            chunk_metadata["semantic_split"] = True
            chunk_metadata["chunk_index"] = i
            chunk_metadata["total_chunks"] = len(current_chunks)

            chunks.append(
                Chunk(
                    text=chunk_text.strip(),
                    tokens=tokens,
                    start_pos=start_pos,
                    end_pos=start_pos + len(chunk_text),
                    metadata=chunk_metadata,
                )
            )
            start_pos += len(chunk_text)

        # Add overlap
        chunks = self._add_overlap(chunks, text)

        return chunks

    def _chunk_fixed(
        self, text: str, metadata: dict[str, Any] | None = None, chunk_size: int | None = None
    ) -> list[Chunk]:
        """Chunk text into fixed-size chunks with overlap.

        Note: This strategy has performance issues with tiktoken encoding on
        repetitive text patterns. Consider using semantic or hierarchical
        chunking for better performance and context preservation.

        Research (2024) recommends:
        - General text: 200-500 tokens, 10-20% overlap
        - Code/technical: 100-200 tokens, 15-25% overlap
        - Current default: 512 tokens, ~10% overlap ✓

        References:
        - https://www.pinecone.io/learn/chunking-strategies/
        - MongoDB study: ~100 tokens, ~15 overlap for Python docs

        Args:
            text: Input text
            metadata: Optional metadata

        Returns:
            List of chunks
        """
        chunks = []
        metadata = metadata or {}

        # Calculate chunk size in characters (approximate)
        # Rough estimate: 1 token ≈ 4 characters
        target_size = chunk_size or self.config.chunk_size
        chunk_size_chars = target_size * 4
        overlap_chars = self.config.chunk_overlap * 4

        start = 0
        while start < len(text):
            end = start + chunk_size_chars
            chunk_text = text[start:end]

            # Adjust to sentence boundary if possible
            if end < len(text):
                # Look for sentence ending
                sentence_end = self._find_sentence_boundary(chunk_text)
                if sentence_end > 0:
                    chunk_text = chunk_text[:sentence_end]

            tokens = self.token_counter.count_tokens(chunk_text)

            if not chunk_text:
                break

            chunks.append(
                Chunk(
                    text=chunk_text,
                    tokens=tokens,
                    start_pos=start,
                    end_pos=start + len(chunk_text),
                    metadata=metadata.copy(),
                )
            )

            # Move start with overlap
            advance = len(chunk_text) - overlap_chars
            if advance <= 0:
                advance = len(chunk_text) or chunk_size_chars or 1
            start += advance

            # Prevent infinite loop
            if start + chunk_size_chars <= start:
                start += chunk_size_chars

        return chunks

    def _split_by_headings(self, text: str) -> list[tuple[str, str]]:
        """Split text by Markdown headings.

        Args:
            text: Markdown text

        Returns:
            List of (heading, content) tuples
        """
        # Match Markdown headings (# Heading)
        heading_pattern = r"^(#{1,6})\s+(.+)$"
        lines = text.split("\n")

        sections: list[tuple[str, str]] = []
        current_heading = "Introduction"
        current_content: list[str] = []

        for line in lines:
            match = re.match(heading_pattern, line)
            if match:
                # Save previous section
                if current_content:
                    sections.append((current_heading, "\n".join(current_content)))

                # Start new section
                current_heading = match.group(2).strip()
                current_content = []
            else:
                current_content.append(line)

        # Add final section
        if current_content:
            sections.append((current_heading, "\n".join(current_content)))

        return sections if sections else [("Main Content", text)]

    def _split_large_section(
        self, text: str, metadata: dict[str, Any], chunk_size: int
    ) -> list[Chunk]:
        """Split large section into multiple chunks.

        Args:
            text: Section text
            metadata: Section metadata

        Returns:
            List of chunks
        """
        # Check for code blocks first
        if self.config.preserve_code_blocks:
            code_blocks = self._extract_code_blocks(text)
            if code_blocks:
                return self._chunk_with_code_blocks(text, code_blocks, metadata, chunk_size)

        # Fall back to paragraph splitting
        return self._chunk_semantic(text, metadata, chunk_size)

    def _split_paragraphs(self, text: str) -> list[str]:
        """Split text into paragraphs.

        Args:
            text: Input text

        Returns:
            List of paragraphs
        """
        # Split on double newlines
        paragraphs = re.split(r"\n\s*\n", text)
        return [p.strip() for p in paragraphs if p.strip()]

    def _split_by_sentences(
        self, text: str, metadata: dict[str, Any], chunk_size: int
    ) -> list[Chunk]:
        """Split text by sentences.

        Args:
            text: Input text
            metadata: Metadata

        Returns:
            List of chunks
        """
        # Simple sentence splitting (can be improved with NLTK)
        sentence_pattern = r"[.!?]+(?:\s+|$)"
        sentences = re.split(sentence_pattern, text)
        sentences = [s.strip() for s in sentences if s.strip()]

        chunks = []
        current_text = []
        current_tokens = 0
        start_pos = 0

        target_size = chunk_size

        for sentence in sentences:
            sentence_tokens = self.token_counter.count_tokens(sentence)

            if current_tokens + sentence_tokens <= target_size:
                current_text.append(sentence)
                current_tokens += sentence_tokens
            else:
                if current_text:
                    chunk_text = " ".join(current_text)
                    chunks.append(
                        Chunk(
                            text=chunk_text,
                            tokens=current_tokens,
                            start_pos=start_pos,
                            end_pos=start_pos + len(chunk_text),
                            metadata=metadata.copy(),
                        )
                    )
                    start_pos += len(chunk_text)

                current_text = [sentence]
                current_tokens = sentence_tokens

        if current_text:
            chunk_text = " ".join(current_text)
            chunks.append(
                Chunk(
                    text=chunk_text,
                    tokens=current_tokens,
                    start_pos=start_pos,
                    end_pos=start_pos + len(chunk_text),
                    metadata=metadata.copy(),
                )
            )

        return chunks

    def _extract_code_blocks(self, text: str) -> list[tuple[int, int, str]]:
        """Extract code block positions.

        Args:
            text: Text with code blocks

        Returns:
            List of (start, end, code) tuples
        """
        pattern = r"```.*?\n(.*?)```"
        blocks = []

        for match in re.finditer(pattern, text, re.DOTALL):
            blocks.append((match.start(), match.end(), match.group(0)))

        return blocks

    def _chunk_with_code_blocks(
        self,
        text: str,
        code_blocks: list[tuple[int, int, str]],
        metadata: dict[str, Any],
        chunk_size: int,
    ) -> list[Chunk]:
        """Chunk text while preserving code blocks.

        Args:
            text: Input text
            code_blocks: List of code block positions
            metadata: Metadata

        Returns:
            List of chunks
        """
        chunks = []
        last_end = 0

        for start, end, code in code_blocks:
            # Chunk text before code block
            before_text = text[last_end:start].strip()
            if before_text:
                before_chunks = self._chunk_semantic(before_text, metadata, chunk_size)
                chunks.extend(before_chunks)

            # Add code block as separate chunk (if not too large)
            code_tokens = self.token_counter.count_tokens(code)
            if code_tokens <= self.config.max_chunk_size:
                chunks.append(
                    Chunk(
                        text=code,
                        tokens=code_tokens,
                        start_pos=start,
                        end_pos=end,
                        metadata={**metadata, "type": "code"},
                    )
                )
            else:
                # Code block too large, split it
                _get_logger().warning(
                    "code_block_too_large",
                    tokens=code_tokens,
                    max_size=self.config.max_chunk_size,
                )
                # Include it anyway, but mark it
                chunks.append(
                    Chunk(
                        text=code,
                        tokens=code_tokens,
                        start_pos=start,
                        end_pos=end,
                        metadata={**metadata, "type": "code", "oversized": True},
                    )
                )

            last_end = end

        # Chunk remaining text
        remaining_text = text[last_end:].strip()
        if remaining_text:
            remaining_chunks = self._chunk_semantic(remaining_text, metadata, chunk_size)
            chunks.extend(remaining_chunks)

        return chunks

    def _add_overlap(self, chunks: list[Chunk], _original_text: str) -> list[Chunk]:
        """Add overlap between chunks.

        Args:
            chunks: List of chunks
            original_text: Original text

        Returns:
            Chunks with overlap
        """
        if len(chunks) <= 1 or self.config.chunk_overlap == 0:
            return chunks

        overlapped_chunks = []

        for i, chunk in enumerate(chunks):
            if i == 0:
                # First chunk - add suffix from next chunk
                overlapped_chunks.append(chunk)
            else:
                # Add prefix from previous chunk
                prev_chunk = chunks[i - 1]
                overlap_text = self.token_counter.truncate_to_tokens(
                    prev_chunk.text, self.config.chunk_overlap
                )

                # Find actual overlap position in prev chunk
                if overlap_text:
                    new_text = overlap_text + "\n" + chunk.text
                    new_tokens = self.token_counter.count_tokens(new_text)

                    overlapped_chunks.append(
                        Chunk(
                            text=new_text,
                            tokens=new_tokens,
                            start_pos=chunk.start_pos,
                            end_pos=chunk.end_pos,
                            metadata=chunk.metadata,
                        )
                    )
                else:
                    overlapped_chunks.append(chunk)

        return overlapped_chunks

    def _select_chunk_size(self, text: str) -> int:
        """Determine effective chunk size based on content characteristics.

        Args:
            text: Source content to analyse.

        Returns:
            Chunk size in tokens respecting configured minimum and maximum bounds.
        """

        if not self.config.adaptive_chunking or not text.strip():
            return self.config.chunk_size

        base_min = self.config.min_chunk_size
        base_max = self.config.max_chunk_size

        code_ratio = calculate_code_block_ratio(text)
        if code_ratio >= self.config.code_block_threshold:
            return max(base_min, min(self.config.code_chunk_size, base_max))

        avg_words = average_sentence_word_count(text)
        if avg_words >= self.config.dense_sentence_threshold:
            return max(base_min, min(self.config.dense_chunk_size, base_max))

        return max(base_min, min(self.config.chunk_size, base_max))

    def _find_sentence_boundary(self, text: str) -> int:
        """Find the last sentence boundary in text.

        Args:
            text: Input text

        Returns:
            Position of boundary, or -1 if not found
        """
        # Look for sentence endings in last 20% of text
        search_start = max(0, int(len(text) * 0.8))
        search_text = text[search_start:]

        # Find last sentence ending
        pattern = r"[.!?]+\s"
        matches = list(re.finditer(pattern, search_text))

        if matches:
            last_match = matches[-1]
            return search_start + last_match.end()

        return -1
