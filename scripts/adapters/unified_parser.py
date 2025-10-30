"""Parse unified format YAML files for IDE configuration generation."""

import re
from pathlib import Path
from typing import Any

import yaml


class UnifiedParser:
    """Parse unified format YAML files with frontmatter and content."""

    def __init__(self):
        """Initialize the parser."""
        self.frontmatter_pattern = re.compile(
            r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL | re.MULTILINE
        )

    def parse(self, file_path: str) -> dict[str, Any]:
        """Parse unified file and return structured data.

        Args:
            file_path: Path to the unified format file

        Returns:
            Dictionary with 'frontmatter' and 'content' keys

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = path.read_text(encoding="utf-8")

        # Extract frontmatter and content
        match = self.frontmatter_pattern.match(content)
        if not match:
            raise ValueError(f"Invalid unified format in {file_path}: missing frontmatter")

        frontmatter_text, content_text = match.groups()

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML frontmatter in {file_path}: {e}")

        if not isinstance(frontmatter, dict):
            raise ValueError(f"Frontmatter must be a dictionary in {file_path}")

        return {
            "frontmatter": frontmatter,
            "content": content_text.strip(),
            "file_path": str(path),
            "file_name": path.stem,
        }

    def parse_rule(self, file_path: str) -> dict[str, Any]:
        """Parse a unified rule file.

        Args:
            file_path: Path to the unified rule file

        Returns:
            Parsed rule data with validation

        Raises:
            ValueError: If rule format is invalid
        """
        data = self.parse(file_path)
        frontmatter = data["frontmatter"]

        # Validate required fields
        required_fields = ["title", "description", "type"]
        for field in required_fields:
            if field not in frontmatter:
                raise ValueError(f"Missing required field '{field}' in {file_path}")

        if frontmatter["type"] != "rule":
            raise ValueError(f"Expected type 'rule' in {file_path}")

        # Validate Windsurf configuration
        if "windsurf" not in frontmatter:
            raise ValueError(f"Missing 'windsurf' configuration in {file_path}")

        windsurf_config = frontmatter["windsurf"]
        if "trigger" not in windsurf_config:
            raise ValueError(f"Missing 'trigger' in windsurf config in {file_path}")

        valid_triggers = ["always_on", "glob", "model_decision", "manual"]
        if windsurf_config["trigger"] not in valid_triggers:
            raise ValueError(
                f"Invalid trigger '{windsurf_config['trigger']}' in {file_path}. "
                f"Must be one of: {valid_triggers}"
            )

        # Validate Cursor configuration
        if "cursor" not in frontmatter:
            raise ValueError(f"Missing 'cursor' configuration in {file_path}")

        cursor_config = frontmatter["cursor"]
        if "alwaysApply" not in cursor_config:
            raise ValueError(f"Missing 'alwaysApply' in cursor config in {file_path}")

        return data

    def parse_command(self, file_path: str) -> dict[str, Any]:
        """Parse a unified command file.

        Args:
            file_path: Path to the unified command file

        Returns:
            Parsed command data with validation

        Raises:
            ValueError: If command format is invalid
        """
        data = self.parse(file_path)
        frontmatter = data["frontmatter"]

        # Validate required fields
        required_fields = ["title", "description", "type"]
        for field in required_fields:
            if field not in frontmatter:
                raise ValueError(f"Missing required field '{field}' in {file_path}")

        if frontmatter["type"] != "command":
            raise ValueError(f"Expected type 'command' in {file_path}")

        # Validate Windsurf configuration
        if "windsurf" not in frontmatter:
            raise ValueError(f"Missing 'windsurf' configuration in {file_path}")

        windsurf_config = frontmatter["windsurf"]
        if "type" not in windsurf_config:
            raise ValueError(f"Missing 'type' in windsurf config in {file_path}")

        # Validate Cursor configuration
        if "cursor" not in frontmatter:
            raise ValueError(f"Missing 'cursor' configuration in {file_path}")

        return data

    def list_unified_files(self, directory: str, file_type: str) -> list[str]:
        """List all unified files of a specific type.

        Args:
            directory: Directory to search in
            file_type: Type of files to find ('rule' or 'command')

        Returns:
            List of file paths
        """
        path = Path(directory)
        if not path.exists():
            return []

        files = []
        for file_path in path.glob("*.md"):
            try:
                data = self.parse(str(file_path))
                if data["frontmatter"].get("type") == file_type:
                    files.append(str(file_path))
            except (ValueError, yaml.YAMLError):
                # Skip invalid files, but log warning
                print(f"Warning: Skipping invalid file {file_path}")
                continue

        return sorted(files)
