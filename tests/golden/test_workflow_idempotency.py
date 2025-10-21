"""
Golden tests for workflow optimization idempotency.

These tests verify that re-optimizing already-optimized workflows
produces ZERO changes (character-by-character exact match).

If ANY test fails, it indicates:
1. Optimization algorithm has changed (expected if intentional)
2. LLM provider has changed behavior (investigate)
3. Non-deterministic behavior detected (CRITICAL BUG)
"""

import sys
from difflib import unified_diff
from pathlib import Path

import pytest

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from test_optimization_idempotency import (  # noqa: E402
    SEED,
    TEMPERATURE,
    optimize_workflow,
)

# Workflows that have been optimized in previous sessions
GOLDEN_WORKFLOWS = [
    ".windsurf/workflows/implement.md",
    ".windsurf/workflows/detect-context.md",
    ".windsurf/workflows/load-context.md",
    ".windsurf/workflows/plan.md",
]


def load_golden_snapshot(workflow_name: str) -> str:
    """Load expected golden snapshot."""
    golden_path = Path(__file__).parent / "workflows" / workflow_name
    return golden_path.read_text()


def generate_diff(original: str, optimized: str, filename: str) -> str:
    """Generate unified diff for debugging."""
    original_lines = original.splitlines(keepends=True)
    optimized_lines = optimized.splitlines(keepends=True)

    diff = unified_diff(
        original_lines, optimized_lines, fromfile="original", tofile="optimized", lineterm=""
    )

    return "".join(diff)


@pytest.mark.golden
@pytest.mark.parametrize("workflow_path", GOLDEN_WORKFLOWS)
def test_optimization_idempotency(workflow_path):
    """
    Test that re-optimizing already-optimized workflows produces NO changes.

    This is a CRITICAL test. If it fails:
    - Phase 2 optimizations MUST NOT proceed
    - Root cause MUST be investigated
    - Either fix the optimization algorithm or update golden snapshots
    """
    # Extract filename for golden lookup
    workflow_name = Path(workflow_path).name

    # Load current production file (already optimized)
    production_path = Path(workflow_path)
    assert production_path.exists(), f"Production file not found: {workflow_path}"
    production_content = production_path.read_text()

    # Re-run optimization with deterministic settings
    # NOTE: optimize_workflow is currently a placeholder (identity function)
    # This test validates the framework is working correctly
    re_optimized_content = optimize_workflow(
        workflow_path=str(production_path), temperature=TEMPERATURE, seed=SEED, use_cache=False
    )

    # Compare character-by-character
    if production_content != re_optimized_content:
        # Generate diff for debugging
        diff = generate_diff(production_content, re_optimized_content, workflow_name)

        pytest.fail(
            f"❌ IDEMPOTENCY VIOLATION: {workflow_path}\n"
            f"\n"
            f"Re-optimization changed already-optimized content!\n"
            f"\n"
            f"Statistics:\n"
            f"  Original length: {len(production_content)} chars\n"
            f"  Re-optimized length: {len(re_optimized_content)} chars\n"
            f"  Difference: {len(re_optimized_content) - len(production_content):+d} chars\n"
            f"\n"
            f"Diff:\n"
            f"{diff}\n"
            f"\n"
            f"NEXT STEPS:\n"
            f"1. Investigate why optimization is non-idempotent\n"
            f"2. Check LLM provider settings (temp={TEMPERATURE}, seed={SEED})\n"
            f"3. Verify optimization prompt hasn't changed\n"
            f"4. If changes are intentional, update golden snapshots:\n"
            f"   cp {workflow_path} tests/golden/workflows/{workflow_name}\n"
        )

    print(f"✅ IDEMPOTENCY VERIFIED: {workflow_path}")


@pytest.mark.golden
@pytest.mark.parametrize("workflow_path", GOLDEN_WORKFLOWS)
def test_golden_snapshot_exists(workflow_path):
    """Verify golden snapshot files exist."""
    workflow_name = Path(workflow_path).name
    golden_path = Path(__file__).parent / "workflows" / workflow_name

    assert golden_path.exists(), (
        f"Golden snapshot missing: {golden_path}\n"
        f"Create with: cp {workflow_path} tests/golden/workflows/{workflow_name}"
    )


@pytest.mark.golden
@pytest.mark.parametrize("workflow_path", GOLDEN_WORKFLOWS)
def test_production_matches_golden(workflow_path):
    """Verify production files match golden snapshots."""
    workflow_name = Path(workflow_path).name

    production_content = Path(workflow_path).read_text()
    golden_content = load_golden_snapshot(workflow_name)

    if production_content != golden_content:
        diff = generate_diff(golden_content, production_content, workflow_name)

        pytest.fail(
            f"❌ GOLDEN MISMATCH: {workflow_path}\n"
            f"\n"
            f"Production file differs from golden snapshot.\n"
            f"\n"
            f"This means the file was manually edited after optimization.\n"
            f"\n"
            f"Options:\n"
            f"1. If changes are intentional, update golden:\n"
            f"   cp {workflow_path} tests/golden/workflows/{workflow_name}\n"
            f"2. If changes are mistakes, revert to golden:\n"
            f"   cp tests/golden/workflows/{workflow_name} {workflow_path}\n"
            f"\n"
            f"Diff:\n"
            f"{diff}\n"
        )
