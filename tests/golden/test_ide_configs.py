"""Regression tests ensuring IDE artefacts match golden snapshots."""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = PROJECT_ROOT / "scripts"


def _load_build_configs() -> Callable[[], bool]:
    """Dynamically import build_configs after adjusting sys.path."""

    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))

    from build_ide_configs import build_configs as builder  # type: ignore import

    return builder


GOLDEN_ROOT = PROJECT_ROOT / "tests" / "golden" / "ide"
CURSOR_ROOT = PROJECT_ROOT / ".cursor"
WINDSURF_ROOT = PROJECT_ROOT / ".windsurf"


@pytest.fixture(scope="module", autouse=True)
def rebuild_ide_configs() -> None:
    """Rebuild IDE configurations before running comparisons."""

    success = _load_build_configs()()
    assert success, "Failed to rebuild IDE configurations before golden comparisons"


def _assert_directory_matches(actual_dir: Path, golden_dir: Path) -> None:
    """Assert that all files in actual_dir match golden_dir contents."""

    assert golden_dir.exists(), f"Golden directory missing: {golden_dir}"
    assert actual_dir.exists(), f"Actual directory missing: {actual_dir}"

    actual_files = {
        path.relative_to(actual_dir): path for path in actual_dir.rglob("*") if path.is_file()
    }
    golden_files = {
        path.relative_to(golden_dir): path for path in golden_dir.rglob("*") if path.is_file()
    }

    assert actual_files.keys() == golden_files.keys(), (
        "Mismatch between generated artefacts and golden snapshots."
        f"\nMissing in actual: {sorted(golden_files.keys() - actual_files.keys())}"
        f"\nMissing in golden: {sorted(actual_files.keys() - golden_files.keys())}"
    )

    for relative_path, actual_path in actual_files.items():
        golden_path = golden_files[relative_path]
        actual_content = actual_path.read_text(encoding="utf-8")
        golden_content = golden_path.read_text(encoding="utf-8")

        assert actual_content == golden_content, (
            f"Content mismatch for {relative_path} between generated and golden files"
        )


@pytest.mark.golden
def test_cursor_rules_match_golden() -> None:
    """Verify Cursor rule outputs match golden snapshots."""

    actual_dir = CURSOR_ROOT / "rules"
    golden_dir = GOLDEN_ROOT / "cursor" / "rules"
    _assert_directory_matches(actual_dir, golden_dir)


@pytest.mark.golden
def test_cursor_commands_match_golden() -> None:
    """Verify Cursor command outputs match golden snapshots."""

    actual_dir = CURSOR_ROOT / "commands"
    golden_dir = GOLDEN_ROOT / "cursor" / "commands"
    _assert_directory_matches(actual_dir, golden_dir)


@pytest.mark.golden
def test_windsurf_rules_match_golden() -> None:
    """Verify Windsurf rule outputs match golden snapshots."""

    actual_dir = WINDSURF_ROOT / "rules"
    golden_dir = GOLDEN_ROOT / "windsurf" / "rules"
    _assert_directory_matches(actual_dir, golden_dir)


@pytest.mark.golden
def test_windsurf_workflows_match_golden() -> None:
    """Verify Windsurf workflow outputs match golden snapshots."""

    actual_dir = WINDSURF_ROOT / "workflows"
    golden_dir = GOLDEN_ROOT / "windsurf" / "workflows"
    _assert_directory_matches(actual_dir, golden_dir)
