#!/usr/bin/env python3
"""Documentation coverage analyzer for mcp-web.

Scans Python source files to calculate documentation coverage based on
docstrings for public classes, functions, and methods.

Usage:
    python scripts/doc_coverage.py [--threshold 80] [--output report.json]

Exit codes:
    0: Coverage meets threshold
    1: Coverage below threshold or error
"""

import argparse
import ast
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class DocCoverageStats:
    """Statistics for documentation coverage."""

    total_items: int = 0
    documented_items: int = 0
    undocumented: list[str] = field(default_factory=list)

    @property
    def coverage_percentage(self) -> float:
        """Calculate coverage percentage."""
        if self.total_items == 0:
            return 100.0
        return (self.documented_items / self.total_items) * 100


class DocCoverageAnalyzer(ast.NodeVisitor):
    """AST visitor to analyze documentation coverage."""

    def __init__(self, file_path: str):
        """Initialize analyzer.

        Args:
            file_path: Path to the file being analyzed
        """
        self.file_path = file_path
        self.stats = DocCoverageStats()
        self.current_class: str | None = None

    def is_public(self, name: str) -> bool:
        """Check if name is public (doesn't start with _).

        Args:
            name: Name to check

        Returns:
            True if public, False otherwise
        """
        return not name.startswith("_")

    def has_docstring(self, node: ast.FunctionDef | ast.ClassDef | ast.AsyncFunctionDef) -> bool:
        """Check if node has a docstring.

        Args:
            node: AST node to check

        Returns:
            True if has docstring, False otherwise
        """
        return ast.get_docstring(node) is not None and len(ast.get_docstring(node).strip()) > 0

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition.

        Args:
            node: Class definition node
        """
        if self.is_public(node.name):
            self.stats.total_items += 1
            if self.has_docstring(node):
                self.stats.documented_items += 1
            else:
                self.stats.undocumented.append(f"{self.file_path}::{node.name}")

            # Track current class for method names
            old_class = self.current_class
            self.current_class = node.name
            self.generic_visit(node)
            self.current_class = old_class
        else:
            self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition.

        Args:
            node: Function definition node
        """
        self._visit_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition.

        Args:
            node: Async function definition node
        """
        self._visit_function(node)

    def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
        """Visit function or async function definition.

        Args:
            node: Function definition node
        """
        # Skip private functions/methods
        if not self.is_public(node.name):
            self.generic_visit(node)
            return

        # Skip special methods (except __init__)
        if node.name.startswith("__") and node.name != "__init__":
            self.generic_visit(node)
            return

        self.stats.total_items += 1

        if self.has_docstring(node):
            self.stats.documented_items += 1
        else:
            if self.current_class:
                name = f"{self.file_path}::{self.current_class}.{node.name}"
            else:
                name = f"{self.file_path}::{node.name}"
            self.stats.undocumented.append(name)

        self.generic_visit(node)


def analyze_file(file_path: Path) -> DocCoverageStats:
    """Analyze documentation coverage for a single file.

    Args:
        file_path: Path to Python file

    Returns:
        Documentation coverage statistics
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=str(file_path))

        # Get relative path for display
        try:
            relative_path = file_path.absolute().relative_to(Path.cwd().absolute())
        except ValueError:
            relative_path = file_path

        analyzer = DocCoverageAnalyzer(str(relative_path))
        analyzer.visit(tree)
        return analyzer.stats
    except SyntaxError:
        print(f"⚠️  Skipping {file_path}: Syntax error", file=sys.stderr)
        return DocCoverageStats()
    except Exception as e:
        print(f"⚠️  Error analyzing {file_path}: {e}", file=sys.stderr)
        return DocCoverageStats()


def analyze_directory(
    directory: Path, exclude_patterns: list[str] | None = None
) -> DocCoverageStats:
    """Analyze documentation coverage for all Python files in directory.

    Args:
        directory: Directory to analyze
        exclude_patterns: Patterns to exclude (e.g., ["test_", "__pycache__"])

    Returns:
        Combined documentation coverage statistics
    """
    if exclude_patterns is None:
        exclude_patterns = ["test_", "__pycache__", ".venv", "venv", "build", "dist"]

    total_stats = DocCoverageStats()

    for py_file in directory.rglob("*.py"):
        # Skip excluded patterns
        if any(pattern in str(py_file) for pattern in exclude_patterns):
            continue

        file_stats = analyze_file(py_file)
        total_stats.total_items += file_stats.total_items
        total_stats.documented_items += file_stats.documented_items
        total_stats.undocumented.extend(file_stats.undocumented)

    return total_stats


def print_report(stats: DocCoverageStats, threshold: float) -> None:
    """Print documentation coverage report.

    Args:
        stats: Documentation coverage statistics
        threshold: Minimum required coverage percentage
    """
    coverage = stats.coverage_percentage

    print("📚 Documentation Coverage Report")
    print("=" * 60)
    print(f"Total items:       {stats.total_items}")
    print(f"Documented:        {stats.documented_items}")
    print(f"Undocumented:      {len(stats.undocumented)}")
    print(f"Coverage:          {coverage:.1f}%")
    print(f"Threshold:         {threshold:.1f}%")
    print("=" * 60)

    if coverage >= threshold:
        print(f"✅ PASS: Coverage {coverage:.1f}% meets threshold {threshold:.1f}%")
    else:
        print(f"❌ FAIL: Coverage {coverage:.1f}% below threshold {threshold:.1f}%")

    if stats.undocumented:
        print(f"\n📝 Missing Documentation ({len(stats.undocumented)} items):")
        print("-" * 60)
        for item in sorted(stats.undocumented)[:50]:  # Show first 50
            print(f"  - {item}")
        if len(stats.undocumented) > 50:
            print(f"  ... and {len(stats.undocumented) - 50} more")


def save_report(stats: DocCoverageStats, output_path: Path) -> None:
    """Save documentation coverage report to JSON file.

    Args:
        stats: Documentation coverage statistics
        output_path: Path to output JSON file
    """
    report = {
        "total_items": stats.total_items,
        "documented_items": stats.documented_items,
        "undocumented_count": len(stats.undocumented),
        "coverage_percentage": stats.coverage_percentage,
        "undocumented": stats.undocumented,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n📄 Report saved to {output_path}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Analyze documentation coverage for Python code")
    parser.add_argument(
        "--threshold",
        type=float,
        default=80.0,
        help="Minimum coverage percentage required (default: 80)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output JSON report file path",
    )
    parser.add_argument(
        "--src-dir",
        type=Path,
        default=Path("src"),
        help="Source directory to analyze (default: src)",
    )

    args = parser.parse_args()

    # Validate source directory
    if not args.src_dir.exists():
        print(f"❌ Error: Source directory not found: {args.src_dir}", file=sys.stderr)
        sys.exit(1)

    # Analyze documentation coverage
    stats = analyze_directory(args.src_dir)

    # Print report
    print_report(stats, args.threshold)

    # Save JSON report if requested
    if args.output:
        save_report(stats, args.output)

    # Exit with appropriate code
    if stats.coverage_percentage >= args.threshold:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
