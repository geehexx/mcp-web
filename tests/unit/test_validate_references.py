#!/usr/bin/env python3
"""Tests for validate_references.py script.

Tests internal markdown link validation including:
- Relative path resolution
- Section anchor validation
- Code block exclusion
- External link ignoring
"""

from pathlib import Path

import pytest


@pytest.fixture
def temp_docs_dir(tmp_path: Path) -> Path:
    """Create temporary docs directory structure for testing."""
    docs = tmp_path / "docs"
    docs.mkdir()

    # Create test files
    (docs / "guide.md").write_text(
        """# Test Guide

## Section One

This is section one.

## Section Two

This is section two.
"""
    )

    (docs / "README.md").write_text(
        """# Documentation

[Valid link](./guide.md)
[Valid link with anchor](./guide.md#section-one)
[Broken link](./nonexistent.md)
[Broken anchor](./guide.md#nonexistent-section)

External links should be ignored:
[External](https://example.com)
[HTTP](http://example.org)

```markdown
[Code block link](./should-be-ignored.md)
```
"""
    )

    arch_dir = docs / "architecture"
    arch_dir.mkdir()
    (arch_dir / "nested.md").write_text(
        """# Nested Document

[Parent link](../guide.md)
[Root link](../../guide.md)
[Sibling](./architecture.md)
"""
    )

    return docs


class TestMarkdownLinkExtraction:
    """Test extraction of markdown links from text."""

    def test_extract_simple_link(self):
        """Extract basic markdown link."""
        from scripts.validation.validate_references import extract_markdown_links

        text = "[Example](./file.md)"
        links = extract_markdown_links(text)

        assert len(links) == 1
        assert links[0]["text"] == "Example"
        assert links[0]["url"] == "./file.md"
        assert links[0]["line"] == 0

    def test_extract_multiple_links(self):
        """Extract multiple links from same line."""
        from scripts.validation.validate_references import extract_markdown_links

        text = "[Link1](./file1.md) and [Link2](./file2.md)"
        links = extract_markdown_links(text)

        assert len(links) == 2
        assert links[0]["url"] == "./file1.md"
        assert links[1]["url"] == "./file2.md"

    def test_extract_link_with_anchor(self):
        """Extract link with section anchor."""
        from scripts.validation.validate_references import extract_markdown_links

        text = "[Section](./file.md#heading)"
        links = extract_markdown_links(text)

        assert len(links) == 1
        assert links[0]["url"] == "./file.md#heading"
        assert "#heading" in links[0]["url"]

    def test_ignore_external_links(self):
        """External URLs should not be extracted."""
        from scripts.validation.validate_references import extract_markdown_links

        text = """
[HTTP](http://example.com)
[HTTPS](https://example.org)
[Internal](./file.md)
"""
        links = extract_markdown_links(text)

        # Only internal link should be extracted
        assert len(links) == 1
        assert links[0]["url"] == "./file.md"

    def test_ignore_code_blocks(self):
        """Links in code blocks should be ignored."""
        from scripts.validation.validate_references import extract_markdown_links

        text = """
[Valid link](./file.md)

```markdown
[Code block link](./should-ignore.md)
```

[Another valid](./file2.md)
"""
        links = extract_markdown_links(text)

        # Should only extract links outside code blocks
        assert len(links) == 2
        assert links[0]["url"] == "./file.md"
        assert links[1]["url"] == "./file2.md"

    def test_extract_with_line_numbers(self):
        """Links should include correct line numbers."""
        from scripts.validation.validate_references import extract_markdown_links

        text = """Line 0
[Link on line 1](./file1.md)
Line 2
[Link on line 3](./file2.md)
"""
        links = extract_markdown_links(text)

        assert links[0]["line"] == 1
        assert links[1]["line"] == 3


class TestPathResolution:
    """Test relative path resolution."""

    def test_resolve_current_directory(self):
        """Resolve ./file.md relative to current file."""
        from scripts.validation.validate_references import resolve_link_path

        source = Path("/project/docs/README.md")
        link = "./guide.md"
        resolved = resolve_link_path(source, link, root=Path("/project"))

        assert resolved == Path("/project/docs/guide.md")

    def test_resolve_parent_directory(self):
        """Resolve ../file.md going up one level."""
        from scripts.validation.validate_references import resolve_link_path

        source = Path("/project/docs/guides/testing.md")
        link = "../README.md"
        resolved = resolve_link_path(source, link, root=Path("/project"))

        assert resolved == Path("/project/docs/README.md")

    def test_resolve_absolute_from_root(self):
        """Resolve /docs/file.md as absolute from project root."""
        from scripts.validation.validate_references import resolve_link_path

        source = Path("/project/docs/guides/testing.md")
        link = "/docs/README.md"
        resolved = resolve_link_path(source, link, root=Path("/project"))

        assert resolved == Path("/project/docs/README.md")

    def test_resolve_removes_anchor(self):
        """Path resolution should remove #anchor fragment."""
        from scripts.validation.validate_references import resolve_link_path

        source = Path("/project/docs/README.md")
        link = "./guide.md#section-one"
        resolved = resolve_link_path(source, link, root=Path("/project"))

        assert resolved == Path("/project/docs/guide.md")


