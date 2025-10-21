#!/usr/bin/env python3
"""Validate Windsurf rules front-matter.

Ensures all .windsurf/rules/*.md files have valid trigger types.

Valid trigger types (per Windsurf documentation):
- always_on: Rule always applied
- model_decision: Model decides based on description (requires description field)
- glob: Applied to files matching patterns (requires globs field as YAML array)

Reference: https://docs.windsurf.com/windsurf/cascade/memories
"""

import sys
from pathlib import Path

import yaml

VALID_TRIGGERS = {"always_on", "model_decision", "glob"}
RULES_DIR = Path(".windsurf/rules")


def validate_rule_file(file_path: Path) -> list[str]:
    """Validate a single rule file's front-matter.

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

        # Windsurf accepts unquoted globs, but YAML doesn't
        # Parse with lenient handling for glob lines
        frontmatter = {}
        for line in yaml_content.strip().split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                # For globs, accept unquoted format (Windsurf-specific)
                if key == "globs":
                    frontmatter[key] = value  # Keep raw value
                else:
                    # Parse as YAML for other fields
                    try:
                        parsed = yaml.safe_load(f"{key}: {value}")
                        if parsed:
                            frontmatter.update(parsed)
                    except yaml.YAMLError:
                        # Fallback to raw string
                        frontmatter[key] = value
    except ValueError:
        return [f"{file_path}: Malformed YAML front-matter (missing closing ---)"]
    except Exception as e:
        return [f"{file_path}: Invalid front-matter: {e}"]

    if not isinstance(frontmatter, dict):
        return [f"{file_path}: Front-matter must be a YAML dictionary"]

    # Validate trigger field
    trigger = frontmatter.get("trigger")
    if not trigger:
        errors.append(f"{file_path}: Missing 'trigger' field")
    elif trigger not in VALID_TRIGGERS:
        errors.append(
            f"{file_path}: Invalid trigger '{trigger}'. "
            f"Must be one of: {', '.join(sorted(VALID_TRIGGERS))}"
        )

    # Validate trigger-specific requirements
    if trigger == "model_decision":
        if not frontmatter.get("description"):
            errors.append(f"{file_path}: 'model_decision' trigger requires 'description' field")
    elif trigger == "glob":
        globs = frontmatter.get("globs")
        if not globs:
            errors.append(f"{file_path}: 'glob' trigger requires 'globs' field")
        # Accept both YAML array and comma-separated string
        elif not isinstance(globs, list | str):
            errors.append(f"{file_path}: 'globs' field must be a list or string")

    # Validate created/updated fields (recommended but not required)
    created = frontmatter.get("created")
    updated = frontmatter.get("updated")
    if created and not isinstance(created, str):
        errors.append(f"{file_path}: 'created' field must be a string (YYYY-MM-DD format)")
    if updated and not isinstance(updated, str):
        errors.append(f"{file_path}: 'updated' field must be a string (YYYY-MM-DD format)")

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
        print(f"\n📖 Valid trigger types: {', '.join(sorted(VALID_TRIGGERS))}")
        print("📚 Reference: https://docs.windsurf.com/windsurf/cascade/memories")
        return 1

    print(f"✅ All {len(rule_files)} rule files have valid front-matter")
    return 0


if __name__ == "__main__":
    sys.exit(main())
