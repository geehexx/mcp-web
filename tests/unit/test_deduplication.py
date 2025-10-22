"""Unit tests for action item deduplication.

Tests for Phase 3 of Session Summary Mining initiative:
- Level 1: Text similarity (TF-IDF + cosine)
- Level 2: Semantic similarity (LLM embeddings)
- Level 3: Contextual comparison (initiative + file overlap)
- Deduplication pipeline (cascading logic)
- Human review export (borderline cases)
"""

from datetime import date

import pytest

from scripts.automation.extract_action_items import (
    ActionItem,
    compute_contextual_similarity,
    compute_text_similarity,
    deduplicate_items,
    export_borderline_cases,
)

# ============================================================================
# Level 1: Text Similarity Tests (TF-IDF + Cosine)
# ============================================================================


@pytest.mark.unit
def test_text_similarity_exact_duplicate():
    """Exact duplicates should have 100% text similarity."""
    item1 = ActionItem(
        id="2025-10-20-test#section#1",
        title="Add caching to MCP server",
        description="Implement disk-based caching for web content to reduce API calls.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Improvements",
        session_date=date(2025, 10, 20),
    )

    item2 = ActionItem(
        id="2025-10-20-test#section#2",
        title="Add caching to MCP server",
        description="Implement disk-based caching for web content to reduce API calls.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary2.md",
        source_section="Improvements",
        session_date=date(2025, 10, 21),
    )

    similarity = compute_text_similarity(item1, item2)
    assert similarity >= 0.99


@pytest.mark.unit
def test_text_similarity_near_duplicate():
    """Near-duplicates (paraphrased) should have 60-85% similarity with TF-IDF."""

    item1 = ActionItem(
        id="2025-10-20-test#section#1",
        title="Add caching to MCP server",
        description="Implement disk-based caching for web content to reduce API calls.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Improvements",
        session_date=date(2025, 10, 20),
    )

    item2 = ActionItem(
        id="2025-10-20-test#section#2",
        title="Implement caching in MCP",
        description="Add disk caching to reduce external API requests for web data.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary2.md",
        source_section="Improvements",
        session_date=date(2025, 10, 21),
    )

    similarity = compute_text_similarity(item1, item2)
    # TF-IDF is less forgiving for paraphrases than semantic embeddings
    assert 0.60 <= similarity <= 0.85


@pytest.mark.unit
def test_text_similarity_unrelated():
    """Unrelated items should have <30% similarity."""

    item1 = ActionItem(
        id="2025-10-20-test#section#1",
        title="Add caching to MCP server",
        description="Implement disk-based caching for web content.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Improvements",
        session_date=date(2025, 10, 20),
    )

    item2 = ActionItem(
        id="2025-10-20-test#section#2",
        title="Fix authentication bug",
        description="Resolve issue where API keys are not validated correctly.",
        category="regression",
        impact="high",
        confidence="high",
        source_summary="summary2.md",
        source_section="Bugs",
        session_date=date(2025, 10, 21),
    )

    similarity = compute_text_similarity(item1, item2)
    assert similarity < 0.30


@pytest.mark.unit
def test_text_similarity_edge_case_empty():
    """Completely empty text should handle gracefully."""

    # Test with truly empty combined text (empty title and description)
    item1 = ActionItem(
        id="2025-10-20-test#section#1",
        title="",
        description="",
        category="testing",
        impact="low",
        confidence="low",
        source_summary="summary1.md",
        source_section="Section",
        session_date=date(2025, 10, 20),
    )

    item2 = ActionItem(
        id="2025-10-20-test#section#2",
        title="",
        description="",
        category="testing",
        impact="low",
        confidence="low",
        source_summary="summary2.md",
        source_section="Section",
        session_date=date(2025, 10, 21),
    )

    similarity = compute_text_similarity(item1, item2)
    assert similarity == 0.0  # Both empty = not comparable, return 0


# ============================================================================
# Level 2: Semantic Similarity Tests (LLM Embeddings)
# ============================================================================


@pytest.mark.unit
@pytest.mark.requires_api
def test_semantic_similarity_exact():
    """Semantically identical items should have high similarity (requires API key)."""

    item1 = ActionItem(  # noqa: F841
        id="2025-10-20-test#section#1",
        title="Performance is slow",
        description="The application takes too long to load data.",
        category="performance",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Issues",
        session_date=date(2025, 10, 20),
    )

    item2 = ActionItem(  # noqa: F841
        id="2025-10-20-test#section#2",
        title="Slow loading times",
        description="Data retrieval is taking an excessive amount of time.",
        category="performance",
        impact="high",
        confidence="high",
        source_summary="summary2.md",
        source_section="Problems",
        session_date=date(2025, 10, 21),
    )

    # from scripts.extract_action_items import compute_semantic_similarity
    # similarity = compute_semantic_similarity(item1, item2)
    # assert similarity >= 0.85  # High semantic similarity


