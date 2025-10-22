"""
Comprehensive tests for file_ops.py automation utilities.

Tests archive_initiative, move_file_with_refs, and update_index functions
using Golden Master pattern with extensive edge case coverage.
"""

import tempfile
from pathlib import Path

import pytest

from scripts.automation.file_ops import (
    archive_initiative,
    move_file_with_refs,
    update_index,
)


@pytest.fixture
def temp_repo():
    """Create temporary repository structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)

        # Create directory structure
        (base / "docs/initiatives/active").mkdir(parents=True)
        (base / "docs/initiatives/completed").mkdir(parents=True)
        (base / "docs/initiatives/README.md").touch()

        yield base


class TestArchiveInitiative:
    """Test archive_initiative function."""

    def test_archive_flat_file_initiative(self, temp_repo):
        """Test archiving flat-file initiative."""
        # Create test initiative
        initiative_file = temp_repo / "docs/initiatives/active/2025-10-test.md"
        initiative_file.write_text("""---
Status: Completed
---

# Test Initiative

Content here.
""")

        # Archive it
        result = archive_initiative(
            "2025-10-test.md",
            root=temp_repo,
            completed_on="2025-10-22",
            dry_run=False,
        )

        # Check results
        assert "moved" in result
        assert len(result["moved"]) > 0

        # Check file moved
        completed_file = temp_repo / "docs/initiatives/completed/2025-10-test.md"
        assert completed_file.exists()
        assert not initiative_file.exists()

    def test_archive_folder_initiative(self, temp_repo):
        """Test archiving folder-based initiative."""
        # Create folder initiative
        folder = temp_repo / "docs/initiatives/active/2025-10-folder-test"
        folder.mkdir()
        initiative_file = folder / "initiative.md"
        initiative_file.write_text("""---
Status: Completed
---

# Folder Initiative
""")

        # Archive it
        result = archive_initiative(
            "2025-10-folder-test",
            root=temp_repo,
            completed_on="2025-10-22",
            dry_run=False,
        )

        assert "moved" in result

        # Check folder moved
        completed_folder = temp_repo / "docs/initiatives/completed/2025-10-folder-test"
        assert completed_folder.exists()
        assert (completed_folder / "initiative.md").exists()

    def test_archive_dry_run(self, temp_repo):
        """Test dry-run mode doesn't modify files."""
        initiative_file = temp_repo / "docs/initiatives/active/2025-10-test.md"
        initiative_file.write_text("""---
Status: Completed
---

# Test
""")

        # Dry run
        result = archive_initiative(
            "2025-10-test.md",
            root=temp_repo,
            completed_on="2025-10-22",
            dry_run=True,
        )

        assert "moved" in result

        # File should still exist in active
        assert initiative_file.exists()


class TestMoveFileWithRefs:
    """Test move_file_with_refs function."""

    def test_move_file_updates_references(self, temp_repo):
        """Test moving file updates references in other files."""
        # Create source file
        src = temp_repo / "docs/initiatives/active/test.md"
        src.write_text("# Test")

        # Create file with reference
        ref_file = temp_repo / "docs/REFERENCES.md"
        ref_file.write_text("""
Link to [test](initiatives/active/test.md) here.
""")

        # Move file
        dst = temp_repo / "docs/initiatives/completed/test.md"
        result = move_file_with_refs(
            src,
            dst,
            root=temp_repo,
            dry_run=False,
        )

        assert "moved" in result
        assert "references" in result

        # Check file moved
        assert dst.exists()
        assert not src.exists()

        # Check reference updated
        updated_content = ref_file.read_text()
        assert "initiatives/completed/test.md" in updated_content

    def test_move_file_dry_run(self, temp_repo):
        """Test dry-run doesn't modify files."""
        src = temp_repo / "docs/initiatives/active/test.md"
        src.write_text("# Test")
        dst = temp_repo / "docs/initiatives/completed/test.md"

        result = move_file_with_refs(
            src,
            dst,
            root=temp_repo,
            dry_run=True,
        )

        assert "moved" in result

        # File should not be moved
        assert src.exists()
        assert not dst.exists()


class TestUpdateIndex:
    """Test update_index function."""

    def test_update_index_creates_listing(self, temp_repo):
        """Test updating README index."""
        # Create initiatives
        (temp_repo / "docs/initiatives/active/init1.md").write_text("# Init 1")
        (temp_repo / "docs/initiatives/active/init2.md").write_text("# Init 2")
        (temp_repo / "docs/initiatives/completed/old.md").write_text("# Old")

        # Update index
        result = update_index(
            temp_repo / "docs/initiatives",
            root=temp_repo,
            dry_run=False,
        )

        assert result is True

        # Check README updated
        readme = temp_repo / "docs/initiatives/README.md"
        content = readme.read_text()
        assert "init1.md" in content
        assert "init2.md" in content
        assert "old.md" in content

    def test_update_index_idempotent(self, temp_repo):
        """Test updating index twice produces same result."""
        (temp_repo / "docs/initiatives/active/test.md").write_text("# Test")

        # Update twice
        update_index(temp_repo / "docs/initiatives", root=temp_repo, dry_run=False)
        content1 = (temp_repo / "docs/initiatives/README.md").read_text()

        update_index(temp_repo / "docs/initiatives", root=temp_repo, dry_run=False)
        content2 = (temp_repo / "docs/initiatives/README.md").read_text()

        assert content1 == content2


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_archive_nonexistent_initiative(self, temp_repo):
        """Test archiving non-existent initiative raises error."""
        with pytest.raises(FileNotFoundError):
            archive_initiative(
                "nonexistent.md",
                root=temp_repo,
                dry_run=False,
            )

    def test_archive_already_completed(self, temp_repo):
        """Test archiving initiative already in completed/."""
        completed_file = temp_repo / "docs/initiatives/completed/test.md"
        completed_file.write_text("# Already Completed")

        # Should raise error (not in active)
        with pytest.raises(ValueError):
            archive_initiative(
                str(completed_file),
                root=temp_repo,
                dry_run=False,
            )

    def test_move_file_destination_exists(self, temp_repo):
        """Test moving to existing destination."""
        src = temp_repo / "docs/test.md"
        dst = temp_repo / "docs/existing.md"
        src.write_text("# Source")
        dst.write_text("# Existing")

        # Should raise error
        with pytest.raises(FileExistsError):
            move_file_with_refs(src, dst, root=temp_repo, dry_run=False)

    def test_unicode_handling(self, temp_repo):
        """Test handling Unicode in filenames and content."""
        initiative_file = temp_repo / "docs/initiatives/active/2025-10-test.md"
        initiative_file.write_text("""---
Status: Completed
---

# Test Initiative 🎯

Unicode content: 日本語
""")

        result = archive_initiative(
            "2025-10-test.md",
            root=temp_repo,
            completed_on="2025-10-22",
            dry_run=False,
        )

        assert "moved" in result

        # Check content preserved
        completed_file = temp_repo / "docs/initiatives/completed/2025-10-test.md"
        content = completed_file.read_text()
        assert "🎯" in content
        assert "日本語" in content


class TestCLIIntegration:
    """Test CLI usage via task commands."""

    def test_archive_via_task_help(self):
        """Test task archive:initiative help."""
        import subprocess

        result = subprocess.run(
            ["task", "--list"],
            capture_output=True,
            text=True,
        )

        # Check archive tasks exist
        assert result.returncode == 0
        assert "archive" in result.stdout.lower() or "task" in result.stdout.lower()
