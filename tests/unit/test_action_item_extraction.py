"""Unit tests for action item extraction from session summaries.

Tests the Pydantic schemas, section parsing, and extraction logic
implemented in Phase 2 of the Session Summary Mining initiative.
"""

import sqlite3

# Import from the extraction script
import sys
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from scripts.automation.extract_action_items import (
    ActionItem,
    extract_date_from_filename,
    extract_title,
    init_database,
    log_extraction,
    parse_markdown_sections,
    should_skip_section,
)

# ============================================================================
# Schema Validation Tests
# ============================================================================


@pytest.mark.unit
def test_action_item_schema_valid():
    """Valid ActionItem passes validation."""
    item = ActionItem(
        id="2025-10-20-test#section#1",
        title="Add validation hook",
        description="Create pre-commit hook for task format validation",
        category="automation",
        impact="high",
        confidence="high",
        source_summary="2025-10-20-test.md",
        source_section="Recommendations",
        session_date=date(2025, 10, 20),
        related_files=["scripts/validate_tasks.py"],
        blockers=None,
    )

    assert item.id == "2025-10-20-test#section#1"
    assert item.category == "automation"
    assert item.impact == "high"
    assert len(item.related_files) == 1


@pytest.mark.unit
def test_action_item_schema_invalid_category():
    """Invalid category raises ValidationError."""
    with pytest.raises(ValidationError):
        ActionItem(
            id="test-1",
            title="Test item",
            description="Test description",
            category="invalid_category",  # Not in Literal list
            impact="high",
            confidence="high",
            source_summary="test.md",
            source_section="Section",
            session_date=date(2025, 10, 20),
        )


@pytest.mark.unit
def test_action_item_schema_missing_required_field():
    """Missing required field raises ValidationError."""
    with pytest.raises(ValidationError):
        ActionItem(
            id="test-1",
            title="Test item",
            # Missing description
            category="automation",
            impact="high",
            confidence="high",
            source_summary="test.md",
            source_section="Section",
            session_date=date(2025, 10, 20),
        )


@pytest.mark.unit
def test_action_item_schema_defaults():
    """Optional fields have correct defaults."""
    item = ActionItem(
        id="test-1",
        title="Test item",
        description="Test description",
        category="automation",
        impact="high",
        confidence="high",
        source_summary="test.md",
        source_section="Section",
        session_date=date(2025, 10, 20),
        # Not providing optional fields
    )

    assert item.related_files == []
    assert item.blockers is None


# ============================================================================
# Section Parsing Tests
# ============================================================================


@pytest.mark.unit
def test_parse_markdown_sections():
    """Parse markdown into sections by headers."""
    content = """# Main Title

Intro content here.

## Section 1

Content for section 1.
Multiple lines.

## Section 2

Content for section 2.

### Subsection 2.1

Subsection content.
"""

    sections = parse_markdown_sections(content)

    # Should have Introduction, Section 1, Section 2, Subsection 2.1
    assert len(sections) >= 3

    # Find section by header
    section_1 = next(s for s in sections if s["header"] == "Section 1")
    assert "Content for section 1" in section_1["content"]
    assert "Multiple lines" in section_1["content"]


@pytest.mark.unit
def test_parse_markdown_sections_empty():
    """Empty content returns empty sections list."""
    sections = parse_markdown_sections("")
    assert len(sections) <= 1  # May have empty Introduction section


@pytest.mark.unit
def test_should_skip_section():
    """Skip sections unlikely to contain action items."""
    assert should_skip_section("Table of Contents") is True
    assert should_skip_section("Metadata") is True
    assert should_skip_section("Files Changed") is True
    assert should_skip_section("Commits") is True
    assert should_skip_section("Git Log") is True

    # Should not skip valuable sections
    assert should_skip_section("Pain Points") is False
    assert should_skip_section("Recommendations") is False
    assert should_skip_section("Next Steps") is False


# ============================================================================
# Metadata Extraction Tests
# ============================================================================


@pytest.mark.unit
def test_extract_date_from_filename():
    """Extract date from session summary filename."""
    filename = "2025-10-20-daily-summary.md"
    extracted_date = extract_date_from_filename(filename)

    assert extracted_date == date(2025, 10, 20)


