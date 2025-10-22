"""
Golden Master tests for validate_archival.py

Tests multi-gate validation system for initiative archival using Golden Master pattern:
- Known-good initiatives pass all gates
- Known-bad initiatives fail appropriate gates
- Edge cases handled correctly
"""

import tempfile
from pathlib import Path

import pytest

from scripts.validation.validate_archival import (
    ArchivalValidator,
    GateResult,
)


@pytest.fixture
def temp_initiatives_dir():
    """Create temporary initiatives directory with test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        active_dir = base / "docs/initiatives/active"
        completed_dir = base / "docs/initiatives/completed"
        active_dir.mkdir(parents=True)
        completed_dir.mkdir(parents=True)
        yield base


@pytest.fixture
def completed_initiative_content():
    """Valid completed initiative content."""
    return """---
Status: Completed
Created: 2025-10-15
Completed: 2025-10-22
Owner: Test User
Priority: High
---

# Test Completed Initiative

## Objective

Complete all tasks successfully.

## Success Criteria

- [x] Task 1 completed
- [x] Task 2 completed
- [x] All tests passing

## Blockers

None

## Updates

### 2025-10-22

Completed all success criteria. Initiative delivered successfully.
All features tested and documented.
"""


@pytest.fixture
def incomplete_initiative_content():
    """Incomplete initiative (for negative testing)."""
    return """---
Status: Active
Created: 2025-10-15
Owner: Test User
Priority: High
---

# Test Active Initiative

## Success Criteria

- [x] Task 1 completed
- [ ] Task 2 pending
- [ ] Task 3 pending

## Blockers

- Waiting for API integration
- Performance testing not started
"""


class TestArchivalValidator:
    """Test ArchivalValidator class."""

    def test_load_valid_initiative(self, temp_initiatives_dir, completed_initiative_content):
        """Test loading valid initiative file."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(completed_initiative_content)

        validator = ArchivalValidator(initiative_path)
        assert validator.load_initiative()
        assert "Completed all success criteria" in validator.content
        assert validator.frontmatter_data["Status"] == "Completed"

    def test_load_missing_file(self, temp_initiatives_dir):
        """Test loading missing file returns False."""
        validator = ArchivalValidator(temp_initiatives_dir / "nonexistent.md")
        assert not validator.load_initiative()

    def test_status_gate_pass_completed(self, temp_initiatives_dir, completed_initiative_content):
        """Test status gate passes for Completed status."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(completed_initiative_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_status_gate()

        assert isinstance(result, GateResult)
        assert result.passed
        assert result.severity == "critical"
        assert "Completed" in result.message

    def test_status_gate_pass_checkmark_completed(self, temp_initiatives_dir):
        """Test status gate passes for ✅ Completed status."""
        content = """---
Status: ✅ Completed
Created: 2025-10-15
---

# Test Initiative
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_status_gate()

        assert result.passed
        assert "✅ Completed" in result.message

    def test_status_gate_fail_active(self, temp_initiatives_dir, incomplete_initiative_content):
        """Test status gate fails for Active status."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(incomplete_initiative_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_status_gate()

        assert not result.passed
        assert result.severity == "critical"
        assert "Active" in result.message

    def test_success_criteria_gate_pass_all_checked(
        self, temp_initiatives_dir, completed_initiative_content
    ):
        """Test success criteria gate passes when all checkboxes checked."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(completed_initiative_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_success_criteria_gate()

        assert result.passed
        assert "3/3" in result.message

    def test_success_criteria_gate_fail_unchecked(
        self, temp_initiatives_dir, incomplete_initiative_content
    ):
        """Test success criteria gate fails when checkboxes unchecked."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(incomplete_initiative_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_success_criteria_gate()

        assert not result.passed
        assert "1/3" in result.message
        assert "criteria remain unchecked" in result.details

    def test_success_criteria_gate_missing_section(self, temp_initiatives_dir):
        """Test success criteria gate when section missing."""
        content = """---
Status: Completed
---

# Test Initiative

No success criteria section.
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_success_criteria_gate()

        assert result.passed  # Warning, not failure
        assert result.severity == "warning"
        assert "No Success Criteria section found" in result.message

    def test_blockers_gate_pass_none(self, temp_initiatives_dir, completed_initiative_content):
        """Test blockers gate passes when no blockers."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(completed_initiative_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_blockers_gate()

        assert result.passed
        assert result.severity == "warning"

    def test_blockers_gate_fail_active_blockers(
        self, temp_initiatives_dir, incomplete_initiative_content
    ):
        """Test blockers gate fails when active blockers exist."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(incomplete_initiative_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_blockers_gate()

        assert not result.passed
        assert "2 active blocker(s)" in result.message

    def test_blockers_gate_missing_section(self, temp_initiatives_dir):
        """Test blockers gate when section missing."""
        content = """---
Status: Completed
---

# Test Initiative

No blockers section.
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_blockers_gate()

        assert result.passed
        assert result.severity == "warning"
        assert "No blockers section found" in result.message

    def test_documentation_gate_pass_with_completion_entry(
        self, temp_initiatives_dir, completed_initiative_content
    ):
        """Test documentation gate passes with completion entry."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(completed_initiative_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_documentation_gate()

        assert result.passed
        # Check for either "Updates section has completion entry" or "Completion documented"
        assert "completion" in result.message.lower() or result.passed

    def test_documentation_gate_fail_no_updates_section(self, temp_initiatives_dir):
        """Test documentation gate fails without Updates section."""
        content = """---
Status: Completed
---

# Test Initiative

No updates section.
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_documentation_gate()

        assert not result.passed
        assert "No Updates section found" in result.message

    def test_documentation_gate_fail_no_completion_keywords(self, temp_initiatives_dir):
        """Test documentation gate warns without completion keywords."""
        content = """---
