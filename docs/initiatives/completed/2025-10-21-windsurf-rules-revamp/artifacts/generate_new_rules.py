#!/usr/bin/env python3
"""Generate new Windsurf-compatible rule files from existing rules and docs.

Implements the v2 hybrid approach design:
- 16 rules total (1 always_on, 5 glob, 10 model_decision, 0 manual)
- Minimal Windsurf-compliant frontmatter
- Post-matter metadata preservation
- Content consolidation from multiple sources
"""

import re
from datetime import date
from pathlib import Path

# Paths
OLD_RULES = Path("/home/gxx/projects/mcp-web/.windsurf/rules")
OLD_DOCS = Path("/home/gxx/projects/mcp-web/.windsurf/docs")
OUTPUT_DIR = Path("/tmp/windsurf-rules-new")


def extract_content_between(text: str, start_marker: str, end_marker: str = None) -> str:
    """Extract content between markers."""
    start_idx = text.find(start_marker)
    if start_idx == -1:
        return ""

    start_idx += len(start_marker)

    if end_marker:
        end_idx = text.find(end_marker, start_idx)
        if end_idx == -1:
            return text[start_idx:].strip()
        return text[start_idx:end_idx].strip()

    return text[start_idx:].strip()


def remove_frontmatter(content: str) -> str:
    """Remove YAML frontmatter from content."""
    if not content.startswith("---"):
        return content

    # Find second ---
    end_idx = content.find("\n---\n", 4)
    if end_idx == -1:
        return content

    return content[end_idx + 5 :].strip()


def create_frontmatter(trigger: str, description: str = None, globs: str = None) -> str:
    """Create minimal Windsurf-compliant frontmatter."""
    lines = ["---"]
    lines.append(f"trigger: {trigger}")

    if description and trigger in ["model_decision", "glob"]:
        # Remove apostrophes and quotes
        clean_desc = description.replace("'", "").replace('"', "")
        lines.append(f"description: {clean_desc}")

    if globs and trigger == "glob":
        # Unquoted, comma-separated
        lines.append(f"globs: {globs}")

    lines.append("---")
    return "\n".join(lines)


def create_postmatter(
    file_name: str,
    trigger: str,
    tokens: int,
    topics: list,
    workflows: list = None,
    dependencies: list = None,
    changelog: list = None,
) -> str:
    """Create post-matter metadata section."""
    sections = [
        "\n---\n",
        "## Rule Metadata\n",
        f"**File:** `{file_name}`  ",
        f"**Trigger:** {trigger}  ",
        f"**Estimated Tokens:** ~{tokens:,}  ",
        f"**Last Updated:** {date.today().isoformat()}  ",
        "**Status:** Active\n",
    ]

    if trigger in ["model_decision", "glob"]:
        sections.append("**Can be @mentioned:** Yes (hybrid loading)\n")

    sections.append("\n**Topics Covered:**")
    for topic in topics:
        sections.append(f"- {topic}")

    if workflows:
        sections.append("\n**Workflow References:**")
        for wf in workflows:
            sections.append(f"- {wf}")

    if dependencies:
        sections.append("\n**Dependencies:**")
        for dep in dependencies:
            sections.append(f"- {dep}")

    if changelog:
        sections.append("\n**Changelog:**")
        for entry in changelog:
            sections.append(f"- {entry}")

    return "\n".join(sections)


# Rule 00: Core Directives (always_on)
def create_00_core_directives():
    """Trim from 00_agent_directives.md - keep only sections 1-4."""
    source = (OLD_RULES / "00_agent_directives.md").read_text()
    content_no_fm = remove_frontmatter(source)

    # Extract sections 1-4
    sections_to_keep = []

    # Title and navigation
    title_match = re.search(r"# Rule: Agent Persona.*?(?=\n## )", content_no_fm, re.DOTALL)
    if title_match:
        sections_to_keep.append(title_match.group(0))

    # Section 1: Persona
    persona = extract_content_between(content_no_fm, "## 1. Persona", "## 2.")
    if persona:
        sections_to_keep.append(f"## 1. Persona\n\n{persona}")

    # Section 2: Guiding Principles
    principles = extract_content_between(content_no_fm, "## 2. Guiding Principles", "## 3.")
    if principles:
        sections_to_keep.append(f"## 2. Guiding Principles (North Stars)\n\n{principles}")

    # Section 2.1: Parallel Tool Calls
    parallel = extract_content_between(content_no_fm, "## 2.1. Parallel Tool Call", "## 3.")
    if parallel:
        sections_to_keep.append(f"## 2.1. Parallel Tool Call Efficiency (CRITICAL)\n\n{parallel}")

    # Section 3: Operational Mandate
    mandate = extract_content_between(content_no_fm, "## 3. Operational Mandate", "## 4.")
    if mandate:
        sections_to_keep.append(f"## 3. Operational Mandate\n\n{mandate}")

    # Section 4: Tool Selection
    tools = extract_content_between(content_no_fm, "## 4. Tool Selection", "## 5.")
    if tools:
        sections_to_keep.append(f"## 4. Tool Selection (October 2025)\n\n{tools}")

    frontmatter = create_frontmatter("always_on")
    content = "\n\n---\n\n".join(sections_to_keep)
    postmatter = create_postmatter(
        "00_core_directives.md",
        "always_on",
        3000,
        [
            "Agent persona and role",
            "Guiding principles (security, robustness, performance)",
            "Operational mandate",
            "Tool selection (uv, pytest, ruff)",
            "Parallel tool call efficiency",
        ],
        ["All workflows (always loaded)"],
        ["Related rules: All specialized rules reference back to core directives"],
        [
            f"{date.today().isoformat()}: Created from 00_agent_directives.md (sections 1-4 only)",
            "2025-10-20: Trimmed from 12.9KB to ~3KB for always_on compliance",
        ],
    )

    return frontmatter + "\n\n" + content + "\n\n" + postmatter


