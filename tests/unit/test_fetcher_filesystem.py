"""Unit tests for file system fetching."""

import tempfile
from pathlib import Path

import pytest

from mcp_web.config import FetcherSettings
from mcp_web.fetcher import URLFetcher, _parse_file_url, _validate_file_path


class TestFileURLParsing:
    """Test file:// URL parsing."""

    def test_parse_file_url_with_scheme(self):
        """Test parsing file:// URL."""
        result = _parse_file_url("file:///home/user/document.txt")
        assert result == Path("/home/user/document.txt")

    def test_parse_file_url_absolute_path(self):
        """Test parsing absolute path."""
        result = _parse_file_url("/home/user/document.txt")
        assert result == Path("/home/user/document.txt")

    def test_parse_file_url_with_url_encoding(self):
        """Test parsing URL-encoded file:// URL."""
        result = _parse_file_url("file:///home/user/my%20document.txt")
        assert result == Path("/home/user/my document.txt")

    def test_parse_file_url_windows_style(self):
        """Test parsing Windows-style file:// URL."""
        # Note: This may behave differently on Windows vs Unix
        result = _parse_file_url("file:///C:/Users/user/document.txt")
        assert isinstance(result, Path)


class TestPathValidation:
    """Test path validation against whitelist."""

    def test_validate_path_within_allowed_directory(self):
        """Test validation of path within allowed directory."""
        allowed_dirs = [Path("/home/user").resolve()]
        path = Path("/home/user/document.txt")

        is_valid, error = _validate_file_path(path, allowed_dirs)

        assert is_valid is True
        assert error == ""

    def test_validate_path_outside_allowed_directory(self):
        """Test validation of path outside allowed directory."""
        allowed_dirs = [Path("/home/user").resolve()]
        path = Path("/etc/passwd")

        is_valid, error = _validate_file_path(path, allowed_dirs)

        assert is_valid is False
        assert "outside allowed directories" in error.lower()

    def test_validate_path_traversal_attempt(self):
        """Test validation prevents path traversal."""
        allowed_dirs = [Path("/home/user/documents").resolve()]
        # Attempt to traverse up and access parent directory
        path = Path("/home/user/documents/../../.ssh/id_rsa")

        is_valid, error = _validate_file_path(path, allowed_dirs)

        # Path resolves to /home/.ssh/id_rsa which is outside allowed directory
        assert is_valid is False

    def test_validate_path_symlink_outside_allowed(self, tmp_path):
        """Test validation follows symlinks."""
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()

        forbidden_dir = tmp_path / "forbidden"
        forbidden_dir.mkdir()
        forbidden_file = forbidden_dir / "secret.txt"
        forbidden_file.write_text("secret")

        # Create symlink inside allowed dir pointing to forbidden file
        symlink = allowed_dir / "link.txt"
        symlink.symlink_to(forbidden_file)

        is_valid, error = _validate_file_path(symlink, [allowed_dir.resolve()])

        # Symlink resolves to forbidden directory
        assert is_valid is False

    def test_validate_multiple_allowed_directories(self):
        """Test validation with multiple allowed directories."""
        allowed_dirs = [
            Path("/home/user/documents").resolve(),
            Path("/home/user/downloads").resolve(),
        ]

        path1 = Path("/home/user/documents/file.txt")
        is_valid1, _ = _validate_file_path(path1, allowed_dirs)
        assert is_valid1 is True

        path2 = Path("/home/user/downloads/file.txt")
        is_valid2, _ = _validate_file_path(path2, allowed_dirs)
        assert is_valid2 is True

        path3 = Path("/home/user/music/song.mp3")
        is_valid3, _ = _validate_file_path(path3, allowed_dirs)
        assert is_valid3 is False