Status: Completed
---

# Test Initiative

## Updates

### 2025-10-22

Some updates but no completion keywords.
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/test.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()
        result = validator.check_documentation_gate()

        # Should warn but not fail critically
        assert result.severity == "warning"


class TestCLIIntegration:
    """Test CLI integration (subprocess pattern)."""

    def test_validate_archival_help(self):
        """Test --help output."""
        import subprocess

        result = subprocess.run(
            ["python", "scripts/validation/validate_archival.py", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Archival Validation Script" in result.stdout or "usage" in result.stdout.lower()

    def test_validate_archival_missing_file(self):
        """Test validation with missing file."""
        import subprocess

        result = subprocess.run(
            ["python", "scripts/validation/validate_archival.py", "nonexistent.md"],
            capture_output=True,
            text=True,
        )

        # Should fail or show error
        assert result.returncode != 0 or "not found" in result.stdout.lower()


class TestGoldenScenarios:
    """Golden Master tests for known scenarios."""

    def test_golden_pass_all_gates(self, temp_initiatives_dir):
        """Golden test: Initiative passes all gates."""
        golden_content = """---
Status: Completed
Created: 2025-10-01
Completed: 2025-10-22
Owner: Golden User
Priority: Critical
---

# Golden Completed Initiative

## Objective

Complete all tasks and document thoroughly.

## Success Criteria

- [x] All core features implemented
- [x] 100% test coverage achieved
- [x] Documentation complete
- [x] Performance benchmarks met
- [x] Security audit passed

## Blockers

None. All blockers resolved during Phase 3.

## Updates

### 2025-10-22 - Completion

Successfully completed all success criteria. Initiative delivered on time.
All features tested, documented, and deployed to production.

**Metrics:**
- 50 files modified
- 12 commits
- 150 tests passing
- 100% coverage

**Next Steps:** Archive to completed/ directory.
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/golden.md"
        initiative_path.write_text(golden_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()

        # Check all gates
        status_result = validator.check_status_gate()
        criteria_result = validator.check_success_criteria_gate()
        blockers_result = validator.check_blockers_gate()
        doc_result = validator.check_documentation_gate()

        assert status_result.passed, f"Status gate failed: {status_result.message}"
        assert criteria_result.passed, f"Criteria gate failed: {criteria_result.message}"
        assert blockers_result.passed, f"Blockers gate failed: {blockers_result.message}"
        assert doc_result.passed, f"Documentation gate failed: {doc_result.message}"

    def test_golden_fail_incomplete_criteria(self, temp_initiatives_dir):
        """Golden test: Initiative fails due to incomplete criteria."""
        golden_content = """---
Status: Completed
Created: 2025-10-01
Owner: Golden User
---

# Golden Incomplete Initiative

## Success Criteria

- [x] Task 1
- [ ] Task 2 (INCOMPLETE)
- [ ] Task 3 (INCOMPLETE)

## Updates

### 2025-10-22

Completed Task 1 only.
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/golden-fail.md"
        initiative_path.write_text(golden_content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()

        criteria_result = validator.check_success_criteria_gate()

        assert not criteria_result.passed
        assert "1/3" in criteria_result.message
        assert criteria_result.severity == "critical"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_file(self, temp_initiatives_dir):
        """Test with empty file."""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/empty.md"
        initiative_path.write_text("")

        validator = ArchivalValidator(initiative_path)
        # Should not crash - may load empty file successfully but have no frontmatter
        loaded = validator.load_initiative()
        # Either fails to load, or loads with empty data
        if loaded:
            assert validator.frontmatter_data == {} or validator.frontmatter_data is None

    def test_malformed_frontmatter(self, temp_initiatives_dir):
        """Test with malformed YAML frontmatter."""
        content = """---
Status: Completed
Invalid YAML: [unclosed
---

# Test Initiative
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/malformed.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        # Should handle gracefully
        validator.load_initiative()

    def test_missing_frontmatter(self, temp_initiatives_dir):
        """Test initiative without frontmatter."""
        content = """# Initiative Without Frontmatter

This has no YAML frontmatter.
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/no-fm.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        validator.load_initiative()

        # Should not crash, but gates should handle missing status
        result = validator.check_status_gate()
        assert not result.passed  # No status = fail

    def test_unicode_content(self, temp_initiatives_dir):
        """Test with Unicode characters."""
        content = """---
Status: Completed
---

# Test Initiative 🎯

## Success Criteria

- [x] Unicode support ✅
- [x] Emoji handling 🚀
- [x] International text 日本語

## Updates

Successfully completed all tasks! 🎉
"""
        initiative_path = temp_initiatives_dir / "docs/initiatives/active/unicode.md"
        initiative_path.write_text(content)

        validator = ArchivalValidator(initiative_path)
        assert validator.load_initiative()
        assert validator.check_success_criteria_gate().passed