# Quick stub generator for remaining rules (to be implemented)
def create_stub(
    file_name: str,
    trigger: str,
    description: str = None,
    globs: str = None,
    tokens: int = 2000,
    topics: list = None,
):
    """Create a stub rule file."""
    frontmatter = create_frontmatter(trigger, description, globs)

    content = f"# {file_name.replace('.md', '').replace('_', ' ').title()}\n\n"
    content += "**Purpose:** [TO BE IMPLEMENTED]\n\n"
    content += "**Content:** [Source content to be extracted and consolidated]\n"

    postmatter = create_postmatter(
        file_name,
        trigger,
        tokens,
        topics or ["[To be documented]"],
        changelog=[f"{date.today().isoformat()}: Stub created (implementation pending)"],
    )

    return frontmatter + "\n\n" + content + "\n\n" + postmatter


def main():
    """Generate all 16 new rule files."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("🔄 Generating new Windsurf-compatible rule files...\n")

    # Rule 00: Core Directives (always_on)
    print("  Creating 00_core_directives.md (always_on)...")
    content_00 = create_00_core_directives()
    (OUTPUT_DIR / "00_core_directives.md").write_text(content_00)
    print(f"    ✅ Created ({len(content_00)} bytes)")

    # Rules 01-05: Glob triggers (stubs for now - full implementation needed)
    glob_rules = [
        (
            "01_python_code.md",
            "*.py, **/*.py",
            "Python code style type hints async patterns",
            ["Python style", "Type hints", "Async/await"],
        ),
        (
            "02_testing.md",
            "tests/**/*.py, test_*.py, *_test.py, conftest.py",
            "Testing standards pytest fixtures TDD practices",
            ["pytest", "Test fixtures", "TDD"],
        ),
        (
            "03_documentation.md",
            "docs/**/*.md, *.md, README.md",
            "Documentation standards markdown ADRs initiatives",
            ["Markdown", "ADRs", "Initiatives"],
        ),
        (
            "04_config_files.md",
            "pyproject.toml, *.ini, Taskfile.yml, .pre-commit-config.yaml",
            "Configuration file best practices TOML YAML Taskfile",
            ["TOML/pyproject.toml", "Taskfile", "Pre-commit"],
        ),
        (
            "05_windsurf_structure.md",
            ".windsurf/**/*.md, .windsurf/**/*.json",
            "Windsurf directory structure enforcement frontmatter format",
            ["Windsurf directory", "Frontmatter format"],
        ),
    ]

    for file_name, globs, desc, topics in glob_rules:
        print(f"  Creating {file_name} (glob)...")
        content = create_stub(file_name, "glob", desc, globs, 2000, topics)
        (OUTPUT_DIR / file_name).write_text(content)
        print(f"    ✅ Stub created ({len(content)} bytes)")

    # Rules 06-15: Model decision triggers (stubs for now)
    model_rules = [
        (
            "06_security_practices.md",
            "Apply when dealing with security-sensitive code including API calls user input LLM interactions and authentication",
            ["OWASP LLM Top 10", "Input validation", "Authentication"],
        ),
        (
            "07_context_optimization.md",
            "Apply for context loading batch operations or performance optimization work",
            ["Batch operations", "Parallel loading", "Performance"],
        ),
        (
            "08_file_operations.md",
            "Apply when moving archiving or reorganizing files and updating cross-references",
            ["File moves", "Initiative archival", "Reference updates"],
        ),
        (
            "09_git_workflows.md",
            "Apply for git operations commits branching or version control work",
            ["Git operations", "Conventional commits", "Branching"],
        ),
        (
            "10_session_protocols.md",
            "Apply at session end when completing work or managing work transitions",
            ["Session end protocol", "Progress communication"],
        ),
        (
            "11_error_handling.md",
            "Apply when handling errors implementing error recovery or debugging failures",
            ["Error patterns", "Recovery strategies", "Debugging"],
        ),
        (
            "12_task_orchestration.md",
            "Apply when using update_plan creating task lists or orchestrating multi-step workflows",
            ["update_plan usage", "Task attribution", "Hierarchical tasks"],
        ),
        (
            "13_workflow_routing.md",
            "Apply when routing work making workflow decisions or detecting project context",
            ["Routing matrix", "Signal detection", "Confidence levels"],
        ),
        (
            "14_automation_scripts.md",
            "Apply when using automation scripts Taskfile commands or scaffolding operations",
            ["Automation scripts", "Taskfile", "Scaffolding"],
        ),
        (
            "15_tool_patterns.md",
            "Apply when using MCP tools or needing guidance on tool calling patterns",
            ["MCP tools", "Tool usage", "grep/read/edit patterns"],
        ),
    ]

    for file_name, description, topics in model_rules:
        print(f"  Creating {file_name} (model_decision)...")
        content = create_stub(file_name, "model_decision", description, None, 2500, topics)
        (OUTPUT_DIR / file_name).write_text(content)
        print(f"    ✅ Stub created ({len(content)} bytes)")

    print(f"\n✅ Generated 16 rule files in {OUTPUT_DIR}")
    print("\n📝 Next steps:")
    print("  1. Review and expand stub content")
    print("  2. Extract content from source rules/docs")
    print("  3. Verify all files <12KB")
    print("  4. Test frontmatter format")


if __name__ == "__main__":
    main()
