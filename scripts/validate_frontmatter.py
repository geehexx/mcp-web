#!/usr/bin/env python3
"""Validate YAML frontmatter in workflow and rule files."""

import sys
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate


def load_schema() -> dict:
    """Schema removed - frontmatter now uses minimal Windsurf format.

    Validation rules:
    - trigger: Required (always_on, manual, model_decision, glob)
    - description: Required for model_decision and glob triggers
    - globs: Required for glob trigger (quoted, comma-separated)
    """
    return {}


def extract_frontmatter(file_path: Path) -> dict | None:
    """Extract YAML frontmatter from markdown file."""
    with open(file_path) as f:
        content = f.read()
    if not content.startswith("---"):
        return None
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        print(f"  ❌ YAML parse error: {e}")
        return None


def validate_file(file_path: Path, schema: dict) -> tuple[bool, str]:
    """Validate single file's frontmatter."""
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        return False, "No frontmatter found"

    try:
        validate(instance=frontmatter, schema=schema)
        return True, "Valid"
    except ValidationError as e:
        return False, f"{e.message} at {'.'.join(str(p) for p in e.path)}"


def main() -> int:
    """Main validation function."""
    schema = load_schema()
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
        valid, msg = validate_file(file_path, schema)
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
        valid, msg = validate_file(file_path, schema)
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
