"""Transform unified format to Windsurf IDE format."""

import re
from pathlib import Path
from typing import Any


def _ensure_trailing_newline(text: str) -> str:
    """Guarantee text ends with a single newline."""

    return text if text.endswith("\n") else f"{text}\n"


def _normalize_content(text: str) -> str:
    """Ensure lists have blank lines separating them from preceding paragraphs."""

    return re.sub(r"(\*\*[^*\n]+?\*\*:)(\n)([-\d])", r"\1\2\n\3", text)


class WindsurfAdapter:
    """Transform unified format to Windsurf .md format."""

    def __init__(self):
        """Initialize the Windsurf adapter."""
        self.trigger_mapping = {
            "always_on": "always_on",
            "glob": "glob",
            "model_decision": "model_decision",
            "manual": "manual",
        }

    def transform_rule(self, unified_data: dict[str, Any]) -> dict[str, Any]:
        """Transform unified rule to Windsurf .md format.

        Args:
            unified_data: Parsed unified rule data

        Returns:
            Windsurf rule data ready for .md file generation
        """
        frontmatter = unified_data["frontmatter"]
        content = unified_data["content"]

        # Extract Windsurf configuration
        windsurf_config = frontmatter["windsurf"]

        # Build Windsurf frontmatter
        windsurf_frontmatter = {}

        # Add trigger
        windsurf_frontmatter["trigger"] = windsurf_config["trigger"]

        # Add description if present
        if "description" in frontmatter:
            windsurf_frontmatter["description"] = frontmatter["description"]

        # Add title if present
        if "title" in frontmatter:
            windsurf_frontmatter["title"] = frontmatter["title"]

        # Add globs if present
        if "globs" in windsurf_config:
            windsurf_frontmatter["globs"] = windsurf_config["globs"]

        return {
            "frontmatter": windsurf_frontmatter,
            "content": content,
            "file_name": unified_data["file_name"],
            "file_path": unified_data["file_path"],
        }

    def transform_workflow(self, unified_data: dict[str, Any]) -> dict[str, Any]:
        """Transform unified command to Windsurf workflow format.

        Args:
            unified_data: Parsed unified command data

        Returns:
            Windsurf workflow data ready for .md file generation
        """
        frontmatter = unified_data["frontmatter"]
        content = unified_data["content"]

        # Extract Windsurf configuration
        windsurf_config = frontmatter["windsurf"]

        # Build Windsurf frontmatter
        windsurf_frontmatter = {}

        # Add required fields
        windsurf_frontmatter["description"] = frontmatter["description"]

        # Add title if present
        if "title" in frontmatter:
            windsurf_frontmatter["title"] = frontmatter["title"]

        # Add Windsurf-specific fields
        if "type" in windsurf_config:
            windsurf_frontmatter["type"] = windsurf_config["type"]

        if "category" in windsurf_config:
            windsurf_frontmatter["category"] = windsurf_config["category"]

        if "complexity" in windsurf_config:
            windsurf_frontmatter["complexity"] = windsurf_config["complexity"]

        if "dependencies" in windsurf_config:
            windsurf_frontmatter["dependencies"] = windsurf_config["dependencies"]

        # Add metadata
        windsurf_frontmatter["status"] = frontmatter.get("status", "active")

        # Add timestamps if not present
        if "created" not in windsurf_frontmatter:
            windsurf_frontmatter["created"] = "2025-10-22"
        if "updated" not in windsurf_frontmatter:
            windsurf_frontmatter["updated"] = "2025-10-22"

        return {
            "frontmatter": windsurf_frontmatter,
            "content": content,
            "file_name": unified_data["file_name"],
            "file_path": unified_data["file_path"],
        }

    def generate_rule_file(self, windsurf_rule_data: dict[str, Any], output_path: str) -> None:
        """Generate a Windsurf .md file from transformed rule data.

        Args:
            windsurf_rule_data: Transformed rule data
            output_path: Path to write the .md file
        """
        frontmatter = windsurf_rule_data["frontmatter"]
        content = _normalize_content(windsurf_rule_data["content"])

        # Build the .md content
        md_content = "---\n"

        # Add frontmatter fields
        for key, value in frontmatter.items():
            if isinstance(value, list):
                md_content += f"{key}: {value}\n"
            else:
                md_content += f"{key}: {value}\n"

        md_content += "---\n\n"
        md_content += content

        # Write the file
        Path(output_path).write_text(_ensure_trailing_newline(md_content), encoding="utf-8")

    def generate_workflow_file(
        self, windsurf_workflow_data: dict[str, Any], output_path: str
    ) -> None:
        """Generate a Windsurf workflow .md file from transformed workflow data.

        Args:
            windsurf_workflow_data: Transformed workflow data
            output_path: Path to write the .md file
        """
        frontmatter = windsurf_workflow_data["frontmatter"]
        content = _normalize_content(windsurf_workflow_data["content"])

        # Build the .md content
        md_content = "---\n"

        # Add frontmatter fields
        for key, value in frontmatter.items():
            if isinstance(value, list):
                md_content += f"{key}: {value}\n"
            else:
                md_content += f"{key}: {value}\n"

        md_content += "---\n\n"
        md_content += content

        # Write the file
        Path(output_path).write_text(_ensure_trailing_newline(md_content), encoding="utf-8")

    def transform_globs_format(self, globs_list: list[str]) -> str:
        """Convert Cursor globs format to Windsurf format.

        Args:
            globs_list: List of glob patterns from Cursor

        Returns:
            Comma-separated globs string for Windsurf
        """
        if not globs_list:
            return ""

        # Join with commas and spaces
        return ", ".join(globs_list)

    def validate_windsurf_rule(self, windsurf_rule_data: dict[str, Any]) -> bool:
        """Validate Windsurf rule format.

        Args:
            windsurf_rule_data: Windsurf rule data to validate

        Returns:
            True if valid, False otherwise
        """
        frontmatter = windsurf_rule_data["frontmatter"]

        # Check required fields
        if "trigger" not in frontmatter:
            return False

        # Check trigger value
        valid_triggers = ["always_on", "glob", "model_decision", "manual"]
        if frontmatter["trigger"] not in valid_triggers:
            return False

        description = frontmatter.get("description")
        return description is None or isinstance(description, str)

    def validate_windsurf_workflow(self, windsurf_workflow_data: dict[str, Any]) -> bool:
        """Validate Windsurf workflow format.

        Args:
            windsurf_workflow_data: Windsurf workflow data to validate

        Returns:
            True if valid, False otherwise
        """
        frontmatter = windsurf_workflow_data["frontmatter"]

        # Check required fields
        if "description" not in frontmatter:
            return False

        # Check description is string
        return isinstance(frontmatter["description"], str)
