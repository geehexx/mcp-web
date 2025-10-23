#!/usr/bin/env python3
"""Build IDE-specific configs from unified source."""

import argparse
import sys
from pathlib import Path
from typing import Any

# Add the adapters module to the path
sys.path.insert(0, str(Path(__file__).parent))

from adapters import CursorAdapter, UnifiedParser, Validator, WindsurfAdapter


def build_configs(
    cursor_only: bool = False, windsurf_only: bool = False, verbose: bool = False
) -> bool:
    """Main build function.

    Args:
        cursor_only: Only build Cursor configs
        windsurf_only: Only build Windsurf configs
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    project_root = Path(__file__).parent.parent
    unified_dir = project_root / ".unified"

    if not unified_dir.exists():
        print(f"Error: Unified directory not found: {unified_dir}")
        return False

    # Initialize components
    parser = UnifiedParser()
    cursor_adapter = CursorAdapter()
    windsurf_adapter = WindsurfAdapter()
    validator = Validator()

    success = True
    stats = {
        "rules_processed": 0,
        "commands_processed": 0,
        "cursor_rules_generated": 0,
        "cursor_commands_generated": 0,
        "windsurf_rules_generated": 0,
        "windsurf_workflows_generated": 0,
        "errors": [],
    }

    print("🔄 Building IDE configurations from unified source...")

    # Process rules
    if not cursor_only:
        print("\n📋 Processing rules...")
        success &= process_rules(
            unified_dir, parser, cursor_adapter, windsurf_adapter, validator, stats, verbose
        )

    # Process commands
    if not windsurf_only:
        print("\n📋 Processing commands...")
        success &= process_commands(
            unified_dir, parser, cursor_adapter, windsurf_adapter, validator, stats, verbose
        )

    # Print summary
    print_summary(stats, success)

    return success


def process_rules(
    unified_dir: Path,
    parser: UnifiedParser,
    cursor_adapter: CursorAdapter,
    windsurf_adapter: WindsurfAdapter,
    validator: Validator,
    stats: dict[str, Any],
    verbose: bool,
) -> bool:
    """Process unified rules and generate IDE-specific configs.

    Args:
        unified_dir: Path to unified directory
        parser: Unified parser instance
        cursor_adapter: Cursor adapter instance
        windsurf_adapter: Windsurf adapter instance
        validator: Validator instance
        stats: Statistics dictionary
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    rules_dir = unified_dir / "rules"
    if not rules_dir.exists():
        print(f"Warning: Rules directory not found: {rules_dir}")
        return True

    # Get list of rule files
    rule_files = parser.list_unified_files(str(rules_dir), "rule")

    if not rule_files:
        print("No rule files found")
        return True

    print(f"Found {len(rule_files)} rule files")

    # Create output directories
    project_root = Path(__file__).parent.parent
    cursor_rules_dir = project_root / ".cursor" / "rules"
    windsurf_rules_dir = project_root / ".windsurf" / "rules"

    cursor_rules_dir.mkdir(parents=True, exist_ok=True)
    windsurf_rules_dir.mkdir(parents=True, exist_ok=True)

    success = True

    for rule_file in rule_files:
        try:
            if verbose:
                print(f"  Processing rule: {Path(rule_file).name}")

            # Parse unified rule
            unified_data = parser.parse_rule(rule_file)
            stats["rules_processed"] += 1

            # Transform to Cursor format
            cursor_data = cursor_adapter.transform_rule(unified_data)

            # Validate Cursor rule
            is_valid, errors = validator.validate_cursor_rule(cursor_data)
            if not is_valid:
                print(f"    ❌ Cursor validation failed: {errors}")
                stats["errors"].extend(errors)
                success = False
                continue

            # Generate Cursor .mdc file
            cursor_output = cursor_rules_dir / f"{cursor_data['file_name']}.mdc"
            cursor_adapter.generate_mdc_file(cursor_data, str(cursor_output))
            stats["cursor_rules_generated"] += 1

            if verbose:
                print(f"    ✅ Generated Cursor rule: {cursor_output.name}")

            # Transform to Windsurf format
            windsurf_data = windsurf_adapter.transform_rule(unified_data)

            # Validate Windsurf rule
            is_valid, errors = validator.validate_windsurf_rule(windsurf_data)
            if not is_valid:
                print(f"    ❌ Windsurf validation failed: {errors}")
                stats["errors"].extend(errors)
                success = False
                continue

            # Generate Windsurf .md file
            windsurf_output = windsurf_rules_dir / f"{windsurf_data['file_name']}.md"
            windsurf_adapter.generate_rule_file(windsurf_data, str(windsurf_output))
            stats["windsurf_rules_generated"] += 1

            if verbose:
                print(f"    ✅ Generated Windsurf rule: {windsurf_output.name}")

            # Validate transformation consistency
            is_consistent, errors = validator.validate_transformation_consistency(
                unified_data, cursor_data, windsurf_data
            )
            if not is_consistent:
                print(f"    ⚠️  Transformation consistency issues: {errors}")
                stats["errors"].extend(errors)

        except Exception as e:
            print(f"    ❌ Error processing rule {rule_file}: {e}")
            stats["errors"].append(str(e))
            success = False

    return success


