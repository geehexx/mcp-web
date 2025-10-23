"""Unit tests for initiative mapping (Phase 4 of Session Summary Mining).

Tests the initiative metadata loading, file-based mapping algorithm,
and auto-creation heuristics implemented in Phase 4.
"""

from datetime import date
from pathlib import Path

import pytest
from scripts.automation.extract_action_items import (
    ActionItem,
    load_initiative_metadata,
    map_action_item_to_initiatives,
    should_create_new_initiative,
)

# ============================================================================
# Initiative Metadata Loading Tests
# ============================================================================


@pytest.mark.unit
def test_load_initiative_metadata_valid_initiative(tmp_path: Path):
    """Load metadata from valid initiative markdown file."""
    # Create test initiative file
    initiative_content = """---
Status: Active
Created: 2025-10-19
---

# Initiative: Test Initiative

## Objective

Test objective here.

## Tasks

- [x] Task 1 in `src/module.py`
- [ ] Task 2 in `tests/test_module.py`

## Files

- `src/fetcher.py` - Main implementation
- `src/config.py` - Configuration
- `tests/test_fetcher.py` - Tests
"""

    initiative_file = tmp_path / "test-initiative.md"
    initiative_file.write_text(initiative_content)

    # Load metadata
    metadata = load_initiative_metadata(tmp_path)

    assert len(metadata) == 1
    assert metadata[0]["title"] == "Initiative: Test Initiative"
    assert metadata[0]["status"] == "Active"
    assert "src/module.py" in metadata[0]["related_files"]
    assert "tests/test_module.py" in metadata[0]["related_files"]
    assert "src/fetcher.py" in metadata[0]["related_files"]


@pytest.mark.unit
def test_load_initiative_metadata_multiple_initiatives(tmp_path: Path):
    """Load metadata from multiple initiative files."""
    # Create two initiative files
    init1 = tmp_path / "initiative-1.md"
    init1.write_text("""# Initiative: First Initiative

Status: Active

Files: `src/module1.py`
""")

    init2 = tmp_path / "initiative-2.md"
    init2.write_text("""# Initiative: Second Initiative

Status: Completed

Files: `src/module2.py`, `tests/test_module2.py`
""")

    # Load metadata
    metadata = load_initiative_metadata(tmp_path)

    assert len(metadata) == 2
    titles = {m["title"] for m in metadata}
    assert "Initiative: First Initiative" in titles
    assert "Initiative: Second Initiative" in titles


@pytest.mark.unit
def test_load_initiative_metadata_empty_directory(tmp_path: Path):
    """Handle empty directory gracefully."""
    metadata = load_initiative_metadata(tmp_path)
    assert metadata == []


@pytest.mark.unit
def test_load_initiative_metadata_nonexistent_directory():
    """Handle nonexistent directory gracefully."""
    nonexistent_dir = Path("/tmp/nonexistent-directory-12345")
    metadata = load_initiative_metadata(nonexistent_dir)
    assert metadata == []


@pytest.mark.unit
def test_load_initiative_metadata_no_python_files(tmp_path: Path):
    """Handle initiative with no Python files mentioned."""
    initiative_file = tmp_path / "docs-only-initiative.md"
    initiative_file.write_text("""# Initiative: Documentation Only

Status: Active

## Tasks

- [ ] Update docs/README.md
- [ ] Write guides/tutorial.md
""")

    metadata = load_initiative_metadata(tmp_path)

    assert len(metadata) == 1
    assert metadata[0]["related_files"] == []


@pytest.mark.unit
def test_load_initiative_metadata_file_limit(tmp_path: Path):
    """Metadata loader limits to 10 files per initiative."""
    # Create initiative with 15 file references
    files = "\n".join([f"- [ ] File in `src/file{i}.py`" for i in range(15)])
    initiative_content = f"""# Initiative: Many Files

Status: Active

## Tasks

{files}
"""

    initiative_file = tmp_path / "many-files-initiative.md"
    initiative_file.write_text(initiative_content)

    metadata = load_initiative_metadata(tmp_path)

    assert len(metadata) == 1
    # Should limit to 10 files
    assert len(metadata[0]["related_files"]) <= 10


# ============================================================================
# Initiative Mapping Tests
# ============================================================================


