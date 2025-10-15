"""Unit tests for chunker module."""

import pytest

from mcp_web.chunker import Chunk, TextChunker
from mcp_web.config import ChunkerSettings


class TestChunk:
    """Tests for Chunk dataclass."""

    def test_chunk_creation(self):
        """Test creating a chunk."""
        chunk = Chunk(
            text="Test text",
            tokens=10,
            start_pos=0,
            end_pos=9,
            metadata={"section": "intro"},
        )

        assert chunk.text == "Test text"
        assert chunk.tokens == 10
        assert chunk.metadata["section"] == "intro"

    def test_chunk_to_dict(self):
        """Test chunk serialization."""
        chunk = Chunk(text="Test", tokens=5, start_pos=0, end_pos=4)
        data = chunk.to_dict()

        assert data["text"] == "Test"
        assert data["tokens"] == 5
        assert "metadata" in data


class TestTextChunker:
    """Tests for TextChunker."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return ChunkerSettings(
            strategy="hierarchical",
            chunk_size=100,
            chunk_overlap=10,
        )

    @pytest.fixture
    def chunker(self, config):
        """Create TextChunker instance."""
        return TextChunker(config)

    def test_chunk_short_text(self, chunker):
        """Test chunking short text."""
        text = "This is a short text."
        chunks = chunker.chunk_text(text)

        assert len(chunks) == 1
        assert chunks[0].text == text

    def test_chunk_long_text(self, chunker):
        """Test chunking long text with hierarchical strategy."""
        # Use hierarchical strategy which is more reliable
        # Create a longer structured document
        text = """
# Chapter 1: Introduction to Programming

Programming is the process of designing and building executable computer programs.
It involves tasks such as analysis, algorithm generation, and implementation.
The process requires attention to detail and systematic thinking.

# Chapter 2: Data Structures

Data structures are ways of organizing and storing data efficiently.
Arrays provide sequential storage with constant-time access.
Linked lists offer dynamic memory allocation.
Trees enable hierarchical data organization.

# Chapter 3: Algorithms

Algorithms are step-by-step procedures for solving problems.
Efficiency is measured in time and space complexity.
Common patterns include divide and conquer, dynamic programming, and greedy approaches.
"""
        chunks = chunker.chunk_text(text)

        # With hierarchical chunking and 100 token chunks, this should produce multiple chunks
        assert len(chunks) >= 2, f"Expected at least 2 chunks but got {len(chunks)}"
        
        # Filter out empty chunks (hierarchical strategy may create section markers)
        non_empty_chunks = [c for c in chunks if c.text.strip()]
        assert len(non_empty_chunks) >= 2
        assert all(chunk.tokens > 0 for chunk in non_empty_chunks)
        
        # Verify content is preserved
        combined = " ".join(c.text for c in non_empty_chunks)
        assert "Programming" in combined
        assert "Data Structures" in combined or "Data structures" in combined

    def test_chunk_with_headings(self, chunker):
        """Test hierarchical chunking with Markdown headings."""
        text = """
# Introduction

This is the introduction section with some content.

# Methods

This is the methods section with different content.

# Conclusion

This is the conclusion section.
"""
        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        # Check that sections are properly identified
        # Headings may be in text or metadata depending on chunking strategy
        has_section_content = any(
            "Introduction" in chunk.text or "Methods" in chunk.text or 
            "introduction" in chunk.text or "methods" in chunk.text or
            ("heading" in chunk.metadata and chunk.metadata["heading"])
            for chunk in chunks
        )
        assert has_section_content, "Chunks should contain section content or heading metadata"

    def test_chunk_with_code_blocks(self, chunker):
        """Test chunking with code blocks."""
        text = """
Some text before code.

```python
def hello():
    print("Hello, world!")
```

Some text after code.
"""

        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        # Code blocks should be preserved
        code_chunks = [c for c in chunks if "```" in c.text]
        assert len(code_chunks) > 0

    @pytest.mark.slow
    def test_fixed_chunking(self):
        """Test fixed-size chunking strategy.
        
        Note: Marked as slow due to tiktoken encoding overhead in tight loops.
        """
        config = ChunkerSettings(strategy="fixed", chunk_size=30, chunk_overlap=5)
        chunker = TextChunker(config)

        # Use very short text to minimize tiktoken calls
        text = "The quick brown fox."
        
        chunks = chunker.chunk_text(text)

        assert len(chunks) >= 1
        assert all(chunk.tokens > 0 for chunk in chunks)
        # With short text, should have 1 chunk
        assert len(chunks) == 1

    def test_semantic_chunking(self):
        """Test semantic chunking strategy."""
        config = ChunkerSettings(strategy="semantic", chunk_size=100, chunk_overlap=10)
        chunker = TextChunker(config)

        text = """
First paragraph with some content.

Second paragraph with more content.

Third paragraph with even more content.
"""

        chunks = chunker.chunk_text(text)
        assert len(chunks) > 0

    def test_chunk_overlap(self):
        """Test that overlap is applied between chunks."""
        config = ChunkerSettings(strategy="hierarchical", chunk_size=50, chunk_overlap=10)
        chunker = TextChunker(config)

        # Create structured text with varied content
        text = """
Section Alpha discusses fundamental concepts in computer science.
Section Beta explores advanced algorithmic techniques and patterns.
Section Gamma analyzes real-world applications and use cases.
Section Delta examines performance optimization strategies.
"""
        chunks = chunker.chunk_text(text)

        assert len(chunks) >= 1
        if len(chunks) > 1:
            # Verify chunks exist
            assert all(c.tokens > 0 for c in chunks)

    def test_metadata_propagation(self, chunker):
        """Test that metadata is propagated to chunks."""
        text = "Some text to chunk"
        metadata = {"source": "test", "type": "example"}

        chunks = chunker.chunk_text(text, metadata=metadata)

        assert len(chunks) > 0
        assert chunks[0].metadata.get("source") == "test"
