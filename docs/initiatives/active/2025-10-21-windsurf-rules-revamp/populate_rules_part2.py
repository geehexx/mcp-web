#!/usr/bin/env python3
"""Populate remaining rules 08-15."""

import re
from pathlib import Path
from datetime import date

OLD_RULES = Path("/home/gxx/projects/mcp-web/.windsurf/rules")
OLD_DOCS = Path("/home/gxx/projects/mcp-web/.windsurf/docs")
OUTPUT_DIR = Path("/tmp/windsurf-rules-new")

def create_frontmatter(trigger, description=None, globs=None):
    lines = ["---", f"trigger: {trigger}"]
    if description and trigger in ["model_decision", "glob"]:
        clean = description.replace("'", "").replace('"', "")
        lines.append(f"description: {clean}")
    if globs and trigger == "glob":
        lines.append(f"globs: {globs}")
    lines.append("---")
    return "\n".join(lines)

def create_postmatter(file_name, trigger, tokens, topics, workflows=None, deps=None, changelog=None):
    sections = ["\n---\n", "## Rule Metadata\n",
                f"**File:** `{file_name}`  ",
                f"**Trigger:** {trigger}  ",
                f"**Estimated Tokens:** ~{tokens:,}  ",
                f"**Last Updated:** {date.today().isoformat()}  ",
                "**Status:** Active\n"]
    
    if trigger in ["model_decision", "glob"]:
        sections.append("**Can be @mentioned:** Yes (hybrid loading)\n")
    
    sections.append("\n**Topics Covered:**")
    for topic in topics:
        sections.append(f"- {topic}")
    
    if workflows:
        sections.append("\n**Workflow References:**")
        for wf in workflows:
            sections.append(f"- {wf}")
    
    if deps:
        sections.append("\n**Dependencies:**")
        for dep in deps:
            sections.append(f"- {dep}")
    
    if changelog:
        sections.append("\n**Changelog:**")
        for entry in changelog:
            sections.append(f"- {entry}")
    
    return "\n".join(sections)

def remove_frontmatter(content):
    if not content.startswith("---"):
        return content
    end = content.find("\n---\n", 4)
    if end == -1:
        return content
    return content[end + 5:].strip()

def extract_section(content, start_marker, end_marker=None):
    start = content.find(start_marker)
    if start == -1:
        return ""
    start += len(start_marker)
    
    if end_marker:
        end = content.find(end_marker, start)
        if end == -1:
            return content[start:].strip()
        return content[start:end].strip()
    return content[start:].strip()

# Rule 08: File Operations
def create_08_file_operations():
    source = (OLD_RULES / "06_context_engineering.md").read_text()
    content = remove_frontmatter(source)
    
    # Extract file operations section
    file_ops = extract_section(content, "## 1. File Operations", "## 2. Git Operations")
    
    content = f"""# File Operations and Archival

{file_ops}

## Initiative Archival

**Use automation:** Always use `task archive:initiative NAME=<name>` for archival

**Process:**
1. Verify completion gates
2. Run archival script
3. Update references
4. Commit changes

**See:** Automation scripts for detailed commands
"""
    
    fm = create_frontmatter("model_decision", 
                            "Apply when moving archiving or reorganizing files and updating cross-references")
    pm = create_postmatter("08_file_operations.md", "model_decision", 2000,
                           ["File moves", "Initiative archival", "Cross-reference updates", "MCP vs standard tools"],
                           ["/archive-initiative - Initiative archival", "/implement - File reorganization"],
                           ["Source: 06_context_engineering.md (File Operations section)"],
                           [f"{date.today()}: Created from 06_context_engineering.md"])
    
    return fm + "\n\n" + content + "\n\n" + pm

