"""Tests for scripts.lib.frontmatter module."""

from pathlib import Path

import pytest

from scripts.lib.frontmatter import (
    FrontmatterError,
    extract_frontmatter,
    extract_frontmatter_lenient,
    has_frontmatter,
    validate_frontmatter,
)


@pytest.fixture
def tmp_markdown_file(tmp_path):
    """Fixture to create temporary markdown files."""

    def _create(content: str) -> Path:
        file_path = tmp_path / "test.md"
        file_path.write_text(content)
        return file_path

    return _create


class TestExtractFrontmatter:
    """Tests for extract_frontmatter()."""

    def test_valid_frontmatter(self, tmp_markdown_file):
        """Test extracting valid YAML frontmatter."""
        content = """---
title: Test Document
status: active
tags: ["test", "example"]
---

# Content here
"""
        file_path = tmp_markdown_file(content)
        result = extract_frontmatter(file_path)

        assert result is not None
        assert result["title"] == "Test Document"
        assert result["status"] == "active"
        assert result["tags"] == ["test", "example"]

    def test_no_frontmatter(self, tmp_markdown_file):
        """Test file without frontmatter."""
        content = "# Just content"
        file_path = tmp_markdown_file(content)

        # Non-strict mode returns None
        result = extract_frontmatter(file_path, strict=False)
        assert result is None

        # Strict mode raises error
        with pytest.raises(FrontmatterError, match="No frontmatter found"):
            extract_frontmatter(file_path, strict=True)

    def test_missing_closing_delimiter(self, tmp_markdown_file):
        """Test frontmatter without closing ---."""
        content = """---
title: Test
# Content"""
        file_path = tmp_markdown_file(content)

        result = extract_frontmatter(file_path, strict=False)
        assert result is None

        with pytest.raises(FrontmatterError, match="Invalid frontmatter format"):
            extract_frontmatter(file_path, strict=True)

    def test_invalid_yaml(self, tmp_markdown_file):
        """Test frontmatter with invalid YAML."""
        content = """---
title: Test
invalid: [unclosed
---

# Content
"""
        file_path = tmp_markdown_file(content)

        result = extract_frontmatter(file_path, strict=False)
        assert result is None

        with pytest.raises(FrontmatterError, match="Invalid YAML"):
            extract_frontmatter(file_path, strict=True)

    def test_frontmatter_not_dict(self, tmp_markdown_file):
        """Test frontmatter that doesn't parse to dict."""
        content = """---
- item1
- item2
---

# Content
"""
        file_path = tmp_markdown_file(content)

        result = extract_frontmatter(file_path, strict=False)
        assert result is None

    def test_empty_frontmatter(self, tmp_markdown_file):
        """Test empty frontmatter block."""
        content = """---
---

# Content
"""
        file_path = tmp_markdown_file(content)
        result = extract_frontmatter(file_path)

        # Empty YAML parses to None, which should be handled
        assert result is None


class TestExtractFrontmatterLenient:
    """Tests for extract_frontmatter_lenient()."""

    def test_standard_yaml(self, tmp_markdown_file):
        """Test that lenient parser handles standard YAML."""
        content = """---
title: "Test"
globs: ["*.py", "**/*.py"]
---

# Content
"""
        file_path = tmp_markdown_file(content)
        result = extract_frontmatter_lenient(file_path)

        assert result is not None
        assert result["title"] == "Test"
        assert result["globs"] == ["*.py", "**/*.py"]

    def test_windsurf_unquoted_globs(self, tmp_markdown_file):
        """Test Windsurf format with unquoted globs."""
        content = """---
trigger: glob
globs: *.py, **/*.py
description: Some description
---

# Content
"""
        file_path = tmp_markdown_file(content)
        result = extract_frontmatter_lenient(file_path)

        assert result is not None
        assert result["trigger"] == "glob"
        assert result["globs"] == "*.py, **/*.py"  # Kept as string
        assert result["description"] == "Some description"

    def test_mixed_format(self, tmp_markdown_file):
        """Test mixed standard and Windsurf formats."""
        content = """---
trigger: glob
globs: *.py, **/*.py
tags: ["test"]
---

# Content
"""
        file_path = tmp_markdown_file(content)
        result = extract_frontmatter_lenient(file_path)

        assert result is not None
        assert result["trigger"] == "glob"
        assert result["globs"] == "*.py, **/*.py"

    def test_no_frontmatter(self, tmp_markdown_file):
        """Test lenient parser with no frontmatter."""
        content = "# Just content"
        file_path = tmp_markdown_file(content)
        result = extract_frontmatter_lenient(file_path)

        assert result is None


class TestValidateFrontmatter:
    """Tests for validate_frontmatter()."""

    def test_all_required_fields_present(self):
        """Test validation with all required fields."""
        data = {"title": "Test", "status": "active"}
        errors = validate_frontmatter(data, required_fields=["title", "status"])

        assert errors == []

    def test_missing_required_field(self):
        """Test validation with missing required field."""
        data = {"title": "Test"}
        errors = validate_frontmatter(data, required_fields=["title", "status"])

        assert len(errors) == 1
        assert "Missing required field: status" in errors[0]

    def test_multiple_missing_fields(self):
        """Test validation with multiple missing fields."""
        data = {}
        errors = validate_frontmatter(data, required_fields=["title", "status", "date"])

        assert len(errors) == 3

    def test_no_required_fields(self):
        """Test validation with no requirements."""
        data = {"any": "data"}
        errors = validate_frontmatter(data, required_fields=None)

        assert errors == []


class TestHasFrontmatter:
    """Tests for has_frontmatter()."""

    def test_file_with_frontmatter(self, tmp_markdown_file):
        """Test file that has frontmatter."""
        content = """---
title: Test
---

# Content
"""
        file_path = tmp_markdown_file(content)
        assert has_frontmatter(file_path) is True

    def test_file_without_frontmatter(self, tmp_markdown_file):
        """Test file without frontmatter."""
        content = "# Just content"
        file_path = tmp_markdown_file(content)
        assert has_frontmatter(file_path) is False

    def test_nonexistent_file(self, tmp_path):
        """Test nonexistent file."""
        file_path = tmp_path / "nonexistent.md"
        assert has_frontmatter(file_path) is False