class TestAnchorValidation:
    """Test markdown section anchor validation."""

    def test_validate_existing_anchor(self):
        """Valid anchor to existing heading should pass."""
        from scripts.validation.validate_references import validate_anchor

        content = """
# Main Title

## Section One

Some content here.

### Subsection

More content.
"""
        assert validate_anchor(content, "section-one") is True

    def test_validate_nonexistent_anchor(self):
        """Anchor to non-existent heading should fail."""
        from scripts.validation.validate_references import validate_anchor

        content = """
# Main Title

## Section One
"""
        assert validate_anchor(content, "section-two") is False

    def test_normalize_anchor_casing(self):
        """Anchors should be normalized (lowercase, hyphenated)."""
        from scripts.validation.validate_references import validate_anchor

        content = "## Section One Two"

        # All these should match the heading
        assert validate_anchor(content, "section-one-two") is True
        assert validate_anchor(content, "Section-One-Two") is True  # Normalized to lowercase

    def test_validate_anchor_special_chars(self):
        """Anchors with special characters should be handled."""
        from scripts.validation.validate_references import validate_anchor

        content = "## Testing & Validation"

        # Special chars removed in anchor generation (& becomes nothing)
        assert validate_anchor(content, "testing-validation") is True


class TestLinkValidation:
    """Test full link validation workflow."""

    def test_validate_valid_file_link(self, temp_docs_dir: Path):
        """Valid link to existing file should pass."""
        from scripts.validation.validate_references import validate_link

        source = temp_docs_dir / "README.md"
        link = {"url": "./guide.md", "text": "Guide", "line": 1}

        result = validate_link(source, link, root=temp_docs_dir.parent)

        assert result["valid"] is True
        assert result["error"] is None

    def test_validate_broken_file_link(self, temp_docs_dir: Path):
        """Invalid link to non-existent file should fail."""
        from scripts.validation.validate_references import validate_link

        source = temp_docs_dir / "README.md"
        link = {"url": "./nonexistent.md", "text": "Broken", "line": 1}

        result = validate_link(source, link, root=temp_docs_dir.parent)

        assert result["valid"] is False
        assert "does not exist" in result["error"].lower()

    def test_validate_valid_anchor_link(self, temp_docs_dir: Path):
        """Valid link with anchor to existing section should pass."""
        from scripts.validation.validate_references import validate_link

        source = temp_docs_dir / "README.md"
        link = {"url": "./guide.md#section-one", "text": "Guide", "line": 1}

        result = validate_link(source, link, root=temp_docs_dir.parent)

        assert result["valid"] is True

    def test_validate_broken_anchor_link(self, temp_docs_dir: Path):
        """Link with invalid anchor should fail."""
        from scripts.validation.validate_references import validate_link

        source = temp_docs_dir / "README.md"
        link = {"url": "./guide.md#nonexistent", "text": "Guide", "line": 1}

        result = validate_link(source, link, root=temp_docs_dir.parent)

        assert result["valid"] is False
        assert "anchor" in result["error"].lower()


class TestScriptIntegration:
    """Test full script execution."""

    def test_scan_directory(self, temp_docs_dir: Path):
        """Scan directory and find all markdown files."""
        from scripts.validation.validate_references import scan_markdown_files

        files = scan_markdown_files(temp_docs_dir)

        assert len(files) >= 2
        assert any(f.name == "README.md" for f in files)
        assert any(f.name == "guide.md" for f in files)

    def test_validate_directory_with_errors(self, temp_docs_dir: Path):
        """Validate directory and detect broken links."""
        from scripts.validation.validate_references import validate_directory

        errors = validate_directory(temp_docs_dir, root=temp_docs_dir.parent)

        # Should find at least 2 errors from README.md
        # (broken file link and broken anchor)
        assert len(errors) >= 2

        # Check error structure
        error = errors[0]
        assert "file" in error
        assert "line" in error
        assert "link" in error
        assert "error" in error

    def test_generate_report(self, temp_docs_dir: Path):
        """Generate human-readable error report."""
        from scripts.validation.validate_references import generate_report, validate_directory

        errors = validate_directory(temp_docs_dir, root=temp_docs_dir.parent)
        report = generate_report(errors)

        assert "broken links" in report.lower()
        assert len(errors) > 0  # Should have errors from test setup


class TestIgnorePatterns:
    """Test link ignore patterns."""

    def test_ignore_placeholder_links(self):
        """Placeholder links like 'path/to/file' should be ignored."""
        from scripts.validation.validate_references import should_ignore_link

        assert should_ignore_link("path/to/file.md") is True
        assert should_ignore_link("relative/path/to/docs") is True

    def test_ignore_external_links(self):
        """External URLs should be ignored."""
        from scripts.validation.validate_references import should_ignore_link

        assert should_ignore_link("https://example.com") is True
        assert should_ignore_link("http://example.org") is True
        assert should_ignore_link("mailto:test@example.com") is True

    def test_allow_internal_links(self):
        """Internal relative links should not be ignored."""
        from scripts.validation.validate_references import should_ignore_link

        assert should_ignore_link("./docs/file.md") is False
        assert should_ignore_link("../README.md") is False
        assert should_ignore_link("/docs/guide.md") is False
