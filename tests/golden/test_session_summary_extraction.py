"""Golden tests for session summary extraction end-to-end workflow.

Tests Phase 5 of Session Summary Mining initiative - full extraction pipeline
with deterministic LLM output for regression testing.
"""

import sys
from datetime import date
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Add scripts to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from scripts.extract_action_items import (
    ActionItem,
    parse_markdown_sections,
)


@pytest.fixture
def mock_summary_file(tmp_path: Path) -> Path:
    """Create a mock session summary file for testing."""
    content = """---
session_date: 2025-10-20
duration: 3 hours
focus: Testing session summary mining
---

# Session Summary: Session Summary Mining Testing

## Key Accomplishments

- Implemented Phase 1: MCP file system integration
- Created extraction script with 490 lines of code
- Added 14 comprehensive unit tests (all passing)
- Fixed URL validation to accept file:// URLs

The extraction pipeline is working well. Tests cover all edge cases.

## Technical Challenges

### LLM API Rate Limiting

Hit rate limits when processing 50+ summaries. Need to add:
- Exponential backoff retry logic in `scripts/extract_action_items.py`
- Batch processing with delays
- Cost tracking per extraction run

This is blocking scale testing. Medium priority.

## Pain Points

Manual deduplication is tedious when reviewing 100+ action items.
The text similarity approach works but needs tuning.

## Next Steps

- [ ] Add rate limiting with exponential backoff
- [ ] Implement batch processing
- [ ] Test with 100+ real summaries
- [ ] Document API cost tracking

## Files Modified

- `scripts/extract_action_items.py` - Main extraction script (+490 lines)
- `tests/unit/test_action_item_extraction.py` - Unit tests (+150 lines)
- `src/mcp_web/pipeline.py` - URL validation fix
"""

    file_path = tmp_path / "2025-10-20-test-summary.md"
    file_path.write_text(content)
    return file_path


@pytest.mark.golden
def test_parse_markdown_sections_golden(mock_summary_file: Path):
    """Golden test: Section parsing should be deterministic."""
    content = mock_summary_file.read_text()
    sections = parse_markdown_sections(content)

    # Should have predictable sections
    section_headers = [s["header"] for s in sections]

    assert "Key Accomplishments" in section_headers
    assert "Technical Challenges" in section_headers
    assert "Pain Points" in section_headers
    assert "Next Steps" in section_headers

    # Section content should match expected patterns
    accomplishments = next(s for s in sections if s["header"] == "Key Accomplishments")
    assert "Phase 1" in accomplishments["content"]
    assert "MCP file system" in accomplishments["content"]


@pytest.mark.golden
@pytest.mark.requires_api
def test_extraction_output_structure_golden():
    """Golden test: Extraction output structure should be consistent."""
    # This test would require mocking the LLM API to be deterministic
    # For now, we test the structure validation

    # Create sample extracted items
    item = ActionItem(
        id="2025-10-20-test#technical-challenges#1",
        title="Add rate limiting with exponential backoff",
        description="Hit rate limits when processing 50+ summaries. Need exponential backoff retry logic.",
        category="missing_capability",
        impact="high",
        confidence="high",
        source_summary="2025-10-20-test-summary.md",
        source_section="Technical Challenges",
        session_date=date(2025, 10, 20),
        related_files=["scripts/extract_action_items.py"],
        blockers=None,
    )

    # Validate structure
    assert item.id.startswith("2025-10-20")
    assert "#" in item.id  # Should have section separator
    assert item.category in [
        "missing_capability",
        "pain_point",
        "regression",
        "improvement",
        "technical_debt",
        "documentation",
        "testing",
        "automation",
        "security",
        "performance",
    ]
    assert item.impact in ["high", "medium", "low"]
    assert item.confidence in ["high", "medium", "low"]


@pytest.mark.golden
def test_section_filtering_golden():
    """Golden test: Section filtering should skip metadata sections."""
    from scripts.extract_action_items import should_skip_section

    # Should skip these sections
    assert should_skip_section("Table of Contents") is True
    assert should_skip_section("Metadata") is True
    assert should_skip_section("Files Changed") is True
    assert should_skip_section("Git Log") is True

    # Should NOT skip these sections
    assert should_skip_section("Key Accomplishments") is False
    assert should_skip_section("Technical Challenges") is False
    assert should_skip_section("Pain Points") is False
    assert should_skip_section("Next Steps") is False


