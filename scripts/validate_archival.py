#!/usr/bin/env python3
"""
Archival Validation Script

Multi-gate validation system for initiative archival. Ensures completeness
before moving initiatives to completed/ directory.

Usage:
    python scripts/validate_archival.py path/to/initiative.md
    python scripts/validate_archival.py path/to/initiative.md --force --reason "Superseded by X"
    python scripts/validate_archival.py path/to/initiative.md --report path/to/report.md

References:
    - Initiative System Lifecycle Improvements Phase 5 (2025-10-19)
    - Quality Gates (PMI/DTU ProjectLab, 2025)
    - Stage-Gate Process (ProjectManager, 2025)
"""

import argparse
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

try:
    import frontmatter
except ImportError:
    print("ERROR: Required dependencies not installed")
    print("Install: uv add python-frontmatter pyyaml")
    sys.exit(1)


@dataclass
class GateResult:
    """Result of a single validation gate check."""

    gate_name: str
    severity: str  # "critical", "warning"
    passed: bool
    message: str
    details: str | None = None


class ArchivalValidator:
    """Validates initiatives against archival gates."""

    def __init__(self, initiative_path: Path):
        self.initiative_path = initiative_path
        self.gates: list[GateResult] = []
        self.content: str = ""
        self.frontmatter_data: dict = {}

    def load_initiative(self) -> bool:
        """Load initiative file and parse frontmatter."""
        try:
            with open(self.initiative_path, encoding="utf-8") as f:
                post = frontmatter.load(f)
                self.content = post.content
                self.frontmatter_data = post.metadata
            return True
        except Exception as e:
            print(f"❌ Failed to load initiative: {e}")
            return False

    def check_status_gate(self) -> GateResult:
        """Gate 1: Status must be 'Completed' or '✅ Completed'."""
        status = self.frontmatter_data.get("Status", "")
        valid_statuses = ["Completed", "✅ Completed"]

        passed = status in valid_statuses
        message = f"Status: {status}"

        if not passed:
            details = f"Expected: {' or '.join(valid_statuses)}, Got: {status}"
        else:
            details = "Initiative marked as completed"

        return GateResult(
            gate_name="Status Completion",
            severity="critical",
            passed=passed,
            message=message,
            details=details,
        )

    def check_success_criteria_gate(self) -> GateResult:
        """Gate 2: All success criteria checkboxes must be checked."""
        # Find Success Criteria section
        success_section_match = re.search(
            r"##\s+Success\s+(Criteria|Metrics)", self.content, re.IGNORECASE
        )

        if not success_section_match:
            return GateResult(
                gate_name="Success Criteria",
                severity="warning",
                passed=True,
                message="No Success Criteria section found",
                details="Initiative does not define explicit success criteria",
            )

        # Extract section content (until next ## or end of file)
        section_start = success_section_match.end()
        next_section_match = re.search(r"\n##\s+", self.content[section_start:])
        if next_section_match:
            section_content = self.content[
                section_start : section_start + next_section_match.start()
            ]
        else:
            section_content = self.content[section_start:]

        # Count checked vs unchecked boxes
        checked = len(re.findall(r"- \[x\]", section_content, re.IGNORECASE))
        unchecked = len(re.findall(r"- \[ \]", section_content))
        total = checked + unchecked

        passed = unchecked == 0 and total > 0
        message = f"{checked}/{total} success criteria met"

        if not passed and total == 0:
            details = "No checkboxes found in Success Criteria section"
        elif not passed:
            details = f"{unchecked} criteria remain unchecked"
        else:
            details = None

        return GateResult(
            gate_name="Success Criteria",
            severity="critical",
            passed=passed,
            message=message,
            details=details,
        )

    def check_blockers_gate(self) -> GateResult:
        """Gate 3: All blockers must be resolved."""
        # Check for Blockers section in content
        blockers_section_match = re.search(r"##\s+Blockers", self.content, re.IGNORECASE)

        if not blockers_section_match:
            return GateResult(
                gate_name="Blockers",
                severity="warning",
                passed=True,
                message="No blockers section found",
                details="Initiative has no documented blockers",
            )

        # Extract blockers section
        section_start = blockers_section_match.end()
        next_section_match = re.search(r"\n##\s+", self.content[section_start:])
        if next_section_match:
            section_content = self.content[
                section_start : section_start + next_section_match.start()
            ]
        else:
            section_content = self.content[section_start:]

        # Look for "Current Blockers" subsection
        current_blockers_match = re.search(
            r"(?:Current|Active)\s+Blockers", section_content, re.IGNORECASE
        )

        # Check if section says "None"
        if not current_blockers_match and re.search(
            r"(?:None|No blockers)", section_content, re.IGNORECASE
        ):
            return GateResult(
                gate_name="Blockers",
                severity="warning",
                passed=True,
                message="No active blockers",
                details="Blockers section indicates no current blockers",
            )

        # Look for list items in Current Blockers
        current_start = current_blockers_match.end() if current_blockers_match else 0
        current_section = section_content[current_start:200]  # First 200 chars after heading

        active_blockers = re.findall(r"- .+", current_section)
        active_blockers = [
            b for b in active_blockers if not re.search(r"None|No blockers", b, re.IGNORECASE)
        ]

        passed = len(active_blockers) == 0
        message = (
            f"{len(active_blockers)} active blocker(s)" if active_blockers else "No active blockers"
        )

        if not passed:
            details = f"Resolve these blockers before archival: {', '.join(active_blockers[:3])}"
        else:
            details = "No blockers found"

        return GateResult(
            gate_name="Blockers",
            severity="warning",
            passed=passed,
            message=message,
            details=details,
        )

    def check_dependencies_gate(self) -> GateResult:
        """Gate 4: No initiatives should depend on this one."""
        # Import dependency registry to check dependents
        try:
            from dependency_registry import DependencyRegistry

            registry = DependencyRegistry(Path("docs/initiatives"))
            registry.load_initiatives()
            registry.build_dependency_graph()

            # Get initiative ID from path
            initiative_id = self.initiative_path.parent.name
            if initiative_id in ["active", "completed"]:
                # Flat-file initiative
                initiative_id = self.initiative_path.stem

            # Find dependents
            dependents = []
            for init_id, initiative in registry.initiatives.items():
                for dep in initiative.dependencies:
                    if dep.target_id == initiative_id:
                        dependents.append(init_id)

            passed = len(dependents) == 0
            message = (
                f"{len(dependents)} dependent initiative(s)" if dependents else "No dependents"
            )
            details = None

            if not passed:
                details = f"These initiatives depend on this one: {', '.join(dependents)}"

            return GateResult(
                gate_name="Dependencies",
                severity="critical",
                passed=passed,
                message=message,
                details=details,
            )

        except ImportError:
            return GateResult(
                gate_name="Dependencies",
                severity="warning",
                passed=True,
                message="Dependency check skipped (dependency_registry not found)",
                details="Unable to validate dependencies",
            )
        except Exception as e:
            return GateResult(
                gate_name="Dependencies",
                severity="warning",
                passed=True,
                message=f"Dependency check error: {e}",
                details="Validation incomplete",
            )

    def check_documentation_gate(self) -> GateResult:
        """Gate 5: Updates section should have completion entry."""
        # Find Updates section
        updates_match = re.search(r"##\s+Updates", self.content, re.IGNORECASE)

        if not updates_match:
            return GateResult(
                gate_name="Documentation",
                severity="warning",
                passed=False,
                message="No Updates section found",
                details="Add completion entry to Updates section",
            )

        # Extract section
        section_start = updates_match.end()
        next_section_match = re.search(r"\n##\s+", self.content[section_start:])
        if next_section_match:
            section_content = self.content[
                section_start : section_start + next_section_match.start()
            ]
        else:
            section_content = self.content[section_start:]

        # Look for completion keywords
        completion_keywords = ["complete", "finished", "done", "implemented", "delivered"]
        has_completion = any(keyword in section_content.lower() for keyword in completion_keywords)

        passed = has_completion
        message = "Completion documented" if passed else "No completion entry found"
        details = (
            None if passed else "Add completion entry with date and summary to Updates section"
        )

        return GateResult(
            gate_name="Documentation",
            severity="warning",
            passed=passed,
            message=message,
            details=details,
        )

    def validate_all_gates(self) -> list[GateResult]:
        """Run all validation gates."""
        self.gates = [
            self.check_status_gate(),
            self.check_success_criteria_gate(),
            self.check_blockers_gate(),
            self.check_dependencies_gate(),
            self.check_documentation_gate(),
        ]
        return self.gates

    def get_summary(self) -> dict:
        """Get validation summary."""
        critical_failures = [g for g in self.gates if not g.passed and g.severity == "critical"]
        warning_failures = [g for g in self.gates if not g.passed and g.severity == "warning"]

        return {
            "total_gates": len(self.gates),
            "passed": len([g for g in self.gates if g.passed]),
            "failed": len([g for g in self.gates if not g.passed]),
            "critical_failures": len(critical_failures),
            "warning_failures": len(warning_failures),
            "archival_allowed": len(critical_failures) == 0,
        }

    def generate_report(self) -> str:
        """Generate markdown validation report."""
        lines = []
        lines.append("# Archival Validation Report")
        lines.append("")
        lines.append(f"**Initiative:** `{self.initiative_path}`")
        lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        summary = self.get_summary()
        lines.append("## Summary")
        lines.append("")
        lines.append(f"- **Total gates:** {summary['total_gates']}")
        lines.append(f"- **Passed:** {summary['passed']}")
        lines.append(f"- **Failed:** {summary['failed']}")
        lines.append(f"  - Critical: {summary['critical_failures']}")
        lines.append(f"  - Warnings: {summary['warning_failures']}")
        lines.append("")

        if summary["archival_allowed"]:
            lines.append("**✅ ARCHIVAL ALLOWED** (all critical gates passed)")
        else:
            lines.append("**❌ ARCHIVAL BLOCKED** (critical gate failures)")

        lines.append("")

        # Gate results
        lines.append("## Gate Results")
        lines.append("")
        lines.append("| Gate | Severity | Status | Message |")
        lines.append("|------|----------|--------|---------|")

        for gate in self.gates:
            status = "✅ PASS" if gate.passed else "❌ FAIL"
            lines.append(
                f"| {gate.gate_name} | {gate.severity.upper()} | {status} | {gate.message} |"
            )

        lines.append("")

        # Failed gates details
        failed_gates = [g for g in self.gates if not g.passed]
        if failed_gates:
            lines.append("## Failed Gates")
            lines.append("")

            for gate in failed_gates:
                lines.append(f"### {gate.gate_name} ({gate.severity.upper()})")
                lines.append("")
                lines.append(f"**Status:** {gate.message}")
                if gate.details:
                    lines.append("")
                    lines.append(f"**Details:** {gate.details}")
                lines.append("")

        # Recommendations
        lines.append("## Recommendations")
        lines.append("")

        critical_failed = [g for g in self.gates if not g.passed and g.severity == "critical"]
        warning_failed = [g for g in self.gates if not g.passed and g.severity == "warning"]

        if critical_failed:
            lines.append("**Critical Actions Required:**")
            lines.append("")
            for gate in critical_failed:
                lines.append(f"- [ ] {gate.gate_name}: {gate.details or gate.message}")
            lines.append("")
            lines.append("These must be resolved before archival.")
            lines.append("")

        if warning_failed:
            lines.append("**Recommended Actions:**")
            lines.append("")
            for gate in warning_failed:
                lines.append(f"- [ ] {gate.gate_name}: {gate.details or gate.message}")
            lines.append("")
            lines.append("These can be bypassed with `--force` and justification.")
            lines.append("")

        if not critical_failed and not warning_failed:
            lines.append("No actions required. Initiative ready for archival.")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("*Generated by `scripts/validate_archival.py`*")

        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validate initiative for archival readiness")
    parser.add_argument(
        "initiative_file",
        type=Path,
        help="Path to initiative file (e.g., docs/initiatives/active/2025-10-19-example/initiative.md)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow archival despite gate failures (requires --reason)",
    )
    parser.add_argument(
        "--reason",
        type=str,
        help="Justification for bypassing gate failures (required with --force)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        help="Generate validation report to specified path",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress output (only show summary)",
    )

    args = parser.parse_args()

    # Validate arguments
    if args.force and not args.reason:
        parser.error("--force requires --reason to document bypass justification")

    # Load and validate
    validator = ArchivalValidator(args.initiative_file)

    if not validator.load_initiative():
        sys.exit(1)

    gates = validator.validate_all_gates()
    summary = validator.get_summary()

    # Print results (unless quiet)
    if not args.quiet:
        print(f"\n📋 Archival Validation: {args.initiative_file.name}")
        print(f"{'=' * 60}\n")

        for gate in gates:
            emoji = "✅" if gate.passed else "❌"
            severity = f"[{gate.severity.upper()}]"
            print(f"{emoji} {severity:12} {gate.gate_name:20} {gate.message}")
            if not gate.passed and gate.details:
                print(f"   └─ {gate.details}")

        print(f"\n{'=' * 60}")
        print(f"Passed: {summary['passed']}/{summary['total_gates']}")
        print(f"Critical failures: {summary['critical_failures']}")
        print(f"Warning failures: {summary['warning_failures']}")
        print("")

        if summary["archival_allowed"]:
            print("✅ ARCHIVAL ALLOWED")
        else:
            print("❌ ARCHIVAL BLOCKED")
            if not args.force:
                print('\nResolve critical failures or use --force --reason "justification"')

    # Generate report if requested
    if args.report:
        report = validator.generate_report()
        args.report.write_text(report, encoding="utf-8")
        if not args.quiet:
            print(f"\n📄 Report written to: {args.report}")

    # Handle force bypass
    if args.force:
        if not args.quiet:
            print(f"\n⚠️  FORCE BYPASS: {args.reason}")
            print("✅ Archival permitted despite gate failures")
        sys.exit(0)

    # Exit with appropriate code
    sys.exit(0 if summary["archival_allowed"] else 1)


if __name__ == "__main__":
    main()