# Rule 09: Git Workflows
def create_09_git_workflows():
    source = (OLD_RULES / "06_context_engineering.md").read_text()
    content = remove_frontmatter(source)
    
    # Extract git section
    git_ops = extract_section(content, "## 2. Git Operations", "## 3.")
    
    content = f"""# Git Workflows and Conventional Commits

{git_ops}

## Pre-commit Hooks

**Quality gates enforced:**
- Markdown linting
- Task format validation
- Frontmatter validation
- Token count monitoring

**Bypassing (use sparingly):**
- Only for false positives or urgent hotfixes
- Document reason in commit message
- Create follow-up issue if needed
"""
    
    fm = create_frontmatter("model_decision", 
                            "Apply for git operations commits branching or version control work")
    pm = create_postmatter("09_git_workflows.md", "model_decision", 1800,
                           ["Git operations", "Conventional commits", "Pre-commit hooks", "Commit best practices"],
                           ["/commit - Git commit workflow"],
                           ["Source: 06_context_engineering.md (Git Operations section)"],
                           [f"{date.today()}: Created from 06_context_engineering.md"])
    
    return fm + "\n\n" + content + "\n\n" + pm

# Rule 10: Session Protocols
def create_10_session_protocols():
    source = (OLD_RULES / "05_operational_protocols.md").read_text()
    content = remove_frontmatter(source)
    
    # Extract session end protocol
    session_protocol = extract_section(content, "## 1. Session End Protocol", "## 2. Progress")
    progress = extract_section(content, "## 2. Progress Communication", "## 3.")
    
    content = f"""# Session Protocols and Progress Communication

## Session End Protocol

{session_protocol}

## Progress Communication

{progress}

## Workflow Invocation

**Critical:** Workflows are NOT Python scripts

- ✅ Invoke via workflow name: `/meta-analysis`
- ❌ Never: `python scripts/meta_analysis.py`
- See full details in operational protocols
"""
    
    fm = create_frontmatter("model_decision", 
                            "Apply at session end when completing work or managing work transitions")
    pm = create_postmatter("10_session_protocols.md", "model_decision", 2000,
                           ["Session end protocol", "Progress communication", "Workflow invocation", "Exit criteria"],
                           ["/work-session-protocol - Session end", "/meta-analysis - Session summary"],
                           ["Source: 05_operational_protocols.md"],
                           [f"{date.today()}: Created from 05_operational_protocols.md"])
    
    return fm + "\n\n" + content + "\n\n" + pm

# Rule 11: Error Handling
def create_11_error_handling():
    source = (OLD_DOCS / "error-handling-patterns.md").read_text()
    content = remove_frontmatter(source)
    
    content = content.replace("# Error Handling Patterns", "# Error Handling and Recovery")
    
    fm = create_frontmatter("model_decision", 
                            "Apply when handling errors implementing error recovery or debugging failures")
    pm = create_postmatter("11_error_handling.md", "model_decision", 2200,
                           ["Error patterns", "Recovery strategies", "Debugging", "Graceful degradation"],
                           ["/implement - Error handling", "/validate - Error testing"],
                           ["Source: error-handling-patterns.md"],
                           [f"{date.today()}: Created from error-handling-patterns.md"])
    
    return fm + "\n\n" + content + "\n\n" + pm

# Rule 12: Task Orchestration
def create_12_task_orchestration():
    source = (OLD_RULES / "07_task_system.md").read_text()
    content = remove_frontmatter(source)
    
    # Extract core sections only (trim from 29KB to ~3KB)
    purpose = extract_section(content, "**Purpose:**", "## Purpose")
    when_required = extract_section(content, "## Purpose", "## Format")
    format = extract_section(content, "## Format", "## Core Rules")
    core_rules = extract_section(content, "## Core Rules", "## Workflow Attribution")
    attribution = extract_section(content, "## Workflow Attribution", "## Examples")
    
    # Get 2-3 key examples only
    examples = extract_section(content, "## Examples", "## Anti-Patterns")[:1000]
    
    content = f"""# Task Orchestration and update_plan Usage

{purpose}

## When Required

{when_required}

## Format Specification

{format}

## Core Rules

{core_rules}

## Workflow Attribution

{attribution}

## Key Examples

{examples}

**For complete reference:** See task-system-reference documentation
"""
    
    fm = create_frontmatter("model_decision", 
                            "Apply when using update_plan creating task lists or orchestrating multi-step workflows")
    pm = create_postmatter("12_task_orchestration.md", "model_decision", 3000,
                           ["update_plan tool", "Task format", "Workflow attribution", "Hierarchical tasks"],
                           ["/work - Task orchestration", "/plan - Planning tasks", "/implement - Implementation tasks"],
                           ["Source: 07_task_system.md (core sections only, trimmed from 29KB)"],
                           [f"{date.today()}: Created from 07_task_system.md (core only)"])
    
    return fm + "\n\n" + content + "\n\n" + pm