@pytest.mark.unit
def test_extract_date_from_filename_invalid():
    """Invalid filename returns today's date."""
    filename = "invalid-filename.md"
    extracted_date = extract_date_from_filename(filename)

    # Should return today as fallback
    assert extracted_date == date.today()


@pytest.mark.unit
def test_extract_title():
    """Extract title from markdown first heading."""
    content = """# Session Summary: Testing Improvements

Content here.
"""

    title = extract_title(content)
    assert title == "Session Summary: Testing Improvements"


@pytest.mark.unit
def test_extract_title_no_heading():
    """No heading returns 'Untitled'."""
    content = "Just some content without heading."

    title = extract_title(content)
    assert title == "Untitled"


# ============================================================================
# Database Logging Tests
# ============================================================================


@pytest.mark.unit
def test_init_database(tmp_path):
    """Initialize SQLite database creates correct schema."""
    db_path = tmp_path / "test_extractions.db"

    init_database(db_path)

    # Verify table exists
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='extractions'")
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == "extractions"

    conn.close()


@pytest.mark.unit
def test_log_extraction(tmp_path):
    """Log action items to database."""
    db_path = tmp_path / "test_extractions.db"
    init_database(db_path)

    items = [
        ActionItem(
            id="2025-10-20-test#section#1",
            title="Test item 1",
            description="Description 1",
            category="automation",
            impact="high",
            confidence="high",
            source_summary="test.md",
            source_section="Section 1",
            session_date=date(2025, 10, 20),
            related_files=["file1.py", "file2.py"],
            blockers=["dependency-1"],
        ),
        ActionItem(
            id="2025-10-20-test#section#2",
            title="Test item 2",
            description="Description 2",
            category="testing",
            impact="medium",
            confidence="medium",
            source_summary="test.md",
            source_section="Section 2",
            session_date=date(2025, 10, 20),
        ),
    ]

    log_extraction(db_path, items)

    # Verify logged items
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM extractions")
    count = cursor.fetchone()[0]

    assert count == 2

    # Verify first item details
    cursor.execute("SELECT * FROM extractions WHERE id = ?", ("2025-10-20-test#section#1",))
    row = cursor.fetchone()

    assert row[5] == "Test item 1"  # title
    assert row[6] == "automation"  # category
    assert row[7] == "high"  # impact
    assert row[10] == "file1.py,file2.py"  # related_files
    assert row[11] == "dependency-1"  # blockers

    conn.close()


@pytest.mark.unit
def test_log_extraction_replace_existing(tmp_path):
    """Re-logging same ID replaces existing entry."""
    db_path = tmp_path / "test_extractions.db"
    init_database(db_path)

    # Log initial item
    item_v1 = ActionItem(
        id="2025-10-20-test#section#1",
        title="Original title",
        description="Original description",
        category="automation",
        impact="low",
        confidence="low",
        source_summary="test.md",
        source_section="Section",
        session_date=date(2025, 10, 20),
    )
    log_extraction(db_path, [item_v1])

    # Update same ID
    item_v2 = ActionItem(
        id="2025-10-20-test#section#1",
        title="Updated title",
        description="Updated description",
        category="automation",
        impact="high",  # Changed
        confidence="high",  # Changed
        source_summary="test.md",
        source_section="Section",
        session_date=date(2025, 10, 20),
    )
    log_extraction(db_path, [item_v2])

    # Verify only one entry exists with updated values
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM extractions")
    count = cursor.fetchone()[0]
    assert count == 1

    cursor.execute(
        "SELECT title, impact FROM extractions WHERE id = ?", ("2025-10-20-test#section#1",)
    )
    row = cursor.fetchone()
    assert row[0] == "Updated title"
    assert row[1] == "high"

    conn.close()


# ============================================================================
# Integration Tests (Mocked LLM)
# ============================================================================


@pytest.mark.unit
def test_extract_from_section_mock():
    """Test extraction from section with mocked LLM client."""
    # This test would require mocking the instructor client
    # Skipping for now as it's more of an integration test
    pytest.skip("Requires mocked Instructor client - defer to integration tests")
