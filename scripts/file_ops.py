#!/usr/bin/env python3
"""Utilities for automating documentation file operations.

This module provides helpers used by automation workflows to archive initiatives,
move files while updating references, and regenerate initiative indexes.  The
functions are designed to be safe (guarding against path traversal), tested, and
accessible both programmatically and via a small Click-based CLI.
"""

from __future__ import annotations

import re
import shutil
from collections.abc import Iterable, Sequence
from datetime import date
from pathlib import Path

import click

REPO_ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_MARKER = "**⚠️ ARCHIVED:**"
INDEX_START = "<!-- AUTO:INITIATIVE-INDEX:START -->"
INDEX_END = "<!-- AUTO:INITIATIVE-INDEX:END -->"
TEXT_SUFFIXES = {
    ".md",
    ".markdown",
    ".mdx",
    ".yml",
    ".yaml",
    ".toml",
    ".json",
    ".py",
    ".txt",
    ".ini",
    ".cfg",
    ".rst",
}
TEXT_SUFFIX_ENDINGS = [".md.j2"]
EXCLUDED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "__pycache__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
}

__all__ = [
    "archive_initiative",
    "move_file_with_refs",
    "update_index",
]


def resolve_repo_path(
    path_like: Path | str,
    *,
    root: Path | None = None,
    must_exist: bool = True,
) -> Path:
    """Resolve *path_like* against repository root and ensure safety."""

    base = Path(root) if root else REPO_ROOT
    candidate = Path(path_like)
    candidate = (base / candidate).resolve() if not candidate.is_absolute() else candidate.resolve()

    if not str(candidate).startswith(str(base.resolve())):
        raise ValueError(f"Path {candidate} escapes repository root")

    if must_exist and not candidate.exists():
        raise FileNotFoundError(candidate)

    return candidate


def iter_text_files(root: Path) -> Iterable[Path]:
    """Yield text-like files under *root*, skipping known exclusions."""

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        suffix = path.suffix
        if suffix in TEXT_SUFFIXES or any(path.name.endswith(end) for end in TEXT_SUFFIX_ENDINGS):
            yield path


def replace_in_files(
    root: Path,
    *,
    old: str,
    new: str,
    dry_run: bool = False,
) -> list[str]:
    """Replace occurrences of *old* with *new* in repository text files."""

    updated: list[str] = []
    for path in iter_text_files(root):
        content = path.read_text(encoding="utf-8")
        if old not in content:
            continue
        updated.append(str(path.relative_to(root)))
        if not dry_run:
            path.write_text(content.replace(old, new), encoding="utf-8")
    return updated


def insert_archive_banner(path: Path, completed_on: str, *, dry_run: bool) -> bool:
    """Insert archive banner into markdown file if not already present."""

    content = path.read_text(encoding="utf-8")
    if ARCHIVE_MARKER in content:
        return False

    banner = f"> {ARCHIVE_MARKER} This initiative was completed on {completed_on}.\n\n"

    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) == 3:
            new_content = f"---{parts[1]}---\n\n{banner}{parts[2].lstrip()}"
        else:
            new_content = banner + content
    else:
        new_content = banner + content

    if not dry_run:
        path.write_text(new_content, encoding="utf-8")
    return True


def add_archive_notice_to_directory(directory: Path, completed_on: str, *, dry_run: bool) -> bool:
    """Insert archive banner into the main initiative file within a directory."""

    primary = directory / "initiative.md"
    if primary.exists():
        return insert_archive_banner(primary, completed_on, dry_run=dry_run)
    return False


def move_path(src: Path, dst: Path, *, dry_run: bool) -> None:
    """Move *src* to *dst* handling directories."""

    if dst.exists() and not dry_run:
        raise FileExistsError(dst)

    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))


def update_initiatives_readme(*, root: Path, dry_run: bool) -> bool:
    """Update auto-generated initiatives index block in README."""

    readme_path = root / "docs/initiatives/README.md"
    if not readme_path.exists():
        return False

    active_dir = root / "docs/initiatives/active"
    completed_dir = root / "docs/initiatives/completed"

    def list_entries(directory: Path) -> list[str]:
        if not directory.exists():
            return []
        entries: list[str] = []
        for child in sorted(directory.iterdir(), key=lambda p: p.name.lower()):
            if child.name.startswith("."):
                continue
            rel = child.relative_to(root).as_posix()
            display = f"{child.name}{'/' if child.is_dir() else ''}"
            entries.append(f"- [`{display}`]({rel})")
        return entries

    active_entries = list_entries(active_dir)
    completed_entries = list_entries(completed_dir)

    body_lines = [
        "",
        "### Active Initiatives",
        "",
    ]
    body_lines.extend(active_entries if active_entries else ["_None_"])
    body_lines.extend(
        [
            "",
            "### Completed Initiatives",
            "",
        ]
    )
    body_lines.extend(completed_entries if completed_entries else ["_None_"])
    body_lines.append("")

    body = "\n".join(body_lines)
    content = readme_path.read_text(encoding="utf-8")

    if INDEX_START in content and INDEX_END in content:
        replacement = f"{INDEX_START}{body}{INDEX_END}"
        updated_content = re.sub(
            rf"{re.escape(INDEX_START)}.*?{re.escape(INDEX_END)}",
            replacement,
            content,
            flags=re.DOTALL,
        )
    else:
        block_lines = [
            "## Initiative Directory Index",
            f"{INDEX_START}{body}{INDEX_END}",
            "",
        ]
        block = "\n".join(block_lines)
        updated_content = content
        if not updated_content.endswith("\n"):
            updated_content += "\n"
        updated_content += block

    if not dry_run:
        readme_path.write_text(updated_content, encoding="utf-8")
    return content != updated_content


