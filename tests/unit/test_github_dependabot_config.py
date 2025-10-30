"""Unit tests for GitHub Dependabot configuration.

Tests validate the .github/dependabot.yml file for:
- YAML syntax and structure
- Required fields (version, updates)
- Valid package-ecosystem values
- Valid schedule intervals
- Directory paths
- Schema compliance with GitHub Dependabot requirements
"""

from pathlib import Path

import pytest
import yaml


class TestDependabotConfigStructure:
    """Tests for Dependabot configuration file structure."""

    @pytest.fixture
    def dependabot_file(self):
        """Path to dependabot.yml file."""
        return Path(".github/dependabot.yml")

    @pytest.fixture
    def dependabot_config(self, dependabot_file):
        """Load and parse dependabot.yml configuration."""
        with open(dependabot_file) as f:
            return yaml.safe_load(f)

    def test_dependabot_file_exists(self, dependabot_file):
        """Test that dependabot.yml file exists."""
        assert dependabot_file.exists(), "dependabot.yml file should exist"
        assert dependabot_file.is_file(), "dependabot.yml should be a file"

    def test_valid_yaml_syntax(self, dependabot_file):
        """Test that dependabot.yml has valid YAML syntax."""
        with open(dependabot_file) as f:
            try:
                config = yaml.safe_load(f)
                assert config is not None, "YAML should parse to a non-None value"
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML syntax: {e}")

    def test_yaml_is_dictionary(self, dependabot_config):
        """Test that parsed YAML is a dictionary."""
        assert isinstance(dependabot_config, dict), "Root YAML structure must be a dictionary"

    def test_has_version_field(self, dependabot_config):
        """Test that configuration has version field."""
        assert "version" in dependabot_config, "Configuration must have 'version' field"

    def test_version_is_correct(self, dependabot_config):
        """Test that version is set to 2 (required by GitHub)."""
        assert dependabot_config["version"] == 2, "Version must be 2"

    def test_has_updates_field(self, dependabot_config):
        """Test that configuration has updates field."""
        assert "updates" in dependabot_config, "Configuration must have 'updates' field"

    def test_updates_is_list(self, dependabot_config):
        """Test that updates field is a list."""
        assert isinstance(
            dependabot_config["updates"], list
        ), "Updates field must be a list"

    def test_updates_not_empty(self, dependabot_config):
        """Test that updates list is not empty."""
        assert len(dependabot_config["updates"]) > 0, "Updates list must not be empty"


