#!/usr/bin/env python3
"""
Validate Windsurf rules front-matter (minimal format).

UPDATED 2025-10-20: Validates minimal Windsurf-compatible format.
Activation modes (always_on, glob, model_decision) are now set via Windsurf UI, not frontmatter.

Required frontmatter:
- description: Brief summary (no apostrophes, max 200 chars)

Reference:
- https://docs.windsurf.com/windsurf/cascade/memories
- .windsurf/docs/frontmatter-specification.md
"""

import sys
from pathlib import Path

import yaml

RULES_DIR = Path(".windsurf/rules")


def validate_rule_file(file_path: Path) -> list[str]:
    """Validate a single rule file's front-matter (minimal format).

    Args:
        file_path: Path to the rule file

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Failed to read {file_path}: {e}"]

    # Extract YAML front-matter
    if not content.startswith("---\n"):
        return [f"{file_path}: Missing YAML front-matter"]

    try:
        # Find the closing ---
        end_idx = content.index("\n---\n", 4)
        yaml_content = content[4:end_idx]
        frontmatter = yaml.safe_load(yaml_content)
    except ValueError:
        return [f"{file_path}: Malformed YAML front-matter (missing closing ---)"]
    except yaml.YAMLError as e:
        return [f"{file_path}: Invalid YAML front-matter: {e}"]

    if not isinstance(frontmatter, dict):
        return [f"{file_path}: Front-matter must be a YAML dictionary"]

    # Validate required field: description
    description = frontmatter.get("description")
    if not description:
        errors.append(f"{file_path.name}: Missing required 'description' field")
    elif not isinstance(description, str):
        errors.append(f"{file_path.name}: 'description' must be a string")
    else:
        # Check for problematic characters
        if "'" in description or '"' in description:
            errors.append(f"{file_path.name}: 'description' contains apostrophes/quotes (not Windsurf-compatible)")
        # Check length
        if len(description) > 200:
            errors.append(f"{file_path.name}: 'description' too long ({len(description)} chars, max 200)")

    return errors


def main() -> int:
    """Validate all rule files in .windsurf/rules/.

    Returns:
        Exit code (0 = success, 1 = validation errors)
    """
    if not RULES_DIR.exists():
        print(f"✅ No rules directory found at {RULES_DIR}")
        return 0

    rule_files = list(RULES_DIR.glob("*.md"))
    if not rule_files:
        print(f"✅ No rule files found in {RULES_DIR}")
        return 0

    all_errors = []
    for rule_file in sorted(rule_files):
        errors = validate_rule_file(rule_file)
        all_errors.extend(errors)

    if all_errors:
        print("❌ Rules front-matter validation failed:\n")
        for error in all_errors:
            print(f"  • {error}")
        print("\n📖 Required format: minimal frontmatter with 'description' field only")
        print("📚 Reference: .windsurf/docs/frontmatter-specification.md")
        return 1

    print(f"✅ All {len(rule_files)} rule files have valid minimal front-matter")
    return 0


if __name__ == "__main__":
    sys.exit(main())
