"""Test ADR (Architecture Decision Record) validation.

This module provides automated tests for ADR quality and uniqueness to prevent
duplicate ADR numbers and ensure consistency.

Categories:
- Duplicate number detection
- Filename format validation
- Sequential numbering verification
"""

import re
from collections import Counter
from pathlib import Path

import pytest


def get_adr_files() -> list[Path]:
    """Get all ADR files excluding README and template."""
    adr_dir = Path("docs/adr")
    return [f for f in adr_dir.glob("*.md") if f.name not in ["README.md", "template.md"]]


def extract_adr_number(filename: str) -> int | None:
    """Extract ADR number from filename (e.g., '0019' from '0019-title.md').

    Args:
        filename: ADR filename

    Returns:
        ADR number as integer, or None if not a valid ADR filename
    """
    match = re.match(r"^(\d{4})-", filename)
    return int(match.group(1)) if match else None


@pytest.mark.unit
def test_adr_files_exist() -> None:
    """Verify we have ADR files to test."""
    files = get_adr_files()
    assert len(files) > 0, "No ADR files found to test"
    assert len(files) >= 10, f"Expected at least 10 ADR files, found {len(files)}"


@pytest.mark.unit
def test_no_duplicate_adr_numbers() -> None:
    """Verify all ADR numbers are unique (prevent ADR-0019 duplicate issue).

    This test ensures that each ADR number is used exactly once.
    Duplicate ADR numbers cause confusion and break the sequential numbering system.

    Example violation:
        - 0019-initiative-folder-structure.md
        - 0019-prompt-injection-detection.md  # DUPLICATE!

    Reference: GitHub issue where duplicate ADR-0019 was created.
    """
    files = get_adr_files()
    adr_numbers = []
    adr_mapping = {}  # number -> list of filenames

    for f in files:
        number = extract_adr_number(f.name)
        if number is not None:
            adr_numbers.append(number)
            if number not in adr_mapping:
                adr_mapping[number] = []
            adr_mapping[number].append(f.name)

    # Count occurrences
    counter = Counter(adr_numbers)
    duplicates = {num: count for num, count in counter.items() if count > 1}

    if duplicates:
        error_msg = "Duplicate ADR numbers found:\n"
        for num, count in duplicates.items():
            error_msg += f"  ADR-{num:04d} appears {count} times:\n"
            for filename in adr_mapping[num]:
                error_msg += f"    - {filename}\n"
        error_msg += (
            "\nFix: Renumber duplicate ADRs to the next available number and update all references."
        )
        pytest.fail(error_msg)


@pytest.mark.unit
def test_adr_filename_format() -> None:
    """Verify all ADR filenames follow the correct format: NNNN-title-with-hyphens.md."""
    files = get_adr_files()
    invalid_files = []

    for f in files:
        # Must match: 4 digits + hyphen + lowercase-with-hyphens + .md
        if not re.match(r"^\d{4}-[a-z0-9-]+\.md$", f.name):
            invalid_files.append(f.name)

    if invalid_files:
        error_msg = (
            "ADR files with invalid naming format:\n"
            + "\n".join(f"  - {name}" for name in invalid_files)
            + "\n\nExpected format: NNNN-lowercase-with-hyphens.md"
        )
        pytest.fail(error_msg)


@pytest.mark.unit
def test_adr_numbers_are_four_digits() -> None:
    """Verify all ADR numbers are zero-padded to 4 digits (e.g., 0001, not 1)."""
    files = get_adr_files()
    invalid_files = []

    for f in files:
        match = re.match(r"^(\d+)-", f.name)
        if match and len(match.group(1)) != 4:
            invalid_files.append(f.name)

    if invalid_files:
        error_msg = (
            "ADR files with incorrect number padding:\n"
            + "\n".join(f"  - {name}" for name in invalid_files)
            + "\n\nExpected: 4-digit zero-padded numbers (e.g., 0001, 0023)"
        )
        pytest.fail(error_msg)


@pytest.mark.unit
def test_find_next_available_adr_number() -> None:
    """Helper test: Display the next available ADR number.

    This is not a validation test, but a utility to help developers
    find the next ADR number when creating new ADRs.
    """
    files = get_adr_files()
    adr_numbers = [extract_adr_number(f.name) for f in files if extract_adr_number(f.name)]

    if not adr_numbers:
        next_number = 1
    else:
        next_number = max(adr_numbers) + 1

    # This test always passes but prints useful info
    print(f"\n📋 Next available ADR number: {next_number:04d}")
    print(f"   Usage: docs/adr/{next_number:04d}-your-decision-title.md")

    # Verify the number we suggest is actually available
    assert next_number not in adr_numbers, (
        f"Next suggested number {next_number:04d} is already in use!"
    )
