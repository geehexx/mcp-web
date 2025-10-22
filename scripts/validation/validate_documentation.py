#!/usr/bin/env python3
"""Validate documentation consistency across the project.

This script checks for:
- Accurate file counts in documentation
- Cross-reference validity
- List consistency (ADRs, workflows, rules, guides)
- Missing or outdated references
"""

import re
import sys
from pathlib import Path

# Project root
ROOT = Path(__file__).parent.parent


def count_files(directory: Path, pattern: str = "*.md") -> int:
    """Count files matching pattern in directory."""
    if not directory.exists():
        return 0
    return len(list(directory.glob(pattern)))


def get_numbered_adrs(adr_dir: Path) -> list[str]:
    """Get list of numbered ADR files."""
    return sorted([f.stem for f in adr_dir.glob("[0-9]*.md")])


def get_workflow_files(workflow_dir: Path) -> list[str]:
    """Get list of workflow files."""
    return sorted([f.stem for f in workflow_dir.glob("*.md")])


def get_rule_files(rule_dir: Path) -> list[str]:
    """Get list of rule files."""
    return sorted([f.stem for f in rule_dir.glob("*.md")])


def get_guide_files(guide_dir: Path) -> list[str]:
    """Get list of guide files."""
    return sorted([f.stem for f in guide_dir.glob("*.md")])


def check_documentation_structure() -> list[str]:
    """Check DOCUMENTATION_STRUCTURE.md for accurate counts."""
    errors = []
    doc_file = ROOT / "docs" / "DOCUMENTATION_STRUCTURE.md"

    if not doc_file.exists():
        return ["DOCUMENTATION_STRUCTURE.md not found"]

    content = doc_file.read_text()

    # Count actual files
    actual_workflows = count_files(ROOT / ".windsurf" / "workflows")
    actual_rules = count_files(ROOT / ".windsurf" / "rules")
    actual_adrs = len(get_numbered_adrs(ROOT / "docs" / "adr"))

    # Check workflow count
    workflow_match = re.search(r"workflows/\s+#.*\((\d+)\s+workflows\)", content)
    if workflow_match:
        documented_workflows = int(workflow_match.group(1))
        if documented_workflows != actual_workflows:
            errors.append(
                f"Workflow count mismatch: documented={documented_workflows}, "
                f"actual={actual_workflows}"
            )

    # Check rule count
    rule_match = re.search(r"rules/\s+#.*\((\d+)\s+rules\)", content)
    if rule_match:
        documented_rules = int(rule_match.group(1))
        if documented_rules != actual_rules:
            errors.append(
                f"Rule count mismatch: documented={documented_rules}, actual={actual_rules}"
            )

    # Check ADR count
    adr_match = re.search(r"\.\.\.\s+\((\d+)\s+ADRs total\)", content)
    if adr_match:
        documented_adrs = int(adr_match.group(1))
        if documented_adrs != actual_adrs:
            errors.append(f"ADR count mismatch: documented={documented_adrs}, actual={actual_adrs}")

    return errors


def check_adr_readme() -> list[str]:
    """Check ADR README.md has all ADRs listed."""
    errors = []
    adr_readme = ROOT / "docs" / "adr" / "README.md"

    if not adr_readme.exists():
        return ["ADR README.md not found"]

    content = adr_readme.read_text()
    actual_adrs = get_numbered_adrs(ROOT / "docs" / "adr")

    # Extract ADR numbers from README
    documented_adrs = set()
    for match in re.finditer(r"\[(\d{4})\]", content):
        documented_adrs.add(match.group(1))

    # Check for missing ADRs in README
    for adr in actual_adrs:
        adr_num = adr.split("-")[0]
        if adr_num not in documented_adrs:
            errors.append(f"ADR {adr_num} exists but not listed in README.md: {adr}")

    return errors