class TestDependabotUpdatesConfiguration:
    """Tests for individual update configurations."""

    @pytest.fixture
    def dependabot_config(self):
        """Load dependabot configuration."""
        with open(".github/dependabot.yml") as f:
            return yaml.safe_load(f)

    @pytest.fixture
    def update_configs(self, dependabot_config):
        """Get all update configurations."""
        return dependabot_config["updates"]

    def test_all_updates_have_required_fields(self, update_configs):
        """Test that each update has required fields."""
        required_fields = ["package-ecosystem", "directory", "schedule"]
        for i, update in enumerate(update_configs):
            for field in required_fields:
                assert (
                    field in update
                ), f"Update {i} missing required field: {field}"

    def test_package_ecosystem_is_string(self, update_configs):
        """Test that package-ecosystem is a string."""
        for i, update in enumerate(update_configs):
            assert isinstance(
                update["package-ecosystem"], str
            ), f"Update {i}: package-ecosystem must be a string"

    def test_package_ecosystem_is_valid(self, update_configs):
        """Test that package-ecosystem uses valid values."""
        valid_ecosystems = {
            "bundler",
            "cargo",
            "composer",
            "docker",
            "elm",
            "gitsubmodule",
            "github-actions",
            "gomod",
            "gradle",
            "maven",
            "mix",
            "npm",
            "nuget",
            "pip",
            "pipenv",
            "poetry",
            "pub",
            "terraform",
        }
        for i, update in enumerate(update_configs):
            ecosystem = update["package-ecosystem"]
            assert (
                ecosystem in valid_ecosystems
            ), f"Update {i}: '{ecosystem}' is not a valid package-ecosystem"

    def test_directory_is_string(self, update_configs):
        """Test that directory is a string."""
        for i, update in enumerate(update_configs):
            assert isinstance(
                update["directory"], str
            ), f"Update {i}: directory must be a string"

    def test_directory_is_valid_path(self, update_configs):
        """Test that directory is a valid path format."""
        for i, update in enumerate(update_configs):
            directory = update["directory"]
            assert directory.startswith(
                "/"
            ), f"Update {i}: directory must start with '/'"
            assert (
                "\\" not in directory
            ), f"Update {i}: directory should use forward slashes"

    def test_schedule_is_dictionary(self, update_configs):
        """Test that schedule is a dictionary."""
        for i, update in enumerate(update_configs):
            assert isinstance(
                update["schedule"], dict
            ), f"Update {i}: schedule must be a dictionary"

    def test_schedule_has_interval(self, update_configs):
        """Test that schedule has interval field."""
        for i, update in enumerate(update_configs):
            schedule = update["schedule"]
            assert (
                "interval" in schedule
            ), f"Update {i}: schedule must have 'interval' field"

    def test_schedule_interval_is_valid(self, update_configs):
        """Test that schedule interval uses valid values."""
        valid_intervals = {"daily", "weekly", "monthly"}
        for i, update in enumerate(update_configs):
            interval = update["schedule"]["interval"]
            assert (
                interval in valid_intervals
            ), f"Update {i}: '{interval}' is not a valid schedule interval"


class TestDependabotPipEcosystem:
    """Tests specific to pip package ecosystem configuration."""

    @pytest.fixture
    def pip_updates(self):
        """Get all pip ecosystem updates."""
        with open(".github/dependabot.yml") as f:
            config = yaml.safe_load(f)
        return [u for u in config["updates"] if u["package-ecosystem"] == "pip"]

    def test_pip_ecosystem_present(self, pip_updates):
        """Test that pip ecosystem is configured."""
        assert len(pip_updates) > 0, "At least one pip ecosystem update should be configured"

    def test_pip_directory_exists(self, pip_updates):
        """Test that configured pip directories contain Python package files."""
        for update in pip_updates:
            directory = update["directory"].lstrip("/")
            if not directory:
                directory = "."
            
            dir_path = Path(directory)
            has_python_files = (
                (dir_path / "pyproject.toml").exists()
                or (dir_path / "requirements.txt").exists()
                or (dir_path / "setup.py").exists()
                or (dir_path / "Pipfile").exists()
            )
            assert (
                has_python_files
            ), f"Directory '{directory}' should contain Python package files"

    def test_pip_schedule_appropriate(self, pip_updates):
        """Test that pip updates have appropriate schedule."""
        appropriate_intervals = {"daily", "weekly"}
        for update in pip_updates:
            interval = update["schedule"]["interval"]
            assert (
                interval in appropriate_intervals
            ), f"Pip updates should use 'daily' or 'weekly' interval, got '{interval}'"


