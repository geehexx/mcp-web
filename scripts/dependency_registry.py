#!/usr/bin/env python3
"""
Initiative Dependency Registry

Builds and validates machine-readable dependency graph from initiative frontmatter.
Checks for unsatisfied prerequisites, circular dependencies, and blocker propagation.

Usage:
    python scripts/dependency_registry.py                  # Build registry
    python scripts/dependency_registry.py --validate       # Validate dependencies
    python scripts/dependency_registry.py --graph          # Generate graph (DOT format)
    python scripts/dependency_registry.py --blockers       # Show blocker cascade

References:
    - Initiative System Lifecycle Improvements (2025-10-19)
    - Requirements Traceability Matrix (6Sigma, 2025)
    - Dependency Management (Teamhood, 2025)
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    import frontmatter
except ImportError:
    print("ERROR: Required dependencies not installed")
    print("Install: uv add python-frontmatter pyyaml")
    sys.exit(1)


@dataclass
class InitiativeDependency:
    """Represents a dependency relationship between initiatives."""

    source_id: str  # Initiative that has the dependency
    target_id: str  # Initiative that is depended upon
    dependency_type: str  # "prerequisite", "synergistic", "blocking"
    status: str  # Current dependency status
    blocker_propagation: bool = True


@dataclass
class Initiative:
    """Initiative metadata and relationships."""

    id: str  # Unique identifier (derived from filename)
    title: str
    status: str
    priority: str
    file_path: str
    dependencies: list[InitiativeDependency] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    is_folder_based: bool = False


class DependencyRegistry:
    """Manages initiative dependency relationships."""

    def __init__(self, initiatives_dir: Path):
        self.initiatives_dir = initiatives_dir
        self.initiatives: dict[str, Initiative] = {}
        self.dependency_graph: dict[str, list[str]] = {}

    def load_initiatives(self) -> None:
        """Load all initiative files and extract metadata."""
        for directory in ["active", "completed"]:
            dir_path = self.initiatives_dir / directory
            if not dir_path.exists():
                continue

            # Folder-based initiatives
            for file_path in dir_path.glob("*/initiative.md"):
                self._load_initiative_file(file_path, is_folder_based=True)

            # Flat-file initiatives
            for file_path in dir_path.glob("*.md"):
                if file_path.name != "initiative.md":
                    self._load_initiative_file(file_path, is_folder_based=False)

    def _load_initiative_file(self, file_path: Path, is_folder_based: bool) -> None:
        """Load single initiative file and extract metadata."""
        try:
            with open(file_path, encoding="utf-8") as f:
                post = frontmatter.load(f)

            # Generate initiative ID from path
            initiative_id = file_path.parent.name if is_folder_based else file_path.stem

            # Extract basic metadata
            initiative = Initiative(
                id=initiative_id,
                title=post.metadata.get("title", self._extract_title(post.content)),
                status=post.metadata.get("Status", "Unknown"),
                priority=post.metadata.get("Priority", "Medium"),
                file_path=str(file_path),
                is_folder_based=is_folder_based,
            )

            # Parse dependencies from content
            self._parse_dependencies(post.content, initiative)

            # Parse blockers from content
            self._parse_blockers(post.content, initiative)

            self.initiatives[initiative_id] = initiative

        except Exception as e:
            print(f"Warning: Failed to load {file_path}: {e}", file=sys.stderr)

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content (first H1)."""
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        return match.group(1) if match else "Untitled"

    def _parse_dependencies(self, content: str, initiative: Initiative) -> None:
        """Parse dependency relationships from initiative content."""
        # Look for Dependencies section
        deps_section = re.search(
            r"##\s+Dependencies(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE
        )

        if not deps_section:
            return

        section_content = deps_section.group(1)

        # Parse prerequisite initiatives
        prereq_matches = re.finditer(
            r"\[([^\]]+)\]\(\.\.\/([^)]+)/initiative\.md\)",
            section_content,
        )

        for match in prereq_matches:
            target_id = match.group(2).split("/")[-1]

            # Determine dependency type from context
            dep_type = "prerequisite"
            if "synergistic" in section_content.lower():
                dep_type = "synergistic"
            elif "blocking" in section_content.lower():
                dep_type = "blocking"

            dependency = InitiativeDependency(
                source_id=initiative.id,
                target_id=target_id,
                dependency_type=dep_type,
                status="pending",  # Will be updated during validation
            )

            initiative.dependencies.append(dependency)

    def _parse_blockers(self, content: str, initiative: Initiative) -> None:
        """Parse blockers from initiative content."""
        # Look for Blockers section
        blockers_section = re.search(
            r"##\s+Blockers(.*?)(?=##|\Z)", content, re.DOTALL | re.IGNORECASE
        )

        if not blockers_section:
            return

        section_content = blockers_section.group(1)

        # Find current blockers (lines starting with -)
        current_blockers = re.search(
            r"\*\*Current Blockers:\*\*(.*?)(?=\*\*|$)",
            section_content,
            re.DOTALL,
        )

        if current_blockers:
            blocker_lines = re.findall(r"^- (.+)$", current_blockers.group(1), re.MULTILINE)
            # Filter out "None" entries
            initiative.blockers = [
                b.strip() for b in blocker_lines if not b.strip().lower().startswith("none")
            ]

    def build_dependency_graph(self) -> dict[str, list[str]]:
        """Build adjacency list representation of dependency graph."""
        graph = {}

        for initiative_id, initiative in self.initiatives.items():
            graph[initiative_id] = []
            for dep in initiative.dependencies:
                if dep.dependency_type == "prerequisite":
                    graph[initiative_id].append(dep.target_id)

        self.dependency_graph = graph
        return graph

    def validate_dependencies(self) -> list[str]:
        """Validate all dependencies and return list of issues."""
        issues = []

        for initiative_id, initiative in self.initiatives.items():
            for dep in initiative.dependencies:
                # Check 1: Target initiative exists
                if dep.target_id not in self.initiatives:
                    issues.append(
                        f"❌ {initiative_id}: Depends on non-existent initiative '{dep.target_id}'"
                    )
                    continue

                target = self.initiatives[dep.target_id]

                # Check 2: Prerequisite should not be blocked
                if dep.dependency_type == "prerequisite":
                    if target.status in ["Archived", "Superseded"]:
                        issues.append(
                            f"⚠️  {initiative_id}: Prerequisite '{dep.target_id}' is {target.status}"
                        )

                    if len(target.blockers) > 0:
                        issues.append(
                            f"🚫 {initiative_id}: Prerequisite '{dep.target_id}' is blocked: {', '.join(target.blockers)}"
                        )

                # Check 3: Active initiative shouldn't depend on incomplete prerequisite
                if (
                    initiative.status == "Active"
                    and dep.dependency_type == "prerequisite"
                    and target.status not in ["Completed", "✅ Completed"]
                ):
                    issues.append(
                        f"⚠️  {initiative_id}: Active but prerequisite '{dep.target_id}' not completed (status: {target.status})"
                    )

        return issues

    def detect_circular_dependencies(self) -> list[list[str]]:
        """Detect circular dependency chains."""
        cycles = []
        visited = set()
        rec_stack = set()

        def dfs(node: str, path: list[str]) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in self.dependency_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor, path.copy())
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_start = path.index(neighbor)
                    cycles.append(path[cycle_start:] + [neighbor])

            rec_stack.remove(node)

        for initiative_id in self.initiatives:
            if initiative_id not in visited:
                dfs(initiative_id, [])

        return cycles

    def propagate_blockers(self) -> dict[str, list[str]]:
        """Propagate blockers to dependent initiatives."""
        propagated_blockers = {}

        for initiative_id, initiative in self.initiatives.items():
            if len(initiative.blockers) == 0:
                continue

            # Find all initiatives that depend on this one
            for dep_id, dep_initiative in self.initiatives.items():
                for dep in dep_initiative.dependencies:
                    if (
                        dep.target_id == initiative_id
                        and dep.blocker_propagation
                        and dep.dependency_type == "prerequisite"
                    ):
                        if dep_id not in propagated_blockers:
                            propagated_blockers[dep_id] = []

                        propagated_blockers[dep_id].extend(
                            [
                                f"Upstream blocker in {initiative_id}: {b}"
                                for b in initiative.blockers
                            ]
                        )

        return propagated_blockers

    def generate_dot_graph(self) -> str:
        """Generate DOT format graph for visualization."""
        dot = ["digraph InitiativeDependencies {"]
        dot.append("  rankdir=LR;")
        dot.append("  node [shape=box, style=rounded];")

        # Add nodes
        for initiative_id, initiative in self.initiatives.items():
            color = "lightblue"
            if initiative.status in ["Completed", "✅ Completed"]:
                color = "lightgreen"
            elif len(initiative.blockers) > 0:
                color = "lightcoral"

            label = f"{initiative_id}\\n({initiative.status})"
            dot.append(f'  "{initiative_id}" [label="{label}", fillcolor={color}, style=filled];')

        # Add edges
        for initiative_id, initiative in self.initiatives.items():
            for dep in initiative.dependencies:
                style = "solid"
                if dep.dependency_type == "synergistic":
                    style = "dashed"

                dot.append(f'  "{initiative_id}" -> "{dep.target_id}" [style={style}];')

        dot.append("}")
        return "\n".join(dot)

    def export_registry(self, output_path: Path) -> None:
        """Export dependency registry as JSON."""
        registry_data = {
            "initiatives": {
                init_id: {
                    "title": init.title,
                    "status": init.status,
                    "priority": init.priority,
                    "file_path": init.file_path,
                    "blockers": init.blockers,
                    "dependencies": [
                        {
                            "target": dep.target_id,
                            "type": dep.dependency_type,
                            "blocker_propagation": dep.blocker_propagation,
                        }
                        for dep in init.dependencies
                    ],
                }
                for init_id, init in self.initiatives.items()
            },
            "graph": self.dependency_graph,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(registry_data, f, indent=2)

        print(f"✅ Registry exported to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Build and validate initiative dependency registry"
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate dependencies and report issues",
    )
    parser.add_argument(
        "--graph",
        action="store_true",
        help="Generate DOT graph for visualization",
    )
    parser.add_argument(
        "--blockers",
        action="store_true",
        help="Show blocker propagation cascade",
    )
    parser.add_argument(
        "--export",
        type=Path,
        help="Export registry to JSON file",
    )
    parser.add_argument(
        "--initiatives-dir",
        type=Path,
        default=Path("docs/initiatives"),
        help="Path to initiatives directory",
    )

    args = parser.parse_args()

    registry = DependencyRegistry(args.initiatives_dir)
    registry.load_initiatives()
    registry.build_dependency_graph()

    print(f"📋 Loaded {len(registry.initiatives)} initiatives")

    if args.validate:
        print("\n🔍 Validating dependencies...\n")
        issues = registry.validate_dependencies()

        if issues:
            for issue in issues:
                print(issue)
            print(f"\n❌ Found {len(issues)} dependency issues")
            sys.exit(1)
        else:
            print("✅ All dependencies valid")

        # Check for circular dependencies
        cycles = registry.detect_circular_dependencies()
        if cycles:
            print(f"\n❌ Found {len(cycles)} circular dependency chains:")
            for cycle in cycles:
                print(f"  {' → '.join(cycle)}")
            sys.exit(1)
        else:
            print("✅ No circular dependencies")

    if args.blockers:
        print("\n🚫 Blocker propagation cascade:\n")
        propagated = registry.propagate_blockers()

        if propagated:
            for initiative_id, blockers in propagated.items():
                print(f"  {initiative_id}:")
                for blocker in blockers:
                    print(f"    - {blocker}")
        else:
            print("  No blockers to propagate")

    if args.graph:
        print("\n📊 Dependency graph (DOT format):\n")
        print(registry.generate_dot_graph())
        print(
            "\nTo visualize: dot -Tpng -o graph.png <(python scripts/dependency_registry.py --graph)"
        )

    if args.export:
        registry.export_registry(args.export)


if __name__ == "__main__":
    main()
