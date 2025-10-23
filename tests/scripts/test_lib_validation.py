"""Tests for scripts.lib.validation module."""

from pathlib import Path

import pytest
from scripts.lib.validation import BaseValidator, ValidationResult, collect_errors, walk_files


class TestValidationResult:
    """Tests for ValidationResult class."""

    def test_initial_state(self):
        """Test ValidationResult initial state."""
        result = ValidationResult()

        assert result.total_files == 0
        assert result.valid_files == 0
        assert result.errors == []
        assert result.warnings == []
        assert not result.has_errors()
        assert result.exit_code() == 0

    def test_add_error(self):
        """Test adding errors."""
        result = ValidationResult()
        result.add_error("Error 1")
        result.add_error("Error 2")

        assert len(result.errors) == 2
        assert result.has_errors()
        assert result.exit_code() == 1

    def test_add_warning(self):
        """Test adding warnings."""
        result = ValidationResult()
        result.add_warning("Warning 1")

        assert len(result.warnings) == 1
        assert not result.has_errors()
        assert result.exit_code() == 0  # Warnings don't affect exit code

    def test_print_report_success(self, capsys):
        """Test print_report with successful validation."""
        result = ValidationResult(total_files=5, valid_files=5)
        result.print_report("Test Report")

        captured = capsys.readouterr()
        assert "Test Report" in captured.out
        assert "Files validated: 5" in captured.out
        assert "Valid: 5" in captured.out
        assert "Errors: 0" in captured.out
        assert "✅ All validations passed!" in captured.out

    def test_print_report_with_errors(self, capsys):
        """Test print_report with errors."""
        result = ValidationResult(total_files=3, valid_files=1)
        result.add_error("Error 1")
        result.add_error("Error 2")
        result.print_report("Test Report")

        captured = capsys.readouterr()
        assert "❌ ERRORS:" in captured.out
        assert "Error 1" in captured.out
        assert "Error 2" in captured.out


class TestBaseValidator:
    """Tests for BaseValidator class."""

    def test_not_implemented_error(self):
        """Test that BaseValidator.validate_file() raises NotImplementedError."""
        validator = BaseValidator()

        with pytest.raises(NotImplementedError, match="must implement validate_file"):
            validator.validate_file(Path("test.md"))

    def test_validate_directory(self, tmp_path):
        """Test validate_directory with custom validator."""

        # Create test validator
        class TestValidator(BaseValidator):
            def validate_file(self, file_path: Path) -> list[str]:
                # Return error if filename contains "bad"
                if "bad" in file_path.name:
                    return ["File is bad"]
                return []

        # Create test files
        (tmp_path / "good1.md").write_text("# Good")
        (tmp_path / "good2.md").write_text("# Good")
        (tmp_path / "bad.md").write_text("# Bad")

        validator = TestValidator()
        result = validator.validate_directory(tmp_path, "*.md")

        assert result.total_files == 3
        assert result.valid_files == 2
        assert len(result.errors) == 1
        assert "bad.md" in result.errors[0]

    def test_validate_directory_with_exclude(self, tmp_path):
        """Test validate_directory with exclusion list."""

        class TestValidator(BaseValidator):
            def validate_file(self, file_path: Path) -> list[str]:
                return []

        (tmp_path / "include.md").write_text("# Include")
        (tmp_path / "exclude.md").write_text("# Exclude")

        validator = TestValidator()
        result = validator.validate_directory(tmp_path, "*.md", exclude=["exclude.md"])

        assert result.total_files == 1
        assert result.valid_files == 1

    def test_validate_directory_verbose(self, tmp_path, capsys):
        """Test validate_directory with verbose mode."""

        class TestValidator(BaseValidator):
            def validate_file(self, file_path: Path) -> list[str]:
                return []

        (tmp_path / "test.md").write_text("# Test")

        validator = TestValidator(verbose=True)
        validator.validate_directory(tmp_path, "*.md")

        captured = capsys.readouterr()
        assert "Validating test.md" in captured.out
        assert "✅" in captured.out


class TestWalkFiles:
    """Tests for walk_files() function."""

    def test_walk_single_directory(self, tmp_path):
        """Test walking single directory."""
        (tmp_path / "file1.md").write_text("# File 1")
        (tmp_path / "file2.md").write_text("# File 2")
        (tmp_path / "file.txt").write_text("Text file")

        files = list(walk_files(tmp_path, "*.md"))

        assert len(files) == 2
        assert all(f.suffix == ".md" for f in files)

    def test_walk_nested_directories(self, tmp_path):
        """Test walking nested directories."""
        (tmp_path / "file1.md").write_text("# File 1")
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (subdir / "file2.md").write_text("# File 2")

        files = list(walk_files(tmp_path, "*.md"))

        assert len(files) == 2

    def test_walk_with_exclusion(self, tmp_path):
        """Test walking with exclusion list."""
        (tmp_path / "include.md").write_text("# Include")
        (tmp_path / "exclude.md").write_text("# Exclude")

        files = list(walk_files(tmp_path, "*.md", exclude=["exclude.md"]))

        assert len(files) == 1
        assert files[0].name == "include.md"

    def test_walk_empty_directory(self, tmp_path):
        """Test walking empty directory."""
        files = list(walk_files(tmp_path, "*.md"))

        assert files == []


class TestCollectErrors:
    """Tests for collect_errors() function."""

    def test_no_errors(self, tmp_path):
        """Test with all checks passing."""
        file_path = tmp_path / "test.md"
        checks = [(True, "Check 1"), (True, "Check 2")]

        errors = collect_errors(file_path, checks)

        assert errors == []

    def test_single_error(self, tmp_path):
        """Test with single failing check."""
        file_path = tmp_path / "test.md"
        checks = [(True, "Check 1"), (False, "Check 2 failed")]

        errors = collect_errors(file_path, checks)

        assert len(errors) == 1
        assert "test.md" in errors[0]
        assert "Check 2 failed" in errors[0]

    def test_multiple_errors(self, tmp_path):
        """Test with multiple failing checks."""
        file_path = tmp_path / "test.md"
        checks = [(False, "Check 1 failed"), (False, "Check 2 failed"), (True, "Check 3")]

        errors = collect_errors(file_path, checks)

        assert len(errors) == 2