class TestFileSystemFetcher:
    """Test file system fetching functionality."""

    @pytest.fixture
    def temp_files(self, tmp_path):
        """Create temporary test files."""
        # Create test files
        text_file = tmp_path / "test.txt"
        text_file.write_text("Hello, world!")

        markdown_file = tmp_path / "test.md"
        markdown_file.write_text("# Heading\n\nSome content.")

        large_file = tmp_path / "large.txt"
        large_file.write_bytes(b"x" * (11 * 1024 * 1024))  # 11MB

        return {
            "dir": tmp_path,
            "text": text_file,
            "markdown": markdown_file,
            "large": large_file,
        }

    @pytest.fixture
    def fetcher(self, temp_files):
        """Create fetcher with temp directory allowed."""
        config = FetcherSettings(
            enable_file_system=True,
            allowed_directories=[str(temp_files["dir"])],
            max_file_size=10 * 1024 * 1024,  # 10MB
        )
        fetcher = URLFetcher(config)
        yield fetcher

    @pytest.mark.asyncio
    async def test_fetch_text_file_with_file_url(self, fetcher, temp_files):
        """Test fetching text file with file:// URL."""
        file_url = f"file://{temp_files['text']}"

        result = await fetcher.fetch(file_url)

        assert result.status_code == 200
        assert result.fetch_method == "filesystem"
        assert result.content == b"Hello, world!"
        assert result.content_type == "text/plain"

    @pytest.mark.asyncio
    async def test_fetch_text_file_with_absolute_path(self, fetcher, temp_files):
        """Test fetching text file with absolute path."""
        result = await fetcher.fetch(str(temp_files["text"]))

        assert result.status_code == 200
        assert result.fetch_method == "filesystem"
        assert result.content == b"Hello, world!"

    @pytest.mark.asyncio
    async def test_fetch_markdown_file(self, fetcher, temp_files):
        """Test fetching markdown file."""
        result = await fetcher.fetch(str(temp_files["markdown"]))

        assert result.status_code == 200
        assert result.content_type == "text/markdown"
        assert b"# Heading" in result.content

    @pytest.mark.asyncio
    async def test_fetch_file_not_found(self, fetcher, temp_files):
        """Test fetching non-existent file."""
        non_existent = temp_files["dir"] / "does-not-exist.txt"

        with pytest.raises(FileNotFoundError):
            await fetcher.fetch(str(non_existent))

    @pytest.mark.asyncio
    async def test_fetch_directory_fails(self, fetcher, temp_files):
        """Test fetching directory fails."""
        with pytest.raises(ValueError, match="Not a file"):
            await fetcher.fetch(str(temp_files["dir"]))

    @pytest.mark.asyncio
    async def test_fetch_file_too_large(self, fetcher, temp_files):
        """Test fetching file exceeding size limit."""
        with pytest.raises(ValueError, match="File too large"):
            await fetcher.fetch(str(temp_files["large"]))

    @pytest.mark.asyncio
    async def test_fetch_unauthorized_path(self, fetcher, temp_files):
        """Test fetching file outside allowed directories."""
        # Create file in system temp (not in allowed directories)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("unauthorized")
            unauthorized_file = f.name

        try:
            with pytest.raises(PermissionError, match="outside allowed directories"):
                await fetcher.fetch(unauthorized_file)
        finally:
            Path(unauthorized_file).unlink()

    @pytest.mark.asyncio
    async def test_fetch_with_file_system_disabled(self, temp_files):
        """Test fetching file when file system is disabled."""
        config = FetcherSettings(enable_file_system=False)
        fetcher = URLFetcher(config)

        try:
            with pytest.raises(ValueError, match="File system access is disabled"):
                await fetcher.fetch(str(temp_files["text"]))
        finally:
            await fetcher.close()

    @pytest.mark.asyncio
    async def test_fetch_multiple_includes_files(self, fetcher, temp_files):
        """Test fetching multiple URLs including file:// URLs."""
        urls = [
            str(temp_files["text"]),
            str(temp_files["markdown"]),
        ]

        results = await fetcher.fetch_multiple(urls)

        assert len(results) == 2
        assert all(r.fetch_method == "filesystem" for r in results.values())

    @pytest.mark.asyncio
    async def test_file_url_with_special_characters(self, fetcher, temp_files):
        """Test file URL with spaces and special characters."""
        special_file = temp_files["dir"] / "file with spaces & special.txt"
        special_file.write_text("content")

        # URL-encode the path
        file_url = f"file://{special_file}".replace(" ", "%20").replace("&", "%26")

        result = await fetcher.fetch(file_url)

        assert result.status_code == 200
        assert result.content == b"content"


class TestFileSystemSecurity:
    """Test security measures for file system access."""

    @pytest.mark.asyncio
    async def test_path_traversal_blocked(self, tmp_path):
        """Test path traversal attempts are blocked."""
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()

        config = FetcherSettings(
            enable_file_system=True,
            allowed_directories=[str(allowed_dir)],
        )
        fetcher = URLFetcher(config)

        try:
            # Attempt path traversal
            traversal_path = str(allowed_dir / ".." / ".." / "etc" / "passwd")

            with pytest.raises(PermissionError):
                await fetcher.fetch(traversal_path)
        finally:
            await fetcher.close()

    @pytest.mark.asyncio
    async def test_symlink_escape_blocked(self, tmp_path):
        """Test symlink escape attempts are blocked."""
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()

        forbidden_dir = tmp_path / "forbidden"
        forbidden_dir.mkdir()
        secret_file = forbidden_dir / "secret.txt"
        secret_file.write_text("secret data")

        # Create symlink in allowed dir pointing to forbidden file
        symlink = allowed_dir / "escape.txt"
        symlink.symlink_to(secret_file)

        config = FetcherSettings(
            enable_file_system=True,
            allowed_directories=[str(allowed_dir)],
        )
        fetcher = URLFetcher(config)

        try:
            # Symlink resolves outside allowed directory
            with pytest.raises(PermissionError):
                await fetcher.fetch(str(symlink))
        finally:
            await fetcher.close()

    @pytest.mark.asyncio
    async def test_relative_path_handling(self, tmp_path):
        """Test relative paths are properly resolved."""
        allowed_dir = tmp_path / "allowed"
        allowed_dir.mkdir()
        test_file = allowed_dir / "test.txt"
        test_file.write_text("content")

        config = FetcherSettings(
            enable_file_system=True,
            allowed_directories=[str(allowed_dir)],
        )
        fetcher = URLFetcher(config)

        try:
            # Even with relative path, should work if it resolves to allowed dir
            result = await fetcher.fetch(str(test_file))
            assert result.status_code == 200
        finally:
            await fetcher.close()
