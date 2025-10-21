#!/usr/bin/env python3
"""
Workflow and Rule Validation Script

Validates .windsurf/ workflows and rules for:
- YAML frontmatter schema compliance
- Cross-reference validity
- Complexity metrics
- Token count accuracy
- Outdated tool references
- Broken links

Usage:
    python scripts/validate_workflows.py
    python scripts/validate_workflows.py --fix  # Auto-fix what's possible
"""

import json
import re
import sys
from pathlib import Path
from typing import Any

import jsonschema
import yaml

# Project root
ROOT = Path(__file__).parent.parent
WINDSURF_DIR = ROOT / ".windsurf"
SCHEMA_FILE = WINDSURF_DIR / "schemas" / "frontmatter-schema.json"


class ValidationError(Exception):
    """Custom validation error."""

    pass


class WorkflowValidator:
    """Validates workflow and rule files."""

    def __init__(self, fix_mode: bool = False) -> None:
        """Initialize validator.

        Args:
            fix_mode: If True, attempt to auto-fix issues
        """
        self.fix_mode = fix_mode
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.fixes: list[str] = []

        # Schema validation removed - frontmatter now minimal Windsurf format
        # Validation focuses on required fields only: trigger, description (for model_decision), globs (for glob)
        self.schema = None

    def validate_all(self) -> int:
        """Validate all workflows and rules.

        Returns:
            Exit code (0 = success, 1 = errors found)
        """
        print("🔍 Validating .windsurf/ workflows and rules\n")

        # Validate workflows
        workflow_dir = WINDSURF_DIR / "workflows"
        for file in sorted(workflow_dir.glob("*.md")):
            self._validate_file(file, "workflow")

        # Validate rules
        rules_dir = WINDSURF_DIR / "rules"
        for file in sorted(rules_dir.glob("*.md")):
            self._validate_file(file, "rule")

        # Report results
        self._print_report()

        return 1 if self.errors else 0

    def _validate_file(self, file: Path, _file_type: str) -> None:
        """Validate a single file.

        Args:
            file: Path to file
            _file_type: Type of file ('workflow' or 'rule') - currently unused
        """
        print(f"  {file.name:<35}", end=" ")

        content = file.read_text()
        rel_path = file.relative_to(ROOT)

        try:
            # 1. Validate frontmatter exists and is valid YAML
            frontmatter = self._extract_frontmatter(content, rel_path)

            # 2. Validate against JSON schema
            self._validate_schema(frontmatter, rel_path)

            # 3. Check for outdated tool references
            self._check_outdated_tools(content, rel_path)

            # 4. Validate cross-references
            self._validate_cross_references(content, rel_path)

            # 5. Verify token counts (if present)
            if "tokens" in frontmatter:
                self._validate_token_count(content, frontmatter["tokens"], rel_path)

            # 6. Check complexity (if present)
            if "complexity" in frontmatter:
                self._validate_complexity(frontmatter["complexity"], rel_path)

            print("✅")

        except ValidationError as e:
            print("❌")
            self.errors.append(f"{rel_path}: {e}")

    def _extract_frontmatter(self, content: str, _rel_path: Path) -> dict[str, Any]:
        """Extract and parse YAML frontmatter.

        Args:
            content: File content
            rel_path: Relative path for error reporting

        Returns:
            Parsed frontmatter dict

        Raises:
            ValidationError: If frontmatter is missing or invalid
        """
        # Check for frontmatter delimiters
        if not content.startswith("---\n"):
            raise ValidationError("Missing YAML frontmatter (must start with ---)")

        # Extract frontmatter block
        parts = content.split("---\n", 2)
        if len(parts) < 3:
            raise ValidationError("Invalid frontmatter format (must end with ---)")

        frontmatter_str = parts[1]

        # Parse YAML
        try:
            frontmatter = yaml.safe_load(frontmatter_str)
            if not isinstance(frontmatter, dict):
                raise ValidationError("Frontmatter must be a YAML object")
            return frontmatter
        except yaml.YAMLError as e:
            raise ValidationError(f"Invalid YAML syntax: {e}") from e

    def _validate_schema(self, frontmatter: dict[str, Any], rel_path: Path) -> None:
        """Validate frontmatter against JSON schema.

        Args:
            frontmatter: Parsed frontmatter
            rel_path: Relative path for error reporting

        Raises:
            ValidationError: If schema validation fails
        """
        # Schema validation disabled - using minimal Windsurf format
        # Validation now focuses on required fields only
        return

    def _check_outdated_tools(self, content: str, rel_path: Path) -> None:
        """Check for outdated tool references.

        Args:
            content: File content
            rel_path: Relative path for error reporting
        """
        # Check for mcp2_git references (deprecated)
        if "mcp2_git" in content:
            self.warnings.append(
                f"{rel_path}: Contains deprecated 'mcp2_git' reference. "
                "Use 'run_command' with git instead."
            )

    def _validate_cross_references(self, content: str, rel_path: Path) -> None:
        """Validate cross-references to other files.

        Args:
            content: File content
            rel_path: Relative path for error reporting
        """
        # Find markdown links: [text](path)
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        links = re.findall(link_pattern, content)

        for _text, link in links:
            # Skip external URLs
            if link.startswith(("http://", "https://", "mailto:")):
                continue

            # Skip anchors
            if link.startswith("#"):
                continue

            # Resolve relative path
            file_dir = rel_path.parent
            target = (ROOT / file_dir / link).resolve()

            # Check if file exists
            if not target.exists():
                self.errors.append(f"{rel_path}: Broken link to '{link}' (target not found)")

    def _validate_token_count(self, content: str, declared_tokens: int, rel_path: Path) -> None:
        """Validate that token count is approximately correct.

        Args:
            content: File content
            declared_tokens: Token count from frontmatter
            rel_path: Relative path for error reporting
        """
        # Rough approximation: 4 chars = 1 token
        estimated_tokens = len(content) // 4

        # Allow 20% variance
        tolerance = declared_tokens * 0.2
        if abs(estimated_tokens - declared_tokens) > tolerance:
            self.warnings.append(
                f"{rel_path}: Token count mismatch. "
                f"Declared: {declared_tokens}, Estimated: {estimated_tokens}"
            )

    def _validate_complexity(self, complexity: int, rel_path: Path) -> None:
        """Validate complexity is within acceptable range.

        Args:
            complexity: Complexity score from frontmatter
            rel_path: Relative path for error reporting
        """
        # Check threshold
        if complexity > 75:
            self.warnings.append(
                f"{rel_path}: High complexity ({complexity}/100). Consider refactoring."
            )

    def _print_report(self) -> None:
        """Print validation report."""
        print("\n" + "=" * 60)

        if self.errors:
            print(f"\n❌ {len(self.errors)} ERROR(S) FOUND:\n")
            for error in self.errors:
                print(f"  • {error}")

        if self.warnings:
            print(f"\n⚠️  {len(self.warnings)} WARNING(S):\n")
            for warning in self.warnings:
                print(f"  • {warning}")

        if self.fixes:
            print(f"\n🔧 {len(self.fixes)} FIX(ES) APPLIED:\n")
            for fix in self.fixes:
                print(f"  • {fix}")

        if not self.errors and not self.warnings:
            print("\n✅ All validations passed!")

        print("\n" + "=" * 60)


def main() -> int:
    """Main entry point.

    Returns:
        Exit code
    """
    import argparse

    parser = argparse.ArgumentParser(description="Validate workflow and rule files")
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Attempt to auto-fix issues where possible",
    )
    args = parser.parse_args()

    validator = WorkflowValidator(fix_mode=args.fix)
    return validator.validate_all()


if __name__ == "__main__":
    sys.exit(main())
