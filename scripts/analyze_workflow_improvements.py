#!/usr/bin/env python3
"""
Analyze workflow files and generate improvement recommendations.

This script simulates what the /improve-workflow would do by analyzing
Windsurf workflows and providing concrete improvement recommendations with
metrics.

Usage:
    python scripts/analyze_workflow_improvements.py
    python scripts/analyze_workflow_improvements.py --workflow <name>
    python scripts/analyze_workflow_improvements.py --apply --dry-run
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class WorkflowMetrics:
    """Metrics for a workflow."""

    name: str
    token_count: int
    word_count: int
    char_count: int
    complexity: int
    stage_count: int
    update_plan_count: int
    example_count: int
    has_frontmatter: bool
    conciseness_weight: float
    priority: str
    recommended_action: str


@dataclass
class ImprovementRecommendation:
    """Improvement recommendation for a workflow."""

    workflow: str
    current_tokens: int
    estimated_tokens_after: int
    reduction_percent: float
    conciseness_weight: float
    techniques: list[str]
    decomposition_needed: bool
    rationale: str


def parse_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown."""
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    return None


def count_tokens(text: str) -> int:
    """Estimate token count (rough approximation: ~0.75 tokens per word)."""
    word_count = len(text.split())
    return int(word_count * 0.75)


def count_stages(content: str) -> int:
    """Count stages in workflow."""
    return len(re.findall(r"^##\s+Stage\s+\d+", content, re.MULTILINE))


def count_update_plans(content: str) -> int:
    """Count update_plan calls."""
    return len(re.findall(r"update_plan\s*\(", content))


def count_examples(content: str) -> int:
    """Count examples in workflow."""
    example_patterns = [
        r"^Example\s+\d+:",
        r"^\*\*Example:\*\*",
        r"```.*?Example",
    ]
    count = 0
    for pattern in example_patterns:
        count += len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
    return count


def calculate_conciseness_weight(token_count: int) -> tuple[float, str]:
    """Calculate conciseness weight based on token count."""
    if token_count < 2000:
        return 1.0, "low"
    elif token_count < 4000:
        return 1.5, "moderate"
    elif token_count < 6000:
        return 2.0, "high"
    else:
        return 2.5, "critical"


def analyze_workflow(file_path: Path) -> WorkflowMetrics:
    """Analyze a single workflow file."""
    content = file_path.read_text()

    frontmatter = parse_frontmatter(content)
    has_frontmatter = frontmatter is not None

    # Get complexity from frontmatter or estimate
    complexity = frontmatter.get("complexity", 50) if frontmatter else 50

    # Calculate metrics
    token_count = count_tokens(content)
    word_count = len(content.split())
    char_count = len(content)
    stage_count = count_stages(content)
    update_plan_count = count_update_plans(content)
    example_count = count_examples(content)

    conciseness_weight, priority = calculate_conciseness_weight(token_count)

    # Determine recommended action
    if token_count > 6000 or complexity > 75:
        recommended_action = "decomposition"
    elif token_count > 4000 or complexity > 65:
        recommended_action = "aggressive_conciseness"
    elif token_count > 2000:
        recommended_action = "moderate_conciseness"
    else:
        recommended_action = "standard_optimization"

    return WorkflowMetrics(
        name=file_path.stem,
        token_count=token_count,
        word_count=word_count,
        char_count=char_count,
        complexity=complexity,
        stage_count=stage_count,
        update_plan_count=update_plan_count,
        example_count=example_count,
        has_frontmatter=has_frontmatter,
        conciseness_weight=conciseness_weight,
        priority=priority,
        recommended_action=recommended_action,
    )


