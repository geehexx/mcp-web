#!/usr/bin/env python3
"""Generate documentation indexes from YAML frontmatter."""

import sys
from datetime import datetime
from pathlib import Path

import yaml


def extract_frontmatter(file_path: Path) -> dict | None:
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


def generate_workflow_index() -> str:
    """Generate workflow index."""
    workflow_dir = Path(".windsurf/workflows")
    workflows_by_category: dict[str, list[tuple[str, dict]]] = {}

    for file_path in sorted(workflow_dir.glob("*.md")):
        frontmatter = extract_frontmatter(file_path)
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


def generate_rule_index() -> str:
    """Generate rule index."""
    rules_dir = Path(".windsurf/rules")
    rules_by_priority: dict[str, list[tuple[str, dict]]] = {}

    for file_path in sorted(rules_dir.glob("*.md")):
        frontmatter = extract_frontmatter(file_path)
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


def generate_dependency_graph() -> str:
    """Generate workflow dependency graph."""
    workflow_dir = Path(".windsurf/workflows")
    workflows: dict[str, dict] = {}

    for file_path in sorted(workflow_dir.glob("*.md")):
        frontmatter = extract_frontmatter(file_path)
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


def main() -> int:
    """Main generation function."""
    print("📝 Generating documentation indexes...")

    try:
        # Generate workflow index
        workflow_index = generate_workflow_index()
        workflow_index_path = Path(".windsurf/docs/workflow-index.md")
        workflow_index_path.write_text(workflow_index)
        print(f"  ✅ Generated {workflow_index_path}")

        # Generate rule index
        rule_index = generate_rule_index()
        rule_index_path = Path(".windsurf/docs/rules-index.md")
        rule_index_path.write_text(rule_index)
        print(f"  ✅ Generated {rule_index_path}")

        # Generate dependency graph
        dependency_graph = generate_dependency_graph()
        dependency_graph_path = Path(".windsurf/docs/workflow-dependencies.md")
        dependency_graph_path.write_text(dependency_graph)
        print(f"  ✅ Generated {dependency_graph_path}")

        print()
        print("✅ All indexes generated successfully")
        return 0

    except Exception as e:
        print(f"❌ Error generating indexes: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
