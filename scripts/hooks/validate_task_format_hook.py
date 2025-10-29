#!/usr/bin/env python3
"""
Pre-commit hook for validating task format in markdown documentation.

Scans workflow files and session summaries for update_plan() examples
and validates they follow Section 1.11 task format requirements.

Usage:
    python scripts/hooks/validate_task_format_hook.py file1.md file2.md ...

Exit codes:
    0: All files valid
    1: Violations found
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Any

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validation.validate_task_format import TaskFormatValidator


def extract_update_plan_calls(content: str) -> list[dict[str, Any]]:
    """
    Extract update_plan() calls from markdown code blocks.

    Args:
        content: Markdown file content

    Returns:
        List of dicts with 'line_number' and 'plan' keys
    """
    results = []

    # Find TypeScript/JavaScript code blocks
    code_block_pattern = re.compile(
        r"```(?:typescript|javascript|ts|js)\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE
    )

    for match in code_block_pattern.finditer(content):
        code_block = match.group(1)
        start_line = content[: match.start()].count("\n") + 1

        # Find update_plan calls in the code block
        # Pattern: update_plan({ ... plan: [...]  })
        update_plan_pattern = re.compile(
            r"update_plan\s*\(\s*\{[^}]*plan\s*:\s*\[(.*?)\]", re.DOTALL
        )

        for plan_match in update_plan_pattern.finditer(code_block):
            plan_content = plan_match.group(1)

            # Parse task objects: { step: "...", status: "..." }
            task_pattern = re.compile(
                r'\{\s*step\s*:\s*["\']([^"\']+)["\']\s*,\s*status\s*:\s*["\']([^"\']+)["\']\s*\}'
            )

            tasks = []
            for task_match in task_pattern.finditer(plan_content):
                tasks.append({"step": task_match.group(1), "status": task_match.group(2)})

            if tasks:
                # Calculate line number in file
                lines_before = code_block[: plan_match.start()].count("\n")
                line_number = start_line + lines_before

                results.append({"line_number": line_number, "plan": tasks})

    return results


def validate_file(file_path: Path) -> tuple[bool, list[str]]:
    """
    Validate task format in a markdown file.

    Args:
        file_path: Path to markdown file

    Returns:
        Tuple of (is_valid, error_messages)
    """
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"Error reading {file_path}: {e}"]

    # Extract update_plan calls
    plan_calls = extract_update_plan_calls(content)

    if not plan_calls:
        # No update_plan calls found - this is OK
        return True, []

    # Placeholders used in documentation (skip validation for these)
    PLACEHOLDERS = {
        "/<routed-workflow>",
        "/<workflow>",
        "/<executor-workflow>",
        "/<orchestrator>",
        "/<sub-workflow>",
    }

    # Validate each plan
    validator = TaskFormatValidator()
    errors = []

    for call in plan_calls:
        # Check if any tasks contain placeholders
        has_placeholders = any(
            any(placeholder in task["step"] for placeholder in PLACEHOLDERS)
            for task in call["plan"]
        )

        if has_placeholders:
            # Skip validation for examples with placeholders
            # These are documentation templates, not real task lists
            continue

        violations = validator.validate_task_update(call["plan"])

        # Filter to only critical and warning violations
        serious_violations = [
            v for v in violations if v.severity in ("critical", "warning") and not v.passed
        ]

        if serious_violations:
            errors.append(f"\n{file_path}:{call['line_number']}: Found task format violations:")
            for violation in serious_violations:
                severity_icon = "❌" if violation.severity == "critical" else "⚠️"
                errors.append(f"  {severity_icon} [{violation.check_name}] {violation.message}")

    return len(errors) == 0, errors


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Validate task format in markdown documentation")
    parser.add_argument("files", nargs="+", type=Path, help="Files to validate")
    parser.add_argument(
        "--skip-non-md",
        action="store_true",
        help="Skip files that aren't markdown (exit 0 instead of error)",
    )

    args = parser.parse_args()

    all_valid = True
    all_errors = []

    for file_path in args.files:
        # Only validate markdown files
        if file_path.suffix != ".md":
            if args.skip_non_md:
                continue
            else:
                all_errors.append(f"Skipping non-markdown file: {file_path}")
                continue

        # Only validate workflow and session summary files
        # (other markdown files don't need task format validation)
        should_validate = False
        if (
            ".windsurf/workflows" in str(file_path)
            or "session-summaries" in str(file_path)
            or "session_summaries" in str(file_path)
        ):
            should_validate = True

        if not should_validate:
            continue

        is_valid, errors = validate_file(file_path)
        if not is_valid:
            all_valid = False
            all_errors.extend(errors)

    if not all_valid:
        print("\n" + "=" * 80)
        print("Task Format Validation Failed")
        print("=" * 80)
        for error in all_errors:
            print(error)
        print("\n" + "=" * 80)
        print(
            "Fix the violations above, or use 'git commit --no-verify' to bypass (not recommended)"
        )
        print("=" * 80)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
