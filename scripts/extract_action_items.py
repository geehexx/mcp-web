#!/usr/bin/env python3
"""Extract action items from session summaries using MCP server.

This script demonstrates Phase 1 of the Session Summary Mining initiative:
- Uses MCP server's file:// URL support for local file summarization
- Processes session summaries from docs/archive/session-summaries/
- Generates focused summaries extracting action items

Usage:
    # Extract from single file
    python scripts/extract_action_items.py docs/archive/session-summaries/2025-10-20-*.md

    # Extract from date range
    python scripts/extract_action_items.py --date-range 2025-10-15:2025-10-19

    # Extract from all summaries
    python scripts/extract_action_items.py --all

    # Save to file
    python scripts/extract_action_items.py --all --output action-items.md
"""

import argparse
import asyncio
import sys
from datetime import date, datetime
from pathlib import Path

from mcp_web.config import Config
from mcp_web.mcp_server import WebSummarizationPipeline


async def extract_action_items_from_file(
    pipeline: WebSummarizationPipeline,
    file_path: Path,
) -> str:
    """Extract action items from a single session summary.

    Args:
        pipeline: Configured MCP pipeline
        file_path: Path to session summary file

    Returns:
        Extracted action items summary
    """
    # Convert to file:// URL
    file_url = f"file://{file_path.absolute()}"

    # Focused query for action item extraction
    query = """Extract all action items, next steps, and unresolved issues from this session summary.
    Focus on:
    - Uncompleted tasks ([ ] checkboxes)
    - "Next Steps" section
    - "Unresolved Issues" or "Blockers" sections
    - Any TODOs or deferred work

    Format as:
    - **[Category]**: Action item description
    """

    # Collect summary chunks
    chunks: list[str] = []
    async for chunk in pipeline.summarize_urls([file_url], query=query):
        chunks.append(chunk)

    return "".join(chunks)


async def process_summaries(
    file_paths: list[Path],
    output_file: Path | None = None,
) -> None:
    """Process multiple session summaries and extract action items.

    Args:
        file_paths: List of session summary files to process
        output_file: Optional output file for results
    """
    # Configure MCP pipeline
    config = Config()
    config.fetcher.enable_file_system = True
    config.fetcher.allowed_directories = [
        "docs/archive/session-summaries",
        str(Path.cwd() / "docs" / "archive" / "session-summaries"),
    ]

    # Disable streaming for cleaner output
    config.summarizer.streaming = False

    pipeline = WebSummarizationPipeline(config)

    # Output header
    output_lines = [
        "# Extracted Action Items\n",
        f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"**Source Files:** {len(file_paths)}\n",
        "\n---\n\n",
    ]

    print("🔍 Extracting action items from session summaries...\n")

    # Process each file
    for i, file_path in enumerate(file_paths, 1):
        print(f"[{i}/{len(file_paths)}] Processing: {file_path.name}")

        try:
            result = await extract_action_items_from_file(pipeline, file_path)

            # Add to output
            output_lines.append(f"## {file_path.stem}\n\n")
            output_lines.append(f"**File:** `{file_path.name}`\n\n")
            output_lines.append(result)
            output_lines.append("\n\n---\n\n")

        except Exception as e:
            error_msg = f"**Error processing {file_path.name}:** {str(e)}\n\n"
            output_lines.append(error_msg)
            print(f"   ❌ Error: {str(e)}")
            continue

    # Write output
    output_text = "".join(output_lines)

    if output_file:
        output_file.write_text(output_text)
        print(f"\n✅ Extracted action items written to: {output_file}")
    else:
        print("\n" + "=" * 80 + "\n")
        print(output_text)


def find_summaries_by_date_range(start_date: date, end_date: date) -> list[Path]:
    """Find session summaries within date range.

    Args:
        start_date: Start date (inclusive)
        end_date: End date (inclusive)

    Returns:
        List of matching session summary files
    """
    summaries_dir = Path("docs/archive/session-summaries")
    if not summaries_dir.exists():
        print(f"❌ Error: Directory not found: {summaries_dir}")
        return []

    matching_files: list[Path] = []

    for file_path in summaries_dir.glob("*.md"):
        # Parse date from filename (format: YYYY-MM-DD-*.md)
        try:
            date_str = file_path.name[:10]  # Extract YYYY-MM-DD
            file_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            if start_date <= file_date <= end_date:
                matching_files.append(file_path)
        except ValueError:
            # Skip files that don't match date format
            continue

    return sorted(matching_files)


def parse_date_range(date_range_str: str) -> tuple[date, date]:
    """Parse date range string.

    Args:
        date_range_str: Date range in format "YYYY-MM-DD:YYYY-MM-DD"

    Returns:
        Tuple of (start_date, end_date)

    Raises:
        ValueError: If format is invalid
    """
    try:
        start_str, end_str = date_range_str.split(":")
        start_date = datetime.strptime(start_str.strip(), "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str.strip(), "%Y-%m-%d").date()

        if start_date > end_date:
            raise ValueError("Start date must be before end date")

        return start_date, end_date
    except Exception as e:
        raise ValueError("Invalid date range format. Use YYYY-MM-DD:YYYY-MM-DD") from e


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract action items from session summaries using MCP server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single file
  python scripts/extract_action_items.py docs/archive/session-summaries/2025-10-20-*.md

  # Date range
  python scripts/extract_action_items.py --date-range 2025-10-15:2025-10-19

  # All summaries
  python scripts/extract_action_items.py --all --output action-items.md
        """,
    )

    parser.add_argument(
        "files",
        nargs="*",
        help="Session summary files to process",
    )

    parser.add_argument(
        "--date-range",
        help="Extract from date range (format: YYYY-MM-DD:YYYY-MM-DD)",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all session summaries",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="Output file for extracted action items",
    )

    args = parser.parse_args()

    # Determine which files to process
    file_paths: list[Path] = []

    if args.all:
        summaries_dir = Path("docs/archive/session-summaries")
        if summaries_dir.exists():
            file_paths = sorted(summaries_dir.glob("*.md"))
        else:
            print(f"❌ Error: Directory not found: {summaries_dir}")
            return 1

    elif args.date_range:
        try:
            start_date, end_date = parse_date_range(args.date_range)
            print(f"📅 Searching for summaries from {start_date} to {end_date}")
            file_paths = find_summaries_by_date_range(start_date, end_date)

            if not file_paths:
                print("❌ No session summaries found in date range")
                return 1

            print(f"✅ Found {len(file_paths)} summaries")

        except ValueError as e:
            print(f"❌ Error: {e}")
            return 1

    elif args.files:
        for file_arg in args.files:
            path = Path(file_arg)
            if path.exists():
                file_paths.append(path)
            else:
                print(f"⚠️  Warning: File not found: {file_arg}")

    else:
        parser.print_help()
        return 1

    if not file_paths:
        print("❌ No valid files to process")
        return 1

    # Process summaries
    asyncio.run(process_summaries(file_paths, args.output))

    return 0


if __name__ == "__main__":
    sys.exit(main())
