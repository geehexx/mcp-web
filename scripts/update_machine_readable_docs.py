#!/usr/bin/env python3
"""
Intelligent machine-readable documentation regeneration with change detection.

This script implements an idempotent documentation lifecycle:
- Detects changes in workflow/rule frontmatter via hashing
- Incrementally regenerates only affected indexes
- Validates output quality and token budgets
- Maintains cache for change detection

Based on Incremental Static Regeneration (ISR) patterns.
"""

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


class DocRegenerator:
    """Intelligent documentation regenerator with change detection."""

    def __init__(self, cache_file: Path = Path(".windsurf/.doc-hashes.json")):
        """Initialize regenerator with cache file."""
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.changes_detected = False

    def _load_cache(self) -> dict[str, str]:
        """Load cached hashes from file."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file) as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save_cache(self) -> None:
        """Save current hashes to cache file."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, "w") as f:
            json.dump(self.cache, f, indent=2)

    def _hash_frontmatter(self, file_path: Path) -> str:
        """
        Extract and hash YAML frontmatter from markdown file.

        Returns stable hash of frontmatter content for change detection.
        """
        with open(file_path) as f:
            content = f.read()

        if not content.startswith("---"):
            return hashlib.sha256(b"").hexdigest()

        parts = content.split("---", 2)
        if len(parts) < 3:
            return hashlib.sha256(b"").hexdigest()

        try:
            # Parse and re-serialize to normalize formatting
            frontmatter = yaml.safe_load(parts[1])
            normalized = yaml.dump(frontmatter, sort_keys=True)
            return hashlib.sha256(normalized.encode()).hexdigest()
        except yaml.YAMLError:
            return hashlib.sha256(b"").hexdigest()

    def _extract_frontmatter(self, file_path: Path) -> dict[str, Any] | None:
        """Extract YAML frontmatter from markdown file."""
        with open(file_path) as f:
            content = f.read()

        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        try:
            return yaml.safe_load(parts[1])
        except yaml.YAMLError:
            return None

    def detect_workflow_changes(self) -> bool:
        """
        Detect changes in workflow frontmatter.

        Returns True if any workflow frontmatter changed.
        """
        workflow_dir = Path(".windsurf/workflows")
        current_hash = ""

        # Compute combined hash of all workflow frontmatter
        hashes = []
        for file_path in sorted(workflow_dir.glob("*.md")):
            hashes.append(self._hash_frontmatter(file_path))

        current_hash = hashlib.sha256("".join(hashes).encode()).hexdigest()
        cached_hash = self.cache.get("workflows", "")

        if current_hash != cached_hash:
            self.cache["workflows"] = current_hash
            return True

        return False

    def detect_rule_changes(self) -> bool:
        """
        Detect changes in rule frontmatter.

        Returns True if any rule frontmatter changed.
        """
        rules_dir = Path(".windsurf/rules")
        current_hash = ""

        # Compute combined hash of all rule frontmatter
        hashes = []
        for file_path in sorted(rules_dir.glob("*.md")):
            hashes.append(self._hash_frontmatter(file_path))

        current_hash = hashlib.sha256("".join(hashes).encode()).hexdigest()
        cached_hash = self.cache.get("rules", "")

        if current_hash != cached_hash:
            self.cache["rules"] = current_hash
            return True

        return False

    def generate_workflow_index(self) -> str:
        """Generate workflow index from frontmatter."""
        workflow_dir = Path(".windsurf/workflows")
        workflows_by_category: dict[str, list[tuple[str, dict]]] = {}

        for file_path in sorted(workflow_dir.glob("*.md")):
            frontmatter = self._extract_frontmatter(file_path)
            if not frontmatter:
                continue
            category = frontmatter.get("category", "Uncategorized")
            if category not in workflows_by_category:
                workflows_by_category[category] = []
            workflows_by_category[category].append((file_path.name, frontmatter))

        # Generate markdown with frontmatter
        lines = [
            "---",
            "type: machine-readable-reference",
            "category: auto-generated",
            "purpose: Auto-generated index of all workflows with metadata",
            "token_budget: low",
            "audience: ai-agent",
            "auto_generated: true",
            "maintenance: auto",
            f'last_updated: "{datetime.now().strftime("%Y-%m-%d")}"',
            'tags: ["workflows", "index", "auto-generated"]',
            "---",
            "",
            "# Workflow Index",
            "",
            "**Generated:** Auto-generated from frontmatter",
            "",
        ]

        for category in sorted(workflows_by_category.keys()):
            lines.append(f"## {category} Workflows")
            lines.append("")
            lines.append("| Workflow | Complexity | Tokens | Dependencies | Status |")
            lines.append("|----------|------------|--------|--------------|--------|")

            for name, fm in sorted(workflows_by_category[category], key=lambda x: x[0]):
                deps = ", ".join(fm.get("dependencies", []))
                if not deps:
                    deps = "-"
                lines.append(
                    f"| [{name[:-3]}]({name}) | {fm.get('complexity', 'N/A')} | "
                    f"{fm.get('tokens', 'N/A')} | {deps} | {fm.get('status', 'unknown')} |"
                )

            lines.append("")

        return "\n".join(lines)

    def generate_rule_index(self) -> str:
        """Generate rule index from frontmatter."""
        rules_dir = Path(".windsurf/rules")
        rules_by_priority: dict[str, list[tuple[str, dict]]] = {}

        for file_path in sorted(rules_dir.glob("*.md")):
            frontmatter = self._extract_frontmatter(file_path)
            if not frontmatter:
                continue
            priority = frontmatter.get("priority", "medium")
            if priority not in rules_by_priority:
                rules_by_priority[priority] = []
            rules_by_priority[priority].append((file_path.name, frontmatter))

        # Generate markdown with frontmatter
        lines = [
            "---",
            "type: machine-readable-reference",
            "category: auto-generated",
            "purpose: Auto-generated index of all agent rules with metadata",
            "token_budget: low",
            "audience: ai-agent",
            "auto_generated: true",
            "maintenance: auto",
            f'last_updated: "{datetime.now().strftime("%Y-%m-%d")}"',
            'tags: ["rules", "index", "auto-generated"]',
            "---",
            "",
            "# Rule Index",
            "",
            "**Generated:** Auto-generated from frontmatter",
            "",
        ]

        priority_order = ["high", "medium", "low"]
        for priority in priority_order:
            if priority not in rules_by_priority:
                continue

            lines.append(f"## {priority.capitalize()} Priority Rules")
            lines.append("")
            lines.append("| Rule | Category | Tokens | Apply To | Status |")
            lines.append("|------|----------|--------|----------|--------|")

            for name, fm in sorted(rules_by_priority[priority], key=lambda x: x[0]):
                apply_to = ", ".join(fm.get("applyTo", []))
                if not apply_to:
                    apply_to = "-"
                lines.append(
                    f"| [{name[:-3]}]({name}) | {fm.get('category', 'N/A')} | "
                    f"{fm.get('tokens', 'N/A')} | {apply_to} | {fm.get('status', 'unknown')} |"
                )

            lines.append("")

        return "\n".join(lines)

    def generate_dependency_graph(self) -> str:
        """Generate workflow dependency graph."""
        workflow_dir = Path(".windsurf/workflows")
        workflows: dict[str, dict] = {}

        for file_path in sorted(workflow_dir.glob("*.md")):
            frontmatter = self._extract_frontmatter(file_path)
            if frontmatter:
                workflows[file_path.stem] = frontmatter

        # Generate Mermaid diagram with frontmatter
        lines = [
            "---",
            "type: machine-readable-reference",
            "category: auto-generated",
            "purpose: Auto-generated dependency graph of all workflows",
            "token_budget: low",
            "audience: ai-agent",
            "auto_generated: true",
            "maintenance: auto",
            f'last_updated: "{datetime.now().strftime("%Y-%m-%d")}"',
            'tags: ["workflows", "dependencies", "graph", "auto-generated"]',
            "---",
            "",
            "# Workflow Dependencies",
            "",
            "**Generated:** Auto-generated from frontmatter",
            "",
            "## Dependency Graph",
            "",
            "```mermaid",
            "graph TD",
        ]

        # Add nodes and edges
        for name, fm in workflows.items():
            deps = fm.get("dependencies", [])
            for dep in deps:
                lines.append(f"    {name}[{name}] --> {dep}[{dep}]")

        lines.append("```")
        lines.append("")

        # Add dependency table
        lines.append("## Dependency Details")
        lines.append("")
        lines.append("| Workflow | Dependencies | Complexity |")
        lines.append("|----------|--------------|------------|")

        for name, fm in sorted(workflows.items()):
            deps = fm.get("dependencies", [])
            deps_str = ", ".join(deps) if deps else "None"
            complexity = fm.get("complexity", "N/A")
            lines.append(f"| {name} | {deps_str} | {complexity} |")

        return "\n".join(lines)

    def validate_token_budget(self, content: str, max_words: int = 1000) -> bool:
        """
        Validate that generated content meets token budget.

        Args:
            content: Generated markdown content
            max_words: Maximum word count (proxy for tokens)

        Returns:
            True if within budget, False otherwise
        """
        word_count = len(content.split())
        return word_count <= max_words

    def regenerate(self, force: bool = False) -> int:
        """
        Intelligently regenerate machine-readable documentation.

        Args:
            force: If True, regenerate all regardless of changes

        Returns:
            0 on success, 1 on error
        """
        print("🔍 Detecting changes in workflows and rules...")

        workflow_changed = self.detect_workflow_changes()
        rule_changed = self.detect_rule_changes()

        if not force and not workflow_changed and not rule_changed:
            print("✅ No changes detected. Documentation is up-to-date.")
            return 0

        print()
        if workflow_changed or force:
            print("📝 Regenerating workflow documentation...")

            # Generate workflow index
            workflow_index = self.generate_workflow_index()
            workflow_index_path = Path(".windsurf/docs/workflow-index.md")

            if not self.validate_token_budget(workflow_index, max_words=1000):
                print("  ⚠️  Warning: workflow-index.md exceeds token budget")

            workflow_index_path.write_text(workflow_index)
            print(f"  ✅ Generated {workflow_index_path}")

            # Generate dependency graph
            dependency_graph = self.generate_dependency_graph()
            dependency_graph_path = Path(".windsurf/docs/workflow-dependencies.md")

            if not self.validate_token_budget(dependency_graph, max_words=1000):
                print("  ⚠️  Warning: workflow-dependencies.md exceeds token budget")

            dependency_graph_path.write_text(dependency_graph)
            print(f"  ✅ Generated {dependency_graph_path}")

        if rule_changed or force:
            print("📝 Regenerating rule documentation...")

            # Generate rule index
            rule_index = self.generate_rule_index()
            rule_index_path = Path(".windsurf/docs/rules-index.md")

            if not self.validate_token_budget(rule_index, max_words=1000):
                print("  ⚠️  Warning: rules-index.md exceeds token budget")

            rule_index_path.write_text(rule_index)
            print(f"  ✅ Generated {rule_index_path}")

        # Save cache
        self._save_cache()
        print()
        print("✅ Machine-readable documentation updated successfully")
        return 0


def main() -> int:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Intelligently regenerate machine-readable documentation"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force regeneration regardless of changes",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check if regeneration is needed (exit 1 if needed)",
    )

    args = parser.parse_args()

    regenerator = DocRegenerator()

    if args.check:
        workflow_changed = regenerator.detect_workflow_changes()
        rule_changed = regenerator.detect_rule_changes()

        if workflow_changed or rule_changed:
            print("⚠️  Changes detected. Regeneration needed.")
            return 1
        else:
            print("✅ No changes detected.")
            return 0

    return regenerator.regenerate(force=args.force)


if __name__ == "__main__":
    sys.exit(main())