class TestDependabotEdgeCases:
    """Tests for edge cases and potential issues."""

    @pytest.fixture
    def dependabot_config(self):
        """Load dependabot configuration."""
        with open(".github/dependabot.yml") as f:
            return yaml.safe_load(f)

    def test_no_duplicate_ecosystems_same_directory(self, dependabot_config):
        """Test that same ecosystem is not configured twice for same directory."""
        updates = dependabot_config["updates"]
        seen = set()
        for update in updates:
            key = (update["package-ecosystem"], update["directory"])
            assert (
                key not in seen
            ), f"Duplicate configuration: {update['package-ecosystem']} in {update['directory']}"
            seen.add(key)

    def test_schedule_has_no_extra_invalid_fields(self, dependabot_config):
        """Test that schedule doesn't have obviously invalid fields."""
        valid_schedule_fields = {"interval", "day", "time", "timezone"}
        
        for i, update in enumerate(dependabot_config["updates"]):
            schedule = update["schedule"]
            for field in schedule.keys():
                assert (
                    field in valid_schedule_fields
                ), f"Update {i}: schedule has invalid field '{field}'"

    def test_update_configs_are_dictionaries(self, dependabot_config):
        """Test that each update configuration is a dictionary."""
        for i, update in enumerate(dependabot_config["updates"]):
            assert isinstance(
                update, dict
            ), f"Update {i} must be a dictionary"

    def test_no_unexpected_root_fields(self, dependabot_config):
        """Test that configuration doesn't have unexpected root-level fields."""
        expected_fields = {"version", "updates", "registries", "enable-beta-ecosystems"}
        
        for field in dependabot_config.keys():
            assert (
                field in expected_fields
            ), f"Unexpected root field '{field}'"


class TestDependabotConfigurationQuality:
    """Tests for configuration quality and best practices."""

    @pytest.fixture
    def dependabot_file(self):
        """Path to dependabot.yml file."""
        return Path(".github/dependabot.yml")

    @pytest.fixture
    def dependabot_content(self, dependabot_file):
        """Get raw file content."""
        return dependabot_file.read_text()

    def test_file_has_comments(self, dependabot_content):
        """Test that configuration has helpful comments."""
        assert "#" in dependabot_content, "Configuration should have comments"

    def test_proper_yaml_indentation(self, dependabot_content):
        """Test that YAML uses consistent indentation (2 spaces)."""
        lines = dependabot_content.split("\n")
        for line_num, line in enumerate(lines, 1):
            if line.strip() and not line.strip().startswith("#"):
                leading_spaces = len(line) - len(line.lstrip(" "))
                if leading_spaces > 0:
                    assert (
                        leading_spaces % 2 == 0
                    ), f"Line {line_num} has inconsistent indentation"

    def test_file_ends_with_newline(self, dependabot_content):
        """Test that file ends with a newline character."""
        assert dependabot_content.endswith(
            "\n"
        ), "File should end with a newline character"

    def test_no_trailing_whitespace(self, dependabot_content):
        """Test that lines don't have trailing whitespace."""
        lines = dependabot_content.split("\n")
        for line_num, line in enumerate(lines, 1):
            if line and line != line.rstrip():
                pytest.fail(f"Line {line_num} has trailing whitespace")


class TestDependabotConfigurationIntegration:
    """Integration tests for Dependabot configuration."""

    @pytest.fixture
    def repo_root(self):
        """Get repository root path."""
        return Path(".")

    @pytest.fixture
    def dependabot_config(self):
        """Load dependabot configuration."""
        with open(".github/dependabot.yml") as f:
            return yaml.safe_load(f)

    def test_configured_directories_exist(self, dependabot_config, repo_root):
        """Test that all configured directories exist in repository."""
        for i, update in enumerate(dependabot_config["updates"]):
            directory = update["directory"].lstrip("/")
            if not directory:
                directory = "."
            
            dir_path = repo_root / directory
            assert dir_path.exists(), \
                f"Update {i}: Directory '{directory}' does not exist"
            assert dir_path.is_dir(), \
                f"Update {i}: Path '{directory}' is not a directory"

    def test_ecosystem_matches_repo_files(self, dependabot_config, repo_root):
        """Test that configured ecosystems match actual package files."""
        ecosystem_files = {
            "pip": ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"],
            "npm": ["package.json"],
            "bundler": ["Gemfile"],
            "cargo": ["Cargo.toml"],
            "composer": ["composer.json"],
            "gomod": ["go.mod"],
            "github-actions": [],
        }
        
        for update in dependabot_config["updates"]:
            ecosystem = update["package-ecosystem"]
            directory = update["directory"].lstrip("/")
            if not directory:
                directory = "."
            
            dir_path = repo_root / directory
            
            if ecosystem in ecosystem_files:
                expected_files = ecosystem_files[ecosystem]
                if expected_files:
                    has_expected_file = any(
                        (dir_path / f).exists() or
                        any(dir_path.glob(f"*{f}"))
                        for f in expected_files
                    )
                    assert has_expected_file, \
                        f"Ecosystem '{ecosystem}' in '{directory}' missing package files"


