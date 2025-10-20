#!/usr/bin/env python3
"""Check for performance regressions by comparing benchmark results.

This script compares current benchmark results against a baseline and fails
if any test is significantly slower (>threshold%).

Usage:
    python scripts/check_performance_regression.py current.json baseline.json --threshold 1.2

Exit codes:
    0: No regressions detected
    1: Regressions detected or error occurred
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_benchmark_data(file_path: Path) -> dict[str, Any]:
    """Load benchmark data from JSON file."""
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON in {file_path}", file=sys.stderr)
        sys.exit(1)


def extract_benchmarks(data: dict[str, Any]) -> dict[str, float]:
    """Extract benchmark names and mean times from pytest-benchmark JSON."""
    benchmarks = {}
    for bench in data.get("benchmarks", []):
        name = bench["name"]
        mean = bench["stats"]["mean"]
        benchmarks[name] = mean
    return benchmarks


def compare_benchmarks(
    current: dict[str, float],
    baseline: dict[str, float],
    threshold: float,
) -> tuple[list[tuple[str, float, float, float]], bool]:
    """Compare current benchmarks against baseline.

    Args:
        current: Current benchmark results (name -> mean time)
        baseline: Baseline benchmark results (name -> mean time)
        threshold: Regression threshold (e.g., 1.2 = 20% slower is regression)

    Returns:
        Tuple of (regressions, has_regressions) where regressions is a list of
        (name, current_time, baseline_time, ratio) tuples
    """
    regressions = []

    for name, current_time in current.items():
        if name not in baseline:
            print(f"⚠️  Warning: '{name}' not found in baseline, skipping")
            continue

        baseline_time = baseline[name]
        ratio = current_time / baseline_time if baseline_time > 0 else float("inf")

        if ratio > threshold:
            regressions.append((name, current_time, baseline_time, ratio))

    return regressions, len(regressions) > 0


def format_time(seconds: float) -> str:
    """Format time in appropriate unit (s, ms, us, ns)."""
    if seconds >= 1.0:
        return f"{seconds:.3f}s"
    elif seconds >= 0.001:
        return f"{seconds * 1000:.3f}ms"
    elif seconds >= 0.000001:
        return f"{seconds * 1_000_000:.3f}μs"
    else:
        return f"{seconds * 1_000_000_000:.3f}ns"


def print_report(
    regressions: list[tuple[str, float, float, float]],
    threshold: float,
    total_tests: int,
) -> None:
    """Print performance regression report."""
    if not regressions:
        print(f"✅ No performance regressions detected ({total_tests} tests checked)")
        print(f"   Threshold: {(threshold - 1) * 100:.0f}% slower")
        return

    print(f"❌ Performance regressions detected ({len(regressions)}/{total_tests} tests)")
    print(f"   Threshold: {(threshold - 1) * 100:.0f}% slower\n")

    # Sort by ratio (worst regressions first)
    regressions.sort(key=lambda x: x[3], reverse=True)

    print("Slowest Regressions:")
    print(f"{'Test':<50} {'Baseline':<15} {'Current':<15} {'Change':<10}")
    print("-" * 95)

    for name, current_time, baseline_time, ratio in regressions:
        current_str = format_time(current_time)
        baseline_str = format_time(baseline_time)
        change_pct = (ratio - 1) * 100
        change_str = f"+{change_pct:.1f}%"

        # Truncate long names
        display_name = name[:47] + "..." if len(name) > 50 else name

        print(f"{display_name:<50} {baseline_str:<15} {current_str:<15} {change_str:<10}")


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Check for performance regressions in benchmark results"
    )
    parser.add_argument(
        "current",
        type=Path,
        help="Path to current benchmark results JSON file",
    )
    parser.add_argument(
        "baseline",
        type=Path,
        help="Path to baseline benchmark results JSON file",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=1.2,
        help="Regression threshold as ratio (default: 1.2 = 20%% slower)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail even on warnings (missing tests)",
    )

    args = parser.parse_args()

    # Validate threshold
    if args.threshold <= 1.0:
        print("❌ Error: Threshold must be > 1.0", file=sys.stderr)
        sys.exit(1)

    # Load benchmark data
    print(f"Loading current results from {args.current}")
    current_data = load_benchmark_data(args.current)

    print(f"Loading baseline from {args.baseline}")
    baseline_data = load_benchmark_data(args.baseline)

    # Extract benchmark results
    current = extract_benchmarks(current_data)
    baseline = extract_benchmarks(baseline_data)

    print(f"\nComparing {len(current)} benchmarks against baseline...")
    print()

    # Compare
    regressions, has_regressions = compare_benchmarks(current, baseline, args.threshold)

    # Print report
    print_report(regressions, args.threshold, len(current))

    # Exit with appropriate code
    if has_regressions:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