def generate_improvement_recommendation(metrics: WorkflowMetrics) -> ImprovementRecommendation:
    """Generate improvement recommendation based on metrics."""
    techniques = []

    # Base techniques
    if metrics.recommended_action in [
        "moderate_conciseness",
        "aggressive_conciseness",
        "decomposition",
    ]:
        techniques.extend(["information_distillation", "structured_bullets", "keyword_extraction"])

    # Additional for high priority
    if metrics.recommended_action in ["aggressive_conciseness", "decomposition"]:
        techniques.extend(["example_consolidation", "reference_externalization"])

    # Estimate reduction
    if metrics.recommended_action == "decomposition":
        # Aim for 40-50% reduction + decomposition
        reduction_percent = 45.0
    elif metrics.recommended_action == "aggressive_conciseness":
        # Aim for 30-40% reduction
        reduction_percent = 35.0
    elif metrics.recommended_action == "moderate_conciseness":
        # Aim for 20-30% reduction
        reduction_percent = 25.0
    else:
        # Aim for 10-15% reduction
        reduction_percent = 12.5

    estimated_tokens_after = int(metrics.token_count * (1 - reduction_percent / 100))

    # Generate rationale
    rationale_parts = []

    if metrics.token_count > 6000:
        rationale_parts.append(
            f"Very large workflow ({metrics.token_count} tokens > 6000 threshold)"
        )
    elif metrics.token_count > 4000:
        rationale_parts.append(f"Large workflow ({metrics.token_count} tokens)")
    elif metrics.token_count > 2000:
        rationale_parts.append(f"Moderate workflow ({metrics.token_count} tokens)")

    if metrics.complexity > 75:
        rationale_parts.append(f"high complexity ({metrics.complexity}/100)")

    if metrics.example_count > 5:
        rationale_parts.append(f"many examples ({metrics.example_count})")

    if metrics.stage_count > 8:
        rationale_parts.append(f"many stages ({metrics.stage_count})")

    rationale = "; ".join(rationale_parts) if rationale_parts else "standard optimization"

    decomposition_needed = metrics.recommended_action == "decomposition"

    return ImprovementRecommendation(
        workflow=metrics.name,
        current_tokens=metrics.token_count,
        estimated_tokens_after=estimated_tokens_after,
        reduction_percent=reduction_percent,
        conciseness_weight=metrics.conciseness_weight,
        techniques=techniques,
        decomposition_needed=decomposition_needed,
        rationale=rationale,
    )


