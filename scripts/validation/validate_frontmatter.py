#!/usr/bin/env python3
"""Validate YAML frontmatter in workflow and rule files."""

import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.lib.frontmatter import extract_frontmatter


def validate_file(file_path: Path) -> tuple[bool, str]:
    """Validate single file's frontmatter.

    Args:
        file_path: Path to markdown file

    Returns:
        Tuple of (is_valid, message)
    """
    frontmatter = extract_frontmatter(file_path, strict=False)
    if not frontmatter:
        return False, "No frontmatter found"
    return True, "Valid"


def main() -> int:
    """Main validation function.

    Returns:
        Exit code (0 = success, 1 = errors found)
    """
    workflow_dir = Path(".windsurf/workflows")
    rules_dir = Path(".windsurf/rules")

    errors = []
    valid_count = 0
    total_count = 0

    print("🔍 Validating YAML frontmatter...")
    print()

    # Validate workflows
    print("**Workflows:**")
    for file_path in sorted(workflow_dir.glob("*.md")):
        # Skip generated files
        if file_path.name in ("INDEX.md", "DEPENDENCIES.md"):
            continue
        total_count += 1
        valid, msg = validate_file(file_path)
        if valid:
            valid_count += 1
            print(f"  ✅ {file_path.name}")
        else:
            errors.append(f"{file_path}: {msg}")
            print(f"  ❌ {file_path.name}: {msg}")

    print()

    # Validate rules
    print("**Rules:**")
    for file_path in sorted(rules_dir.glob("*.md")):
        # Skip generated files
        if file_path.name in ("INDEX.md",):
            continue
        total_count += 1
        valid, msg = validate_file(file_path)
        if valid:
            valid_count += 1
            print(f"  ✅ {file_path.name}")
        else:
            errors.append(f"{file_path}: {msg}")
            print(f"  ❌ {file_path.name}: {msg}")

    print()
    print(f"**Summary:** {valid_count}/{total_count} files valid")

    if errors:
        print()
        print("**Validation errors:**")
        for error in errors:
            print(f"  - {error}")
        return 1
    else:
        print("✅ All frontmatter valid")
        return 0


if __name__ == "__main__":
    sys.exit(main())