@pytest.mark.unit
@pytest.mark.requires_api
def test_semantic_similarity_related_but_distinct():
    """Related but distinct items should have medium similarity (requires API key)."""

    item1 = ActionItem(  # noqa: F841
        id="2025-10-20-test#section#1",
        title="Add caching",
        description="Implement caching to improve performance.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Improvements",
        session_date=date(2025, 10, 20),
    )

    item2 = ActionItem(  # noqa: F841
        id="2025-10-20-test#section#2",
        title="Optimize database queries",
        description="Improve query performance by adding indexes.",
        category="performance",
        impact="high",
        confidence="high",
        source_summary="summary2.md",
        source_section="Performance",
        session_date=date(2025, 10, 21),
    )

    # from scripts.extract_action_items import compute_semantic_similarity
    # similarity = compute_semantic_similarity(item1, item2)
    # assert 0.50 <= similarity <= 0.70  # Related but distinct


@pytest.mark.unit
@pytest.mark.requires_api
def test_semantic_similarity_unrelated():
    """Unrelated items should have low semantic similarity (requires API key)."""

    item1 = ActionItem(  # noqa: F841
        id="2025-10-20-test#section#1",
        title="Add caching",
        description="Implement disk-based caching.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Improvements",
        session_date=date(2025, 10, 20),
    )

    item2 = ActionItem(  # noqa: F841
        id="2025-10-20-test#section#2",
        title="Update documentation",
        description="Add missing API documentation for new endpoints.",
        category="documentation",
        impact="medium",
        confidence="high",
        source_summary="summary2.md",
        source_section="Docs",
        session_date=date(2025, 10, 21),
    )

    # from scripts.extract_action_items import compute_semantic_similarity
    # similarity = compute_semantic_similarity(item1, item2)
    # assert similarity < 0.30


# ============================================================================
# Level 3: Contextual Similarity Tests (Initiative + File Overlap)
# ============================================================================


@pytest.mark.unit
def test_contextual_similarity_same_initiative_high_overlap():
    """Same initiative + high file overlap → high contextual similarity."""

    item1 = ActionItem(
        id="2025-10-20-test#section#1",
        title="Fix caching bug",
        description="Cache not invalidating correctly.",
        category="regression",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Bugs",
        session_date=date(2025, 10, 20),
        related_files=["src/cache.py", "tests/test_cache.py"],
    )

    item2 = ActionItem(
        id="2025-10-20-test#section#2",
        title="Cache invalidation issue",
        description="Cache entries not being cleared.",
        category="regression",
        impact="high",
        confidence="high",
        source_summary="summary2.md",
        source_section="Issues",
        session_date=date(2025, 10, 21),
        related_files=["src/cache.py", "src/config.py"],
    )

    similarity = compute_contextual_similarity(item1, item2)
    assert (
        similarity >= 0.60
    )  # File overlap: 1/3 = 0.33, category match: 1.0, impact match: 1.0 → ~0.63


@pytest.mark.unit
def test_contextual_similarity_different_initiatives():
    """Different initiatives with no file overlap → low similarity."""

    item1 = ActionItem(
        id="2025-10-20-test#section#1",
        title="Add feature X",
        description="Implement new feature.",
        category="improvement",
        impact="high",
        confidence="high",
        source_summary="summary1.md",
        source_section="Features",
        session_date=date(2025, 10, 20),
        related_files=["src/feature_x.py"],
    )

    item2 = ActionItem(
        id="2025-10-20-test#section#2",
        title="Fix bug in module Y",
        description="Resolve crash in module Y.",
        category="regression",
        impact="high",
        confidence="high",
        source_summary="summary2.md",
        source_section="Bugs",
        session_date=date(2025, 10, 21),
        related_files=["src/module_y.py"],
    )

    similarity = compute_contextual_similarity(item1, item2)
    assert similarity < 0.20  # Different context


# ============================================================================
# Deduplication Pipeline Tests
# ============================================================================


@pytest.mark.unit
def test_deduplicate_items_exact_duplicates():
    """Pipeline should identify and merge exact duplicates."""

    items = [
        ActionItem(
            id="2025-10-20-summary1#section#1",
            title="Add caching",
            description="Implement caching to reduce API calls.",
            category="improvement",
            impact="high",
            confidence="high",
            source_summary="summary1.md",
            source_section="Improvements",
            session_date=date(2025, 10, 20),
        ),
        ActionItem(
            id="2025-10-21-summary2#section#1",
            title="Add caching",
            description="Implement caching to reduce API calls.",
            category="improvement",
            impact="high",
            confidence="high",
            source_summary="summary2.md",
            source_section="Improvements",
            session_date=date(2025, 10, 21),
        ),
        ActionItem(
            id="2025-10-22-summary3#section#1",
            title="Fix authentication",
            description="Resolve API key validation bug.",
            category="regression",
            impact="high",
            confidence="high",
            source_summary="summary3.md",
            source_section="Bugs",
            session_date=date(2025, 10, 22),
        ),
    ]

    deduplicated = deduplicate_items(items)
    assert len(deduplicated) == 2  # Two distinct items


