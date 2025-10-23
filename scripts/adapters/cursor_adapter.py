"""Transform unified format to Cursor IDE format."""

from pathlib import Path
from typing import Any


class CursorAdapter:
    """Transform unified format to Cursor .mdc and command format."""

    def __init__(self):
        """Initialize the Cursor adapter."""
        self.trigger_mapping = {
            "always_on": {"alwaysApply": True},
            "glob": {"alwaysApply": False},  # Will add globs field
            "model_decision": {"alwaysApply": False},  # Intelligent application via description
            "manual": {"alwaysApply": False},  # Manual reference only
        }

    def transform_rule(self, unified_data: dict[str, Any]) -> dict[str, Any]:
        """Transform unified rule to Cursor .mdc format.

        Args:
            unified_data: Parsed unified rule data

        Returns:
            Cursor rule data ready for .mdc file generation
        """
        frontmatter = unified_data["frontmatter"]
        content = unified_data["content"]

        # Extract Windsurf configuration
        windsurf_config = frontmatter["windsurf"]
        trigger = windsurf_config["trigger"]

        # Build Cursor configuration
        cursor_config = self.trigger_mapping[trigger].copy()

        # Handle glob patterns - only for 'glob' trigger
        if trigger == "glob":
            # Check windsurf config first, then cursor config
            if "globs" in windsurf_config:
                globs_str = windsurf_config["globs"]
                if globs_str:
                    # Keep as raw, unquoted comma-separated string for Cursor
                    cursor_config["globs"] = globs_str
            elif "globs" in cursor_config:
                # Use globs from cursor config if available
                globs_str = cursor_config["globs"]
                if globs_str:
                    cursor_config["globs"] = globs_str

        # Add description (required for Cursor)
        cursor_config["description"] = frontmatter["description"]

        # Add title if present
        if "title" in frontmatter:
            cursor_config["title"] = frontmatter["title"]

        # Add other metadata
        if "tags" in frontmatter:
            cursor_config["tags"] = frontmatter["tags"]

        if "related" in frontmatter:
            cursor_config["related"] = frontmatter["related"]

        return {
            "frontmatter": cursor_config,
            "content": content,
            "file_name": unified_data["file_name"],
            "file_path": unified_data["file_path"],
        }

    def transform_command(self, unified_data: dict[str, Any]) -> dict[str, Any]:
        """Transform unified command to Cursor markdown format.

        Args:
            unified_data: Parsed unified command data

        Returns:
            Cursor command data ready for markdown file generation
        """
        frontmatter = unified_data["frontmatter"]
        content = unified_data["content"]

        # Cursor commands are simpler - mostly pass-through
        cursor_config = frontmatter["cursor"].copy()

        # Add description
        cursor_config["description"] = frontmatter["description"]

        # Add title if present
        if "title" in frontmatter:
            cursor_config["title"] = frontmatter["title"]

        # Add other metadata
        if "tags" in frontmatter:
            cursor_config["tags"] = frontmatter["tags"]

        if "related" in frontmatter:
            cursor_config["related"] = frontmatter["related"]

        return {
            "frontmatter": cursor_config,
            "content": content,
            "file_name": unified_data["file_name"],
            "file_path": unified_data["file_path"],
        }

    def generate_mdc_file(self, cursor_rule_data: dict[str, Any], output_path: str) -> None:
        """Generate a Cursor .mdc file from transformed rule data.

        Args:
            cursor_rule_data: Transformed rule data
            output_path: Path to write the .mdc file
        """
        frontmatter = cursor_rule_data["frontmatter"]
        content = cursor_rule_data["content"]

        # Build the .mdc content
        mdc_content = "---\n"

        # Add frontmatter fields
        for key, value in frontmatter.items():
            if key == "globs" and isinstance(value, list):
                # Format globs as array
                mdc_content += f"{key}: {value}\n"
            elif key == "alwaysApply" and isinstance(value, bool):
                mdc_content += f"{key}: {str(value).lower()}\n"
            else:
                mdc_content += f"{key}: {value}\n"

        mdc_content += "---\n\n"
        mdc_content += content

        # Write the file
        Path(output_path).write_text(mdc_content, encoding="utf-8")

    def generate_command_file(self, cursor_command_data: dict[str, Any], output_path: str) -> None:
        """Generate a Cursor command markdown file from transformed command data.

        Args:
            cursor_command_data: Transformed command data
            output_path: Path to write the markdown file
        """
        frontmatter = cursor_command_data["frontmatter"]
        content = cursor_command_data["content"]

        # Build the markdown content
        md_content = "---\n"

        # Add frontmatter fields
        for key, value in frontmatter.items():
            if isinstance(value, list):
                md_content += f"{key}: {value}\n"
            elif isinstance(value, bool):
                md_content += f"{key}: {str(value).lower()}\n"
            else:
                md_content += f"{key}: {value}\n"

        md_content += "---\n\n"
        md_content += content

        # Write the file
        Path(output_path).write_text(md_content, encoding="utf-8")

    def transform_globs_format(self, globs_str: str) -> list[str]:
        """Convert Windsurf globs format to Cursor format.

        Args:
            globs_str: Comma-separated globs string from Windsurf

        Returns:
            List of glob patterns for Cursor
        """
        if not globs_str:
            return []

        # Split by comma and clean up
        globs = [g.strip() for g in globs_str.split(",") if g.strip()]

        # Cursor uses the same glob syntax as Windsurf
        return globs

    def validate_cursor_rule(self, cursor_rule_data: dict[str, Any]) -> bool:
        """Validate Cursor rule format.

        Args:
            cursor_rule_data: Cursor rule data to validate

        Returns:
            True if valid, False otherwise
        """
        frontmatter = cursor_rule_data["frontmatter"]

        # Check required fields
        if "description" not in frontmatter:
            return False

        # Check globs format if present
        if "globs" in frontmatter:
            globs = frontmatter["globs"]
            if not isinstance(globs, list):
                return False

        # Check alwaysApply format if present
        if "alwaysApply" in frontmatter:
            if not isinstance(frontmatter["alwaysApply"], bool):
                return False

        return True

    def validate_cursor_command(self, cursor_command_data: dict[str, Any]) -> bool:
        """Validate Cursor command format.

        Args:
            cursor_command_data: Cursor command data to validate

        Returns:
            True if valid, False otherwise
        """
        frontmatter = cursor_command_data["frontmatter"]

        # Check required fields
        if "description" not in frontmatter:
            return False

        return True