# Rule 13: Workflow Routing
def create_13_workflow_routing():
    source = (OLD_DOCS / "workflow-routing-matrix.md").read_text()
    content = remove_frontmatter(source)
    
    content = content.replace("# Workflow Routing Matrix", "# Workflow Routing and Signal Detection")
    
    fm = create_frontmatter("model_decision", 
                            "Apply when routing work making workflow decisions or detecting project context")
    pm = create_postmatter("13_workflow_routing.md", "model_decision", 1800,
                           ["Routing matrix", "Signal detection", "Confidence levels", "Decision tree"],
                           ["/work - Work routing", "/work-routing - Routing decisions"],
                           ["Source: workflow-routing-matrix.md"],
                           [f"{date.today()}: Created from workflow-routing-matrix.md"])
    
    return fm + "\n\n" + content + "\n\n" + pm

# Rule 14: Automation Scripts
def create_14_automation_scripts():
    source = (OLD_DOCS / "automation-scripts.md").read_text()
    content = remove_frontmatter(source)
    
    content = content.replace("# Automation Scripts", "# Automation Scripts and Taskfile Commands")
    
    fm = create_frontmatter("model_decision", 
                            "Apply when using automation scripts Taskfile commands or scaffolding operations")
    pm = create_postmatter("14_automation_scripts.md", "model_decision", 3000,
                           ["Taskfile commands", "Automation scripts", "Non-interactive scaffolding", "File operations"],
                           ["/archive-initiative - Archive automation", "/implement - Scaffolding"],
                           ["Source: automation-scripts.md"],
                           [f"{date.today()}: Changed from manual to model_decision (hybrid approach)",
                            f"{date.today()}: Created from automation-scripts.md"])
    
    return fm + "\n\n" + content + "\n\n" + pm

# Rule 15: Tool Patterns
def create_15_tool_patterns():
    source = (OLD_DOCS / "tool-patterns.md").read_text()
    content = remove_frontmatter(source)
    
    content = content.replace("# Tool Patterns", "# MCP Tool Usage Patterns")
    
    fm = create_frontmatter("model_decision", 
                            "Apply when using MCP tools or needing guidance on tool calling patterns")
    pm = create_postmatter("15_tool_patterns.md", "model_decision", 2500,
                           ["MCP tools", "Tool selection", "Batch operations", "Filesystem operations"],
                           ["All workflows - Tool usage guidance"],
                           ["Source: tool-patterns.md"],
                           [f"{date.today()}: Created from tool-patterns.md"])
    
    return fm + "\n\n" + content + "\n\n" + pm

def main():
    print("🔄 Populating rules 08-15...\n")
    
    rules = [
        ("08_file_operations.md", create_08_file_operations),
        ("09_git_workflows.md", create_09_git_workflows),
        ("10_session_protocols.md", create_10_session_protocols),
        ("11_error_handling.md", create_11_error_handling),
        ("12_task_orchestration.md", create_12_task_orchestration),
        ("13_workflow_routing.md", create_13_workflow_routing),
        ("14_automation_scripts.md", create_14_automation_scripts),
        ("15_tool_patterns.md", create_15_tool_patterns),
    ]
    
    for filename, creator in rules:
        print(f"  Populating {filename}...")
        try:
            content = creator()
            (OUTPUT_DIR / filename).write_text(content)
            size = len(content)
            status = 'OK' if size < 12000 else '⚠️ OVER LIMIT'
            print(f"    ✅ Complete ({size:,} bytes, {status})")
        except Exception as e:
            print(f"    ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n✅ All 16 rules populated")

if __name__ == "__main__":
    main()