class TestDependabotScheduleConfiguration:
    """Detailed tests for schedule configuration."""

    @pytest.fixture
    def dependabot_config(self):
        """Load dependabot configuration."""
        with open(".github/dependabot.yml") as f:
            return yaml.safe_load(f)

    def test_schedule_interval_is_lowercase(self, dependabot_config):
        """Test that schedule intervals are lowercase."""
        for i, update in enumerate(dependabot_config["updates"]):
            interval = update["schedule"]["interval"]
            assert interval == interval.lower(), \
                f"Update {i}: interval should be lowercase"

    def test_daily_schedule_consistency(self, dependabot_config):
        """Test consistency for daily schedules."""
        daily_updates = [
            u for u in dependabot_config["updates"]
            if u["schedule"]["interval"] == "daily"
        ]
        
        for update in daily_updates:
            schedule = update["schedule"]
            assert "day" not in schedule, \
                "Daily schedule should not specify 'day' field"

    def test_weekly_schedule_has_day_if_specified(self, dependabot_config):
        """Test that weekly schedules have valid day if specified."""
        valid_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        weekly_updates = [
            u for u in dependabot_config["updates"]
            if u["schedule"]["interval"] == "weekly"
        ]
        
        for update in weekly_updates:
            schedule = update["schedule"]
            if "day" in schedule:
                day = schedule["day"]
                assert day in valid_days, \
                    f"Weekly schedule day '{day}' not valid"

    def test_time_format_if_specified(self, dependabot_config):
        """Test that time is in valid format if specified (HH:MM)."""
        import re
        time_pattern = re.compile(r"^([0-1][0-9]|2[0-3]):[0-5][0-9]$")
        
        for i, update in enumerate(dependabot_config["updates"]):
            schedule = update["schedule"]
            if "time" in schedule:
                time = schedule["time"]
                assert time_pattern.match(time), \
                    f"Update {i}: time '{time}' should be in HH:MM format"


class TestDependabotSecurityBestPractices:
    """Tests for security and best practice configurations."""

    @pytest.fixture
    def dependabot_config(self):
        """Load dependabot configuration."""
        with open(".github/dependabot.yml") as f:
            return yaml.safe_load(f)

    def test_no_insecure_registries_without_token(self, dependabot_config):
        """Test that private registries are properly configured."""
        if "registries" in dependabot_config:
            registries = dependabot_config["registries"]
            for name, config in registries.items():
                has_auth = any(
                    key in config for key in ["token", "username", "password", "key"]
                )
                assert has_auth, \
                    f"Registry '{name}' should have authentication configured"

    def test_recommended_interval_for_security(self, dependabot_config):
        """Test that security-critical ecosystems use appropriate intervals."""
        security_critical = {"pip", "npm", "bundler", "composer", "maven", "gradle"}
        recommended_intervals = {"daily", "weekly"}
        
        for update in dependabot_config["updates"]:
            ecosystem = update["package-ecosystem"]
            if ecosystem in security_critical:
                interval = update["schedule"]["interval"]
                assert interval in recommended_intervals, \
                    f"Security-critical ecosystem '{ecosystem}' should use frequent updates"

    def test_no_overly_broad_ignore_patterns(self, dependabot_config):
        """Test that ignore configurations aren't too broad."""
        for i, update in enumerate(dependabot_config["updates"]):
            if "ignore" in update:
                ignore_list = update["ignore"]
                for ignore_entry in ignore_list:
                    assert ignore_entry.get("dependency-name") != "*", \
                        f"Update {i}: Should not ignore ALL dependencies"