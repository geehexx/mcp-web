"""
Unit tests for initiative validation script.

Tests validation of frontmatter fields, status consistency, success criteria,
and phase integrity per Initiative System Lifecycle Improvements (2025-10-19).
"""

import tempfile
from pathlib import Path

import pytest

from scripts.validation.validate_initiatives import InitiativeValidator


@pytest.fixture
def temp_initiatives_dir():
    """Create temporary initiatives directory structure."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        (base / "active").mkdir()
        (base / "completed").mkdir()
        yield base


@pytest.fixture
def valid_initiative_content():
    """Valid initiative file content with all required fields."""
    return """---
Status: Active
Created: 2025-10-19
Owner: Test User
Priority: High
Estimated Duration: 10 hours
Target Completion: 2025-10-26
---

# Test Initiative

## Objective

Test objective here.

## Success Criteria

- [ ] Criterion 1
- [ ] Criterion 2
- [x] Criterion 3

## Tasks

- [ ] Task 1
- [ ] Task 2
"""


@pytest.fixture
def completed_initiative_content():
    """Completed initiative content."""
    return """---
Status: Completed
Created: 2025-10-15
Completed: 2025-10-18
Owner: Test User
Priority: High
---

# Completed Initiative

## Success Criteria

- [x] All tasks done
- [x] Tests passing

## Tasks

- [x] Task 1
- [x] Task 2
"""


class TestInitiativeValidator:
    """Test InitiativeValidator class."""

    def test_validate_valid_initiative(self, temp_initiatives_dir, valid_initiative_content):
        """Test validation passes for valid initiative."""
        # Create test file
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(valid_initiative_content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have no critical or warning failures
        critical_failures = [r for r in results if r.severity == "critical" and not r.passed]
        assert len(critical_failures) == 0, f"Unexpected critical failures: {critical_failures}"

    def test_missing_required_field(self, temp_initiatives_dir):
        """Test validation fails when required field is missing."""
        content = """---
Created: 2025-10-19
Owner: Test User
# Missing Status and Priority
---

# Test Initiative
"""
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have critical failures for missing Status and Priority
        critical_failures = [r for r in results if r.severity == "critical" and not r.passed]
        assert len(critical_failures) >= 2
        assert any("Status" in r.message for r in critical_failures)
        assert any("Priority" in r.message for r in critical_failures)

    def test_invalid_date_format(self, temp_initiatives_dir):
        """Test validation warns on invalid date format."""
        content = """---
Status: Active
Created: 10/19/2025
Owner: Test User
Priority: High
---

# Test Initiative
"""
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have warning for invalid date format
        warnings = [r for r in results if r.severity == "warning" and not r.passed]
        assert any("YYYY-MM-DD" in r.message for r in warnings)

    def test_status_location_mismatch(self, temp_initiatives_dir, completed_initiative_content):
        """Test validation fails when completed initiative is in active directory."""
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(completed_initiative_content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have critical failure for status-location mismatch
        critical_failures = [r for r in results if r.severity == "critical" and not r.passed]
        assert any("completed/" in r.message.lower() for r in critical_failures)

    def test_active_without_unchecked_tasks(self, temp_initiatives_dir):
        """Test validation warns when active initiative has no unchecked tasks."""
        content = """---
Status: Active
Created: 2025-10-19
Owner: Test User
Priority: High
---

# Test Initiative

## Tasks

- [x] Task 1
- [x] Task 2
"""
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have warning suggesting completion
        warnings = [r for r in results if r.severity == "warning" and not r.passed]
        assert any("completed" in r.message.lower() for r in warnings)

    def test_missing_success_criteria(self, temp_initiatives_dir):
        """Test validation warns when success criteria section is missing."""
        content = """---
Status: Active
Created: 2025-10-19
Owner: Test User
Priority: High
---

# Test Initiative

## Objective

Test objective.

## Tasks

- [ ] Task 1
"""
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have warning for missing success criteria
        warnings = [r for r in results if r.severity == "warning" and not r.passed]
        assert any("success criteria" in r.message.lower() for r in warnings)

    def test_validate_all_initiatives(self, temp_initiatives_dir, valid_initiative_content):
        """Test validate_all finds and validates multiple initiatives."""
        # Create multiple test files
        (temp_initiatives_dir / "active" / "init1.md").write_text(valid_initiative_content)
        (temp_initiatives_dir / "active" / "init2.md").write_text(valid_initiative_content)

        # Create folder-based initiative
        folder_init = temp_initiatives_dir / "active" / "2025-10-19-folder-init"
        folder_init.mkdir()
        (folder_init / "initiative.md").write_text(valid_initiative_content)

        validator = InitiativeValidator(temp_initiatives_dir)
        all_results = validator.validate_all()

        # Should find all 3 initiatives
        assert len(all_results) == 3

    def test_folder_based_with_phases(self, temp_initiatives_dir, valid_initiative_content):
        """Test validation checks for phases directory in folder-based initiatives."""
        folder_init = temp_initiatives_dir / "active" / "2025-10-19-test-init"
        folder_init.mkdir()
        (folder_init / "initiative.md").write_text(valid_initiative_content)

        # Create empty phases directory
        (folder_init / "phases").mkdir()

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(folder_init / "initiative.md")

        # Should have info message about empty phases directory
        infos = [r for r in results if r.severity == "info"]
        assert any("phases/" in r.message and "empty" in r.message for r in infos)

    def test_invalid_status_value(self, temp_initiatives_dir):
        """Test validation warns on invalid status value."""
        content = """---
Status: InProgress
Created: 2025-10-19
Owner: Test User
Priority: High
---

# Test Initiative
"""
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have warning for invalid status
        warnings = [r for r in results if r.severity == "warning" and not r.passed]
        assert any(
            "status" in r.message.lower() and "invalid" in r.message.lower() for r in warnings
        )

    def test_recommended_fields(self, temp_initiatives_dir):
        """Test validation provides info on missing recommended fields."""
        content = """---
Status: Active
Created: 2025-10-19
Owner: Test User
Priority: High
---

# Test Initiative
"""
        test_file = temp_initiatives_dir / "active" / "test-initiative.md"
        test_file.write_text(content)

        validator = InitiativeValidator(temp_initiatives_dir)
        results = validator.validate_file(test_file)

        # Should have info about missing recommended fields
        infos = [r for r in results if r.severity == "info"]
        recommended_fields = ["Estimated Duration", "Target Completion", "Updated"]
        for field in recommended_fields:
            assert any(field in r.message for r in infos)
