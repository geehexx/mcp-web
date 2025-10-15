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

from mcp_web.config import ChunkerSettings
from mcp_web.metrics import get_metrics_collector
from mcp_web.utils import TokenCounter

logger = None


def _get_logger():
    """Lazy logger initialization."""
    global logger
    if logger is None:
        import structlog

        logger = structlog.get_logger()
    return logger


@dataclass
class Chunk:
    """Text chunk with metadata."""

    text: str
    tokens: int
    start_pos: int
    end_pos: int
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
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

    def chunk_text(self, text: str, metadata: dict | None = None) -> list[Chunk]:
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

        if self.config.strategy == "hierarchical":
            chunks = self._chunk_hierarchical(text, metadata)
        elif self.config.strategy == "semantic":
            chunks = self._chunk_semantic(text, metadata)
        else:  # fixed
            chunks = self._chunk_fixed(text, metadata)

        duration_ms = (time.perf_counter() - start_time) * 1000

        # Record metrics
        avg_chunk_size = sum(c.tokens for c in chunks) / len(chunks) if chunks else 0
        self.metrics.record_chunking(
            content_length=len(text),
            num_chunks=len(chunks),
            avg_chunk_size=avg_chunk_size,
            duration_ms=duration_ms,
        )

        _get_logger().info(
            "chunking_complete",
            num_chunks=len(chunks),
            avg_tokens=round(avg_chunk_size, 1),
            duration_ms=round(duration_ms, 2),
        )

        return chunks

    def _chunk_hierarchical(self, text: str, metadata: dict | None = None) -> list[Chunk]:
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

            if section_tokens <= self.config.chunk_size:
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
                section_chunks = self._split_large_section(section_text, section_metadata)
                chunks.extend(section_chunks)

        # Handle overlap between chunks
        chunks = self._add_overlap(chunks, text)

        return chunks

    def _chunk_semantic(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        """Chunk text at semantic boundaries (paragraphs, sentences).

        Args:
            text: Input text
            metadata: Optional metadata

        Returns:
            List of chunks
        """
        chunks = []
        metadata = metadata or {}

        # Split into paragraphs
        paragraphs = self._split_paragraphs(text)

        current_chunk_text = []
        current_chunk_tokens = 0
        start_pos = 0

        for para in paragraphs:
            para_tokens = self.token_counter.count_tokens(para)

            # Check if paragraph fits in current chunk
            if current_chunk_tokens + para_tokens <= self.config.chunk_size:
                current_chunk_text.append(para)
                current_chunk_tokens += para_tokens
            else:
                # Save current chunk if not empty
                if current_chunk_text:
                    chunk_text = "\n\n".join(current_chunk_text)
                    chunks.append(
                        Chunk(
                            text=chunk_text,
                            tokens=current_chunk_tokens,
                            start_pos=start_pos,
                            end_pos=start_pos + len(chunk_text),
                            metadata=metadata.copy(),
                        )
                    )
                    start_pos += len(chunk_text)

                # Start new chunk
                if para_tokens > self.config.max_chunk_size:
                    # Paragraph too large, split by sentences
                    para_chunks = self._split_by_sentences(para, metadata)
                    chunks.extend(para_chunks)
                    current_chunk_text = []
                    current_chunk_tokens = 0
                else:
                    current_chunk_text = [para]
                    current_chunk_tokens = para_tokens

        # Add final chunk
        if current_chunk_text:
            chunk_text = "\n\n".join(current_chunk_text)
            chunks.append(
                Chunk(
                    text=chunk_text,
                    tokens=current_chunk_tokens,
                    start_pos=start_pos,
                    end_pos=start_pos + len(chunk_text),
                    metadata=metadata.copy(),
                )
            )

        # Add overlap
        chunks = self._add_overlap(chunks, text)

        return chunks

    def _chunk_fixed(self, text: str, metadata: dict | None = None) -> list[Chunk]:
        """Chunk text into fixed-size chunks with overlap.

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
        chunk_size_chars = self.config.chunk_size * 4
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
            start += len(chunk_text) - overlap_chars

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

        sections = []
        current_heading = "Introduction"
        current_content = []

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

    def _split_large_section(self, text: str, metadata: dict) -> list[Chunk]:
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
                return self._chunk_with_code_blocks(text, code_blocks, metadata)

        # Fall back to paragraph splitting
        return self._chunk_semantic(text, metadata)

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

    def _split_by_sentences(self, text: str, metadata: dict) -> list[Chunk]:
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

        for sentence in sentences:
            sentence_tokens = self.token_counter.count_tokens(sentence)

            if current_tokens + sentence_tokens <= self.config.chunk_size:
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
        self, text: str, code_blocks: list[tuple[int, int, str]], metadata: dict
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
                before_chunks = self._chunk_semantic(before_text, metadata)
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
            remaining_chunks = self._chunk_semantic(remaining_text, metadata)
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
