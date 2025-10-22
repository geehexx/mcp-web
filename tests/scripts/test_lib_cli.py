"""Tests for scripts.lib.cli module."""

from scripts.lib.cli import add_common_args, confirm_action, create_parser, handle_exit


class TestCreateParser:
    """Tests for create_parser()."""

    def test_basic_parser(self):
        """Test creating basic parser."""
        parser = create_parser("Test description")

        assert parser.description == "Test description"
        assert parser.epilog is None

    def test_parser_with_epilog(self):
        """Test parser with epilog."""
        parser = create_parser("Description", epilog="Epilog text")

        assert parser.description == "Description"
        assert parser.epilog == "Epilog text"


class TestAddCommonArgs:
    """Tests for add_common_args()."""

    def test_adds_verbose_arg(self):
        """Test that --verbose is added."""
        parser = create_parser("Test")
        add_common_args(parser)

        args = parser.parse_args(["--verbose"])
        assert args.verbose is True

        args = parser.parse_args([])
        assert args.verbose is False

    def test_adds_dry_run_arg(self):
        """Test that --dry-run is added."""
        parser = create_parser("Test")
        add_common_args(parser)

        args = parser.parse_args(["--dry-run"])
        assert args.dry_run is True

        args = parser.parse_args([])
        assert args.dry_run is False

    def test_both_args_work_together(self):
        """Test both arguments can be used together."""
        parser = create_parser("Test")
        add_common_args(parser)

        args = parser.parse_args(["--verbose", "--dry-run"])
        assert args.verbose is True
        assert args.dry_run is True


class TestHandleExit:
    """Tests for handle_exit()."""

    def test_success_no_errors(self, capsys):
        """Test successful exit with no errors."""
        exit_code = handle_exit([], success_msg="All good!")

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✅ All good!" in captured.out

    def test_success_no_message(self, capsys):
        """Test successful exit without success message."""
        exit_code = handle_exit([])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert captured.out == ""

    def test_failure_with_errors(self, capsys):
        """Test failure exit with errors."""
        errors = ["Error 1", "Error 2"]
        exit_code = handle_exit(errors)

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "❌ Validation failed" in captured.err
        assert "Error 1" in captured.err
        assert "Error 2" in captured.err


class TestConfirmAction:
    """Tests for confirm_action()."""

    def test_confirm_yes(self, monkeypatch):
        """Test confirmation with 'yes'."""
        monkeypatch.setattr("builtins.input", lambda _: "y")
        assert confirm_action("Proceed?") is True

        monkeypatch.setattr("builtins.input", lambda _: "yes")
        assert confirm_action("Proceed?") is True

        monkeypatch.setattr("builtins.input", lambda _: "Y")
        assert confirm_action("Proceed?") is True

    def test_confirm_no(self, monkeypatch):
        """Test confirmation with 'no'."""
        monkeypatch.setattr("builtins.input", lambda _: "n")
        assert confirm_action("Proceed?") is False

        monkeypatch.setattr("builtins.input", lambda _: "no")
        assert confirm_action("Proceed?") is False

    def test_confirm_default_true(self, monkeypatch):
        """Test confirmation with default True."""
        monkeypatch.setattr("builtins.input", lambda _: "")
        assert confirm_action("Proceed?", default=True) is True

    def test_confirm_default_false(self, monkeypatch):
        """Test confirmation with default False."""
        monkeypatch.setattr("builtins.input", lambda _: "")
        assert confirm_action("Proceed?", default=False) is False

    def test_confirm_invalid_input(self, monkeypatch):
        """Test confirmation with invalid input."""
        monkeypatch.setattr("builtins.input", lambda _: "maybe")
        assert confirm_action("Proceed?", default=False) is False
