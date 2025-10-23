"""Validate transformed rules and commands for IDE compatibility."""

from pathlib import Path
from typing import Any


class Validator:
    """Validate transformed rules and commands."""

    def __init__(self):
        """Initialize the validator."""
        self.cursor_required_fields = {"rule": ["description"], "command": ["description"]}

        self.windsurf_required_fields = {"rule": ["trigger"], "workflow": ["description"]}

    def validate_cursor_rule(self, rule_data: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate Cursor rule format.

        Args:
            rule_data: Cursor rule data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        frontmatter = rule_data.get("frontmatter", {})

        # Check required fields
        for field in self.cursor_required_fields["rule"]:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")

        # Check description format
        if "description" in frontmatter:
            if not isinstance(frontmatter["description"], str):
                errors.append("Description must be a string")

        # Check alwaysApply format
        if "alwaysApply" in frontmatter:
            if not isinstance(frontmatter["alwaysApply"], bool):
                errors.append("alwaysApply must be a boolean")

        # Check globs format
        if "globs" in frontmatter:
            globs = frontmatter["globs"]
            if not isinstance(globs, str):
                errors.append("globs must be a string (raw, unquoted comma-separated format)")

        # Check that either alwaysApply or globs is present (not both)
        has_always_apply = "alwaysApply" in frontmatter and frontmatter["alwaysApply"]
        has_globs = "globs" in frontmatter and frontmatter["globs"]

        if has_always_apply and has_globs:
            errors.append("Cannot have both alwaysApply=true and globs")

        return len(errors) == 0, errors

    def validate_cursor_command(self, command_data: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate Cursor command format.

        Args:
            command_data: Cursor command data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        frontmatter = command_data.get("frontmatter", {})

        # Check required fields
        for field in self.cursor_required_fields["command"]:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")

        # Check description format
        if "description" in frontmatter:
            if not isinstance(frontmatter["description"], str):
                errors.append("Description must be a string")

        return len(errors) == 0, errors

    def validate_windsurf_rule(self, rule_data: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate Windsurf rule format.

        Args:
            rule_data: Windsurf rule data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        frontmatter = rule_data.get("frontmatter", {})

        # Check required fields
        for field in self.windsurf_required_fields["rule"]:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")

        # Check trigger value
        if "trigger" in frontmatter:
            valid_triggers = ["always_on", "glob", "model_decision", "manual"]
            if frontmatter["trigger"] not in valid_triggers:
                errors.append(
                    f"Invalid trigger: {frontmatter['trigger']}. Must be one of: {valid_triggers}"
                )

        # Check description format
        if "description" in frontmatter:
            if not isinstance(frontmatter["description"], str):
                errors.append("Description must be a string")

        # Check globs format
        if "globs" in frontmatter:
            globs = frontmatter["globs"]
            if not isinstance(globs, str):
                errors.append("globs must be a string (comma-separated)")

        return len(errors) == 0, errors

    def validate_windsurf_workflow(self, workflow_data: dict[str, Any]) -> tuple[bool, list[str]]:
        """Validate Windsurf workflow format.

        Args:
            workflow_data: Windsurf workflow data to validate

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        frontmatter = workflow_data.get("frontmatter", {})

        # Check required fields
        for field in self.windsurf_required_fields["workflow"]:
            if field not in frontmatter:
                errors.append(f"Missing required field: {field}")

        # Check description format
        if "description" in frontmatter:
            if not isinstance(frontmatter["description"], str):
                errors.append("Description must be a string")

        # Check complexity format
        if "complexity" in frontmatter:
            valid_complexities = ["simple", "moderate", "complex"]
            if frontmatter["complexity"] not in valid_complexities:
                errors.append(
                    f"Invalid complexity: {frontmatter['complexity']}. Must be one of: {valid_complexities}"
                )

        # Check dependencies format
        if "dependencies" in frontmatter:
            deps = frontmatter["dependencies"]
            if not isinstance(deps, list):
                errors.append("dependencies must be a list")
            else:
                for i, dep in enumerate(deps):
                    if not isinstance(dep, str):
                        errors.append(f"dependencies[{i}] must be a string")

        return len(errors) == 0, errors

    def validate_file_exists(self, file_path: str) -> bool:
        """Validate that a file exists.

        Args:
            file_path: Path to check

        Returns:
            True if file exists, False otherwise
        """
        return Path(file_path).exists()

    def validate_file_content(
        self, file_path: str, expected_extension: str
    ) -> tuple[bool, list[str]]:
        """Validate file content format.

        Args:
            file_path: Path to the file to validate
            expected_extension: Expected file extension (e.g., '.mdc', '.md')

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        if not self.validate_file_exists(file_path):
            errors.append(f"File does not exist: {file_path}")
            return False, errors

        path = Path(file_path)

        # Check extension
        if path.suffix != expected_extension:
            errors.append(f"Expected extension {expected_extension}, got {path.suffix}")

        # Check file is readable
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Cannot read file: {e}")
            return False, errors

        # Check for frontmatter
        if not content.startswith("---"):
            errors.append("File does not start with frontmatter (---)")

        # Check for content after frontmatter
        if "---\n\n" not in content:
            errors.append("File does not have proper frontmatter/content separation")

        return len(errors) == 0, errors

    def validate_transformation_consistency(
        self,
        unified_data: dict[str, Any],
        cursor_data: dict[str, Any],
        windsurf_data: dict[str, Any],
    ) -> tuple[bool, list[str]]:
        """Validate that transformations maintain consistency.

        Args:
            unified_data: Original unified data
            cursor_data: Transformed Cursor data
            windsurf_data: Transformed Windsurf data

        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []

        # Check that content is preserved
        unified_content = unified_data.get("content", "")
        cursor_content = cursor_data.get("content", "")
        windsurf_content = windsurf_data.get("content", "")

        if unified_content != cursor_content:
            errors.append("Content not preserved in Cursor transformation")

        if unified_content != windsurf_content:
            errors.append("Content not preserved in Windsurf transformation")

        # Check that title is preserved
        unified_title = unified_data.get("frontmatter", {}).get("title", "")
        cursor_title = cursor_data.get("frontmatter", {}).get("title", "")
        windsurf_title = windsurf_data.get("frontmatter", {}).get("title", "")

        if unified_title and unified_title != cursor_title:
            errors.append("Title not preserved in Cursor transformation")

        if unified_title and unified_title != windsurf_title:
            errors.append("Title not preserved in Windsurf transformation")

        return len(errors) == 0, errors
