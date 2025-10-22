"""
Task format validation for AI agent task system compliance.

Validates that task updates follow Section 1.11 requirements:
1. Every task has `<number>. /<workflow> - <description>` format
2. Completed tasks are never removed from plan
3. Workflow attribution is correct (executor vs orchestrator)

Usage:
    python scripts/validate_task_format.py --session path/to/session-summary.md
    python scripts/validate_task_format.py --validate "task text"

Based on violations from 2025-10-19 sessions (Phase 5 implementation).
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationResult:
    """Result of a single validation check."""

    check_name: str
    severity: str  # 'critical', 'warning', 'info'
    passed: bool
    message: str
    task_step: str | None = None


class TaskFormatValidator:
    """Validates task format compliance per Section 1.11."""

    # Orchestrator workflows (coordinate, don't execute)
    ORCHESTRATOR_WORKFLOWS = {
        "/work",
        "/plan",
        "/meta-analysis",
    }

    # Executor workflows (perform actual work)
    EXECUTOR_WORKFLOWS = {
        "/implement",
        "/validate",
        "/commit",
        "/detect-context",
        "/load-context",
        "/research",
        "/generate-plan",
        "/extract-session",
        "/summarize-session",
        "/consolidate-summaries",
        "/archive-initiative",
        "/new-adr",
        "/bump-version",
        "/update-docs",
    }

    # Sub-workflow executors (called by parent workflows)
    SUB_WORKFLOW_EXECUTORS = {
        "/work-routing",
        "/work-session-protocol",
    }

    # Execution keywords that shouldn't use orchestrators
    EXECUTION_KEYWORDS = {
        "fix",
        "create",
        "write",
        "implement",
        "add",
        "update",
        "refactor",
        "delete",
        "modify",
        "build",
        "generate",
        "test",
    }

    def __init__(self) -> None:
        """Initialize validator."""
        self.results: list[ValidationResult] = []

    def validate_task_update(self, plan: list[dict[str, str]]) -> list[ValidationResult]:
        """
        Validate a single task update/plan.

        Args:
            plan: List of task dicts with 'step' and 'status' keys

        Returns:
            List of ValidationResult objects
        """
        self.results = []

        # Check 1: Workflow prefix presence
        self._check_workflow_prefix(plan)

        # Check 2: Correct attribution
        self._check_workflow_attribution(plan)

        # Check 3: Single in_progress task
        self._check_single_in_progress(plan)

        # Check 4: Valid numbering
        self._check_valid_numbering(plan)

        return self.results

    def validate_task_history(
        self, previous_plan: list[dict[str, str]], current_plan: list[dict[str, str]]
    ) -> list[ValidationResult]:
        """
        Validate task history to detect removed completed tasks.

        Args:
            previous_plan: Previous task plan
            current_plan: Current task plan

        Returns:
            List of ValidationResult objects
        """
        self.results = []

        # Extract completed tasks from previous plan
        previous_completed = {
            task["step"] for task in previous_plan if task.get("status") == "completed"
        }

        # Extract all tasks from current plan
        current_all = {task["step"] for task in current_plan}

        # Check for removed completed tasks
        removed_completed = previous_completed - current_all

        for removed_task in removed_completed:
            self.results.append(
                ValidationResult(
                    check_name="Completed Task Preservation",
                    severity="critical",
                    passed=False,
                    message=f"Removed completed task: '{removed_task}'. "
                    f"Completed tasks must be preserved in task history.",
                    task_step=removed_task,
                )
            )

        return self.results

    def _check_workflow_prefix(self, plan: list[dict[str, str]]) -> None:
        """Check that every task has /<workflow> prefix."""
        # Pattern: <number>. /<workflow> - <description>
        # Allow hierarchical: 1.1.1. /<workflow> - ...
        workflow_pattern = re.compile(r"^\s*(\d+(?:\.\d+)*)\.\s+(/[a-z-]+)\s+-\s+.+")

        for task in plan:
            step = task.get("step", "")

            # Extract task number (with indentation)
            number_match = re.match(r"^\s*(\d+(?:\.\d+)*)\.", step)
            if not number_match:
                # No number found - might be malformed
                self.results.append(
                    ValidationResult(
                        check_name="Task Format",
                        severity="critical",
                        passed=False,
                        message=f"Task '{step}' is malformed (no task number found). "
                        f"Expected format: '<number>. /<workflow> - <description>'",
                        task_step=step,
                    )
                )
                continue

            # Check for workflow prefix
            if not workflow_pattern.match(step):
                # Missing workflow prefix
                task_number = number_match.group(1)
                # Try to extract description after number
                desc_match = re.match(r"^\s*\d+(?:\.\d+)*\.\s+(.+)", step)
                description = desc_match.group(1) if desc_match else "task"

                self.results.append(
                    ValidationResult(
                        check_name="Workflow Prefix",
                        severity="critical",
                        passed=False,
                        message=f"Task '{step}' missing workflow prefix. "
                        f"Expected format: '{task_number}. /<workflow> - {description}'. "
                        f"Example: '{task_number}. /implement - {description}'",
                        task_step=step,
                    )
                )

    def _check_workflow_attribution(self, plan: list[dict[str, str]]) -> None:
        """Check that workflows are correctly attributed (executor vs orchestrator)."""
        for task in plan:
            step = task.get("step", "")

            # Extract workflow name
            workflow_match = re.search(r"/([a-z-]+)", step)
            if not workflow_match:
                continue  # Already flagged by prefix check

            workflow = f"/{workflow_match.group(1)}"

            # Extract description (after workflow prefix)
            desc_match = re.search(r"/[a-z-]+\s+-\s+(.+)", step)
            description = desc_match.group(1).lower() if desc_match else ""

            # Check if orchestrator is being used for execution work
            if workflow in self.ORCHESTRATOR_WORKFLOWS:
                # Check for execution keywords
                has_execution_keyword = any(
                    keyword in description for keyword in self.EXECUTION_KEYWORDS
                )

                if has_execution_keyword:
                    # Suggest correct workflow
                    suggested = "/implement"
                    self.results.append(
                        ValidationResult(
                            check_name="Workflow Attribution",
                            severity="warning",
                            passed=False,
                            message=f"Task '{step}' uses orchestrator {workflow} for execution work. "
                            f"Execution tasks should use {suggested} or other executor workflows. "
                            f"Orchestrators coordinate, executors perform work.",
                            task_step=step,
                        )
                    )

            # Check for specific anti-patterns
            if workflow == "/work" and "session end protocol" in description:
                self.results.append(
                    ValidationResult(
                        check_name="Workflow Attribution",
                        severity="warning",
                        passed=False,
                        message=f"Task '{step}' should use /work-session-protocol instead of /work. "
                        f"Use sub-workflow for session end protocol.",
                        task_step=step,
                    )
                )

            if workflow == "/plan" and any(
                keyword in description for keyword in ["write", "implement", "create code"]
            ):
                self.results.append(
                    ValidationResult(
                        check_name="Workflow Attribution",
                        severity="warning",
                        passed=False,
                        message=f"Task '{step}' uses /plan for execution work. "
                        f"/plan is for planning, use /implement for code changes.",
                        task_step=step,
                    )
                )

    def _check_single_in_progress(self, plan: list[dict[str, str]]) -> None:
        """Check that only one task is in_progress at a time (excluding parent-child chains)."""
        in_progress_tasks = [task for task in plan if task.get("status") == "in_progress"]

        if len(in_progress_tasks) <= 1:
            return

        # Extract task numbers to check for parent-child relationships
        task_numbers = []
        for task in in_progress_tasks:
            step = task["step"]
            number_match = re.match(r"^\s*(\d+(?:\.\d+)*)\.", step)
            if number_match:
                task_numbers.append(number_match.group(1))

        # Check if all in_progress tasks form a parent-child chain
        # Valid examples: ["1", "1.1"], ["1", "1.1", "1.1.2"], ["2.3", "2.3.1"]
        # Invalid: ["1", "2"], ["1.1", "1.2"]

        # Sort by hierarchy depth (fewer dots = higher in hierarchy)
        sorted_numbers = sorted(task_numbers, key=lambda x: x.count("."))

        # Check each task is ancestor/descendant of previous
        is_valid_chain = True
        for i in range(1, len(sorted_numbers)):
            current = sorted_numbers[i]
            previous = sorted_numbers[i - 1]

            # Current should start with previous + "."
            if not current.startswith(previous + "."):
                is_valid_chain = False
                break

        if not is_valid_chain:
            self.results.append(
                ValidationResult(
                    check_name="Single In-Progress Task",
                    severity="warning",
                    passed=False,
                    message="Multiple tasks in_progress: only one task can be in_progress at a time",
                    task_step=None,
                )
            )

    def _check_valid_numbering(self, plan: list[dict[str, str]]) -> None:
        """Check that task numbering is sequential and valid."""
        # Extract numbers from tasks
        task_numbers = []
        for task in plan:
            step = task.get("step", "")
            number_match = re.match(r"^\s*(\d+(?:\.\d+)*)\.", step)
            if number_match:
                task_numbers.append(number_match.group(1))

        # Group by depth (number of dots)
        by_depth: dict[int, list[str]] = {}
        for number_str in task_numbers:
            depth = number_str.count(".")
            if depth not in by_depth:
                by_depth[depth] = []
            by_depth[depth].append(number_str)

        # Check each depth level for gaps
        for depth, numbers in by_depth.items():
            # For each unique parent prefix at this depth
            parent_groups: dict[str, list[int]] = {}
            for number_str in numbers:
                if depth == 0:
                    # Top level - group all together
                    parent_prefix = ""
                else:
                    # Get parent prefix (everything before last dot)
                    parts = number_str.split(".")
                    parent_prefix = ".".join(parts[:-1])

                if parent_prefix not in parent_groups:
                    parent_groups[parent_prefix] = []

                # Extract the last number component
                last_component = int(number_str.split(".")[-1])
                parent_groups[parent_prefix].append(last_component)

            # Check each group for sequential numbering
            for parent_prefix, nums in parent_groups.items():
                unique_sorted = sorted(set(nums))

                # Check for gaps
                for i in range(len(unique_sorted) - 1):
                    current = unique_sorted[i]
                    next_num = unique_sorted[i + 1]

                    if next_num - current > 1:
                        # Found a gap
                        expected = current + 1

                        if depth == 0:
                            # Top level: "Numbering gap: expected 2, found 3"
                            self.results.append(
                                ValidationResult(
                                    check_name="Task Numbering",
                                    severity="warning",
                                    passed=False,
                                    message=f"Numbering gap: expected {expected}, found {next_num}",
                                    task_step=None,
                                )
                            )
                        else:
                            # Subtasks: "Numbering gap in subtasks: expected 1.2, found 1.3"
                            expected_full = f"{parent_prefix}.{expected}"
                            found_full = f"{parent_prefix}.{next_num}"
                            self.results.append(
                                ValidationResult(
                                    check_name="Task Numbering",
                                    severity="warning",
                                    passed=False,
                                    message=f"Numbering gap in subtasks: expected {expected_full}, found {found_full}",
                                    task_step=None,
                                )
                            )


def validate_session_file(session_file: Path) -> list[ValidationResult]:
    """
    Validate task format in a session summary file.

    Args:
        session_file: Path to session summary markdown file

    Returns:
        List of ValidationResult objects
    """
    # TODO: Parse session file and extract task updates
    # For now, return empty list
    _ = session_file  # Will be used when session parsing is implemented
    return []


def print_results(results: list[ValidationResult], verbose: bool = False) -> None:
    """Print validation results in human-readable format."""
    if not results:
        print("✅ No violations found")
        return

    critical_failures = [r for r in results if r.severity == "critical" and not r.passed]
    warnings = [r for r in results if r.severity == "warning" and not r.passed]
    infos = [r for r in results if r.severity == "info"]

    print(f"\n{'=' * 80}")
    print("Task Format Validation Report")
    print(f"{'=' * 80}")
    print(f"Total checks: {len(results)}")
    print(f"❌ Critical failures: {len(critical_failures)}")
    print(f"⚠️  Warnings: {len(warnings)}")
    print(f"ℹ️  Info: {len(infos)}")
    print(f"{'=' * 80}\n")

    # Print critical failures
    if critical_failures:
        print("❌ CRITICAL FAILURES (Must fix):\n")
        for result in critical_failures:
            print(f"  Check: {result.check_name}")
            if result.task_step:
                print(f"  Task: {result.task_step}")
            print(f"  Message: {result.message}")
            print()

    # Print warnings
    if warnings:
        print("⚠️  WARNINGS (Recommended fixes):\n")
        for result in warnings:
            print(f"  Check: {result.check_name}")
            if result.task_step:
                print(f"  Task: {result.task_step}")
            print(f"  Message: {result.message}")
            print()

    # Print info (verbose mode only)
    if infos and verbose:
        print("ℹ️  INFORMATION:\n")
        for result in infos:
            print(f"  {result.message}")
            print()

    # Exit status
    if critical_failures:
        print("❌ Validation FAILED (critical failures detected)")
        sys.exit(1)
    elif warnings:
        print("⚠️  Validation PASSED (with warnings)")
    else:
        print("✅ Validation PASSED")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Validate task format compliance")
    parser.add_argument(
        "--session",
        type=Path,
        help="Validate tasks in session summary file",
    )
    parser.add_argument(
        "--validate",
        type=str,
        help="Validate a single task string",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show informational messages",
    )

    args = parser.parse_args()

    validator = TaskFormatValidator()

    if args.session:
        # Validate session file
        results = validate_session_file(args.session)
        print_results(results, verbose=args.verbose)

    elif args.validate:
        # Validate single task
        task = {"step": args.validate, "status": "pending"}
        results = validator.validate_task_update([task])
        print_results(results, verbose=args.verbose)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