def process_commands(
    unified_dir: Path,
    parser: UnifiedParser,
    cursor_adapter: CursorAdapter,
    windsurf_adapter: WindsurfAdapter,
    validator: Validator,
    stats: dict[str, Any],
    verbose: bool,
) -> bool:
    """Process unified commands and generate IDE-specific configs.

    Args:
        unified_dir: Path to unified directory
        parser: Unified parser instance
        cursor_adapter: Cursor adapter instance
        windsurf_adapter: Windsurf adapter instance
        validator: Validator instance
        stats: Statistics dictionary
        verbose: Enable verbose output

    Returns:
        True if successful, False otherwise
    """
    commands_dir = unified_dir / "commands"
    if not commands_dir.exists():
        print(f"Warning: Commands directory not found: {commands_dir}")
        return True

    # Get list of command files
    command_files = parser.list_unified_files(str(commands_dir), "command")

    if not command_files:
        print("No command files found")
        return True

    print(f"Found {len(command_files)} command files")

    # Create output directories
    project_root = Path(__file__).parent.parent
    cursor_commands_dir = project_root / ".cursor" / "commands"
    windsurf_workflows_dir = project_root / ".windsurf" / "workflows"

    cursor_commands_dir.mkdir(parents=True, exist_ok=True)
    windsurf_workflows_dir.mkdir(parents=True, exist_ok=True)

    success = True

    for command_file in command_files:
        try:
            if verbose:
                print(f"  Processing command: {Path(command_file).name}")

            # Parse unified command
            unified_data = parser.parse_command(command_file)
            stats["commands_processed"] += 1

            # Transform to Cursor format
            cursor_data = cursor_adapter.transform_command(unified_data)

            # Validate Cursor command
            is_valid, errors = validator.validate_cursor_command(cursor_data)
            if not is_valid:
                print(f"    ❌ Cursor validation failed: {errors}")
                stats["errors"].extend(errors)
                success = False
                continue

            # Generate Cursor command file
            cursor_output = cursor_commands_dir / f"{cursor_data['file_name']}.md"
            cursor_adapter.generate_command_file(cursor_data, str(cursor_output))
            stats["cursor_commands_generated"] += 1

            if verbose:
                print(f"    ✅ Generated Cursor command: {cursor_output.name}")

            # Transform to Windsurf format
            windsurf_data = windsurf_adapter.transform_workflow(unified_data)

            # Validate Windsurf workflow
            is_valid, errors = validator.validate_windsurf_workflow(windsurf_data)
            if not is_valid:
                print(f"    ❌ Windsurf validation failed: {errors}")
                stats["errors"].extend(errors)
                success = False
                continue

            # Generate Windsurf workflow file
            windsurf_output = windsurf_workflows_dir / f"{windsurf_data['file_name']}.md"
            windsurf_adapter.generate_workflow_file(windsurf_data, str(windsurf_output))
            stats["windsurf_workflows_generated"] += 1

            if verbose:
                print(f"    ✅ Generated Windsurf workflow: {windsurf_output.name}")

            # Validate transformation consistency
            is_consistent, errors = validator.validate_transformation_consistency(
                unified_data, cursor_data, windsurf_data
            )
            if not is_consistent:
                print(f"    ⚠️  Transformation consistency issues: {errors}")
                stats["errors"].extend(errors)

        except Exception as e:
            print(f"    ❌ Error processing command {command_file}: {e}")
            stats["errors"].append(str(e))
            success = False

    return success


def print_summary(stats: dict[str, Any], success: bool) -> None:
    """Print build summary.

    Args:
        stats: Statistics dictionary
        success: Whether build was successful
    """
    print("\n" + "=" * 60)
    print("📊 BUILD SUMMARY")
    print("=" * 60)

    print(f"Rules processed: {stats['rules_processed']}")
    print(f"Commands processed: {stats['commands_processed']}")
    print(f"Cursor rules generated: {stats['cursor_rules_generated']}")
    print(f"Cursor commands generated: {stats['cursor_commands_generated']}")
    print(f"Windsurf rules generated: {stats['windsurf_rules_generated']}")
    print(f"Windsurf workflows generated: {stats['windsurf_workflows_generated']}")

    if stats["errors"]:
        print(f"\n❌ Errors encountered: {len(stats['errors'])}")
        for error in stats["errors"]:
            print(f"  - {error}")
    else:
        print("\n✅ No errors encountered")

    if success:
        print("\n🎉 Build completed successfully!")
    else:
        print("\n💥 Build completed with errors")

    print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Build IDE-specific configs from unified source")
    parser.add_argument("--cursor-only", action="store_true", help="Only build Cursor configs")
    parser.add_argument("--windsurf-only", action="store_true", help="Only build Windsurf configs")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    if args.cursor_only and args.windsurf_only:
        print("Error: Cannot specify both --cursor-only and --windsurf-only")
        sys.exit(1)

    success = build_configs(
        cursor_only=args.cursor_only, windsurf_only=args.windsurf_only, verbose=args.verbose
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
