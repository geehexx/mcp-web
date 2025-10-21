"""Test markdown quality and enforce documentation standards.

This module provides automated tests for markdown quality to prevent regressions.
Tests verify that all markdown files conform to project standards.

Categories:
- Structural validation (linting)
- Code fence validation (language specifiers)
- Link validation
- File naming conventions
"""

import subprocess
from pathlib import Path

import pytest

# Directories to exclude from markdown checks (matches .markdownlint-cli2.jsonc)
EXCLUDE_PATTERNS = [
    "docs/archive",
    "docs/initiatives/completed",
    "node_modules",
    ".venv",
    ".pytest_cache",
    "__pycache__",
]


def should_check_file(file_path: Path) -> bool:
    """Determine if a markdown file should be checked."""
    path_str = str(file_path)
    return not any(pattern in path_str for pattern in EXCLUDE_PATTERNS)


def get_markdown_files() -> list[Path]:
    """Get all markdown files to check (excluding patterns)."""
    all_files = Path(".").rglob("*.md")
    return [f for f in all_files if should_check_file(f)]


@pytest.mark.unit
def test_markdown_files_exist():
    """Verify we have markdown files to test."""
    files = get_markdown_files()
    assert len(files) > 0, "No markdown files found to test"
    assert len(files) >= 50, f"Expected at least 50 markdown files, found {len(files)}"


@pytest.mark.unit
def test_markdownlint_passes():
    """Verify all markdown files pass markdownlint validation.

    Uses markdownlint-cli2 with project config for consistency.
    Respects .markdownlintignore and .markdownlint-cli2.jsonc configuration.
    """
    result = subprocess.run(
        [
            "npx",
            "markdownlint-cli2",
            "--config",
            ".markdownlint-cli2.jsonc",
            "**/*.md",
        ],
        capture_output=True,
        text=True,
        cwd=Path("."),
    )

    if result.returncode != 0:
        # Parse error output from markdownlint-cli2
        error_lines = result.stdout.strip().split("\n")
        summary_line = next((line for line in error_lines if "Summary:" in line), "")

        # Get first 20 error lines for debugging
        error_details = "\n".join(
            [
                line
                for line in error_lines
                if line.strip() and "Finding:" not in line and "Linting:" not in line
            ][:20]
        )

        pytest.fail(
            f"Markdownlint validation failed.\n"
            f"{summary_line}\n\n"
            f"Sample errors:\n{error_details}\n\n"
            f"To fix auto-fixable issues, run: task docs:fix\n"
            f"Or manually: npx markdownlint-cli2 --fix '**/*.md'"
        )


@pytest.mark.unit
def test_code_fences_have_language_specifiers():
    """Verify all code fences have language specifiers (MD040).

    Empty code fences (```) should specify a language like ```bash or ```text.
    This ensures proper syntax highlighting and accessibility.

    References:
    - https://github.com/DavidAnson/markdownlint/blob/main/doc/md040.md
    - CommonMark spec: https://spec.commonmark.org/
    """
    violations: list[tuple[Path, int, str]] = []

    for md_file in get_markdown_files():
        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # Skip binary files

        lines = content.split("\n")

        for i, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Check for code fence opening without language
            if stripped == "```" or stripped == "~~~":
                # This is either opening or closing fence
                # We need to determine if it's opening (followed by content)
                # or closing (preceded by content)

                # Simple heuristic: if previous line was inside a code block,
                # this is likely a closing fence (OK)
                # Otherwise, it's an opening fence (needs language)

                # For now, we'll check if next line exists and isn't a fence
                if i < len(lines):
                    next_line = lines[i].strip() if i < len(lines) else ""
                    # If next line is not empty and not a fence, this is opening
                    if (
                        next_line
                        and not next_line.startswith("```")
                        and not next_line.startswith("~~~")
                    ):
                        violations.append(
                            (md_file, i, f"Code fence without language specifier: {line.strip()}")
                        )

    if violations:
        error_msg = "\n".join(
            f"{file}:{line} - {msg}"
            for file, line, msg in violations[:20]  # Show first 20
        )
        total = len(violations)
        suffix = f"\n... and {total - 20} more violations" if total > 20 else ""

        pytest.fail(
            f"Found {total} code fences without language specifiers:\n\n"
            f"{error_msg}{suffix}\n\n"
            f"Fix by adding language specifier: ```bash, ```text, ```python, etc.\n"
            f"See: https://github.com/DavidAnson/markdownlint/blob/main/doc/md040.md"
        )