def main():
    parser = argparse.ArgumentParser(description="Analyze workflows for improvement opportunities")
    parser.add_argument("--workflow", help="Analyze specific workflow (name without .md)", type=str)
    parser.add_argument(
        "--output",
        help="Output JSON file for results",
        type=Path,
        default=Path(".windsurf/workflow-improvement-analysis.json"),
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    # Find workflow directory
    workflows_dir = Path(".windsurf/workflows")
    if not workflows_dir.exists():
        print(f"❌ Workflows directory not found: {workflows_dir}")
        return 1

    # Get workflow files
    if args.workflow:
        workflow_files = [workflows_dir / f"{args.workflow}.md"]
        if not workflow_files[0].exists():
            print(f"❌ Workflow not found: {args.workflow}")
            return 1
    else:
        workflow_files = sorted(workflows_dir.glob("*.md"))

    print(f"\n📊 Analyzing {len(workflow_files)} workflows...\n")

    # Analyze all workflows
    all_metrics = []
    all_recommendations = []

    for workflow_file in workflow_files:
        metrics = analyze_workflow(workflow_file)
        recommendation = generate_improvement_recommendation(metrics)

        all_metrics.append(metrics)
        all_recommendations.append(recommendation)

        if args.verbose:
            print(
                f"  {metrics.name:30s} | {metrics.token_count:5d} tokens | "
                f"{metrics.priority:8s} priority | {metrics.recommended_action}"
            )

    # Sort by token count (descending)
    all_recommendations.sort(key=lambda x: x.current_tokens, reverse=True)

    # Generate summary
    print("\n" + "=" * 80)
    print("📈 IMPROVEMENT ANALYSIS SUMMARY")
    print("=" * 80 + "\n")

    # Group by priority
    by_priority = {"critical": [], "high": [], "moderate": [], "low": []}
    for rec in all_recommendations:
        metrics = next(m for m in all_metrics if m.name == rec.workflow)
        by_priority[metrics.priority].append((metrics, rec))

    total_current = sum(m.token_count for m in all_metrics)
    total_estimated = sum(r.estimated_tokens_after for r in all_recommendations)
    total_reduction = total_current - total_estimated
    total_reduction_percent = (total_reduction / total_current) * 100

    print(f"**Current Total:** {total_current:,} tokens")
    print(f"**Estimated After:** {total_estimated:,} tokens")
    print(f"**Potential Reduction:** {total_reduction:,} tokens ({total_reduction_percent:.1f}%)\n")

    for priority in ["critical", "high", "moderate", "low"]:
        items = by_priority[priority]
        if not items:
            continue

        print(f"\n### {priority.upper()} PRIORITY ({len(items)} workflows)")
        print("-" * 80)

        for metrics, rec in items:
            print(f"\n**{metrics.name}**")
            print(
                f"  Current: {rec.current_tokens:,} tokens → Estimated: {rec.estimated_tokens_after:,} tokens "
                f"(-{rec.reduction_percent:.0f}%)"
            )
            print(f"  Techniques: {', '.join(rec.techniques)}")
            if rec.decomposition_needed:
                print("  ⚠️  DECOMPOSITION RECOMMENDED")
            print(f"  Rationale: {rec.rationale}")

    # Save detailed results
    results = {
        "analysis_date": "2025-10-21",
        "total_workflows": len(all_metrics),
        "summary": {
            "current_total_tokens": total_current,
            "estimated_total_tokens": total_estimated,
            "total_reduction_tokens": total_reduction,
            "total_reduction_percent": total_reduction_percent,
        },
        "workflows": [
            {
                "name": rec.workflow,
                "current_tokens": rec.current_tokens,
                "estimated_tokens": rec.estimated_tokens_after,
                "reduction_percent": rec.reduction_percent,
                "priority": next(m for m in all_metrics if m.name == rec.workflow).priority,
                "techniques": rec.techniques,
                "decomposition_needed": rec.decomposition_needed,
                "rationale": rec.rationale,
            }
            for rec in all_recommendations
        ],
    }

    args.output.write_text(json.dumps(results, indent=2))
    print(f"\n\n💾 Detailed results saved to: {args.output}")

    # Recommendations
    print("\n" + "=" * 80)
    print("🎯 RECOMMENDED ACTIONS")
    print("=" * 80 + "\n")

    decomposition_candidates = [r for r in all_recommendations if r.decomposition_needed]
    if decomposition_candidates:
        print(f"1. **DECOMPOSITION REQUIRED** ({len(decomposition_candidates)} workflows):")
        for rec in decomposition_candidates:
            print(f"   - {rec.workflow} ({rec.current_tokens:,} tokens)")
        print()

    aggressive_candidates = [
        r for r in all_recommendations if not r.decomposition_needed and r.reduction_percent >= 30
    ]
    if aggressive_candidates:
        print(f"2. **AGGRESSIVE CONCISENESS** ({len(aggressive_candidates)} workflows):")
        for rec in aggressive_candidates[:5]:  # Top 5
            print(
                f"   - {rec.workflow} ({rec.current_tokens:,} → {rec.estimated_tokens_after:,} tokens)"
            )
        if len(aggressive_candidates) > 5:
            print(f"   ... and {len(aggressive_candidates) - 5} more")
        print()

    print("3. **Next Steps:**")
    print("   - Review decomposition candidates manually")
    print("   - Run /improve-prompt on high-priority workflows")
    print("   - Validate improvements before applying")
    print("   - Commit improvements in batches")

    return 0


if __name__ == "__main__":
    sys.exit(main())