@pytest.mark.unit
def test_map_action_item_high_overlap():
    """Map action item to initiative with high file overlap."""
    item = ActionItem(
        id="test-1",
        title="Fix caching bug",
        description="Cache not invalidating correctly",
        category="regression",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Bugs",
        session_date=date(2025, 10, 20),
        related_files=["src/cache.py", "tests/test_cache.py"],
    )

    initiatives = [
        {
            "title": "Caching System Overhaul",
            "status": "Active",
            "path": "/path/to/caching-initiative.md",
            "related_files": ["src/cache.py", "tests/test_cache.py", "src/config.py"],
        },
        {
            "title": "Security Improvements",
            "status": "Active",
            "path": "/path/to/security-initiative.md",
            "related_files": ["src/auth.py", "src/security.py"],
        },
    ]

    matches = map_action_item_to_initiatives(item, initiatives)

    # Should match caching initiative with high overlap
    assert len(matches) >= 1
    assert matches[0]["title"] == "Caching System Overhaul"
    # Overlap: 2 files in common out of 3 total = 2/3 = 0.67
    assert matches[0]["overlap_score"] > 0.6


@pytest.mark.unit
def test_map_action_item_no_overlap():
    """Map action item with no file overlap to initiatives."""
    item = ActionItem(
        id="test-1",
        title="Add new feature",
        description="Implement new API endpoint",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Features",
        session_date=date(2025, 10, 20),
        related_files=["src/new_module.py"],
    )

    initiatives = [
        {
            "title": "Caching System",
            "status": "Active",
            "path": "/path/to/caching.md",
            "related_files": ["src/cache.py", "tests/test_cache.py"],
        }
    ]

    matches = map_action_item_to_initiatives(item, initiatives)

    # No overlap - should return empty list
    assert matches == []


@pytest.mark.unit
def test_map_action_item_no_related_files():
    """Map action item with no related files mentioned."""
    item = ActionItem(
        id="test-1",
        title="Improve documentation",
        description="Add more examples to docs",
        category="documentation",
        impact="medium",
        confidence="high",
        source_summary="summary.md",
        source_section="Docs",
        session_date=date(2025, 10, 20),
        related_files=[],
    )

    initiatives = [
        {
            "title": "Documentation Initiative",
            "status": "Active",
            "path": "/path/to/docs.md",
            "related_files": ["docs/guide.md", "docs/api.md"],
        }
    ]

    matches = map_action_item_to_initiatives(item, initiatives)

    # No files in item - cannot match
    assert matches == []


@pytest.mark.unit
def test_map_action_item_initiative_no_files():
    """Map action item to initiative with no files listed."""
    item = ActionItem(
        id="test-1",
        title="Fix bug",
        description="Bug in module",
        category="regression",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Bugs",
        session_date=date(2025, 10, 20),
        related_files=["src/module.py"],
    )

    initiatives = [
        {
            "title": "Bug Fixes",
            "status": "Active",
            "path": "/path/to/bugs.md",
            "related_files": [],  # No files listed
        }
    ]

    matches = map_action_item_to_initiatives(item, initiatives)

    # Initiative has no files - cannot match
    assert matches == []


@pytest.mark.unit
def test_map_action_item_multiple_matches_sorted():
    """Map action item to multiple initiatives, sorted by overlap."""
    item = ActionItem(
        id="test-1",
        title="Improve performance",
        description="Optimize database queries",
        category="performance",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Performance",
        session_date=date(2025, 10, 20),
        related_files=["src/database.py", "src/query.py"],
    )

    initiatives = [
        {
            "title": "Database Optimization",
            "status": "Active",
            "path": "/path/to/db.md",
            "related_files": ["src/database.py", "src/query.py", "tests/test_db.py"],
        },
        {
            "title": "General Performance",
            "status": "Active",
            "path": "/path/to/perf.md",
            "related_files": ["src/database.py", "src/cache.py", "src/config.py"],
        },
    ]

    matches = map_action_item_to_initiatives(item, initiatives)

    # Should return both matches, sorted by overlap score
    assert len(matches) == 2
    # First match should have higher overlap
    assert matches[0]["overlap_score"] >= matches[1]["overlap_score"]
    # Database Optimization has 2/3 = 0.67, General Performance has 1/4 = 0.25
    assert matches[0]["title"] == "Database Optimization"