def archive_initiative(
    initiative_path: Path | str,
    *,
    root: Path | None = None,
    completed_on: str | None = None,
    dry_run: bool = False,
) -> dict[str, Sequence[str]]:
    """Archive an initiative (file or folder) into completed/ and update references."""

    base = Path(root) if root else REPO_ROOT
    completed_on = completed_on or date.today().isoformat()

    src = resolve_repo_path(initiative_path, root=base)
    try:
        relative = src.relative_to(base)
    except ValueError as exc:  # pragma: no cover - safety guard
        raise ValueError("Initiative path must reside within repository") from exc

    active_dir = base / "docs/initiatives/active"
    completed_dir = base / "docs/initiatives/completed"
    if active_dir not in src.parents and src != active_dir:
        raise ValueError("Initiative must be under docs/initiatives/active")

    destination = completed_dir / relative.relative_to(active_dir)

    changed_files: list[str] = []

    # Insert archive banner
    banner_added = False
    if src.is_file():
        banner_added = insert_archive_banner(src, completed_on, dry_run=dry_run)
        if banner_added:
            changed_files.append(str(src.relative_to(base)))
    else:
        banner_added = add_archive_notice_to_directory(src, completed_on, dry_run=dry_run)
        if banner_added:
            changed_files.append(str((src / "initiative.md").relative_to(base)))

    # Move to completed/
    move_path(src, destination, dry_run=dry_run)

    summary = {
        "moved": [str(relative), str(destination.relative_to(base))],
        "references": [],
        "changed": changed_files,
    }

    old_rel = relative.as_posix()
    new_rel = destination.relative_to(base).as_posix()
    summary["references"] = replace_in_files(base, old=old_rel, new=new_rel, dry_run=dry_run)

    if update_initiatives_readme(root=base, dry_run=dry_run):
        summary["changed"].append("docs/initiatives/README.md")

    return summary


def move_file_with_refs(
    src_path: Path | str,
    dst_path: Path | str,
    *,
    root: Path | None = None,
    dry_run: bool = False,
    update_refs: bool = True,
    completed_on: str | None = None,  # noqa: ARG001
) -> dict[str, Sequence[str]]:
    """Move a file or directory and optionally update repository references."""

    base = Path(root) if root else REPO_ROOT
    src = resolve_repo_path(src_path, root=base)
    dst = resolve_repo_path(dst_path, root=base, must_exist=False)

    move_path(src, dst, dry_run=dry_run)

    summary = {
        "moved": [str(src.relative_to(base)), str(dst.relative_to(base))],
        "references": [],
    }

    if update_refs:
        summary["references"] = replace_in_files(
            base,
            old=src.relative_to(base).as_posix(),
            new=dst.relative_to(base).as_posix(),
            dry_run=dry_run,
        )

    return summary


def update_index(
    directory: Path | str,
    *,
    root: Path | None = None,
    dry_run: bool = False,
) -> bool:
    """Update known indexes for *directory* (currently initiatives)."""

    base = Path(root) if root else REPO_ROOT
    target = resolve_repo_path(directory, root=base)

    initiatives_root = base / "docs/initiatives"
    if target == initiatives_root:
        return update_initiatives_readme(root=base, dry_run=dry_run)

    raise ValueError("update_index currently supports only docs/initiatives")


@click.group()
def cli() -> None:
    """File operation helpers."""


@cli.command("archive-initiative")
@click.argument("initiative")
@click.option("--completed-on", help="Completion date (YYYY-MM-DD)")
@click.option("--dry-run", is_flag=True, help="Preview actions without writing")
def archive_command(initiative: str, completed_on: str | None, dry_run: bool) -> None:
    """Archive INITIATIVE from active/ to completed/."""

    summary = archive_initiative(initiative, completed_on=completed_on, dry_run=dry_run)
    click.echo("Moved: " + " → ".join(summary["moved"]))
    if summary["references"]:
        click.echo(f"Updated references in {len(summary['references'])} files")
    if summary["changed"]:
        click.echo("Changed files: ")
        for item in summary["changed"]:
            click.echo(f"  - {item}")
    if dry_run:
        click.echo("Dry-run mode: no files were modified.")


@cli.command("move-file")
@click.argument("src")
@click.argument("dst")
@click.option("--no-update-refs", is_flag=True, help="Skip reference updates")
@click.option("--dry-run", is_flag=True, help="Preview actions without writing")
def move_file_command(src: str, dst: str, no_update_refs: bool, dry_run: bool) -> None:
    """Move SRC to DST and update references."""

    summary = move_file_with_refs(
        src,
        dst,
        dry_run=dry_run,
        update_refs=not no_update_refs,
    )
    click.echo("Moved: " + " → ".join(summary["moved"]))
    if summary["references"]:
        click.echo(f"Updated references in {len(summary['references'])} files")
    if dry_run:
        click.echo("Dry-run mode: no files were modified.")


@cli.command("update-index")
@click.argument("directory")
@click.option("--dry-run", is_flag=True, help="Preview actions without writing")
def update_index_command(directory: str, dry_run: bool) -> None:
    """Update index data for DIRECTORY (e.g. docs/initiatives)."""

    changed = update_index(directory, dry_run=dry_run)
    if changed:
        click.echo("Index updated")
    else:
        click.echo("No changes required")
    if dry_run:
        click.echo("Dry-run mode: no files were modified.")


if __name__ == "__main__":
    cli()
