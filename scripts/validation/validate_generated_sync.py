#!/usr/bin/env python3
"""Ensure generated IDE artefacts are in sync with unified sources."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = ROOT / "scripts"
CURSOR_DIR = ROOT / ".cursor"
WINDSURF_DIR = ROOT / ".windsurf"


def run(cmd: list[str], *, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    """Run command and return completed process."""
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        text=True,
        capture_output=True,
    )


def build_configs() -> bool:
    """Invoke the unified build pipeline in-process."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        from build_ide_configs import build_configs as _build_configs
    except ImportError as exc:  # pragma: no cover - defensive
        print(f"❌ Unable to import build_ide_configs: {exc}")
        return False

    success = _build_configs()
    if not success:
        print("❌ Building IDE configs failed.")
    return success


def ensure_dirs_exist() -> bool:
    """Validate that generated directories exist after build."""
    missing = [str(path) for path in (CURSOR_DIR, WINDSURF_DIR) if not path.exists()]
    if missing:
        print("❌ Missing generated directories after build:")
        for path in missing:
            print(f"   - {path}")
        return False
    return True


def check_git_clean() -> bool:
    """Verify generated artefacts match committed state."""
    diff_cmd = ["git", "diff", "--quiet", "--", str(CURSOR_DIR), str(WINDSURF_DIR)]
    result = run(diff_cmd, cwd=ROOT)
    if result.returncode == 0:
        print("✅ Generated artefacts are in sync with committed state.")
        return True

    # Provide helpful diff output limited to names for pre-commit readability
    name_only = run(
        ["git", "diff", "--name-only", "--", str(CURSOR_DIR), str(WINDSURF_DIR)],
        cwd=ROOT,
    )
    print("❌ Generated artefacts are out of sync with unified sources.")
    if name_only.stdout.strip():
        print("   Files with differences:")
        for line in name_only.stdout.strip().splitlines():
            print(f"     - {line}")
    else:
        print("   (Diff detected but no filenames captured.)")
    print("\nRun: python scripts/build_ide_configs.py && git add .cursor .windsurf")
    return False


def main() -> int:
    if not build_configs():
        return 1

    if not ensure_dirs_exist():
        return 1

    return 0 if check_git_clean() else 1


if __name__ == "__main__":
    sys.exit(main())