@pytest.mark.unit
def test_map_action_item_partial_file_path_match():
    """Test that file paths must match exactly (not partial matches)."""
    item = ActionItem(
        id="test-1",
        title="Fix bug",
        description="Bug in cache module",
        category="regression",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Bugs",
        session_date=date(2025, 10, 20),
        related_files=["src/cache.py"],
    )

    initiatives = [
        {
            "title": "Cache Initiative",
            "status": "Active",
            "path": "/path/to/cache.md",
            "related_files": ["src/cache_utils.py"],  # Different file
        }
    ]

    matches = map_action_item_to_initiatives(item, initiatives)

    # Paths don't match exactly - no overlap
    assert matches == []


# ============================================================================
# Auto-Creation Heuristic Tests
# ============================================================================


@pytest.mark.unit
def test_should_create_new_initiative_high_impact_high_confidence():
    """High impact + high confidence + no match → should create."""
    item = ActionItem(
        id="test-1",
        title="Critical missing feature",
        description="Feature X is missing and blocking progress",
        category="missing_capability",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Missing",
        session_date=date(2025, 10, 20),
    )

    # No existing match (score < 0.3)
    assert should_create_new_initiative(item, best_match_score=0.0) is True
    assert should_create_new_initiative(item, best_match_score=0.2) is True
    assert should_create_new_initiative(item, best_match_score=0.29) is True


@pytest.mark.unit
def test_should_create_new_initiative_with_good_match():
    """High impact + high confidence + good match → should NOT create."""
    item = ActionItem(
        id="test-1",
        title="Enhancement",
        description="Improve existing feature",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Improvements",
        session_date=date(2025, 10, 20),
    )

    # Good existing match (score >= 0.3)
    assert should_create_new_initiative(item, best_match_score=0.3) is False
    assert should_create_new_initiative(item, best_match_score=0.5) is False
    assert should_create_new_initiative(item, best_match_score=0.8) is False


@pytest.mark.unit
def test_should_create_new_initiative_medium_impact():
    """Medium impact → should NOT create (regardless of confidence)."""
    item = ActionItem(
        id="test-1",
        title="Nice to have",
        description="Would be nice to have this feature",
        category="improvement",
        impact="medium",  # Not high
        confidence="high",
        source_summary="summary.md",
        source_section="Improvements",
        session_date=date(2025, 10, 20),
    )

    # Medium impact - should not create
    assert should_create_new_initiative(item, best_match_score=0.0) is False


@pytest.mark.unit
def test_should_create_new_initiative_medium_confidence():
    """Medium confidence → should NOT create (even if high impact)."""
    item = ActionItem(
        id="test-1",
        title="Possible issue",
        description="Might be an issue, not sure",
        category="pain_point",
        impact="high",
        confidence="medium",  # Not high
        source_summary="summary.md",
        source_section="Issues",
        session_date=date(2025, 10, 20),
    )

    # Medium confidence - should not create
    assert should_create_new_initiative(item, best_match_score=0.0) is False


@pytest.mark.unit
def test_should_create_new_initiative_low_impact_low_confidence():
    """Low impact + low confidence → should NOT create."""
    item = ActionItem(
        id="test-1",
        title="Minor thing",
        description="Small thing to consider",
        category="improvement",
        impact="low",
        confidence="low",
        source_summary="summary.md",
        source_section="Notes",
        session_date=date(2025, 10, 20),
    )

    assert should_create_new_initiative(item, best_match_score=0.0) is False


@pytest.mark.unit
def test_should_create_new_initiative_edge_case_exact_threshold():
    """Test exact threshold boundary (0.3)."""
    item = ActionItem(
        id="test-1",
        title="Feature",
        description="New feature needed",
        category="missing_capability",
        impact="high",
        confidence="high",
        source_summary="summary.md",
        source_section="Features",
        session_date=date(2025, 10, 20),
    )

    # Exact threshold - should NOT create (>= 0.3)
    assert should_create_new_initiative(item, best_match_score=0.3) is False

    # Just below threshold - should create (< 0.3)
    assert should_create_new_initiative(item, best_match_score=0.299) is True
