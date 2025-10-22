"""Tests for documentation file automation helpers."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from scripts.automation.file_ops import (  # type: ignore  # pylint: disable=import-error
    ARCHIVE_MARKER,
    INDEX_END,
    INDEX_START,
    archive_initiative,
    move_file_with_refs,
    update_index,
)


@pytest.fixture()
def tmp_repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    (root / "docs" / "initiatives" / "active").mkdir(parents=True)
    (root / "docs" / "initiatives" / "completed").mkdir(parents=True)
    (root / "docs" / "initiatives" / "README.md").write_text(
        "\n".join(
            [
                "# Initiatives",
                f"{INDEX_START}",
                "Legacy block",
                f"{INDEX_END}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return root


@pytest.mark.unit
def test_archive_initiative_file_moves_and_updates(tmp_repo: Path) -> None:
    active_file = tmp_repo / "docs/initiatives/active/2025-10-18-sample.md"
    active_file.write_text("# Initiative\n", encoding="utf-8")

    other_doc = tmp_repo / "docs" / "notes.md"
    other_doc.write_text(
        "Reference: docs/initiatives/active/2025-10-18-sample.md\n",
        encoding="utf-8",
    )

    summary = archive_initiative(
        active_file,
        root=tmp_repo,
        completed_on="2025-10-19",
    )

    completed_file = tmp_repo / "docs/initiatives/completed/2025-10-18-sample.md"
    assert completed_file.exists()
    assert not active_file.exists()

    content = completed_file.read_text(encoding="utf-8")
    assert ARCHIVE_MARKER in content
    assert "2025-10-19" in content

    updated_ref = other_doc.read_text(encoding="utf-8")
    assert "docs/initiatives/completed/2025-10-18-sample.md" in updated_ref

    readme = (tmp_repo / "docs/initiatives/README.md").read_text(encoding="utf-8")
    assert "### Completed Initiatives" in readme
    assert "2025-10-18-sample.md" in readme
    assert summary["moved"] == [
        "docs/initiatives/active/2025-10-18-sample.md",
        "docs/initiatives/completed/2025-10-18-sample.md",
    ]


@pytest.mark.unit
def test_archive_initiative_directory_inserts_banner(tmp_repo: Path) -> None:
    directory = tmp_repo / "docs/initiatives/active/2025-10-18-folder"
    (directory / "initiative.md").parent.mkdir(parents=True)
    (directory / "initiative.md").write_text("# Folder initiative\n", encoding="utf-8")

    archive_initiative(
        directory,
        root=tmp_repo,
        completed_on="2025-10-19",
    )

    destination = tmp_repo / "docs/initiatives/completed/2025-10-18-folder"
    assert destination.is_dir()
    initiative_md = destination / "initiative.md"
    assert ARCHIVE_MARKER in initiative_md.read_text(encoding="utf-8")


@pytest.mark.unit
def test_move_file_with_refs_updates_links(tmp_repo: Path) -> None:
    src = tmp_repo / "docs/source.md"
    src.write_text("content", encoding="utf-8")
    dst = tmp_repo / "docs/subdir/destination.md"
    dst.parent.mkdir(parents=True)

    referencing = tmp_repo / "docs/ref.md"
    referencing.write_text("docs/source.md", encoding="utf-8")

    summary = move_file_with_refs(src, dst, root=tmp_repo)

    assert not src.exists()
    assert dst.exists()
    assert referencing.read_text(encoding="utf-8") == "docs/subdir/destination.md"
    assert summary["moved"] == ["docs/source.md", "docs/subdir/destination.md"]
    assert referencing.relative_to(tmp_repo).as_posix() in summary["references"]


@pytest.mark.unit
def test_update_index_rejects_unsupported_directory(tmp_repo: Path) -> None:
    with pytest.raises(ValueError):
        update_index(tmp_repo / "docs", root=tmp_repo)
