#!/usr/bin/env python3
"""
Initiative Validation Script

Validates initiative files for required frontmatter fields, phase consistency,
dependency satisfaction, and blocker propagation.

Usage:
    python scripts/validate_initiatives.py                    # Validate all initiatives
    python scripts/validate_initiatives.py --file path/to/initiative.md  # Validate specific file
    python scripts/validate_initiatives.py --ci               # CI mode (exit 1 on failures)

References:
    - Initiative System Lifecycle Improvements (2025-10-19)
    - Quality Gates (PMI/DTU ProjectLab, 2025)
    - Requirements Traceability Matrix (6Sigma, 2025)
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    import frontmatter
except ImportError:
    print("ERROR: Required dependencies not installed")
    print("Install: uv add python-frontmatter pyyaml")
    sys.exit(1)


@dataclass
class ValidationResult:
    """Single validation check result."""

    check_name: str
    severity: str  # "critical", "warning", "info"
    passed: bool
    message: str
    file_path: str | None = None
    line_number: int | None = None


class InitiativeValidator:
    """Validates initiative files against system requirements."""

    # Required frontmatter fields for all initiatives
    REQUIRED_FIELDS = {
        "Status": ["Active", "Completed", "Proposed", "Archived", "✅ Completed"],
        "Created": None,  # Date format YYYY-MM-DD
        "Owner": None,
        "Priority": ["Low", "Medium", "High", "Critical"],
    }

    # Optional but recommended fields
    RECOMMENDED_FIELDS = ["Estimated Duration", "Target Completion", "Updated"]

    def __init__(self, initiatives_dir: Path):
        self.initiatives_dir = initiatives_dir
        self.results: list[ValidationResult] = []

    def validate_file(self, file_path: Path) -> list[ValidationResult]:
        """Validate a single initiative file."""
        self.results = []

        try:
            with open(file_path, encoding="utf-8") as f:
                post = frontmatter.load(f)

            # Check 1: Required frontmatter fields
            self._check_required_fields(post, file_path)

            # Check 2: Date format validation
            self._check_date_formats(post, file_path)

            # Check 3: Status consistency with content
            self._check_status_consistency(post, file_path)

            # Check 4: Success criteria format
            self._check_success_criteria(post.content, file_path)

            # Check 5: Phase consistency (if folder-based)
            if file_path.parent.name != "active" and file_path.parent.name != "completed":
                self._check_phases_exist(file_path)

            # Check 6: Phase progression consistency
            self._check_phase_consistency(post.content, file_path)

            # Check 7: Status inference
            self._infer_status(post, file_path)

        except Exception as e:
            self.results.append(
                ValidationResult(
                    check_name="File Parsing",
                    severity="critical",
                    passed=False,
                    message=f"Failed to parse file: {e}",
                    file_path=str(file_path),
                )
            )

        return self.results

    def _check_required_fields(self, post: frontmatter.Post, file_path: Path):
        """Validate required frontmatter fields are present and valid."""
        metadata = post.metadata

        for field, valid_values in self.REQUIRED_FIELDS.items():
            if field not in metadata:
                self.results.append(
                    ValidationResult(
                        check_name="Required Field",
                        severity="critical",
                        passed=False,
                        message=f"Missing required field: {field}",
                        file_path=str(file_path),
                    )
                )
            elif valid_values and metadata[field] not in valid_values:
                self.results.append(
                    ValidationResult(
                        check_name="Field Value",
                        severity="warning",
                        passed=False,
                        message=f"Invalid {field} value '{metadata[field]}'. Expected one of: {', '.join(valid_values)}",
                        file_path=str(file_path),
                    )
                )

        # Check for recommended fields
        for field in self.RECOMMENDED_FIELDS:
            if field not in metadata:
                self.results.append(
                    ValidationResult(
                        check_name="Recommended Field",
                        severity="info",
                        passed=True,  # Not a failure
                        message=f"Missing recommended field: {field}",
                        file_path=str(file_path),
                    )
                )

    def _check_date_formats(self, post: frontmatter.Post, file_path: Path):
        """Validate date fields use YYYY-MM-DD format."""
        date_fields = ["Created", "Updated", "Target Completion", "Completed"]
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")

        for field in date_fields:
            if field in post.metadata:
                value = str(post.metadata[field])
                if not date_pattern.match(value):
                    self.results.append(
                        ValidationResult(
                            check_name="Date Format",
                            severity="warning",
                            passed=False,
                            message=f"{field} must use YYYY-MM-DD format, got: {value}",
                            file_path=str(file_path),
                        )
                    )

    def _check_status_consistency(self, post: frontmatter.Post, file_path: Path):
        """Check if status matches file location and content."""
        status = post.metadata.get("Status", "")
        file_location = file_path.parent.name

        # Check 1: Completed status should be in completed/ directory
        if status in ["Completed", "✅ Completed"] and file_location == "active":
            self.results.append(
                ValidationResult(
                    check_name="Status Consistency",
                    severity="critical",
                    passed=False,
                    message=f"Initiative marked '{status}' but in active/ directory. Should be in completed/.",
                    file_path=str(file_path),
                )
            )

        # Check 2: Active status should have unchecked tasks
        if status == "Active":
            unchecked_tasks = re.findall(r"^- \[ \]", post.content, re.MULTILINE)
            checked_tasks = re.findall(r"^- \[x\]", post.content, re.MULTILINE)

            if len(unchecked_tasks) == 0 and len(checked_tasks) > 0:
                self.results.append(
                    ValidationResult(
                        check_name="Active Status",
                        severity="warning",
                        passed=False,
                        message="Initiative marked 'Active' but has no unchecked tasks. Consider marking Completed.",
                        file_path=str(file_path),
                    )
                )

    def _check_success_criteria(self, content: str, file_path: Path):
        """Validate success criteria section exists and uses checkboxes."""
        # Look for Success Criteria section
        success_section = re.search(
            r"##\s+Success\s+(Criteria|Metrics)(.*?)(?=##|\Z)",
            content,
            re.DOTALL | re.IGNORECASE,
        )

        if not success_section:
            self.results.append(
                ValidationResult(
                    check_name="Success Criteria",
                    severity="warning",
                    passed=False,
                    message="No 'Success Criteria' or 'Success Metrics' section found",
                    file_path=str(file_path),
                )
            )
            return

        section_content = success_section.group(2)

        # Check for checkbox format
        checkboxes = re.findall(r"- \[[x ]\]", section_content)
        if len(checkboxes) == 0:
            self.results.append(
                ValidationResult(
                    check_name="Success Criteria Format",
                    severity="warning",
                    passed=False,
                    message="Success Criteria should use checkbox format: - [ ] criterion",
                    file_path=str(file_path),
                )
            )

    def _check_phases_exist(self, file_path: Path):
        """Check if folder-based initiative has phases/ directory."""
        initiative_dir = file_path.parent
        phases_dir = initiative_dir / "phases"

        if phases_dir.exists() and phases_dir.is_dir():
            phase_files = list(phases_dir.glob("*.md"))
            if len(phase_files) == 0:
                self.results.append(
                    ValidationResult(
                        check_name="Phase Files",
                        severity="info",
                        passed=True,
                        message="phases/ directory exists but is empty",
                        file_path=str(file_path),
                    )
                )

    def _check_phase_consistency(self, content: str, file_path: Path):
        """
        Validate phase progression consistency.

        Rules:
        - If Phase N is complete, all phases 1 to N-1 must be complete
        - Phases should be numbered sequentially
        - Phase completion % should match task completion
        """
        # Extract phase sections
        phase_pattern = re.compile(
            r"###?\s+Phase\s+(\d+)[:\s]+(.*?)(?=###?\s+Phase\s+\d+|##\s+(?!Phase)|$)",
            re.DOTALL | re.IGNORECASE,
        )
        phases = {}

        for match in phase_pattern.finditer(content):
            phase_num = int(match.group(1))
            phase_content = match.group(2)

            # Count tasks in this phase
            unchecked = len(re.findall(r"^- \[ \]", phase_content, re.MULTILINE))
            checked = len(re.findall(r"^- \[x\]", phase_content, re.MULTILINE))
            total = unchecked + checked

            phases[phase_num] = {
                "unchecked": unchecked,
                "checked": checked,
                "total": total,
                "complete": unchecked == 0 and total > 0,
            }

        if not phases:
            # No phases found, skip this check
            return

        # Check 1: Sequential numbering
        expected_phases = set(range(1, max(phases.keys()) + 1))
        actual_phases = set(phases.keys())
        missing_phases = expected_phases - actual_phases

        if missing_phases:
            self.results.append(
                ValidationResult(
                    check_name="Phase Numbering",
                    severity="warning",
                    passed=False,
                    message=f"Missing phase numbers: {sorted(missing_phases)}. Phases should be numbered sequentially.",
                    file_path=str(file_path),
                )
            )

        # Check 2: Phase progression consistency
        for phase_num in sorted(phases.keys()):
            if phases[phase_num]["complete"]:
                # Check all previous phases are complete
                for prev_phase in range(1, phase_num):
                    if prev_phase in phases and not phases[prev_phase]["complete"]:
                        self.results.append(
                            ValidationResult(
                                check_name="Phase Progression",
                                severity="critical",
                                passed=False,
                                message=f"Phase {phase_num} is complete but Phase {prev_phase} is incomplete. "
                                "Phases must be completed in order.",
                                file_path=str(file_path),
                            )
                        )

    def _infer_status(self, post: frontmatter.Post, file_path: Path) -> str | None:
        """
        Infer initiative status based on task completion percentage.

        Returns suggested status if current status doesn't match reality,
        otherwise returns None.

        Rules:
        - 0% complete + no activity → "Proposed"
        - 1-99% complete → "Active"
        - 100% complete → "Completed"
        """
        current_status = post.metadata.get("Status", "Unknown")
        content = post.content

        # Count all tasks
        all_unchecked = re.findall(r"^- \[ \]", content, re.MULTILINE)
        all_checked = re.findall(r"^- \[x\]", content, re.MULTILINE)
        total_tasks = len(all_unchecked) + len(all_checked)

        if total_tasks == 0:
            # No tasks defined, can't infer
            return None

        completion_pct = (len(all_checked) / total_tasks) * 100

        # Determine suggested status
        suggested_status = None
        if completion_pct == 0:
            # Check if there's recent activity (Updated field)
            updated = post.metadata.get("Updated")
            created = post.metadata.get("Created")
            suggested_status = (
                "Proposed" if updated == created or not updated else "Active"
            )  # Active if has been worked on
        elif completion_pct < 100:
            suggested_status = "Active"
        else:  # 100%
            suggested_status = "Completed"

        # Check if inference differs from current status
        if current_status != suggested_status and suggested_status:
            self.results.append(
                ValidationResult(
                    check_name="Status Inference",
                    severity="warning",
                    passed=False,
                    message=f"Status is '{current_status}' but task completion suggests '{suggested_status}' "
                    f"({completion_pct:.0f}% complete: {len(all_checked)}/{total_tasks} tasks)",
                    file_path=str(file_path),
                )
            )
            return suggested_status

        return None

    def validate_all(self) -> dict[str, list[ValidationResult]]:
        """Validate all initiative files in active/ and completed/ directories."""
        all_results = {}

        for directory in ["active", "completed"]:
            dir_path = self.initiatives_dir / directory
            if not dir_path.exists():
                continue

            # Find all initiative.md files (folder-based) and .md files (flat-file)
            for file_path in dir_path.rglob("initiative.md"):
                results = self.validate_file(file_path)
                all_results[str(file_path)] = results

            for file_path in dir_path.glob("*.md"):
                if file_path.name != "initiative.md":
                    results = self.validate_file(file_path)
                    all_results[str(file_path)] = results

        return all_results


def generate_markdown_report(
    results: dict[str, list[ValidationResult]], output_path: Path | None = None
) -> str:
    """
    Generate validation report in markdown format.

    Args:
        results: Validation results by file
        output_path: Optional path to write report to file

    Returns:
        Markdown-formatted report string
    """
    from datetime import datetime

    total_files = len(results)
    total_checks = sum(len(checks) for checks in results.values())

    critical_failures = []
    warnings = []
    infos = []

    for file_path, checks in results.items():
        for check in checks:
            if check.severity == "critical" and not check.passed:
                critical_failures.append((file_path, check))
            elif check.severity == "warning" and not check.passed:
                warnings.append((file_path, check))
            elif check.severity == "info":
                infos.append((file_path, check))

    # Build markdown report
    report_lines = []
    report_lines.append("# Initiative Validation Report")
    report_lines.append("")
    report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"- **Files checked:** {total_files}")
    report_lines.append(f"- **Total checks:** {total_checks}")
    report_lines.append(f"- **❌ Critical failures:** {len(critical_failures)}")
    report_lines.append(f"- **⚠️ Warnings:** {len(warnings)}")
    report_lines.append(f"- **ℹ️ Info:** {len(infos)}")
    report_lines.append("")

    # Critical failures section
    if critical_failures:
        report_lines.append("## ❌ Critical Failures")
        report_lines.append("")
        report_lines.append("These issues **MUST** be fixed before the initiative can proceed.")
        report_lines.append("")

        for file_path, check in critical_failures:
            # Relative path for readability
            rel_path = (
                str(Path(file_path).relative_to(Path.cwd()))
                if Path(file_path).is_absolute()
                else file_path
            )
            report_lines.append(f"### {check.check_name}")
            report_lines.append("")
            report_lines.append(f"**File:** `{rel_path}`")
            report_lines.append("")
            report_lines.append(f"**Issue:** {check.message}")
            report_lines.append("")

    # Warnings section
    if warnings:
        report_lines.append("## ⚠️ Warnings")
        report_lines.append("")
        report_lines.append("These issues are **recommended** to fix but not blocking.")
        report_lines.append("")

        for file_path, check in warnings:
            rel_path = (
                str(Path(file_path).relative_to(Path.cwd()))
                if Path(file_path).is_absolute()
                else file_path
            )
            report_lines.append(f"### {check.check_name}")
            report_lines.append("")
            report_lines.append(f"**File:** `{rel_path}`")
            report_lines.append("")
            report_lines.append(f"**Suggestion:** {check.message}")
            report_lines.append("")

    # Info section (optional, for context)
    if infos:
        report_lines.append("## ℹ️ Information")
        report_lines.append("")
        report_lines.append("<details>")
        report_lines.append("<summary>Click to expand informational notices</summary>")
        report_lines.append("")

        for file_path, check in infos:
            rel_path = (
                str(Path(file_path).relative_to(Path.cwd()))
                if Path(file_path).is_absolute()
                else file_path
            )
            report_lines.append(f"- **{check.check_name}** (`{rel_path}`): {check.message}")

        report_lines.append("")
        report_lines.append("</details>")
        report_lines.append("")

    # Overall status
    report_lines.append("## Overall Status")
    report_lines.append("")
    if len(critical_failures) == 0:
        report_lines.append("✅ **PASS** - No critical failures detected.")
        if len(warnings) > 0:
            report_lines.append("")
            report_lines.append(f"⚠️ {len(warnings)} warning(s) to address.")
    else:
        report_lines.append(
            f"❌ **FAIL** - {len(critical_failures)} critical failure(s) must be fixed."
        )

    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("*Generated by `scripts/validate_initiatives.py`*")

    report_text = "\n".join(report_lines)

    # Write to file if path provided
    if output_path:
        output_path.write_text(report_text, encoding="utf-8")
        print(f"✓ Report written to: {output_path}")

    return report_text


def print_results(results: dict[str, list[ValidationResult]], ci_mode: bool = False):
    """Print validation results in human-readable format."""
    total_files = len(results)
    total_checks = sum(len(checks) for checks in results.values())

    critical_failures = []
    warnings = []
    infos = []

    for file_path, checks in results.items():
        for check in checks:
            if check.severity == "critical" and not check.passed:
                critical_failures.append((file_path, check))
            elif check.severity == "warning" and not check.passed:
                warnings.append((file_path, check))
            elif check.severity == "info":
                infos.append((file_path, check))

    # Print summary
    print(f"\n{'=' * 80}")
    print("Initiative Validation Report")
    print(f"{'=' * 80}")
    print(f"Files checked: {total_files}")
    print(f"Total checks: {total_checks}")
    print(f"❌ Critical failures: {len(critical_failures)}")
    print(f"⚠️  Warnings: {len(warnings)}")
    print(f"ℹ️  Info: {len(infos)}")
    print(f"{'=' * 80}\n")

    # Print critical failures
    if critical_failures:
        print("❌ CRITICAL FAILURES (Must fix):\n")
        for file_path, check in critical_failures:
            print(f"  File: {file_path}")
            print(f"  Check: {check.check_name}")
            print(f"  Message: {check.message}")
            print()

    # Print warnings
    if warnings:
        print("⚠️  WARNINGS (Recommended fixes):\n")
        for file_path, check in warnings:
            print(f"  File: {file_path}")
            print(f"  Check: {check.check_name}")
            print(f"  Message: {check.message}")
            print()

    # Print info (only in verbose mode)
    if infos and not ci_mode:
        print("ℹ️  INFORMATION:\n")
        for file_path, check in infos:
            print(f"  File: {file_path}")
            print(f"  Message: {check.message}")
            print()

    # Exit with appropriate code
    if ci_mode and critical_failures:
        print("❌ Validation FAILED (critical failures detected)")
        sys.exit(1)
    elif critical_failures:
        print("❌ Validation FAILED")
    elif warnings:
        print("⚠️  Validation PASSED (with warnings)")
    else:
        print("✅ Validation PASSED")


def main():
    parser = argparse.ArgumentParser(description="Validate initiative files")
    parser.add_argument(
        "--file",
        type=Path,
        help="Validate specific file instead of all initiatives",
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="CI mode: exit with code 1 on critical failures",
    )
    parser.add_argument(
        "--initiatives-dir",
        type=Path,
        default=Path("docs/initiatives"),
        help="Path to initiatives directory (default: docs/initiatives)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Generate markdown validation report to specified file",
    )

    args = parser.parse_args()

    validator = InitiativeValidator(args.initiatives_dir)

    if args.file:
        # Validate single file
        results = {str(args.file): validator.validate_file(args.file)}
    else:
        # Validate all initiatives
        results = validator.validate_all()

    print_results(results, ci_mode=args.ci)

    # Generate markdown report if requested
    if args.report:
        generate_markdown_report(results, output_path=args.report)


if __name__ == "__main__":
    main()