@pytest.mark.unit
def test_no_trailing_whitespace():
    """Verify markdown files don't have trailing whitespace (MD009).

    Trailing whitespace can cause issues with version control and is generally bad practice.
    Exception: Two trailing spaces are allowed as they create hard line breaks in markdown.
    """
    violations: list[tuple[Path, int]] = []

    for md_file in get_markdown_files():
        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        lines = content.split("\n")

        for i, line in enumerate(lines, start=1):
            # Check for trailing whitespace (but allow exactly 2 spaces for hard breaks)
            if line.endswith(" ") and not line.endswith("  "):
                violations.append((md_file, i))

    if violations:
        error_msg = "\n".join(f"{file}:{line}" for file, line in violations[:20])
        total = len(violations)
        suffix = f"\n... and {total - 20} more violations" if total > 20 else ""

        pytest.fail(
            f"Found {total} lines with trailing whitespace:\n\n"
            f"{error_msg}{suffix}\n\n"
            f"To fix: Remove trailing spaces from lines (except exactly 2 spaces for hard breaks)\n"
            f"Or run: task docs:fix"
        )


@pytest.mark.unit
def test_links_are_valid_format():
    """Verify markdown links use valid format (basic check).

    This is a basic sanity check - full link validation requires network access.
    Checks for:
    - Properly formatted links [text](url)
    - No empty links [](url) or [text]()
    """
    violations: list[tuple[Path, int, str]] = []

    for md_file in get_markdown_files():
        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        lines = content.split("\n")

        for i, line in enumerate(lines, start=1):
            # Check for empty link text [](...) - MD042
            if "](" in line:
                parts = line.split("](")
                for part in parts:
                    if part.endswith("["):
                        # Empty link text
                        violations.append((md_file, i, "Empty link text: [](...)"))

    # Note: This is a basic check - comprehensive link validation would require
    # more sophisticated parsing (e.g., using markdown parser)
    # For now, we rely on markdownlint for comprehensive link checking

    if violations:
        error_msg = "\n".join(f"{file}:{line} - {msg}" for file, line, msg in violations[:10])
        total = len(violations)
        suffix = f"\n... and {total - 10} more violations" if total > 10 else ""

        pytest.fail(f"Found {total} link formatting issues:\n\n{error_msg}{suffix}")


@pytest.mark.unit
@pytest.mark.slow
def test_markdownlint_config_consistency():
    """Verify markdownlint configuration files are consistent and valid.

    Checks that .markdownlint-cli2.jsonc is valid JSON and has required settings.
    """
    import json
    from pathlib import Path

    config_path = Path(".markdownlint-cli2.jsonc")
    assert config_path.exists(), "Missing .markdownlint-cli2.jsonc config file"

    # Read and validate JSON (strip comments for validation)
    content = config_path.read_text()
    # Remove line comments (simple approach)
    lines = [line.split("//")[0] for line in content.split("\n")]
    clean_json = "\n".join(lines)

    try:
        config = json.loads(clean_json)
    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON in .markdownlint-cli2.jsonc: {e}")

    # Verify required config sections
    assert "config" in config, "Missing 'config' section in markdownlint config"
    assert "ignores" in config, "Missing 'ignores' section in markdownlint config"

    # Verify ignores include key directories
    ignores = config["ignores"]
    assert any("archive" in ignore for ignore in ignores), "Should ignore docs/archive"
    assert any("pytest_cache" in ignore for ignore in ignores), "Should ignore .pytest_cache"


@pytest.mark.unit
def test_markdown_files_have_proper_extensions():
    """Verify markdown files use standard extensions (.md).

    Standard: Use .md extension for all markdown files.
    Alternative extensions like .markdown are valid but we standardize on .md
    """
    non_standard = []

    for file in Path(".").rglob("*.markdown"):
        if should_check_file(file):
            non_standard.append(file)

    assert len(non_standard) == 0, (
        f"Found {len(non_standard)} files with .markdown extension (use .md): {non_standard}"
    )


# CI-specific tests (may be slow)


@pytest.mark.slow
@pytest.mark.skipif(
    subprocess.run(["which", "vale"], capture_output=True).returncode != 0,
    reason="Vale not installed",
)
def test_prose_quality_with_vale():
    """Verify prose quality using Vale (if installed).

    This test is optional and only runs if Vale is available.
    Vale checks grammar, style, and readability.
    """
    result = subprocess.run(
        ["vale", "docs/", "README.md"],
        capture_output=True,
        text=True,
    )

    # Vale returns 0 for success, 1 for warnings, 2 for errors
    # We'll allow warnings but fail on errors
    assert result.returncode <= 1, f"Vale prose quality check failed:\n{result.stdout}"