def check_project_summary() -> list[str]:
    """Check PROJECT_SUMMARY.md for accurate references."""
    errors = []
    summary_file = ROOT / "PROJECT_SUMMARY.md"

    if not summary_file.exists():
        return ["PROJECT_SUMMARY.md not found"]

    content = summary_file.read_text()

    # Check for ADR references
    adr_refs = set(re.findall(r"ADR-(\d{4})", content))
    actual_adrs = {adr.split("-")[0] for adr in get_numbered_adrs(ROOT / "docs" / "adr")}

    # Check for non-existent ADR references
    for adr_ref in adr_refs:
        if adr_ref not in actual_adrs:
            errors.append(f"PROJECT_SUMMARY.md references non-existent ADR-{adr_ref}")

    return errors


def check_agents_md() -> list[str]:
    """Check AGENTS.md for broken links."""
    errors = []
    agents_file = ROOT / "AGENTS.md"

    if not agents_file.exists():
        return ["AGENTS.md not found"]

    content = agents_file.read_text()

    # Extract markdown links (excluding code blocks)
    in_code_block = False
    links = []

    for line in content.split("\n"):
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue

        if not in_code_block:
            # Find markdown links [text](url)
            for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", line):
                link = match.group(2)
                # Skip external links and placeholders
                if not link.startswith(("http://", "https://", "#")) and not link.startswith(
                    ("relative/path/to", "path/to")
                ):
                    links.append(link)

    # Check if files exist
    for link in links:
        # Remove anchor
        file_path = link.split("#")[0]
        if (
            file_path
            and not (ROOT / file_path).exists()
            and not (ROOT / "docs" / file_path).exists()
        ):
            errors.append(f"AGENTS.md broken link: {link}")

    return errors


def check_cross_references() -> list[str]:
    """Check for broken cross-references in workflows and rules."""
    errors = []

    # Check workflow cross-references
    workflow_dir = ROOT / ".windsurf" / "workflows"
    for workflow_file in workflow_dir.glob("*.md"):
        content = workflow_file.read_text()

        # Find relative workflow links
        for match in re.finditer(r"\]\(\./([^)]+)\)", content):
            target = match.group(1).split("#")[0]
            if target and not (workflow_dir / target).exists():
                errors.append(f"{workflow_file.name} has broken workflow link: ./{target}")

    # Check ADR references
    for search_dir in [ROOT / ".windsurf", ROOT / "docs"]:
        for file in search_dir.rglob("*.md"):
            content = file.read_text()

            # Find ADR references
            for match in re.finditer(r"ADR-(\d{4})", content):
                adr_num = match.group(1)
                # Skip placeholder patterns
                if "X" in adr_num:
                    continue

                # Check if ADR exists
                adr_files = list((ROOT / "docs" / "adr").glob(f"{adr_num}-*.md"))
                if not adr_files:
                    errors.append(f"{file.relative_to(ROOT)} references non-existent ADR-{adr_num}")

    return errors


def main() -> int:
    """Run all validation checks."""
    print("🔍 Validating documentation consistency...\n")

    all_errors = []

    # Run checks
    checks = [
        ("DOCUMENTATION_STRUCTURE.md", check_documentation_structure),
        ("ADR README.md", check_adr_readme),
        ("PROJECT_SUMMARY.md", check_project_summary),
        ("AGENTS.md", check_agents_md),
        ("Cross-references", check_cross_references),
    ]

    for check_name, check_func in checks:
        print(f"Checking {check_name}...", end=" ")
        errors = check_func()
        if errors:
            print(f"❌ {len(errors)} error(s)")
            all_errors.extend([f"  [{check_name}] {err}" for err in errors])
        else:
            print("✅")

    # Print summary
    print("\n" + "=" * 60)
    if all_errors:
        print(f"❌ Found {len(all_errors)} validation error(s):\n")
        for error in all_errors:
            print(error)
        return 1
    else:
        print("✅ All documentation validation checks passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
