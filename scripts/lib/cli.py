"""Common CLI utilities for scripts.

This module provides shared argparse patterns and exit handling utilities
used across multiple scripts.

Usage:
    from scripts.lib.cli import create_parser, add_common_args

    parser = create_parser("My script description")
    add_common_args(parser)
    parser.add_argument("--specific", help="Script-specific arg")
    args = parser.parse_args()
"""

import argparse
import sys


def create_parser(description: str, epilog: str | None = None) -> argparse.ArgumentParser:
    """Create ArgumentParser with consistent formatting.

    Args:
        description: Script description
        epilog: Optional epilog text

    Returns:
        Configured ArgumentParser
    """
    return argparse.ArgumentParser(
        description=description, epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter
    )


def add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add common arguments to parser.

    Adds:
        --verbose: Enable verbose output
        --dry-run: Dry run mode (show what would be done)

    Args:
        parser: ArgumentParser to modify
    """
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run mode - show what would be done without making changes",
    )


def handle_exit(errors: list[str], success_msg: str | None = None) -> int:
    """Handle script exit based on errors.

    Args:
        errors: List of error messages
        success_msg: Optional success message to print if no errors

    Returns:
        Exit code (0 = success, 1 = errors)
    """
    if errors:
        print("\n❌ Validation failed with errors:", file=sys.stderr)
        for error in errors:
            print(f"  • {error}", file=sys.stderr)
        return 1
    else:
        if success_msg:
            print(f"\n✅ {success_msg}")
        return 0


def confirm_action(prompt: str, default: bool = False) -> bool:
    """Prompt user for yes/no confirmation.

    Args:
        prompt: Prompt message
        default: Default value if user presses Enter

    Returns:
        True if user confirms, False otherwise
    """
    suffix = " (Y/n): " if default else " (y/N): "
    response = input(prompt + suffix).strip().lower()

    if not response:
        return default

    return response in ("y", "yes")
