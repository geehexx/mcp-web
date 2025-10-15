"""Benchmark-specific fixtures and configuration.

This conftest provides mock LLM responses to make benchmarks:
- Deterministic (no API variability)
- Fast (no network calls)
- Cost-free (no API charges)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for benchmarks.
    
    Returns deterministic responses without making actual API calls.
    """
    with patch("openai.AsyncOpenAI") as mock_class:
        mock_client = AsyncMock()
        
        # Mock streaming response
        async def mock_stream_generator():
            """Generate mock streaming chunks."""
            chunks = [
                "This ",
                "is ",
                "a ",
                "concise ",
                "test ",
                "summary ",
                "of ",
                "the ",
                "content. ",
                "It ",
                "captures ",
                "the ",
                "key ",
                "points ",
                "efficiently.",
            ]
            for chunk_text in chunks:
                chunk = MagicMock()
                chunk.choices = [MagicMock()]
                chunk.choices[0].delta = MagicMock()
                chunk.choices[0].delta.content = chunk_text
                chunk.choices[0].finish_reason = None
                yield chunk
            
            # Final chunk with finish_reason
            final_chunk = MagicMock()
            final_chunk.choices = [MagicMock()]
            final_chunk.choices[0].delta = MagicMock()
            final_chunk.choices[0].delta.content = None
            final_chunk.choices[0].finish_reason = "stop"
            yield final_chunk
        
        # Mock non-streaming response
        def mock_non_stream_response():
            """Generate mock non-streaming response."""
            response = MagicMock()
            response.choices = [MagicMock()]
            response.choices[0].message = MagicMock()
            response.choices[0].message.content = (
                "This is a concise test summary of the content. "
                "It captures the key points efficiently."
            )
            response.usage = MagicMock()
            response.usage.prompt_tokens = 100
            response.usage.completion_tokens = 50
            response.usage.total_tokens = 150
            return response
        
        # Configure mock to return appropriate response based on stream parameter
        async def create_completion(**kwargs):
            if kwargs.get("stream", False):
                return mock_stream_generator()
            else:
                return mock_non_stream_response()
        
        mock_client.chat.completions.create = create_completion
        mock_class.return_value = mock_client
        
        yield mock_client


@pytest.fixture
def mock_summarizer(test_config, mock_openai_client):
    """Summarizer with mocked LLM for benchmarks.
    
    Uses the mock OpenAI client to avoid real API calls.
    """
    from mcp_web.summarizer import Summarizer
    
    return Summarizer(test_config.summarizer)


@pytest.fixture
def sample_chunks():
    """Sample text chunks for benchmarking summarization.
    
    Returns a realistic set of chunks similar to what would be
    generated from a typical web page.
    """
    from mcp_web.chunker import Chunk
    
    chunks = []
    for i in range(5):
        chunk = Chunk(
            text=f"Section {i+1}: " + "This is sample content. " * 50,
            tokens=100,
            start_pos=i * 100,
            end_pos=(i + 1) * 100,
            metadata={"section": i + 1},
        )
        chunks.append(chunk)
    
    return chunks


@pytest.fixture
def large_chunks():
    """Larger set of chunks for testing parallel map-reduce.
    
    Simulates a long document that would benefit from parallel processing.
    """
    from mcp_web.chunker import Chunk
    
    chunks = []
    for i in range(20):
        chunk = Chunk(
            text=f"Chunk {i+1}: " + "Content paragraph. " * 40,
            tokens=150,
            start_pos=i * 150,
            end_pos=(i + 1) * 150,
            metadata={"chunk_id": i + 1},
        )
        chunks.append(chunk)
    
    return chunks
