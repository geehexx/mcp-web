#!/usr/bin/env python3
"""Regenerate Cursor and Windsurf golden files from unified sources."""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPTS_DIR = ROOT / "scripts"
GOLDEN_ROOT = ROOT / "tests" / "golden" / "ide"

OUTPUT_MAP: list[tuple[str, str, Path]] = [
    ("cursor", "commands", ROOT / ".cursor" / "commands"),
    ("cursor", "rules", ROOT / ".cursor" / "rules"),
    ("windsurf", "workflows", ROOT / ".windsurf" / "workflows"),
    ("windsurf", "rules", ROOT / ".windsurf" / "rules"),
]


def build_configs() -> None:
    """Invoke the unified build pipeline in-process."""
    import sys

    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))

    from build_ide_configs import build_configs as _build_configs  # type: ignore import

    success = _build_configs()
    if not success:
        msg = "Failed to rebuild IDE configurations before updating goldens"
        raise SystemExit(msg)


def sync_directory(src: Path, dest: Path) -> None:
    """Sync files from src directory into destination golden directory."""
    if not src.exists():
        raise SystemExit(f"Source directory missing: {src}")

    dest.mkdir(parents=True, exist_ok=True)

    # Remove stale files in destination
    for stale in dest.rglob("*"):
        if stale.is_file():
            relative = stale.relative_to(dest)
            if not (src / relative).exists():
                stale.unlink()

    # Copy current files
    for file_path in src.rglob("*"):
        if not file_path.is_file():
            continue

        relative = file_path.relative_to(src)
        target = dest / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target)


def main() -> int:
    build_configs()

    for ide, category, src in OUTPUT_MAP:
        dest = GOLDEN_ROOT / ide / category
        sync_directory(src, dest)

    print("✅ Updated IDE golden files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
