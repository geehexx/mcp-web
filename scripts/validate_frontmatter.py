#!/usr/bin/env python3
"""
Validate YAML frontmatter in workflow and rule files.

Updated 2025-10-20: Validates minimal Windsurf-compatible format.
See: .windsurf/docs/frontmatter-specification.md
"""

import sys
from pathlib import Path

import yaml


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


def validate_minimal_format(frontmatter: dict) -> tuple[bool, str]:
    """
    Validate Windsurf-compatible minimal frontmatter format.
    
    Required:
    - Must have 'description' field
    - Description must be string
    - Description must not contain apostrophes (causes YAML parse issues)
    - Description should be <= 200 characters
    """
    # Check required field
    if "description" not in frontmatter:
        return False, "Missing required field: description"
    
    description = frontmatter["description"]
    
    # Check type
    if not isinstance(description, str):
        return False, f"description must be string, got {type(description).__name__}"
    
    # Check for problematic characters
    if "'" in description or '"' in description:
        return False, "description contains apostrophes or quotes (not Windsurf-compatible)"
    
    # Check length
    if len(description) > 200:
        return False, f"description too long ({len(description)} chars, max 200)"
    
    # Warn about extra fields (not an error, just informational)
    extra_fields = set(frontmatter.keys()) - {"description"}
    if extra_fields:
        return True, f"Valid (note: extra fields ignored by Windsurf: {', '.join(extra_fields)})"
    
    return True, "Valid"


def validate_file(file_path: Path) -> tuple[bool, str]:
    """Validate single file's frontmatter."""
    frontmatter = extract_frontmatter(file_path)
    if not frontmatter:
        return False, "No frontmatter found"
    
    return validate_minimal_format(frontmatter)


def main() -> int:
    """Main validation function."""
    workflow_dir = Path(".windsurf/workflows")
    rules_dir = Path(".windsurf/rules")

    errors = []
    warnings = []
    valid_count = 0
    total_count = 0

    print("🔍 Validating YAML frontmatter (Windsurf minimal format)...")
    print("   Spec: .windsurf/docs/frontmatter-specification.md")
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
            if "extra fields" in msg.lower():
                warnings.append(f"{file_path.name}: {msg}")
                print(f"  ⚠️  {file_path.name}: {msg}")
            else:
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
            if "extra fields" in msg.lower():
                warnings.append(f"{file_path.name}: {msg}")
                print(f"  ⚠️  {file_path.name}: {msg}")
            else:
                print(f"  ✅ {file_path.name}")
        else:
            errors.append(f"{file_path}: {msg}")
            print(f"  ❌ {file_path.name}: {msg}")

    print()
    print(f"**Summary:** {valid_count}/{total_count} files valid")
    
    if warnings:
        print(f"**Warnings:** {len(warnings)} files with extra fields (will be ignored by Windsurf)")

    if errors:
        print()
        print("**Validation errors:**")
        for error in errors:
            print(f"  - {error}")
        return 1
    else:
        print("✅ All frontmatter valid and Windsurf-compatible")
        return 0


if __name__ == "__main__":
    sys.exit(main())
