#!/usr/bin/env python3
"""Test trigger consistency between Windsurf and Cursor configurations."""

import sys
from pathlib import Path

# Add the adapters module to the path
sys.path.insert(0, str(Path(__file__).parent))

from adapters import CursorAdapter, UnifiedParser, WindsurfAdapter


def test_trigger_consistency():
    """Test that Windsurf and Cursor triggers are consistent."""
    project_root = Path(__file__).parent.parent
    unified_dir = project_root / ".unified"

    parser = UnifiedParser()
    cursor_adapter = CursorAdapter()
    windsurf_adapter = WindsurfAdapter()

    # Get all rule files
    rule_files = parser.list_unified_files(str(unified_dir / "rules"), "rule")

    errors = []

    for rule_file in rule_files:
        try:
            # Parse unified rule
            unified_data = parser.parse_rule(rule_file)
            frontmatter = unified_data["frontmatter"]

            # Get configurations
            windsurf_config = frontmatter.get("windsurf", {})
            cursor_config = frontmatter.get("cursor", {})

            windsurf_trigger = windsurf_config.get("trigger")
            cursor_always_apply = cursor_config.get("alwaysApply")
            cursor_globs = cursor_config.get("globs")

            # Check consistency
            if windsurf_trigger == "always_on" and cursor_always_apply != True:
                errors.append(
                    f"{rule_file}: Windsurf 'always_on' should map to Cursor 'alwaysApply: true'"
                )

            if windsurf_trigger == "glob" and cursor_always_apply != False:
                errors.append(
                    f"{rule_file}: Windsurf 'glob' should map to Cursor 'alwaysApply: false'"
                )

            if windsurf_trigger == "model_decision" and cursor_always_apply != False:
                errors.append(
                    f"{rule_file}: Windsurf 'model_decision' should map to Cursor 'alwaysApply: false'"
                )

            if windsurf_trigger == "model_decision" and cursor_globs is not None:
                errors.append(
                    f"{rule_file}: Windsurf 'model_decision' should not have globs in Cursor config"
                )

            if windsurf_trigger == "manual" and cursor_always_apply != False:
                errors.append(
                    f"{rule_file}: Windsurf 'manual' should map to Cursor 'alwaysApply: false'"
                )

            if windsurf_trigger == "manual" and cursor_globs is not None:
                errors.append(
                    f"{rule_file}: Windsurf 'manual' should not have globs in Cursor config"
                )

        except Exception as e:
            errors.append(f"{rule_file}: Error parsing rule - {e}")

    if errors:
        print("❌ Trigger consistency validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Trigger consistency validation passed")
        return True


def test_transformation_consistency():
    """Test that transformations produce consistent results."""
    project_root = Path(__file__).parent.parent
    unified_dir = project_root / ".unified"

    parser = UnifiedParser()
    cursor_adapter = CursorAdapter()
    windsurf_adapter = WindsurfAdapter()

    # Get all rule files
    rule_files = parser.list_unified_files(str(unified_dir / "rules"), "rule")

    errors = []

    for rule_file in rule_files:
        try:
            # Parse unified rule
            unified_data = parser.parse_rule(rule_file)

            # Transform to both formats
            cursor_data = cursor_adapter.transform_rule(unified_data)
            windsurf_data = windsurf_adapter.transform_rule(unified_data)

            # Check that content is preserved
            if unified_data["content"] != cursor_data["content"]:
                errors.append(f"{rule_file}: Content not preserved in Cursor transformation")

            if unified_data["content"] != windsurf_data["content"]:
                errors.append(f"{rule_file}: Content not preserved in Windsurf transformation")

            # Check that title is preserved
            unified_title = unified_data["frontmatter"].get("title", "")
            cursor_title = cursor_data["frontmatter"].get("title", "")
            windsurf_title = windsurf_data["frontmatter"].get("title", "")

            if unified_title and unified_title != cursor_title:
                errors.append(f"{rule_file}: Title not preserved in Cursor transformation")

            if unified_title and unified_title != windsurf_title:
                errors.append(f"{rule_file}: Title not preserved in Windsurf transformation")

        except Exception as e:
            errors.append(f"{rule_file}: Error transforming rule - {e}")

    if errors:
        print("❌ Transformation consistency validation failed:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Transformation consistency validation passed")
        return True


def main():
    """Run all consistency tests."""
    print("🔍 Running trigger consistency validation...")
    trigger_ok = test_trigger_consistency()

    print("\n🔍 Running transformation consistency validation...")
    transform_ok = test_transformation_consistency()

    if trigger_ok and transform_ok:
        print("\n🎉 All consistency validations passed!")
        return 0
    else:
        print("\n💥 Some consistency validations failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