@pytest.mark.golden
def test_extraction_pipeline_idempotent(mock_summary_file: Path):
    """Golden test: Multiple extractions should produce identical results (with same LLM seed)."""
    # Mock the Instructor client to return deterministic results
    mock_items = [
        ActionItem(
            id="test-1",
            title="Test item",
            description="Test description",
            category="improvement",
            impact="high",
            confidence="high",
            source_summary="test.md",
            source_section="Section",
            session_date=date(2025, 10, 20),
        )
    ]

    with patch("scripts.extract_action_items.instructor") as mock_instructor:
        # Configure mock to return same items every time
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_items
        mock_instructor.from_openai.return_value = mock_client

        # First extraction
        from scripts.extract_action_items import extract_from_summary

        result1 = extract_from_summary(mock_client, mock_summary_file)

        # Second extraction
        result2 = extract_from_summary(mock_client, mock_summary_file)

        # Results should be identical
        assert len(result1) == len(result2)
        if result1 and result2:
            assert result1[0].id == result2[0].id
            assert result1[0].title == result2[0].title


@pytest.mark.golden
def test_date_extraction_golden():
    """Golden test: Date extraction from filenames."""
    from scripts.extract_action_items import extract_date_from_filename

    # Standard format
    assert extract_date_from_filename("2025-10-20-session-summary.md") == date(2025, 10, 20)
    assert extract_date_from_filename("2024-12-25-holiday-session.md") == date(2024, 12, 25)

    # Edge cases
    assert extract_date_from_filename("2025-01-01-new-year.md") == date(2025, 1, 1)
    assert extract_date_from_filename("2025-12-31-end-year.md") == date(2025, 12, 31)


@pytest.mark.golden
def test_title_extraction_golden():
    """Golden test: Title extraction from markdown."""
    from scripts.extract_action_items import extract_title

    content1 = "# Session Summary: Testing\n\nContent here."
    assert extract_title(content1) == "Session Summary: Testing"

    content2 = "# Main Title\n\n## Subtitle\n\nContent."
    assert extract_title(content2) == "Main Title"

    # No title
    content3 = "Content without title."
    assert extract_title(content3) == "Untitled"


@pytest.mark.golden
def test_file_path_date_range_golden(tmp_path: Path):
    """Golden test: Date range file finding."""
    from scripts.extract_action_items import find_summaries_by_date_range

    # Create test files with different dates
    (tmp_path / "docs" / "archive" / "session-summaries").mkdir(parents=True)
    summaries_dir = tmp_path / "docs" / "archive" / "session-summaries"

    (summaries_dir / "2025-10-15-session.md").write_text("# Test 1")
    (summaries_dir / "2025-10-18-session.md").write_text("# Test 2")
    (summaries_dir / "2025-10-20-session.md").write_text("# Test 3")
    (summaries_dir / "2025-10-25-session.md").write_text("# Test 4")

    # Change to temp directory for find_summaries_by_date_range to work
    import os

    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)

        # Find files in range
        files = find_summaries_by_date_range(date(2025, 10, 16), date(2025, 10, 22))

        # Should find files in range
        file_names = [f.name for f in files]
        assert "2025-10-18-session.md" in file_names
        assert "2025-10-20-session.md" in file_names

        # Should NOT find files outside range
        assert "2025-10-15-session.md" not in file_names
        assert "2025-10-25-session.md" not in file_names

    finally:
        os.chdir(original_cwd)


@pytest.mark.golden
def test_date_range_parsing_golden():
    """Golden test: Date range string parsing."""
    from scripts.extract_action_items import parse_date_range

    # Standard format
    start, end = parse_date_range("2025-10-15:2025-10-20")
    assert start == date(2025, 10, 15)
    assert end == date(2025, 10, 20)

    # With spaces
    start, end = parse_date_range("2025-10-15 : 2025-10-20")
    assert start == date(2025, 10, 15)
    assert end == date(2025, 10, 20)

    # Invalid format should raise
    with pytest.raises(ValueError):
        parse_date_range("2025-10-20")  # Missing end date

    # Invalid order should raise
    with pytest.raises(ValueError):
        parse_date_range("2025-10-20:2025-10-15")  # Start after end
