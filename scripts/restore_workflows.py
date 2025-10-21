#!/usr/bin/env python3
"""
Workflow Restoration Script

Systematically restores workflows from pre-optimization commits,
checks for post-optimization additions, and merges valid updates.

Usage:
    python scripts/restore_workflows.py --workflows research validate generate-plan
    python scripts/restore_workflows.py --all
    python scripts/restore_workflows.py --dry-run
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Optional


# Pre-optimization commit mapping
PRE_OPTIMIZATION_COMMITS = {
    # High-priority workflows (before 411a807)
    "research.md": "a0bb689",
    "validate.md": "a0bb689",
    "generate-plan.md": "a0bb689",
    
    # Medium-priority workflows (before d4d60af)
    "bump-version.md": "411a807",
    "extract-session.md": "411a807",
    "work-session-protocol.md": "411a807",
    "update-docs.md": "411a807",
    "archive-initiative.md": "411a807",
    "summarize-session.md": "411a807",
    
    # Tier 1-2 workflows (before 47cbdcc)
    "implement.md": "8cf2925",
    "detect-context.md": "8cf2925",
    "load-context.md": "8cf2925",
    "plan.md": "8cf2925",
    
    # Earlier optimized (need individual review)
    "consolidate-summaries.md": "95ed96e^",
    "meta-analysis.md": "29e3e28^",
    "improve-prompt.md": "35e08c1^",
    "improve-workflow.md": "5a8be3a^",
}

WORKFLOWS_DIR = Path(".windsurf/workflows")


def run_git_command(cmd: list[str], check: bool = True) -> tuple[int, str, str]:
    """Run git command and return exit code, stdout, stderr."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        print(f"❌ Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(f"Error: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.returncode, result.stdout, result.stderr


def get_original_content(workflow: str, commit: str) -> Optional[str]:
    """Extract original workflow content from git commit."""
    workflow_path = f"{WORKFLOWS_DIR}/{workflow}"
    _, content, stderr = run_git_command(
        ["git", "show", f"{commit}:{workflow_path}"],
        check=False,
    )
    if content:
        return content
    print(f"⚠️  Could not extract {workflow} from {commit}: {stderr}", file=sys.stderr)
    return None


def get_post_optimization_changes(workflow: str, from_commit: str) -> list[str]:
    """Get commits that modified workflow after optimization."""
    workflow_path = f"{WORKFLOWS_DIR}/{workflow}"
    _, commits, _ = run_git_command(
        ["git", "log", "--oneline", f"{from_commit}..HEAD", "--", workflow_path],
        check=False,
    )
    return [line for line in commits.strip().split("\n") if line]


def check_current_state(workflow: str) -> tuple[int, int]:
    """Get current line and token count for workflow."""
    workflow_path = WORKFLOWS_DIR / workflow
    if not workflow_path.exists():
        return 0, 0
    
    with open(workflow_path) as f:
        content = f.read()
        lines = len(content.splitlines())
        # Rough token estimate (4 chars per token)
        tokens = len(content) // 4
    
    return lines, tokens


def restore_workflow(workflow: str, commit: str, dry_run: bool = False) -> bool:
    """Restore workflow from pre-optimization commit."""
    print(f"\n📦 Restoring {workflow} from commit {commit}")
    
    # Get original content
    original = get_original_content(workflow, commit)
    if not original:
        print(f"  ❌ Could not extract original content")
        return False
    
    # Check current state
    current_lines, current_tokens = check_current_state(workflow)
    original_lines = len(original.splitlines())
    original_tokens = len(original) // 4  # Rough estimate
    
    print(f"  Current: {current_lines} lines (~{current_tokens} tokens)")
    print(f"  Original: {original_lines} lines (~{original_tokens} tokens)")
    print(f"  Change: {original_lines - current_lines:+d} lines ({original_tokens - current_tokens:+d} tokens)")
    
    # Check for post-optimization changes
    post_changes = get_post_optimization_changes(workflow, commit)
    if post_changes:
        print(f"  ⚠️  Found {len(post_changes)} post-optimization commits:")
        for change in post_changes[:3]:  # Show first 3
            print(f"    - {change}")
        if len(post_changes) > 3:
            print(f"    ... and {len(post_changes) - 3} more")
        print(f"  ⚠️  Manual review needed to merge valid additions")
    else:
        print(f"  ✅ No post-optimization changes detected")
    
    if dry_run:
        print(f"  🔍 DRY RUN: Would restore {workflow}")
        return True
    
    # Write restored content
    workflow_path = WORKFLOWS_DIR / workflow
    with open(workflow_path, "w") as f:
        f.write(original)
    
    print(f"  ✅ Restored {workflow}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Restore workflows from pre-optimization state")
    parser.add_argument(
        "--workflows",
        nargs="+",
        help="Specific workflows to restore (e.g., research validate)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Restore all workflows",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be restored without making changes",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all workflows with their restoration commits",
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("Available workflows for restoration:\n")
        for workflow, commit in sorted(PRE_OPTIMIZATION_COMMITS.items()):
            print(f"  {workflow:30s} ← {commit}")
        return
    
    # Determine which workflows to restore
    if args.all:
        workflows = list(PRE_OPTIMIZATION_COMMITS.keys())
    elif args.workflows:
        workflows = [w if w.endswith(".md") else f"{w}.md" for w in args.workflows]
        # Validate workflows
        invalid = [w for w in workflows if w not in PRE_OPTIMIZATION_COMMITS]
        if invalid:
            print(f"❌ Unknown workflows: {', '.join(invalid)}", file=sys.stderr)
            print(f"\nUse --list to see available workflows", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Check if in correct directory
    if not WORKFLOWS_DIR.exists():
        print(f"❌ Directory not found: {WORKFLOWS_DIR}", file=sys.stderr)
        print(f"   Run from repository root", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 70)
    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")
    print(f"Restoring {len(workflows)} workflow(s)")
    print("=" * 70)
    
    # Restore workflows
    success_count = 0
    for workflow in workflows:
        commit = PRE_OPTIMIZATION_COMMITS[workflow]
        if restore_workflow(workflow, commit, dry_run=args.dry_run):
            success_count += 1
    
    print("\n" + "=" * 70)
    print(f"✅ Successfully restored {success_count}/{len(workflows)} workflows")
    if args.dry_run:
        print("   (DRY RUN - no changes made)")
    print("=" * 70)
    
    if not args.dry_run and success_count > 0:
        print("\n📋 Next steps:")
        print("   1. Review restored workflows manually")
        print("   2. Check git diff for unexpected changes")
        print("   3. Apply intelligent re-optimization")
        print("   4. Validate quality (task docs:lint)")


if __name__ == "__main__":
    main()
