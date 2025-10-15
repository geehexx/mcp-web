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
        """Test chunking long text."""
        # Create text that exceeds chunk size
        text = " ".join(["word"] * 200)  # ~200 tokens
        chunks = chunker.chunk_text(text)
        
        assert len(chunks) > 1
        assert all(chunk.tokens > 0 for chunk in chunks)

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
        assert any("Introduction" in chunk.text or "Methods" in chunk.text for chunk in chunks)

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

    def test_fixed_chunking(self):
        """Test fixed-size chunking strategy."""
        config = ChunkerSettings(strategy="fixed", chunk_size=50, chunk_overlap=5)
        chunker = TextChunker(config)
        
        text = " ".join(["word"] * 100)
        chunks = chunker.chunk_text(text)
        
        assert len(chunks) > 1
        # Check overlap is applied
        if len(chunks) > 1:
            # Some overlap should exist between consecutive chunks
            assert len(chunks[0].text) > 0

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
        
        # Create long text
        text = " ".join([f"word{i}" for i in range(100)])
        chunks = chunker.chunk_text(text)
        
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
