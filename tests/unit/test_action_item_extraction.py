"""Unit tests for action item extraction from session summaries.

Tests the Pydantic schemas, section parsing, and extraction logic
implemented in Phase 2 of the Session Summary Mining initiative.
"""

import sqlite3
import sys
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from scripts.automation.extract_action_items import (
    ActionItem,
    deduplicate_items,
    export_borderline_cases,
    extract_date_from_filename,
    extract_from_section,
    extract_from_summary,
    extract_title,
    init_database,
    load_initiative_metadata,
    log_extraction,
    map_action_item_to_initiatives,
    parse_markdown_sections,
    should_create_new_initiative,
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


# ============================================================================
# Additional Utility Function Tests
# ============================================================================


@pytest.mark.unit
def test_parse_markdown_sections_nested_headers():
    """Parse markdown with nested headers correctly."""
    content = """# Main

## Section 1
Content 1

### Subsection 1.1
Nested content

### Subsection 1.2
More nested

## Section 2
Content 2
"""
    sections = parse_markdown_sections(content)

    # Should parse all sections
    assert len(sections) >= 4
    headers = [s["header"] for s in sections]
    assert "Section 1" in headers
    assert "Section 2" in headers


@pytest.mark.unit
def test_should_skip_section_case_insensitive():
    """Skip section check is case-insensitive."""
    assert should_skip_section("TABLE OF CONTENTS") is True
    assert should_skip_section("table of contents") is True
    assert should_skip_section("Table Of Contents") is True


@pytest.mark.unit
def test_extract_date_with_full_path():
    """Extract date from full file path."""
    # Function extracts from filename component, not full path
    path = "2025-10-15-important-session.md"
    extracted = extract_date_from_filename(path)
    assert extracted == date(2025, 10, 15)


@pytest.mark.unit
def test_extract_title_with_markdown_formatting():
    """Extract title strips markdown formatting."""
    content = "# **Bold Title** with _emphasis_\n\nContent."
    title = extract_title(content)
    assert "Bold Title" in title


@pytest.mark.unit
def test_init_database_idempotent(tmp_path):
    """Initialize database multiple times is safe."""
    db_path = tmp_path / "test.db"

    # Initialize twice
    init_database(db_path)
    init_database(db_path)

    # Should still work
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM extractions")
    count = cursor.fetchone()[0]
    assert count == 0  # No data yet
    conn.close()


@pytest.mark.unit
def test_log_extraction_empty_list(tmp_path):
    """Log empty extraction list."""
    db_path = tmp_path / "test.db"
    init_database(db_path)

    # Log empty list
    log_extraction(db_path, [])

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM extractions")
    count = cursor.fetchone()[0]
    assert count == 0
    conn.close()


@pytest.mark.unit
def test_action_item_with_no_blockers():
    """Action item with no blockers stores None."""
    item = ActionItem(
        id="test-1",
        title="Test",
        description="Description",
        category="automation",
        impact="medium",
        confidence="high",
        source_summary="test.md",
        source_section="Section",
        session_date=date(2025, 10, 20),
        blockers=None,
    )
    assert item.blockers is None


@pytest.mark.unit
def test_action_item_with_empty_related_files():
    """Action item defaults to empty related_files list."""
    item = ActionItem(
        id="test-1",
        title="Test",
        description="Description",
        category="testing",
        impact="low",
        confidence="medium",
        source_summary="test.md",
        source_section="Section",
        session_date=date(2025, 10, 20),
    )
    assert item.related_files == []
    assert isinstance(item.related_files, list)


@pytest.mark.unit
def test_extract_from_section_populates_missing_metadata():
    """Extraction populates metadata when response omits fields."""

    class FakeCompletions:
        def __init__(self, items):
            self._items = items

        def create(self, **kwargs):
            return self._items

    class FakeChat:
        def __init__(self, items):
            self.completions = FakeCompletions(items)

    class FakeClient:
        def __init__(self, items):
            self.chat = FakeChat(items)

    metadata = {
        "filename": "2025-10-22-summary.md",
        "date": date(2025, 10, 22),
        "title": "Session Summary",
    }
    section = {"header": "Findings", "content": "Relevant findings content." * 5}
    items = [
        ActionItem.model_construct(  # type: ignore[attr-defined]
            id="",
            title="Address coverage gaps",
            description="Improve validation coverage for scripts.",
            category="testing",
            impact="high",
            confidence="medium",
            source_summary="",
            source_section="",
            session_date=None,
            related_files=[],
            blockers=None,
        )
    ]

    client = FakeClient(items)
    result = extract_from_section(client, section, metadata)

    assert result[0].source_summary == "2025-10-22-summary.md"
    assert result[0].source_section == "Findings"
    assert result[0].session_date == date(2025, 10, 22)
    assert result[0].id.startswith("2025-10-22-2025-10-22-summary")


@pytest.mark.unit
def test_extract_from_summary_skips_short_sections(monkeypatch, tmp_path):
    """Summary extraction skips short or ignorable sections."""

    summary_path = tmp_path / "2025-10-22-summary.md"
    content = """# Session Summary

## Table of Contents
Short

## Action Items
This section contains actionable insights with sufficient detail for extraction purposes.
"""
    summary_path.write_text(content, encoding="utf-8")

    captured_headers = []

    def fake_extract(client, section, metadata):
        captured_headers.append(section["header"])
        return [
            ActionItem(
                id="2025-10-22-summary#action-items#1",
                title="Increase coverage",
                description="Add missing tests.",
                category="testing",
                impact="high",
                confidence="high",
                source_summary=metadata["filename"],
                source_section=section["header"],
                session_date=metadata["date"],
                related_files=["scripts/automation/extract_action_items.py"],
                blockers=None,
            )
        ]

    monkeypatch.setattr(
        "scripts.automation.extract_action_items.extract_from_section",
        fake_extract,
    )

    class DummyClient:
        pass

    items = extract_from_summary(DummyClient(), summary_path)

    assert len(items) == 1
    assert captured_headers == ["Action Items"]


@pytest.mark.unit
def test_deduplicate_items_merges_high_similarity():
    """High similarity items are merged during deduplication."""

    base = {
        "title": "Enforce validation",
        "description": "Ensure initiative validation covers dependency checks.",
        "category": "testing",
        "impact": "high",
        "confidence": "high",
        "source_summary": "summary.md",
        "source_section": "Actions",
        "session_date": date(2025, 10, 22),
        "related_files": ["scripts/validation/validate_initiatives.py"],
        "blockers": None,
    }
    items = [
        ActionItem(id="item-1", **base),
        ActionItem(id="item-2", **base),
    ]

    deduplicated, borderline = deduplicate_items(items, return_borderline=True)

    assert len(deduplicated) == 1
    assert borderline == []


@pytest.mark.unit
def test_deduplicate_items_returns_borderline_pairs():
    """Borderline contextual similarity is surfaced for review."""

    item_a = ActionItem(
        id="item-a",
        title="Expand coverage",
        description="Add tests for summary extraction.",
        category="testing",
        impact="high",
        confidence="medium",
        source_summary="summary.md",
        source_section="Next Steps",
        session_date=date(2025, 10, 22),
        related_files=[
            "scripts/automation/extract_action_items.py",
            "tests/unit/test_action_item_extraction.py",
        ],
        blockers=None,
    )
    item_b = ActionItem(
        id="item-b",
        title="Refine coverage",
        description="Improve validation suite structure.",
        category="testing",
        impact="high",
        confidence="medium",
        source_summary="summary.md",
        source_section="Action Items",
        session_date=date(2025, 10, 22),
        related_files=[
            "scripts/automation/extract_action_items.py",
            "tests/scripts/test_validate_workflows.py",
        ],
        blockers=None,
    )

    deduplicated, borderline = deduplicate_items([item_a, item_b], return_borderline=True)

    assert len(deduplicated) == 2
    assert len(borderline) == 1
    assert borderline[0]["level"] == "contextual"


@pytest.mark.unit
def test_export_borderline_cases(tmp_path):
    """Borderline cases are exported to YAML for review."""

    output_path = tmp_path / "borderline.yaml"
    item = ActionItem(
        id="item-1",
        title="Improve docs",
        description="Document validation workflow.",
        category="documentation",
        impact="medium",
        confidence="medium",
        source_summary="summary.md",
        source_section="Docs",
        session_date=date(2025, 10, 22),
        related_files=["docs/initiatives/active/initiative.md"],
        blockers=None,
    )
    pair = {
        "item1": item,
        "item2": item,
        "similarity": 0.65,
        "level": "contextual",
    }

    export_borderline_cases([pair], output_path)

    content = output_path.read_text(encoding="utf-8")

    assert "review_required" in content
    assert "item-1" in content


@pytest.mark.unit
def test_should_create_new_initiative_heuristic():
    """Heuristic requests new initiative for impactful unmatched items."""

    item = ActionItem(
        id="item-1",
        title="Critical blocker",
        description="Address missing initiative.",
        category="automation",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Blockers",
        session_date=date(2025, 10, 22),
        related_files=[],
        blockers=None,
    )

    assert should_create_new_initiative(item, best_match_score=0.1) is True
    assert should_create_new_initiative(item, best_match_score=0.5) is False


@pytest.mark.unit
def test_load_initiative_metadata(tmp_path):
    """Initiative metadata loader extracts title, status, and related files."""

    initiative_dir = tmp_path / "active"
    initiative_dir.mkdir()
    initiative_path = initiative_dir / "testing-excellence.md"
    initiative_path.write_text(
        """# Testing Excellence Initiative\n\nStatus: Active\n\nFocus on scripts like `scripts/automation/extract_action_items.py`.\n""",
        encoding="utf-8",
    )

    metadata = load_initiative_metadata(initiative_dir)

    assert len(metadata) == 1
    entry = metadata[0]
    assert entry["title"] == "Testing Excellence Initiative"
    assert entry["status"] == "Active"
    assert "scripts/automation/extract_action_items.py" in entry["related_files"]


@pytest.mark.unit
def test_map_action_item_to_initiatives(tmp_path):
    """Action items map to initiatives using overlapping related files."""

    initiative_dir = tmp_path / "active"
    initiative_dir.mkdir()
    (initiative_dir / "initiative-a.md").write_text(
        """# Initiative A\n\nStatus: Active\n\nReferences `scripts/automation/extract_action_items.py`.\n""",
        encoding="utf-8",
    )
    initiatives = load_initiative_metadata(initiative_dir)

    item = ActionItem(
        id="item-initiative",
        title="Align action",
        description="Ensure scripts initiatives align.",
        category="testing",
        impact="medium",
        confidence="medium",
        source_summary="summary.md",
        source_section="Initiatives",
        session_date=date(2025, 10, 22),
        related_files=["scripts/automation/extract_action_items.py"],
        blockers=None,
    )

    matches = map_action_item_to_initiatives(item, initiatives)

    assert len(matches) == 1
    assert matches[0]["title"] == "Initiative A"
    assert matches[0]["overlap_score"] == 1.0