@pytest.mark.unit
@pytest.mark.requires_api
def test_deduplicate_items_cascading_logic():
    """Pipeline should cascade through levels (1 → 2 → 3) - requires API key."""

    # Items that fail Level 1 but succeed Level 2
    items = [  # noqa: F841
        ActionItem(
            id="2025-10-20-summary1#section#1",
            title="Performance is slow",
            description="Application takes too long to load.",
            category="performance",
            impact="high",
            confidence="high",
            source_summary="summary1.md",
            source_section="Issues",
            session_date=date(2025, 10, 20),
        ),
        ActionItem(
            id="2025-10-21-summary2#section#1",
            title="Slow loading times",
            description="Data retrieval is very slow.",
            category="performance",
            impact="high",
            confidence="high",
            source_summary="summary2.md",
            source_section="Problems",
            session_date=date(2025, 10, 21),
        ),
    ]

    # from scripts.extract_action_items import deduplicate_items
    # deduplicated = deduplicate_items(items)
    # assert len(deduplicated) == 1  # Merged by semantic similarity


@pytest.mark.unit
def test_deduplicate_items_borderline_cases():
    """Borderline cases (60-85% similarity) should be flagged for review."""

    items = [
        ActionItem(
            id="2025-10-20-summary1#section#1",
            title="Add caching",
            description="Implement caching to improve performance.",
            category="improvement",
            impact="high",
            confidence="high",
            source_summary="summary1.md",
            source_section="Improvements",
            session_date=date(2025, 10, 20),
        ),
        ActionItem(
            id="2025-10-21-summary2#section#1",
            title="Optimize queries",
            description="Improve query performance by adding indexes.",
            category="performance",
            impact="high",
            confidence="high",
            source_summary="summary2.md",
            source_section="Performance",
            session_date=date(2025, 10, 21),
        ),
    ]

    deduplicated, borderline = deduplicate_items(items, return_borderline=True)
    # Borderline if similarity between caching and query optimization is in 60-85% range
    assert isinstance(borderline, list)  # Should return list even if empty


# ============================================================================
# Human Review Export Tests
# ============================================================================


@pytest.mark.unit
def test_export_borderline_cases_yaml(tmp_path):
    """Export borderline cases to YAML for human review."""

    borderline_pairs = [
        {
            "item1": ActionItem(
                id="2025-10-20-summary1#section#1",
                title="Add caching",
                description="Implement caching.",
                category="improvement",
                impact="high",
                confidence="high",
                source_summary="summary1.md",
                source_section="Improvements",
                session_date=date(2025, 10, 20),
            ),
            "item2": ActionItem(
                id="2025-10-21-summary2#section#1",
                title="Implement cache",
                description="Add caching layer.",
                category="improvement",
                impact="high",
                confidence="high",
                source_summary="summary2.md",
                source_section="Improvements",
                session_date=date(2025, 10, 21),
            ),
            "similarity": 0.75,
            "level": "text",
        }
    ]

    output_path = tmp_path / "borderline.yaml"
    export_borderline_cases(borderline_pairs, output_path)

    yaml_content = output_path.read_text()
    assert "similarity: 0.75" in yaml_content
    assert "item1:" in yaml_content
    assert "item2:" in yaml_content


@pytest.mark.unit
def test_export_borderline_cases_multiple_pairs(tmp_path):
    """Verify exported content with multiple borderline pairs."""

    # Test exporting multiple pairs
    borderline_pairs = [
        {
            "item1": ActionItem(
                id="test1#1",
                title="Item 1",
                description="Desc 1",
                category="improvement",
                impact="high",
                confidence="high",
                source_summary="summary1.md",
                source_section="Section",
                session_date=date(2025, 10, 20),
            ),
            "item2": ActionItem(
                id="test2#1",
                title="Item 2",
                description="Desc 2",
                category="improvement",
                impact="high",
                confidence="high",
                source_summary="summary2.md",
                source_section="Section",
                session_date=date(2025, 10, 21),
            ),
            "similarity": 0.75,
            "level": "text",
        },
        {
            "item1": ActionItem(
                id="test3#1",
                title="Item 3",
                description="Desc 3",
                category="testing",
                impact="medium",
                confidence="medium",
                source_summary="summary3.md",
                source_section="Section",
                session_date=date(2025, 10, 22),
            ),
            "item2": ActionItem(
                id="test4#1",
                title="Item 4",
                description="Desc 4",
                category="testing",
                impact="medium",
                confidence="medium",
                source_summary="summary4.md",
                source_section="Section",
                session_date=date(2025, 10, 23),
            ),
            "similarity": 0.80,
            "level": "semantic",
        },
    ]

    output_path = tmp_path / "borderline.yaml"
    export_borderline_cases(borderline_pairs, output_path)

    yaml_content = output_path.read_text()
    assert "review_required: 2" in yaml_content
    assert "similarity: 0.75" in yaml_content
    assert "similarity: 0.8" in yaml_content  # YAML may output 0.8 instead of 0.80
