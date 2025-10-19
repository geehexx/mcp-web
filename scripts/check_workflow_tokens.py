#!/usr/bin/env python3
"""
Workflow Token Monitoring Script

Tracks token counts across workflows and rules to:
- Prevent regression after optimization
- Monitor complexity trends over time
- Fail CI builds if thresholds exceeded

Usage:
    python scripts/check_workflow_tokens.py
    python scripts/check_workflow_tokens.py --threshold 60000
    python scripts/check_workflow_tokens.py --save-baseline
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

# Project root
ROOT = Path(__file__).parent.parent
WINDSURF_DIR = ROOT / ".windsurf"
BENCHMARKS_DIR = ROOT / ".benchmarks"
BASELINE_FILE = BENCHMARKS_DIR / "workflow-tokens-baseline.json"
HISTORY_FILE = BENCHMARKS_DIR / "workflow-tokens-history.jsonl"


class TokenMonitor:
    """Monitors token counts across workflows and rules."""

    def __init__(self, threshold: int = 60000, save_baseline: bool = False) -> None:
        """Initialize monitor.

        Args:
            threshold: Maximum allowed total tokens
            save_baseline: If True, save current state as baseline
        """
        self.threshold = threshold
        self.save_baseline_mode = save_baseline

        # Ensure benchmarks directory exists
        BENCHMARKS_DIR.mkdir(exist_ok=True)

    def run(self) -> int:
        """Run token monitoring.

        Returns:
            Exit code (0 = pass, 1 = threshold exceeded)
        """
        print("📊 Monitoring workflow and rule token counts\n")

        # Collect current counts
        current = self._collect_token_counts()

        # Print summary
        self._print_summary(current)

        # Save baseline if requested
        if self.save_baseline_mode:
            self._save_baseline(current)
            print("\n✅ Baseline saved")
            return 0

        # Load baseline
        baseline = self._load_baseline()

        # Compare and validate
        return self._validate_against_baseline(current, baseline)

    def _collect_token_counts(self) -> dict[str, Any]:
        """Collect token counts from all workflows and rules.

        Returns:
            Dictionary with token counts and metadata
        """
        data: dict[str, Any] = {
            "timestamp": datetime.now().isoformat(),
            "workflows": {},
            "rules": {},
            "totals": {"workflows": 0, "rules": 0, "combined": 0},
        }

        # Collect workflow tokens
        workflow_dir = WINDSURF_DIR / "workflows"
        for file in sorted(workflow_dir.glob("*.md")):
            tokens = self._extract_token_count(file)
            data["workflows"][file.name] = tokens
            data["totals"]["workflows"] += tokens

        # Collect rule tokens
        rules_dir = WINDSURF_DIR / "rules"
        for file in sorted(rules_dir.glob("*.md")):
            tokens = self._extract_token_count(file)
            data["rules"][file.name] = tokens
            data["totals"]["rules"] += tokens

        # Combined total
        data["totals"]["combined"] = data["totals"]["workflows"] + data["totals"]["rules"]

        return data

    def _extract_token_count(self, file: Path) -> int:
        """Extract token count from frontmatter.

        Args:
            file: Path to file

        Returns:
            Token count (or estimated if not in frontmatter)
        """
        content = file.read_text()

        # Try to extract from frontmatter
        if content.startswith("---\n"):
            parts = content.split("---\n", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    if isinstance(frontmatter, dict) and "tokens" in frontmatter:
                        return frontmatter["tokens"]
                except yaml.YAMLError:
                    pass

        # Fallback: estimate from file size (4 chars ≈ 1 token)
        return len(content) // 4

    def _print_summary(self, data: dict[str, Any]) -> None:
        """Print token count summary.

        Args:
            data: Token count data
        """
        print(f"📅 Timestamp: {data['timestamp']}\n")

        # Workflows
        print("📝 Workflows:")
        for name, tokens in sorted(data["workflows"].items()):
            print(f"  {name:<35} {tokens:>6} tokens")
        print(f"  {'TOTAL':<35} {data['totals']['workflows']:>6} tokens\n")

        # Rules
        print("📏 Rules:")
        for name, tokens in sorted(data["rules"].items()):
            print(f"  {name:<35} {tokens:>6} tokens")
        print(f"  {'TOTAL':<35} {data['totals']['rules']:>6} tokens\n")

        # Combined
        print(f"🎯 COMBINED TOTAL: {data['totals']['combined']:,} tokens")
        print(f"📊 THRESHOLD:      {self.threshold:,} tokens")

    def _save_baseline(self, data: dict[str, Any]) -> None:
        """Save current state as baseline.

        Args:
            data: Token count data
        """
        # Save baseline file
        with open(BASELINE_FILE, "w") as f:
            json.dump(data, f, indent=2)

        # Append to history
        with open(HISTORY_FILE, "a") as f:
            f.write(json.dumps(data) + "\n")

    def _load_baseline(self) -> dict[str, Any] | None:
        """Load baseline data.

        Returns:
            Baseline data or None if not found
        """
        if not BASELINE_FILE.exists():
            return None

        with open(BASELINE_FILE) as f:
            return json.load(f)

    def _validate_against_baseline(
        self, current: dict[str, Any], baseline: dict[str, Any] | None
    ) -> int:
        """Validate current counts against baseline.

        Args:
            current: Current token counts
            baseline: Baseline token counts

        Returns:
            Exit code (0 = pass, 1 = fail)
        """
        print("\n" + "=" * 60)

        # Check threshold
        current_total = current["totals"]["combined"]
        if current_total > self.threshold:
            print(f"\n❌ THRESHOLD EXCEEDED: {current_total:,} > {self.threshold:,}")
            print("   Token count has grown beyond acceptable limit.")
            print("   Consider refactoring or updating threshold.")
            print("\n" + "=" * 60)
            return 1

        # Compare to baseline
        if baseline:
            baseline_total = baseline["totals"]["combined"]
            diff = current_total - baseline_total
            pct_change = (diff / baseline_total * 100) if baseline_total > 0 else 0

            print("\n📊 Baseline Comparison:")
            print(f"   Baseline:  {baseline_total:,} tokens")
            print(f"   Current:   {current_total:,} tokens")
            print(f"   Change:    {diff:+,} tokens ({pct_change:+.1f}%)")

            if diff > 0:
                print(f"\n⚠️  Token count increased by {abs(diff):,} tokens")
                print("   Consider reviewing changes for optimization opportunities.")

            elif diff < 0:
                print(f"\n✅ Token count decreased by {abs(diff):,} tokens!")
                print("   Great work on optimization!")

        else:
            print("\n⚠️  No baseline found. Run with --save-baseline to set one.")

        print("\n✅ All checks passed!")
        print("=" * 60)

        # Append to history
        with open(HISTORY_FILE, "a") as f:
            f.write(json.dumps(current) + "\n")

        return 0


def main() -> int:
    """Main entry point.

    Returns:
        Exit code
    """
    import argparse

    parser = argparse.ArgumentParser(description="Monitor workflow and rule token counts")
    parser.add_argument(
        "--threshold",
        type=int,
        default=60000,
        help="Maximum allowed total tokens (default: 60000)",
    )
    parser.add_argument(
        "--save-baseline",
        action="store_true",
        help="Save current state as baseline",
    )
    args = parser.parse_args()

    monitor = TokenMonitor(threshold=args.threshold, save_baseline=args.save_baseline)
    return monitor.run()


if __name__ == "__main__":
    sys.exit(main())
