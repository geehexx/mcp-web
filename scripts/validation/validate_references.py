#!/usr/bin/env python3
"""Validate internal markdown links across documentation.

This script scans markdown files for internal links and validates:
- File existence (relative paths resolved correctly)
- Section anchors (if present)
- Reports broken links with file, line, and error details

Usage:
    python scripts/validate_references.py                    # Validate all docs
    python scripts/validate_references.py --dir docs/guides  # Validate specific dir
    python scripts/validate_references.py --ci               # CI mode (exit 1 on failures)

References:
    - Quality Automation Initiative (2025-10-19)
    - markdown-link-check (https://github.com/tcort/markdown-link-check)
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any

# Project root
ROOT = Path(__file__).parent.parent


def extract_markdown_links(text: str) -> list[dict[str, Any]]:
    """Extract internal markdown links from text.

    Args:
        text: Markdown content as string

    Returns:
        List of dicts with keys: text, url, line

    Ignores:
        - External URLs (http://, https://, mailto:)
        - Links inside code blocks
        - Placeholder links (path/to/...)
    """
    links = []
    in_code_block = False
    lines = text.split("\n")

    for line_num, line in enumerate(lines):
        # Track code block state
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Find markdown links: [text](url)
        for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
            link_text = match.group(1)
            link_url = match.group(2)

            # Skip external links
            if should_ignore_link(link_url):
                continue

            links.append({"text": link_text, "url": link_url, "line": line_num})

    return links


def should_ignore_link(url: str) -> bool:
    """Check if link should be ignored (external, placeholder, etc).

    Args:
        url: Link URL to check

    Returns:
        True if link should be ignored, False otherwise
    """
    # External URLs
    if url.startswith(("http://", "https://", "mailto:", "ftp://")):
        return True

    # Placeholder patterns
    if url.startswith(("path/to/", "relative/path/to")):
        return True

    # Same-file anchors (no validation needed here)
    return bool(url.startswith("#"))


def resolve_link_path(source_file: Path, link: str, root: Path) -> Path:
    """Resolve relative link to absolute path.

    Args:
        source_file: File containing the link
        link: Link URL (may include #anchor)
        root: Project root directory

    Returns:
        Resolved absolute path (anchor removed)
    """
    # Remove anchor fragment
    if "#" in link:
        link = link.split("#")[0]

    # Absolute from root (starts with /)
    if link.startswith("/"):
        return root / link.lstrip("/")

    # Relative to source file directory
    source_dir = source_file.parent
    return (source_dir / link).resolve()


def normalize_anchor(anchor: str) -> str:
    """Normalize anchor to markdown heading format.

    Args:
        anchor: Anchor string (e.g., "Section-One-Two")

    Returns:
        Normalized anchor (lowercase, hyphenated)
    """
    # Lowercase and keep hyphens
    normalized = anchor.lower()

    # Remove common special characters
    normalized = re.sub(r"[^\w\s-]", "", normalized)

    # Replace spaces with hyphens
    normalized = re.sub(r"\s+", "-", normalized)

    return normalized


def extract_heading_anchors(content: str) -> set[str]:
    """Extract all valid heading anchors from markdown content.

    Args:
        content: Markdown file content

    Returns:
        Set of normalized anchor strings
    """
    anchors = set()

    # Find all markdown headings (# Title, ## Subtitle, etc.)
    for match in re.finditer(r"^#{1,6}\s+(.+)$", content, re.MULTILINE):
        heading_text = match.group(1).strip()

        # Generate anchor from heading
        # GitHub/most parsers: lowercase, hyphens, remove special chars
        anchor = heading_text.lower()
        anchor = re.sub(r"[^\w\s-]", "", anchor)
        anchor = re.sub(r"\s+", "-", anchor)

        anchors.add(anchor)

    return anchors


def validate_anchor(content: str, anchor: str) -> bool:
    """Validate if anchor exists as a heading in content.

    Args:
        content: Markdown file content
        anchor: Anchor string to validate

    Returns:
        True if anchor exists, False otherwise
    """
    valid_anchors = extract_heading_anchors(content)
    normalized = normalize_anchor(anchor)

    return normalized in valid_anchors


def validate_link(source_file: Path, link: dict[str, Any], root: Path) -> dict[str, Any]:
    """Validate a single markdown link.

    Args:
        source_file: File containing the link
        link: Link dict with keys: text, url, line
        root: Project root directory

    Returns:
        Dict with keys: valid (bool), error (str or None)
    """
    url = link["url"]

    # Extract anchor if present
    anchor = None
    if "#" in url:
        url_parts = url.split("#")
        url = url_parts[0]
        anchor = url_parts[1] if len(url_parts) > 1 else None

    # Resolve file path
    if url:  # Not just an anchor
        resolved_path = resolve_link_path(source_file, url, root)

        # Check if file exists
        if not resolved_path.exists():
            return {
                "valid": False,
                "error": f"File does not exist: {resolved_path.relative_to(root)}",
            }
    else:
        # Just an anchor (same file)
        resolved_path = source_file

    # Validate anchor if present
    if anchor:
        content = resolved_path.read_text(encoding="utf-8", errors="ignore")
        if not validate_anchor(content, anchor):
            return {
                "valid": False,
                "error": f"Anchor #{anchor} not found in {resolved_path.name}",
            }

    return {"valid": True, "error": None}


def scan_markdown_files(directory: Path) -> list[Path]:
    """Scan directory recursively for markdown files.

    Args:
        directory: Directory to scan

    Returns:
        List of markdown file paths
    """
    return sorted(directory.rglob("*.md"))


def validate_directory(
    directory: Path, root: Path, exclude_patterns: list[str] | None = None
) -> list[dict[str, Any]]:
    """Validate all markdown files in directory.

    Args:
        directory: Directory to validate
        root: Project root directory
        exclude_patterns: Optional list of path patterns to exclude

    Returns:
        List of error dicts with keys: file, line, link, error
    """
    if exclude_patterns is None:
        exclude_patterns = []

    errors = []
    markdown_files = scan_markdown_files(directory)

    for file_path in markdown_files:
        # Check exclusion patterns
        if any(pattern in str(file_path) for pattern in exclude_patterns):
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        links = extract_markdown_links(content)

        for link in links:
            result = validate_link(file_path, link, root)

            if not result["valid"]:
                errors.append(
                    {
                        "file": str(file_path.relative_to(root)),
                        "line": link["line"] + 1,  # 1-indexed for humans
                        "link": link["url"],
                        "error": result["error"],
                    }
                )

    return errors


def generate_report(errors: list[dict[str, Any]]) -> str:
    """Generate human-readable error report.

    Args:
        errors: List of error dicts

    Returns:
        Formatted report string
    """
    if not errors:
        return "✅ No broken links found!"

    report = f"❌ Found {len(errors)} broken links:\n\n"

    for error in errors:
        report += f"  {error['file']}:{error['line']}\n"
        report += f"    Link: {error['link']}\n"
        report += f"    Error: {error['error']}\n\n"

    return report


def main() -> int:
    """Run link validation."""
    parser = argparse.ArgumentParser(description="Validate internal markdown links")
    parser.add_argument(
        "--dir",
        type=Path,
        default=ROOT / "docs",
        help="Directory to validate (default: docs/)",
    )
    parser.add_argument("--ci", action="store_true", help="CI mode: exit 1 on failures")
    parser.add_argument(
        "--exclude",
        nargs="+",
        default=["archive", "node_modules", ".venv", "template"],
        help="Patterns to exclude from validation",
    )

    args = parser.parse_args()

    print(f"🔍 Validating markdown links in {args.dir}...\n")

    # Also check root files
    root_files = [
        ROOT / "README.md",
        ROOT / "AGENTS.md",
        ROOT / "CONSTITUTION.md",
    ]

    all_errors = []

    # Validate directory
    errors = validate_directory(args.dir, ROOT, args.exclude)
    all_errors.extend(errors)

    # Validate root files
    for root_file in root_files:
        if root_file.exists():
            content = root_file.read_text(encoding="utf-8", errors="ignore")
            links = extract_markdown_links(content)

            for link in links:
                result = validate_link(root_file, link, ROOT)

                if not result["valid"]:
                    all_errors.append(
                        {
                            "file": str(root_file.relative_to(ROOT)),
                            "line": link["line"] + 1,
                            "link": link["url"],
                            "error": result["error"],
                        }
                    )

    # Generate report
    report = generate_report(all_errors)
    print(report)

    # Exit code
    if all_errors and args.ci:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
