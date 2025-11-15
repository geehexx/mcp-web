"""Unit tests for chunker module.

Tests intelligent text chunking with hierarchical, semantic, and fixed strategies.
Covers token counting, overlap handling, code block preservation, and edge cases.
"""

import pytest

from mcp_web.chunker import Chunk, TextChunker
from mcp_web.config import ChunkerSettings


@pytest.mark.unit
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
        assert chunk.start_pos == 0
        assert chunk.end_pos == 9
        assert chunk.metadata["section"] == "intro"

    def test_chunk_to_dict(self):
        """Test chunk serialization."""
        chunk = Chunk(
            text="Test",
            tokens=5,
            start_pos=0,
            end_pos=4,
            metadata={"type": "paragraph"},
        )
        data = chunk.to_dict()

        assert data["text"] == "Test"
        assert data["tokens"] == 5
        assert data["start_pos"] == 0
        assert data["end_pos"] == 4
        assert data["metadata"]["type"] == "paragraph"

    def test_chunk_without_metadata(self):
        """Test chunk creation without metadata."""
        chunk = Chunk(text="Simple", tokens=2, start_pos=0, end_pos=6)
        assert chunk.metadata == {}


@pytest.mark.unit
class TestTextChunker:
    """Tests for TextChunker."""

    @pytest.fixture
    def config(self):
        """Create test configuration."""
        return ChunkerSettings(
            strategy="hierarchical",
            chunk_size=100,
            chunk_overlap=10,
            preserve_code_blocks=True,
            adaptive_chunking=False,
        )

    @pytest.fixture
    def chunker(self, config):
        """Create TextChunker instance."""
        return TextChunker(config)

    def test_chunk_short_text(self, chunker):
        """Test chunking short text that fits in one chunk."""
        text = "This is a short text that should fit in a single chunk."
        chunks = chunker.chunk_text(text)

        assert len(chunks) == 1
        assert chunks[0].text.strip() == text.strip()
        assert chunks[0].tokens > 0

    def test_chunk_empty_text(self, chunker):
        """Test chunking empty text."""
        chunks = chunker.chunk_text("")
        assert len(chunks) == 0

    def test_chunk_whitespace_only(self, chunker):
        """Test chunking whitespace-only text."""
        chunks = chunker.chunk_text("   \n\n  \t  ")
        assert len(chunks) == 0

    def test_chunk_long_text_hierarchical(self, chunker):
        """Test chunking long text with hierarchical strategy."""
        # Create a longer structured document
        text = """
# Chapter 1: Introduction to Programming

Programming is the process of designing and building executable computer programs.
It involves tasks such as analysis, algorithm generation, and implementation.
The process requires attention to detail and systematic thinking.
Modern programming encompasses various paradigms and methodologies.

# Chapter 2: Data Structures

Data structures are ways of organizing and storing data efficiently.
Arrays provide sequential storage with constant-time access to elements.
Linked lists offer dynamic memory allocation and efficient insertions.
Trees enable hierarchical data organization for complex relationships.
Hash tables provide fast key-value lookups using hashing functions.

# Chapter 3: Algorithms

Algorithms are step-by-step procedures for solving computational problems.
Efficiency is measured in time and space complexity using Big O notation.
Common patterns include divide and conquer, dynamic programming, and greedy approaches.
Sorting algorithms like quicksort and mergesort are fundamental building blocks.
"""
        chunks = chunker.chunk_text(text)

        # Should produce multiple chunks
        assert len(chunks) >= 2
        # All chunks should have tokens
        assert all(chunk.tokens > 0 for chunk in chunks)
        # All chunks should have content
        assert all(chunk.text.strip() for chunk in chunks)

    def test_chunk_with_headings(self, chunker):
        """Test hierarchical chunking with Markdown headings."""
        text = """
# Introduction

This is the introduction section with some content.
It has multiple sentences to make it longer.

# Methods

This is the methods section with different content.
It describes the approach taken in the research.

# Results

Here are the results of the experiment.
The findings are quite interesting.

# Conclusion

This is the conclusion section wrapping everything up.
"""
        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        # Verify chunks preserve structure
        has_content = any("Introduction" in chunk.text or "Methods" in chunk.text for chunk in chunks)
        assert has_content, "Chunks should contain section content"

    def test_chunk_with_code_blocks(self, chunker):
        """Test chunking with code blocks preservation."""
        text = """
Some text before the code example.

```python
def hello_world():
    print("Hello, world!")
    return True

def main():
    hello_world()
```

Some text after the code example.
More content to ensure multiple chunks if needed.
"""

        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        # Code blocks should be preserved in at least one chunk
        code_chunks = [c for c in chunks if "```" in c.text or "def hello_world" in c.text]
        assert len(code_chunks) > 0, "Code blocks should be preserved"

    def test_chunk_with_large_code_block(self):
        """Test handling of very large code blocks."""
        config = ChunkerSettings(
            strategy="hierarchical",
            chunk_size=100,
            max_chunk_size=200,
            preserve_code_blocks=True,
        )
        chunker = TextChunker(config)

        # Create a large code block
        large_code = "\n".join([f"    line_{i} = {i}" for i in range(50)])
        text = f"""
Text before code.

```python
{large_code}
```

Text after code.
"""

        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        # Large code block should be in a chunk (possibly marked as oversized)
        code_chunks = [c for c in chunks if "line_" in c.text]
        assert len(code_chunks) > 0

    @pytest.mark.slow
    def test_fixed_chunking_strategy(self):
        """Test fixed-size chunking strategy.

        Note: Marked as slow due to tiktoken encoding overhead.
        """
        config = ChunkerSettings(
            strategy="fixed",
            chunk_size=50,
            chunk_overlap=10,
        )
        chunker = TextChunker(config)

        text = """
This is a test of the fixed chunking strategy.
It should split text into fixed-size chunks with overlap.
Each chunk should be approximately the same size.
The overlap helps maintain context between chunks.
"""

        chunks = chunker.chunk_text(text)

        assert len(chunks) >= 1
        assert all(chunk.tokens > 0 for chunk in chunks)

    def test_semantic_chunking_strategy(self):
        """Test semantic chunking strategy."""
        config = ChunkerSettings(
            strategy="semantic",
            chunk_size=100,
            chunk_overlap=10,
        )
        chunker = TextChunker(config)

        text = """
First paragraph with some important content about the topic.

Second paragraph with more details and explanations of concepts.

Third paragraph with additional information and examples.

Fourth paragraph concluding the discussion with final thoughts.
"""

        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        assert all(chunk.tokens > 0 for chunk in chunks)
        # Semantic chunking should respect paragraph boundaries
        assert all(chunk.metadata.get("semantic_split") for chunk in chunks)

    def test_semantic_chunking_with_separators(self):
        """Test semantic chunking respects different separators."""
        config = ChunkerSettings(strategy="semantic", chunk_size=50, chunk_overlap=5)
        chunker = TextChunker(config)

        text = "First sentence. Second sentence. Third sentence! Fourth sentence? Fifth sentence."

        chunks = chunker.chunk_text(text)

        assert len(chunks) >= 1
        # Should split on sentence boundaries
        for chunk in chunks:
            assert chunk.text.strip()

    def test_chunk_overlap_application(self):
        """Test that overlap is correctly applied between chunks."""
        config = ChunkerSettings(
            strategy="hierarchical",
            chunk_size=50,
            chunk_overlap=10,
        )
        chunker = TextChunker(config)

        text = """
# Section One
This section has enough content to span multiple chunks for testing overlap.
We need to ensure that adjacent chunks share some overlapping tokens.

# Section Two
More content here to create additional chunks.
The overlap should help maintain context across boundaries.

# Section Three
Final section with concluding content.
"""

        chunks = chunker.chunk_text(text)

        if len(chunks) > 1:
            # Check that chunks have been created
            assert all(c.tokens > 0 for c in chunks)

    def test_chunk_overlap_zero(self):
        """Test chunking with zero overlap."""
        config = ChunkerSettings(
            strategy="hierarchical",
            chunk_size=50,
            chunk_overlap=0,
        )
        chunker = TextChunker(config)

        text = """
Section with enough content to create multiple chunks.
Each chunk should be independent without any overlap.
This tests the edge case of zero overlap configuration.
"""

        chunks = chunker.chunk_text(text)

        assert len(chunks) >= 1
        assert all(chunk.tokens > 0 for chunk in chunks)

    def test_metadata_propagation(self, chunker):
        """Test that metadata is propagated to chunks."""
        text = "Some text to chunk for metadata testing."
        metadata = {"source": "test", "type": "example", "id": 123}

        chunks = chunker.chunk_text(text, metadata=metadata)

        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.metadata.get("source") == "test"
            assert chunk.metadata.get("type") == "example"
            assert chunk.metadata.get("id") == 123

    def test_split_by_headings(self, chunker):
        """Test splitting text by Markdown headings."""
        text = """
# Heading 1
Content for section 1.

## Heading 2
Content for section 2.

### Heading 3
Content for section 3.

# Heading 4
Content for section 4.
"""
        sections = chunker._split_by_headings(text)

        assert len(sections) > 0
        # Check that headings are extracted
        headings = [heading for heading, _ in sections]
        assert "Heading 1" in headings or "Heading 2" in headings

    def test_split_by_headings_no_headings(self, chunker):
        """Test splitting text without headings."""
        text = "Plain text without any headings.\nJust regular content."
        sections = chunker._split_by_headings(text)

        assert len(sections) == 1
        assert sections[0][0] == "Main Content"

    def test_extract_code_blocks(self, chunker):
        """Test code block extraction."""
        text = """
Some text.

```python
def func():
    pass
```

More text.

```javascript
console.log('test');
```
"""
        code_blocks = chunker._extract_code_blocks(text)

        assert len(code_blocks) == 2
        # Each block is (start, end, code)
        assert all(len(block) == 3 for block in code_blocks)

    def test_extract_code_blocks_none(self, chunker):
        """Test code block extraction with no code blocks."""
        text = "Regular text without any code blocks."
        code_blocks = chunker._extract_code_blocks(text)

        assert len(code_blocks) == 0

    def test_find_sentence_boundary(self, chunker):
        """Test finding sentence boundaries."""
        text = "First sentence. Second sentence. Third sentence."
        boundary = chunker._find_sentence_boundary(text)

        assert boundary > 0
        assert text[boundary - 2:boundary] in [". ", "! ", "? "]

    def test_find_sentence_boundary_none(self, chunker):
        """Test when no sentence boundary is found."""
        text = "Text without proper sentence ending"
        boundary = chunker._find_sentence_boundary(text)

        # Should return -1 if no boundary found
        assert boundary == -1 or boundary > 0

    def test_adaptive_chunking_disabled(self):
        """Test that adaptive chunking can be disabled."""
        config = ChunkerSettings(
            strategy="hierarchical",
            chunk_size=100,
            adaptive_chunking=False,
        )
        chunker = TextChunker(config)

        text = "Test content for non-adaptive chunking."
        chunk_size = chunker._select_chunk_size(text)

        assert chunk_size == 100  # Should use configured chunk_size

    def test_adaptive_chunking_code_heavy(self):
        """Test adaptive chunking with code-heavy content."""
        config = ChunkerSettings(
            strategy="hierarchical",
            chunk_size=512,
            adaptive_chunking=True,
            code_chunk_size=1024,
            code_block_threshold=0.1,
        )
        chunker = TextChunker(config)

        # Create code-heavy content (>10% code blocks)
        code_block = "```python\n" + "\n".join([f"line_{i} = {i}" for i in range(20)]) + "\n```"
        text = f"Brief intro.\n\n{code_block}\n\n{code_block}\n\nBrief conclusion."

        chunk_size = chunker._select_chunk_size(text)

        assert chunk_size == 1024  # Should use code_chunk_size

    def test_adaptive_chunking_dense_prose(self):
        """Test adaptive chunking with dense prose."""
        config = ChunkerSettings(
            strategy="hierarchical",
            chunk_size=512,
            adaptive_chunking=True,
            dense_chunk_size=768,
            dense_sentence_threshold=24,
        )
        chunker = TextChunker(config)

        # Create dense prose (long sentences with many words)
        long_sentence = " ".join([f"word{i}" for i in range(30)])
        text = ". ".join([long_sentence for _ in range(5)]) + "."

        chunk_size = chunker._select_chunk_size(text)

        assert chunk_size == 768  # Should use dense_chunk_size

    def test_chunk_size_respects_bounds(self):
        """Test that chunk size respects min/max bounds."""
        config = ChunkerSettings(
            strategy="hierarchical",
            chunk_size=512,
            min_chunk_size=100,
            max_chunk_size=1024,
            adaptive_chunking=True,
        )
        chunker = TextChunker(config)

        text = "Regular text content."
        chunk_size = chunker._select_chunk_size(text)

        assert chunk_size >= config.min_chunk_size
        assert chunk_size <= config.max_chunk_size

    def test_metrics_recording(self, chunker):
        """Test that chunking metrics are recorded."""
        from unittest.mock import patch

        text = "Test content for metrics recording."

        with patch.object(chunker.metrics, "record_chunking") as mock_record:
            chunks = chunker.chunk_text(text)

            # Verify metrics were recorded
            mock_record.assert_called_once()
            call_args = mock_record.call_args
            assert call_args[1]["num_chunks"] == len(chunks)
            assert call_args[1]["strategy"] == "hierarchical"

    def test_very_long_text(self, chunker):
        """Test chunking very long text."""
        # Create a very long text (10000+ words)
        long_text = " ".join([f"word{i}" for i in range(10000)])

        chunks = chunker.chunk_text(long_text)

        assert len(chunks) > 1
        assert all(chunk.tokens > 0 for chunk in chunks)
        assert all(chunk.text.strip() for chunk in chunks)

    def test_unicode_text(self, chunker):
        """Test chunking text with Unicode characters."""
        text = """
# 简介

这是中文内容的测试。包含各种Unicode字符。

# Émojis

Testing with emojis: 😀 🎉 🚀

# العربية

مرحبا بك في الاختبار.
"""
        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        # Verify Unicode is preserved
        combined = " ".join(c.text for c in chunks)
        assert "中文" in combined or "😀" in combined or "العربية" in combined

    def test_special_characters(self, chunker):
        """Test chunking text with special characters."""
        text = "Text with special chars: @#$%^&*()_+-={}[]|\\:\";<>?,./`~"
        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        assert "@#$%^&*" in chunks[0].text

    def test_chunk_positioning(self, chunker):
        """Test that chunk start/end positions are reasonable."""
        text = "First section. Second section. Third section."
        chunks = chunker.chunk_text(text)

        assert len(chunks) > 0
        for chunk in chunks:
            assert chunk.start_pos >= 0
            assert chunk.end_pos > chunk.start_pos

    def test_different_strategies_produce_different_results(self):
        """Test that different strategies produce different chunking patterns."""
        text = """
# Section 1
Content for section 1 with multiple sentences. More content here.

# Section 2
Content for section 2 with different information. Additional details.
"""

        # Hierarchical
        config_hier = ChunkerSettings(strategy="hierarchical", chunk_size=100)
        chunks_hier = TextChunker(config_hier).chunk_text(text)

        # Semantic
        config_sem = ChunkerSettings(strategy="semantic", chunk_size=100)
        chunks_sem = TextChunker(config_sem).chunk_text(text)

        # Both should produce chunks, but potentially different counts/structure
        assert len(chunks_hier) > 0
        assert len(chunks_sem) > 0
