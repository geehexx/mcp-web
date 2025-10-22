"""
Golden Master tests for validate_workflows.py

Tests workflow and rule validation including frontmatter schema, cross-references,
and complexity metrics.
"""

import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_windsurf_dir():
    """Create temporary .windsurf directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir) / ".windsurf"
        workflows_dir = base / "workflows"
        rules_dir = base / "rules"
        schemas_dir = base / "schemas"

        workflows_dir.mkdir(parents=True)
        rules_dir.mkdir(parents=True)
        schemas_dir.mkdir(parents=True)

        yield base


@pytest.fixture
def valid_workflow_content():
    """Valid workflow file with frontmatter."""
    return """---
created: "2025-10-15"
updated: "2025-10-22"
description: Test workflow for validation
category: Testing
complexity: 50
tokens: 500
---

# Test Workflow

## Stage 1: Setup

Test content here.

See [other-workflow.md](./other-workflow.md) for details.
"""


@pytest.fixture
def valid_rule_content():
    """Valid rule file with frontmatter."""
    return """---
trigger: always_on
description: Test rule
estimated_tokens: 300
---

# Test Rule

Rule content here.
"""


class TestWorkflowValidator:
    """Test WorkflowValidator class."""

    def test_validate_valid_workflow(self, temp_windsurf_dir, valid_workflow_content):
        """Test validation passes for valid workflow."""
        from scripts.validation.validate_workflows import WorkflowValidator

        workflow_file = temp_windsurf_dir / "workflows" / "test-workflow.md"
        workflow_file.write_text(valid_workflow_content)

        # Create the referenced workflow to avoid broken link error
        other_workflow = temp_windsurf_dir / "workflows" / "other-workflow.md"
        other_workflow.write_text("""---
description: Other workflow
---
# Other Workflow
""")

        validator = WorkflowValidator()
        # Monkey patch ROOT to use temp directory
        import scripts.validation.validate_workflows as validate_module

        original_root = validate_module.ROOT
        validate_module.ROOT = temp_windsurf_dir.parent
        validate_module.WINDSURF_DIR = temp_windsurf_dir

        try:
            exit_code = validator.validate_all()
            assert exit_code == 0
            assert len(validator.errors) == 0
        finally:
            validate_module.ROOT = original_root

    def test_validate_missing_frontmatter(self, temp_windsurf_dir):
        """Test validation fails for missing frontmatter."""
        from scripts.validation.validate_workflows import WorkflowValidator

        workflow_file = temp_windsurf_dir / "workflows" / "no-frontmatter.md"
        workflow_file.write_text("# Workflow Without Frontmatter\n\nContent here.")

        validator = WorkflowValidator()
        import scripts.validation.validate_workflows as validate_module

        original_root = validate_module.ROOT
        validate_module.ROOT = temp_windsurf_dir.parent
        validate_module.WINDSURF_DIR = temp_windsurf_dir

        try:
            exit_code = validator.validate_all()
            assert exit_code == 1
            assert len(validator.errors) > 0
            assert any("frontmatter" in err.lower() for err in validator.errors)
        finally:
            validate_module.ROOT = original_root

    def test_validate_broken_link(self, temp_windsurf_dir, valid_workflow_content):
        """Test validation detects broken links."""
        from scripts.validation.validate_workflows import WorkflowValidator

        workflow_file = temp_windsurf_dir / "workflows" / "test-workflow.md"
        workflow_file.write_text(valid_workflow_content)

        validator = WorkflowValidator()
        import scripts.validation.validate_workflows as validate_module

        original_root = validate_module.ROOT
        validate_module.ROOT = temp_windsurf_dir.parent
        validate_module.WINDSURF_DIR = temp_windsurf_dir

        try:
            validator.validate_all()
            # Should have error about broken link to other-workflow.md
            assert len(validator.errors) > 0
            assert any(
                "broken link" in err.lower() or "not found" in err.lower()
                for err in validator.errors
            )
        finally:
            validate_module.ROOT = original_root


class TestCLIIntegration:
    """Test CLI behavior."""

    def test_validate_workflows_help(self):
        """Test --help output."""
        result = subprocess.run(
            ["python", "scripts/validation/validate_workflows.py", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "workflow" in result.stdout.lower() or "usage" in result.stdout.lower()

    def test_validate_workflows_fix_mode(self):
        """Test --fix flag accepted."""
        result = subprocess.run(
            ["python", "scripts/validation/validate_workflows.py", "--fix"],
            capture_output=True,
            text=True,
        )

        # Should not crash (will fail validation but accept flag)
        assert result.returncode in [0, 1]


class TestEdgeCases:
    """Test edge cases."""

    def test_empty_workflow_file(self, temp_windsurf_dir):
        """Test with empty file."""
        from scripts.validation.validate_workflows import WorkflowValidator

        workflow_file = temp_windsurf_dir / "workflows" / "empty.md"
        workflow_file.write_text("")

        validator = WorkflowValidator()
        import scripts.validation.validate_workflows as validate_module

        original_root = validate_module.ROOT
        validate_module.ROOT = temp_windsurf_dir.parent
        validate_module.WINDSURF_DIR = temp_windsurf_dir

        try:
            exit_code = validator.validate_all()
            # Should handle gracefully
            assert isinstance(exit_code, int)
        finally:
            validate_module.ROOT = original_root

    def test_malformed_yaml_frontmatter(self, temp_windsurf_dir):
        """Test with malformed YAML."""
        from scripts.validation.validate_workflows import WorkflowValidator

        workflow_file = temp_windsurf_dir / "workflows" / "malformed.md"
        content = """---
description: "Unclosed quote
tokens: not_a_number
---

# Workflow
"""
        workflow_file.write_text(content)

        validator = WorkflowValidator()
        import scripts.validation.validate_workflows as validate_module

        original_root = validate_module.ROOT
        validate_module.ROOT = temp_windsurf_dir.parent
        validate_module.WINDSURF_DIR = temp_windsurf_dir

        try:
            # Should handle malformed YAML gracefully
            exit_code = validator.validate_all()
            assert isinstance(exit_code, int)
        finally:
            validate_module.ROOT = original_root
