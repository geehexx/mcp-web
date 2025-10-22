"""Common validation patterns for scripts.

This module provides base classes and utilities for validation scripts,
consolidating error collection, file walking, and reporting patterns.

Usage:
    from scripts.lib.validation import BaseValidator, ValidationResult

    class MyValidator(BaseValidator):
        def validate_file(self, file_path: Path) -> list[str]:
            errors = []
            # ... validation logic
            return errors

    validator = MyValidator()
    result = validator.validate_directory(Path("docs/"), "*.md")
    result.print_report()
    sys.exit(result.exit_code())
"""

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of validation run."""

    total_files: int = 0
    valid_files: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, error: str) -> None:
        """Add validation error."""
        self.errors.append(error)

    def add_warning(self, warning: str) -> None:
        """Add validation warning."""
        self.warnings.append(warning)

    def has_errors(self) -> bool:
        """Check if validation had errors."""
        return len(self.errors) > 0

    def exit_code(self) -> int:
        """Get exit code (0 = success, 1 = errors found)."""
        return 1 if self.has_errors() else 0

    def print_report(self, title: str = "Validation Report") -> None:
        """Print formatted validation report."""
        print()
        print("=" * 70)
        print(f"{title}")
        print("=" * 70)
        print()
        print(f"Files validated: {self.total_files}")
        print(f"Valid: {self.valid_files}")
        print(f"Errors: {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print()

        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  • {error}")
            print()

        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()

        if not self.errors and not self.warnings:
            print("✅ All validations passed!")
            print()


class BaseValidator:
    """Base class for validation scripts.

    Subclasses should implement validate_file() method.
    """

    def __init__(self, verbose: bool = False) -> None:
        """Initialize validator.

        Args:
            verbose: If True, print per-file validation status
        """
        self.verbose = verbose

    def validate_file(self, file_path: Path) -> list[str]:
        """Validate single file.

        Args:
            file_path: Path to file to validate

        Returns:
            List of error messages (empty if valid)
        """
        raise NotImplementedError("Subclasses must implement validate_file()")

    def validate_directory(
        self, directory: Path, pattern: str = "*.md", exclude: list[str] | None = None
    ) -> ValidationResult:
        """Validate all files matching pattern in directory.

        Args:
            directory: Directory to search
            pattern: Glob pattern for files to validate
            exclude: List of filenames to exclude

        Returns:
            ValidationResult with aggregated results
        """
        result = ValidationResult()
        exclude = exclude or []

        for file_path in walk_files(directory, pattern, exclude):
            result.total_files += 1

            if self.verbose:
                print(f"  Validating {file_path.name}...", end=" ")

            errors = self.validate_file(file_path)

            if errors:
                for error in errors:
                    result.add_error(f"{file_path}: {error}")
                if self.verbose:
                    print("❌")
            else:
                result.valid_files += 1
                if self.verbose:
                    print("✅")

        return result


def walk_files(
    directory: Path, pattern: str = "*.md", exclude: list[str] | None = None
) -> Iterator[Path]:
    """Walk directory and yield files matching pattern.

    Args:
        directory: Directory to search
        pattern: Glob pattern for files
        exclude: List of filenames to exclude

    Yields:
        Path objects for matching files
    """
    exclude = exclude or []

    for file_path in sorted(directory.rglob(pattern)):
        if file_path.is_file() and file_path.name not in exclude:
            yield file_path


def collect_errors(file_path: Path, checks: list[tuple[bool, str]]) -> list[str]:
    """Collect errors from validation checks.

    Args:
        file_path: Path to file being validated
        checks: List of (is_valid, error_message) tuples

    Returns:
        List of error messages for failed checks
    """
    errors = []
    for is_valid, error_msg in checks:
        if not is_valid:
            errors.append(f"{file_path}: {error_msg}")
    return errors
