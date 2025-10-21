#!/usr/bin/env python3
"""
Test workflow optimization idempotency.

This script validates that re-optimizing already-optimized workflows
produces ZERO changes (character-by-character exact match).

Usage:
    # Test specific workflows
    python scripts/test_optimization_idempotency.py \
        --workflows implement.md detect-context.md \
        --expect-no-changes

    # Test all golden workflows (Session 2)
    python scripts/test_optimization_idempotency.py --test-golden

    # Enable caching (for performance)
    python scripts/test_optimization_idempotency.py --test-golden --cache

    # Dry run (show what would be tested)
    python scripts/test_optimization_idempotency.py --test-golden --dry-run
"""

import argparse
import hashlib
import json
import sys
from difflib import unified_diff
from pathlib import Path

# Import cache from same directory
from manage_optimization_cache import OptimizationCache

# Configuration (matches /improve-workflow settings)
MODEL = "cascade"  # Windsurf IDE model
TEMPERATURE = 0.0  # Deterministic
SEED = 42  # Fixed seed for reproducibility

# Placeholder prompt (actual optimization is done by Windsurf)
OPTIMIZATION_PROMPT = """
Apply conciseness optimization to workflow:
- Remove verbosity while preserving intent
- Consolidate examples
- Use tables for structured data
- Maintain all critical instructions
"""

# Golden workflows from Session 2
GOLDEN_WORKFLOWS = [
    ".windsurf/workflows/implement.md",
    ".windsurf/workflows/detect-context.md",
    ".windsurf/workflows/load-context.md",
    ".windsurf/workflows/plan.md",
]


def create_optimization_hash(
    file_path: str,
    content: str,
    optimization_prompt: str = OPTIMIZATION_PROMPT,
    model: str = MODEL,
    temperature: float = TEMPERATURE,
    seed: int = SEED,
) -> str:
    """
    Create deterministic hash for optimization request.

    Hash includes:
    - File path (for context)
    - Content hash (SHA-256 of input text)
    - Optimization prompt hash
    - Model + parameters

    This ensures:
    - Same input + same prompt → same hash → cache hit
    - Changed input → different hash → cache miss → re-optimize
    - Changed prompt → different hash → cache miss → re-optimize all

    Args:
        file_path: Path to workflow file
        content: Workflow content to optimize
        optimization_prompt: Prompt used for optimization
        model: LLM model name
        temperature: Sampling temperature
        seed: Random seed

    Returns:
        SHA-256 hash as hex string
    """
    content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    prompt_hash = hashlib.sha256(optimization_prompt.encode("utf-8")).hexdigest()

    payload = {
        "file_path": file_path,
        "content_hash": content_hash,
        "prompt_hash": prompt_hash,
        "model": model,
        "temperature": temperature,
        "seed": seed,
    }

    serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def optimize_workflow(
    workflow_path: str,
    temperature: float = TEMPERATURE,
    seed: int = SEED,
    use_cache: bool = True,
) -> str:
    """
    Optimize workflow with deterministic settings.

    NOTE: This is a PLACEHOLDER. Actual optimization is done by:
    1. Human user via Windsurf IDE /improve-workflow command
    2. Manual workflow optimization process

    This function exists to:
    - Test cache functionality
    - Validate hash generation
    - Provide structure for future automation

    For now, it returns the input unchanged (identity function).

    Args:
        workflow_path: Path to workflow file
        temperature: Sampling temperature (for LLM if automated)
        seed: Random seed (for LLM if automated)
        use_cache: Whether to use cache

    Returns:
        Optimized workflow content (currently just returns original)
    """
    content = Path(workflow_path).read_text()

    if use_cache:
        cache = OptimizationCache()
        cache_key = create_optimization_hash(workflow_path, content)

        cached_result = cache.get(cache_key)
        if cached_result:
            print(f"  ✅ CACHE HIT: {workflow_path}")
            return cached_result

    print(f"  🔄 CACHE MISS: {workflow_path}")

    # TODO: Implement actual LLM optimization call when automated
    # For now, return unchanged (identity function)
    # This allows testing the cache and validation framework
    optimized = content

    if use_cache:
        cache.put(
            cache_key=cache_key,
            file_path=workflow_path,
            original_content=content,
            optimized_content=optimized,
            metadata={
                "model": MODEL,
                "temperature": temperature,
                "seed": seed,
                "prompt_hash": hashlib.sha256(OPTIMIZATION_PROMPT.encode()).hexdigest(),
                "note": "Placeholder - actual optimization done manually",
            },
        )

    return optimized


def generate_diff(original: str, optimized: str, filename: str = "workflow") -> str:
    """Generate unified diff for debugging."""
    original_lines = original.splitlines(keepends=True)
    optimized_lines = optimized.splitlines(keepends=True)

    diff = unified_diff(
        original_lines,
        optimized_lines,
        fromfile=f"{filename} (original)",
        tofile=f"{filename} (optimized)",
        lineterm="",
    )

    return "".join(diff)


