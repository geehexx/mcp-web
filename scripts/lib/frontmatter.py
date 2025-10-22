"""Unified frontmatter parsing for markdown files.

This module consolidates 3+ duplicate frontmatter parsing implementations
from various validation scripts into a single, well-tested library.

Usage:
    from scripts.lib.frontmatter import extract_frontmatter, extract_frontmatter_lenient

    # Standard parsing (strict YAML)
    data = extract_frontmatter(Path("workflow.md"))

    # Lenient parsing (handles Windsurf format with unquoted globs)
    data = extract_frontmatter_lenient(Path("rule.md"))
"""

from pathlib import Path
from typing import Any

import yaml


class FrontmatterError(Exception):
    """Exception raised for frontmatter parsing errors."""

    pass


def extract_frontmatter(file_path: Path, strict: bool = True) -> dict[str, Any] | None:
    """Extract YAML frontmatter from markdown file (strict parsing).

    Standard format:
    ```markdown
    ---
    key: "value"
    list: ["item1", "item2"]
    ---

    # Content here
    ```

    Args:
        file_path: Path to markdown file
        strict: If True, raise FrontmatterError on parse failures

    Returns:
        Parsed frontmatter as dict, or None if no frontmatter found

    Raises:
        FrontmatterError: If strict=True and parsing fails
    """
    try:
        with open(file_path) as f:
            content = f.read()
    except OSError as e:
        if strict:
            raise FrontmatterError(f"Cannot read file: {e}") from e
        return None

    # Check for frontmatter delimiters
    if not content.startswith("---"):
        if strict:
            raise FrontmatterError("No frontmatter found (file must start with ---)")
        return None

    # Split on frontmatter delimiters
    parts = content.split("---", 2)
    if len(parts) < 3:
        if strict:
            raise FrontmatterError("Invalid frontmatter format (missing closing ---)")
        return None

    frontmatter_str = parts[1]

    # Parse YAML
    try:
        data = yaml.safe_load(frontmatter_str)
        # Handle empty frontmatter (yaml.safe_load returns None)
        if data is None:
            return None
        if not isinstance(data, dict):
            if strict:
                raise FrontmatterError(
                    f"Frontmatter must be a YAML object (got {type(data).__name__})"
                )
            return None
        return data
    except yaml.YAMLError as e:
        if strict:
            raise FrontmatterError(f"Invalid YAML: {e}") from e
        return None


def extract_frontmatter_lenient(file_path: Path) -> dict[str, Any] | None:
    """Extract YAML frontmatter with lenient parsing (Windsurf-compatible).

    Windsurf format allows unquoted globs:
    ```markdown
    ---
    trigger: glob
    globs: *.py, **/*.py
    description: Some description
    ---
    ```

    This function first tries standard YAML parsing, then falls back to
    line-by-line parsing for Windsurf-specific formats.

    Args:
        file_path: Path to markdown file

    Returns:
        Parsed frontmatter as dict, or None if no frontmatter found
    """
    # Try standard parsing first
    result = extract_frontmatter(file_path, strict=False)
    if result is not None:
        return result

    # Fallback: lenient line-by-line parsing
    try:
        with open(file_path) as f:
            content = f.read()
    except OSError:
        return None

    if not content.startswith("---\n"):
        return None

    parts = content.split("---\n", 2)
    if len(parts) < 3:
        return None

    frontmatter_str = parts[1]
    frontmatter: dict[str, Any] = {}

    for line in frontmatter_str.strip().split("\n"):
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        # For globs field, accept Windsurf's comma-separated format
        if key == "globs":
            frontmatter[key] = value  # Keep as string
        else:
            # Try to parse other fields as YAML
            try:
                parsed = yaml.safe_load(f"{key}: {value}")
                if parsed and isinstance(parsed, dict):
                    frontmatter.update(parsed)
                else:
                    frontmatter[key] = value
            except yaml.YAMLError:
                frontmatter[key] = value

    return frontmatter if frontmatter else None


def validate_frontmatter(
    data: dict[str, Any],
    required_fields: list[str] | None = None,
    _optional_fields: list[str] | None = None,
) -> list[str]:
    """Validate frontmatter data against field requirements.

    Args:
        data: Parsed frontmatter dict
        required_fields: List of required field names
        _optional_fields: List of optional field names (for warnings, not yet implemented)

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    if required_fields:
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")

    # Note: _optional_fields parameter reserved for future warning generation
    # Currently not implemented to keep function minimal

    return errors


def has_frontmatter(file_path: Path) -> bool:
    """Check if file has YAML frontmatter.

    Args:
        file_path: Path to markdown file

    Returns:
        True if file starts with '---', False otherwise
    """
    try:
        with open(file_path) as f:
            return f.read(3) == "---"
    except OSError:
        return False