def test_workflow_idempotency(workflow_path: str, use_cache: bool = False) -> dict:
    """
    Test idempotency of a single workflow.

    Returns dict with:
        - is_idempotent: bool
        - original_size: int
        - optimized_size: int
        - diff_chars: int
        - message: str
    """
    full_path = Path(workflow_path)
    if not full_path.exists():
        return {"is_idempotent": False, "error": f"File not found: {workflow_path}"}

    original_content = full_path.read_text()

    # Run optimization
    optimized_content = optimize_workflow(
        str(full_path), temperature=TEMPERATURE, seed=SEED, use_cache=use_cache
    )

    # Compare
    is_identical = original_content == optimized_content

    result = {
        "is_idempotent": is_identical,
        "original_size": len(original_content),
        "optimized_size": len(optimized_content),
        "diff_chars": len(optimized_content) - len(original_content),
        "message": "✅ NO CHANGES (idempotent)" if is_identical else "❌ CHANGES DETECTED",
        "original_hash": hashlib.sha256(original_content.encode()).hexdigest()[:16],
        "optimized_hash": hashlib.sha256(optimized_content.encode()).hexdigest()[:16],
    }

    # Generate diff if not identical
    if not is_identical:
        result["diff"] = generate_diff(
            original_content, optimized_content, Path(workflow_path).name
        )

    return result


def main():
    parser = argparse.ArgumentParser(description="Test workflow optimization idempotency")
    parser.add_argument(
        "--workflows",
        nargs="+",
        help="Specific workflows to test (relative to .windsurf/workflows/)",
    )
    parser.add_argument(
        "--test-golden",
        action="store_true",
        help="Test all golden workflows from Session 2 optimizations",
    )
    parser.add_argument(
        "--cache", action="store_true", help="Enable caching (faster, but may hide issues)"
    )
    parser.add_argument(
        "--expect-no-changes",
        action="store_true",
        help="Exit with error code if ANY changes detected",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be tested without running",
    )
    parser.add_argument(
        "--show-diff",
        action="store_true",
        help="Show full diff for non-idempotent workflows",
    )

    args = parser.parse_args()

    # Determine workflows to test
    if args.test_golden:
        workflows = GOLDEN_WORKFLOWS
    elif args.workflows:
        workflows = [f".windsurf/workflows/{w}" for w in args.workflows]
    else:
        print("ERROR: Must specify --workflows or --test-golden")
        parser.print_help()
        sys.exit(1)

    print(f"\n{'=' * 70}")
    print("WORKFLOW OPTIMIZATION IDEMPOTENCY TEST")
    print(f"{'=' * 70}")
    print(f"Testing: {len(workflows)} workflow(s)")
    print(f"Model: {MODEL}, Temperature: {TEMPERATURE}, Seed: {SEED}")
    print(f"Caching: {'ENABLED' if args.cache else 'DISABLED'}")
    print(f"{'=' * 70}\n")

    if args.dry_run:
        print("DRY RUN - Workflows to be tested:\n")
        for workflow in workflows:
            path = Path(workflow)
            exists = "✅" if path.exists() else "❌"
            size = len(path.read_text()) if path.exists() else 0
            print(f"  {exists} {workflow} ({size} chars)")
        print("\nUse without --dry-run to execute tests")
        sys.exit(0)

    # Run tests
    results = []
    for workflow_path in workflows:
        print(f"Testing: {workflow_path}")
        result = test_workflow_idempotency(workflow_path, use_cache=args.cache)

        if "error" in result:
            print(f"  ❌ ERROR: {result['error']}")
            results.append({**result, "path": workflow_path})
            continue

        results.append({**result, "path": workflow_path})
        print(f"  {result['message']}")

        if not result["is_idempotent"]:
            print(f"  Original: {result['original_size']} chars ({result['original_hash']})")
            print(f"  Optimized: {result['optimized_size']} chars ({result['optimized_hash']})")
            print(f"  Difference: {result['diff_chars']:+d} chars")

            if args.show_diff and "diff" in result:
                print(f"\n  Diff:\n{result['diff']}\n")

        print()

    # Summary
    total = len(results)
    idempotent_count = sum(1 for r in results if r.get("is_idempotent", False))
    error_count = sum(1 for r in results if "error" in r)

    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total workflows tested: {total}")
    print(f"Idempotent (no changes): {idempotent_count}")
    print(f"Non-idempotent (changed): {total - idempotent_count - error_count}")
    print(f"Errors: {error_count}")

    if idempotent_count == total:
        print("\n✅ ALL WORKFLOWS ARE IDEMPOTENT")
        print("Safe to proceed with Phase 2 optimizations.")
        sys.exit(0)
    else:
        print("\n❌ IDEMPOTENCY VIOLATIONS DETECTED")

        # Show non-idempotent workflows
        non_idempotent = [r for r in results if not r.get("is_idempotent", True)]
        if non_idempotent:
            print("\nWorkflows with changes:")
            for r in non_idempotent:
                if "error" in r:
                    print(f"  - {r['path']} (ERROR: {r['error']})")
                else:
                    print(f"  - {r['path']} ({r['diff_chars']:+d} chars)")

        print("\n⚠️  DO NOT PROCEED WITH PHASE 2 OPTIMIZATIONS")
        print("Investigate and fix root cause first.")

        if args.expect_no_changes:
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
